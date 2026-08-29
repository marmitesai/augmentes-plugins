#!/usr/bin/env bash
# lancer.sh : harnais de test reproductible du kit-plaud.
# Enchaîne : test_check_ingested.sh -> génération de la page -> verifier.py
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "1/3 : check_ingested.sh"
bash "$HERE/test_check_ingested.sh"

echo "2/3 : génération de la page de correction"
python3 "$HERE/generer_page.py" \
  "$HERE/fixtures/reunion-exemple.json" \
  "$HERE/fixtures/config-exemple.json" \
  "$HERE/out/page.html"

echo "3/3 : vérification du contenu"
python3 "$HERE/verifier.py" \
  "$HERE/out/page.html" \
  "$HERE/fixtures/reunion-exemple.json" \
  "$HERE/fixtures/config-exemple.json"

echo "OK : harnais du kit-plaud au vert"
