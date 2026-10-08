"""Independent exact CTMC diagnostics of PR141's joint-clock mechanism.

This finite-state analogue is not an approximation argument for Brownian motion.
The Brownian proof is assessed in REPORT.md. Checks remain active under -O.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, permutations, product
from math import factorial
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import sys

C = Counter()
NEGATIVE = []


def check(group, value):
    if not value:
        raise RuntimeError(group)
    C[group] += 1


def solve(matrix, right):
    n = len(right)
    aug = [[F(x) for x in row] + [F(b)] for row, b in zip(matrix, right)]
    for col in range(n):
        row = next(r for r in range(col, n) if aug[r][col])
        aug[col], aug[row] = aug[row], aug[col]
        divisor = aug[col][col]
        aug[col] = [x / divisor for x in aug[col]]
        for r in range(n):
            if r != col and aug[r][col]:
                scale = aug[r][col]
                aug[r] = [x - scale * y for x, y in zip(aug[r], aug[col])]
    answer = [aug[r][-1] for r in range(n)]
    check("independent_exact_linear_system_residual", all(
        sum(F(a) * x for a, x in zip(row, answer)) == F(b)
        for row, b in zip(matrix, right)))
    return answer


def direct_all_hitting_transform(L, targets, rates):
    """Global Feynman--Kac equations on (remaining-target-set, current-site).

    A unit-rate continuous-time symmetric walk jumps left/right with rate 1/2.
    The killing rate is sum(s_j for targets not hit yet). Upon first hitting
    a target, that target is removed. Previously hit sites remain traversable.
    This calculation never enumerates target permutations.
    """
    rate = dict(zip(targets, rates))

    @lru_cache(None)
    def block(A):
        A = frozenset(A)
        if not A:
            return tuple(F(1) for _ in range(L))
        sites = tuple(z for z in range(L) if z not in A)
        index = {z: j for j, z in enumerate(sites)}
        q = sum(rate[a] for a in A)
        matrix = [[F(0)] * len(sites) for _ in sites]
        right = [F(0)] * len(sites)
        for z in sites:
            j = index[z]
            matrix[j][j] = 1 + q
            for w in ((z - 1) % L, (z + 1) % L):
                if w in A:
                    right[j] += F(1, 2) * block(frozenset(A - {w}))[w]
                else:
                    matrix[j][index[w]] -= F(1, 2)
        solution = solve(matrix, right)
        return tuple(solution[index[z]] if z not in A else F(-1) for z in range(L))
    return block(frozenset(targets))


@lru_cache(None)
def one_stage_transform(L, A, destination, q):
    """Resolvent of the walk killed on A, with boundary 1 at destination.

    This is the exact CTMC counterpart of the displayed Brownian exit kernel's
    Laplace transform. Both neighboring directions are added for singleton A.
    """
    sites = tuple(z for z in range(L) if z not in A)
    index = {z: j for j, z in enumerate(sites)}
    matrix = [[F(0)] * len(sites) for _ in sites]
    right = [F(0)] * len(sites)
    for z in sites:
        j = index[z]
        matrix[j][j] = 1 + q
        for w in ((z - 1) % L, (z + 1) % L):
            if w in A:
                right[j] += F(1, 2) * int(w == destination)
            else:
                matrix[j][index[w]] -= F(1, 2)
    solution = solve(matrix, right)
    return tuple(solution[index[z]] if z not in A else F(-1) for z in range(L))


def permutation_transform(L, targets, rates, start, incorrect_increment_weights=False):
    """Integrate the order/increment product against exp(-sum(s_j T_j))."""
    rate = dict(zip(targets, rates))
    total = F(0)
    for order in permutations(targets):
        weight = F(1)
        for r, destination in enumerate(order):
            A = frozenset(order[r:])
            # Each elapsed increment contributes to ALL still-unhit targets'
            # absolute first-arrival times, including those not visited next.
            q = rate[destination] if incorrect_increment_weights else sum(rate[a] for a in A)
            z = start if r == 0 else order[r - 1]
            weight *= one_stage_transform(L, A, destination, q)[z]
        total += weight
    return total


configurations = 0
for L in range(3, 8):
    for m in range(1, min(4, L - 1) + 1):
        for targets in combinations(range(L), m):
            # Include asymmetric configurations, non-adjacent starts, zero
            # coordinates, all-zero transforms and unequal positive rates.
            rate_vectors = [tuple(F(0) for _ in targets),
                            tuple(F(j + 1, m + 2) for j in range(m)),
                            tuple(F(0) if j % 2 else F(3, 7) for j in range(m))]
            for rates in rate_vectors:
                direct = direct_all_hitting_transform(L, targets, rates)
                for start in range(L):
                    if start in targets:
                        continue
                    order_value = permutation_transform(L, targets, rates, start)
                    check("global_visited_set_vs_order_cumulative_time", direct[start] == order_value)
                    check("joint_transform_in_unit_interval", 0 <= order_value <= 1)
                    if not any(rates):
                        check("all_zero_rate_normalization", order_value == 1)
                    configurations += 1

# Falsify two realistic substitutes for the submission's correlated mechanism.
L, targets, rates, start = 7, (1, 4, 5), (F(1, 3), F(2, 5), F(3, 7)), 0
correct = permutation_transform(L, targets, rates, start)
wrong_increment = permutation_transform(L, targets, rates, start, True)
independent_clocks = F(1)
for target, rate in zip(targets, rates):
    independent_clocks *= one_stage_transform(L, frozenset({target}), target, rate)[start]
check("negative_control_raw_increment_weights_rejected", correct != wrong_increment)
check("negative_control_within_walker_independence_rejected", correct != independent_clocks)
NEGATIVE.append({"case": "correlated_clock_weights", "L": L, "targets": targets,
                 "rates": [str(x) for x in rates], "start": start,
                 "correct": str(correct), "wrong_increment": str(wrong_increment),
                 "wrong_independent_clocks": str(independent_clocks)})

# An explicit ownership example where comparing raw increments instead of
# physical cumulative times reverses the owner at the second query point.
orders = ((0, 1), (1, 0))
increments = ((F(2), F(1)), (F(5, 2), F(1, 5)))
physical = []
raw_by_target = []
for order, row in zip(orders, increments):
    h = [F(0), F(0)]
    raw = [F(0), F(0)]
    t = F(0)
    for j, dt in zip(order, row):
        t += dt
        h[j] = t
        raw[j] = dt
    physical.append(h)
    raw_by_target.append(raw)
owner = tuple(min(range(2), key=lambda i: physical[i][j]) for j in range(2))
raw_owner = tuple(min(range(2), key=lambda i: raw_by_target[i][j]) for j in range(2))
check("negative_control_raw_increment_owner_rejected", owner != raw_owner)
NEGATIVE.append({"case": "owner_reversal", "orders": orders,
                 "increments": [[str(x) for x in row] for row in increments],
                 "correct_owner": owner, "wrong_raw_increment_owner": raw_owner})

# Exact multi-index coefficient extraction from homogeneous moment polynomials,
# with irregular piece lengths and correlated label patterns on three outcomes.
piece_lengths = (F(1, 7), F(2, 7), F(4, 7))
outcomes = ((0, 1, 2), (2, 2, 0), (1, 0, 1))
weights = (F(1, 5), F(3, 10), F(1, 2))
length_vectors = []
for pattern in outcomes:
    length_vectors.append(tuple(sum(length for length, owner in zip(piece_lengths, pattern)
                                    if owner == label) for label in range(3)))
for m in range(7):
    coefficients = Counter()
    for samples in product(range(3), repeat=m):
        volume = F(1)
        for j in samples:
            volume *= piece_lengths[j]
        for pattern, weight in zip(outcomes, weights):
            multi_index = tuple(sum(pattern[j] == label for j in samples) for label in range(3))
            coefficients[multi_index] += weight * volume
    for nu in product(range(m + 1), repeat=3):
        if sum(nu) != m:
            continue
        expected = F(0)
        for weight, lengths in zip(weights, length_vectors):
            term = weight
            for length, exponent in zip(lengths, nu):
                term *= length ** exponent
            expected += term
        multiplier = F(factorial(m))
        for exponent in nu:
            multiplier /= factorial(exponent)
        check("mixed_moment_multinomial_coefficient", coefficients[nu] == multiplier * expected)
    for theta in ((F(0), F(0), F(0)), (F(2), F(2), F(2)), (F(1, 3), F(0), F(7, 5))):
        polynomial = F(0)
        for nu, value in coefficients.items():
            for th, exponent in zip(theta, nu):
                value *= th ** exponent
            polynomial += value
        direct = sum(weight * sum(th * length for th, length in zip(theta, lengths)) ** m
                     for weight, lengths in zip(weights, length_vectors))
        check("mixed_polynomial_vs_direct_bounded_moment", polynomial == direct)
        check("irregular_partition_theta_bound", 0 <= polynomial <= max(theta) ** m)

result = {"schema": "pr141-independent-joint-clock-controls/v1",
          "actual_pid": os.getpid(), "utc": datetime.now(timezone.utc).isoformat(),
          "optimized": bool(sys.flags.optimize), "verdict": "PASS",
          "assertions": sum(C.values()), "groups": dict(sorted(C.items())),
          "weighted_CTMC_configurations": configurations, "negative_controls": NEGATIVE,
          "scope": "Exact finite-state analogue and finite-probability-space identities; these controls do not prove Brownian convergence or the continuum law.",
          "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(result, indent=2, sort_keys=True))
