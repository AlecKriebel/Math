#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo=$(git -C "$here" rev-parse --show-toplevel)
candidate_dir="$repo/gamma_theta_eternal_domination/math/working/full_list_restoration_cross_color_coupling"

hash_file() {
    shasum -a 256 "$1" | awk '{print $1}'
}

test "$(git -C "$repo" show e2e8809d0b397bff64d38f70e9ce93f38a1cc75e:gamma_theta_eternal_domination/math/working/full_list_restoration_cross_color_coupling/NOTE.md | shasum -a 256 | awk '{print $1}')" = "3abeac165f1ad0830cbced17012d2ef7b2435fc4486a663dc7160d87cf27aeea"
test "$(hash_file "$candidate_dir/NOTE.md")" = "3abeac165f1ad0830cbced17012d2ef7b2435fc4486a663dc7160d87cf27aeea"
test "$(hash_file "$candidate_dir/MANIFEST.json")" = "ebbc2c06c116052a8e1e90d32bd1e7c3d9c39489d7a7c84f2d3ccb87a58cd2fd"

test "$(hash_file "$repo/gamma_theta_eternal_domination/math/working/full_list_anchor_restoration/NOTE.md")" = "fc407cb436bfd48f1eb26123cbe02ad1318f4a8a3a8cdee02a48064362261b9d"
test "$(hash_file "$repo/gamma_theta_eternal_domination/math/working/full_list_three_color_coupling/NOTE.md")" = "3d0e38493159d69b6d790b9614253e02f92ab7acbf5acf7a54dc003f7f10bb87"
test "$(hash_file "$repo/gamma_theta_eternal_domination/math/working/full_list_escape_completion_fan/NOTE.md")" = "4eb6944a766ccb56c0260ad14bfbcdf6ea9b765d371b293f302f35b4519057c4"
test "$(hash_file "$repo/gamma_theta_eternal_domination/math/working/full_list_rank_rebound_iteration/NOTE.md")" = "378633621b759c31d1b747b0f1a7bd657f17d8b60da9b8356488640e8fbb8f19"
test "$(hash_file "$repo/gamma_theta_eternal_domination/math/working/full_list_rank_one_anchor_exit/NOTE.md")" = "b3aeccda5f44540510559712ee18840560e82646062b1be279afe4f03791d1df"
test "$(hash_file "$repo/gamma_theta_eternal_domination/reviews/full_list_rank_one_anchor_exit_hostile/MANIFEST.json")" = "c2096408b4ab4b7ca87fee7bd387d4b528935f1954baee6a30e6589e646e71f5"

"$candidate_dir/verify_strict.sh" >/dev/null

actual=$(python3 "$here/verify_clean.py")
expected=$(tr -d '\n' < "$here/expected_result.json")
test "$actual" = "$expected"

grep -Fq '**UNCONDITIONAL PASS.**' "$here/REVIEW.md"
grep -Fq 'no C-176 ancestry asserted' "$here/expected_result.json"

python3 - "$here" <<'PY'
import hashlib
import json
import sys
from pathlib import Path

directory = Path(sys.argv[1])
manifest = json.loads((directory / "MANIFEST.json").read_text())
for relative, expected in manifest["files"].items():
    actual = hashlib.sha256((directory / relative).read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f"hash mismatch {relative}: {actual}")
PY

printf '%s\n' "PASS hostile review of restoration rebound"
