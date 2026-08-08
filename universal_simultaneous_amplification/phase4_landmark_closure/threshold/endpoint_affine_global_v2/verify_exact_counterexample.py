#!/usr/bin/env python3
"""Exact endpoint counterexample from the full two-count orbit chain.

The graph has a two-vertex class A and a twenty-vertex class B.  Its edge
weights are 137 inside A, 1 inside B, and 1/500 across the classes.  The
automorphism group is ``S_2 x S_20``; hence a mutant configuration is an
orbit exactly when its two mutant counts agree.  The program derives every
orbit-to-orbit changing rate from the microscopic update rules and solves
both absorbing systems over QQ using FLINT.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction as F

from flint import fmpq, fmpq_mat


R = F(3, 2)
A = 2
B = 20
N = A + B
W_AA = F(137)
W_BB = F(1)
W_AB = F(1, 500)


def fq(value: F) -> fmpq:
    return fmpq(value.numerator, value.denominator)


def digest(value: F) -> str:
    return hashlib.sha256(f"{value.numerator}/{value.denominator}".encode()).hexdigest()


def states():
    return tuple(
        (i, j)
        for i in range(A + 1)
        for j in range(B + 1)
        if (i, j) not in ((0, 0), (A, B))
    )


def changing_rates(state, rule: str):
    """Aggregate labelled target/source events directly from the rules."""
    i, j = state
    degree_a = (A - 1) * W_AA + B * W_AB
    degree_b = (B - 1) * W_BB + A * W_AB
    moves = []
    if rule == "Bd":
        if i < A:
            parent_mass = i * W_AA / degree_a + j * W_AB / degree_b
            moves.append(((i + 1, j), R * (A - i) * parent_mass))
        if i:
            parent_mass = (A - i) * W_AA / degree_a + (B - j) * W_AB / degree_b
            moves.append(((i - 1, j), i * parent_mass))
        if j < B:
            parent_mass = j * W_BB / degree_b + i * W_AB / degree_a
            moves.append(((i, j + 1), R * (B - j) * parent_mass))
        if j:
            parent_mass = (B - j) * W_BB / degree_b + (A - i) * W_AB / degree_a
            moves.append(((i, j - 1), j * parent_mass))
    elif rule == "dB":
        if i < A:
            mutant_weight = i * W_AA + j * W_AB
            resident_weight = degree_a - mutant_weight
            moves.append(
                ((i + 1, j), (A - i) * R * mutant_weight / (R * mutant_weight + resident_weight))
            )
        if i:
            mutant_weight = (i - 1) * W_AA + j * W_AB
            resident_weight = degree_a - mutant_weight
            moves.append(
                ((i - 1, j), i * resident_weight / (R * mutant_weight + resident_weight))
            )
        if j < B:
            mutant_weight = j * W_BB + i * W_AB
            resident_weight = degree_b - mutant_weight
            moves.append(
                ((i, j + 1), (B - j) * R * mutant_weight / (R * mutant_weight + resident_weight))
            )
        if j:
            mutant_weight = (j - 1) * W_BB + i * W_AB
            resident_weight = degree_b - mutant_weight
            moves.append(
                ((i, j - 1), j * resident_weight / (R * mutant_weight + resident_weight))
            )
    else:
        raise ValueError(rule)
    return tuple((target, rate) for target, rate in moves if rate)


def fixation(rule: str) -> F:
    transient = states()
    index = {state: row for row, state in enumerate(transient)}
    matrix = fmpq_mat(len(transient), len(transient))
    rhs = fmpq_mat(len(transient), 1)
    for state, row in index.items():
        moves = changing_rates(state, rule)
        matrix[row, row] = fq(sum((rate for _, rate in moves), F(0)))
        for target, rate in moves:
            if target == (A, B):
                rhs[row, 0] += fq(rate)
            elif target != (0, 0):
                matrix[row, index[target]] -= fq(rate)
    solution = matrix.solve(rhs)
    value = F(A, N) * F(int(solution[index[(1, 0)], 0].p), int(solution[index[(1, 0)], 0].q))
    value += F(B, N) * F(int(solution[index[(0, 1)], 0].p), int(solution[index[(0, 1)], 0].q))

    # Independent exact row residual and boundary checks.
    assert matrix * solution == rhs
    assert 0 < value < 1
    return value


def baseline(rule: str) -> F:
    if rule == "Bd":
        return F(3 ** (N - 1), 3**N - 2**N)
    return F((N - 1) * 3 ** (N - 2), N * (3 ** (N - 1) - 2 ** (N - 1)))


def weak_cut_limit() -> tuple[F, F]:
    """Independent rare-event formula at cross weight tending to zero."""
    sigma = F((B - 1), (A - 1) * 137)

    def bd_complete(order):
        return (1 - 1 / R) / (1 - R ** (-order))

    def db_complete(order):
        return (1 - 1 / R) * F(order - 1, order) / (1 - R ** (1 - order))

    z_ba = sigma * R**B * (R**A - 1) / (R**B - 1)
    z_bb = sigma ** (-1) * R**A * (R**B - 1) / (R**A - 1)
    z_da = (
        sigma ** (-1)
        * F(A * (B - 1), B * (A - 1))
        * R**B
        * (R ** (A - 1) - 1)
        / (R ** (B - 1) - 1)
    )
    z_db = (
        sigma
        * F(B * (A - 1), A * (B - 1))
        * R**A
        * (R ** (B - 1) - 1)
        / (R ** (A - 1) - 1)
    )
    rho_b = F(A, N) * bd_complete(A) * z_ba / (1 + z_ba)
    rho_b += F(B, N) * bd_complete(B) * z_bb / (1 + z_bb)
    rho_d = F(A, N) * db_complete(A) * z_da / (1 + z_da)
    rho_d += F(B, N) * db_complete(B) * z_db / (1 + z_db)
    return rho_b, rho_d


def main() -> None:
    rho_b = fixation("Bd")
    rho_d = fixation("dB")
    x = rho_b / baseline("Bd")
    y = rho_d / baseline("dB")
    excess = (x + 2 * y) / 3 - 1
    crossing = (y - 1) / (y - x)
    assert F(9334, 10000) < x < F(9335, 10000)
    assert F(10336, 10000) < y < F(10337, 10000)
    assert F(2, 10000) < excess < F(3, 10000)
    assert x < 1 < y
    assert F(3355, 10000) < crossing < F(3356, 10000)
    assert crossing > F(1, 3)

    limit_b, limit_d = weak_cut_limit()
    limit_excess = (limit_b / baseline("Bd") + 2 * limit_d / baseline("dB")) / 3 - 1
    assert limit_excess > F(4, 10000)

    print(f"order={N}, orbit states={len(states())}")
    print("weights: AA=137, BB=1, AB=1/500")
    print(f"x~{float(x):.15g} y~{float(y):.15g} excess~{float(excess):.15g}")
    print(f"rho_Bd hash={digest(rho_b)}")
    print(f"rho_dB hash={digest(rho_d)}")
    print(f"affine-excess hash={digest(excess)}")
    print(f"theta_0~{float(crossing):.15g} hash={digest(crossing)}")
    print(f"weak-limit excess~{float(limit_excess):.15g} hash={digest(limit_excess)}")
    print("PASS exact connected weighted K_2--K_20 one-third counterexample")


if __name__ == "__main__":
    main()
