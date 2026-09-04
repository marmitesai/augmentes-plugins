#!/usr/bin/env python3
"""Geste 1 de « créer son ontologie » : compter le vault avant de le lire.

Usage : inventaire.py <workspace | dossier Cerveaux | un cerveau> --sortie <dossier>
Écrit inventaire.json et inventaire.md. Stdlib seule. Sortie 2 si aucun cerveau n'est trouvé.
"""

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

DOSSIER_IPCRA = re.compile(r"^\d ")
# Un dossier de sauvegarde s'exclut ; un projet qui PARLE de sauvegarde se compte.
# « Backup et gestion centralisée Forti » est un chantier client, pas une copie.
SEGMENT_EXCLU = re.compile(
    r"^(\..+|logs?|node_modules|__pycache__|backups?|sauvegardes?|"
    r"[\w.-]*[-_](backup|scrub|bak)[\w.-]*|[\w.-]*scrub[\w.-]*)$",
    re.IGNORECASE,
)
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
SEPARATEUR_TABLE = re.compile(r"^\|?\s*:?-{3,}")
CLES_GENERIQUES = {"type", "tags", "created", "updated", "aliases", "title"}
SYNONYMES = {
    "quand": {"date", "date_decision", "decision_date", "target_decision_date", "decided_on"},
    "qui": {"auteur", "author", "owner", "deciders", "decideurs", "decided_by"},
    "source": {"source", "sources"},
    "statut": {"status", "statut", "etat", "state"},
}
# On reconnait un identifiant a la FORME de sa cle, jamais au nom d'un logiciel :
# « odoo_raw_name » est un libelle et « odoo » un drapeau, ni l'un ni l'autre une cle.
IDENTIFIANT_EXTERNE = re.compile(
    r"(^id$|_id$|^id_|^uid$|^uuid$|^guid$|^eid$|^siren$|^siret$|^tva$|"
    r"num[eé]ro|^num_|_num$|^ref_|_ref$|^code_|_code$|^matricule)",
    re.IGNORECASE,
)
SEUIL_REGIME = 100
NOTES_MIN_GISEMENT = 5
CLES_MIN_GISEMENT = 3
LIGNES_MIN_TABLE = 20
# Un nom qui est une date ou une pièce de structure n'est pas une entité homonyme.
NOM_NON_ENTITE = re.compile(
    r"^(\d{4}-\d{2}(-\d{2})?|\d{4}-W\d{2}|_?index|readme|agents|claude|overview|skill|config|_.*)$",
    re.IGNORECASE,
)


def nfc(texte: str) -> str:
    return unicodedata.normalize("NFC", texte)


def cle_de(nom: str) -> str:
    return nfc(nom).casefold().strip()


def est_exclu(relatif: Path) -> str | None:
    """Rend le préfixe exclu (jusqu'au segment fautif) ou None."""
    for i, segment in enumerate(relatif.parts):
        if SEGMENT_EXCLU.match(segment):
            return "/".join(relatif.parts[: i + 1])
    return None


def lire_frontmatter(texte: str) -> tuple[dict, str]:
    """Lit le sous-ensemble YAML des notes : clé: valeur, [a, b], et listes en bloc."""
    if not texte.startswith("---"):
        return {}, texte
    lignes = texte.split("\n")
    fin = next((i for i in range(1, len(lignes)) if lignes[i].strip() == "---"), None)
    if fin is None:
        return {}, texte
    fm: dict = {}
    cle_courante = None
    for ligne in lignes[1:fin]:
        if not ligne.strip() or ligne.lstrip().startswith("#"):
            continue
        if ligne.startswith((" ", "\t")):
            if cle_courante is not None and ligne.strip().startswith("- ") and isinstance(fm.get(cle_courante), list):
                fm[cle_courante].append(_scalaire(ligne.strip()[2:]))
            continue
        if ligne.startswith("- ") and cle_courante is not None and isinstance(fm.get(cle_courante), list):
            fm[cle_courante].append(_scalaire(ligne[2:]))
            continue
        if ":" not in ligne:
            continue
        cle, _, valeur = ligne.partition(":")
        cle = nfc(cle.strip())
        valeur = valeur.strip()
        cle_courante = cle
        if valeur == "":
            fm[cle] = []
        elif valeur.startswith("[") and valeur.endswith("]"):
            fm[cle] = [_scalaire(v) for v in _decouper_liste(valeur[1:-1])]
        else:
            fm[cle] = _scalaire(valeur)
    return fm, "\n".join(lignes[fin + 1 :])


def _decouper_liste(contenu: str) -> list[str]:
    morceaux, courant, guillemet = [], "", None
    for c in contenu:
        if guillemet:
            courant += c
            if c == guillemet:
                guillemet = None
        elif c in "\"'":
            guillemet = c
            courant += c
        elif c == ",":
            morceaux.append(courant)
            courant = ""
        else:
            courant += c
    if courant.strip():
        morceaux.append(courant)
    return [m for m in morceaux if m.strip()]


def _scalaire(valeur: str) -> str:
    valeur = valeur.strip()
    if len(valeur) >= 2 and valeur[0] == valeur[-1] and valeur[0] in "\"'":
        valeur = valeur[1:-1]
    return nfc(valeur)


def tables_de(corps: str) -> list[dict]:
    tables, bloc = [], []
    for ligne in corps.split("\n") + [""]:
        if ligne.lstrip().startswith("|"):
            bloc.append(ligne.strip())
            continue
        if len(bloc) >= 3 and SEPARATEUR_TABLE.match(bloc[1]):
            colonnes = [c.strip() for c in bloc[0].strip("|").split("|")]
            tables.append({"colonnes": colonnes, "lignes": len(bloc) - 2})
        bloc = []
    return tables


def decouvrir_cerveaux(racine: Path) -> tuple[Path, list[Path]]:
    racine = racine.resolve()
    if racine.name == "Cerveaux":
        base = racine
    elif (racine / "Cerveaux").is_dir():
        base = racine / "Cerveaux"
    elif any(DOSSIER_IPCRA.match(nfc(p.name)) for p in racine.iterdir() if p.is_dir()):
        return racine.parent, [racine]
    else:
        return racine, []
    cerveaux = []
    for p in base.iterdir():
        if not p.is_dir() or SEGMENT_EXCLU.match(p.name):
            continue
        ipcra = any(DOSSIER_IPCRA.match(nfc(s.name)) for s in p.iterdir() if s.is_dir())
        if ipcra or (p / "AGENTS.md").exists():
            cerveaux.append(p)
    cerveaux.sort(key=lambda p: (0 if "priv" in cle_de(p.name) else 1, cle_de(p.name)))
    return base, cerveaux


def inventorier(racine: Path) -> dict:
    base, cerveaux = decouvrir_cerveaux(Path(racine))
    notes: list[dict] = []
    exclus: set[str] = set()
    resultats_cerveaux = []

    cadrage: list[dict] = []
    for cerveau in cerveaux:
        nom = nfc(cerveau.name)
        for doc in sorted(cerveau.glob("*.md")):
            try:
                contenu = doc.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            cadrage.append({"cerveau": nom, "chemin": f"{nom}/{nfc(doc.name)}", "mots": len(contenu.split())})
        par_dossier: Counter = Counter()
        par_sous_dossier: Counter = Counter()
        nb = 0
        for fichier in cerveau.rglob("*.md"):
            relatif = fichier.relative_to(cerveau)
            if len(relatif.parts) == 1:
                continue  # AGENTS.md, CLAUDE.md : la doc du cerveau, pas une note
            exclu = est_exclu(relatif.parent)
            if exclu:
                exclus.add(f"{nom}/{nfc(exclu)}")
                continue
            try:
                texte = fichier.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            fm, corps = lire_frontmatter(texte)
            premier = nfc(relatif.parts[0])
            par_dossier[premier] += 1
            if len(relatif.parts) > 2:
                par_sous_dossier[f"{premier}/{nfc(relatif.parts[1])}"] += 1
            notes.append({
                "cerveau": nom,
                "chemin": f"{nom}/{nfc(str(relatif))}",
                "dossier": f"{nom}/{nfc(str(relatif.parent))}",
                "nom": nfc(fichier.stem),
                "frontmatter": fm,
                "liens": [nfc(m.split("/")[-1].strip()) for m in WIKILINK.findall(corps + "\n" + texte[: len(texte) - len(corps)])],
                "tables": tables_de(corps),
            })
            nb += 1
        resultats_cerveaux.append({
            "nom": nom,
            "chemin": str(cerveau),
            "notes": nb,
            "par_dossier": dict(sorted(par_dossier.items())),
            "par_sous_dossier": dict(sorted(par_sous_dossier.items())),
        })

    inv = {
        "racine": str(base),
        "cerveaux": resultats_cerveaux,
        "cadrage": cadrage,
        "total_notes": len(notes),
        "regime": "petit" if len(notes) < SEUIL_REGIME else "gros",
        "exclus": sorted(exclus),
    }
    inv.update(_frontmatters(notes))
    inv.update(_graphe(notes))
    inv.update(_gisements(notes))
    return inv


def _frontmatters(notes: list[dict]) -> dict:
    cles: Counter = Counter()
    valeurs = {"type": Counter(), "subtype": Counter(), "status": Counter(), "tags": Counter()}
    identifiants: dict[str, Counter] = defaultdict(Counter)
    avec_fm = 0
    for n in notes:
        fm = n["frontmatter"]
        if fm:
            avec_fm += 1
        for cle, valeur in fm.items():
            cles[cle] += 1
            if cle in valeurs:
                for v in (valeur if isinstance(valeur, list) else [valeur]):
                    if str(v):
                        valeurs[cle][str(v)] += 1
            if IDENTIFIANT_EXTERNE.search(cle):
                identifiants[cle][n["dossier"]] += 1
    normalisees = {}
    for canon, brutes in SYNONYMES.items():
        presentes = {c: cles[c] for c in brutes if cles.get(c)}
        normalisees[canon] = {"total": sum(presentes.values()), "brutes": presentes}
    return {
        "notes_avec_frontmatter": avec_fm,
        "cles": dict(cles.most_common(40)),
        "cles_normalisees": normalisees,
        "valeurs": {k: dict(v.most_common(30)) for k, v in valeurs.items()},
        "identifiants_externes": [
            {"cle": cle, "total": sum(c.values()), "dossiers": dict(c.most_common(5))}
            for cle, c in sorted(identifiants.items(), key=lambda kv: -sum(kv[1].values()))
        ],
    }


def _graphe(notes: list[dict]) -> dict:
    index: dict[str, dict] = {}
    doublons: dict[str, set] = defaultdict(set)
    for n in notes:
        k = cle_de(n["nom"])
        doublons[k].add(n["cerveau"])
        index.setdefault(k, n)
    alias_vers: dict[str, str] = {}
    for n in notes:
        aliases = n["frontmatter"].get("aliases", [])
        for a in (aliases if isinstance(aliases, list) else [aliases]):
            if a and cle_de(str(a)) not in index:
                alias_vers.setdefault(cle_de(str(a)), cle_de(n["nom"]))

    entrants: Counter = Counter()
    morts: Counter = Counter()
    par_alias: Counter = Counter()
    par_casse: Counter = Counter()
    for n in notes:
        for cible in n["liens"]:
            k = cle_de(cible)
            if k in index:
                entrants[k] += 1
                if cible != index[k]["nom"]:
                    par_casse[cible] += 1
            elif k in alias_vers:
                entrants[alias_vers[k]] += 1
                par_alias[cible] += 1
            else:
                morts[cible] += 1

    hubs = [
        {"nom": index[k]["nom"], "liens": c, "cerveau": index[k]["cerveau"], "chemin": index[k]["chemin"]}
        for k, c in entrants.most_common(40)
    ]
    orphelines = [n["nom"] for n in notes if cle_de(n["nom"]) not in entrants and not n["nom"].startswith("_")]
    return {
        "wikilinks": sum(len(n["liens"]) for n in notes),
        "hubs": hubs,
        "orphelines": len(orphelines),
        "orphelines_exemples": orphelines[:20],
        "liens_morts": dict(morts.most_common(60)),
        "liens_resolus_par_alias": dict(par_alias.most_common(30)),
        "liens_resolus_par_casse": dict(par_casse.most_common(30)),
        "doublons_inter_cerveaux": sorted(
            index[k]["nom"] for k, c in doublons.items()
            if len(c) > 1 and not NOM_NON_ENTITE.match(index[k]["nom"])
        ),
    }


def _gisements(notes: list[dict]) -> dict:
    par_dossier: dict[str, list[dict]] = defaultdict(list)
    for n in notes:
        par_dossier[n["dossier"]].append(n)
    gisements = []
    for dossier, groupe in par_dossier.items():
        if len(groupe) < NOTES_MIN_GISEMENT:
            continue
        compte: Counter = Counter()
        types: Counter = Counter()
        for n in groupe:
            for cle in n["frontmatter"]:
                if cle not in CLES_GENERIQUES:
                    compte[cle] += 1
            types[str(n["frontmatter"].get("type", ""))] += 1
        communes = sorted(c for c, k in compte.items() if k >= 0.8 * len(groupe))
        if len(communes) >= CLES_MIN_GISEMENT:
            gisements.append({"dossier": dossier, "notes": len(groupe), "cles_communes": communes, "types": dict(types.most_common(3))})
    gisements.sort(key=lambda g: -g["notes"])
    # On agrège par note : une matrice découpée en douze blocs de huit lignes est un
    # gisement, même si aucun bloc ne franchit le seuil tout seul.
    tables = []
    for n in notes:
        if not n["tables"]:
            continue
        total = sum(t["lignes"] for t in n["tables"])
        if total < LIGNES_MIN_TABLE:
            continue
        plus_grande = max(n["tables"], key=lambda t: t["lignes"])
        tables.append({
            "note": n["chemin"],
            "lignes": total,
            "tables": len(n["tables"]),
            "plus_grande": plus_grande["lignes"],
            "colonnes": plus_grande["colonnes"],
            "type": str(n["frontmatter"].get("type", "")),
        })
    tables.sort(key=lambda t: -t["lignes"])
    return {"gisements": gisements, "tables_internes": tables}


def rendre_markdown(inv: dict) -> str:
    l = ["# Inventaire du second cerveau", ""]
    l.append(f"Racine : `{inv['racine']}` · {inv['total_notes']} notes · régime **{inv['regime']}** · {inv['wikilinks']} wikilinks · {inv['notes_avec_frontmatter']} notes avec frontmatter.")
    if inv["exclus"]:
        l.append("")
        l.append("Exclus des comptages (logs, sauvegardes) : " + ", ".join(f"`{e}`" for e in inv["exclus"]))
    l += ["", "## Les cerveaux", "", "| Cerveau | Notes | Par dossier |", "|---|---:|---|"]
    for c in inv["cerveaux"]:
        detail = ", ".join(f"{d} {n}" for d, n in c["par_dossier"].items())
        l.append(f"| {c['nom']} | {c['notes']} | {detail} |")
    if inv["cadrage"]:
        l += ["", "## Les documents de cadrage", "",
              "Ils ne comptent pas comme notes, et ce sont pourtant les premiers à lire : sur un cerveau neuf, ils portent l'essentiel de ce qui est écrit.", ""]
        l += [f"- `{d['chemin']}` : {d['mots']} mots" for d in inv["cadrage"]]
    l += ["", "## Le vocabulaire des frontmatters", ""]
    for cle in ("type", "subtype", "status"):
        top = ", ".join(f"{v} {n}" for v, n in list(inv["valeurs"][cle].items())[:15])
        l.append(f"- `{cle}` : {top or 'aucune valeur'}")
    l.append("- clés synonymes : " + " ; ".join(
        f"{canon} = {d['total']} ({', '.join(d['brutes'])})" for canon, d in inv["cles_normalisees"].items() if d["total"]) )
    if inv["identifiants_externes"]:
        l.append("- identifiants externes : " + ", ".join(f"`{i['cle']}` {i['total']}" for i in inv["identifiants_externes"][:8]))
    l += ["", "## Le graphe", "", f"{inv['orphelines']} orphelines · {sum(inv['liens_morts'].values())} liens morts · {sum(inv['liens_resolus_par_alias'].values())} liens résolus par alias · {sum(inv['liens_resolus_par_casse'].values())} par la casse.", "", "| Hub | Liens | Cerveau |", "|---|---:|---|"]
    for h in inv["hubs"][:25]:
        l.append(f"| {h['nom']} | {h['liens']} | {h['cerveau']} |")
    if inv["liens_morts"]:
        l += ["", "Liens morts les plus fréquents : " + ", ".join(f"{k} ({v})" for k, v in list(inv["liens_morts"].items())[:15])]
    if inv["doublons_inter_cerveaux"]:
        l += ["", "Doublons inter-cerveaux (même nom, deux cerveaux) : " + ", ".join(inv["doublons_inter_cerveaux"][:20])]
    l += ["", "## Les gisements (tables qui s'ignorent)", ""]
    if not inv["gisements"] and not inv["tables_internes"]:
        l.append("Aucun gisement : le cerveau est encore trop jeune pour porter des colonnes répétées. Régime petit : lire les notes, interroger le dirigeant.")
    for g in inv["gisements"][:15]:
        l.append(f"- `{g['dossier']}` : {g['notes']} notes, colonnes communes {', '.join(g['cles_communes'][:8])}")
    for t in inv["tables_internes"][:10]:
        bloc = f", en {t['tables']} tables" if t["tables"] > 1 else ""
        l.append(f"- table interne dans `{t['note']}` : {t['lignes']} lignes{bloc}, colonnes {', '.join(t['colonnes'][:6])}")
    return "\n".join(l) + "\n"


def ecrire(inv: dict, sortie: Path) -> None:
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "inventaire.json").write_text(json.dumps(inv, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (sortie / "inventaire.md").write_text(rendre_markdown(inv), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compte un second cerveau avant de le lire (geste 1).")
    parser.add_argument("racine", help="le workspace, son dossier Cerveaux, ou un cerveau")
    parser.add_argument("--sortie", required=True, help="dossier où écrire inventaire.json et inventaire.md")
    args = parser.parse_args(argv)
    racine = Path(args.racine).expanduser()
    if not racine.is_dir():
        print(f"Dossier introuvable : {racine}", file=sys.stderr)
        return 2
    inv = inventorier(racine)
    if not inv["cerveaux"]:
        print(f"Aucun cerveau trouvé sous {racine} (attendu : Cerveaux/<nom>/ avec des dossiers IPCRA).", file=sys.stderr)
        return 2
    ecrire(inv, Path(args.sortie).expanduser())
    print(f"{inv['total_notes']} notes dans {len(inv['cerveaux'])} cerveau(x), régime {inv['regime']} · {Path(args.sortie) / 'inventaire.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
