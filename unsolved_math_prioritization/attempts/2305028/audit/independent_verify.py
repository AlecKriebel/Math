#!/usr/bin/env python3
"""Independent exact-arithmetic audit of the constants in PROOF.md.

This does not import or execute the author's verifier. Infinite-dimensional
analytic claims are assessed in AUDIT_REPORT.md, not proved by this script.
"""
from fractions import Fraction as F
import json

# Reconstruct the cutoff size from its stated quarter and third powers.
quarter_root, third_root = 64, 256
radius = quarter_root ** 4
assert radius == third_root ** 3 == 16777216
norm_bound = quarter_root + third_root
cutoff_error = F(norm_bound, radius)

# Analytic input: 3 < pi < 4, and cos(x) <= 1 - x^2/2 + x^4/24.
# On (0,1) the polynomial decreases, allowing x = pi/48 > 1/16.
x = F(3, 48)
cosine_polynomial = F(1) - x**2 / 2 + x**4 / 24
boundary_bound = 2 * cosine_polynomial + cutoff_error
radial_value = F(2 * radius, radius + 1)
gap = F(1001, 1000)
strict_margin = radial_value - gap * boundary_bound
assert strict_margin > 0
assert radial_value / boundary_bound == F(1649267441664, 1646063091521)

lower_boundary_norm = F(1, 2 * norm_bound)
error_parameter = F(1, 10000)
amplitude_ratio = error_parameter * lower_boundary_norm / 4
assert 0 < amplitude_ratio < F(1, 2)
# The geometric-tail inequality is independent of n after cancellation.
tail_normalized = 2 * amplitude_ratio / (1 - amplitude_ratio)
tail_allowance = error_parameter * lower_boundary_norm
assert tail_normalized <= tail_allowance

previous_and_future_errors = 2 * error_parameter
claimed_ratio = (gap - previous_and_future_errors) / (1 + previous_and_future_errors)
assert claimed_ratio == F(1668, 1667)
assert claimed_ratio > 1

# Redundant finite-index regressions, explicitly not a substitute for the
# general geometric-series calculation or the gliding-hump proof.
indices = [1, 2, 3, 7, 20, 100]
for n in indices:
    amplitude = amplitude_ratio ** (n - 1)
    future = 2 * amplitude_ratio ** n / (1 - amplitude_ratio)
    assert future <= tail_allowance * amplitude
    past = tail_allowance * amplitude
    worst_boundary = lower_boundary_norm * amplitude
    assert (gap * worst_boundary - past - future) / (worst_boundary + past + future) >= claimed_ratio

print(json.dumps({
    'all_checks_passed': True,
    'independent_of_author_verifier': True,
    'arithmetic': 'Python standard-library exact rational arithmetic',
    'R': radius,
    'M': norm_bound,
    'A_upper': str(cutoff_error),
    'G_upper': str(2 * cosine_polynomial),
    'combined_boundary_upper': str(boundary_bound),
    'radial_value': str(radial_value),
    'strict_gap_margin': str(strict_margin),
    'half_plane_ratio_lower': str(radial_value / boundary_bound),
    'lambda': str(gap),
    'c': str(lower_boundary_norm),
    'eta': str(error_parameter),
    'q': str(amplitude_ratio),
    'tail_normalized': str(tail_normalized),
    'tail_allowance': str(tail_allowance),
    'limsup_ratio_lower': str(claimed_ratio),
    'finite_regression_indices': indices,
    'scope': 'Arithmetic only; not a formal analytic proof or numerical boundary optimization.'
}, indent=2, sort_keys=True))
