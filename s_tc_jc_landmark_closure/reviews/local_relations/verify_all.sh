#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$HERE"

shasum -a 256 -c MANIFEST.sha256

gzip -t certificates/descriptor_bits.json.gz
gzip -t certificates/screen_candidates_n3.jsonl.gz
gzip -t certificates/equal_relations_n3.jsonl.gz
gzip -t certificates/strict_sign_workcache_n3.json.gz

test "$(jq -r '.body_sha256' certificates/screen_n3.json)" = \
  d2fef86e118c01732bda1772bbe174f4dbe3a29302d4d3ab5e6885f2d3bc264a
test "$(jq -r '.canonical_equal_relations' certificates/equal_audit_n3.json)" = 1014
test "$(jq -r '.counts.labelled_isomorphism' certificates/equal_audit_n3.json)" = 5
test "$(jq -r '.counts.ordinary_T' certificates/equal_audit_n3.json)" = 4
test "$(jq -r '.counts.pending_support_completion' certificates/equal_audit_n3.json)" = 1005
test "$(jq -r '.failure_count' certificates/equal_audit_n3.json)" = 0

test "$(gzip -cd certificates/strict_sign_workcache_n3.json.gz | jq '.certificates|length')" = 25
test "$(gzip -cd certificates/strict_sign_workcache_n3.json.gz | jq '[.certificates[]|select(.certified==true)]|length')" = 7

test ! -e certificates/strict_descriptor_audit_n3.json
grep -q '^\*\*UNRESOLVED\.\*\*' REVIEW.md

echo 'PASS: preserved scope-limited records are byte-exact; verdict remains UNRESOLVED.'
