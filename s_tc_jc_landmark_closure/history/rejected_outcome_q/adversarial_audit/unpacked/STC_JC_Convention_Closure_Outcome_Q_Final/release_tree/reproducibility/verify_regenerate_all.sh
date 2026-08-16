#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
cp -a "$ROOT/." "$TMP/pkg"
cd "$TMP/pkg"
mkdir -p expected
cp certificates/*.json expected/
rm -f certificates/*.json
python src/primary_convention_frontier.py >/dev/null
python src/verify_root_zipper_structure.py >/dev/null
python src/verify_cleanup_jc.py >/dev/null
g++ -O2 -std=c++17 review/independent_frontier.cpp -o independent_frontier
./independent_frontier certificates/independent_frontier.json >/dev/null
g++ -O2 -std=c++17 review/independent_rooting_fibres.cpp -o independent_rooting
./independent_rooting certificates/independent_rooting_fibres.json >/dev/null
python review/independent_cleanup_model.py >/dev/null
python review/review_convention_equivalence.py >/dev/null
python review/run_mutation_suite.py >/dev/null
python reproducibility/dependency_audit.py >/dev/null
for f in expected/*.json; do cmp "$f" "certificates/$(basename "$f")"; done
python reproducibility/verify_release.py
printf 'CONVENTION-CLOSURE REGENERATE-ALL VERIFICATION PASSED\n'
