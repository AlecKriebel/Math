#!/usr/bin/env python3
"""Exact finite-time audit for the active harmonic baseline conjecture.

This is an independent QQ implementation of the active chain.  It certifies
the rank summation-by-parts and flux identities and exactly refutes the
stronger pointwise finite-time CDF order.  Finite iteration does not prove the
all-time harmonic inequality.
"""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations
from math import comb


RANK_TAIL_WEIGHTS = (
    1, 3, 3, 1000, 30, 1000, 300, 3, 1, 10, 1, 30, 1, 300, 30,
)


def replacement_kernel(n: int, edge_weights) -> list[list[Q]]:
    weights = [[0 for _ in range(n)] for _ in range(n)]
    for value, (u, v) in zip(edge_weights, combinations(range(n), 2)):
        weights[u][v] = weights[v][u] = value
    answer = []
    for v, row in enumerate(weights):
        degree = sum(row)
        assert degree > 0 and row[v] == 0
        answer.append([Q(value, degree) for value in row])
    return answer


def active_chain(P: list[list[Q]]):
    n = len(P)
    states = [
        (subset, target)
        for target in range(n)
        for subset in range(1, 1 << n)
        if not subset >> target & 1
    ]
    index = {state: j for j, state in enumerate(states)}
    rows: list[dict[int, Q]] = []
    for subset, target in states:
        rank = subset.bit_count()
        row: dict[int, Q] = {}

        def add(destination, probability):
            j = index[destination]
            row[j] = row.get(j, Q(0)) + probability

        # Continue branch: retain the target and add a P_target sample.
        for sample, probability in enumerate(P[target]):
            if probability:
                add((subset | (1 << sample), target), probability / 2)

        # Relabel branch: choose a cache member, delete it, make it the new
        # target, and add a sample from that target's row.
        for new_target in range(n):
            if not subset >> new_target & 1:
                continue
            retained = subset & ~(1 << new_target)
            for sample, probability in enumerate(P[new_target]):
                if probability:
                    add(
                        (retained | (1 << sample), new_target),
                        probability / (2 * rank),
                    )
        assert sum(row.values(), Q(0)) == 1
        rows.append(row)
    return states, rows


def propagate(law: list[Q], rows: list[dict[int, Q]]) -> list[Q]:
    answer = [Q(0) for _ in law]
    for source, mass in enumerate(law):
        for destination, probability in rows[source].items():
            answer[destination] += mass * probability
    assert sum(answer, Q(0)) == sum(law, Q(0))
    return answer


def rank_law(law: list[Q], states, N: int) -> list[Q]:
    answer = [Q(0) for _ in range(N + 1)]
    for mass, (subset, _) in zip(law, states):
        answer[subset.bit_count()] += mass
    assert sum(answer, Q(0)) == 1
    return answer


def harmonic(law: list[Q], states) -> Q:
    return sum(
        (mass / subset.bit_count() for mass, (subset, _) in zip(law, states)),
        Q(0),
    )


def fluxes(law: list[Q], states, rows, N: int):
    upward = [Q(0) for _ in range(N + 1)]
    downward = [Q(0) for _ in range(N + 1)]
    for source, (subset, _) in enumerate(states):
        rank = subset.bit_count()
        for destination, probability in rows[source].items():
            new_rank = states[destination][0].bit_count()
            if new_rank == rank + 1:
                upward[rank] += law[source] * probability
            elif new_rank == rank - 1:
                downward[rank] += law[source] * probability
            else:
                assert new_rank == rank
    return upward, downward


def main() -> None:
    n = 6
    N = n - 1
    P = replacement_kernel(n, RANK_TAIL_WEIGHTS)
    states, rows = active_chain(P)
    assert len(states) == n * (2**N - 1)

    normalization = n * N * 2 ** (N - 1)
    law = [Q(subset.bit_count(), normalization) for subset, _ in states]
    assert sum(law, Q(0)) == 1
    complete_rank = [Q(0)] + [
        Q(comb(N - 1, rank - 1), 2 ** (N - 1))
        for rank in range(1, N + 1)
    ]
    baseline = Q(2**N - 1, N * 2 ** (N - 1))
    assert harmonic(law, states) == baseline == Q(31, 80)

    saved = {}
    all_harmonic_nonnegative = True
    for time in range(89):
        ranks = rank_law(law, states, N)
        cdf_excess = [Q(0) for _ in range(N)]
        for cutoff in range(1, N):
            cdf_excess[cutoff] = sum(
                (ranks[k] - complete_rank[k] for k in range(1, cutoff + 1)),
                Q(0),
            )
        harmonic_gap = harmonic(law, states) - baseline
        cdf_reconstruction = sum(
            (cdf_excess[cutoff] / (cutoff * (cutoff + 1))
             for cutoff in range(1, N)),
            Q(0),
        )
        assert harmonic_gap == cdf_reconstruction
        all_harmonic_nonnegative &= harmonic_gap >= 0
        if time < 88:
            assert cdf_excess[1] >= 0
        if time in (0, 1, 2, 20, 87, 88):
            saved[time] = (cdf_excess, harmonic_gap)

        if time == 88:
            break
        upward, downward = fluxes(law, states, rows, N)
        next_law = propagate(law, rows)
        next_gap = harmonic(next_law, states) - harmonic(law, states)
        flux_reconstruction = sum(
            ((downward[cutoff + 1] - upward[cutoff])
             / (cutoff * (cutoff + 1))
             for cutoff in range(1, N)),
            Q(0),
        )
        assert next_gap == flux_reconstruction
        law = next_law

    assert saved[0][1] == 0 and saved[1][1] == 0
    assert saved[2][1] > 0
    assert all_harmonic_nonnegative  # finite exact evidence only

    # Pointwise active-CDF domination is already false at a finite time,
    # despite the harmonic weighted aggregate remaining strictly positive.
    assert saved[87][0][1] > 0
    assert saved[88][0][1] < 0
    assert saved[88][1] > 0

    cdf_88 = saved[88][0][1]
    harmonic_88 = saved[88][1]
    print("PASS: independent 186-state active chain over QQ")
    print("PASS: exact CDF summation-by-parts and rank-flux identities")
    print("PASS: a_0=a_1 and exact harmonic baseline through t=88")
    print(
        "finite-time singleton CDF: "
        f"t=87 {float(saved[87][0][1]):.12g} > 0, "
        f"t=88 {float(cdf_88):.12g} < 0"
    )
    print(
        "at t=88 the required weighted harmonic gap is still "
        f"{float(harmonic_88):.12g} > 0"
    )
    print(
        "EXACTLY REFUTED: pointwise finite-time active-CDF domination; "
        f"negative numerator has {len(str(abs(cdf_88.numerator)))} digits"
    )
    print("OPEN: universal finite-time harmonic baseline FT-H")


if __name__ == "__main__":
    main()
