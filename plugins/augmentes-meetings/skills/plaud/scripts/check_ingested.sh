#!/usr/bin/env bash
# check_ingested.sh <coffre> <plaud_id>...
# Imprime les ids déjà ingérés (présents en frontmatter plaud_id: d'un .md du coffre).
set -euo pipefail
coffre="$1"; shift
for id in "$@"; do
  if grep -rl --include='*.md' -m1 "^plaud_id: *\"*${id}\"*[[:space:]]*$" "$coffre" >/dev/null 2>&1; then
    echo "$id"
  fi
done
