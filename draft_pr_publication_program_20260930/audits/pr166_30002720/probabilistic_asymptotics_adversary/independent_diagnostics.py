#!/usr/bin/env python3
"""Independent probability/cost diagnostics. Finite checks are not the proof.
All validation uses explicit exceptions and remains active under Python -O.
No author verifier is imported or executed. Output goes only to stdout.
"""
from fractions import Fraction as F
from itertools import combinations
from math import erf, sqrt
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, sys

Q, R = F(3, 4), F(1, 4)
COUNTS = {}
NEGATIVES = {}

class DiagnosticFailure(RuntimeError):
    pass

def need(condition, group, message):
    if not condition:
        raise DiagnosticFailure(group + ': ' + message)
    COUNTS[group] = COUNTS.get(group, 0) + 1

def reject_mutation(name, callback):
    try:
        callback()
    except DiagnosticFailure as error:
        NEGATIVES[name] = {'detected': True, 'reason': str(error)}
    else:
        raise DiagnosticFailure('Undetected negative mutation: ' + name)

def empirical_error(us):
    n = len(us)
    return max(max(abs(F(i, n)-u), abs(F(i+1, n)-u))
               for i, u in enumerate(sorted(us)))

def grid_error(us, mesh_denominator):
    n = len(us)
    return max(abs(F(sum(u <= x for u in us), n)-x)
               for x in (F(r, mesh_denominator) for r in range(mesh_denominator+1)))

def path_for(u, depth):
    left, mass, previous = F(0), F(1), None
    result = [(left, mass)]
    for _ in range(depth):
        p0 = F(1, 2) if previous is None else (Q if previous == 0 else R)
        boundary = left + mass*p0
        bit = 0 if u < boundary else 1
        if bit:
            left = boundary
            mass *= 1-p0
        else:
            mass *= p0
        previous = bit
        result.append((left, mass))
    return result

def selection_operations(us, u):
    active = tuple(us)
    left, mass, previous, total, depth = F(0), F(1), None, 0, 0
    while len(active) > 1:
        total += len(active)
        p0 = F(1, 2) if previous is None else (Q if previous == 0 else R)
        boundary = left + mass*p0
        bit = 0 if u < boundary else 1
        if bit:
            active = tuple(x for x in active if x >= boundary)
            left = boundary
            mass *= 1-p0
        else:
            active = tuple(x for x in active if x < boundary)
            mass *= p0
        previous = bit
        depth += 1
        if depth > 200:
            raise DiagnosticFailure('Distinct rational points failed to separate')
    return total, depth

# Independent exact two-string collision recursion, not cylinder enumeration.
state = [F(1, 4), F(1, 4)]
for depth in range(1, 81):
    collision = sum(state, F(0))
    need(collision == F(1, 2)*F(5, 8)**(depth-1),
         'collision_recursion', 'Two-string exact collision law')
    need(collision <= F(1, 2)*Q**(depth-1),
         'collision_envelope', 'Maximum-cylinder envelope')
    state = [state[0]*Q*Q + state[1]*R*R,
             state[0]*R*R + state[1]*Q*Q]
reject_mutation('collision_exponent_shift', lambda: need(
    F(1, 2) <= F(1, 2)*F(5, 8), 'negative', 'False H instead of H-1 bound'))

# Rational empirical-CDF checks, using points with odd denominators so none
# can be a source cylinder endpoint (all source endpoints are dyadic).
points = [F(i, 11) for i in range(1, 11)]
max_depth = 0
for n in range(2, 5):
    for us in combinations(points, n):
        d = empirical_error(us)
        grid = grid_error(us, 4)
        need(d <= grid + F(1, 4), 'grid_interpolation', 'Missing monotone mesh control')
        operations = [selection_operations(us, u) for u in us]
        height = max(depth for _, depth in operations)
        max_depth = max(max_depth, height)
        for u, (cost, stopped_depth) in zip(us, operations):
            path = path_for(u, height)
            means = [mass for _, mass in path[:height]]
            occupancies = [sum(left <= x < left+mass for x in us)
                           for left, mass in path[:height]]
            for occupied, mean in zip(occupancies, means):
                need(abs(occupied - n*mean) <= 2*n*d,
                     'interval_count_control', 'Uniform interval count error')
            singleton_losses = sum(occupied == 1 for occupied in occupancies)
            decomposition = sum((F(occupied)-n*mean for occupied, mean in zip(occupancies, means)), F(0)) - singleton_losses
            need(F(cost)-n*sum(means, F(0)) == decomposition,
                 'operational_cost_decomposition', 'Singleton correction/sign/depth')
            need(singleton_losses <= height,
                 'singleton_loss', 'Singleton loss bounded by truncation height')
            need(abs(decomposition) <= 2*n*height*d + height,
                 'truncated_cost_control', 'Operational stopping cost control')
            tail_mass = path[height][1]
            lower = sum(means, F(0)); upper = lower + 4*tail_mass
            need(max(abs(F(cost)-n*lower), abs(F(cost)-n*upper)) <= 2*n*height*d + height + 4*n*tail_mass,
                 'mean_tail_enclosure', 'Whole infinite mean enclosed without reading singleton')
            need(stopped_depth <= height, 'global_height', 'Common stopping depth')
need(selection_operations((F(3, 11),), F(3, 11))[0] == 0,
     'n_one', 'Singleton input must cost zero')
reject_mutation('omit_grid_mesh', lambda: need(
    empirical_error((F(1, 11), F(2, 11))) <= grid_error((F(1, 11), F(2, 11)), 4),
    'negative', 'ECDF grid value alone need not bound the supremum'))
reject_mutation('charge_singleton', lambda: need(
    sum([1 for _ in range(5)]) == 0, 'negative', 'Continuing a singleton charges forbidden cost'))

# Exact ceiling controls and an explicit rational upper envelope for the
# asymptotic relative cost error. P is built by the independent block ratio.
p = F(9, 32)
t_prefix = F(0)
previous_n = 0
subsequence_rows = []
for j in range(2, 121):
    t_prefix += Q*p
    width = p*Q**j
    reciprocal = width**-2
    n = (reciprocal.numerator + reciprocal.denominator - 1)//reciprocal.denominator
    need(F(1) <= n*width*width < F(1)+width*width,
         'exact_ceiling', 'Ceiling error must remain below one')
    need(n*p*p >= Q**(-2*j), 'divergent_separation', 'Jump exceeds q^-j at sqrt(n) scale')
    need(n > previous_n, 'subsequence_growth', 'Strictly increasing subsequence')
    need(n <= 2*16**(j*j+j-1), 'log_upper_control', 'Polynomial logarithmic scale bound')
    previous_n = n
    if j in [2, 10, 40, 80, 120]:
        subsequence_rows.append({'j': j, 'n_bit_length': n.bit_length(),
                                 'q_to_j_float': float(Q**j),
                                 'ceiling_scaled_width_square_float': float(n*width*width)})
    if j == 6:
        t6 = t_prefix
    p *= R*R*Q**(2*j-1)

def error_envelope(j):
    return (Q**(j//2) + 976*j**3*Q**j + 61*j**2*Q**(2*j)
            + F(61, 2)*j**2*Q**(4*j) + F(1, 256)*Q**(10*j))
need(error_envelope(80) < F(1, 8), 'explicit_large_index_control', 'All-large-index band bound starts at j=80')
for j in range(80, 160):
    need(error_envelope(j+1) <= error_envelope(j), 'envelope_monotonicity', 'Envelope nonincrease')
    need(12*Q**(j-j//2) < 1, 'window_inclusion', 'Both side windows fit inside adjacent cylinders')
need(Q*F(11, 10)**3 < 1, 'analytic_monotonicity', 'j^3 q^j decreases for j>=10')
need(Q*Q*F(5, 4)**2 < 1, 'analytic_monotonicity', 'j^2 q^(2j) decreases for j>=4')

# Exact rational binomial tails with an integer recurrence. These diagnose the
# moving-rank indexing and normal scale; they do not certify an asymptotic CLT.
def order_cdf(n, k, parameter):
    a, b = parameter.numerator, parameter.denominator
    if not 0 < a < b:
        raise DiagnosticFailure('Binomial parameter outside (0,1)')
    value = (b-a)**n
    total, tail = value, value if k == 0 else 0
    for r in range(n):
        numerator = value*(n-r)*a
        denominator = (r+1)*(b-a)
        quotient, remainder = divmod(numerator, denominator)
        if remainder:
            raise DiagnosticFailure('Nonintegral binomial integer recurrence')
        value = quotient
        total += value
        if r+1 >= k:
            tail += value
    need(total == b**n, 'binomial_mass', 'Exact binomial law must sum to one')
    return F(tail, total)

phi = lambda z: (1+erf(z/sqrt(2)))/2
sigma = sqrt(float(t6*(1-t6)))
clt_rows = []
for n in [64, 256, 1024]:
    root_n = int(sqrt(n))
    k = (n*t6).numerator//(n*t6).denominator + 1
    need(1 <= k <= n, 'rank_rounding', 'Integer rank inside legal range')
    row = {'n': n, 'k': k, 'points': []}
    for z in [-1, 0, 1]:
        parameter = t6 + F(z, root_n)
        cdf = float(order_cdf(n, k, parameter))
        target = phi(z/sigma)
        row['points'].append({'z': z, 'exact_rational_cdf_float': cdf,
                              'normal_cdf': target, 'absolute_error': abs(cdf-target)})
        if n == 1024:
            need(abs(cdf-target) < .03, 'finite_clt_orientation', 'Finite moving-endpoint normal-scale control')
    clt_rows.append(row)
need(order_cdf(2, 1, F(1, 3)) == F(5, 9), 'order_binomial_duality', 'First-order-statistic event')
reject_mutation('rank_floor_without_plus_one', lambda: need(
    1 <= (2*t6).numerator//(2*t6).denominator <= 2, 'negative', 'Rank zero from floor(nt)'))
reject_mutation('binomial_tail_off_by_one', lambda: need(
    order_cdf(2, 0, F(1, 3)) == F(5, 9), 'negative', 'Wrong Bin>=k-1 threshold'))
reject_mutation('unit_variance_normal_scale', lambda: need(
    abs(clt_rows[-1]['points'][-1]['exact_rational_cdf_float']-phi(1)) < .03,
    'negative', 'Ignoring t(1-t) yields wrong limit variance'))

# A dependence adversary: the bad event is contained in the left-window event.
space = set(range(100)); event = set(range(49)); good = space-{0}
actual = F(len(event & good), 100)
need(actual >= F(len(event), 100)-F(len(space-good), 100),
     'dependence_free_union_control', 'Subtracting bad probability needs no independence')
reject_mutation('false_event_independence', lambda: need(
    actual >= F(len(event), 100)*F(len(good), 100),
    'negative', 'Product lower bound fails for dependent events'))

# Two deterministic bands and an adversarial center chosen after them.
left_band = (F(0), F(1)); right_band = (F(9), F(10)); radius = F(3)
for center in [F(k, 4) for k in range(-20, 61)]:
    interval = (center-radius, center+radius)
    intersects = lambda band: interval[0] <= band[1] and band[0] <= interval[1]
    need(not (intersects(left_band) and intersects(right_band)),
         'uniform_center_geometry', 'Short interval cannot meet both bands')

receipt = {
    'schema': 'independent-probability-diagnostics-v1',
    'status': 'PASS', 'created_at_utc': datetime.now(timezone.utc).isoformat(),
    'python': sys.version, 'optimization_level': sys.flags.optimize,
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'explicit_exception_checks': sum(COUNTS.values()), 'groups': COUNTS,
    'negative_mutations': NEGATIVES, 'max_operational_stopping_depth': max_depth,
    'subsequence_controls': subsequence_rows,
    'error_envelope_at_80_float': float(error_envelope(80)),
    'rank_prefix_j6_float': float(t6), 'rank_infinite_orientation_float': float(t_prefix),
    'rho_orientation_float': phi(1/sigma)-.5,
    'exact_binomial_orientation': clt_rows,
    'scope': 'Independent finite falsification diagnostics. The all-index probability/CLT/tightness proof is in DERIVATION.md. No author code is imported or executed.'
}
print(json.dumps(receipt, indent=2, sort_keys=True))
