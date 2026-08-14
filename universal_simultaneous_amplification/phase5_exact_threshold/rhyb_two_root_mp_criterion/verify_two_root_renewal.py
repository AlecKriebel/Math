#!/usr/bin/env python3
"""Exact replay for the normalizer-free two-root MP renewal reduction.

This verifies identities and a finite-depth pseudo-law obstruction.  The
pseudo-laws are intentionally not stationary at rank three and are not graph
counterexamples.  No graph or kernel enumeration is performed.
"""

from __future__ import annotations

from math import comb

import sympy as sp


def add_rate(row: dict[int, sp.Expr], state: int, destination: int, rate) -> None:
    """Add an off-diagonal generator rate to a sparse row."""

    rate = sp.sympify(rate)
    if destination != state and rate != 0:
        row[destination] = row.get(destination, sp.Integer(0)) + rate


def finish_row(state: int, row: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    """Insert the exact generator diagonal."""

    row[state] = -sum(row.values(), sp.Integer(0))
    return row


def submasks(mask: int):
    """Yield every submask of ``mask``."""

    value = mask
    while True:
        yield value
        if value == 0:
            return
        value = (value - 1) & mask


def geometric_union_law(order: int, fitness: sp.Expr, target: int):
    """Exact union law of a geometric number of complete-kernel samples."""

    support = ((1 << order) - 1) & ~(1 << target)
    row_mass = sp.Rational(1, order - 1)

    def pgf(mass):
        return mass / (fitness - (fitness - 1) * mass)

    law: dict[int, sp.Expr] = {}
    for target_set in submasks(support):
        if target_set == 0:
            continue
        probability = sp.Integer(0)
        for included in submasks(target_set):
            mass = row_mass * included.bit_count()
            probability += (
                (-1) ** (target_set.bit_count() - included.bit_count())
                * pgf(mass)
            )
        law[target_set] = sp.cancel(probability)
    assert sp.cancel(sum(law.values(), sp.Integer(0)) - 1) == 0
    assert all(probability > 0 for probability in law.values())
    return law


def bd_row(state: int, order: int, fitness: sp.Expr) -> dict[int, sp.Expr]:
    """One exact complete-kernel Bd-dual generator row."""

    row: dict[int, sp.Expr] = {}
    arrow_rate = sp.Rational(1, order - 1)
    for target in range(order):
        if not ((state >> target) & 1):
            continue
        for source in range(order):
            if source == target:
                continue
            neutral = (state & ~(1 << target)) | (1 << source)
            selective = state | (1 << source)
            add_rate(row, state, neutral, arrow_rate)
            add_rate(row, state, selective, (fitness - 1) * arrow_rate)
    return finish_row(state, row)


def db_row(
    state: int,
    order: int,
    union_laws: list[dict[int, sp.Expr]],
) -> dict[int, sp.Expr]:
    """One exact complete-kernel dB-dual generator row."""

    row: dict[int, sp.Expr] = {}
    for target in range(order):
        if not ((state >> target) & 1):
            continue
        retained = state & ~(1 << target)
        for parent_set, probability in union_laws[target].items():
            add_rate(row, state, retained | parent_set, probability)
    return finish_row(state, row)


def stationary_row(generator: sp.Matrix) -> list[sp.Expr]:
    """Solve a finite irreducible generator stationary law exactly."""

    system = generator.T.copy()
    rhs = sp.zeros(generator.rows, 1)
    for column in range(generator.cols):
        system[-1, column] = 1
    rhs[-1] = 1
    solution = list(sp.linsolve((system, rhs)).args[0])
    assert all(value >= 0 for value in solution)
    assert sp.factor(sum(solution) - 1) == 0
    return solution


def bd_rank_law(order: int, fitness: sp.Expr) -> list[sp.Expr]:
    """Exact complete-kernel Bd-dual rank law on ranks 1,...,s."""

    weights = [comb(order, rank) * (fitness - 1) ** rank for rank in range(1, order + 1)]
    normalizer = sum(weights, sp.Integer(0))
    law = [sp.cancel(weight / normalizer) for weight in weights]
    for rank in range(1, order):
        birth = (
            (fitness - 1)
            * rank
            * (order - rank)
            * sp.Rational(1, order - 1)
        )
        death_next = sp.Rational((rank + 1) * rank, order - 1)
        assert sp.factor(law[rank - 1] * birth - law[rank] * death_next) == 0
    return law


def db_rank_law(
    order: int,
    union_laws: list[dict[int, sp.Expr]],
) -> list[sp.Expr]:
    """Exact proper-level complete-kernel dB-dual rank law."""

    # The recurrent dB class has ranks 1,...,s-1: samples exclude the removed
    # target, so a transition cannot create the full set.
    generator = sp.zeros(order - 1, order - 1)
    for rank in range(1, order):
        representative = (1 << rank) - 1
        row = db_row(representative, order, union_laws)
        for destination, rate in row.items():
            destination_rank = destination.bit_count()
            assert 1 <= destination_rank <= order - 1
            generator[rank - 1, destination_rank - 1] += rate
    assert all(sp.factor(sum(generator.row(index))) == 0 for index in range(order - 1))
    return stationary_row(generator)


def algebra_audit() -> None:
    """Replay the cancellation, pair polynomial, and orientation split."""

    HB, HD, Z = sp.symbols("H_B H_D Z", positive=True)
    Bi, Bj, Di, Dj = sp.symbols("B_i B_j D_i D_j", positive=True)
    ei, ej, xi, xj = sp.symbols("e_i e_j x_i x_j", positive=True)

    # Clearing the normalized singleton totals gives the cycle-level target.
    normalized_gap = (
        (xi * Bi + xj * Bj) / HB
        * (xi * ei * Di + xj * ej * Dj) / HD
        - Z / (HB * HD) * (xi + xj) * (ei * xi + ej * xj)
    )
    cycle_gap = (
        (xi * Bi + xj * Bj) * (xi * ei * Di + xj * ej * Dj)
        - Z * (xi + xj) * (ei * xi + ej * xj)
    )
    assert sp.expand(HB * HD * normalized_gap - cycle_gap) == 0

    diagonal_i = ei * (Bi * Di - Z)
    diagonal_j = ej * (Bj * Dj - Z)
    cross = Bi * ej * Dj + Bj * ei * Di - Z * (ei + ej)
    pair_polynomial = diagonal_i * xi**2 + cross * xi * xj + diagonal_j * xj**2
    assert sp.expand(pair_polynomial - cycle_gap) == 0

    orientation = (sp.sqrt(Bi * ej * Dj) - sp.sqrt(Bj * ei * Di)) ** 2
    hellinger_cross = 2 * sp.sqrt(ei * ej * Bi * Di * Bj * Dj)
    assert sp.simplify(
        Bi * ej * Dj + Bj * ei * Di - orientation - hellinger_cross
    ) == 0

    # Audit the normalized-to-cycle minimax substitution.
    lam, t = sp.symbols("lambda t", positive=True)
    z = lam * sp.sqrt(HD / HB)
    normalized_side = lam * Bi / HB + (ei * Di / HD) / lam
    assert sp.simplify(sp.sqrt(HB * HD) * normalized_side - (z * Bi + ei * Di / z)) == 0
    assert sp.simplify(sp.sqrt(HB * HD) * sp.sqrt(Z / (HB * HD)) - sp.sqrt(Z)) == 0

    # Strict exact-product/root-Hellinger separation.
    data = {
        ei: sp.Integer(100),
        ej: sp.Integer(1),
        Bi: sp.Integer(100),
        Bj: sp.Integer(1),
        Di: sp.Rational(1, 50),
        Dj: sp.Integer(2),
        Z: sp.Integer(1),
    }
    di_value = diagonal_i.subs(data)
    dj_value = diagonal_j.subs(data)
    cross_value = cross.subs(data)
    orientation_value = sp.simplify(orientation.subs(data))
    exact_margin = sp.simplify(cross_value + 2 * sp.sqrt(di_value * dj_value))
    hellinger_margin = sp.simplify(exact_margin - orientation_value)
    assert (di_value, dj_value, cross_value) == (100, 1, 101)
    assert orientation_value == 162
    assert exact_margin == 121
    assert hellinger_margin == -41


def finite_depth_pseudolaw_audit() -> None:
    """Check all m=2 labelled equations for both K8 dual pseudo-laws."""

    order = 8
    fitness = sp.Rational(3, 2)
    epsilon = sp.Rational(1, 1000)
    max_checked_rank = 2
    max_scaled_rank = max_checked_rank + 1
    residual_rank = max_checked_rank + 2

    union_laws = [
        geometric_union_law(order, fitness, target) for target in range(order)
    ]
    rank_laws = {
        "Bd": bd_rank_law(order, fitness),
        "dB": db_rank_law(order, union_laws),
    }
    row_builders = {
        "Bd": lambda state: bd_row(state, order, fitness),
        "dB": lambda state: db_row(state, order, union_laws),
    }

    low_states = [
        state
        for state in range(1, 1 << order)
        if state.bit_count() <= max_scaled_rank
    ]
    destinations = [
        state for state in low_states if state.bit_count() <= max_checked_rank
    ]
    first_omitted_destinations = [
        state for state in low_states if state.bit_count() == max_scaled_rank
    ]
    residual_state = sum(1 << vertex for vertex in range(residual_rank))

    pseudo_data = {}
    for rule in ("Bd", "dB"):
        rank_law = rank_laws[rule]
        builder = row_builders[rule]
        rows = {state: builder(state) for state in low_states}
        residual_row = builder(residual_state)

        # The one-step support fact is checked directly at the first omitted
        # rank for each dual.
        assert all(
            destination.bit_count() >= max_scaled_rank
            for destination, rate in residual_row.items()
            if destination != residual_state and rate != 0
        )

        # Complete symmetry assigns pi_k/C(s,k) to every k-set.
        genuine_low_mass = {
            state: rank_law[state.bit_count() - 1] / comb(order, state.bit_count())
            for state in low_states
        }
        for destination in destinations:
            balance = sum(
                mass * rows[state].get(destination, 0)
                for state, mass in genuine_low_mass.items()
            )
            assert sp.factor(balance) == 0

        low_total = sum(rank_law[:max_scaled_rank], sp.Integer(0))
        pseudo = {
            state: epsilon * mass for state, mass in genuine_low_mass.items()
        }
        pseudo[residual_state] = 1 - epsilon * low_total
        pseudo_rows = dict(rows)
        pseudo_rows[residual_state] = residual_row
        assert sp.factor(sum(pseudo.values(), sp.Integer(0)) - 1) == 0
        assert all(mass >= 0 for mass in pseudo.values())
        for destination in destinations:
            balance = sum(
                mass * pseudo_rows[state].get(destination, 0)
                for state, mass in pseudo.items()
            )
            assert sp.factor(balance) == 0
        assert any(
            sp.factor(
                sum(
                    mass * pseudo_rows[state].get(destination, 0)
                    for state, mass in pseudo.items()
                )
            )
            != 0
            for destination in first_omitted_destinations
        )

        density = sp.factor(
            sum(mass * state.bit_count() for state, mass in pseudo.items()) / order
        )
        singleton_atom = sp.factor(
            pseudo.get(1, sp.Integer(0))
        )
        pseudo_data[rule] = (density, singleton_atom)
        assert density > (fitness - 1) / fitness

    density_b, singleton_b = pseudo_data["Bd"]
    density_d, singleton_d = pseudo_data["dB"]
    p = (fitness - 1) / fitness
    raw_target = sp.factor(fitness**3 * (density_b - p) * (density_d - p))
    root_product = sp.factor(singleton_b * singleton_d)
    assert raw_target > 0
    assert root_product < raw_target

    # Exact asymptotic coefficient in the general theorem.
    eps, r, c_b, c_d = sp.symbols("epsilon r c_B c_D", positive=True)
    half_excess = sp.Rational(1, 2) - (r - 1) / r
    leading = sp.factor(r**3 * half_excess**2 / (c_b * c_d))
    assert sp.factor(leading - r * (2 - r) ** 2 / (4 * c_b * c_d)) == 0


def main() -> None:
    algebra_audit()
    finite_depth_pseudolaw_audit()
    print("PASS: exact singleton-to-renewal normalizer cancellation")
    print("PASS: exact two-root polynomial and orientation-square split")
    print("PASS: strict rational exact-product/Hellinger separation")
    print("PASS: both K8 dual pseudo-laws satisfy all rank <= 2 equations")
    print("PASS: both pseudo-laws have a nonzero first-omitted rank residual")
    print("PASS: strict one-root MP failure of the finite-prefix pseudo-laws")
    print("OPEN: full-rank orientation-preserving renewal inequality")


if __name__ == "__main__":
    main()
