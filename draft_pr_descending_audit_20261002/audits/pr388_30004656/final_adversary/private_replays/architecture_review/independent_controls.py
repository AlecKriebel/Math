#!/usr/bin/env python3
"""Exact architecture controls; imports no author/reviewer implementation.

Run in this directory: python3 independent_controls.py
Finite controls are not substitutes for the analytic probability/uniformity proof.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from math import factorial, prod
from pathlib import Path
import hashlib
import json
import random
from datetime import datetime, timezone

COUNTS = defaultdict(int)
RNG = random.Random(2026100238845)


def check(value, group):
    assert value, group
    COUNTS[group] += 1


def sq(vector):
    return sum(v * v for v in vector)


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


# Exact series coefficients supporting both mgf arguments.
for d in [2, 3, 4, 5, 8, 16, 64, 257]:
    for h in range(1, 65):
        odd = prod(range(1, 2 * h, 2))
        sphere_moment = F(odd, prod(d + 2 * j for j in range(h)))
        check(sphere_moment <= F(odd, d ** h), "sphere_moment")
        check(F(4 ** h * odd, factorial(2 * h)) == F(2 ** h, factorial(h)), "relu_mgf_coefficient")
        check(odd <= 2 ** h * factorial(h), "quadratic_raw_moment")
        if h >= 2:
            check(2 ** (h - 1) * (2 ** h * factorial(h) + 1) <= 4 ** h * factorial(h), "quadratic_centered_moment")

# Convex-power inequality used for independent-copy symmetrization, including
# both signs and highly unequal endpoints (rather than centered-moment guesses).
values = [F(-11), F(-3, 2), F(-1, 10), F(0), F(1, 10), F(7, 3), F(17)]
for a, b, h in product(values, values, range(1, 13)):
    check((a - b) ** (2 * h) <= 2 ** (2 * h - 1) * (a ** (2 * h) + b ** (2 * h)), "independent_copy")

# Every activation orthant is realized by explicitly solving an invertible
# bidiagonal W. Points need not be normalized because positive normalization
# leaves strict signs invariant.
for k in range(1, 10):
    for signs in product((-1, 1), repeat=k):
        x = [F(0)] * k
        for j in range(k - 1, -1, -1):
            x[j] = F(signs[j]) - (x[j + 1] if j + 1 < k else 0)
        image = tuple(x[j] + (x[j + 1] if j + 1 < k else 0) for j in range(k))
        check(image == signs, "activation_orthants")
        check(sq(x) > 0, "activation_orthants")

# Arbitrarily ill-conditioned but full-rank pair, with all strict patterns.
for power in range(1, 19):
    delta = F(1, 10 ** power)
    for s1, s2 in product((-1, 1), repeat=2):
        x = (F(s1), F(s2 - s1) / delta)
        check((x[0], x[0] + delta * x[1]) == (s1, s2), "ill_conditioned_orthants")

# Vector cancellation and complementary subset identities, with exact sums.
for k in range(1, 9):
    for dimension in [2, 3, 7]:
        for _ in range(4):
            vectors = [[F(RNG.randrange(-20, 21), RNG.randrange(1, 8)) for _ in range(dimension)] for _ in range(k)]
            energy = sum(sq(v) for v in vectors)
            total_signed = 0
            max_subset_sq = F(0)
            for eps in product((-1, 1), repeat=k):
                signed = [sum(eps[i] * vectors[i][j] for i in range(k)) for j in range(dimension)]
                a = [sum(vectors[i][j] for i in range(k) if eps[i] == 1) for j in range(dimension)]
                ac = [sum(vectors[i][j] for i in range(k) if eps[i] == -1) for j in range(dimension)]
                check(signed == [a[j] - ac[j] for j in range(dimension)], "subset_identity")
                check(sq(signed) <= 2 * (sq(a) + sq(ac)), "subset_identity")
                total_signed += sq(signed)
                max_subset_sq = max(max_subset_sq, sq(a), sq(ac))
            check(total_signed == 2 ** k * energy, "rademacher_energy")
            check(energy <= 4 * max_subset_sq, "rademacher_energy")

# Radial homogeneity bridge, checking the joint inequality directly in squares.
for r_int, s_int, chord_num in product(range(1, 21), range(21), range(41)):
    r, s, chord = F(r_int, 7), F(s_int, 7), F(chord_num, 20)
    if s > r:
        continue
    distance_sq = (r - s) ** 2 + r * s * chord ** 2
    check((s * chord + 2 * (r - s)) ** 2 <= 9 * distance_sq, "radial_bridge")

# Exact finite geometric series, controlling the infinite threshold sum.
for J in range(1, 129):
    check(sum(F(1, 2 ** j) for j in range(1, J + 1)) == 1 - F(1, 2 ** J), "chaining_series")
    check(sum(F(j, 2 ** j) for j in range(1, J + 1)) == 2 - F(J + 2, 2 ** J), "chaining_series")
    check(sum(F(j + 2, 2 ** j) for j in range(1, J + 1)) == 4 - F(J + 4, 2 ** J), "chaining_series")
for d, j, v in product([2, 3, 4, 17, 1000], range(1, 101), [F(1, 100), F(1), F(2), F(1000)]):
    check(1 + 2 ** (j + 1) <= 2 ** (j + 2), "chaining_cardinality")
    # Replacing log(2) by 1 makes this a stronger rational upper bound.
    log_failure_upper = d * (2 * j + 3) - 8 * (d * (j + 2) + v + j)
    check(log_failure_upper <= -v - j, "chaining_union")
check(8 + 32 * (4 + 1 + 2) == 232 < 256, "chaining_constants")
check(2 * 6 * 256 == 3072 and F(1, 3072) >= F(1, 4096), "relu_final_constant")

# Bernstein regimes: normalized dt/N, with exact optimizer and boundary.
for ratio in [F(0), F(1, 100000), F(1), F(399, 100), F(4), F(401, 100), F(8), F(1000)]:
    if ratio <= 4:
        lam = ratio / 64
        check(lam <= F(1, 16), "bernstein_regime")
        check(-lam * ratio + 32 * lam * lam == -ratio * ratio / 128, "bernstein_regime")
    else:
        check(-ratio / 16 + F(1, 8) <= -ratio / 32, "bernstein_regime")
for lambda_abs in [F(0), F(1, 100000), F(1, 32), F(1, 16), F(1, 8)]:
    check(16 * lambda_abs ** 2 / (1 - 4 * lambda_abs) <= 32 * lambda_abs ** 2, "quadratic_mgf_radius")

# Logarithms bounded by exact truncated exponential series, without floats.
# exp(1)>2, exp(3)>9, exp(2)>5 => log2<1, log9<3, log5<2.
for value, target in [(F(1), 2), (F(3), 9), (F(2), 5)]:
    check(sum(value ** j / factorial(j) for j in range(20)) > target, "net_log_constants")

# Label count/parity controls include each possible label count, not only an
# assumed rounded N. Input independence after label-only selection is analytic.
for n in range(16, 601):
    for plus_count in range(n + 1):
        minus_count = n - plus_count
        if min(plus_count, minus_count) * 8 < 3 * n:
            continue
        N = 2 * min(plus_count, minus_count)
        check(N % 2 == 0 and N <= n and N * 4 >= 3 * n, "label_parity_balance")
        check(F(N * n, 256) <= F(N * N, 4), "selected_error_correlation")
    # Choose the smallest actually possible balanced N under the label event.
    min_m = (3 * n + 7) // 8
    N = 2 * min_m
    for d in sorted(set([2, n // 8])):
        if d < 2 or n < 8 * d:
            continue
        check(N >= d, "matrix_concentration_domain")
        for k in sorted(set([1, d - 1, d, d + 1, 10 * d])):
            check(F(N, 32 ** 2) >= F(n, 8192 ** 2 * k), "linear_final_constant")
            if k < d:
                check(F(N * d, (2048 * k) ** 2) >= F(N, 2048 ** 2 * k), "low_rank_gain")
                check(F(N * d, (2048 * k) ** 2) >= F(n, 8192 ** 2 * k), "quadratic_final_constant")
            else:
                check(F(N, 1024 ** 2 * d) >= F(n, 8192 ** 2 * k), "quadratic_final_constant")

# Rational circle grid for non-diagonal symmetric quadratics. Spectral-spread
# square in 2D is (a-c)^2+4b^2, so no numerical eigensolver is involved.
circle = []
for t in [F(j, 7) for j in range(-5, 6)]:
    circle.append(((1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)))
for x in circle:
    check(sq(x) == 1, "rational_sphere")
for a, b, c in product(range(-2, 3), repeat=3):
    spread_sq = (a - c) ** 2 + 4 * b * b
    def quadratic(x):
        return a * x[0] ** 2 + 2 * b * x[0] * x[1] + c * x[1] ** 2
    for x, y in product(circle, repeat=2):
        check((quadratic(x) - quadratic(y)) ** 2 <= spread_sq * sq([x[j] - y[j] for j in range(2)]), "spectral_spread_chord")
        check(quadratic((-x[0], -x[1])) == quadratic(x), "antipodal_even")

for d in [2, 3, 4, 5, 17, 64]:
    for _ in range(100):
        eigenvalues = [F(RNG.randrange(-10 ** 6, 10 ** 6 + 1), 13) for _ in range(d)]
        spread = max(eigenvalues) - min(eigenvalues)
        midpoint = (max(eigenvalues) + min(eigenvalues)) / 2
        check(sum(abs(e - midpoint) for e in eigenvalues) <= d * spread / 2, "shifted_nuclear_norm")
        eigenvalues[RNG.randrange(d)] = F(0)
        rank = sum(e != 0 for e in eigenvalues)
        spread = max(eigenvalues) - min(eigenvalues)
        check(max(abs(e) for e in eigenvalues) <= spread, "low_rank_operator_norm")
        check(sum(abs(e) for e in eigenvalues) <= rank * spread, "low_rank_nuclear_norm")

# Exact balanced traces and scalar shift pairings, with repeated points allowed.
for _ in range(250):
    m = RNG.randrange(1, 13)
    points = [RNG.choice(circle) for _ in range(2 * m)]
    signs = [1] * m + [-1] * m
    omega = [[sum(signs[i] * points[i][a] * points[i][b] for i in range(2 * m)) for b in range(2)] for a in range(2)]
    check(omega[0][0] + omega[1][1] == 0, "balanced_trace")
    a, b, c, shift = [F(RNG.randrange(-100, 101), 3) for _ in range(4)]
    pairing = a * omega[0][0] + 2 * b * omega[0][1] + c * omega[1][1]
    shifted = (a - shift) * omega[0][0] + 2 * b * omega[0][1] + (c - shift) * omega[1][1]
    check(pairing == shifted, "scalar_shift_pairing")

# Negative controls: show explicitly that crucial restrictions cannot be dropped.
M = F(10 ** 9)
for x in [-100, -1, 0, 1, 100]:
    check(M * max(0, x) - M * max(0, x) == 0, "dependent_row_negative_control")
check(2 * M * M > 0, "dependent_row_negative_control")
for x in circle:
    check(M * sq(x) == M, "radial_constant_negative_control")
check(M > 0, "radial_constant_negative_control")

# Core activation algebra at both boundary and interior arguments.
def psi(t):
    return t * t if abs(t) <= 1 else 2 * abs(t) - 1

for numerator in range(-100, 101):
    original_arg = F(numerator, 7)
    R = max(F(1), abs(original_arg))
    check(R * R * psi(original_arg / R) == original_arg * original_arg, "quadratic_core_scaling")
for a, b in product([F(j, 4) for j in range(-12, 13)], repeat=2):
    check(abs(psi(a) - psi(b)) <= 2 * abs(a - b), "quadratic_core_lipschitz")

result = {
    "status": "PASS",
    "assertions": sum(COUNTS.values()),
    "groups": dict(sorted(COUNTS.items())),
    "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    "scope": "Exact finite independent controls; stochastic theorems, infinite chaining and all-parameter quantifiers are verified analytically in INDEPENDENT_DERIVATION.md.",
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
Path(__file__).with_name("CONTROLS_RECEIPT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
