#!/usr/bin/env python3
"""Geste 5 de « créer son ontologie » : valider le brouillon, puis émettre ontologie.yaml et Ontologie.md.

Usage : rendre.py <ontologie.json> --sortie <dossier>
Refuse (sortie 1, rien d'écrit) tout brouillon qui viole une règle de la méthode :
plafond, combinaisons vers un type non déclaré (G2), moins de trois exemples pour un
élément retenu (G4), énumérations, noyau incomplet, question servie mais absente. Stdlib seule.
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ETATS = ("retenu", "par_reference", "flou", "absent")
VERDICTS = ("passe", "partiel", "par_reference", "trou", "a_jouer")
STATUTS = ("draft-IA", "approved")
PROVENANCES = ("lu", "dit", "deduit", "déduit")
NOYAU_TYPES = ("personne", "role", "equipe", "activite", "process", "outil")
NOYAU_VERBES = ("occupe", "repond_de", "sert", "tourne_sur", "precede")
PLAFOND_DEFAUT = 20
EXEMPLES_MIN = 3
SCALAIRE_SIMPLE = re.compile(r"^[A-Za-z0-9\u00C0-\u024F][^\n:#\[\]{},&*!|>'\"%@`]*$")
RESSEMBLE_A_UN_NOMBRE = re.compile(r"^[-+]?(\d[\d_ ]*([.,]\d+)?|\.\d+)([eE][-+]?\d+)?$")
MOTS_RESERVES = {"true", "false", "yes", "no", "on", "off", "null", "~", "y", "n"}
ANNOTATION = re.compile(r"\([^)]*\)")


def valider(data: dict) -> list[str]:
    erreurs: list[str] = []
    onto = data.get("ontologie") or {}
    if onto.get("statut") not in STATUTS:
        erreurs.append(f"statut : « {onto.get('statut')} » n'est pas dans {list(STATUTS)}")
    plafond = onto.get("plafond") or {}
    p_types = int(plafond.get("types", PLAFOND_DEFAUT))
    p_verbes = int(plafond.get("verbes", PLAFOND_DEFAUT))
    types = data.get("types") or []
    verbes = data.get("verbes") or []
    questions = data.get("questions") or []

    if len(types) > p_types:
        erreurs.append(f"plafond : {len(types)} types pour un plafond de {p_types}, fusionne avant d'émettre")
    if len(verbes) > p_verbes:
        erreurs.append(f"plafond : {len(verbes)} verbes pour un plafond de {p_verbes}, fusionne avant d'émettre")

    cles_types = [t.get("cle") for t in types]
    for cle, n in Counter(cles_types).items():
        if n > 1:
            erreurs.append(f"type en double : {cle}")
    for cle in NOYAU_TYPES:
        if cle not in cles_types:
            erreurs.append(f"noyau : le type {cle} manque (le noyau reste présent, à l'état absent s'il le faut)")
    cles_verbes = [v.get("cle") for v in verbes]
    for cle in NOYAU_VERBES:
        if cle not in cles_verbes:
            erreurs.append(f"noyau : le verbe {cle} manque (le noyau reste présent, à l'état absent s'il le faut)")

    vocabulaire = set(cles_types) | {v.get("cle") for v in verbes}
    ids_questions = {q.get("id") for q in questions}
    for q in questions:
        for etape in q.get("chemin") or []:
            for mot in _mots_du_chemin(etape):
                if mot not in vocabulaire:
                    erreurs.append(
                        f"question {q.get('id')} : le chemin cite « {mot} », qui n'est ni un type ni un verbe déclaré "
                        f"(déclare-le, ou écris « ⚠ manque: {mot} » pour le signaler)"
                    )
        if q.get("verdict") not in VERDICTS:
            erreurs.append(f"question {q.get('id')} : verdict « {q.get('verdict')} » n'est pas dans {list(VERDICTS)}")
        elif q["verdict"] in ("passe", "partiel", "par_reference") and not q.get("preuve"):
            erreurs.append(f"question {q.get('id')} : verdict {q['verdict']} sans preuve (instance réelle et notes sources)")

    for t in types:
        cle = t.get("cle", "?")
        if t.get("etat") not in ETATS:
            erreurs.append(f"type {cle} : etat « {t.get('etat')} » n'est pas dans {list(ETATS)}")
        if t.get("etat") == "retenu":
            exemples = [e for e in (t.get("exemples") or []) if e.get("nom") and e.get("source")]
            if len(exemples) < EXEMPLES_MIN:
                erreurs.append(f"G4 : le type {cle} est retenu avec {len(exemples)} exemple(s), il en faut {EXEMPLES_MIN} avec leur note source")
        _verifier_provenance(t, f"type {cle}", erreurs)
        _verifier_sert(t, f"type {cle}", ids_questions, erreurs)

    for v in verbes:
        cle = v.get("cle", "?")
        if v.get("etat") not in ETATS:
            erreurs.append(f"verbe {cle} : etat « {v.get('etat')} » n'est pas dans {list(ETATS)}")
        combinaisons = v.get("combinaisons") or []
        if not combinaisons:
            erreurs.append(f"G2 : le verbe {cle} n'a aucune combinaison déclarée (type source → type cible)")
        for c in combinaisons:
            for bout in ("source", "cible"):
                if c.get(bout) not in cles_types:
                    erreurs.append(f"G2 : le verbe {cle} relie {c.get('source')} → {c.get('cible')}, type inconnu « {c.get(bout)} » : déclare le type ou refuse la relation")
        if v.get("etat") == "retenu":
            exemples = [e for e in (v.get("exemples") or []) if e.get("note")]
            if len(exemples) < EXEMPLES_MIN:
                erreurs.append(f"G4 : le verbe {cle} est retenu avec {len(exemples)} exemple(s), il en faut {EXEMPLES_MIN} avec leur note source")
        _verifier_provenance(v, f"verbe {cle}", erreurs)
        _verifier_sert(v, f"verbe {cle}", ids_questions, erreurs)
    return erreurs


def _mots_du_chemin(etape) -> list[str]:
    """Les mots de vocabulaire d'une étape de chemin.

    Une étape s'annote comme on la lit au tableau : « occupe (dates) », « repond_de⁻¹ (A) »
    pour le sens inverse, « ¬ repond_de⁻¹ (R) » pour une absence, « a | b » pour une
    alternative, « champ tutoiement » pour un attribut, « ⚠ manque: x » pour un trou assumé.
    Seul ce qui prétend être un type ou un verbe est contrôlé.
    """
    texte = str(etape).strip()
    if "⚠" in texte or texte.lower().startswith("champ "):
        return []
    texte = ANNOTATION.sub("", texte)
    mots = []
    for morceau in texte.split("|"):
        mot = morceau.strip().lstrip("¬").strip().rstrip("\u207b\u00b9").strip()
        if mot:
            mots.append(mot)
    return mots


def _verifier_provenance(element: dict, nom: str, erreurs: list[str]) -> None:
    provenance = str(element.get("provenance", ""))
    if not provenance.startswith(PROVENANCES):
        erreurs.append(f"{nom} : provenance « {provenance} » doit commencer par lu, dit ou deduit")


def _verifier_sert(element: dict, nom: str, ids: set, erreurs: list[str]) -> None:
    for q in element.get("sert") or []:
        if q not in ids:
            erreurs.append(f"{nom} : sert la question {q}, qui n'est pas déclarée dans questions")


def structure_emise(data: dict) -> dict:
    onto = dict(data.get("ontologie") or {})
    onto["compte"] = {"types": len(data.get("types") or []), "verbes": len(data.get("verbes") or [])}
    score = Counter(q.get("verdict") for q in data.get("questions") or [])
    sortie = {"ontologie": onto, "types": data.get("types") or [], "verbes": data.get("verbes") or [],
              "questions": data.get("questions") or [], "score": dict(score)}
    for cle in ("trous", "contradictions", "candidats_refuses", "decisions", "a_trancher_au_tableau"):
        sortie[cle] = data.get(cle) or []
    return sortie


def emettre_yaml(data: dict) -> str:
    entete = [
        "# Ontologie émise par le skill creer-son-ontologie (geste 5). Source de vérité du modèle.",
        "# etat : retenu | par_reference | flou | absent · verdict : passe | partiel | par_reference | trou | a_jouer",
        "# Rien ne se dérive d'un draft-IA : le statut passe à approved après l'atelier au tableau.",
        "",
    ]
    return "\n".join(entete + _yaml(structure_emise(data), 0)) + "\n"


def _yaml(valeur, indent: int) -> list[str]:
    pad = " " * indent
    lignes: list[str] = []
    if isinstance(valeur, dict):
        for cle, v in valeur.items():
            if isinstance(v, dict) and v:
                lignes.append(f"{pad}{cle}:")
                lignes += _yaml(v, indent + 2)
            elif isinstance(v, list) and v:
                lignes.append(f"{pad}{cle}:")
                lignes += _yaml(v, indent)
            elif isinstance(v, (dict, list)):
                lignes.append(f"{pad}{cle}: {'{}' if isinstance(v, dict) else '[]'}")
            else:
                lignes.append(f"{pad}{cle}: {_scalaire(v)}")
    elif isinstance(valeur, list):
        for element in valeur:
            if isinstance(element, dict):
                sous = _yaml(element, indent + 2)
                if sous:
                    sous[0] = f"{pad}- {sous[0][indent + 2:]}"
                    lignes += sous
                else:
                    lignes.append(f"{pad}- {{}}")
            elif isinstance(element, list):
                lignes.append(f"{pad}- [{', '.join(_scalaire(e) for e in element)}]")
            else:
                lignes.append(f"{pad}- {_scalaire(element)}")
    return lignes


def _scalaire(v) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    if (not s or s != s.strip() or not SCALAIRE_SIMPLE.match(s) or s.endswith(":")
            or s.lower() in MOTS_RESERVES or RESSEMBLE_A_UN_NOMBRE.match(s) or " #" in s or ": " in s):
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'
    return s


def rendre_note(data: dict) -> str:
    onto = data.get("ontologie") or {}
    types = data.get("types") or []
    verbes = data.get("verbes") or []
    questions = data.get("questions") or []
    plafond = onto.get("plafond") or {}
    score = Counter(q.get("verdict") for q in questions)
    libelle = {t["cle"]: t.get("libelle", t["cle"]) for t in types}

    l = ["---", "type: deliverable", f"status: {onto.get('statut', 'draft-IA')}", f"version: {onto.get('version', '0.1.0')}",
         f"created: {onto.get('date', '')}", "source_yaml: ontologie.yaml", "tags: [ontologie, draft-ia]", "---", "",
         f"# Ontologie de {onto.get('organisation', '?')} (brouillon)", "",
         f"Rendu lisible de `ontologie.yaml`, source de vérité du modèle. Statut `{onto.get('statut', 'draft-IA')}`, "
         f"émis le {onto.get('date', '?')} depuis {', '.join(onto.get('cerveaux') or [])}. "
         f"Rien ne se dérive d'un brouillon : le dirigeant tranche au tableau, puis le statut passe à `approved`.", "",
         f"**{len(types)} types et {len(verbes)} verbes**, pour un plafond de {plafond.get('types', PLAFOND_DEFAUT)} et {plafond.get('verbes', PLAFOND_DEFAUT)}.", ""]

    l += ["## Les types", "", "| Type | Noyau | État | Instances | Cerveau | Questions servies |", "|---|---|---|---:|---|---|"]
    for t in types:
        l.append(f"| {t.get('libelle', t['cle'])} | {'oui' if t.get('noyau') else ''} | {t.get('etat', '')} | {t.get('instances', '')} | {t.get('cerveau', '')} | {', '.join(str(q) for q in t.get('sert') or [])} |")
    l.append("")
    for t in types:
        if t.get("etat") == "retenu" and t.get("exemples"):
            ex = " · ".join(f"{e.get('nom')} (`{e.get('source')}`)" for e in t["exemples"][:EXEMPLES_MIN])
            l.append(f"- **{t.get('libelle', t['cle'])}** : {t.get('definition', '')}. Exemples : {ex}")
        elif t.get("etat") != "retenu":
            motif = " ".join(x for x in (
                f"Vérité : {t['verite']}." if t.get("verite") else "",
                t.get("note", ""),
            ) if x)
            l.append(f"- **{t.get('libelle', t['cle'])}** ({t.get('etat')}) : {t.get('definition', '')}. {motif}".rstrip())
    l += ["", "## Les verbes", "", "| Verbe | De → vers | Porte | État | Questions |", "|---|---|---|---|---|"]
    for v in verbes:
        combos = " ; ".join(f"{libelle.get(c.get('source'), c.get('source'))} → {libelle.get(c.get('cible'), c.get('cible'))}" for c in v.get("combinaisons") or [])
        porte = ", ".join(x for x in (
            ("rôles " + "/".join(r.get("role", "") for r in v.get("roles") or [])) if v.get("roles") else "",
            "dates" if v.get("porte_dates") else "",
            ", ".join(v.get("champs") or [])) if x)
        l.append(f"| {v.get('libelle', v['cle'])} | {combos} | {porte} | {v.get('etat', '')} | {', '.join(str(q) for q in v.get('sert') or [])} |")

    l += ["", "## La preuve : les questions jouées sur de vraies notes", "",
          "| # | Question | Chemin typé | Verdict | Preuve ou manque |", "|---|---|---|---|---|"]
    for q in questions:
        detail = q.get("manque") or q.get("preuve") or ""
        chemin = " → ".join(str(e) for e in q.get("chemin") or [])
        l.append(f"| {q.get('id')} | {q.get('question')} | {chemin} | {q.get('verdict')} | {detail} |")
    l += ["", "**Score :** " + ", ".join(f"{n} {v}" for v, n in score.items()) + "."]

    l += ["", "## Les trous", ""]
    trous = data.get("trous") or []
    l += [f"- {_ligne(t)}" for t in trous] or ["Aucun trou déclaré."]
    l += ["", "## Les contradictions", ""]
    contradictions = data.get("contradictions") or []
    l += [f"- **{c.get('sujet')}** : {c.get('a')} contre {c.get('b')}" + (f" ({', '.join(c.get('notes') or [])})" if c.get("notes") else "") for c in contradictions] or ["Aucune contradiction rencontrée."]

    l += ["", "## Décisions", ""]
    decisions = data.get("decisions") or []
    if decisions:
        l += ["Tranchées :", ""] + [f"- {d.get('date')}, {d.get('par')} : {d.get('sujet')}, {d.get('decision')}" for d in decisions] + [""]
    a_trancher = list(data.get("a_trancher_au_tableau") or [])
    a_trancher += [f"{e.get('libelle', e['cle'])} : {e['a_trancher']}"
                   for e in list(types) + list(verbes) if e.get("a_trancher")]
    l += ["À trancher au tableau :", ""] + ([f"{i}. {x}" for i, x in enumerate(a_trancher, 1)] or ["- rien en attente"])
    refuses = data.get("candidats_refuses") or []
    if refuses:
        l += ["", "## Candidats refusés", ""] + [f"- {r.get('candidat')} : {r.get('motif')}" for r in refuses]
    return "\n".join(l) + "\n"


def _ligne(t: dict) -> str:
    sujet = t.get("type") or t.get("verbe") or t.get("champ") or (f"question {t['question']}" if t.get("question") else "")
    parts = [f"**{sujet}**" if sujet else "", t.get("motif", ""), f"vérité : {t['verite']}" if t.get("verite") else ""]
    return " : ".join(p for p in parts[:2] if p) + (f" ({parts[2]})" if parts[2] else "")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Valide un brouillon d'ontologie et émet ontologie.yaml + Ontologie.md (geste 5).")
    parser.add_argument("entree", help="le ontologie.json de travail")
    parser.add_argument("--sortie", required=True, help="dossier de sortie (Cerveau Privé/4 TOOLS/ontologie/)")
    args = parser.parse_args(argv)
    entree = Path(args.entree).expanduser()
    try:
        data = json.loads(entree.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"REFUS : impossible de lire {entree} ({exc})", file=sys.stderr)
        return 1
    erreurs = valider(data)
    if erreurs:
        for e in erreurs:
            print(f"REFUS : {e}", file=sys.stderr)
        print(f"{len(erreurs)} règle(s) violée(s), rien n'a été écrit.", file=sys.stderr)
        return 1
    sortie = Path(args.sortie).expanduser()
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "ontologie.yaml").write_text(emettre_yaml(data), encoding="utf-8")
    (sortie / "Ontologie.md").write_text(rendre_note(data), encoding="utf-8")
    compte = structure_emise(data)["ontologie"]["compte"]
    print(f"{compte['types']} types, {compte['verbes']} verbes, {len(data.get('questions') or [])} questions · {sortie / 'ontologie.yaml'} et {sortie / 'Ontologie.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
