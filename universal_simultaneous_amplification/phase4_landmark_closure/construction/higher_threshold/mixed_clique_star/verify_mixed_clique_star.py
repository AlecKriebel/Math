#!/usr/bin/env python3
"""Exact verifier for the mixed-clique-star cross-sum certificate."""

from __future__ import annotations

from fractions import Fraction as F

import sympy as sp


def birth_death_fixation(up: list[F], down: list[F]) -> F:
    """Fixation from count one for a nearest-neighbor absorbing chain."""
    assert len(up) == len(down)
    product = F(1)
    denominator = F(1)
    for plus, minus in zip(up, down):
        product *= minus / plus
        denominator += product
    return 1 / denominator


def clique_values(size: int, fitness: F) -> tuple[F, F]:
    """Reconstruct uniform-singleton Bd and dB fixation from count rates."""
    bd_up: list[F] = []
    bd_down: list[F] = []
    db_up: list[F] = []
    db_down: list[F] = []
    for mutants in range(1, size):
        residents = size - mutants
        total_fitness = fitness * mutants + residents
        bd_up.append(
            fitness * mutants / total_fitness * F(residents, size - 1)
        )
        bd_down.append(
            residents / total_fitness * F(mutants, size - 1)
        )

        db_up.append(
            F(residents, size)
            * fitness * mutants
            / (fitness * mutants + residents - 1)
        )
        db_down.append(
            F(mutants, size)
            * residents
            / (fitness * (mutants - 1) + residents)
        )
    return birth_death_fixation(bd_up, bd_down), birth_death_fixation(db_up, db_down)


def declared_clique_values(size: int, fitness: F) -> tuple[F, F, F, F]:
    r = fitness
    a_bd = (r - 1) * r ** (size - 1) / (r**size - 1)
    b_bd = (r - 1) / (r**size - 1)
    a_db = (
        F(size - 1, size)
        * (r - 1)
        * r ** (size - 2)
        / (r ** (size - 1) - 1)
    )
    b_db = F(size - 1, size) * (r - 1) / (r ** (size - 1) - 1)
    return a_bd, b_bd, a_db, b_db


def handoff(size: int, fitness: F, scale: F) -> tuple[F, F]:
    r, z = fitness, scale
    amplitude = (r - 1) * r ** (size - 1)
    a = r**size - 1
    c = r * size * (r ** (size - 1) - 1) / (size - 1)
    return amplitude * z / (1 + a * z), amplitude / (z + c)


def finite_center_handoff(size: int, center: int, fitness: F, scale: F) -> tuple[F, F]:
    """Evaluate the exact finite-center gamma formulas used before the limit."""
    r, z = fitness, scale
    a_l_bd, b_l_bd, a_l_db, b_l_db = declared_clique_values(size, r)
    a_c_bd, b_c_bd, a_c_db, b_c_db = declared_clique_values(center, r)

    # These are the exact trace competition probabilities from the two
    # directional rate pairs; gamma=(1-A)/B.
    first_bd = r * a_c_bd / (r * a_c_bd + b_l_bd / z)
    second_bd = (r * a_l_bd / z) / (r * a_l_bd / z + b_c_bd)
    gamma_bd = (1 - first_bd) / second_bd

    first_db = (r * a_c_db / z) / (r * a_c_db / z + b_l_db / r)
    second_db = (r * a_l_db) / (r * a_l_db + b_c_db / (r * z))
    gamma_db = (1 - first_db) / second_db
    return a_l_bd * (1 - gamma_bd), a_l_db * (1 - gamma_db)


def symbolic_factorization(max_size: int = 12) -> int:
    r = sp.symbols("r")
    checks = 0
    for size in range(2, max_size + 1):
        a = r**size - 1
        c = r * size * (r ** (size - 1) - 1) / (size - 1)
        lhs = sp.factor(2 * (a * c - 1) - r**size * (a + c - 2))
        positive_sum = sum((k + 1) * r ** (size - 2 - k) for k in range(size - 1))
        rhs = (r - 1) ** 2 * (r**size - 2) * positive_sum / (size - 1)
        assert sp.factor(lhs - rhs) == 0

        z_star = (c - 1) / (a - 1)
        amplitude = (r - 1) * r ** (size - 1)
        total = amplitude * (z_star / (1 + a * z_star) + 1 / (z_star + c))
        maximum = amplitude * (a + c - 2) / (a * c - 1)
        assert sp.factor(total - maximum) == 0
        checks += 2
    return checks


def main() -> None:
    checks = symbolic_factorization()
    for size in range(2, 41):
        for r in (F(3, 2), F(8, 5), F(2), F(7, 3), F(5)):
            exact_bd, exact_db = clique_values(size, r)
            a_bd, b_bd, a_db, b_db = declared_clique_values(size, r)
            assert exact_bd == a_bd
            assert exact_db == a_db
            reverse_bd, reverse_db = clique_values(size, 1 / r)
            assert reverse_bd == b_bd
            assert reverse_db == b_db

            for z in (F(1, 17), F(2, 3), F(1), F(9, 5), F(13)):
                bd, db = handoff(size, r, z)
                baseline = 1 - 1 / r
                assert bd + db <= 2 * baseline
                assert (bd >= baseline) == (z >= 1)
                threshold = r * (size - r ** (size - 1)) / (size - 1)
                assert (db >= baseline) == (z <= threshold)

                # The finite-center trace converges to the declared handoff.
                finite_bd, finite_db = finite_center_handoff(size, 80, r, z)
                assert abs(finite_bd - bd) < F(1, 500)
                assert abs(finite_db - db) < F(1, 500)
                checks += 8

    print(f"PASS exact mixed-clique-star certificates checks={checks}")


if __name__ == "__main__":
    main()
