#!/usr/bin/env python3
"""Exact audit of the r=2 factorial-moment recurrence and finite screen.

All transition probabilities and invariant laws are computed over QQ with
python-flint.  Finite screening is not a proof of the universal hierarchy.
"""

from __future__ import annotations

from itertools import combinations, product
from math import comb
from random import Random

from flint import fmpq as Q, fmpq_mat


def weight_matrix(n: int, edge_weights) -> list[list[int]]:
    weights = [[0 for _ in range(n)] for _ in range(n)]
    for value, (u, v) in zip(edge_weights, combinations(range(n), 2)):
        weights[u][v] = weights[v][u] = value
    return weights


def connected(weights) -> bool:
    seen = {0}
    stack = [0]
    while stack:
        v = stack.pop()
        for u, value in enumerate(weights[v]):
            if value and u not in seen:
                seen.add(u)
                stack.append(u)
    return len(seen) == len(weights)


def row_kernel(weights) -> list[list[Q]]:
    answer = []
    for v, row in enumerate(weights):
        degree = sum(row)
        assert degree > 0 and row[v] == 0
        answer.append([Q(value, degree) for value in row])
    return answer


def union_law(row: list[Q]) -> dict[int, Q]:
    """Law of the distinct values in a fair-geometric sample burst."""
    support = [i for i, value in enumerate(row) if value]
    values = [Q(0) for _ in range(1 << len(support))]
    for mask in range(1, 1 << len(support)):
        mass = sum(
            (row[support[j]] for j in range(len(support)) if mask >> j & 1),
            Q(0),
        )
        values[mask] = mass / (2 - mass)
    for j in range(len(support)):
        for mask in range(1 << len(support)):
            if mask >> j & 1:
                values[mask] -= values[mask ^ (1 << j)]
    answer = {}
    for mask in range(1, 1 << len(support)):
        actual = sum(
            (1 << support[j] for j in range(len(support)) if mask >> j & 1),
            0,
        )
        if values[mask]:
            assert values[mask] > 0
            answer[actual] = values[mask]
    assert sum(answer.values(), Q(0)) == 1
    return answer


def stationary_data(weights):
    P = row_kernel(weights)
    n = len(P)
    states = list(range(1, (1 << n) - 1))
    index = {state: i for i, state in enumerate(states)}
    laws = [union_law(row) for row in P]
    transition = fmpq_mat(len(states), len(states))
    for source, A in enumerate(states):
        for v in range(n):
            if not A >> v & 1:
                transition[source, source] += Q(1, n)
            else:
                for U, probability in laws[v].items():
                    B = (A & ~(1 << v)) | U
                    transition[source, index[B]] += probability / n
        assert sum((transition[source, j] for j in range(len(states))), Q(0)) == 1
    system = transition.transpose() - fmpq_mat(
        len(states), len(states),
        [int(i == j) for i in range(len(states)) for j in range(len(states))],
    )
    rhs = fmpq_mat(len(states), 1)
    for j in range(len(states)):
        system[len(states) - 1, j] = 1
    rhs[len(states) - 1, 0] = 1
    solution = system.solve(rhs)
    stationary = [solution[i, 0] for i in range(len(states))]
    assert all(value > 0 for value in stationary)
    assert sum(stationary, Q(0)) == 1
    assert transition.transpose() * solution == solution
    return P, states, laws, stationary


def coverage(row: list[Q], subset: int) -> Q:
    """Probability that every member of nonempty ``subset`` is hit."""
    if not subset:
        return Q(1)
    vertices = [i for i in range(len(row)) if subset >> i & 1]
    inclusion = Q(0)
    laplace = Q(0)
    for mask in range(1 << len(vertices)):
        mass = sum(
            (row[vertices[j]] for j in range(len(vertices)) if mask >> j & 1),
            Q(0),
        )
        sign = -1 if mask.bit_count() % 2 else 1
        inclusion += sign * (1 - mass) / (1 + mass)
        laplace += 2 * sign / (1 + mass)
    assert inclusion == laplace and inclusion >= 0
    return inclusion


def coverage_sum(row: list[Q], holes: int, order: int) -> Q:
    if order == 0:
        return Q(1)
    vertices = [i for i in range(len(row)) if holes >> i & 1]
    return sum(
        (coverage(row, sum(1 << vertices[j] for j in chosen))
         for chosen in combinations(range(len(vertices)), order)),
        Q(0),
    )


def conditional_moment(A, v, order, laws) -> Q:
    return sum(
        (probability * comb(((A & ~(1 << v)) | U).bit_count(), order)
         for U, probability in laws[v].items()),
        Q(0),
    )


def complete_moment(n: int, order: int) -> Q:
    N = n - 1
    return Q(comb(N, order) * 2 ** (N - order), 2**N - 1)


def audit_graph(weights, check_recurrence=False):
    P, states, laws, stationary = stationary_data(weights)
    n = len(P)
    moments = [
        sum(
            (probability * comb(A.bit_count(), order)
             for A, probability in zip(states, stationary)),
            Q(0),
        )
        for order in range(1, n)
    ]
    slacks = [complete_moment(n, j) - moments[j - 1] for j in range(1, n)]
    assert all(slack >= 0 for slack in slacks), (weights, slacks)

    if check_recurrence:
        for A in states:
            k = A.bit_count()
            holes = ((1 << n) - 1) ^ A
            for v in range(n):
                if not A >> v & 1:
                    continue
                for order in range(1, n):
                    formula = sum(
                        (Q(comb(k - 1, order - ell))
                         * coverage_sum(P[v], holes, ell)
                         for ell in range(order + 1)),
                        Q(0),
                    )
                    assert formula == conditional_moment(A, v, order, laws)
        for order, moment in enumerate(moments, 1):
            rhs = Q(0)
            for A, probability in zip(states, stationary):
                k = A.bit_count()
                holes = ((1 << n) - 1) ^ A
                local = Q(0)
                for v in range(n):
                    if A >> v & 1:
                        local += sum(
                            (Q(comb(k - 1, order - ell))
                             * coverage_sum(P[v], holes, ell)
                             for ell in range(1, order + 1)),
                            Q(0),
                        )
                rhs += probability * local
            assert rhs == order * moment
    return slacks


def deterministic_graphs(n: int, count: int, seed: int):
    rng = Random(seed)
    alphabet = (0, 0, 1, 2, 7, 100, 1000)
    while count:
        weights = weight_matrix(
            n, [rng.choice(alphabet) for _ in range(n * (n - 1) // 2)]
        )
        if connected(weights):
            yield weights
            count -= 1


def pointwise_failure():
    path = weight_matrix(4, (1, 0, 0, 1, 0, 1))
    complete = weight_matrix(4, (1, 1, 1, 1, 1, 1))
    A, v = 0b1101, 0  # {0,2,3}; the sole old hole is vertex 1.
    _, _, laws_path, _ = stationary_data(path)
    _, _, laws_complete, _ = stationary_data(complete)
    for order in range(1, 4):
        gap = (
            conditional_moment(A, v, order, laws_path)
            - conditional_moment(A, v, order, laws_complete)
        )
        assert gap == Q(comb(2, order - 1), 2) and gap > 0
    print("PASS: exact P4 pointwise complete-transition comparison is false")


def main():
    frozen = [
        ("P3", weight_matrix(3, (1, 1, 0))),
        ("K4-cycle4-diagonal1", weight_matrix(4, (4, 1, 4, 4, 1, 4))),
        ("n5-log-concavity", weight_matrix(5, (0, 1000, 7, 0, 0, 0, 7, 0, 7, 0))),
        ("n6-split", weight_matrix(6, (3, 300, 2, 5, 1, 3, 3, 1, 300, 1, 1, 1, 20, 1, 1))),
        ("n6-rank-tail", weight_matrix(6, (1, 3, 3, 1000, 30, 1000, 300, 3, 1, 10, 1, 30, 1, 300, 30))),
    ]
    for label, weights in frozen:
        slacks = audit_graph(weights, check_recurrence=True)
        print(label, "PASS", [f"{float(value):.10g}" for value in slacks])

    counts = []
    for n, alphabet in ((3, (0, 1, 2, 5)), (4, (0, 1, 2))):
        tested = 0
        for values in product(alphabet, repeat=n * (n - 1) // 2):
            weights = weight_matrix(n, values)
            if connected(weights):
                audit_graph(weights)
                tested += 1
        counts.append((n, tested))
    tested = 0
    for weights in deterministic_graphs(5, 48, 26080805):
        audit_graph(weights)
        tested += 1
    counts.append((5, tested))
    pointwise_failure()
    print("PASS: exact coverage identity and falling-factorial recurrence")
    print("PASS: exact finite factorial-moment screen", counts)
    print("OPEN: universal factorial-moment hierarchy (including order one)")


if __name__ == "__main__":
    main()

