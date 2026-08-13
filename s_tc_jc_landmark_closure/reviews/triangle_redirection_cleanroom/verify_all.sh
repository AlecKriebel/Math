#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT=$(CDPATH= cd -- "$HERE/../.." && pwd)
TMPDIR_REVIEW=$(mktemp -d "${TMPDIR:-/tmp}/triangle-redirection-review.XXXXXX")
trap 'rm -rf "$TMPDIR_REVIEW"' EXIT HUP INT TERM

EXPECTED_PRIMARY_SCRIPT=1898123e26dd2e3818f8a9e31d228cbe387f977362f3ea5d55cc4a5dbe97eb88
EXPECTED_PRIMARY_CLAIM=1124e93f0d9f7af828564b51d77f17a9e638627bb31394204532c21cd03c9c37

actual_script=$(shasum -a 256 "$PROJECT/primary/verify_triangle_redirection.py" | awk '{print $1}')
actual_claim=$(shasum -a 256 "$PROJECT/primary/certificates/jc_triangle_redirection_active.json" | awk '{print $1}')
test "$actual_script" = "$EXPECTED_PRIMARY_SCRIPT"
test "$actual_claim" = "$EXPECTED_PRIMARY_CLAIM"

env -i PATH="$PATH" PYTHONDONTWRITEBYTECODE=1 \
  python3 "$HERE/cleanroom_verify.py" \
  --claim "$PROJECT/primary/certificates/jc_triangle_redirection_active.json" \
  --certificate "$TMPDIR_REVIEW/certificate.json" \
  --mutations "$TMPDIR_REVIEW/mutation_results.json"

cmp "$TMPDIR_REVIEW/certificate.json" "$HERE/certificate.json"
cmp "$TMPDIR_REVIEW/mutation_results.json" "$HERE/mutation_results.json"

(cd "$HERE" && shasum -a 256 -c MANIFEST.sha256)
printf '%s\n' 'VERIFIED: clean-room ordinary JC triangle-redirection certificate'
