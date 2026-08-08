#!/usr/bin/env python3
"""Exact directed-kernel audit for the true r=2 collision target.

Directed loopless row kernels are outside the admissible undirected graph
model.  They are tested here because a violation would prove that vertex-walk
reversibility is indispensable.  The script checks two distinct signs:

* true collision: ``1/m - 1/m_K >= 0``;
* stronger promotion: ``1/m - U M_P^2 psi >= 0``.

The stationary fair-geometric union chain and both signs are constructed over
QQ.  A promotion violation alone refutes only that sufficient proof route; a
true-collision violation would be the more important directed witness.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product
from math import comb
from random import Random

from flint import fmpq, fmpq_mat


Q = fmpq
ALPHABET = (1, 2, 10, 1000, 10**6)


def as_float(value: Q) -> float:
    return int(value.p) / int(value.q)


def union_law(row: list[Q]) -> dict[int, Q]:
    support = [i for i, probability in enumerate(row) if probability]
    values = [Q(0) for _ in range(1 << len(support))]
    for mask in range(1, 1 << len(support)):
        mass = sum(
            (row[support[j]] for j in range(len(support)) if mask >> j & 1),
            Q(0),
        )
        values[mask] = mass / (2 - mass)
    # Boolean-lattice Moebius inversion.
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


def normalized_kernel(weights) -> list[list[Q]]:
    n = len(weights)
    answer = []
    for v, row in enumerate(weights):
        converted = [Q(value) if isinstance(value, int) else value for value in row]
        if converted[v]:
            raise ValueError("loop")
        degree = sum(converted, Q(0))
        if not degree:
            raise ValueError("zero row")
        answer.append([value / degree for value in converted])
    return answer


def stationary_mean(weights) -> tuple[Q, list[list[Q]]]:
    P = normalized_kernel(weights)
    n = len(P)
    states = list(range(1, (1 << n) - 1))
    index = {state: row for row, state in enumerate(states)}
    size = len(states)
    laws = [union_law(P[v]) for v in range(n)]
    transition = fmpq_mat(size, size)
    for state, row in index.items():
        for v in range(n):
            if not state >> v & 1:
                transition[row, row] += Q(1, n)
            else:
                for union, probability in laws[v].items():
                    target = (state & ~(1 << v)) | union
                    transition[row, index[target]] += probability / n
        assert sum((transition[row, column] for column in range(size)), Q(0)) == 1

    matrix = transition.transpose() - fmpq_mat(size, size, [
        Q(int(row == column)) for row in range(size) for column in range(size)
    ])
    for column in range(size):
        matrix[size - 1, column] = 1
    rhs = fmpq_mat(size, 1)
    rhs[size - 1, 0] = 1
    stationary = matrix.solve(rhs)
    masses = [stationary[row, 0] for row in range(size)]
    if not all(mass > 0 for mass in masses):
        raise ValueError("proper dual is not irreducible")
    assert sum(masses, Q(0)) == 1
    mean = sum(
        (mass * state.bit_count() for mass, state in zip(masses, states)), Q(0)
    )
    return mean, P


def integrated_two_step(P: list[list[Q]]) -> Q:
    n = len(P)
    N = n - 1
    reference = Q(2**N - 1, N * 2 ** (N - 1))
    row_square = sum((P[v][i] ** 2 for v in range(n) for i in range(n)), Q(0))
    columns = [sum((P[v][i] for v in range(n)), Q(0)) for i in range(n)]
    column_square = sum((value**2 for value in columns), Q(0))
    mutual = sum((P[v][i] * P[i][v] for v in range(n) for i in range(n)), Q(0))
    defect_1 = row_square - Q(n, n - 1)
    defect_2 = (column_square - mutual) - (n - row_square)
    assert defect_1 >= 0 and defect_2 >= 0
    if n == 3:
        return reference + defect_1 / 24
    s = n - 2
    integrated_sum = sum(
        (Q(comb(s - 2, j), (j + 1) * (j + 2) ** 2) for j in range(s - 1)),
        Q(0),
    )
    integrated_half = Q(2**s - 1, s) - Q(2 ** (s + 1) - 1, 2 * (s + 1))
    alpha = (integrated_half - integrated_sum) / (n * 2**s)
    beta = integrated_sum / (2 * n * 2**s)
    return reference + alpha * defect_1 + beta * defect_2


def margins(weights):
    mean, P = stationary_mean(weights)
    n = len(P)
    inverse_complete_mean = Q(2 ** (n - 1) - 1, (n - 1) * 2 ** (n - 2))
    inverse_mean = 1 / mean
    return inverse_mean - inverse_complete_mean, inverse_mean - integrated_two_step(P), mean


def positive_matrix(n: int, values) -> list[list[Q]]:
    iterator = iter(values)
    return [
        [Q(0) if u == v else Q(next(iterator)) for v in range(n)]
        for u in range(n)
    ]


def corpus():
    # Exhaustive K3 row ratios after fixing one outgoing weight per row.
    ratios = (1, 2, 10, 1000, 10**6)
    for values in product(ratios, repeat=3):
        yield "K3-row-grid", [
            [Q(0), Q(1), Q(values[0])],
            [Q(values[1]), Q(0), Q(1)],
            [Q(1), Q(values[2]), Q(0)],
        ]

    # Positive perturbations of every nontrivial permutation kernel.
    for n in range(3, 8):
        count = 0
        for permutation in permutations(range(n)):
            if any(permutation[v] == v for v in range(n)):
                continue
            count += 1
            if count > (80 if n <= 5 else 30):
                break
            for dominant in (2, 10, 1000, 10**6, 10**12):
                weights = [
                    [Q(0) if u == v else Q(dominant if v == permutation[u] else 1)
                     for v in range(n)]
                    for u in range(n)
                ]
                yield f"n{n}-permutation-perturbation", weights

    # Seeded complete-support directed rational kernels over many scales.
    rng = Random(26080809)
    for n, count in ((4, 400), (5, 300), (6, 120), (7, 50)):
        for _ in range(count):
            values = [rng.choice(ALPHABET) for _ in range(n * (n - 1))]
            yield f"n{n}-seeded-directed", positive_matrix(n, values)


def main() -> None:
    tested = 0
    collision_violations = []
    promotion_violations = []
    smallest_collision = None
    smallest_promotion = None
    reducible = 0
    by_label: dict[str, int] = {}
    for label, weights in corpus():
        try:
            collision, promotion, mean = margins(weights)
        except ValueError:
            reducible += 1
            continue
        record = (collision, promotion, mean, label, weights)
        if collision < 0:
            collision_violations.append(record)
        if promotion < 0:
            promotion_violations.append(record)
        if smallest_collision is None or collision < smallest_collision[0]:
            smallest_collision = record
        if smallest_promotion is None or promotion < smallest_promotion[1]:
            smallest_promotion = record
        tested += 1
        by_label[label] = by_label.get(label, 0) + 1

    assert smallest_collision is not None and smallest_promotion is not None
    print("EXACT DIRECTED KERNEL SCREEN", tested, "irreducible kernels; reducible=", reducible)
    for label, count in sorted(by_label.items()):
        print(f"  {label}: {count}")
    print(
        "true-collision violations=", len(collision_violations),
        "stronger-promotion violations=", len(promotion_violations),
    )
    collision, promotion, mean, label, weights = smallest_collision
    print(
        "smallest true-collision margin:", label, collision,
        f"(~{as_float(collision):.17g}); promotion~{as_float(promotion):.17g};",
        "mean=", mean,
    )
    print("weights=", [[str(value) for value in row] for row in weights])
    collision, promotion, mean, label, weights = smallest_promotion
    print(
        "smallest promotion margin:", label, promotion,
        f"(~{as_float(promotion):.17g}); collision~{as_float(collision):.17g};",
        "mean=", mean,
    )
    print("weights=", [[str(value) for value in row] for row in weights])
    if collision_violations:
        print("DIRECTED TRUE-COLLISION COUNTEREXAMPLE FOUND EXACTLY")
    else:
        print("No true-collision violation in this directed corpus.")
    if promotion_violations:
        print("DIRECTED STRONGER-PROMOTION COUNTEREXAMPLE FOUND EXACTLY")
    else:
        print("No stronger-promotion violation in this directed corpus.")
    print("Directed kernels are diagnostic only and are not admissible undirected graphs.")


if __name__ == "__main__":
    main()
