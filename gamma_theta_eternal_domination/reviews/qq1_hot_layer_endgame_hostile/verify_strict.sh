#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
candidate="$root/math/working/qq1_hot_layer_endgame"
review="$root/reviews/qq1_hot_layer_endgame_hostile"
temporary=$(mktemp -d "${TMPDIR:-/tmp}/qq1-hot-hostile.XXXXXX")
trap 'rm -rf "$temporary"' EXIT HUP INT TERM

check_hash() {
    expected=$1
    file=$2
    actual=$(shasum -a 256 "$file" | awk '{print $1}')
    test "$actual" = "$expected"
}

check_hash 9076ab509b24a9c9c8a36c7badc3d2a0f27906e5b967a1dbe825bf01924e80cd "$candidate/CANDIDATE_MANIFEST.json"
check_hash a7d9edb6e09354b8ce941377a0840ffa99c27315f9968ddee09395ed2c70a506 "$candidate/NOTE.md"
check_hash 94c846b8fdb61784719184cb54e8c651cbd4aa9195d3067dbbd54a43b54d7707 "$candidate/RESEARCH_LOG.md"
check_hash eeaf6f78a778e2e85919f52bd4bda175b9bd7cb0d6ef4472503536f720d9a2c0 "$candidate/expected_result.json"
check_hash 37a2e64807978ecd8c93641e449f7f66679e03a6f0582b81b0d3b3cc71c502e1 "$candidate/verify_implication.py"
check_hash 4ebb0d778814edeea49ad4a6003bbe7a99a387bb8161b9119450f587524202e8 "$candidate/verify_strict.sh"

check_hash cbe29f9d95e5b354aadb68711dccfb68e0d12323dc9a0b0609b5df236dadcdde "$review/independent_verify.py"
check_hash 2f89eda613b30647505eb652e306572b67645287bac8a24afe245b8a4c7b0cc8 "$review/expected.sha256"
check_hash 36dd5a715d9b6faa4fda354a7c2cc262efa520a948f5c4e3b0b008770a3a67f1 "$review/REVIEW.md"
check_hash 7d8795ee85b93c07d2a46b84c9b0091380d5ab934b548f5570bd9e18be87a68c "$review/RESEARCH_LOG.md"

sh "$candidate/verify_strict.sh"
python3 -I "$review/independent_verify.py" > "$temporary/result.json"
expected_result_hash=$(tr -d '[:space:]' < "$review/expected.sha256")
check_hash "$expected_result_hash" "$temporary/result.json"
printf '%s\n' 'QQ1 hot-layer endgame hostile review: PASS'
