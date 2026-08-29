"""
triage.py — sépare le signal du bruit dans une fenêtre de mails, et croise
les reçus contre les envoyés.

Aucune dépendance : bibliothèque standard Python uniquement. Aucun appel
réseau. Tout reste sur la machine.

Entrée : un dossier contenant inbox.json et sent.json au format normalisé
(voir SKILL.md, section « Le format d'échange »).
Sortie : triage.json, digest-signal.txt, digest-envois.txt dans le même dossier.

    python3 triage.py --dir ./fenetre --config ./config.json
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# Le bruit universel, celui qui ne dépend d'aucune entreprise.
# Non ancré : « mssecurity-noreply » et « sc-noreply » doivent tomber aussi.
NOREPLY = re.compile(
    r"(no-?reply|no_reply|nepasrepondre|ne-pas-repondre|donotreply|do-not-reply|"
    r"noresponse|bounce|postmaster|mailer-daemon)",
    re.I,
)
BOITE_GENERIQUE = re.compile(
    r"^(notifications?|alerts?|mailer|newsletters?|news|info|contact|hello|"
    r"bonjour|invoices?|billing|factures?|facturation|marketing|team|updates?|"
    r"support|admin|webmaster|abuse|privacy)$",
    re.I,
)
SOUS_DOMAINE_ENVOI = re.compile(
    r"(^|\.)(mail|email|e|m|news|notification|notifications|info|information|"
    r"reply|em|mg|sent-via|welcome|engage|creator|receipt|media|marketing)\.",
    re.I,
)
PLATEFORME = re.compile(
    r"(beehiiv|substack|mailchimp|sendgrid|hubspot|mailjet|brevo|sendinblue|"
    r"intercom|zendesk|atlassian\.net|circle\.so|skool|patreon|eventbrite|"
    r"linkedin|instagram|facebook|twitter|tiktok|youtube|meetup|doodle)",
    re.I,
)
SUJET_PUB = re.compile(
    r"(newsletter|se d[ée]sabonner|unsubscribe|webinar|webinaire|soldes|promo|"
    r"black friday|d[ée]couvrez nos|profitez de|derni[èe]re chance|"
    r"votre facture .* est disponible|subscription renewal|receipt from)",
    re.I,
)
# Un client sur une boîte grand public ne fait pas de son fournisseur d'accès
# un domaine proche. Sans ça, tout gmail deviendrait prioritaire.
GRAND_PUBLIC = {
    "gmail.com", "googlemail.com", "orange.fr", "wanadoo.fr", "free.fr", "sfr.fr",
    "neuf.fr", "laposte.net", "hotmail.com", "hotmail.fr", "outlook.com",
    "outlook.fr", "live.com", "live.fr", "yahoo.com", "yahoo.fr", "icloud.com",
    "me.com", "aol.com", "bbox.fr", "numericable.fr", "protonmail.com", "proton.me",
}
# Une vraie personne écrit depuis prenom.nom@, pas depuis service-client@.
HUMAIN = re.compile(r"^[a-zà-ÿ]+([.\-_][a-zà-ÿ]+)+@", re.I)


def domaine(adresse: str) -> str:
    return adresse.split("@")[-1].lower() if "@" in adresse else ""


class Filtre:
    def __init__(self, cfg: dict):
        self.interne = (cfg.get("mon_domaine") or "").lower()
        self.proches = {d.lower() for d in cfg.get("domaines_proches", []) if d}
        self.proches -= GRAND_PUBLIC
        self.proches.discard(self.interne)
        self.robots = {a.lower() for a in cfg.get("robots_internes", []) if a}
        motifs = [re.escape(s) for s in cfg.get("sujets_automatiques", []) if s]
        self.sujets_auto = re.compile(r"^\s*(" + "|".join(motifs) + ")", re.I) if motifs else None

    def est_bruit(self, m: dict) -> bool:
        exp = (m.get("expediteur") or "").lower()
        sujet = m.get("sujet") or ""
        if exp in self.robots:
            return True
        # Les automatismes maison partent de vraies boîtes d'équipe : seul le
        # sujet les trahit, il prime donc sur toute liste de domaines.
        if self.sujets_auto and self.sujets_auto.search(sujet):
            return True
        local, dom = exp.split("@")[0] if "@" in exp else exp, domaine(exp)
        if NOREPLY.search(local):
            return True
        # Passé ce point, un proche ou un interne ne peut pas être du bruit.
        if dom == self.interne or dom in self.proches:
            return False
        if PLATEFORME.search(dom) or SOUS_DOMAINE_ENVOI.search(dom):
            return True
        if BOITE_GENERIQUE.match(local):
            return True
        return bool(SUJET_PUB.search(sujet))

    def est_signal(self, m: dict, correspondants: set[str]) -> bool:
        exp = (m.get("expediteur") or "").lower()
        dom = domaine(exp)
        return bool(
            dom == self.interne
            or dom in self.proches
            or exp in correspondants
            or HUMAIN.match(exp)
        )


def _age_jours(iso: str | None) -> int:
    if not iso:
        return 0
    try:
        d = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - d).days
    except Exception:  # noqa: BLE001
        return 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="dossier contenant inbox.json et sent.json")
    ap.add_argument("--config", required=True)
    args = ap.parse_args()

    d = Path(args.dir)
    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    inbox = json.loads((d / "inbox.json").read_text(encoding="utf-8"))
    sent = json.loads((d / "sent.json").read_text(encoding="utf-8"))
    f = Filtre(cfg)
    seuil = int(cfg.get("seuil_jours", 2))

    # Toute personne à qui on a écrit sur la fenêtre est un correspondant connu.
    correspondants = {
        a.lower() for m in sent for a in (m.get("a", []) + m.get("copie", [])) if a
    }
    # Le croisement, c'est le cœur : par fil ET par destinataire. Une réponse
    # envoyée hors du fil compte quand même comme une réponse.
    fils_repondus = {m.get("fil") for m in sent if m.get("fil")}
    dernier_envoi_a: dict[str, str] = {}
    for m in sorted(sent, key=lambda x: x.get("date") or ""):
        for a in m.get("a", []):
            dernier_envoi_a[a.lower()] = m.get("date") or ""

    fils: dict[str, list[dict]] = defaultdict(list)
    stats = {"total": len(inbox), "bruit": 0, "signal": 0}
    for m in inbox:
        if f.est_bruit(m) or not f.est_signal(m, correspondants):
            stats["bruit"] += 1
            continue
        stats["signal"] += 1
        fils[m.get("fil") or m.get("id") or m.get("sujet") or ""].append(m)

    resultat = []
    for fid, msgs in fils.items():
        msgs.sort(key=lambda x: x.get("date") or "")
        dernier = msgs[-1]
        exp = (dernier.get("expediteur") or "").lower()
        repondu_fil = fid in fils_repondus
        repondu_hors = dernier_envoi_a.get(exp, "") > (dernier.get("date") or "")
        age = _age_jours(dernier.get("date"))
        resultat.append(
            {
                "fil": fid,
                "sujet": dernier.get("sujet"),
                "expediteur": exp,
                "nom": dernier.get("nom"),
                "domaine": domaine(exp),
                "proche": domaine(exp) in f.proches,
                "interne": domaine(exp) == f.interne,
                "date": dernier.get("date"),
                "age_jours": age,
                "nb_messages": len(msgs),
                "repondu_dans_le_fil": repondu_fil,
                "repondu_hors_fil": repondu_hors,
                "en_attente": not (repondu_fil or repondu_hors) and age >= seuil,
                "extrait": (dernier.get("extrait") or "")[:400],
            }
        )
    resultat.sort(key=lambda x: x.get("date") or "", reverse=True)

    (d / "triage.json").write_text(
        json.dumps({"stats": stats, "fils": resultat}, ensure_ascii=False, indent=1),
        encoding="utf-8",
    )

    with (d / "digest-signal.txt").open("w", encoding="utf-8") as fh:
        for c in resultat:
            etat = "EN ATTENTE" if c["en_attente"] else (
                "repondu" if (c["repondu_dans_le_fil"] or c["repondu_hors_fil"]) else "lu"
            )
            qui = "INTERNE" if c["interne"] else ("PROCHE" if c["proche"] else "EXTERNE")
            fh.write(
                f"\n=== [{etat}/{qui}] {(c['date'] or '')[:10]} (J+{c['age_jours']}) "
                f"| {c['nom']} <{c['expediteur']}> ({c['nb_messages']} msg)\n"
                f"SUJET: {c['sujet']}\n  {c['extrait']}\n"
            )

    with (d / "digest-envois.txt").open("w", encoding="utf-8") as fh:
        for m in sorted(sent, key=lambda x: x.get("date") or ""):
            fh.write(
                f"{(m.get('date') or '')[:16]} -> {','.join(m.get('a', []))[:70]}\n"
                f"   {m.get('sujet')}\n   {(m.get('extrait') or '')[:260]}\n"
            )

    print(
        json.dumps(
            {**stats, "fils": len(resultat),
             "en_attente": sum(1 for c in resultat if c["en_attente"])},
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
