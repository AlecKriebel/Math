#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
campaign=$(CDPATH= cd -- "$here/../.." && pwd)
temporary=$(mktemp -d "${TMPDIR:-/tmp}/qq1-inner-global-hostile.XXXXXX")
trap 'rm -rf "$temporary"' EXIT HUP INT TERM

python3 "$here/independent_verify.py" >"$temporary/cleanroom.json"
python3 "$here/audit_candidate_manifest.py" >"$temporary/manifest-audit.json"

expected_cleanroom=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["cleanroom_result_json_sha256"])' "$here/expected_digests.json")
expected_manifest_audit=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["candidate_manifest_audit_json_sha256"])' "$here/expected_digests.json")
expected_candidate_manifest=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["candidate_manifest_sha256"])' "$here/expected_digests.json")

actual_cleanroom=$(shasum -a 256 "$temporary/cleanroom.json" | awk '{print $1}')
actual_manifest_audit=$(shasum -a 256 "$temporary/manifest-audit.json" | awk '{print $1}')
actual_candidate_manifest=$(shasum -a 256 "$campaign/math/working/qq1_inner_global_attack/CANDIDATE_MANIFEST.json" | awk '{print $1}')

test "$actual_cleanroom" = "$expected_cleanroom"
test "$actual_manifest_audit" = "$expected_manifest_audit"
test "$actual_candidate_manifest" = "$expected_candidate_manifest"

sh "$campaign/math/working/qq1_inner_global_attack/verify_strict.sh" >"$temporary/candidate-replay.txt"
grep -Fx 'QQ1 inner global control audit: PASS' "$temporary/candidate-replay.txt" >/dev/null

PYTHONPYCACHEPREFIX="$temporary/pycache" \
  python3 -m py_compile "$here/independent_verify.py" "$here/audit_candidate_manifest.py"
printf '%s\n' 'QQ1 inner global hostile review: PASS'
