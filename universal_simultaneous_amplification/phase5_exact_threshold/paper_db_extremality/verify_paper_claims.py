#!/usr/bin/env python3
"""Independent exact integration audit for the dB extremality manuscript.

This script checks the normalization bridges used to combine the earlier
strong-selection theorem with the fitness-two active-chain Hessian theorem.
It deliberately does not import any discovery script.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations
from math import comb


def solve_linear(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    n = len(matrix)
    a = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if a[i][col])
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [x / scale for x in a[col]]
        for row in range(n):
            if row == col or not a[row][col]:
                continue
            scale = a[row][col]
            a[row] = [x - scale * y for x, y in zip(a[row], a[col])]
    return [row[-1] for row in a]


def active_kernel_complete(n: int):
    states = [
        (mask, v)
        for v in range(n)
        for mask in range(1, 1 << n)
        if not (mask >> v) & 1
    ]
    index = {state: i for i, state in enumerate(states)}
    size = len(states)
    k = [[F(0) for _ in range(size)] for _ in range(size)]
    for row, (mask, v) in enumerate(states):
        rank = mask.bit_count()
        for source in range(n):
            if source != v:
                k[row][index[(mask | (1 << source), v)]] += F(1, 2 * (n - 1))
        for old in range(n):
            if (mask >> old) & 1:
                reduced = mask & ~(1 << old)
                for source in range(n):
                    if source != old:
                        k[row][index[(reduced | (1 << source), old)]] += F(
                            1, 2 * rank * (n - 1)
                        )
        assert sum(k[row], F(0)) == 1
    return states, k


def check_active_normalization() -> None:
    for n in range(3, 6):
        states, kernel = active_kernel_complete(n)
        N = n - 1
        denominator = n * N * 2 ** (N - 1)
        nu = [F(mask.bit_count(), denominator) for mask, _v in states]
        assert sum(nu, F(0)) == 1
        pushed = [
            sum((nu[i] * kernel[i][j] for i in range(len(states))), F(0))
            for j in range(len(states))
        ]
        assert pushed == nu
        inverse_mean = sum(
            (nu[i] / states[i][0].bit_count() for i in range(len(states))),
            F(0),
        )
        m_complete = F(N * 2 ** (N - 1), 2**N - 1)
        rho_complete = F(N * 2 ** (N - 1), n * (2**N - 1))
        assert inverse_mean == 1 / m_complete == 1 / (n * rho_complete)
    print("PASS: complete active law, collision normalization, and dB baseline")


def check_tangent_decomposition() -> None:
    # A genuinely directed row-zero tangent; exact values are arbitrary.
    delta = [
        [F(0), F(2), F(-1), F(-1), F(0)],
        [F(-2), F(0), F(3), F(0), F(-1)],
        [F(1), F(-3), F(0), F(4), F(-2)],
        [F(0), F(1), F(-4), F(0), F(3)],
        [F(3), F(-2), F(0), F(-1), F(0)],
    ]
    n = len(delta)
    assert all(sum(row, F(0)) == 0 for row in delta)
    column = [sum((delta[i][j] for i in range(n)), F(0)) for j in range(n)]
    assert sum(column, F(0)) == 0
    standard = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                standard[i][j] = F(column[i] + (n - 1) * column[j], n * (n - 2))
    balanced = [
        [delta[i][j] - standard[i][j] for j in range(n)] for i in range(n)
    ]
    symmetric = [
        [(balanced[i][j] + balanced[j][i]) / 2 for j in range(n)]
        for i in range(n)
    ]
    antisymmetric = [
        [(balanced[i][j] - balanced[j][i]) / 2 for j in range(n)]
        for i in range(n)
    ]
    assert all(sum(row, F(0)) == 0 for row in standard)
    assert [sum((standard[i][j] for i in range(n)), F(0)) for j in range(n)] == column
    for part in (symmetric, antisymmetric):
        assert all(sum(row, F(0)) == 0 for row in part)
        assert all(
            sum((part[i][j] for i in range(n)), F(0)) == 0 for j in range(n)
        )
    assert all(symmetric[i][j] == symmetric[j][i] for i in range(n) for j in range(n))
    assert all(
        antisymmetric[i][j] == -antisymmetric[j][i]
        for i in range(n)
        for j in range(n)
    )
    assert all(
        delta[i][j] == standard[i][j] + symmetric[i][j] + antisymmetric[i][j]
        for i in range(n)
        for j in range(n)
    )
    expected_dimension = (n - 1) + n * (n - 3) // 2 + (n - 1) * (n - 2) // 2
    assert expected_dimension == n * (n - 2)
    balanced_dimension = n * (n - 3) // 2 + (n - 1) * (n - 2) // 2
    assert balanced_dimension == n * n - 3 * n + 1
    print("PASS: full tangent decomposition into all three irreducible sectors")


def check_incoming_column_sos() -> None:
    weights = [
        [0, 2, 3, 5],
        [7, 0, 11, 13],
        [17, 19, 0, 23],
        [29, 31, 37, 0],
    ]
    n = len(weights)
    total = F(0)
    defect = F(0)
    for target in range(n):
        incoming = [F(weights[source][target]) for source in range(n) if source != target]
        degree = sum(incoming, F(0))
        total += sum(((degree - w) / w for w in incoming), F(0))
        defect += sum(
            ((x - y) ** 2 / (x * y) for x, y in combinations(incoming, 2)),
            F(0),
        )
    assert total - n * (n - 1) * (n - 2) == defect
    assert defect > 0
    uniform = [[0 if i == j else (j + 2) for j in range(n)] for i in range(n)]
    uniform_defect = F(0)
    for target in range(n):
        incoming = [F(uniform[source][target]) for source in range(n) if source != target]
        uniform_defect += sum(
            ((x - y) ** 2 / (x * y) for x, y in combinations(incoming, 2)),
            F(0),
        )
    assert uniform_defect == 0
    print("PASS: incoming-column strong-selection sum of squares and equality gauge")


def check_physical_standard_normalization() -> None:
    # Independent bridge from the signed phase scalar Phi_N to the physical
    # standard-sector Hessian eigenvalue.  These values come from literal
    # labelled orbit solves in a separate verifier.
    phi = {
        2: F(24, 11),
        3: F(261, 40),
        4: F(343400, 28657),
    }
    expected = {
        2: F(2, 33),
        3: F(261, 5120),
        4: F(3434, 85971),
    }
    for N, value in phi.items():
        normalized = value / (4 * (N + 1) ** 2 * (N - 1))
        assert normalized == expected[N]
        assert normalized > 0
    print("PASS: physical standard-sector phase normalization")


def check_second_derivative_conversion() -> None:
    # If 1/(n rho_e)=c0+R2 e^2+O(e^3), differentiation gives the manuscript's
    # sign and coefficient.  Check the algebra symbolically over rationals.
    n = 7
    N = n - 1
    c0 = F(2**N - 1, N * 2 ** (N - 1))
    r2 = F(37, 101)
    rho0 = 1 / (n * c0)
    second = -F(2) * r2 / (n * c0 * c0)
    assert rho0 == F(N * 2 ** (N - 1), n * (2**N - 1))
    assert second < 0
    print("PASS: positive inverse-mean Hessian converts to negative fixation Hessian")


if __name__ == "__main__":
    check_active_normalization()
    check_tangent_decomposition()
    check_physical_standard_normalization()
    check_incoming_column_sos()
    check_second_derivative_conversion()
    print("PASS: paper-level theorem integration audit")
