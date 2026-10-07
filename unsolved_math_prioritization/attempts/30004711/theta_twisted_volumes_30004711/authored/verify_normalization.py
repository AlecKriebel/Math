"""Check scalar/sign arithmetic; does not verify analytic extension theorems."""
from fractions import Fraction as F
import json
from pathlib import Path

chern_integral = -2 * (F(11, 24**2) + F(1, 24**2) + F(1, 2) * F(1, 24) * F(1, 2))
assert chern_integral == -F(1, 16)
raw = -chern_integral
theta = -2 * chern_integral
assert raw == F(1, 16) and theta == F(1, 8)
assert raw != theta and 2 * raw == theta
for g in range(8):
    for n in range(9):
        if 2*g-2+n > 0:
            r = 2*g-2+n
            assert (-1)**r == (-1)**n
            assert F(2)**(g-1+n) * F(2)**(1-g-n) == 1
report = {
    'problem_id': 30004711,
    'source': 'https://arxiv.org/abs/1712.03662v4',
    'source_result': 'Proposition 2.9',
    'method': 'Exact rational arithmetic on the independent orbifold GRR calculation; not recursion matching',
    'pushforward_c1_E_integral': str(chern_integral),
    'dual_euler_integral': str(raw),
    'theta_integral': str(theta),
    'normalized_factor_g1_n1': 2,
    'raw_equals_theta': raw == theta,
    'normalized_raw_equals_theta': 2 * raw == theta,
    'bounded_scalar_sign_test': {'g': [0,7], 'n': [0,8], 'stable_pairs_only': True, 'passed': True},
    'analytic_theorem_independently_tested': False,
}
Path(__file__).with_name('NORMALIZATION_CHECK.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
