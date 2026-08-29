#!/usr/bin/env bash
# Harnais de test de la recette Le Point. Relançable à volonté.
#   ./tests/lancer.sh
set -euo pipefail
cd "$(dirname "$0")/.."
TMP=$(mktemp -d)
cp tests/inbox.json tests/sent.json "$TMP/"
python3 scripts/triage.py --dir "$TMP" --config tests/config.json >/dev/null
python3 tests/verifier.py "$TMP"
python3 scripts/rapport.py --input tests/constat.json --output "$TMP/rapport.html" >/dev/null
python3 - "$TMP/rapport.html" <<'PY'
import sys,re
h=open(sys.argv[1],encoding="utf-8").read()
assert h.count('class="card" data-id')==2, "cartes manquantes"
assert 'cm-fab' in h and 'cm-copy' in h, "zone de correction absente"
assert 'recette M:armites.ai' in h, "signature absente"
assert 'http://' not in h.replace('http://www.w3.org',''), "appel réseau dans le rapport"
print("  OK   rapport HTML : 2 cartes, zone de correction, signature, zéro appel réseau")
PY
rm -rf "$TMP"
echo "Tout passe."
