#!/usr/bin/env python3
"""New exact analytic falsification controls, independent of frozen diagnostics.

These finite checks are implementation diagnostics, not a universal proof of
the topological theorem. No floating-point decisions or external dependencies.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb
from pathlib import Path
import datetime
import hashlib
import json
import random
import sys

counts = Counter()
negative_controls = []


def require(statement, label):
    if not statement:
        raise AssertionError(label)
    counts[label] += 1


def changes(values):
    signs = [1 if v > 0 else -1 for v in values if v]
    return sum(a != b for a, b in zip(signs, signs[1:]))


def upper(values):
    """Closed zero-block formula, rather than frozen scripts' DP/brute force."""
    retained = [(j, 1 if v > 0 else -1) for j, v in enumerate(values) if v]
    if not retained:
        return len(values) - 1
    result = retained[0][0] + len(values) - retained[-1][0] - 1
    for (j, s), (h, t) in zip(retained, retained[1:]):
        available = h - j
        result += available - ((available % 2) != (s != t))
    return result


def brute_extrema(values):
    zero = [j for j, value in enumerate(values) if value == 0]
    vv = []
    for fill in product((-1, 1), repeat=len(zero)):
        x = list(values)
        for j, sign in zip(zero, fill):
            x[j] = sign
        vv.append(changes(x))
    return min(vv), max(vv)


def determinant(rows):
    a = [[Q(x) for x in row] for row in rows]
    out = Q(1)
    for j in range(len(a)):
        pivot = next((h for h in range(j, len(a)) if a[h][j]), None)
        if pivot is None:
            return Q(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            out = -out
        v = a[j][j]
        out *= v
        for h in range(j + 1, len(a)):
            scale = a[h][j] / v
            for k in range(j + 1, len(a)):
                a[h][k] -= scale * a[j][k]
            a[h][j] = 0
    return out


def apply_matrix(a, x):
    return [sum(v * c for v, c in zip(row, x)) for row in a]


def sign_blocks(x):
    blocks = []
    for j, value in enumerate(x):
        if not value:
            continue
        sign = 1 if value > 0 else -1
        if not blocks or blocks[-1][0] != sign:
            blocks.append((sign, []))
        blocks[-1][1].append(j)
    return blocks


def polynomial_operator(coefficients, n):
    out = [Q(0)] * len(coefficients)
    for h, value in enumerate(coefficients):
        for j in range(h + 1):
            out[j] += value * n * comb(h, j)
        for j in range(1, h + 1):
            out[j] += value * comb(h, j - 1) * ((-1) ** (h - j + 1) - 1)
    return out


def evaluate(coefficients, node):
    out = Q(0)
    for value in reversed(coefficients):
        out = out * node + value
    return out


def polynomial_spectrum(n):
    columns = []
    for k in range(n + 1):
        col = polynomial_operator([Q(0)] * k + [Q(1)], n)
        columns.append(col + [Q(0)] * (n - k))
        require(col[k] == n - 2 * k, 'monomial_diagonal_integer_spectrum')
    out = []
    for k in range(n + 1):
        p = [Q(0)] * k + [Q(1)]
        lam = n - 2 * k
        for j in reversed(range(k)):
            p[j] = -sum(columns[h][j] * p[h] for h in range(j + 1, k + 1)) / (2 * (k - j))
        require(polynomial_operator(p, n) == [lam * c for c in p], 'triangular_polynomial_eigenidentity')
        vv = [evaluate(p, j) for j in range(n + 1)]
        for j in range(n + 1):
            lhs = ((n - j) * vv[j + 1] if j < n else 0) + (j * vv[j - 1] if j else 0)
            require(lhs == lam * vv[j], 'fresh_monic_evaluation_eigenidentity')
        if n <= 12:
            for h in range(k):
                require(sum(comb(n, j) * vv[j] * j ** h for j in range(n + 1)) == 0,
                        'fresh_eigenpolynomial_lower_moment_orthogonality')
        require(upper(vv) == k and changes(vv) == k, 'fresh_eigenpolynomial_zero_sensitive_oscillation')
        out.append(p)
    return out


def compound_moves(d, k, cut=None):
    states = list(combinations(range(d), k))
    graph = {s: [] for s in states}
    for s in states:
        for pos, j in enumerate(s):
            for target in (j - 1, j + 1):
                if not 0 <= target < d or target in s:
                    continue
                if cut is not None and min(j, target) == cut:
                    continue
                raw = list(s)
                raw[pos] = target
                inversions = sum(raw[h] > raw[t] for h in range(k) for t in range(h + 1, k))
                require(inversions == 0, 'no_crossing_compound_wedge_sign')
                graph[s].append(tuple(raw))
    return graph


def connected(graph):
    initial = next(iter(graph))
    stack = [initial]
    seen = {initial}
    while stack:
        for s in graph[stack.pop()]:
            if s not in seen:
                seen.add(s)
                stack.append(s)
    return len(seen) == len(graph)


def expect_failure(label, witness, statement):
    require(statement, 'negative_control_' + label)
    negative_controls.append({'label': label, 'expected_failure_detected': True, 'witness': witness})


def main():
    # Independently check the full zero-block formula, including d=1.
    for d in range(1, 9):
        for x in product((-1, 0, 1), repeat=d):
            lo, hi = brute_extrema(x)
            require(upper(x) == hi, 'closed_zero_block_splus_formula')
            if any(x):
                require(changes(x) == lo, 'minimum_completion_zero_blocks')

    # Completely different TP matrix family; arbitrary signed magnitudes.
    rng = random.Random(30001696)
    for d in range(2, 7):
        a = [[Q(1, j + h + 1) for h in range(d)] for j in range(d)]
        for k in range(1, d + 1):
            for rows in combinations(range(d), k):
                for cols in combinations(range(d), k):
                    require(determinant([[a[j][h] for h in cols] for j in rows]) > 0,
                            'hilbert_strict_tp_minors')
        vectors = list(product((-3, -1, 0, 1, 2), repeat=d)) if d <= 4 else [
            tuple(rng.choice((-100, -3, -1, 0, 0, 0, 1, 7, 200)) for _ in range(d)) for _ in range(600)]
        vectors += [tuple(Q(1, j + 1) if j == h else 0 for j in range(d)) for h in range(d)]
        for x in vectors:
            if not any(x):
                continue
            y = apply_matrix(a, x)
            blocks = sign_blocks(x)
            q = len(blocks)
            b = [[sum(abs(x[h]) * a[j][h] for h in indices) for _, indices in blocks] for j in range(d)]
            require(apply_matrix(b, [sign for sign, _ in blocks]) == y, 'sign_block_compression_identity')
            for rows in combinations(range(d), q):
                require(determinant([b[j] for j in rows]) > 0, 'ordered_block_compressed_minor')
            for rows in combinations(range(d), q + 1):
                minors = [determinant([b[j] for j in rows if j != omitted]) for omitted in rows]
                require(sum((-1) ** h * minor * y[j] for h, (j, minor) in enumerate(zip(rows, minors))) == 0,
                        'positive_cofactor_annihilation_identity')
                require(any(y[j] for j in rows), 'cofactor_nonzero_output_guard')
            require(upper(y) <= changes(x), 'hilbert_arbitrary_magnitudes_strict_variation')

    # Obtain the eigensystem without the frozen scripts' Krawtchouk formula.
    for n in range(1, 25):
        polynomial_spectrum(n)

    # Sharp sparse F vectors: barycentric Vandermonde circuits in physical
    # coordinates, not sampled eigenvector combinations. z_j=q_j/sqrt(w_j).
    for d in range(2, 13):
        for r in range(1, d):
            for support in combinations(range(d), r + 1):
                q = [Q(0)] * d
                for j in support:
                    denominator = 1
                    for h in support:
                        if h != j:
                            denominator *= j - h
                    q[j] = Q(1, denominator)
                for k in range(r):
                    require(sum(q[j] * j ** k for j in support) == 0, 'sparse_F_vandermonde_moment')
                require(changes(q) == r, 'sharp_sparse_F_sign_bound')
                require(upper(q) >= r, 'sparse_F_zero_block_splus')

    # Near-sharp low-degree E with roots both at and between grid nodes.
    for d in range(2, 11):
        for degree in range(d - 1):
            for roots in combinations(range(d), degree):
                values = []
                for j in range(d):
                    v = Q(1)
                    for h in roots:
                        v *= j - h
                    values.append(v)
                require(upper(values) == degree, 'maximal_grid_zeros_sharp_E_bound')
            half_roots = [Q(2 * h + 1, 2) for h in range(degree)]
            repeated_roots = [Q(h // 2) for h in range(degree)]
            for roots in (half_roots, repeated_roots):
                values = []
                for j in range(d):
                    v = Q(1)
                    for h in roots:
                        v *= j - h
                    values.append(v)
                require(upper(values) <= degree, 'between_node_and_repeated_roots_E_bound')

    # All singleton spectral supports test exact extremal gaps; mixtures test
    # zeros among coefficients and the derivative/ratio proof independently.
    eps = Q(1, 8)
    for n in range(1, 17):
        for r in range(1, n + 1):
            weights = [({j: Q(1)}, {h: Q(1)}) for j in range(r) for h in range(r, n + 1)]
            ee = {0: Q(1)} if r == 1 else {0: Q(1, 3), r - 1: Q(2, 3)}
            ff = {r: Q(1)} if r == n else {r: Q(4, 7), n: Q(3, 7)}
            weights.append((ee, ff))
            for e, f in weights:
                for a in (Q(1, 64), Q(1, 8), Q(1, 2), Q(1), Q(3), Q(64)):
                    ev = sum(value * a ** (2 * k) for k, value in e.items())
                    fv = sum(value * a ** (2 * k) for k, value in f.items())
                    ratio2 = fv / ev
                    slope = sum(k * value * a ** (2 * k) for k, value in f.items()) / fv - sum(
                        k * value * a ** (2 * k) for k, value in e.items()) / ev
                    require(1 <= slope <= n, 'sparse_spectral_log_derivative')
                    require(a ** (2 * n) <= ratio2 <= a ** 2 if a <= 1 else a ** 2 <= ratio2 <= a ** (2 * n),
                            'sparse_spectral_uniform_ratio_bounds')
                    require(not ratio2 < eps ** (2 * n) or a < eps, 'uniform_core_neighborhood_implication')
                    if n == 1:
                        require(ratio2 == a * a and slope == 1, 'N1_exact_ratio_edge')

    # Compound connectivity and critical hypothesis mutation.
    for d in range(2, 11):
        for k in range(1, d):
            require(connected(compound_moves(d, k)), 'fresh_compound_connectivity')
            for cut in range(d - 1):
                require(not connected(compound_moves(d, k, cut)), 'cut_edge_compound_disconnection')

    # Cutoff condition numbers: beta arbitrarily close to epsilon, or huge.
    for m in range(1, 65):
        for beta in (eps + Q(1, 2 ** m), Q(2 ** m)):
            def h(a):
                return a if a <= eps else eps + (1 - eps) * (a - eps) / (beta - eps)
            def inverse(b):
                return b if b <= eps else eps + (beta - eps) * (b - eps) / (1 - eps)
            points = [eps / 2, eps] + [eps + (beta - eps) * Q(j, 16) for j in range(1, 17)]
            require(h(beta) == 1, 'near_degenerate_cutoff_endpoint')
            require(all(h(a) < h(b) for a, b in zip(points, points[1:])), 'near_degenerate_cutoff_monotonicity')
            for a in points:
                require(inverse(h(a)) == a, 'near_degenerate_cutoff_exact_inverse')
                require((h(a) <= eps) == (a <= eps), 'near_degenerate_cutoff_fixed_neighborhood')

    expect_failure('TN_is_not_strict_TP', {'A': 'identity_3', 'x': [1, 0, 0], 'sminus_x': 0, 'splus_Ax': 2},
                   upper([1, 0, 0]) > changes([1, 0, 0]))
    expect_failure('zero_input_guard_required', {'A': 'any_3_by_3_TP', 'x': [0, 0, 0]},
                   upper([0, 0, 0]) > changes([0, 0, 0]))
    # Positive, symmetric, irreducible generator with a long jump: J=ones-I.
    # At t=log 2 its exponential is (1/2)I+(7/6)ones, exactly rational.
    a = [[Q(7, 6) + (Q(1, 2) if j == h else 0) for h in range(3)] for j in range(3)]
    bad_minor = determinant([[a[j][h] for h in (1, 2)] for j in (0, 1)])
    x = [Q(10), Q(-9), Q(-1, 10)]
    y = apply_matrix(a, x)
    expect_failure('positive_long_jump_generator_not_TP', {'generator': 'ones_3-I_3', 'time': 'log(2)',
                   'minor_rows': [0, 1], 'minor_cols': [1, 2], 'minor': str(bad_minor),
                   'x': list(map(str, x)), 'Ax': list(map(str, y))},
                   bad_minor == Q(-7, 12) and upper(y) == 2 and changes(x) == 1)
    expect_failure('cut_edge_not_strict_trap', {'generator': '0_direct_sum_adjacent_2_block', 'x': [1, 0, 0]},
                   not connected(compound_moves(3, 1, 0)) and upper([1, 0, 0]) > changes([1, 0, 0]))
    expect_failure('overlapping_spectral_support_not_section', {'E_index': 1, 'F_index': 1,
                   'ratio_squared_at_a=1/2': '1', 'ratio_squared_at_a=2': '1'},
                   Q(1, 2) ** 2 / Q(1, 2) ** 2 == Q(2) ** 2 / Q(2) ** 2)
    expect_failure('reversed_spectral_order_wrong_monotonicity', {'E_index': 1, 'F_index': 0,
                   'ratio_squared_at_a=1/2': '4', 'ratio_squared_at_a=2': '1/4'},
                   Q(1, 2) ** -2 > Q(2) ** -2)
    expect_failure('cutoff_beta_below_epsilon', {'epsilon': str(eps), 'beta': str(eps / 2),
                   'slope': str((1 - eps) / (eps / 2 - eps))},
                   (1 - eps) / (eps / 2 - eps) < 0)
    # Naive h_s(a)=a/beta(s) need not extend at a higher-dimensional core.
    # E indices 0,1; F index 2. Rational circle parametrization lets every
    # finite step be checked exactly. The original E ratio is identically 1,
    # the rescaled ratios identically beta, and F/E ratios tend to zero.
    for m in range(2, 66):
        t = Q(1, 2 ** m)
        u0, u1 = 2 * t / (1 + t * t), (1 - t * t) / (1 + t * t)
        a = u0 / u1
        require(u0 * u0 + u1 * u1 == 1, 'naive_rescaling_rational_section')
        require(u0 / (a * u1) == 1, 'naive_rescaling_identical_original_E_direction')
        original_R2 = a ** 4 / (u0 ** 2 + (a * u1) ** 2)
        require(original_R2 <= 4 * t * t, 'naive_rescaling_original_approaches_core')
        for beta in (Q(1), Q(2)):
            b = a / beta
            require(u0 / (b * u1) == beta, 'naive_rescaling_distinct_output_E_directions')
            image_R2 = b ** 4 / (u0 ** 2 + (b * u1) ** 2)
            require(image_R2 <= 8 * t * t, 'naive_rescaling_images_approach_different_core_points')
    expect_failure('naive_core_rescaling_direction_dependence', {'E_indices': [0, 1], 'F_index': 2,
                   'original_limit_E_ratio': '1', 'output_limit_E_ratios': ['1', '2'],
                   'beta_on_F_components': ['1', '2'], 'scope': 'toy continuous hitting graph; necessity control, not a counterexample to C_i'},
                   Q(1) != Q(2))

    receipt = {'status': 'PASS', 'created_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'runtime': sys.version, 'arithmetic': 'exact Python integers and fractions',
               'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'assertions': sum(counts.values()), 'counts': dict(sorted(counts.items())),
               'negative_controls': negative_controls,
               'scope': 'Finite new diagnostics and deliberately falsified mutations; universal analytic verification is in FIRST_PASS_SEALED.md.'}
    Path(__file__).with_name('new_control_results.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
