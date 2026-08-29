#!/usr/bin/env bash
# test_check_ingested.sh
# Test check_ingested.sh script with a temp vault
set -euo pipefail

# Create temp vault with test notes
tmpvault=$(mktemp -d)
trap "rm -rf '$tmpvault'" EXIT

# Note 1: exact match abc123
cat > "$tmpvault/note1.md" << 'EOF'
---
type: source
subtype: plaud
plaud_id: abc123
date: 2026-07-24
---
# Note 1
Content here.
EOF

# Note 2: prefix case - abc1234 (should NOT match query abc123)
cat > "$tmpvault/note2.md" << 'EOF'
---
type: source
subtype: plaud
plaud_id: abc1234
date: 2026-07-24
---
# Note 2
Content here.
EOF

# Note 3: quoted form def456
cat > "$tmpvault/note3.md" << 'EOF'
---
type: source
subtype: plaud
plaud_id: "def456"
date: 2026-07-24
---
# Note 3
Content here.
EOF

# Test 1: Basic exact match + non-match
output=$("$(dirname "$0")/../scripts/check_ingested.sh" "$tmpvault" abc123 zzz999)
expected="abc123"
if [ "$output" != "$expected" ]; then
  echo "FAIL Test 1: expected '$expected', got '$output'"
  exit 1
fi

# Test 2: Prefix case - abc123 should NOT match abc1234
output=$("$(dirname "$0")/../scripts/check_ingested.sh" "$tmpvault" abc123)
expected="abc123"
if [ "$output" != "$expected" ]; then
  echo "FAIL Test 2 (prefix): expected '$expected', got '$output'"
  exit 1
fi

# Test 3: Quoted form
output=$("$(dirname "$0")/../scripts/check_ingested.sh" "$tmpvault" def456)
expected="def456"
if [ "$output" != "$expected" ]; then
  echo "FAIL Test 3 (quoted): expected '$expected', got '$output'"
  exit 1
fi

# Test 4: Path with spaces
tmpvault_space=$(mktemp -d "/tmp/test vault XXXXXX")
trap "rm -rf '$tmpvault' '$tmpvault_space'" EXIT
cat > "$tmpvault_space/note.md" << 'EOF'
---
plaud_id: space123
---
Content
EOF
output=$("$(dirname "$0")/../scripts/check_ingested.sh" "$tmpvault_space" space123)
expected="space123"
if [ "$output" != "$expected" ]; then
  echo "FAIL Test 4 (spaces): expected '$expected', got '$output'"
  exit 1
fi

echo "OK"
exit 0
