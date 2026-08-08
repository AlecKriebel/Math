#!/usr/bin/env python3
"""Exact verifier for the fixed-count two-replica reduction.

The analytic proof covers the antisymmetric sector in every order and the
entire directed three-vertex case.  The larger standard/symmetric loop is an
exact finite screen, not a universal proof.
"""

from __future__ import annotations

from fractions import Fraction as Q
from math import comb

import sympy as sp


def active_operator(rows):
    """Return the active operator over exact ``Fraction`` entries."""

    n = len(rows)
    states = [
        (B, v)
        for v in range(n)
        for B in range(1, 1 << n)
        if not (B >> v) & 1
    ]
    index = {state: i for i, state in enumerate(states)}
    matrix = [[Q(0) for _ in states] for _ in states]
    for source, (B, v) in enumerate(states):
        k = B.bit_count()
        for i, mass in enumerate(rows[v]):
            if mass:
                matrix[source][index[(B | (1 << i), v)]] += mass / 2
        for w in range(n):
            if (B >> w) & 1:
                C = B & ~(1 << w)
                for i, mass in enumerate(rows[w]):
                    if mass:
                        matrix[source][index[(C | (1 << i), w)]] += mass / (2 * k)
        assert sum(matrix[source], Q(0)) == 1 or sum(rows[v], Q(0)) == 0
    return states, matrix


def mat_vec(matrix, vector):
    return [sum((entry * value for entry, value in zip(row, vector)), Q(0)) for row in matrix]


def row_mat(row, matrix):
    return [
        sum((row[i] * matrix[i][j] for i in range(len(row))), Q(0))
        for j in range(len(row))
    ]


def dot(row, column):
    return sum((x * y for x, y in zip(row, column)), Q(0))


def rank_step(h, N):
    out = [Q(0)] * (N + 1)
    for k in range(1, N + 1):
        up = Q(N - k, 2 * N)
        down = Q(k - 1, 2 * N)
        out[k] = (1 - up - down) * h[k]
        if k < N:
            out[k] += up * h[k + 1]
        if k > 1:
            out[k] += down * h[k - 1]
    return out


def radial_differences(h, N):
    return [Q(0)] + [h[k] - h[k + 1] for k in range(1, N)] + [Q(0)]


def difference_step(d, N):
    out = [Q(0)] * (N + 1)
    for k in range(1, N):
        out[k] = d[k] / 2
        out[k] += Q(N - k - 1, 2 * N) * d[k + 1]
        out[k] += Q(k - 1, 2 * N) * d[k - 1]
    return out


def antisymmetric_feature_step(r, N):
    out = [Q(0)] * (N + 2)
    for k in range(1, N):
        out[k] = Q(k, 2 * N) * r[k]
        out[k] += Q(N - k - 1, 2 * N) * r[k + 1]
    return out


def antisymmetric_output(r, n):
    """Equation (31), divided by the Frobenius norm of the direction."""

    N = n - 1
    answer = Q(0)
    for k in range(1, N + 1):
        bracket = Q(k * (N - k), N - 1) * (r[k] - r[k + 1])
        bracket += (N - k) * r[k + 1]
        if k > 1:
            bracket += Q((k - 1) * (N - k + 1), N - 1) * (r[k - 1] - r[k])
        bracket += (N - k + 1) * r[k]
        assert bracket >= 0
        pi = Q(comb(N - 1, k - 1), 2 ** (N - 1))
        answer += pi * bracket / (2 * n * N)
    return answer


def antisymmetric_all_time_audit():
    """Audit the two elementary cone recurrences used in the all-n proof."""

    for n in range(3, 41):
        N = n - 1
        d = [Q(0)] + [Q(1, k * (k + 1)) for k in range(1, N)] + [Q(0)]
        for _m in range(41):
            assert all(d[k] > 0 for k in range(1, N))
            assert all(d[k] > d[k + 1] for k in range(1, N - 1))
            r = [value / 2 for value in d] + [Q(0)]
            for _ell in range(41):
                assert all(r[k] > 0 for k in range(1, N))
                assert all(r[k] >= r[k + 1] for k in range(1, N - 1))
                assert antisymmetric_output(r, n) > 0
                r = antisymmetric_feature_step(r, N)
            d = difference_step(d, N)
    print("PASS: exact positive/decreasing antisymmetric cones for n<=40, l,m<=40")
    print("PROVED ANALYTICALLY: every antisymmetric two-colour packet is positive")


def standard_force(h, n):
    N = n - 1
    d = radial_differences(h, N)
    a = [Q(0)] * (N + 1)
    b = [Q(0)] * (N + 1)
    D = n * (N - 1)
    for k in range(1, N + 1):
        a[k] = Q(k, 2 * D) * d[k]
        b[k] = Q(N, 2 * D) * d[k]
        if k > 1:
            b[k] += Q(k - 1, 2 * k * (N - 1)) * d[k - 1]
    return a, b


def standard_step(a, b, n):
    N = n - 1
    ap = [Q(0)] * (N + 1)
    bp = [Q(0)] * (N + 1)
    for k in range(1, N + 1):
        ap[k] = Q(k, 2 * N) * a[k]
        if k < N:
            ap[k] += Q(N - k, 2 * N) * a[k + 1] - Q(1, 2 * N) * b[k + 1]

        bp[k] = Q(k, 2 * N) * b[k]
        if k < N:
            bp[k] += Q(N - k - 1, 2 * N) * b[k + 1]
        if k > 1:
            bp[k] += Q(k - 1, 2 * k * N) * a[k - 1]
            bp[k] += Q((k - 1) ** 2, 2 * k * N) * b[k - 1]
        bp[k] += Q(N - k + 1, 2 * k * N) * a[k]
        bp[k] += Q(k * (N - k) - (N - k + 1), 2 * k * N) * b[k]
    return ap, bp


def standard_output(b, n):
    N = n - 1
    return sum(
        Q(comb(N - 1, k - 1), 2 ** (N - 1))
        * Q(N - k, n * (N - 1))
        * b[k]
        for k in range(1, N + 1)
    )


def symmetric_force(h, n):
    N = n - 1
    d = radial_differences(h, N)
    a = [Q(0)] * (N + 1)
    b = [Q(0)] * (N + 1)
    for k in range(1, N):
        a[k] = d[k] / 2
    for k in range(2, N):
        b[k] = d[k - 1] / (2 * k)
    return a, b


def symmetric_step(a, b, n):
    N = n - 1
    ap = [Q(0)] * (N + 1)
    bp = [Q(0)] * (N + 1)
    for k in range(1, N):
        ap[k] = Q(k, 2 * N) * a[k]
        if k < N - 1:
            ap[k] += Q(N - k - 1, 2 * N) * a[k + 1] - Q(1, N) * b[k + 1]
    for k in range(2, N):
        bp[k] = Q(N - k, 2 * k * N) * a[k]
        if k > 1:
            bp[k] += Q(k - 1, 2 * k * N) * a[k - 1]
            bp[k] += Q((k - 1) * (k - 2), 2 * k * N) * b[k - 1]
        bp[k] += Q(k, 2 * N) * b[k]
        bp[k] += Q(k * (N - k - 1) - 2 * (N - k), 2 * k * N) * b[k]
        if k < N - 1:
            bp[k] += Q(N - k - 2, 2 * N) * b[k + 1]
    return ap, bp


def symmetric_output(a, b, n):
    N = n - 1
    answer = Q(0)
    for k in range(1, N):
        pi = Q(comb(N - 1, k - 1), 2 ** (N - 1))
        r = a[k] - Q(2 * (k - 1), N - 2) * b[k]
        answer += pi * Q(N - k, (N - 1) * (N + 1)) * r
    return answer


def add_pair(left, right):
    return (
        [x + y for x, y in zip(left[0], right[0])],
        [x + y for x, y in zip(left[1], right[1])],
    )


def exact_sector_screen():
    """Fast exact screen of the two unresolved forced rank systems."""

    counts = {"standard": 0, "symmetric": 0}
    for n in range(4, 32):
        N = n - 1
        h = [Q(0)] + [Q(1, k) for k in range(1, N + 1)]
        std = None
        sym = None
        for lag in range(101):
            std_source = standard_force(h, n)
            sym_source = symmetric_force(h, n)
            if lag == 0:
                std = std_source
                sym = sym_source
            else:
                std = add_pair(standard_step(*std, n), std_source)
                sym = add_pair(symmetric_step(*sym, n), sym_source)
            assert standard_output(std[1], n) >= 0
            assert symmetric_output(*sym, n) >= 0
            counts["standard"] += 1
            counts["symmetric"] += 1
            h = rank_step(h, N)
    print("PASS: exact unresolved-sector diagonal screen", counts)
    print("OPEN: all-n proof of the standard and symmetric diagonal signs")


def three_vertex_standard_gf():
    """Build the exact 9-state resolvent and prove all cumulative coefficients."""

    n = 3
    N = 2
    complete_rows = [
        [Q(0) if i == j else Q(1, N) for j in range(n)] for i in range(n)
    ]
    s = (Q(N), Q(-1), Q(-1))
    direction_rows = [
        [
            Q(0) if i == j else (s[i] + N * s[j]) / (n * (N - 1))
            for j in range(n)
        ]
        for i in range(n)
    ]
    states, K0 = active_operator(complete_rows)
    direction_states, Delta = active_operator(direction_rows)
    assert states == direction_states
    z = sp.symbols("z")
    K = sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in row] for row in K0])
    D = sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in row] for row in Delta])
    nu = sp.Matrix([[sp.Rational(B.bit_count(), 12) for B, _ in states]])
    H = sp.Matrix([sp.Rational(1, B.bit_count()) for B, _ in states])
    resolvent = (sp.eye(len(states)) - z * K).inv()
    norm_s = sum(value * value for value in s)
    diagonal_gf = sp.factor((nu * D * resolvent * D * resolvent * H)[0] / norm_s)
    expected = 2 * (z + 8) / (9 * (z**3 + 8 * z**2 - 40 * z + 64))
    assert sp.factor(diagonal_gf - expected) == 0

    # If S_d is the cumulative coefficient, S_d=2/33+r_d and
    # r_d=(5/8)r_(d-1)-(1/8)r_(d-2)-(1/64)r_(d-3).
    q = [Q(1, 36), Q(1, 48), Q(11, 1152)]
    S = [q[0], q[0] + q[1], sum(q, Q(0))]
    r = [value - Q(2, 33) for value in S]
    alpha = Q(13, 16)
    norm_at_two = max(abs(r[2]), alpha * abs(r[1]), alpha**2 * abs(r[0]))
    assert norm_at_two == Q(2197, 101376) < Q(2, 33)
    assert Q(5, 8) + Q(2, 13) + Q(4, 169) < alpha
    for degree in range(3, 301):
        next_r = Q(5, 8) * r[-1] - Q(1, 8) * r[-2] - Q(1, 64) * r[-3]
        r.append(next_r)
        assert abs(next_r) <= alpha ** (degree - 2) * norm_at_two
        assert Q(2, 33) + next_r > 0
    print("PASS: exact n=3 standard diagonal generating function")
    print("PROVED ANALYTICALLY: every cumulative n=3 standard coefficient is positive")


def matrix_product(left, right):
    return [
        [
            sum((left[i][k] * right[k][j] for k in range(len(right))), Q(0))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def matrix_power(matrix, exponent):
    answer = [[Q(i == j) for j in range(len(matrix))] for i in range(len(matrix))]
    while exponent:
        if exponent & 1:
            answer = matrix_product(answer, matrix)
        matrix = matrix_product(matrix, matrix)
        exponent //= 2
    return answer


def four_vertex_standard_gf():
    """Exact all-time positivity of the n=4 standard fixed-lag diagonal."""

    n = 4
    N = 3
    z = sp.symbols("z")

    # Build the two-feature and radial matrices from the recurrence itself.
    feature_dimension = 2 * N
    feature = sp.zeros(feature_dimension)
    for column in range(feature_dimension):
        a = [Q(0)] * (N + 1)
        b = [Q(0)] * (N + 1)
        (a if column < N else b)[column % N + 1] = Q(1)
        ap, bp = standard_step(a, b, n)
        values = ap[1:] + bp[1:]
        for row, value in enumerate(values):
            feature[row, column] = sp.Rational(value.numerator, value.denominator)

    source = sp.zeros(feature_dimension, N)
    rank = sp.zeros(N)
    for column in range(N):
        h = [Q(0)] * (N + 1)
        h[column + 1] = Q(1)
        a, b = standard_force(h, n)
        for row, value in enumerate(a[1:] + b[1:]):
            source[row, column] = sp.Rational(value.numerator, value.denominator)
        next_h = rank_step(h, N)
        for row, value in enumerate(next_h[1:]):
            rank[row, column] = sp.Rational(value.numerator, value.denominator)

    left = sp.zeros(1, feature_dimension)
    for k in range(1, N + 1):
        weight = Q(comb(N - 1, k - 1), 2 ** (N - 1)) * Q(N - k, n * (N - 1))
        left[0, N + k - 1] = sp.Rational(weight.numerator, weight.denominator)
    H = sp.Matrix([sp.Rational(1, k) for k in range(1, N + 1)])
    gf = sp.factor(
        (left * (sp.eye(feature_dimension) - z * feature).inv()
         * source * (sp.eye(N) - z * rank).inv() * H)[0]
    )
    expected = (
        9
        * (4 * z**5 - 13 * z**4 - 128 * z**3 + 807 * z**2 - 1809 * z + 1458)
        / (
            256
            * (z - 3)
            * (2 * z - 3)
            * (z**5 + z**4 - 54 * z**3 + 297 * z**2 - 621 * z + 486)
        )
    )
    assert sp.factor(gf - expected) == 0

    # Isolate the positive dominant term A*(2/3)^m.  The residual companion
    # is a strict contraction over blocks of length 21.
    coefficients = [
        Q(29, 18),
        -Q(28, 27),
        Q(17, 54),
        -Q(19, 486),
        -Q(1, 729),
        Q(1, 1458),
    ]
    companion = [coefficients] + [
        [Q(i == j) for j in range(6)] for i in range(5)
    ]
    block = matrix_power(companion, 21)
    block_norm = max(sum((abs(value) for value in row), Q(0)) for row in block)
    assert block_norm == Q(960357059082763123, 4918301009412067196928)
    assert block_norm < Q(2, 3) ** 21

    h = [Q(0)] + [Q(1, k) for k in range(1, N + 1)]
    response = None
    diagonal = []
    for lag in range(60):
        forcing = standard_force(h, n)
        response = forcing if lag == 0 else add_pair(standard_step(*response, n), forcing)
        diagonal.append(standard_output(response[1], n))
        h = rank_step(h, N)
    A = Q(55, 4032)
    lam = Q(2, 3)
    residual = [diagonal[m] - A * lam**m for m in range(len(diagonal))]
    for m in range(6, len(residual)):
        assert residual[m] == sum(
            coefficients[j] * residual[m - 1 - j] for j in range(6)
        )
    assert all(value > 0 for value in diagonal[:30])

    state_norm = max(abs(residual[30 - j]) for j in range(6))
    ratios = []
    for shift in range(21):
        first_row = matrix_power(companion, shift)[0]
        row_norm = sum((abs(value) for value in first_row), Q(0))
        ratios.append(row_norm * state_norm / (A * lam ** (30 + shift)))
    exact_maximum = Q(
        13143953338764611150595571035307,
        128945158113455203437948306456576,
    )
    assert max(ratios) == ratios[3] == exact_maximum < 1
    print("PASS: exact n=4 standard diagonal generating function and block contraction")
    print("PROVED ANALYTICALLY: every n=4 standard fixed-lag diagonal is positive")


def full_chain_packet_checks():
    """Check a negative atom and the triangular fixed-count identity directly."""

    n = 4
    N = 3
    complete_rows = [
        [Q(0) if i == j else Q(1, N) for j in range(n)] for i in range(n)
    ]
    symmetric = [[Q(0) for _ in range(n)] for _ in range(n)]
    for i, j, value in (
        (0, 1, 1),
        (0, 2, -1),
        (1, 3, -1),
        (2, 3, 1),
    ):
        symmetric[i][j] = symmetric[j][i] = Q(value)
    states, K0 = active_operator(complete_rows)
    direction_states, Delta = active_operator(symmetric)
    assert states == direction_states
    nu = [Q(B.bit_count(), n * N * 2 ** (N - 1)) for B, _ in states]
    H = [Q(1, B.bit_count()) for B, _ in states]
    packet = dot(row_mat(nu, Delta), mat_vec(K0, mat_vec(Delta, H)))
    assert packet == Q(-1, 36)

    # For t=5, average every word with two actual colours and compare with
    # the triangular Delta expansion.  A small directed rational kernel is
    # deliberately outside every balanced sector.
    rows = [
        [Q(0), Q(1, 6), Q(1, 3), Q(1, 2)],
        [Q(1, 4), Q(0), Q(1, 4), Q(1, 2)],
        [Q(1, 7), Q(2, 7), Q(0), Q(4, 7)],
        [Q(2, 5), Q(1, 5), Q(2, 5), Q(0)],
    ]
    actual_states, actual = active_operator(rows)
    assert actual_states == states
    Delta = [[actual[i][j] - K0[i][j] for j in range(len(states))] for i in range(len(states))]
    t = 5
    word_total = Q(0)
    for first in range(t):
        for second in range(first + 1, t):
            value = H
            for time in reversed(range(t)):
                value = mat_vec(actual if time in (first, second) else K0, value)
            word_total += dot(nu, value)
    word_average = word_total / comb(t, 2)
    baseline = dot(nu, H)
    triangular = Q(0)
    for ell in range(t - 1):
        for m in range(t - 1 - ell):
            value = H
            for _ in range(m):
                value = mat_vec(K0, value)
            value = mat_vec(Delta, value)
            for _ in range(ell):
                value = mat_vec(K0, value)
            value = mat_vec(Delta, value)
            triangular += dot(nu, value)
    assert word_average - baseline == triangular / comb(t, 2)
    print("PASS: exact negative symmetric atom Q_(1,0)=-1/36")
    print("PASS: independent full-chain fixed-count/triangular identity")


def main():
    full_chain_packet_checks()
    three_vertex_standard_gf()
    four_vertex_standard_gf()
    antisymmetric_all_time_audit()
    exact_sector_screen()


if __name__ == "__main__":
    main()
