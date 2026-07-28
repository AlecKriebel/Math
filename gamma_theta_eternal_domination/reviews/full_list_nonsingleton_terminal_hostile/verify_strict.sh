#!/bin/sh
set -eu

repo_root=$(git rev-parse --show-toplevel)
review_dir="$repo_root/gamma_theta_eternal_domination/reviews/full_list_nonsingleton_terminal_hostile"
candidate_dir="$repo_root/gamma_theta_eternal_domination/math/working/full_list_nonsingleton_terminal"
scratch=$(mktemp -d "${TMPDIR:-/tmp}/full-list-nonsingleton-review.XXXXXX")

cleanup() {
  find "$scratch" -type f -delete
  rmdir "$scratch"
}
trap cleanup EXIT HUP INT TERM

hash_file() {
  shasum -a 256 "$1" | awk '{print $1}'
}

check_hash() {
  actual=$(hash_file "$1")
  expected=$2
  label=$3
  if [ "$actual" != "$expected" ]; then
    echo "FAIL $label expected=$expected actual=$actual" >&2
    exit 1
  fi
  echo "PASS $label $actual"
}

check_hash \
  "$candidate_dir/CANDIDATE.md" \
  0497d07b8cf2bf1f5e3572f35d400d954745abae4490e6cac707f15cbcaeb22c \
  candidate-note
check_hash \
  "$candidate_dir/COLLISION_AUDIT.md" \
  24a7fcf9ee9f0bd4a4a24e7a1105fa6ef152e5bfa82c004f5f6b9c1204446eba \
  candidate-collision-audit
check_hash \
  "$candidate_dir/verify_cyclic_corridor_control.py" \
  3001b7f7b922cf91ad9ad4780b32d7f38acc4b673263ee7583869589709d6fc8 \
  candidate-verifier
check_hash \
  "$repo_root/gamma_theta_eternal_domination/math/working/full_list_safe_color_proof/NOTE.md" \
  a3a2fc44befb4084b783b73afe108e81af8b7ac3f20b0d34d00bfc35d1f4e62d \
  c149-source

python3 -I -B -W error \
  "$candidate_dir/verify_cyclic_corridor_control.py" \
  > "$scratch/candidate.json"
check_hash \
  "$scratch/candidate.json" \
  ca0b15eb32c5db9e47c8fca23af2c2d614a1f87626bf59bee585a2e294378b11 \
  candidate-output

python3 -I -B -W error \
  "$review_dir/independent_replay.py" \
  > "$scratch/independent.json"
check_hash \
  "$scratch/independent.json" \
  2aadb3446aad5074588631eeca448bc50d6c746232cdd749166c77e37f2596e1 \
  independent-output

python3 -I -B -W error \
  "$review_dir/search_local_countermodels.py" \
  > "$scratch/local-search.json"
check_hash \
  "$scratch/local-search.json" \
  1c2fd5a8673256a1a0db81197fbee864a43f90d61fc3cb48cf42a03be1177a0d \
  local-search-output

echo "PASS FULL_LIST_NONSINGLETON_TERMINAL_HOSTILE"
