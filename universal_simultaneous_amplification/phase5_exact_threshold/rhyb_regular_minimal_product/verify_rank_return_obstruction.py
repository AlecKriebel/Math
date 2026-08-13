#!/usr/bin/env python3
"""Exact replay of two regular-VDR proof-route obstructions.

The script verifies:

1. a rank-four pseudo-law on complete K8 that satisfies every singleton and
   doubleton coordinate equation, including triple entrance, but violates
   VDR; and
2. a connected regular 2+4 equitable kernel whose dB singleton atoms are
   nonuniform for every r>1.

Neither object is claimed to refute VDR for a genuine stationary graph law.
No graph enumeration or floating-point sign test is used.
"""

from __future__ import annotations

import sys
from math import comb
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OBSTRUCTION = HERE.parents[1] / "phase4_landmark_closure" / "obstruction"
sys.path.insert(0, str(OBSTRUCTION))

from verify_exact_duals import (  # noqa: E402
    dual_generator,
    geometric_union_probabilities,
    stationary,
)


def subsets(mask: int):
    """Yield all submasks of mask."""

    subset = mask
    while True:
        yield subset
        if subset == 0:
            return
        subset = (subset - 1) & mask


def transition_row(
    state: int,
    union_laws: list[dict[int, sp.Expr]],
    order: int,
) -> dict[int, sp.Expr]:
    """Return one exact dB-dual generator row as a sparse dictionary."""

    answer: dict[int, sp.Expr] = {}
    for target in range(order):
        if not ((state >> target) & 1):
            continue
        retained = state & ~(1 << target)
        for parent_set, probability in union_laws[target].items():
            new_state = retained | parent_set
            if new_state != state:
                answer[new_state] = answer.get(new_state, 0) + probability
    answer[state] = -sum(answer.values(), sp.Integer(0))
    return answer


def complete_rank_generator(
    order: int,
    union_laws: list[dict[int, sp.Expr]],
) -> sp.Matrix:
    """Build the exact proper-level lumping of the complete dB dual."""

    generator = sp.zeros(order - 1, order - 1)
    for rank in range(1, order):
        representative = (1 << rank) - 1
        for new_state, rate in transition_row(
            representative, union_laws, order
        ).items():
            generator[rank - 1, new_state.bit_count() - 1] += rate
    assert all(sp.factor(sum(generator.row(i))) == 0 for i in range(order - 1))
    return generator


def rank_two_return_obstruction() -> None:
    """Verify the m=2 finite-prefix obstruction exactly on K8."""

    order = 8
    fitness = sp.Rational(3, 2)
    transition = [
        [
            sp.Integer(0) if i == j else sp.Rational(1, order - 1)
            for j in range(order)
        ]
        for i in range(order)
    ]
    union_laws = [
        geometric_union_probabilities(row, fitness) for row in transition
    ]

    rank_generator = complete_rank_generator(order, union_laws)
    rank_law = stationary(rank_generator)
    assert rank_law == [
        sp.Rational(448, 2059),
        sp.Rational(672, 2059),
        sp.Rational(560, 2059),
        sp.Rational(280, 2059),
        sp.Rational(84, 2059),
        sp.Rational(14, 2059),
        sp.Rational(1, 2059),
    ]

    low_states = [
        state
        for state in range(1, 1 << order)
        if state.bit_count() <= 3
    ]
    low_rows = {
        state: transition_row(state, union_laws, order)
        for state in low_states
    }

    # Complete symmetry assigns rank_law[k-1]/C(order,k) to every k-set.
    # Check every singleton and doubleton coordinate equation, not only its
    # scalar level sum.  Incoming states have rank at most three.
    for destination in low_states:
        if destination.bit_count() > 2:
            continue
        balance = sum(
            rank_law[source.bit_count() - 1]
            / comb(order, source.bit_count())
            * low_rows[source].get(destination, 0)
            for source in low_states
        )
        assert sp.factor(balance) == 0

    # A rank-four state cannot enter rank one or two in one update.
    rank_four = sum(1 << vertex for vertex in range(4))
    rank_four_row = transition_row(rank_four, union_laws, order)
    assert all(
        destination.bit_count() >= 3
        for destination, rate in rank_four_row.items()
        if destination != rank_four and rate != 0
    )

    # Scale all genuine ranks <=3 and put the residual at rank four.
    epsilon = sp.Rational(1, 1000)
    low_mass = sum(rank_law[:3])
    pseudo = {
        state: epsilon
        * rank_law[state.bit_count() - 1]
        / comb(order, state.bit_count())
        for state in low_states
    }
    pseudo[rank_four] = 1 - epsilon * low_mass
    pseudo_rows = dict(low_rows)
    pseudo_rows[rank_four] = rank_four_row
    assert sum(pseudo.values()) == 1
    assert all(value >= 0 for value in pseudo.values())
    for destination in low_states:
        if destination.bit_count() > 2:
            continue
        balance = sum(
            mass * pseudo_rows[source].get(destination, 0)
            for source, mass in pseudo.items()
        )
        assert sp.factor(balance) == 0
    assert any(
        sp.factor(
            sum(
                mass * pseudo_rows[source].get(destination, 0)
                for source, mass in pseudo.items()
            )
        )
        != 0
        for destination in low_states
        if destination.bit_count() == 3
    )

    density = sp.factor(
        (
            epsilon
            * sum((rank + 1) * rank_law[rank] for rank in range(3))
            + 4 * (1 - epsilon * low_mass)
        )
        / order
    )
    singleton = sp.factor(epsilon * rank_law[0] / order)
    p = (fitness - 1) / fitness
    target = sp.factor(fitness**2 * (density - p))
    assert density == sp.Rational(17743, 35500)
    assert singleton == sp.Rational(7, 257375)
    assert target == sp.Rational(53187, 142000)
    assert density > p and singleton < target

    # This exact rational check implies the interval sign used in the note.
    assert sp.Rational(1, 2) - sp.Rational(51, 151) > 0


def stopped_green_audit() -> None:
    """Check the honest root-marked low/high Green identity at r=3/2."""

    fitness = sp.Rational(3, 2)
    order = 6
    cross = sp.Rational(1, 10)
    within_x = sp.Rational(3, 5)
    within_y = sp.Rational(4, 15)
    weights = [
        [
            0
            if i == j
            else within_x
            if i < 2 and j < 2
            else within_y
            if i >= 2 and j >= 2
            else cross
            for j in range(order)
        ]
        for i in range(order)
    ]
    assert all(sum(row) == 1 for row in weights)
    assert sp.Matrix(weights) == sp.Matrix(weights).T

    ambient = dual_generator(weights, fitness, "dB")
    invariant = stationary(ambient)
    full = (1 << order) - 1
    low = [state for state in range(1, full) if state.bit_count() <= 2]
    high = [state for state in range(1, full) if state.bit_count() >= 3]
    low_index = [state - 1 for state in low]
    high_index = [state - 1 for state in high]
    qmm = ambient.extract(low_index, low_index)
    qpm = ambient.extract(high_index, low_index)
    pi_low = sp.Matrix([[invariant[index] for index in low_index]])
    pi_high = sp.Matrix([[invariant[index] for index in high_index]])
    eta = pi_high * qpm
    green = (-qmm).inv()
    assert all(sp.factor(value) == 0 for value in pi_low - eta * green)

    singleton_positions = [low.index(1 << vertex) for vertex in range(order)]
    rooted = [sp.factor((eta * green)[position]) for position in singleton_positions]
    total_singleton = sp.factor(sum(rooted))
    assert total_singleton == sp.factor(
        sum(invariant[(1 << vertex) - 1] for vertex in range(order))
    )

    v_x = sp.Rational(30887287990994154160, 494390162744319752327)
    v_y = sp.Rational(31101376043908505160, 494390162744319752327)
    assert rooted[:2] == [v_x, v_x]
    assert rooted[2:] == [v_y] * 4
    assert v_x < total_singleton / order < v_y


def symbolic_union_probabilities(
    row: list[sp.Expr], fitness: sp.Symbol
) -> dict[int, sp.Expr]:
    """Symbolic geometric-union law, without undecidable sign assertions."""

    support = sum(1 << i for i, value in enumerate(row) if value != 0)
    pgf = lambda z: z / (fitness - (fitness - 1) * z)
    answer: dict[int, sp.Expr] = {}
    for target_set in subsets(support):
        if target_set == 0:
            continue
        probability = sp.Integer(0)
        for included in subsets(target_set):
            mass = sum(
                (
                    row[i]
                    for i in range(len(row))
                    if (included >> i) & 1
                ),
                sp.Integer(0),
            )
            probability += (
                (-1) ** (target_set.bit_count() - included.bit_count())
                * pgf(mass)
            )
        answer[target_set] = sp.cancel(probability)
    assert sp.cancel(sum(answer.values()) - 1) == 0
    return answer


def equitable_orbit_generator(fitness: sp.Symbol) -> tuple[sp.Matrix, list[tuple[int, int]]]:
    """Return the exact 13-state orbit generator for the 2+4 kernel."""

    order = 6
    cross = sp.Rational(1, 10)
    within_x = sp.Rational(3, 5)
    within_y = sp.Rational(4, 15)
    transition = [
        [
            0
            if i == j
            else within_x
            if i < 2 and j < 2
            else within_y
            if i >= 2 and j >= 2
            else cross
            for j in range(order)
        ]
        for i in range(order)
    ]
    union_laws = [
        symbolic_union_probabilities(row, fitness) for row in transition
    ]
    orbits = [
        (x_count, y_count)
        for x_count in range(3)
        for y_count in range(5)
        if (x_count, y_count) not in ((0, 0), (2, 4))
    ]

    def representative(orbit: tuple[int, int]) -> int:
        x_count, y_count = orbit
        vertices = list(range(x_count)) + list(range(2, 2 + y_count))
        return sum(1 << vertex for vertex in vertices)

    def orbit_of(state: int) -> tuple[int, int]:
        return (
            sum((state >> i) & 1 for i in range(2)),
            sum((state >> i) & 1 for i in range(2, 6)),
        )

    generator = sp.zeros(len(orbits), len(orbits))
    for row_index, orbit in enumerate(orbits):
        state = representative(orbit)
        rates: dict[tuple[int, int], sp.Expr] = {}
        for target in range(order):
            if not ((state >> target) & 1):
                continue
            retained = state & ~(1 << target)
            for parent_set, probability in union_laws[target].items():
                destination = orbit_of(retained | parent_set)
                if destination != orbit:
                    rates[destination] = rates.get(destination, 0) + probability
        for destination, rate in rates.items():
            generator[row_index, orbits.index(destination)] = rate
        generator[row_index, row_index] = -sum(rates.values(), sp.Integer(0))
    assert all(
        sp.cancel(sum(generator.row(i))) == 0 for i in range(len(orbits))
    )
    return generator, orbits


def root_average_obstruction() -> None:
    """Derive and sign the nonuniform singleton factorization for all r>1."""

    r = sp.symbols("r", positive=True)
    generator, orbits = equitable_orbit_generator(r)
    system = generator.T.copy()
    rhs = sp.zeros(len(orbits), 1)
    for column in range(len(orbits)):
        system[-1, column] = 1
    rhs[-1] = 1
    orbit_law = tuple(sp.linsolve((system, rhs)).args[0])

    v_x = orbit_law[orbits.index((1, 0))] / 2
    v_y = orbit_law[orbits.index((0, 1))] / 4
    numerator, denominator = sp.fraction(sp.factor(v_x - v_y))
    positive_factor = sp.Poly(
        224583960 * r**10
        + 3150513334 * r**9
        + 17487944995 * r**8
        + 53883076579 * r**7
        + 112461136241 * r**6
        + 181841150181 * r**5
        + 224583406416 * r**4
        + 192172906510 * r**3
        + 102331562256 * r**2
        + 29868277824 * r
        + 3503896704,
        r,
    )
    expected_numerator = sp.expand(
        -375 * r * (r - 1) ** 2 * (9 * r + 1) * positive_factor.as_expr()
    )
    assert sp.expand(numerator - expected_numerator) == 0
    assert all(coefficient > 0 for coefficient in positive_factor.all_coeffs())

    denominator_polynomial = sp.Poly(sp.expand(denominator), r)
    assert denominator_polynomial.degree() == 18
    assert all(coefficient > 0 for coefficient in denominator_polynomial.all_coeffs())
    d_coefficients = (
        1513683376128,
        33103970621568,
        291981783940704,
        1439657416451304,
        4625918408977902,
        10744093126699298,
        19442041987593843,
        28860066322602760,
        36258144436319895,
        39084932504333196,
        36258144436319895,
        28860066322602760,
        19442041987593843,
        10744093126699298,
        4625918408977902,
        1439657416451304,
        291981783940704,
        33103970621568,
        1513683376128,
    )
    displayed_denominator = 2 * sum(
        coefficient * r**degree
        for degree, coefficient in enumerate(d_coefficients)
    )
    assert sp.expand(denominator - displayed_denominator) == 0


def main() -> None:
    rank_two_return_obstruction()
    stopped_green_audit()
    root_average_obstruction()
    print("PASS: every rank <=2 coordinate equation survives rank-four scaling")
    print("PASS: exact pseudo-law violates VDR; it is not a stationary graph law")
    print("PASS: honest stopped Green identity remains root-marked")
    print("REFUTED: uniform-singleton root averaging on a connected regular graph")
    print("OPEN: universal regular vertexwise dB repayment")


if __name__ == "__main__":
    main()
