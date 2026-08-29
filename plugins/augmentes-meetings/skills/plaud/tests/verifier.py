#!/usr/bin/env python3
"""Vérifie la page de correction générée par generer_page.py.

Usage : verifier.py [page.html] [fixture.json] [config.json]
Par défaut : tests/out/page.html, tests/fixtures/reunion-exemple.json,
tests/fixtures/config-exemple.json (chemins relatifs à ce script).

Contrôles : les deux placeholders du template ont disparu, le nom
d'entreprise de la config de test est présent, la mention « powered by »
est présente, aucune chaîne interdite (marque Marmites interne) ne fuite,
la réunion fixture apparaît (titre + ses actions), collectAll (export
JSON) est toujours défini dans le JS livré, et le logo de la config de
test est bien inliné en data URI (pas un chemin relatif cassé).
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Ce que le kit distribué ne doit jamais contenir : identité interne Marmites.
BANNED = ["M:armites", "AUGMENTÉS", "Le Prompt", "@marmites.com"]


def main() -> None:
    args = sys.argv[1:]
    page_path = Path(args[0]) if len(args) > 0 else HERE / "out" / "page.html"
    fixture_path = Path(args[1]) if len(args) > 1 else HERE / "fixtures" / "reunion-exemple.json"
    config_path = Path(args[2]) if len(args) > 2 else HERE / "fixtures" / "config-exemple.json"

    html = page_path.read_text(encoding="utf-8")
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    config = json.loads(config_path.read_text(encoding="utf-8"))

    reunion = fixture["reunions"][0]
    entreprise_nom = config["entreprise"]["nom"]

    n = 0
    failures = []

    def verif(cond: bool, label: str) -> None:
        nonlocal n
        n += 1
        if not cond:
            failures.append(label)

    verif("/*__KIT_CONFIG__*/" not in html, "placeholder /*__KIT_CONFIG__*/ toujours présent")
    verif("/*__PLAUD_DATA__*/" not in html, "placeholder /*__PLAUD_DATA__*/ toujours présent")
    verif(entreprise_nom in html, f"nom d'entreprise « {entreprise_nom} » absent")
    verif("powered by" in html, "mention « powered by » absente")

    for banned in BANNED:
        verif(banned not in html, f"chaîne interdite présente : {banned}")

    verif(reunion["titre"] in html, f"titre de la réunion fixture absent : {reunion['titre']}")
    for action in reunion["actions"]:
        verif(action["texte"] in html, f"action fixture absente : {action['texte']}")

    verif("collectAll" in html, "fonction collectAll absente")
    verif("data:image/png;base64," in html, "logo non inliné en data URI")

    if failures:
        for f in failures:
            print(f"ÉCHEC : {f}")
        sys.exit(1)

    print(f"OK {n} vérifications")


if __name__ == "__main__":
    main()
