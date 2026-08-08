#!/usr/bin/env python3
"""Exact hostile audit of the paired high-Johnson Schur feedback.

At r=3/2 let ``A=-L.T`` be the transient Green operator and split the
transient state space, rank by rank, into Johnson degrees at most two and
their counting-orthogonal complement.  If ``H`` is any full-rank matrix
whose columns span the high space, the basis-independent correction is

    Sigma_A = Pi A H (H.T A H)^(-1) H.T A Pi.

This verifier does four things over QQ.

1. It derives the canonical rank diagonal D from the common reversible
   measure of the two complete-graph chains and checks the detailed-balance
   identity directly.
2. On the unweighted six-cycle it gives tiny exact quadratic witnesses
   proving that neither the D-weighted sum nor the D-weighted difference of
   the Bd and dB corrections has a universal Loewner sign.  The same
   witnesses refute a weighted-adjoint identity.
3. It exact-screens those failed signs on the frozen seven-vertex fake-Green
   witness and two true hostile graphs.
4. On the exact dB-amplifying windmill it proves that restoring the high
   modes strictly raises the normalized endpoint score for *both* rules.

No floating-point value is used for an assertion.
"""

from __future__ import annotations

import hashlib
import itertools
import math
import pathlib
import sys

import sympy as sp
from flint import fmpq, fmpq_mat


HERE = pathlib.Path(__file__).resolve().parent
ENDPOINT = HERE.parent / "endpoint_hostile_exact"
sys.path.insert(0, str(ENDPOINT))

from verify_balanced_poisson import changing_rates
from verify_endpoint_candidates import complete_baseline, graph, hostile_corpus


R = sp.Rational(3, 2)


def as_fmpq(value):
    value = sp.cancel(value)
    numerator, denominator = sp.fraction(value)
    return fmpq(int(numerator), int(denominator))


def transient_states(n: int):
    return tuple(range(1, (1 << n) - 1))


def changing_operator(weights, rule: str, states, index):
    """Return A=-L^T for the continuous type-changing chain."""
    full = (1 << len(weights)) - 1
    matrix = fmpq_mat(len(states), len(states))
    for state in states:
        column = index[state]
        rates = changing_rates(weights, state, rule)
        matrix[column, column] = as_fmpq(
            sum((rate for _, rate in rates), sp.Integer(0))
        )
        for target, rate in rates:
            if target not in (0, full):
                matrix[index[target], column] -= as_fmpq(rate)
    return matrix


def degree_two_high_basis(n: int, states, index):
    """An integer basis for the rankwise counting-orthogonal high space."""
    monomials = (
        ((),)
        + tuple((vertex,) for vertex in range(n))
        + tuple(itertools.combinations(range(n), 2))
    )
    columns = []
    rank_dimensions = {}
    for rank in range(1, n):
        rank_states = tuple(state for state in states if state.bit_count() == rank)
        evaluation = sp.Matrix(
            [
                [int(all(state & (1 << vertex) for vertex in monomial))
                 for monomial in monomials]
                for state in rank_states
            ]
        )
        nullspace = evaluation.T.nullspace()
        rank_dimensions[rank] = len(nullspace)
        for vector in nullspace:
            denominator = sp.ilcm(*[sp.denom(value) for value in vector])
            column = [0] * len(states)
            for state, value in zip(rank_states, vector):
                column[index[state]] = int(value * denominator)
            columns.append(column)

    high = fmpq_mat(len(states), len(columns))
    for column_index, column in enumerate(columns):
        for row, value in enumerate(column):
            if value:
                high[row, column_index] = value
    return high, rank_dimensions


def canonical_green_weights(n: int, states):
    """D=pi^{-1}, where pi_k is the common K_n reversible rank weight.

    Up to a harmless common scalar,

        pi_k = r^(k-1) / binomial(n-2,k-1),
        D_k  = binomial(n-2,k-1) r^(1-k).

    The inverse, rather than pi itself, is the diagonal that makes
    A=-L^T self-adjoint.
    """
    return tuple(
        fmpq(math.comb(n - 2, state.bit_count() - 1))
        * fmpq(2, 3) ** (state.bit_count() - 1)
        for state in states
    )


def rank_pair_vector(n: int, states, terms):
    """Build sum coefficient*1_{|S|=rank,pair subset S}."""
    vector = fmpq_mat(len(states), 1)
    for rank, pair, coefficient in terms:
        for row, state in enumerate(states):
            vector[row, 0] += coefficient * int(
                state.bit_count() == rank
                and all(state & (1 << vertex) for vertex in pair)
            )
    return vector


class SchurContext:
    def __init__(self, operator, high):
        self.operator = operator
        self.operator_high = operator * high
        self.high_block = high.transpose() * self.operator_high
        assert self.high_block.rank() == high.ncols()


def schur_quadratic(context, high, diagonal, vector):
    """Return vector^T D Sigma_A vector exactly."""
    rhs = high.transpose() * (context.operator * vector)
    solution = context.high_block.solve(rhs)
    weighted = fmpq_mat(vector.nrows(), 1)
    for row in range(vector.nrows()):
        weighted[row, 0] = diagonal[row] * vector[row, 0]
    return (weighted.transpose() * context.operator_high * solution)[0, 0]


def rational_hash(value):
    payload = f"{value.p}/{value.q}".encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def check_complete_graph_weight():
    n = 6
    weights = graph(
        n,
        [(left, right, 1) for left in range(n) for right in range(left + 1, n)],
    )
    states = transient_states(n)
    index = {state: row for row, state in enumerate(states)}
    diagonal = canonical_green_weights(n, states)
    for rule in ("Bd", "dB"):
        operator = changing_operator(weights, rule, states, index)
        # D A=A^T D, checked entrywise over QQ.
        for row in range(len(states)):
            for column in range(len(states)):
                assert (
                    diagonal[row] * operator[row, column]
                    == operator[column, row] * diagonal[column]
                )
    print("PASS complete K_6: canonical D A=A^T D for Bd and dB")


def cycle_six_counterexample():
    """Tiny exact counterexample to every natural paired order relation."""
    n = 6
    weights = graph(n, [(vertex, (vertex + 1) % n, 1) for vertex in range(n)])
    states = transient_states(n)
    index = {state: row for row, state in enumerate(states)}
    high, rank_dimensions = degree_two_high_basis(n, states, index)
    assert rank_dimensions == {1: 0, 2: 0, 3: 5, 4: 0, 5: 0}
    assert high.ncols() == 5
    diagonal = canonical_green_weights(n, states)
    contexts = {
        rule: SchurContext(changing_operator(weights, rule, states, index), high)
        for rule in ("Bd", "dB")
    }

    witnesses = {
        "sum-negative": (
            ((4, (0, 4), 1), (4, (1, 3), -1)),
            "sum",
            fmpq(-15488, 3375),
        ),
        "sum-positive": (
            ((3, (0, 2), 1), (3, (3, 5), -1)),
            "sum",
            fmpq(96, 5),
        ),
        "difference-negative": (
            ((4, (0, 2), 1), (4, (3, 5), -1)),
            "difference",
            fmpq(-1792, 3375),
        ),
        "difference-positive": (
            ((3, (0, 4), 1), (3, (1, 3), -1)),
            "difference",
            fmpq(32, 15),
        ),
    }
    for label, (terms, operation, expected) in witnesses.items():
        vector = rank_pair_vector(n, states, terms)
        bd = schur_quadratic(contexts["Bd"], high, diagonal, vector)
        db = schur_quadratic(contexts["dB"], high, diagonal, vector)
        value = bd + db if operation == "sum" else bd - db
        assert value == expected
        print(f"PASS C_6 {label}: {value}")

    # If D Sigma_B=Sigma_D^T D, every quadratic difference would vanish.
    # The last two exact witnesses have opposite nonzero signs, so even a
    # one-sided symmetrized adjoint defect is impossible.
    print(
        "PASS C_6: D(Sigma_B+Sigma_D) and D(Sigma_B-Sigma_D) "
        "both have indefinite symmetric parts"
    )


def fake_green_graph():
    return graph(
        7,
        [
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


def selected_hostile_graphs():
    selected = {label: weights for label, weights in hostile_corpus()}
    return {
        "degree-two-fake-Green": fake_green_graph(),
        "exact-dB-amplifying-windmill": selected[
            "exact-dB-amplifying-windmill"
        ],
        "affine-lower-multiplier-witness": selected[
            "affine-lower-multiplier-witness"
        ],
    }


def seven_vertex_exact_screen():
    """Exact sign screen on the frozen pseudo-flow and true hostile graphs."""
    n = 7
    states = transient_states(n)
    index = {state: row for row, state in enumerate(states)}
    high, rank_dimensions = degree_two_high_basis(n, states, index)
    assert rank_dimensions == {1: 0, 2: 0, 3: 14, 4: 14, 5: 0, 6: 0}
    assert high.ncols() == 28
    diagonal = canonical_green_weights(n, states)

    # Each graph has an explicit negative and positive witness for the
    # symmetric part of both D(Sigma_B+Sigma_D) and D(Sigma_B-Sigma_D).
    specifications = {
        "degree-two-fake-Green": {
            "sum-negative": ((4, (0, 1), 1), (4, (1, 2), -1)),
            "sum-positive": ((4, (3, 4), 1), (4, (5, 6), -1)),
            "difference-negative": ((2, (0, 1), 1), (3, (0, 1), -1)),
            "difference-positive": ((3, (1, 2), 1), (4, (1, 2), 1)),
        },
        "exact-dB-amplifying-windmill": {
            "sum-negative": ((3, (3, 4), 1), (3, (5, 6), 1)),
            "sum-positive": ((4, (3, 4), 1), (4, (5, 6), 1)),
            "difference-negative": ((3, (3, 4), 1), (5, (1, 2), -1)),
            "difference-positive": ((3, (0, 1), 1), (3, (0, 2), 1)),
        },
        "affine-lower-multiplier-witness": {
            "sum-negative": ((3, (3, 4), 1), (3, (5, 6), 1)),
            "sum-positive": ((4, (3, 4), 1), (4, (5, 6), 1)),
            "difference-negative": ((3, (0, 3), 1), (3, (0, 4), -1)),
            "difference-positive": ((3, (0, 1), 1), (3, (0, 2), 1)),
        },
    }

    for graph_label, weights in selected_hostile_graphs().items():
        contexts = {
            rule: SchurContext(
                changing_operator(weights, rule, states, index), high
            )
            for rule in ("Bd", "dB")
        }
        for witness_label, terms in specifications[graph_label].items():
            vector = rank_pair_vector(n, states, terms)
            bd = schur_quadratic(contexts["Bd"], high, diagonal, vector)
            db = schur_quadratic(contexts["dB"], high, diagonal, vector)
            value = (
                bd + db if witness_label.startswith("sum") else bd - db
            )
            expected_positive = witness_label.endswith("positive")
            assert (value > 0) == expected_positive
            print(
                f"PASS {graph_label} {witness_label}: "
                f"~{float(value):.12g}, sha256={rational_hash(value)}"
            )


def seven_vertex_low_basis(states):
    """The deterministic 98-column rank-labelled degree-two basis."""
    n = 7
    labels = []
    for rank in range(1, n):
        order = 1 if rank in (1, n - 1) else 2
        labels.extend(
            (rank, vertices)
            for vertices in itertools.combinations(range(n), order)
        )
    assert len(labels) == 98
    low = fmpq_mat(len(states), len(labels))
    for row, state in enumerate(states):
        for column, (rank, vertices) in enumerate(labels):
            low[row, column] = int(
                state.bit_count() == rank
                and all(state & (1 << vertex) for vertex in vertices)
            )
    assert low.rank() == 98
    return low


def normalized_source_and_flux(weights, rule: str, states, index):
    n = len(weights)
    full = (1 << n) - 1
    source = fmpq_mat(len(states), 1)
    flux = fmpq_mat(len(states), 1)
    for vertex in range(n):
        source[index[1 << vertex], 0] = fmpq(1, n)
    baseline = as_fmpq(complete_baseline(n, rule))
    for state in states:
        total = sum(
            (
                as_fmpq(rate)
                for target, rate in changing_rates(weights, state, rule)
                if target == full
            ),
            fmpq(0),
        )
        flux[index[state], 0] = total / baseline
    return source, flux


def exact_both_improve_windmill():
    """Refute the scalar claim that high feedback cannot help both rules."""
    n = 7
    states = transient_states(n)
    index = {state: row for row, state in enumerate(states)}
    low = seven_vertex_low_basis(states)
    high, _ = degree_two_high_basis(n, states, index)
    assert high.transpose() * low == fmpq_mat(high.ncols(), low.ncols())
    weights = selected_hostile_graphs()["exact-dB-amplifying-windmill"]

    for rule in ("Bd", "dB"):
        operator = changing_operator(weights, rule, states, index)
        source, flux = normalized_source_and_flux(weights, rule, states, index)

        # Galerkin score after suppressing the high coordinates.
        low_operator = low.transpose() * operator * low
        low_solution = low_operator.solve(low.transpose() * source)
        score_without_feedback = (
            flux.transpose() * low * low_solution
        )[0, 0]

        # Exact full-chain score.  Since the flux lies in the low space, the
        # difference is precisely the contribution restored by the Schur
        # feedback, independently of the chosen low/high bases.
        full_score = (flux.transpose() * operator.solve(source))[0, 0]
        improvement = full_score - score_without_feedback
        assert improvement > 0
        print(
            f"PASS windmill {rule}: low~{float(score_without_feedback):.12g}, "
            f"full~{float(full_score):.12g}, delta~{float(improvement):.12g}, "
            f"sha256(delta)={rational_hash(improvement)}"
        )


def main():
    check_complete_graph_weight()
    cycle_six_counterexample()
    seven_vertex_exact_screen()
    exact_both_improve_windmill()
    print(
        "PASS: exact paired Schur audit; canonical adjoint/order and "
        "no-both-improve conjectures are refuted"
    )


if __name__ == "__main__":
    main()
