"""Exact controls targeting the equality-shortcut failure, not sampled theorem checks.

The geometric and compactness proof is in DERIVATION.md. This script supplies a
fully explicit equality case outside the real class to disprove the tempting
shortcut that a Koebe transform equality directly classifies the original map.
"""
from datetime import datetime, timezone
from pathlib import Path
import json
import sympy as s

z, w = s.symbols('z w')
a = s.I / 2
abar = -a
r2 = s.Rational(1, 4)
k = z / (1-z)**2
kp = s.diff(k, z)
psi = (z-a) / (1-abar*z)
f = s.factor((k.subs(z, psi) - k.subs(z, -a)) /
             ((1-r2)*kp.subs(z, -a)))
fp = s.diff(f, z)
fpp = s.diff(fp, z)
phi = (a+w) / (1+abar*w)
transformed = s.simplify((f.subs(z, phi) - f.subs(z, a)) /
                         ((1-r2)*fp.subs(z, a)))
P_at_a = s.simplify(fpp.subs(z, a) / fp.subs(z, a))
A_at_a = s.simplify((1-r2)*P_at_a - 2*abar)
c2 = s.simplify(s.diff(f, z, 2).subs(z, 0)/2)
c3 = s.simplify(s.diff(f, z, 3).subs(z, 0)/6)
# A rotated Koebe map has c2=2 lambda and c3=3 lambda^2.
koebe_identity_residual = s.simplify(4*c3 - 3*c2**2)
checks = {
    'normalization_value_zero': s.simplify(f.subs(z, 0)) == 0,
    'normalization_derivative_one': s.simplify(fp.subs(z, 0)) == 1,
    'koebe_transform_exactly_k_plus': s.simplify(transformed - w/(1-w)**2) == 0,
    'A_at_nonreal_marked_point_is_four': A_at_a == 4,
    'original_not_a_koebe_rotation': koebe_identity_residual != 0,
    'original_not_in_real_class': s.im(c2) != 0,
}
# Endpoint of the omitted ray under the normalized inverse transform.
endpoint = s.simplify((-s.Rational(1, 4) - k.subs(z, -a)) /
                      ((1-r2)*kp.subs(z, -a)))
outgoing_vector = s.simplify(-1 / ((1-r2)*kp.subs(z, -a)))
# This example deliberately has a real endpoint and an oblique ray: checking
# only that the endpoint is real would miss the direction condition.
checks['endpoint_real_but_outgoing_ray_oblique'] = (
    s.im(endpoint) == 0 and s.im(outgoing_vector) != 0)
result = {
    'utc': datetime.now(timezone.utc).isoformat(),
    'kind': 'exact adversarial control; no numerical evidence',
    'construction_univalence_reason':
        'Composition of an injective Koebe map and a disk automorphism, followed '
        'by an affine map with nonzero scale; derived independently in DERIVATION.md.',
    'a': str(a), 'f': str(f), 'koebe_transform': str(transformed),
    'a2': str(c2), 'a3': str(c3),
    '4a3_minus_3a2_squared': str(koebe_identity_residual),
    'A_at_a': str(A_at_a), 'omitted_endpoint': str(endpoint),
    'omitted_ray_outgoing_vector': str(outgoing_vector),
    'check_count': len(checks), 'checks': checks, 'all_pass': all(checks.values()),
}
out = Path(__file__).absolute().parent / 'EXACT_CONTROLS.json'
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
if not result['all_pass']:
    raise SystemExit(1)
