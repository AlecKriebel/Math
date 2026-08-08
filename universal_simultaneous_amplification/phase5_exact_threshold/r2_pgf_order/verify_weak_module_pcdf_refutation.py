#!/usr/bin/env python3
"""Exact certificate for the weak-module refutation of active PCDF.

The calculation is entirely over QQ.  It builds the isolated three-vertex
proper-subset dual from the fair-geometric burst rule, solves its invariant
law, verifies the first-order reduced module chain, and compares the limiting
active rank CDF with the complete-graph law.
"""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations


def solve(matrix: list[list[Q]], rhs: list[Q]) -> list[Q]:
    """Small exact Gaussian elimination over QQ."""
    n = len(rhs)
    augmented = [row[:] + [value] for row, value in zip(matrix, rhs)]
    for column in range(n):
        pivot = next(row for row in range(column, n) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(n):
            if row == column or not augmented[row][column]:
                continue
            scale = augmented[row][column]
            augmented[row] = [
                x - scale * y
                for x, y in zip(augmented[row], augmented[column])
            ]
    return [augmented[row][-1] for row in range(n)]


def union_law(row: list[Q]) -> dict[int, Q]:
    """Law of the distinct vertices in J iid samples, Pr(J=j)=2^-j."""
    support = [vertex for vertex, probability in enumerate(row) if probability]
    hit = [Q(0) for _ in range(1 << len(support))]
    # P(U is contained in S)=p_S/(2-p_S).  Mobius inversion gives P(U=S).
    for mask in range(1, 1 << len(support)):
        mass = sum(
            (row[support[j]] for j in range(len(support)) if mask >> j & 1),
            Q(0),
        )
        hit[mask] = mass / (2 - mass)
    for j in range(len(support)):
        for mask in range(1 << len(support)):
            if mask >> j & 1:
                hit[mask] -= hit[mask ^ (1 << j)]
    answer = {}
    for mask, probability in enumerate(hit):
        if probability:
            actual = sum(
                (1 << support[j] for j in range(len(support)) if mask >> j & 1),
                0,
            )
            answer[actual] = probability
    assert sum(answer.values(), Q(0)) == 1
    assert all(probability > 0 for probability in answer.values())
    return answer


def isolated_module():
    """Build H=0--10--1--1--2, with portal p=2."""
    rows = [
        [Q(0), Q(1), Q(0)],
        [Q(10, 11), Q(0), Q(1, 11)],
        [Q(0), Q(1), Q(0)],
    ]
    laws = [union_law(row) for row in rows]
    states = list(range(1, 7))
    index = {state: j for j, state in enumerate(states)}
    transition = [[Q(0) for _ in states] for _ in states]
    for source, state in enumerate(states):
        for target in range(3):
            if not state >> target & 1:
                transition[source][source] += Q(1, 3)
                continue
            for burst, probability in laws[target].items():
                destination = (state & ~(1 << target)) | burst
                assert destination in index
                transition[source][index[destination]] += probability / 3
        assert sum(transition[source], Q(0)) == 1

    # Solve pi P=pi with the final equation replaced by normalization.
    system = [
        [transition[column][row] - Q(row == column) for column in range(6)]
        for row in range(6)
    ]
    system[-1] = [Q(1) for _ in states]
    rhs = [Q(0) for _ in range(5)] + [Q(1)]
    stationary = solve(system, rhs)
    assert all(value > 0 for value in stationary)
    assert sum(stationary, Q(0)) == 1
    assert all(
        sum((stationary[i] * transition[i][j] for i in range(6)), Q(0))
        == stationary[j]
        for j in range(6)
    )
    return states, stationary


def polynomial_power(base: list[Q], exponent: int) -> list[Q]:
    answer = [Q(1)]
    for _ in range(exponent):
        product = [Q(0) for _ in range(len(answer) + len(base) - 1)]
        for i, x in enumerate(answer):
            for j, y in enumerate(base):
                product[i + j] += x * y
        answer = product
    return answer


def main() -> None:
    states, stationary = isolated_module()
    expected = {
        0b001: Q(5, 12),
        0b010: Q(121, 252),
        0b011: Q(5, 252),
        0b100: Q(1, 42),
        0b101: Q(5, 126),
        0b110: Q(5, 252),
    }
    assert dict(zip(states, stationary)) == expected

    rank = [Q(0), Q(0), Q(0)]
    for state, probability in zip(states, stationary):
        rank[state.bit_count()] += probability
    assert rank[1:] == [Q(58, 63), Q(5, 63)]
    mean = rank[1] + 2 * rank[2]
    assert mean == Q(68, 63)
    active = [Q(0), rank[1] / mean, 2 * rank[2] / mean]
    assert active[1:] == [Q(29, 34), Q(5, 34)]

    portal = 2
    alpha = sum(
        (probability for state, probability in zip(states, stationary)
         if state >> portal & 1),
        Q(0),
    )
    singleton = expected[1 << portal]
    assert alpha == Q(1, 12) and singleton == Q(1, 42)

    # For one specified empty destination, a nonsingleton portal state
    # colonizes with first-order coefficient 2.  A singleton colonizes while
    # surviving with coefficient 3/2.  Loss into one specified occupied
    # destination has coefficient 1/2.  Averaging over the isolated law gives
    # reduced birth/death odds R=4 alpha/s-1.
    birth = 2 * alpha - singleton / 2
    death = singleton / 2
    odds = birth / death
    assert odds == 13
    vacancy = 1 / (1 + odds)
    occupied = 1 - vacancy
    assert vacancy == Q(1, 14) and occupied == Q(13, 14)

    # Verify detailed balance of the reduced chain on nonempty module sets.
    modules = 5
    macro_states = list(range(1, 1 << modules))
    macro_weight = {state: odds ** state.bit_count() for state in macro_states}
    for state in macro_states:
        k = state.bit_count()
        for destination in range(modules):
            if state >> destination & 1:
                continue
            larger = state | (1 << destination)
            forward = Q(k) * birth
            reverse = Q(k) * death
            assert macro_weight[state] * forward == macro_weight[larger] * reverse

    # Limiting proper module PGF g=a+(1-a)H and active PGF
    # Q_*=Q_H g^(M-1).
    internal_proper = [Q(0), rank[1], rank[2]]
    g = [vacancy] + [occupied * value for value in internal_proper[1:]]
    g_power = polynomial_power(g, modules - 1)
    active_limit = [Q(0) for _ in range(len(g_power) + 2)]
    for i, x in enumerate(active[1:], 1):
        for j, y in enumerate(g_power):
            active_limit[i + j] += x * y
    assert sum(active_limit, Q(0)) == 1

    cdf_two = active_limit[1] + active_limit[2]
    assert cdf_two == Q(44803, 41143536)
    complete_cdf_two = Q(7, 4096)  # n=15: (1+13)/2^13.
    gap = cdf_two - complete_cdf_two
    assert gap == Q(-6530729, 10532745216) < 0
    c_one = gap / 2

    # The separate mean-singleton sign remains positive in this limit.
    normalizer = 1 - vacancy**modules
    global_mean = modules * occupied * mean / normalizer
    global_singleton = (
        modules * occupied * vacancy ** (modules - 1) * rank[1] / normalizer
    )
    mean_singleton = Q(14) + global_singleton - 2 * global_mean
    assert mean_singleton == Q(1151848, 289597) > 0

    print("PASS: isolated P3 proper-subset chain solved exactly")
    print("PASS: reduced macro odds R=13 and vacancy a=1/14")
    print(f"limiting active CDF through rank two = {cdf_two}")
    print(f"complete K_15 active CDF through rank two = {complete_cdf_two}")
    print(f"exact CDF gap = {gap} < 0; hence c_1={c_one} < 0")
    print(f"separate limiting MS sign = {mean_singleton} > 0")
    print("EXACT REFUTATION: PCDF fails on connected rational graphs for small epsilon")


if __name__ == "__main__":
    main()
