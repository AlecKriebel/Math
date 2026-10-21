"""Exact arithmetic checks only; not a CAD or genericity certificate."""
from fractions import Fraction as Q
import json
from pathlib import Path
expected = [(0, 0), (160, 0), (930, 0), (3168, 624), (8260, 3808)]
rows = []
for d, pair in zip(range(3, 8), expected):
    e = d * (d - 2) * (d - 3) * (d * d + 2 * d - 4)
    t = Q(d * (d - 3) * (d - 4) * (d - 5) * (d * d + 3 * d - 2), 3)
    if not (t.denominator == 1 and (e, t) == pair):
        raise AssertionError()
    rows.append({'degree': d, 'edge': e, 'tritangent': int(t), 'sum': e + int(t)})
if not Q(1, 2) + Q(1, 2) == 1:
    raise AssertionError()
if not Q(1, 2) + Q(1, 4) == Q(3, 4) < 1:
    raise AssertionError()
if not Q(1, 2) + Q(1, 2) + Q(1, 4) == Q(5, 4) > 1:
    raise AssertionError()
if not Q(1, 2) ** 2 < Q(3, 4) ** 2 * 3:
    raise AssertionError()
if not all(((a - b) ** 2 + 3 > 4 for a, b in [(3, 6), (3, 9), (6, 9)])):
    raise AssertionError()
weights = [Q(1, t) for t in [3, 6, 9]]
weights = [x / sum(weights) for x in weights]
if not len(set((w * t for w, t in zip(weights, [3, 6, 9])))) == 1:
    raise AssertionError()
out = {'degree_checks': rows, 'finite_direction_example': {'q_squared_coordinates': ['1/2', '1/2', '1/4'], 'active_cylinder_sum': '1', 'other_cylinder_sums': ['3/4', '3/4'], 'norm_squared': '5/4'}, 'three_ball_checks': {'disjoint': True, 'free_translation_first_derivative_sign': 'positive for all three balls', 'positive_dependence_weights': [str(w) for w in weights]}, 'cad_execution': 'not performed', 'generic_quartic': 'existence proof only, no explicit generic sample certified'}
Path(__file__).with_name('EXACT_CHECKS.json').write_text(json.dumps(out, indent=2) + '\n')
print('PASS: degree arithmetic, finite-camera patch, and three-ball exact sign/disjointness/dependence checks')
