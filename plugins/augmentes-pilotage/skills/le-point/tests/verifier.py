"""Vérifie que le triage traite correctement les 8 cas piégés du jeu de test."""
import json, sys
from pathlib import Path

t = json.loads((Path(sys.argv[1]) / "triage.json").read_text(encoding="utf-8"))
attente = {c["expediteur"] for c in t["fils"] if c["en_attente"]}
gardes = {c["expediteur"] for c in t["fils"]}

CAS = [
    ("paul.martin@monclient.fr" in gardes and "paul.martin@monclient.fr" not in attente,
     "réponse hors du fil reconnue"),
    ("julie.bernard@monclient.fr" not in attente, "réponse dans le fil reconnue"),
    ("security-noreply@grosseboite.com" not in gardes, "noreply préfixé filtré"),
    ("support@exemple.fr" not in gardes, "automatisme maison filtré"),
    ("notifications@linkedin.com" not in gardes, "plateforme filtrée"),
    ("contact@mon-expert-comptable.fr" in gardes, "boîte générique d'un proche gardée"),
    ("eric@laboutique.fr" not in gardes, "publicité filtrée"),
    ("marie.dupont@monclient.fr" in attente, "vrai silence détecté"),
]
echecs = [m for ok, m in CAS if not ok]
for ok, m in CAS:
    print(f"  {'OK  ' if ok else 'ÉCHEC'} {m}")
if echecs:
    sys.exit(f"{len(echecs)} cas en échec")
