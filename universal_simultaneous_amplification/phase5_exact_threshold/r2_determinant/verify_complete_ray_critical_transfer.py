#!/usr/bin/env python3
"""Exact audit of the complete-ray critical transfer.

The matrix identities are general.  The deterministic colour-order and
derivative screens are exact finite evidence only.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from math import comb

import sympy as sp
from flint import fmpq as Q, fmpq_mat

from verify_complete_refresh_forest import flint_active, sympy_active


def complete_data(P):
    n = len(P)
    P0 = [
        [sp.Integer(0) if i == j else sp.Rational(1, n - 1)
         for j in range(n)]
        for i in range(n)
    ]
    states, kernel0 = sympy_active(P0)
    actual_states, kernel = sympy_active(P)
    assert states == actual_states
    size = len(states)
    one = sp.ones(size, 1)
    nu0 = sp.Matrix([[
        sp.Rational(B.bit_count(), n * (n - 1) * 2 ** (n - 2))
        for B, _ in states
    ]])
    c0 = sp.Rational(2 ** (n - 1) - 1, (n - 1) * 2 ** (n - 2))
    q = sp.Matrix([sp.Rational(1, B.bit_count()) - c0 for B, _ in states])
    return states, kernel0, kernel, nu0, one, q


def stationary_row(kernel):
    size = kernel.rows
    matrix = sp.eye(size) - kernel.T
    matrix[size - 1, :] = sp.ones(1, size)
    rhs = sp.zeros(size, 1)
    rhs[size - 1] = 1
    return matrix.inv(method="DM") * rhs


def transfer_audit(P):
    states, K0, K, nu0, one, q = complete_data(P)
    size = len(states)
    identity = sp.eye(size)
    delta = K - K0
    B0 = identity - K0 + one * nu0
    G = B0.inv()
    h = G * q
    r = one - h
    T = G * delta
    projection = identity - r * nu0

    assert sp.simplify((nu0 * h)[0]) == 0
    assert sp.simplify((nu0 * r)[0]) == 1
    assert (identity - K0) * h == q
    assert sp.simplify((nu0 * T * r)[0]) == 0

    for alpha in (sp.Rational(1, 5), sp.Rational(2, 3)):
        Kalpha = K0 + alpha * delta
        L = identity - alpha * T
        A = identity - Kalpha + q * nu0
        C = identity - Kalpha + one * nu0
        assert B0 * L == C
        assert B0 * (projection - alpha * T) == A

        stationary = stationary_row(Kalpha).T
        assert stationary * Kalpha == stationary
        assert sp.simplify((stationary * one)[0]) == 1
        f_direct = sp.simplify((stationary * q)[0])
        f_transfer = sp.simplify(1 - (nu0 * L.inv() * r)[0])
        assert f_direct == f_transfer
        assert sp.simplify(A.det() - C.det() * f_direct) == 0

        R = L.inv()
        derivative = sp.simplify(-(nu0 * R * T * R * r)[0])
        second = sp.simplify(-2 * (nu0 * R * T * R * T * R * r)[0])
        epsilon = sp.symbols("epsilon")
        local = sp.simplify(1 - (nu0 * (identity - epsilon * T).inv() * r)[0])
        assert sp.simplify(sp.diff(local, epsilon).subs(epsilon, alpha) - derivative) == 0
        assert sp.simplify(sp.diff(local, epsilon, 2).subs(epsilon, alpha) - second) == 0

        W = delta * G * delta * h
        assert sp.simplify(f_direct - alpha**2 * (stationary * W)[0]) == 0

    # Coordinate form of the double-root transfer.  The first coordinate is
    # r and the remaining columns span ker(nu0).
    pivot = size - 1
    columns = [r]
    for j in range(size - 1):
        column = sp.zeros(size, 1)
        column[j] = 1
        column[pivot] = -nu0[j] / nu0[pivot]
        columns.append(column)
    change = sp.Matrix.hstack(*columns)
    inverse = change.inv()
    assert inverse[0, :] == nu0
    block = inverse * T * change
    assert block[0, 0] == 0
    b = block[0, 1:]
    c = block[1:, 0]
    D = block[1:, 1:]
    for alpha in (sp.Rational(1, 4), sp.Rational(3, 5)):
        E = sp.eye(size - 1) - alpha * D
        lhs = (identity - (K0 + alpha * delta) + q * nu0).det()
        rhs = sp.simplify(
            -B0.det() * alpha**2 * E.det() * (b * E.inv() * c)[0]
        )
        assert sp.simplify(lhs - rhs) == 0


def power_from_integer_values(values):
    differences = []
    row = values
    while row:
        differences.append(row[0])
        row = [row[i + 1] - row[i] for i in range(len(row) - 1)]
    degree = max((i for i, value in enumerate(differences) if value), default=0)
    power = [Q(0) for _ in range(degree + 1)]
    falling = [Q(1)]
    for j in range(degree + 1):
        for k, value in enumerate(falling):
            power[k] += differences[j] * value
        next_falling = [Q(0) for _ in range(len(falling) + 1)]
        for k, value in enumerate(falling):
            next_falling[k] -= Q(j, j + 1) * value
            next_falling[k + 1] += Q(1, j + 1) * value
        falling = next_falling
    return power


def bernstein(power, degree):
    return [
        sum((
            power[j] * Q(comb(k, j), comb(degree, j))
            for j in range(min(k, len(power) - 1) + 1)
        ), Q(0))
        for k in range(degree + 1)
    ]


def polynomial_pair(weights):
    n = len(weights)
    complete_weights = [
        [0 if i == j else 1 for j in range(n)] for i in range(n)
    ]
    states, kernel = flint_active(weights)
    complete_states, complete = flint_active(complete_weights)
    assert states == complete_states
    size = len(states)
    identity = fmpq_mat(size, size, [
        int(i == j) for i in range(size) for j in range(size)
    ])
    direction = complete - kernel
    denominator = n * (n - 1) * 2 ** (n - 2)
    c0 = Q(2 ** (n - 1) - 1, (n - 1) * 2 ** (n - 2))

    bases = []
    for signed in (True, False):
        base = identity - complete
        for i, (B, _) in enumerate(states):
            reward = Q(1, B.bit_count()) - c0 if signed else Q(1)
            for j, (C, _) in enumerate(states):
                base[i, j] += reward * Q(C.bit_count(), denominator)
        bases.append(base)

    values = [
        [(base + alpha * direction).det() for alpha in range(size)]
        for base in bases
    ]
    return size, [power_from_integer_values(row) for row in values]


def multiply(left, right):
    answer = [Q(0) for _ in range(len(left) + len(right) - 1)]
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            answer[i + j] += x * y
    return answer


def derivative(power):
    return [Q(i) * power[i] for i in range(1, len(power))]


def subtract(left, right):
    answer = [Q(0) for _ in range(max(len(left), len(right)))]
    for i, value in enumerate(left):
        answer[i] += value
    for i, value in enumerate(right):
        answer[i] -= value
    while len(answer) > 1 and not answer[-1]:
        answer.pop()
    return answer


def forest_order_audit(weights):
    size, (numerator, trees) = polynomial_pair(weights)
    natural_degree = size - 1
    n_controls = bernstein(numerator, natural_degree)
    z_controls = bernstein(trees, natural_degree)
    assert all(value >= 0 for value in z_controls)
    for j in range(natural_degree):
        if z_controls[j] and z_controls[j + 1]:
            assert (
                n_controls[j + 1] * z_controls[j]
                >= n_controls[j] * z_controls[j + 1]
            )

    J = subtract(
        multiply(derivative(numerator), trees),
        multiply(numerator, derivative(trees)),
    )
    assert all(value >= 0 for value in bernstein(J, len(J) - 1))


def deterministic_forest_audit():
    counts = {}
    for n in (3, 4):
        targets_by_row = [tuple(j for j in range(n) if j != i) for i in range(n)]
        tested = 0
        for targets in product(*targets_by_row):
            weights = [
                [0 if i == j else int(targets[i] == j) for j in range(n)]
                for i in range(n)
            ]
            forest_order_audit(weights)
            tested += 1
        counts[f"directed-deterministic-n{n}"] = tested
    print("PASS (EXACT FINITE): natural tree-colour ratio order", counts)
    print("PASS (EXACT FINITE): derivative numerator Bernstein controls")


def decimal(value):
    return sp.Rational(Fraction(value))


def convexity_witness_audit():
    P0 = [
        [0, decimal(".0022551449725194826"), decimal(".9977448550274805")],
        [decimal(".99996654568273524"), 0, decimal(".00003345431726476")],
        [decimal(".99997740241812971"), decimal(".00002259758187029"), 0],
    ]
    P1 = [
        [0, decimal(".0000016744373884679674"), decimal(".9999983255626115")],
        [decimal(".052268871860027794"), 0, decimal(".947731128139972206")],
        [decimal(".99999999997881195"), decimal(".00000000002118805"), 0],
    ]
    # The displayed decimal rows in the hostile-search record were rounded
    # at their last digit.  Normalize those exact decimal rationals before
    # rebuilding the Markov chains.
    for matrix in (P0, P1):
        for i, row in enumerate(matrix):
            total = sum(row)
            matrix[i] = [value / total for value in row]
    assert all(sum(row) == 1 for row in P0 + P1)

    def stationary_scalar(P):
        _, K0, K, _, _, q = complete_data(P)
        del K0
        stationary = stationary_row(K).T
        return sp.factor((stationary * q)[0])

    t = sp.Rational(9, 10)
    midpoint = [
        [(1 - t) * P0[i][j] + t * P1[i][j] for j in range(3)]
        for i in range(3)
    ]
    gap = sp.factor(
        (1 - t) * stationary_scalar(P0)
        + t * stationary_scalar(P1)
        - stationary_scalar(midpoint)
    )
    assert gap < 0

    def integer_row_weights(P):
        weights = []
        for row in P:
            denominator = sp.ilcm(*[value.q for value in row])
            weights.append([int(value * denominator) for value in row])
        return weights

    forest_order_audit(integer_row_weights(P0))
    forest_order_audit(integer_row_weights(P1))
    print("PASS (EXACT REFUTATION): joint affine convexity gap is negative")
    print("PASS (EXACT FINITE): both hostile complete rays retain colour order")


def pointwise_quadratic_obstruction():
    P = [
        [0, sp.Rational(1, 2), sp.Rational(1, 2)],
        [sp.Rational(1, 3), 0, sp.Rational(2, 3)],
        [sp.Rational(1, 4), sp.Rational(3, 4), 0],
    ]
    states, K0, K, nu0, one, q = complete_data(P)
    G = (sp.eye(len(states)) - K0 + one * nu0).inv()
    h = G * q
    W = (K - K0) * G * (K - K0) * h
    index = {state: i for i, state in enumerate(states)}
    assert W[index[(1 << 0, 1)]] == -sp.Rational(1, 3564)
    assert any(value < 0 for value in W)
    print("PASS (EXACT REFUTATION): the quadratic observable is not pointwise positive")


def compressed_transfer(P):
    states, K0, K, nu0, one, q = complete_data(P)
    size = len(states)
    G = (sp.eye(size) - K0 + one * nu0).inv()
    r = one - G * q
    T = G * (K - K0)
    columns = [r]
    for j in range(size - 1):
        column = sp.zeros(size, 1)
        column[j] = 1
        column[size - 1] = -nu0[j] / nu0[size - 1]
        columns.append(column)
    change = sp.Matrix.hstack(*columns)
    block = change.inv() * T * change
    return block[0, 1:], block[1:, 0], block[1:, 1:]


def stieltjes_obstruction_audit():
    P = [
        [0, sp.Rational(1, 3), sp.Rational(2, 3)],
        [sp.Rational(2, 5), 0, sp.Rational(3, 5)],
        [sp.Rational(4, 7), sp.Rational(3, 7), 0],
    ]
    b, c, D = compressed_transfer(P)
    assert any(D[i, i] < 0 for i in range(D.rows))
    assert any(D[i, i] > 0 for i in range(D.rows))
    assert sp.factor(D[0, 1] * D[1, 0]) == -sp.Rational(63985, 276623424)
    assert sp.trace(D**3) == -sp.Rational(256, 114345)

    x = sp.symbols("x")
    characteristic = sp.factor(D.charpoly(x).as_expr())
    expected_characteristic = (
        x**2 * (
            24012450 * x**6 - 1045605 * x**4 + 17920 * x**3
            + 1420 * x**2 - 9
        ) / 24012450
    )
    assert sp.expand(characteristic - expected_characteristic) == 0
    assert sp.Poly(characteristic, x).count_roots(-sp.oo, sp.oo) == 3

    alpha = sp.symbols("alpha")
    transfer = sp.cancel((b * (sp.eye(D.rows) - alpha * D).inv() * c)[0])
    expected = (
        9 * alpha**4 - 1594 * alpha**2 - 23040 * alpha + 561649
    ) / (
        3 * (
            9 * alpha**6 - 1420 * alpha**4 - 17920 * alpha**3
            + 1045605 * alpha**2 - 24012450
        )
    )
    assert sp.cancel(transfer - expected) == 0
    denominator = sp.cancel(transfer).as_numer_denom()[1]
    assert sp.Poly(denominator, alpha).degree() == 6
    assert sp.Poly(denominator, alpha).count_roots(-sp.oo, sp.oo) == 2

    P_end = [
        [0, sp.Rational(11, 26), sp.Rational(15, 26)],
        [sp.Rational(4, 5), 0, sp.Rational(1, 5)],
        [sp.Rational(19, 39), sp.Rational(20, 39), 0],
    ]
    b_end, c_end, _ = compressed_transfer(P_end)
    assert sp.factor(b_end[6] * c_end[6]) == sp.Rational(83, 9034740)
    print("PASS (EXACT REFUTATION): literal substochastic/oscillatory transfer")
    print("PASS (EXACT REFUTATION): rational Stieltjes and opposite-orthant routes")


def monotonicity_refutation_audit():
    n = 5
    values = (10, 100, 10, 1000, 10000, 1, 1, 1, 1, 10000)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    weights = [[0 for _ in range(n)] for _ in range(n)]
    for value, (i, j) in zip(values, pairs):
        weights[i][j] = weights[j][i] = value

    complete_weights = [
        [0 if i == j else 1 for j in range(n)] for i in range(n)
    ]
    states, kernel = flint_active(weights)
    complete_states, complete = flint_active(complete_weights)
    assert states == complete_states
    size = len(states)
    identity = fmpq_mat(size, size, [
        int(i == j) for i in range(size) for j in range(size)
    ])
    delta = kernel - complete
    one = fmpq_mat(size, 1, [Q(1) for _ in range(size)])
    nu0 = fmpq_mat(size, 1, [
        Q(B.bit_count(), n * (n - 1) * 2 ** (n - 2)) for B, _ in states
    ])
    q = fmpq_mat(size, 1, [
        Q(1, B.bit_count()) - Q(15, 32) for B, _ in states
    ])

    def outer(left, right):
        return fmpq_mat(left.nrows(), right.nrows(), [
            left[i, 0] * right[j, 0]
            for i in range(left.nrows()) for j in range(right.nrows())
        ])

    def evaluate(alpha):
        active = complete + alpha * delta
        stationary = (
            identity - active + outer(one, nu0)
        ).transpose().solve(nu0)
        f = (stationary.transpose() * q)[0, 0]
        fundamental = identity - active + outer(one, stationary)
        h = fundamental.solve(q)
        fp = (stationary.transpose() * delta * h)[0, 0]
        return f, fp

    f97, fp97 = evaluate(Q(97, 100))
    assert Q(98, 1000) < f97 < Q(99, 1000)
    assert -Q(17, 1000) < fp97 < -Q(16, 1000)
    f1, fp1 = evaluate(Q(1))
    assert Q(75, 1000) < f1 < Q(76, 1000)
    assert -Q(3580, 1000) < fp1 < -Q(3579, 1000)

    natural_size, (numerator, trees) = polynomial_pair(weights)
    assert natural_size == 75
    n_controls = bernstein(numerator, natural_size - 1)
    z_controls = bernstein(trees, natural_size - 1)
    assert all(value > 0 for value in z_controls)
    bad_ratios = [
        j for j in range(natural_size - 1)
        if n_controls[j + 1] * z_controls[j]
        < n_controls[j] * z_controls[j + 1]
    ]
    assert bad_ratios == [70, 71, 72, 73]
    assert n_controls[0] == n_controls[1] == 0
    assert all(value > 0 for value in n_controls[2:])

    J = subtract(
        multiply(derivative(numerator), trees),
        multiply(numerator, derivative(trees)),
    )
    j_controls = bernstein(J, len(J) - 1)
    assert len(J) - 1 == 138
    assert j_controls[0] == 0
    assert all(value > 0 for value in j_controls[1:132])
    assert all(value < 0 for value in j_controls[132:])
    print("PASS (EXACT REFUTATION): undirected complete-ray monotonicity and CT")
    print("PASS (EXACT): witness retains every fixed-colour numerator sign")
    print("PASS (EXACT): derivative controls have one + to - sign change")


def main():
    transfer_audit([
        [0, sp.Rational(1, 3), sp.Rational(2, 3)],
        [sp.Rational(2, 5), 0, sp.Rational(3, 5)],
        [sp.Rational(4, 7), sp.Rational(3, 7), 0],
    ])
    # A second independent directed specialization.  Keeping the symbolic
    # transfer checks at n=3 makes the replay memory-bounded; the separate
    # FLINT forest audit below covers every deterministic n=4 endpoint.
    transfer_audit([
        [0, sp.Rational(4, 5), sp.Rational(1, 5)],
        [sp.Rational(1, 7), 0, sp.Rational(6, 7)],
        [sp.Rational(3, 8), sp.Rational(5, 8), 0],
    ])
    print("PASS: exact all-order complete-ray transfer identities")
    deterministic_forest_audit()
    convexity_witness_audit()
    pointwise_quadratic_obstruction()
    stieltjes_obstruction_audit()
    monotonicity_refutation_audit()
    print("OPEN: all-order fixed-colour numerator sign and no-downcrossing")


if __name__ == "__main__":
    main()
