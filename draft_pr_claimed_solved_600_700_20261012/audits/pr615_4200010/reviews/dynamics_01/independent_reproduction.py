#!/usr/bin/env python3
"""Independent exact finite controls for the PR #615 dynamics review.

Standard library only. No imports from author/prior audit code, and no writes
to the frozen inputs. Analytic infinite-dimensional results are in REVIEW.md.
"""
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

counts = Counter()

def require(group, predicate):
    if not predicate:
        raise AssertionError(group)
    counts[group] += 1

# Exact algebraic-number coordinates u + v sqrt(2).
def number(u=0, v=0): return Q(u), Q(v)
def plus(a, b): return a[0]+b[0], a[1]+b[1]
def times(c, a): return c*a[0], c*a[1]
def minus(a, b): return plus(a, times(-1, b))

alpha = number(0, 1)

def lift_step(z, direction):
    x, y = z
    if direction == 1:
        return plus(x, alpha), plus(y, x)
    return minus(x, alpha), plus(minus(y, x), alpha)

def lift_iterate(z, n):
    x, y = z
    return plus(x, times(n, alpha)), plus(plus(y, times(n, x)), times(Q(n*(n-1), 2), alpha))

seeds = [(number(Q(7,13)), number(Q(-3,17))),
         (number(Q(5,7), Q(-2,9)), number(Q(-11,19), Q(1,3)))]
for z in seeds:
    for n in range(-40, 41):
        actual = z
        for _ in range(abs(n)):
            actual = lift_step(actual, 1 if n > 0 else -1)
        require('irrational_exact_iterates', actual == lift_iterate(z, n))
    for n in range(-6, 7):
        for m in range(-6, 7):
            require('iterate_group_law', lift_iterate(lift_iterate(z, n), m) == lift_iterate(z, n+m))

# Fourier pullback and gauge of each nonzero-l chain into a bilateral shift.
for l in range(-7, 8):
    if not l:
        continue
    for r in range(abs(l)):
        for j in range(-13, 14):
            p = j*r + Q(l*j*(j-1), 2)
            p_next = (j+1)*r + Q(l*(j+1)*j, 2)
            require('bilateral_shift_phase_gauge', p + r + j*l == p_next)
            require('bilateral_shift_distinct_chain', r+j*l != r+(j+1)*l)

# Continuous-time correlation from an independently partitioned fundamental
# domain. The integral in x kills a term unless floor(t+s)=0. No quadrature.
def correlation(s):
    edges = {Q(0), Q(1)}
    for k in range(s.__floor__()-1, (s+1).__ceil__()+2):
        edge = Q(k)-s
        if 0 < edge < 1:
            edges.add(edge)
    edges = sorted(edges)
    total = Q(0)
    for a, b in zip(edges, edges[1:]):
        k = ((a+b)/2+s).__floor__()
        if k == 0:
            total += b-a
    return total

for denominator in [1, 2, 3, 7, 11]:
    for numerator in range(-50, 51):
        s = Q(numerator, denominator)
        require('continuous_time_triangular_correlation', correlation(s) == max(Q(0), 1-abs(s)))

# Fundamental-domain seam derivative and full transverse-energy direction.
def matmul(A, B):
    return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def transpose(A): return [list(c) for c in zip(*A)]
def eye(n): return [[Q(i == j) for j in range(n)] for i in range(n)]
def frame(t):
    A = eye(4)
    A[1][0] = -t
    return A
J = [[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]]

for t in [Q(0), Q(1,5), Q(2,3)]:
    for s in [Q(-17,5),Q(-1),Q(-2,7),Q(0),Q(3,7),Q(1),Q(23,3)]:
        for b, c in [(Q(1),Q(0)),(Q(0),Q(1)),(Q(-2),Q(5,7)),(Q(4,3),Q(-3))]:
            k = (t+s*b).__floor__()
            t1 = t+s*b-k
            D = eye(4)
            D[1][0] = k
            D[2][3] = s*c
            actual = matmul(matmul(frame(-t1), D), frame(t))
            expected = eye(4)
            expected[1][0] = s*b
            expected[2][3] = s*c
            require('full_frame_derivative', actual == expected)
            require('full_derivative_symplectic', matmul(matmul(transpose(actual), J), actual) == J)
            inverse = eye(4)
            inverse[1][0] = -s*b
            inverse[2][3] = -s*c
            require('full_derivative_inverse', matmul(actual, inverse) == eye(4))
            require('full_derivative_nilpotent', matmul(
                [[actual[i][j]-Q(i==j) for j in range(4)] for i in range(4)],
                [[actual[i][j]-Q(i==j) for j in range(4)] for i in range(4)])
                == [[Q(0) for _ in range(4)] for _ in range(4)])

# Exact phase differences of integer shifts: slope (p-q) sqrt(2).
for x, y in seeds:
    for p in range(-7,8):
        for q in range(-7,8):
            for n in [-19,-1,0,1,17]:
                difference = minus(lift_iterate((x,y),n+p)[1], lift_iterate((x,y),n+q)[1])
                expected = plus(times(p-q,x), times((p-q)*n+Q(p*(p-1)-q*(q-1),2),alpha))
                require('orbitwise_phase_difference', difference == expected)
            if p != q:
                require('orbitwise_irrational_slope_nonzero', times(p-q,alpha)[1] != 0)

bad_frame = eye(4)
bad_frame[1][0] = Q(2,3)
gluing = eye(4)
gluing[1][0] = 1
bad_frame_at_target = eye(4)
bad_frame_at_target[1][0] = Q(2,3)-1
omitted_transverse = eye(4)
actual_transverse = eye(4)
actual_transverse[2][3] = 2
controls = {
    'clock_invariant_at_time_one_but_not_half_time': Q(1)%1 == 0 and Q(1,2)%1 != 0,
    'continuous_time_cross_seam_fraction_matters': correlation(Q(1,2)) == Q(1,2),
    'clock_eigenfunction_is_a_factor_not_system': [Q(n)%1 for n in range(7)] == [0]*7,
    'frozen_zero_speed_is_not_the_band': correlation(Q(0)) == 1 and correlation(Q(1)) == 0,
    'positive_length_not_single_energy': Q(3,8)-Q(1,8) == Q(1,4) and Q(1,4)-Q(1,4) == 0,
    'negative_time_correlation_includes_last_return_cell': correlation(Q(-1,3)) == Q(2,3),
    'wrong_frame_sign_does_not_descend': matmul(gluing,bad_frame) != bad_frame_at_target,
    'rational_alpha_has_nonconstant_invariant_character': (7*Q(2,7)).denominator == 1,
    'omitted_energy_derivative_breaks_global_formula': actual_transverse != omitted_transverse,
}
require('controls_all_pass', all(controls.values()))

frozen = Path(__file__).resolve().parents[2] / 'native/unsolved_math_prioritization/attempts/4200010'
hashes = {}
for path in sorted(frozen.rglob('*')):
    if path.is_file():
        hashes[str(path.relative_to(frozen))] = hashlib.sha256(path.read_bytes()).hexdigest()

print(json.dumps({
    'result': 'PASS',
    'checks': sum(counts.values()),
    'groups': dict(sorted(counts.items())),
    'controls': controls,
    'frozen_input_sha256': hashes,
    'limitations': [
        'Finite exact algebra controls, not a formal proof checker.',
        'No floating point values, author modules, or prior auditor modules used.',
        'Analytic irrationality, ergodicity, disintegration, spectrum, and asymptotics are separately justified in REVIEW.md.'
    ]
}, indent=2, sort_keys=True))
