#!/usr/bin/env python3
"""Exact finite checks for the rank-quadratic Green-flow LP.

The order-five weakly completed star is a hard Pareto witness: Bd is
amplified while dB is suppressed.  On five vertices, rank-labelled Boolean
monomials of degree at most two span *every* transient function.  Hence the
projected Green LP is exact.  This verifier constructs its primal and dual
over QQ, checks strong duality entry by entry, and prints the orbit-reduced
dual multipliers.

It also gives an exact order-three witness showing that scalar rank-cut flow
alone is much too weak: nonnegative artificial occupations satisfy every
rank flow law while their relaxed balanced objective is greater than one.
"""

from __future__ import annotations

import itertools
import hashlib
import pathlib
import sys

import sympy as sp
from flint import fmpq, fmpq_mat


HERE = pathlib.Path(__file__).resolve().parent
ENDPOINT = HERE.parent / "endpoint_hostile_exact"
sys.path.insert(0, str(ENDPOINT))

from verify_balanced_poisson import changing_rates, green_occupation
from verify_endpoint_candidates import complete_baseline, graph


def hard_five_vertex_graph():
    return graph(
        5,
        [(0, vertex, 1000) for vertex in range(1, 5)]
        + [
            (left, right, 1)
            for left in range(1, 5)
            for right in range(left + 1, 5)
        ],
    )


def exact_generator(weights, rule: str):
    n = len(weights)
    full = (1 << n) - 1
    size = full - 1
    generator = sp.zeros(size)
    top_flux = sp.zeros(size, 1)
    for state in range(1, full):
        row = state - 1
        rates = changing_rates(weights, state, rule)
        generator[row, row] = -sum(rate for _, rate in rates)
        for target, rate in rates:
            if target == full:
                top_flux[row] += rate
            elif target:
                generator[row, target - 1] += rate
    return generator, top_flux


def square_degree_two_basis_n5():
    """A deterministic 30-by-30 rank-labelled degree-two basis."""
    n = 5
    full = (1 << n) - 1
    states = tuple(range(1, full))
    labels = []
    rows = []
    # At ranks one and four, singleton indicators form a basis.  At ranks
    # two and three, pair indicators form a basis.  These dimensions are
    # 5+10+10+5=30, exactly the number of transient states.
    for rank, order in ((1, 1), (2, 2), (3, 2), (4, 1)):
        for vertices in itertools.combinations(range(n), order):
            mask = sum(1 << vertex for vertex in vertices)
            labels.append((rank, vertices))
            rows.append(
                [
                    int(
                        state.bit_count() == rank
                        and (state & mask) == mask
                    )
                    for state in states
                ]
            )
    basis = sp.Matrix(rows)
    assert basis.shape == (30, 30)
    assert basis.det() != 0
    return basis, labels


def orbit_type(rank: int, vertices):
    if len(vertices) == 1:
        return f"rank {rank}: center" if vertices == (0,) else f"rank {rank}: leaf"
    return (
        f"rank {rank}: center-leaf"
        if 0 in vertices
        else f"rank {rank}: leaf-leaf"
    )


def verify_hard_n5():
    weights = hard_five_vertex_graph()
    n = 5
    full = (1 << n) - 1
    basis, labels = square_degree_two_basis_n5()
    source = sp.zeros(full - 1, 1)
    for vertex in range(n):
        source[(1 << vertex) - 1] = sp.Rational(1, n)
    rhs = basis * source

    records = {}
    for rule in ("Bd", "dB"):
        generator, top_flux = exact_generator(weights, rule)
        baseline = complete_baseline(n, rule)
        constraint = -basis * generator.T
        objective = top_flux / baseline

        # The exact Green measure is primal feasible.  Since both the basis
        # and the killed generator are nonsingular, it is the unique point
        # satisfying the projected equalities (before z>=0 is even used).
        occupation = sp.Matrix(green_occupation(weights, rule))
        assert constraint * occupation == rhs
        assert all(value > 0 for value in occupation)
        assert constraint.det() != 0
        assert constraint.inv() * rhs == occupation

        # Exact dual: A^T y=c.  Thus f=Phi^T y is the normalized fixation
        # harmonic on transient states and -L f=c state by state.
        dual = constraint.T.inv() * objective
        potential = basis.T * dual
        assert -generator * potential == objective
        primal_value = sp.cancel((objective.T * occupation)[0])
        dual_value = sp.cancel((rhs.T * dual)[0])
        assert primal_value == dual_value

        by_orbit = {}
        for label, value in zip(labels, dual):
            key = orbit_type(*label)
            if key in by_orbit:
                assert by_orbit[key] == value
            else:
                by_orbit[key] = sp.cancel(value)
        assert len(by_orbit) == 8
        records[rule] = {
            "value": primal_value,
            "dual_by_orbit": by_orbit,
        }

    balanced = sp.cancel((records["Bd"]["value"] + records["dB"]["value"]) / 2)
    assert records["Bd"]["value"] > 1
    assert records["dB"]["value"] < 1
    assert balanced < 1
    return records, balanced


def rank_flow_relaxation_witness():
    """Exact scalar rank-flow witness on the path 0--2--1, weights 1,17."""
    weights = graph(3, [(0, 2, 1), (1, 2, 17)])
    # Nonzero artificial occupations, selected from the exact scalar-flow LP.
    witnesses = {
        "Bd": {1: sp.Rational(72, 85), 3: sp.Rational(27, 85)},
        "dB": {4: sp.Rational(55, 161), 6: sp.Rational(106, 161)},
    }
    relaxed_fixation = {"Bd": sp.Rational(81, 85), "dB": sp.Rational(106, 161)}
    for rule, occupation in witnesses.items():
        rho = relaxed_fixation[rule]

        def up_down(state):
            rank = state.bit_count()
            rates = changing_rates(weights, state, rule)
            up = sum(rate for target, rate in rates if target.bit_count() == rank + 1)
            down = sum(rate for target, rate in rates if target.bit_count() == rank - 1)
            return sp.cancel(up), sp.cancel(down)

        # Extinction boundary flow plus rho equals the unit source mass.
        down_one = sum(
            value * up_down(state)[1]
            for state, value in occupation.items()
            if state.bit_count() == 1
        )
        assert sp.cancel(down_one + rho - 1) == 0
        # Every rank-cut current is exactly rho.
        for rank in (1, 2):
            up = sum(
                value * up_down(state)[0]
                for state, value in occupation.items()
                if state.bit_count() == rank
            )
            down = sum(
                value * up_down(state)[1]
                for state, value in occupation.items()
                if state.bit_count() == rank + 1
            )
            assert sp.cancel(up - down - rho) == 0

    normalized_bd = sp.cancel(relaxed_fixation["Bd"] / complete_baseline(3, "Bd"))
    normalized_db = sp.cancel(relaxed_fixation["dB"] / complete_baseline(3, "dB"))
    assert normalized_bd == sp.Rational(171, 85)
    assert normalized_db == sp.Rational(265, 161)
    excess_sum = sp.cancel(normalized_bd + normalized_db - 2)
    assert excess_sum == sp.Rational(22686, 13685) > 0
    return normalized_bd, normalized_db, excess_sum


def degree_two_relaxation_counterexample():
    """Exact positive primal witness refuting universal degree-two closure."""
    n = 7
    weights = graph(
        n,
        [
            # Three blades (1,2), (3,4), (5,6), with center 0.
            (0, 1, 1_000_000),
            (0, 2, 100_000_000_000),
            (1, 2, 20_000_000),
            (0, 3, 3_000_000_000),
            (0, 4, 20_000_000),
            (3, 4, 1),
            (0, 5, 50_000_000),
            (0, 6, 30_000_000),
            (5, 6, 100),
        ],
    )
    full = (1 << n) - 1

    # Deterministic basis of the rank-labelled degree-at-most-two space:
    # singleton indicators at ranks 1,6 and pair indicators at ranks 2--5.
    labels = []
    for rank in range(1, n):
        order = 1 if rank in (1, n - 1) else 2
        for vertices in itertools.combinations(range(n), order):
            labels.append((rank, sum(1 << vertex for vertex in vertices)))
    assert len(labels) == 98

    source = [sp.Rational(1, n) if rank == 1 else sp.Integer(0) for rank, _ in labels]

    supports = {
        "Bd": (
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 16, 17, 18, 20, 21,
            24, 25, 26, 28, 29, 31, 32, 33, 34, 36, 38, 39, 40, 41, 42,
            43, 44, 45, 46, 47, 48, 52, 53, 55, 56, 57, 59, 60, 61, 62,
            63, 64, 65, 66, 68, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
            80, 87, 88, 89, 91, 93, 94, 95, 96, 97, 100, 101, 103, 104,
            105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116,
            117, 118, 119, 120, 121, 122, 123, 124, 125, 126,
        ),
        "dB": (
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 15, 16, 17, 18, 19,
            20, 21, 23, 24, 25, 27, 29, 30, 31, 32, 33, 34, 36, 37, 39,
            40, 41, 42, 44, 45, 47, 48, 49, 53, 55, 56, 57, 58, 59, 61,
            62, 63, 64, 65, 66, 67, 68, 69, 71, 72, 73, 74, 77, 79, 80,
            81, 85, 87, 88, 89, 90, 91, 93, 94, 95, 96, 97, 98, 101,
            103, 104, 105, 106, 107, 109, 110, 111, 112, 113, 115, 116,
            117, 118, 119, 120, 121, 122, 123, 124, 125, 126,
        ),
    }
    assert all(len(support) == len(labels) for support in supports.values())

    def as_fmpq(value):
        value = sp.cancel(value)
        numerator, denominator = sp.fraction(value)
        return fmpq(int(numerator), int(denominator))

    def basis_value(label, state):
        rank, mask = label
        return int(state.bit_count() == rank and (state & mask) == mask)

    values = {}
    actual_values = {}
    first_missing = {}
    for rule in ("Bd", "dB"):
        support = supports[rule]
        matrix = fmpq_mat(len(labels), len(support))
        rhs = fmpq_mat(len(labels), 1)
        for row, (label, source_value) in enumerate(zip(labels, source)):
            rhs[row, 0] = as_fmpq(source_value)
            for column, state in enumerate(support):
                old = basis_value(label, state)
                coefficient = sum(
                    rate * (old - basis_value(label, target))
                    for target, rate in changing_rates(weights, state, rule)
                )
                matrix[row, column] = as_fmpq(coefficient)
        solution = matrix.solve(rhs)
        occupation = tuple(
            sp.Rational(int(solution[row, 0].p), int(solution[row, 0].q))
            for row in range(len(support))
        )
        assert all(value > 0 for value in occupation)

        # Recheck all 98 moment equations in SymPy, independently of FLINT's
        # solve return status.
        for label, source_value in zip(labels, source):
            lhs = sum(
                value
                * sum(
                    rate
                    * (basis_value(label, state) - basis_value(label, target))
                    for target, rate in changing_rates(weights, state, rule)
                )
                for state, value in zip(support, occupation)
            )
            assert sp.cancel(lhs - source_value) == 0

        baseline = complete_baseline(n, rule)
        objective = sum(
            value
            * sum(
                rate for target, rate in changing_rates(weights, state, rule)
                if target == full
            )
            / baseline
            for state, value in zip(support, occupation)
        )
        values[rule] = sp.cancel(objective)

        # Identify the first omitted Johnson layer explicitly.  On n=7 the
        # degree-two basis first misses triple indicators at ranks 3 and 4.
        # Their weak Green residuals show exactly how the artificial measure
        # evades the full chain equations.
        missing_records = []
        for rank in (3, 4):
            for vertices in itertools.combinations(range(n), 3):
                mask = sum(1 << vertex for vertex in vertices)

                def missing_value(state):
                    return int(
                        state.bit_count() == rank and (state & mask) == mask
                    )

                residual = sum(
                    value
                    * sum(
                        rate * (missing_value(state) - missing_value(target))
                        for target, rate in changing_rates(weights, state, rule)
                    )
                    for state, value in zip(support, occupation)
                )
                missing_records.append(
                    (abs(sp.cancel(residual)), rank, vertices, sp.cancel(residual))
                )
        _, rank, vertices, residual = max(missing_records)
        assert residual != 0
        first_missing[rule] = (rank, vertices, residual)

        actual_occupation = green_occupation(weights, rule)
        actual_values[rule] = sp.cancel(
            sum(
                actual_occupation[state - 1]
                * sum(
                    rate
                    for target, rate in changing_rates(weights, state, rule)
                    if target == full
                )
                / baseline
                for state in range(1, full)
            )
        )

    excess_sum = sp.cancel(values["Bd"] + values["dB"] - 2)
    assert excess_sum > 0
    assert actual_values["Bd"] + actual_values["dB"] < 2
    digest = hashlib.sha256(
        f"{sp.numer(excess_sum)}/{sp.denom(excess_sum)}".encode()
    ).hexdigest()
    return values, actual_values, first_missing, excess_sum, digest


def main():
    records, balanced = verify_hard_n5()
    for rule in ("Bd", "dB"):
        print(f"PASS hard n=5 {rule}: exact normalized LP value = {records[rule]['value']}")
        for label, value in records[rule]["dual_by_orbit"].items():
            print(f"  {label}: {value}")
    print(f"PASS hard n=5 balanced exact LP value = {balanced} < 1")
    bd, db, excess = rank_flow_relaxation_witness()
    print(
        "PASS scalar rank-flow relaxation is insufficient: "
        f"Bd={bd}, dB={db}, excess sum={excess}>0"
    )
    values, actual_values, first_missing, quadratic_excess, digest = (
        degree_two_relaxation_counterexample()
    )
    print(
        "PASS rank-quadratic relaxation is insufficient at n=7: "
        f"Bd~{sp.N(values['Bd'], 14)}, dB~{sp.N(values['dB'], 14)}, "
        f"excess sum~{sp.N(quadratic_excess, 14)}>0"
    )
    print(
        "  exact excess certificate: "
        f"numerator bits={int(sp.numer(quadratic_excess)).bit_length()}, "
        f"denominator bits={int(sp.denom(quadratic_excess)).bit_length()}, "
        f"sha256={digest}"
    )
    print(
        "  actual graph is not a fixation counterexample: "
        f"Bd~{sp.N(actual_values['Bd'], 14)}, "
        f"dB~{sp.N(actual_values['dB'], 14)}, "
        f"balanced~{sp.N((actual_values['Bd'] + actual_values['dB']) / 2, 14)}"
    )
    for rule in ("Bd", "dB"):
        rank, vertices, residual = first_missing[rule]
        print(
            f"  first omitted {rule} triple constraint: rank={rank}, "
            f"vertices={vertices}, residual~{sp.N(residual, 14)}"
        )


if __name__ == "__main__":
    main()
