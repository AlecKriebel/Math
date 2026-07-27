#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PYTHON_BIN="${PYTHON_BIN:-python3}"

GENERATED_CERTIFICATE="$(mktemp)"
trap 'rm -f "$GENERATED_CERTIFICATE"' EXIT
"$PYTHON_BIN" generate_certificate.py --output "$GENERATED_CERTIFICATE" >/dev/null
if ! cmp -s certificate.json "$GENERATED_CERTIFICATE"; then
  diff -u certificate.json "$GENERATED_CERTIFICATE"
  echo "FAIL: certificate.json does not regenerate byte-for-byte" >&2
  exit 1
fi
echo "PASS: certificate.json regenerates byte-for-byte"

"$PYTHON_BIN" verify_exact.py
"$PYTHON_BIN" test_cases.py
"$PYTHON_BIN" cycle_family.py 4
shasum -a 256 -c MANIFEST.sha256
