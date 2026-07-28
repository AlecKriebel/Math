#!/bin/sh
set -eu

base=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
campaign=$(CDPATH= cd -- "$base/../.." && pwd)
temporary=$(mktemp -d "${TMPDIR:-/tmp}/repair-holonomy-hostile.XXXXXX")
trap 'rm -rf "$temporary"' EXIT HUP INT TERM

check_hash() {
  expected=$1
  file=$2
  actual=$(shasum -a 256 "$campaign/$file" | awk '{print $1}')
  test "$actual" = "$expected"
}

check_hash 08cfa394f5fb1778beac62d752ec2700027ac7710071ed635d9e914f71133e8e \
  math/lemmas/maximum_independent_states.md
check_hash 543df545dea27669645979ce61451091140d4621f1e11cfdeeaa33437f4b5620 \
  math/lemmas/independent_antineighborhood_projection.md
check_hash d2c899b68f0d2142c250dee26047af43d01e10d83a0ed112c289a14c3f3d5e13 \
  math/reductions.md
check_hash e30a0ac4e028deefbf4c4533646ff934b617d8ff61dce38ec2389a50d622d8e7 \
  math/working/cross_state_response_exchange.md
check_hash d6a0ec8a7daff1cca0094e1929134507364cea3c2c8781fbe24956a3238048d8 \
  math/lemmas/general_target_response_propagation.md
check_hash 3255bcc3d75b8538d6c8e3288f8106b553194bbac1fc3ac590d18ba6d6f81de3 \
  math/working/reverse_state_domination/NOTE.md
check_hash fd4989145e199b68642e862d78f1af00a965f23556c3bee04f9728f33ef86b87 \
  math/working/coinductive_reciprocity/NOTE.md
check_hash 3481a7dcc650a83d3994ff4bfdfb7789a520bb6a29dc57b51c1a84d549fd5b77 \
  math/working/reverse_rank_descent/NOTE.md
check_hash 82baf97f95ff3f62442187fbf5a3bd043e7d790ff052ae01424c0791fac173ae \
  math/working/repair_square_holonomy/NOTE.md

(
  cd "$campaign"
  sh math/working/repair_square_holonomy/verify_strict.sh
)

PYTHONNOUSERSITE=1 python3 -I "$base/verify_cleanroom.py" > "$temporary/cleanroom.json"
cmp "$base/expected_cleanroom.json" "$temporary/cleanroom.json"

printf '%s\n' 'repair-square holonomy hostile review: PASS'
