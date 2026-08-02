#!/usr/bin/env python3
"""Independent exact checks for M1_PARTIAL_CLOSURE.md.

All theorem checks use Fraction arithmetic.  The final complete-graph
chi-square equality is also checked exactly by constructing the full
geometric-union kernel and solving its stationary equations with SymPy.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations

import sympy as sp


def popcount(value: int) -> int:
    """Return the number of set bits (compatible with the verifier's Python 3.9 runtime)."""
    return bin(value).count("1")


def inverse(matrix: list[list[F]]) -> list[list[F]]:
    n = len(matrix)
    aug = [row[:] + [F(int(i == j)) for j in range(n)] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [value / scale for value in aug[col]]
        for row in range(n):
            if row == col:
                continue
            scale = aug[row][col]
            if scale:
                aug[row] = [a - scale * b for a, b in zip(aug[row], aug[col])]
    return [row[n:] for row in aug]


def transition(weights: list[list[int]]) -> list[list[F]]:
    return [
        [F(value, sum(row)) for value in row]
        for row in weights
    ]


def h(value: F) -> F:
    return 2 * value / (1 + value)


def direct_linear_drift(P: list[list[F]], z: list[F], state: int) -> F:
    n = len(P)
    H = [[h(P[v][i]) for i in range(n)] for v in range(n)]
    total = F(0)
    for v in range(n):
        if not (state >> v) & 1:
            continue
        total += z[v]
        for i in range(n):
            if not (state >> i) & 1:
                total -= H[v][i] * z[i]
    return total


def check_subtheorem(weights: list[list[int]]) -> int:
    P = transition(weights)
    n = len(P)
    H = [[h(P[v][i]) for i in range(n)] for v in range(n)]
    T = [sum(H[v][i] for v in range(n)) for i in range(n)]
    S = sum(F(1, 1) / (1 + value) for value in T)
    if S < F(n, 2):
        return 0
    lam = F(n - 2, 1) / (S - 1)
    z = [lam / (1 + value) for value in T]
    Z = sum(z)
    assert Z <= n
    checks = 0
    for state in range(1, (1 << n) - 1):
        holes = [i for i in range(n) if not (state >> i) & 1]
        direct = direct_linear_drift(P, z, state)
        target = 2 * popcount(state) - n
        formula = -(len(holes) - 1) * (Z - n)
        formula += sum(
            z[i] * H[j][i] + z[j] * H[i][j]
            for i, j in combinations(holes, 2)
        )
        assert direct - target == formula
        assert formula >= 0
        checks += 1
    return checks


def exact_union_law(row: list[F]) -> dict[int, F]:
    support = [i for i, value in enumerate(row) if value]
    m = len(support)
    values = [F(0) for _ in range(1 << m)]
    for mask in range(1, 1 << m):
        mass = sum(row[support[j]] for j in range(m) if (mask >> j) & 1)
        values[mask] = mass / (2 - mass)
    for j in range(m):
        for mask in range(1 << m):
            if (mask >> j) & 1:
                values[mask] -= values[mask ^ (1 << j)]
    answer = {}
    for mask in range(1, 1 << m):
        if values[mask]:
            actual = sum(1 << support[j] for j in range(m) if (mask >> j) & 1)
            answer[actual] = values[mask]
    assert sum(answer.values()) == 1
    return answer


def exact_stationary_and_i2(weights: list[list[int]]) -> tuple[list[F], F]:
    P = transition(weights)
    n = len(P)
    states = list(range(1, 1 << n))
    index = {state: pos for pos, state in enumerate(states)}
    laws = [exact_union_law(row) for row in P]
    kernels = []
    average = [[F(0) for _ in states] for _ in states]
    for v in range(n):
        kernel = [[F(0) for _ in states] for _ in states]
        for A in states:
            if not (A >> v) & 1:
                kernel[index[A]][index[A]] = F(1)
            else:
                for U, probability in laws[v].items():
                    B = (A & ~(1 << v)) | U
                    kernel[index[A]][index[B]] += probability
            assert sum(kernel[index[A]]) == 1
        kernels.append(kernel)
        for i in range(len(states)):
            for j in range(len(states)):
                average[i][j] += kernel[i][j] / n

    size = len(states)
    matrix = sp.Matrix(
        [[sp.Rational(average[j][i].numerator, average[j][i].denominator)
          - int(i == j) for j in range(size)] for i in range(size)]
    )
    matrix[size - 1, :] = sp.ones(1, size)
    rhs = sp.zeros(size, 1)
    rhs[size - 1] = 1
    solution = matrix.inv() * rhs
    pi = [F(int(value.p), int(value.q)) for value in solution]
    assert sum(pi) == 1

    i2 = F(0)
    for v in range(n):
        mu = [
            sum(pi[a] * kernels[v][a][b] for a in range(size))
            for b in range(size)
        ]
        for b in range(size):
            if pi[b]:
                i2 += mu[b] * mu[b] / (n * pi[b])
    return pi, i2


def main() -> None:
    # Rational directed rows are allowed by the theorem.  These examples
    # satisfy S_H >= n/2 and exercise heterogeneous columns.
    examples = [
        [[0, 1, 1], [1, 0, 1], [1, 1, 0]],
        [[0, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]],
        [[0, 1, 1, 1, 1], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0],
         [1, 0, 0, 0, 0], [1, 0, 0, 0, 0]],
        [[0, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0],
         [1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0]],
        [[0, 2, 1, 1], [2, 0, 1, 1], [1, 1, 0, 2], [1, 1, 2, 0]],
        [[0, 9, 1, 1, 1], [9, 0, 1, 1, 1], [1, 1, 0, 1, 1],
         [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]],
    ]
    theorem_checks = sum(check_subtheorem(weights) for weights in examples)
    assert theorem_checks > 0

    # Formula (23): compare the declared coefficients against direct drift
    # for one rational graph and arbitrary signed b / nonnegative q.
    weights = examples[4]
    P = transition(weights)
    n = len(P)
    H = [[h(P[v][i]) for i in range(n)] for v in range(n)]
    T = [sum(H[v][i] for v in range(n)) for i in range(n)]
    b = [F(-3), F(-2), F(-5, 2), F(-7, 3)]
    q = {(i, j): F(i + j + 1, 7) for i, j in combinations(range(n), 2)}
    c = [b[i] - sum(q[min(i, j), max(i, j)] for j in range(n) if j != i)
         for i in range(n)]
    alpha0 = -sum(b) - n
    alpha1 = [
        b[i] * (1 + T[i])
        + sum((1 - H[v][i]) * q[min(i, v), max(i, v)]
              for v in range(n) if v != i)
        + 2
        for i in range(n)
    ]
    alpha2 = {}
    for i, j in combinations(range(n), 2):
        L = 2 - H[i][j] - H[j][i] + sum(
            h(P[v][i] + P[v][j]) for v in range(n) if v not in (i, j)
        )
        alpha2[i, j] = -H[i][j] * b[j] - H[j][i] * b[i] - L * q[i, j]
    alpha3 = {}
    for i, j, k in combinations(range(n), 3):
        alpha3[i, j, k] = (
            q[i, j] * h(P[k][i] + P[k][j])
            + q[i, k] * h(P[j][i] + P[j][k])
            + q[j, k] * h(P[i][j] + P[i][k])
        )
        assert alpha3[i, j, k] >= 0

    mobius_checks = 0
    for state in range(1, (1 << n) - 1):
        holes = [i for i in range(n) if not (state >> i) & 1]
        # Direct monomial drift using the exact one- and two-coordinate laws.
        direct = F(0)
        for i in range(n):
            direct += c[i] * (
                -1 if (state >> i) & 1
                else sum(H[v][i] for v in range(n) if (state >> v) & 1)
            )
        for i, j in combinations(range(n), 2):
            xi, xj = (state >> i) & 1, (state >> j) & 1
            if xi and xj:
                drift = F(-2)
            elif (not xi) and xj:
                drift = sum(H[v][i] for v in range(n)
                            if (state >> v) & 1 and v != j)
            elif xi and (not xj):
                drift = sum(H[v][j] for v in range(n)
                            if (state >> v) & 1 and v != i)
            else:
                drift = sum(
                    H[v][i] + H[v][j] - h(P[v][i] + P[v][j])
                    for v in range(n) if (state >> v) & 1
                )
            direct += q[i, j] * drift
        formula = alpha0
        formula += sum(alpha1[i] for i in holes)
        formula += sum(alpha2[i, j] for i, j in combinations(holes, 2))
        formula += sum(alpha3[i, j, k] for i, j, k in combinations(holes, 3))
        assert direct - (2 * popcount(state) - n) == formula
        mobius_checks += 1

    complete_i2 = []
    for n in range(3, 6):
        weights = [[0 if i == j else 1 for j in range(n)] for i in range(n)]
        pi, value = exact_stationary_and_i2(weights)
        assert value == 2
        P_complete = transition(weights)
        H_complete = [[h(P_complete[v][i]) for i in range(n)] for v in range(n)]
        T_complete = [sum(H_complete[v][i] for v in range(n)) for i in range(n)]
        S_complete = sum(F(1) / (1 + item) for item in T_complete)
        holes_mean = sum(
            pi[state - 1] * (n - popcount(state))
            for state in range(1, 1 << n)
        )
        internal = F(0)
        for state in range(1, 1 << n):
            holes = [i for i in range(n) if not (state >> i) & 1]
            internal += pi[state - 1] * sum(
                H_complete[v][i] / (1 + T_complete[i])
                for i in holes for v in holes
            )
        assert holes_mean == S_complete + internal
        complete_i2.append((n, value))

    print(f"PASS: {theorem_checks} exact theorem-state checks")
    print(f"PASS: {mobius_checks} exact quadratic-Mobius checks")
    print(f"PASS: exact complete-graph I2 equalities {complete_i2}")
    print("OPEN: universal I2<=2 and M1 outside S_H>=n/2")


if __name__ == "__main__":
    main()
