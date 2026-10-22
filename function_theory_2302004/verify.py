#!/usr/bin/env python3
"""Supplementary finite controls, not a proof of the Julia-ray theorem.

Run with Python 3 and mpmath 1.3.0. No network, input corpus, or source PDF is
needed. The analytic infinite-preimage proof is in PROOF.md.
"""
from fractions import Fraction as Q
import json
import mpmath as mp

mp.mp.dps = 80
checks = []

def record(name, condition, kind):
    if not condition:
        raise AssertionError(name)
    checks.append({'name': name, 'kind': kind, 'passed': True})

# Exact arithmetic checks on the displayed inequalities and affine map.
for r in (2, 4, 8, 16):
    x_squared = Q(r*r, 2)
    record(f'center_error_bound_r{r}', 1/(2*x_squared) == Q(1, r*r), 'exact algebra')
for r in (3, 4, 8, 16):
    record(f'wedge_nonvanishing_margin_r{r}', Q(2, r*r) < Q(1, 2), 'exact inequality')
for d in (Q(1, 100), Q(1, 10), Q(1, 4)):
    record(f'disk_angle_majorant_{d}', d/(1-d) < 2*d and 1-d > Q(1, 2), 'exact inequality')
for a, b in ((Q(0), Q(1)), (Q(-3, 7), Q(13, 5)), (Q(9), Q(-2))):
    c, k = (a+b)/2, (a-b)/2
    record(f'affine_exception_map_{a}_{b}', k != 0 and c+k == a and c-k == b, 'exact algebra')
record('negative_control_equal_targets_rejected', (Q(2)-Q(2))/2 == 0, 'negative control')

# Non-rigorous high-precision samples of the independently proved estimate.
# Wide safety margins avoid presenting floating-point equality as a certificate.
for r in (2, 4, 8, 16):
    for numerator in (2, 3, 4):
        theta = numerator*mp.pi/12
        z = r*mp.exp(1j*theta)
        x = mp.re(z)
        delta = mp.sqrt(mp.pi)*z*mp.exp(z*z)*mp.erfc(z)-1
        record(f'relative_tail_bound_r{r}_angle{numerator}pi12',
               abs(delta) < 1/(2*x*x), 'non-rigorous numerical sample')

omega = mp.exp(1j*mp.pi/4)
for r in (2, 4, 8, 16):
    z = r*omega
    record(f'center_limit_bound_r{r}',
           abs(mp.erfc(z)) < (1+mp.mpf(r)**-2)/(mp.sqrt(mp.pi)*r),
           'non-rigorous numerical sample')
    record(f'reflection_identity_r{r}',
           abs(mp.erf(-mp.conj(z))+mp.conj(mp.erf(z))) < mp.mpf('1e-70'),
           'non-rigorous numerical sample')
    record(f'derivative_magnitude_r{r}',
           abs(abs(r*2/mp.sqrt(mp.pi)*mp.exp(-z*z))-2*r/mp.sqrt(mp.pi)) < mp.mpf('1e-70'),
           'non-rigorous numerical sample')

# Deliberately wrong candidate estimates must fail at these witnesses.
z = 4*omega
wrong_delta = mp.sqrt(mp.pi)*z*mp.erfc(z)-1 # omitted e^(z^2)
record('negative_control_missing_exponential_detected',
       abs(wrong_delta) > 1/(2*mp.re(z)**2), 'negative control')
wrong_derivatives = [2/mp.sqrt(mp.pi) for r in (2, 4, 8, 16)]
record('negative_control_missing_rescaling_detected',
       not all(a < b for a, b in zip(wrong_derivatives, wrong_derivatives[1:])),
       'negative control')

def bound_applicable(z):
    return mp.re(z) > 0
record('negative_control_left_half_plane_rejected',
       not bound_applicable(-4*omega), 'negative control')

output = {
    'schema_version': 1,
    'problem_id': '2302004',
    'mpmath_version': mp.__version__,
    'decimal_precision': mp.mp.dps,
    'scope': 'Finite supplementary checks only; not a proof of infinite preimages or normality.',
    'checks_passed': len(checks),
    'checks': checks,
}
print(json.dumps(output, indent=2, sort_keys=True))
