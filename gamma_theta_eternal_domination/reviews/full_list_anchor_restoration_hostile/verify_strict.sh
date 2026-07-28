#!/bin/sh
set -eu

review_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
project_dir=$(CDPATH= cd -- "$review_dir/../.." && pwd)
repo_dir=$(CDPATH= cd -- "$project_dir/.." && pwd)
candidate_dir="$project_dir/math/working/full_list_anchor_restoration"
tmp_dir=$(mktemp -d)
trap 'rm -rf -- "$tmp_dir"' EXIT HUP INT TERM

check_sha() {
  expected=$1
  path=$2
  actual=$(shasum -a 256 "$path" | awk '{print $1}')
  if [ "$actual" != "$expected" ]; then
    echo "frozen-byte mismatch: $path" >&2
    echo "actual=$actual expected=$expected" >&2
    exit 1
  fi
}

git -C "$repo_dir" cat-file -e 7a0c7a86^{commit}

check_sha fc407cb436bfd48f1eb26123cbe02ad1318f4a8a3a8cdee02a48064362261b9d \
  "$candidate_dir/NOTE.md"
check_sha a5800450e9a6472beaed52c8e99208f5bab8a4933e5903f779d7e65906885bbb \
  "$candidate_dir/COLLISION_AUDIT.md"
check_sha 897d092ebbcbd4c2b20fef90789226417a91591dc72b7a3c9487d26192776dce \
  "$candidate_dir/MANIFEST.json"
check_sha 42c204b43f50438d6fae80f23bfbc2e681bc04e80d4ba880d311638accf0de61 \
  "$candidate_dir/verify_control.py"
check_sha 64da40a30258e12ceaf76e34da77c3ac5f3284e033eed505b34e18fe628b76ae \
  "$candidate_dir/expected_result.json"
check_sha 55bf6dfedf5f0b90211e98774cf34e4a86222a522f365aa0633c52fdaf0110df \
  "$candidate_dir/verify_strict.sh"

check_sha a3a2fc44befb4084b783b73afe108e81af8b7ac3f20b0d34d00bfc35d1f4e62d \
  "$project_dir/math/working/full_list_safe_color_proof/NOTE.md"
check_sha e25845bbf5e23886284f2046ac8c5c661b48176f4bef9fda5651f733d4a0edb0 \
  "$project_dir/math/working/full_list_positive_rank_terminal/CANDIDATE.md"
check_sha 3e87ca4e7c04987c2f56576c4e8b0f28113e254fdb1a024b4da7a3e0d6bf4c68 \
  "$project_dir/math/working/k3_cross_state_attack.md"

"$candidate_dir/verify_strict.sh" > "$tmp_dir/candidate-strict.txt"
grep -F \
  "PASS full-list anchor-restoration strict replay a00e94a9be2a25a68a5346a5aa223e3a50ec2d946819e12a3e3c4af8bcb635cf" \
  "$tmp_dir/candidate-strict.txt" > /dev/null

python3 -I -B -W error "$review_dir/verify_clean.py" \
  > "$tmp_dir/clean-result.json"
actual_stdout_sha=$(shasum -a 256 "$tmp_dir/clean-result.json" | awk '{print $1}')
expected_stdout_sha=$(
  python3 -I -B -W error -c \
    'import json,sys; f=open(sys.argv[1],encoding="utf-8"); d=json.load(f); f.close(); print(d["verifier_stdout_sha256"])' \
    "$review_dir/expected_result.json"
)
if [ "$actual_stdout_sha" != "$expected_stdout_sha" ]; then
  echo "clean-room replay mismatch: $actual_stdout_sha != $expected_stdout_sha" >&2
  exit 1
fi

python3 -I -B -W error - "$tmp_dir/clean-result.json" \
  "$review_dir/expected_result.json" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as stream:
    actual = json.load(stream)
with open(sys.argv[2], encoding="utf-8") as stream:
    expected = json.load(stream)

assert actual["verdict"] == expected["verdict"] == "PASS"
assert actual["graph"]["graph6"] == expected["graph6"]
assert actual["graph"]["graph6_ascii_sha256"] == expected["graph6_ascii_sha256"]
assert actual["graph"]["edge_list_sha256"] == expected["edge_list_sha256"]
assert list(actual["parameters"].values()) != []
assert [
    actual["parameters"][key]
    for key in ("gamma", "i", "alpha", "gamma_infinity", "theta")
] == expected["parameters_gamma_i_alpha_gamma_infinity_theta"]
assert [
    actual["unrestricted_kernel_sizes"][str(k)] for k in (1, 2, 3)
] == expected["unrestricted_kernel_sizes_1_2_3"]
assert actual["full_list_setup"]["color_zero_rank_counts"] == expected["color_zero_rank_counts"]
assert actual["attacked_secondary_row"]["physical_movers"] == expected["attacked_secondary_physical_movers"]
assert actual["shared_secondary_row"]["physical_movers"] == expected["shared_secondary_physical_movers"]
assert actual["common_alternate"]["state"] == expected["common_alternate"]
assert actual["common_alternate"]["dominates"] is True
assert actual["common_alternate"]["banned"] is True
assert actual["common_alternate"]["retained"] is False
PY

echo "PASS full-list anchor-restoration hostile review $actual_stdout_sha"
