#!/usr/bin/env python3
"""Exact verifier for RESOLVENT_IDENTITIES.md.

The code uses Fraction arithmetic throughout.  It independently constructs
the geometric-union kernels, solves the stationary equations, checks the
midpoint identity, and evaluates the two counterexamples.
"""

from __future__ import annotations

from fractions import Fraction as F


class CertificateFailure(RuntimeError):
    """Raised when an explicit certificate check fails."""


def require(condition, detail="certificate check failed"):
    """Raise a failure that remains active under optimized Python."""
    if not condition:
        raise CertificateFailure(str(detail))


def inverse(matrix: list[list[F]]) -> list[list[F]]:
    n = len(matrix)
    aug = [row[:] + [F(int(i == j)) for j in range(n)]
           for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for row in range(n):
            if row == col:
                continue
            scale = aug[row][col]
            if scale:
                aug[row] = [x - scale * y for x, y in zip(aug[row], aug[col])]
    return [row[n:] for row in aug]


def union_law(row: list[F]) -> dict[int, F]:
    support = [i for i, x in enumerate(row) if x]
    values = [F(0) for _ in range(1 << len(support))]
    for mask in range(1, 1 << len(support)):
        mass = sum(row[support[j]] for j in range(len(support))
                   if mask >> j & 1)
        values[mask] = mass / (2 - mass)
    for j in range(len(support)):
        for mask in range(1 << len(support)):
            if mask >> j & 1:
                values[mask] -= values[mask ^ (1 << j)]
    answer = {}
    for mask in range(1, 1 << len(support)):
        actual = sum(1 << support[j] for j in range(len(support))
                     if mask >> j & 1)
        if values[mask]:
            answer[actual] = values[mask]
    require(sum(answer.values()) == 1)
    return answer


def solve(weights: list[list[int]]):
    n = len(weights)
    P = [[F(weights[i][j], sum(weights[i])) for j in range(n)]
         for i in range(n)]
    states = list(range(1, (1 << n) - 1))
    index = {state: pos for pos, state in enumerate(states)}
    laws = [union_law(P[v]) for v in range(n)]
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
            require(sum(kernel[index[A]]) == 1)
        kernels.append(kernel)
        for i in range(len(states)):
            for j in range(len(states)):
                average[i][j] += kernel[i][j] / n

    size = len(states)
    matrix = [[average[j][i] - F(int(i == j)) for j in range(size)]
              for i in range(size)]
    matrix[-1] = [F(1) for _ in range(size)]
    rhs = [F(0) for _ in range(size)]
    rhs[-1] = F(1)
    inv = inverse(matrix)
    pi = [sum(inv[i][j] * rhs[j] for j in range(size))
          for i in range(size)]
    require(sum(pi) == 1)
    require(all(x > 0 for x in pi))
    return P, states, index, kernels, pi


def measures(weights: list[list[int]]):
    P, states, index, kernels, pi = solve(weights)
    n = len(P)
    full_size = 1 << n
    pi_all = [F(0) for _ in range(full_size)]
    for A, value in zip(states, pi):
        pi_all[A] = value

    nu = [[F(0) for _ in range(full_size)] for _ in range(n)]
    sigma = [[F(0) for _ in range(full_size)] for _ in range(n)]
    for v in range(n):
        mu = [sum(pi[a] * kernels[v][a][b] for a in range(len(states)))
              for b in range(len(states))]
        for B, value in zip(states, mu):
            if not (B >> v) & 1:
                nu[v][B] = value - pi_all[B]
        for C in range(full_size):
            if not (C >> v) & 1:
                sigma[v][C] = pi_all[C | (1 << v)]

    def add(v: int, eta: list[F]) -> list[F]:
        answer = [F(0) for _ in range(full_size)]
        for C, mass in enumerate(eta):
            if not mass:
                continue
            for i in range(n):
                answer[C | (1 << i)] += mass * P[v][i]
        return answer

    nu_add = [add(v, nu[v]) for v in range(n)]
    sigma_add = [add(v, sigma[v]) for v in range(n)]
    for v in range(n):
        for B in range(full_size):
            require(2 * nu[v][B] == sigma_add[v][B] + nu_add[v][B])

    mean = sum(pi_all[B] * B.bit_count() for B in states)
    qmass = n - mean
    energy = sum(
        nu[v][B] ** 2 / pi_all[B]
        for v in range(n) for B in states if not (B >> v) & 1
    )
    add_energy = sum(
        nu_add[v][B] ** 2 / pi_all[B]
        for v in range(n) for B in states if not (B >> v) & 1
    )
    i2 = 1 + mean / n + energy / n

    # Verify the pointwise aggregate effective-incoming identity.
    for B in states:
        require(sum(nu[v][B] for v in range(n) if not (B >> v) & 1) \
            == B.bit_count() * pi_all[B])

    revealed_excess = sum(
        sum(nu[v][B] ** 2 / pi_all[B]
            for v in range(n) if not (B >> v) & 1) / B.bit_count()
        for B in states
    )
    return mean, qmass, energy, add_energy, i2, revealed_excess


def main() -> None:
    path = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
    mean, qmass, energy, add_energy, i2, revealed = measures(path)
    require(mean == F(11, 9))
    require(qmass == F(16, 9))
    require(energy == F(13, 9))
    require(add_energy == F(19, 9))
    require(i2 == F(17, 9))
    require(add_energy - energy == F(2, 3))

    triangle = [[0, 7, 1], [7, 0, 1], [1, 1, 0]]
    values = measures(triangle)
    revealed_gap = values[-1] - 1
    require(revealed_gap > 0)

    print("PASS: exact midpoint resolvent on the path and weighted triangle")
    print(f"PASS: path L2 expansion = {add_energy-energy}")
    print(f"PASS: path I2 = {i2} < 2")
    print(f"PASS: (7,1,1)-triangle revealed-flag excess = {revealed_gap}")
    print("OPEN: universal stationary target inequality I2<=2")


if __name__ == "__main__":
    main()
