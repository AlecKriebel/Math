#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
actual=$(python3 "$here/verify_boundary.py")
expected=$(tr -d '\n' < "$here/expected_result.json")

test "$actual" = "$expected"
grep -Fq '### Lemma 1.1 (tight-shell descent) — PROVED' "$here/NOTE.md"
grep -Fq '### Theorem 3.1 (rank-one anchor exit) — PROVED' "$here/NOTE.md"
grep -Fq '### Theorem 4.1 (two-fan target crossing) — PROVED' "$here/NOTE.md"

printf '%s\n' "PASS full-list rank rebound strict replay"
