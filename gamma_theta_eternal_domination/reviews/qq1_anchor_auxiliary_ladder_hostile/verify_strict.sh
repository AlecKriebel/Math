#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
CAMPAIGN=$(CDPATH= cd -- "$HERE/../.." && pwd)
SHOWG="$CAMPAIGN/tools/nauty2_9_3/showg"
LABELG="$CAMPAIGN/tools/nauty2_9_3/labelg"
WORK=$(mktemp -d "${TMPDIR:-/tmp}/qq1-anchor-hostile.XXXXXX")
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

export PYTHONDONTWRITEBYTECODE=1

expected_showg=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["showg_sha256"])' "$HERE/expected_digests.json")
expected_labelg=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["labelg_sha256"])' "$HERE/expected_digests.json")
expected_cleanroom=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["cleanroom_result_json_sha256"])' "$HERE/expected_digests.json")
expected_candidate_audit=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["candidate_manifest_audit_json_sha256"])' "$HERE/expected_digests.json")
expected_candidate_manifest=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["candidate_manifest_sha256"])' "$HERE/expected_digests.json")

actual_showg=$(shasum -a 256 "$SHOWG" | awk '{print $1}')
actual_labelg=$(shasum -a 256 "$LABELG" | awk '{print $1}')
test "$actual_showg" = "$expected_showg"
test "$actual_labelg" = "$expected_labelg"

python3 "$HERE/independent_verify.py" \
  --showg "$SHOWG" \
  --labelg "$LABELG" \
  >"$WORK/cleanroom.json"
python3 "$HERE/audit_candidate.py" >"$WORK/candidate-audit.json"

python3 -m json.tool "$WORK/cleanroom.json" >/dev/null
python3 -m json.tool "$WORK/candidate-audit.json" >/dev/null

actual_cleanroom=$(shasum -a 256 "$WORK/cleanroom.json" | awk '{print $1}')
actual_candidate_audit=$(shasum -a 256 "$WORK/candidate-audit.json" | awk '{print $1}')
actual_candidate_manifest=$(shasum -a 256 "$CAMPAIGN/math/working/qq1_anchor_auxiliary_ladder/CANDIDATE_MANIFEST.json" | awk '{print $1}')

test "$actual_cleanroom" = "$expected_cleanroom"
test "$actual_candidate_audit" = "$expected_candidate_audit"
test "$actual_candidate_manifest" = "$expected_candidate_manifest"

sh "$CAMPAIGN/math/working/qq1_anchor_auxiliary_ladder/verify_strict.sh" \
  >"$WORK/candidate-replay.txt"
grep -Fx 'QQ1 anchor-auxiliary fixed-control audit: PASS' \
  "$WORK/candidate-replay.txt" >/dev/null

python3 "$HERE/audit_review_manifest.py" >/dev/null
PYTHONPYCACHEPREFIX="$WORK/pycache" python3 -m py_compile \
  "$HERE/independent_verify.py" \
  "$HERE/audit_candidate.py" \
  "$HERE/audit_review_manifest.py"

printf '%s\n' 'QQ1 anchor-auxiliary hostile review: PASS'
