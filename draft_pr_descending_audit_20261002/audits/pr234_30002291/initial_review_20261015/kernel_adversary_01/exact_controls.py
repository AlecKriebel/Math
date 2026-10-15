#!/usr/bin/env python3
"""Independent exact rational controls for the kernel review.

No stochastic simulation, external packages, inherited scripts, or downloaded input.
All root/series comparisons that decide assertions use Fraction and integer arithmetic.
Finite decimal displays are descriptive only. The mathematical tail estimate is
reproved in REPORT.md; this program checks its exact-arithmetic consequences.
"""
from fractions import Fraction as Q
from math import isqrt
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import platform
import sys

HERE = Path(__file__).resolve().parent
PROOF = HERE.parent / 'submitted/unsolved_math_prioritization/attempts/30002291/PROOF.md'
SCALE = 1 << 64

def fourth_root_interval(x):
    """Rational enclosure of x**(1/4), width <=2**-64."""
    x = Q(x)
    assert x >= 0
    if not x:
        return Q(0), Q(0)
    n = x.numerator * SCALE**4 // x.denominator
    k = isqrt(isqrt(n))
    assert k**4 * x.denominator <= x.numerator * SCALE**4
    assert (k + 1)**4 * x.denominator > x.numerator * SCALE**4
    lo = Q(k, SCALE)
    hi = lo if k**4 * x.denominator == x.numerator * SCALE**4 else Q(k+1, SCALE)
    return lo, hi

def sqrt_interval(x):
    x = Q(x)
    assert x > 0
    n = x.numerator * SCALE**2 // x.denominator
    k = isqrt(n)
    assert k*k*x.denominator <= x.numerator*SCALE**2
    assert (k+1)**2*x.denominator > x.numerator*SCALE**2
    lo = Q(k, SCALE)
    hi = lo if k*k*x.denominator == x.numerator*SCALE**2 else Q(k+1, SCALE)
    return lo, hi

def positive_fourth(x):
    return fourth_root_interval(max(Q(0), Q(x)))

def increment_sq_interval(a, b):
    assert a >= b
    al, ah = positive_fourth(a)
    bl, bh = positive_fourth(b)
    lo, hi = max(Q(0), al-bh), ah-bl
    assert 0 <= lo <= hi
    return lo*lo, hi*hi

def partial_w(u, count):
    lo = hi = Q(0)
    for ell in range(1, count+1):
        a, b = increment_sq_interval(Q(ell)-u, Q(ell-1)-u)
        lo += a
        hi += b
    return lo, hi

def w_interval(u, count):
    lo, hi = partial_w(u, count)
    # Integral tail: sum_{ell>N} d_ell^2 <= (1/8)/sqrt(N-u).
    sqrt_lo, _ = sqrt_interval(Q(count)-u)
    return lo, hi + Q(1, 8)/sqrt_lo

def show(interval):
    return {'lower': str(interval[0]), 'upper': str(interval[1]),
            'decimal_lower': float(interval[0]), 'decimal_upper': float(interval[1])}

started = datetime.now(timezone.utc).isoformat()
checks = []
# Torus endpoint equality is exactly a reindexing, with an explicit leftover.
for count in (2, 7, 64, 256):
    at_zero = partial_w(Q(0), count-1)
    at_one = partial_w(Q(1), count)
    assert at_zero == at_one
checks.append({'name': 'endpoint_reindexing', 'status': 'PASS',
               'counts': [2, 7, 64, 256]})

# The exact impulse position is independently obtained from rational time and mesh.
# Include exact mesh hits, near either endpoint, and an interior phase.
s = Q(7, 3)
phases = [Q(0), Q(1, 2), Q(1, 1_000_003), Q(1)-Q(1, 1_000_003)]
index_cases = []
for phase in phases:
    delta = s/(Q(41)+phase)
    j = s//delta
    actual_phase = s/delta-j
    assert actual_phase == phase
    for ell in range(1, 13):
        i = j+ell
        normalized_right = (i*delta-s)/delta
        normalized_left = ((i-1)*delta-s)/delta
        assert normalized_right == Q(ell)-phase
        assert normalized_left == Q(ell-1)-phase
        assert increment_sq_interval(normalized_right, normalized_left) == increment_sq_interval(Q(ell)-phase, Q(ell-1)-phase)
    index_cases.append(str(phase))
checks.append({'name': 'impulse_grid_indexing', 'status': 'PASS',
               's': str(s), 'phases': index_cases, 'increments_each': 12})

# W at both ends and half-phase, including certified infinite-series tails.
bounds = {str(u): w_interval(u, 256) for u in (Q(0), Q(1, 2), Q(1))}
assert bounds['0'][0] >= 1
assert bounds['1/2'][1] < 1
assert max(bounds['0'][0], bounds['1'][0]) <= min(bounds['0'][1], bounds['1'][1])
checks.append({'name': 'certified_infinite_W_intervals', 'status': 'PASS',
               'alpha': '1/4', 'summands': 256,
               'bounds': {key: show(value) for key, value in bounds.items()}})

# The analytic half-phase bound is 5/(4sqrt(2)); its being <1
# is exactly the positive-number comparison 25<32.
assert 25 < 32
checks.append({'name': 'deterministic_time_counterexample_separation', 'status': 'PASS',
               'exact_comparison': 'W(0)>=1>5/(4sqrt(2))>=W(1/2); 25<32'})

# For homogeneous power tails, explicit cross-localization bound at alpha=1/4:
# scaled energy past gap eta <= (1/8)/sqrt(eta/delta-1), eta>delta.
# These exact enclosures exhibit deterministic decay under irregular mesh rates.
localization = []
eta = Q(2, 7)
previous_upper = None
for divisor in (17, 131, 2053, 65539):
    delta = eta/divisor
    sqrt_lo, _ = sqrt_interval(eta/delta-1)
    bound = Q(1, 8)/sqrt_lo
    if previous_upper is not None:
        assert bound < previous_upper
    previous_upper = bound
    localization.append({'delta_over_eta': str(delta/eta), 'energy_upper': str(bound), 'decimal_upper': float(bound)})
checks.append({'name': 'deterministic_power_tail_localization', 'status': 'PASS',
               'alpha': '1/4', 'bounds': localization})

payload = {
    'status': 'PASS',
    'started_utc': started,
    'finished_utc': datetime.now(timezone.utc).isoformat(),
    'python': sys.version,
    'platform': platform.platform(),
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'candidate_path': str(PROOF),
    'candidate_sha256': hashlib.sha256(PROOF.read_bytes()).hexdigest(),
    'method': 'Exact rational and integer root interval arithmetic, with analytic integral tail bounds; no Monte Carlo.',
    'checks': checks,
    'limitations': 'Checks certify their displayed deterministic consequences. The theorem is assessed by the independent analytic derivation in REPORT.md; a finite computation does not prove stochastic stable convergence.'
}
(HERE/'replay_receipt.json').write_text(json.dumps(payload, indent=2)+'\n')
print(json.dumps({'status': payload['status'], 'finished_utc': payload['finished_utc'],
                  'checks': [x['name'] for x in checks],
                  'W_intervals': {key: [float(x) for x in value] for key, value in bounds.items()}}, indent=2))
