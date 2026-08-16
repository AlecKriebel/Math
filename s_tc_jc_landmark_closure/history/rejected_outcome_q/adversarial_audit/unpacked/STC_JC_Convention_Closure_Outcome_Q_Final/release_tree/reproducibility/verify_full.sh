#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python src/primary_convention_frontier.py >/dev/null
g++ -O2 -std=c++17 review/independent_frontier.cpp -o /tmp/stc_independent_frontier
/tmp/stc_independent_frontier certificates/independent_frontier.json >/dev/null
g++ -O2 -std=c++17 review/independent_rooting_fibres.cpp -o /tmp/stc_independent_rooting
/tmp/stc_independent_rooting certificates/independent_rooting_fibres.json >/dev/null
python src/verify_root_zipper_structure.py >/dev/null
python src/verify_cleanup_jc.py >/dev/null
python review/independent_cleanup_model.py >/dev/null
python review/review_convention_equivalence.py >/dev/null
python review/run_mutation_suite.py >/dev/null
python reproducibility/verify_release.py
printf 'CONVENTION-CLOSURE FULL INDEPENDENT VERIFICATION PASSED\n'
