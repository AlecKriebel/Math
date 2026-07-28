#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
review="$root/reviews/qq1_completion_dynamics_hostile"
candidate="$root/math/working/qq1_completion_dynamics"
temporary=$(mktemp -d "${TMPDIR:-/tmp}/qq1-completion-hostile.XXXXXX")
trap 'rm -rf "$temporary"' EXIT HUP INT TERM

check_hash() {
    expected=$1
    file=$2
    actual=$(shasum -a 256 "$file" | awk '{print $1}')
    test "$actual" = "$expected"
}

check_hash 7deb990de3f1c4adf8540f1c922750197604ac0ea44131cd229a523716335328 "$candidate/NOTE.md"
check_hash 4a4f7bb7e1d8fe02f25b7736dc0bc2a51692a838c3958d28beb277333a8a64af "$candidate/RESEARCH_LOG.md"
check_hash 7ff18b948515d9c96f9ee46371b40c7436692dae269ba6112c452175e8be7be8 "$candidate/expected_result.json"
check_hash 9fd44d231d59b2d0f1d8db4fc434b8e6df5e2403985c7fdeaef2e89821192c1e "$candidate/verify_implication.py"
check_hash b8bd7b9cd1b75ea75639c9cb7e916ec8244086d6d24d8c10181d39f373f7dbb3 "$candidate/verify_strict.sh"
check_hash 6be2079e4450b80b11c9c83e4307589d3d1ed4c5c7acea9567d85c69c8b7b808 "$review/independent_verify.py"
check_hash 169b1655d701113d800d05ac532bf163a977b58b264a85263297020ec87e15af "$review/expected_result.json"

sh "$candidate/verify_strict.sh"
python3 -I "$review/independent_verify.py" > "$temporary/result.json"
cmp "$review/expected_result.json" "$temporary/result.json"
printf '%s\n' 'QQ1 completion-dynamics hostile review: PASS'
