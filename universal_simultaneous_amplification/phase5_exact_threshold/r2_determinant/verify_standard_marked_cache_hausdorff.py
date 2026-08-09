#!/usr/bin/env python3
"""Exact verifier for the marked-request and hypergeometric cache reduction.

The script has four independent components.

* It builds the labelled pin active chains and the joint pin-count/state law.
* It compares the marked-request cut formula with a separately built
  labelled standard-perturbation prefix.
* It checks the power/Bernstein/hypergeometric identities over QQ.
* It records the exact rank-CDF counterexample and screens the weaker
  marked-cache Bernstein signs on a declared finite corpus.

The finite sign screen is evidence only.  The algebraic identities are exact.
"""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import product
from math import comb
from typing import Iterator


State = tuple[int, int]
SparseOperator = list[dict[int, Q]]


def compositions(total: int, length: int) -> Iterator[tuple[int, ...]]:
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, length - 1):
            yield (first,) + tail


def states_of_order(n: int) -> list[State]:
    return [
        (B, v)
        for v in range(n)
        for B in range(1, 1 << n)
        if not ((B >> v) & 1)
    ]


def replacement_pin(n: int, pin: int) -> list[list[Q]]:
    rows = [[Q(0) for _ in range(n)] for _ in range(n)]
    for source in range(n):
        if source == pin:
            for target in range(n):
                if target != pin:
                    rows[source][target] = Q(1, n - 1)
        else:
            rows[source][pin] = Q(1)
    return rows


def standard_embedding(n: int, pin: int) -> list[list[Q]]:
    N = n - 1
    s = [Q(N) if vertex == pin else Q(-1) for vertex in range(n)]
    return [
        [
            Q(0)
            if source == target
            else (s[source] + N * s[target]) / (n * (n - 2))
            for target in range(n)
        ]
        for source in range(n)
    ]


def active_operator(rows: list[list[Q]], states: list[State]) -> SparseOperator:
    index = {state: position for position, state in enumerate(states)}
    operator: SparseOperator = []
    for B, v in states:
        rank = B.bit_count()
        row: dict[int, Q] = {}

        def add(target: State, mass: Q) -> None:
            if not mass:
                return
            position = index[target]
            row[position] = row.get(position, Q(0)) + mass

        for sample, mass in enumerate(rows[v]):
            add((B | (1 << sample), v), mass / 2)
        for source in range(len(rows)):
            if (B >> source) & 1:
                cache = B & ~(1 << source)
                for sample, mass in enumerate(rows[source]):
                    add((cache | (1 << sample), source), mass / (2 * rank))
        expected = sum(rows[v], Q(0))
        assert sum(row.values(), Q(0)) == expected
        operator.append({target: mass for target, mass in row.items() if mass})
    return operator


def average_operators(operators: list[SparseOperator]) -> SparseOperator:
    answer: SparseOperator = []
    scale = Q(1, len(operators))
    for row_index in range(len(operators[0])):
        row: dict[int, Q] = {}
        for operator in operators:
            for target, mass in operator[row_index].items():
                row[target] = row.get(target, Q(0)) + scale * mass
        answer.append({target: mass for target, mass in row.items() if mass})
    return answer


def apply(operator: SparseOperator, vector: list[Q]) -> list[Q]:
    return [
        sum((mass * vector[target] for target, mass in row.items()), Q(0))
        for row in operator
    ]


def row_apply(row: list[Q], operator: SparseOperator) -> list[Q]:
    answer = [Q(0) for _ in row]
    for source, source_mass in enumerate(row):
        if source_mass:
            for target, transition in operator[source].items():
                answer[target] += source_mass * transition
    return answer


def dot(row: list[Q], column: list[Q]) -> Q:
    return sum((x * y for x, y in zip(row, column)), Q(0))


def joint_pin_law(n: int, time: int):
    """Return the exact joint law of pin counts and terminal active state."""

    N = n - 1
    states = states_of_order(n)
    pins = [active_operator(replacement_pin(n, x), states) for x in range(n)]
    nu = [Q(B.bit_count(), n * N * 2 ** (N - 1)) for B, _v in states]
    law: dict[tuple[tuple[int, ...], int], Q] = {
        ((0,) * n, state): mass for state, mass in enumerate(nu)
    }
    for _step in range(time):
        new: dict[tuple[tuple[int, ...], int], Q] = {}
        for (counts, source), mass in law.items():
            for pin in range(n):
                next_counts = list(counts)
                next_counts[pin] += 1
                key_counts = tuple(next_counts)
                for target, transition in pins[pin][source].items():
                    key = (key_counts, target)
                    new[key] = new.get(key, Q(0)) + mass * transition / n
        law = new
    assert sum(law.values(), Q(0)) == 1
    return states, law


def marked_moments(n: int, time: int) -> tuple[list[Q], list[Q]]:
    states, law = joint_pin_law(n, time)
    N = n - 1
    target_moment = [Q(0) for _ in range(N + 1)]
    cache_moment = [Q(0) for _ in range(N + 1)]
    for (counts, state), mass in law.items():
        B, v = states[state]
        rank = B.bit_count()
        target_moment[rank] += mass * (counts[v] - Q(time, n))
        cache_moment[rank] += mass * (
            sum((counts[u] for u in range(n) if (B >> u) & 1), 0)
            - Q(rank * time, n)
        )
    return target_moment, cache_moment


def labelled_prefix(n: int, time: int) -> list[Q]:
    """Build (nN)^-1 nu Delta sum K0^q Delta h_j directly."""

    N = n - 1
    states = states_of_order(n)
    pins = [active_operator(replacement_pin(n, x), states) for x in range(n)]
    complete = average_operators(pins)
    direction = active_operator(standard_embedding(n, 0), states)
    nu = [Q(B.bit_count(), n * N * 2 ** (N - 1)) for B, _v in states]
    left = row_apply(nu, direction)
    answers = []
    for atom in range(1, N):
        threshold = [Q(B.bit_count() <= atom) for B, _v in states]
        packet = apply(direction, threshold)
        total = Q(0)
        for _lag in range(time):
            total += dot(left, packet)
            packet = apply(complete, packet)
        answers.append(total / (n * N))
    return answers


def marked_prefix_audit() -> None:
    comparisons = 0
    for n in range(3, 6):
        N = n - 1
        for time in range(1, 5):
            X, I = marked_moments(n, time)
            assert I[N] == -X[N]
            direct = labelled_prefix(n, time)
            for atom in range(1, N):
                bracket = atom * X[atom] + N * I[atom]
                bracket += Q(atom * n, atom + 1) * I[atom + 1]
                reduced = bracket / (2 * n * (N - 1) ** 2)
                assert reduced == direct[atom - 1]
                comparisons += 1
    print(
        "PASS (EXACT FINITE): marked-request/prefix identity "
        f"on {comparisons} labelled order-time-atoms"
    )


def add_unit(counts: tuple[int, ...], coordinate: int) -> tuple[int, ...]:
    answer = list(counts)
    answer[coordinate] += 1
    return tuple(answer)


def rank_controls(n: int, final_time: int):
    """Return uniformly word-symmetrized threshold controls by pin counts."""

    N = n - 1
    states = states_of_order(n)
    pins = [active_operator(replacement_pin(n, x), states) for x in range(n)]
    nu = [Q(B.bit_count(), n * N * 2 ** (N - 1)) for B, _v in states]
    controls = [
        {(0,) * n: [Q(B.bit_count() <= rank) for B, _v in states]}
        for rank in range(1, N)
    ]
    all_rewards = []
    for time in range(1, final_time + 1):
        new_controls = []
        for rank_control in controls:
            new: dict[tuple[int, ...], list[Q]] = {}
            for counts in compositions(time, n):
                value = [Q(0) for _state in states]
                for pin, multiplicity in enumerate(counts):
                    if not multiplicity:
                        continue
                    predecessor = list(counts)
                    predecessor[pin] -= 1
                    image = apply(pins[pin], rank_control[tuple(predecessor)])
                    scale = Q(multiplicity, time)
                    for state, entry in enumerate(image):
                        value[state] += scale * entry
                new[counts] = value
            new_controls.append(new)
        controls = new_controls
        all_rewards.append(
            [
                {counts: dot(nu, value) for counts, value in control.items()}
                for control in controls
            ]
        )
    return all_rewards


def bernstein_from_cdf(cdf: list[Q]) -> list[Q]:
    degree = len(cdf) - 1
    return [
        sum(
            (
                cdf[power]
                * Q(comb(control, power), comb(degree, power))
                for power in range(control + 1)
            ),
            Q(0),
        )
        for control in range(degree + 1)
    ]


def hypergeometric_identity_audit() -> None:
    for N in range(2, 31):
        for m in range(N - 1):
            q = N - 1 - m
            for rank in range(1, N + 1):
                coefficient = sum(
                    (
                        Q(comb(m, r - 1), comb(N - 2, r - 1))
                        for r in range(rank, m + 2)
                    ),
                    Q(0),
                )
                closed = (
                    Q(comb(N - rank, m - rank + 1), comb(N - 2, m))
                    if rank <= m + 1
                    else Q(0)
                )
                marked = Q(N - 1, q) * Q(
                    comb(N - rank, q), comb(N - 1, q)
                )
                assert coefficient == closed == marked
    print("PASS (EXACT ALL-PARAMETER IDENTITY): hypergeometric Bernstein transform")


def finite_marked_cache_screen() -> None:
    scopes = ((3, 25), (4, 12), (5, 8))
    coefficient_checks = 0
    witness = None
    for n, final_time in scopes:
        N = n - 1
        rewards_by_time = rank_controls(n, final_time)
        for time, rewards in enumerate(rewards_by_time, 1):
            for base in compositions(time - 1, n):
                for frequent, less in product(range(n), repeat=2):
                    if base[frequent] < base[less]:
                        continue
                    concentrated = add_unit(base, frequent)
                    dispersed = add_unit(base, less)
                    cdf = [
                        reward[concentrated] - reward[dispersed]
                        for reward in rewards
                    ]
                    controls = bernstein_from_cdf(cdf)
                    assert all(value >= 0 for value in controls)
                    coefficient_checks += len(controls)
                    if (
                        witness is None
                        and n == 4
                        and time == 4
                        and base == (0, 0, 1, 2)
                        and frequent == 3
                        and less == 2
                    ):
                        witness = (cdf, controls)

    assert witness is not None
    cdf, controls = witness
    assert cdf == [Q(13, 2592), -Q(227, 46656)]
    assert controls == [Q(13, 2592), Q(7, 46656)]
    print("EXACTLY REFUTED: rank-CDF order on n=4, counts (0,0,1,2)")
    print("CDF WITNESS:", cdf)
    print("SURVIVING MARKED-CACHE BERNSTEIN CONTROLS:", controls)
    print(
        "PASS (EXACT FINITE): marked-cache coefficients on "
        f"{coefficient_checks} declared comparisons"
    )


def main() -> None:
    marked_prefix_audit()
    hypergeometric_identity_audit()
    finite_marked_cache_screen()
    print("OPEN: prove every marked-cache coefficient for arbitrary n and time")


if __name__ == "__main__":
    main()
