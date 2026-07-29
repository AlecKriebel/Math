#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT HUP INT TERM
python3 "$here/verify_bowtie.py" > "$tmpdir/result.json"
cmp "$tmpdir/result.json" "$here/expected_result.json"
python3 "$here/audit_manifest.py" > "$tmpdir/manifest.json"
cmp "$tmpdir/manifest.json" "$here/MANIFEST.json"
echo "QQ1_SUPPORTED_ASYMMETRY_BOWTIE_STRICT_PASS"
