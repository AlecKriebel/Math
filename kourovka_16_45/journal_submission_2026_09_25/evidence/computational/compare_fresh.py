#!/usr/bin/env python3
"""Compare this review's exact reconstruction with both supplied replays."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent
fresh = json.loads((root/'independent_exact.json').read_text())
fresh_subgroups = {frozenset(tuple(h) for h in K)
                  for K in json.loads((root/'independent_subgroups.json').read_text())}
certificate = json.loads((root/'replay_python/finite_certificate.json').read_text())
matrices = [tuple(h) for h in certificate['matrices']]
python_subgroups = {frozenset(matrices[i] for i in K['elements'])
                   for K in certificate['subgroups']}

def decode(n):
    # Decode directly as a polynomial in 29, independently of the supplied
    # comparison utility's repeated-divmod implementation.
    return tuple(n//(29**i) % 29 for i in (3,2,1,0))

lines = (root/'subgroups_cpp.txt').read_text().splitlines()
cpp_subgroups = {frozenset(decode(int(n)) for n in line.split()) for line in lines[1:]}
if int(lines[0]) != 76 or len(lines) != 77:
    raise AssertionError('Invalid C++ subgroup export')
if not (len(fresh_subgroups) == len(python_subgroups) == len(cpp_subgroups) == 76
        and fresh_subgroups == python_subgroups == cpp_subgroups):
    raise AssertionError('Actual subgroup sets disagree')
summary = json.loads((root/'replay_python/verification_python.json').read_text())
comparisons = [
    (fresh['affine']['order'],summary['group_order'],'affine order'),
    (fresh['affine']['omission_orders'],summary['omission_orders'],'omission orders'),
    (fresh['affine']['elements_sha256'],summary['affine_elements_sha256'],'all affine elements'),
    (fresh['characteristic_11']['deletion_orders'],
     summary['adversarial_prime_11']['deletion_intersection_orders'],'p11 deletion orders'),
    (fresh['affine']['coset_degree'],summary['faithful_3_family']['coset_action_degree'],'action degree'),
]
for left,right,name in comparisons:
    if left != right:
        raise AssertionError(name+' disagrees')
print('PASS: all 76 actual matrix subgroups agree among all three implementations.')
print('PASS: SHA-256 of all 100920 sorted affine elements agrees with supplied Python.')
print('PASS: affine orders, omission orders, action degree, and p=11 deletion orders agree.')
print('Affine elements SHA-256: '+fresh['affine']['elements_sha256'])
