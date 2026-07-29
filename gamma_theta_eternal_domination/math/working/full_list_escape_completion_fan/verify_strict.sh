#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
actual=$(mktemp "${TMPDIR:-/tmp}/full-list-escape-fan.XXXXXX")
trap 'rm -f "$actual"' EXIT HUP INT TERM

python3 -I -B -W error "$here/verify_control.py" > "$actual"
cmp "$here/expected_result.json" "$actual"

python3 -I -B -W error - "$here" <<'PY'
import hashlib
import json
import pathlib
import sys

directory = pathlib.Path(sys.argv[1])
manifest = json.loads(
    (directory / "MANIFEST.json").read_text(encoding="utf-8")
)
for name, expected in manifest["candidate_hashes"].items():
    actual = hashlib.sha256((directory / name).read_bytes()).hexdigest()
    assert actual == expected, (name, expected, actual)
PY

grep -Fq 'Theorem 2.1 (completion fans and rank rebound) — PROVED' \
  "$here/NOTE.md"
grep -Fq 'C_{qw}\subseteq N_G[t]' "$here/NOTE.md"
grep -Fq 'Lemma 2.1 (Johnson-distance rank floor) — PROVED' "$here/NOTE.md"
grep -Fq 'Corollary 2.2 (minimum-rank fan exit) — PROVED' "$here/NOTE.md"
grep -Fq 'reciprocal two-state hinge' "$here/NOTE.md"
grep -Fq 'reciprocal four-state square' "$here/NOTE.md"
grep -Fq 'does **not** force a restricted kernel' "$here/NOTE.md"

actual_sha=$(shasum -a 256 "$actual" | awk '{print $1}')
expected_sha=$(shasum -a 256 "$here/expected_result.json" | awk '{print $1}')
test "$actual_sha" = "$expected_sha"
echo "PASS full-list escape completion fan strict replay $actual_sha"
