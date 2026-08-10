#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 reviews/final_standard_convention/verify_conventions.py
python3 - <<'PY'
import json
from pathlib import Path
p = Path('reviews/final_standard_convention/convention_certificate.json')
d = json.loads(p.read_text())
assert d['verdict'] == 'VERIFIED_AFTER_CORRECTION'
assert d['mutations']['unexpected_survivors'] == []
assert d['exact_tests']['primitive_supports']['support_graphs'] == 12
assert d['exact_tests']['primitive_supports']['admissible_rootings'] == 100
assert d['exact_tests']['simple_double_triangle_k4_minus_edge']['tree_child_rootings'] == 0
assert d['exact_tests']['literal_brits_two_subblob']['external_edge_count'] == 4
print('final standard-convention audit: PASS')
PY
