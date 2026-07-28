#!/bin/sh
set -eu

review=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
candidate=$(CDPATH= cd -- "$review/../../math/working/rank_one_ur1_endgame" && pwd)
temporary=$(mktemp -d "${TMPDIR:-/tmp}/rank-one-ur1-hostile.XXXXXX")
trap 'rm -rf "$temporary"' EXIT HUP INT TERM

check_hash() {
  expected=$1
  file=$2
  actual=$(shasum -a 256 "$file" | awk '{print $1}')
  test "$actual" = "$expected"
}

check_hash 4983d87b0af8cec7ca06aa7a0a12b96bb480b8dbe4c886773770046b9b4090d6 "$candidate/NOTE.md"
check_hash 2321e32049de10822e48b61a2416b7558d10061487f6291c224412cb4bd6653c "$candidate/RESEARCH_LOG.md"
check_hash 61552c2466bd52a1c0617cf70e2917be548cd533de8ace4c787e60f7edd5ab3b "$candidate/MANIFEST.json"
check_hash c7d89a82c16f6010719bcb604a4c21533613e85c3033c93d99c139f95affad7e "$candidate/verify_implication.py"
check_hash 838dfd712a406c5c0a07bebe3ef48bc30833bf3b43011992a1da470cc08ca088 "$candidate/expected_result.json"
check_hash 368f82ffb87ffabda215b3da210c187deab65025048d30a072a68469c5d184ab "$candidate/verify_control.py"
check_hash 453d04b7488634c09f1ab3cd1496150e7b1c11523c205a4b1dfaa2bf5ee32473 "$candidate/expected_control_result.json"
check_hash 6d9ae279056c606b9c5a593375e2b1c85fcc8fa418f5c1c1af95e1fb9183e5b1 "$candidate/verify_strict.sh"

sh "$candidate/verify_strict.sh"
python3 -I "$review/independent_audit.py" > "$temporary/clean-room.json"
cmp "$review/expected_clean_room.json" "$temporary/clean-room.json"

printf '%s\n' 'rank-one ur=1 hostile review: PASS'
