#!/usr/bin/env python3
"""Exact certificates for the endpoint arrow-orientation calculus.

This verifier uses Fraction arithmetic and constructs the labelled-arrow set
generators directly.  It checks the divergence identity, K|A| identity,
full-state midpoint curvature, and the small rational counterexample to a
statewise curvature proof.  It does not claim the open stationary or
transient midpoint inequality.
"""

from __future__ import annotations

from fractions import Fraction as F


R = F(3, 2)
A = R - 1


def add(matrix: list[list[F]], row: int, column: int, rate: F) -> None:
    if row != column and rate:
        matrix[row][column] += rate


def finish(matrix: list[list[F]]) -> list[list[F]]:
    for row in range(len(matrix)):
        matrix[row][row] = -sum(
            (matrix[row][column] for column in range(len(matrix)) if column != row),
            F(0),
        )
    return matrix


def generators(weights: tuple[tuple[int, ...], ...]):
    n = len(weights)
    full = (1 << n) - 1
    degree = [sum(row) for row in weights]
    p = [[F(weights[i][j], degree[i]) for j in range(n)] for i in range(n)]
    left = [[F(0) for _ in range(full)] for _ in range(full)]
    reverse = [[F(0) for _ in range(full)] for _ in range(full)]
    for state in range(1, full + 1):
        row = state - 1
        for target in range(n):
            if not (state >> target) & 1:
                continue
            for source in range(n):
                neutral = (state & ~(1 << target)) | (1 << source)
                selective = state | (1 << source)
                add(left, row, neutral - 1, p[source][target])
                add(left, row, selective - 1, A * p[source][target])
                add(reverse, row, neutral - 1, p[target][source])
                add(reverse, row, selective - 1, A * p[target][source])
    return p, finish(left), finish(reverse)


def mat_vec(matrix: list[list[F]], vector: list[F]) -> list[F]:
    return [
        sum((matrix[i][j] * vector[j] for j in range(len(vector))), F(0))
        for i in range(len(matrix))
    ]


def determinant(matrix: list[list[F]]) -> F:
    """Fraction Gaussian elimination, sufficient for the small tree audit."""
    work = [row[:] for row in matrix]
    answer = F(1)
    for column in range(len(work)):
        pivot = next(row for row in range(column, len(work)) if work[row][column])
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        value = work[column][column]
        answer *= value
        for row in range(column + 1, len(work)):
            multiplier = work[row][column] / value
            for j in range(column + 1, len(work)):
                work[row][j] -= multiplier * work[column][j]
    return answer


def cofactor_tree_weight(generator: list[list[F]], root: int) -> F:
    indices = [i for i in range(len(generator)) if i != root]
    minor = [[-generator[i][j] for j in indices] for i in indices]
    return determinant(minor)


def rooted_tree_weight(
    conductance: list[list[F]], tree: tuple[tuple[int, int], ...], root: int, inward: bool
) -> F:
    adjacency = [[] for _ in conductance]
    for first, second in tree:
        adjacency[first].append(second)
        adjacency[second].append(first)
    parent = [-1] * len(conductance)
    parent[root] = root
    stack = [root]
    while stack:
        vertex = stack.pop()
        for neighbor in adjacency[vertex]:
            if parent[neighbor] == -1:
                parent[neighbor] = vertex
                stack.append(neighbor)
    assert all(value >= 0 for value in parent)
    answer = F(1)
    for vertex in range(len(conductance)):
        if vertex == root:
            continue
        ancestor = parent[vertex]
        answer *= (
            conductance[vertex][ancestor]
            if inward
            else conductance[ancestor][vertex]
        )
    return answer


def midpoint_difference(
    first: list[list[F]], second: list[list[F]]
) -> list[list[F]]:
    return [
        [(first[i][j] - second[i][j]) / 2 for j in range(len(first))]
        for i in range(len(first))
    ]


def check(weights: tuple[tuple[int, ...], ...]) -> tuple[list[F], list[F]]:
    p, left, reverse = generators(weights)
    n = len(weights)
    full = (1 << n) - 1
    incoming = [sum((p[j][i] for j in range(n)), F(0)) for i in range(n)]
    q = [1 - value for value in incoming]

    # q is the weighted divergence of the inverse-degree gradient.
    degree = [sum(row) for row in weights]
    for i in range(n):
        divergence = sum(
            (
                F(weights[i][j], 1)
                * (F(1, degree[i]) - F(1, degree[j]))
                for j in range(n)
                if weights[i][j]
            ),
            F(0),
        )
        assert divergence == q[i]
    assert sum(q, F(0)) == 0

    k = [F(state.bit_count()) for state in range(1, full + 1)]
    defect = midpoint_difference(left, reverse)
    defect_k = mat_vec(defect, k)
    for state in range(1, full + 1):
        q_mass = sum(
            (q[i] for i in range(n) if (state >> i) & 1), F(0)
        )
        assert defect_k[state - 1] == -A * q_mass / 2

    second = mat_vec(defect, defect_k)
    full_curvature = -2 * second[-1]
    assert full_curvature == sum((value * value for value in q), F(0)) / 4
    return q, [-2 * value for value in second]


def main() -> None:
    path = (
        (0, 0, 1),
        (0, 0, 1),
        (1, 1, 0),
    )
    q_path, curvature_path = check(path)
    assert q_path == [F(1, 2), F(1, 2), F(-1)]
    assert all(value >= 0 for value in curvature_path)

    # Exact in/out arborescence representation and the obstruction to a
    # proof performed one underlying spanning tree at a time.
    _, path_left, path_reverse = generators(path)
    path_mu = [A ** state.bit_count() for state in range(1, 8)]
    conductance = [
        [path_mu[i] * path_left[i][j] for j in range(7)] for i in range(7)
    ]
    for i in range(7):
        for j in range(7):
            if i != j:
                assert conductance[i][j] == path_mu[j] * path_reverse[j][i]

    mu_product = F(1)
    for value in path_mu:
        mu_product *= value
    for root in range(7):
        # The cofactor is the in-arborescence total in generator rates.
        # Extracting mu from every nonroot row gives the c-tree total.
        c_in = cofactor_tree_weight(path_left, root) * mu_product / path_mu[root]
        c_out = cofactor_tree_weight(path_reverse, root) * mu_product / path_mu[root]
        assert c_in > 0 and c_out > 0

    tree = ((0, 3), (0, 4), (2, 5), (4, 6), (2, 4), (1, 5))
    in_root = [
        path_mu[root] * rooted_tree_weight(conductance, tree, root, True)
        for root in range(7)
    ]
    out_root = [
        path_mu[root] * rooted_tree_weight(conductance, tree, root, False)
        for root in range(7)
    ]
    rank = [state.bit_count() for state in range(1, 8)]
    in_mean = sum((in_root[i] * rank[i] for i in range(7)), F(0)) / sum(
        in_root, F(0)
    )
    out_mean = sum((out_root[i] * rank[i] for i in range(7)), F(0)) / sum(
        out_root, F(0)
    )
    midpoint_mean = sum(
        (path_mu[i] * rank[i] for i in range(7)), F(0)
    ) / sum(path_mu, F(0))
    assert in_mean == F(7, 5)
    assert out_mean == F(13, 9)
    assert midpoint_mean == F(27, 19)
    assert 2 * midpoint_mean - in_mean - out_mean == F(-2, 855)

    witness = (
        (0, 1, 1, 1),
        (1, 0, 0, 0),
        (1, 0, 0, 3),
        (1, 0, 3, 0),
    )
    q_witness, curvature_witness = check(witness)
    assert q_witness == [F(-1, 2), F(2, 3), F(-1, 12), F(-1, 12)]
    singleton_three = (1 << 3) - 1
    assert curvature_witness[singleton_three] == F(-1, 72)

    # The stronger full-start transient midpoint inequality also fails.
    # python-flint/Arb evaluates the exact rational matrix exponentials with
    # rigorous balls.  This dependency is optional only in the sense that a
    # missing Arb installation should be treated as a failed certificate run.
    from flint import arb, arb_mat, ctx, fmpq

    star = (
        (0, 0, 0, 1),
        (0, 0, 0, 1),
        (0, 0, 0, 1),
        (1, 1, 1, 0),
    )
    _, star_left, star_reverse = generators(star)
    ctx.prec = 200

    def arb_matrix(matrix: list[list[F]]) -> arb_mat:
        return arb_mat(
            [
                [arb(fmpq(value.numerator, value.denominator)) for value in row]
                for row in matrix
            ]
        )

    left_arb = arb_matrix(star_left)
    reverse_arb = arb_matrix(star_reverse)
    midpoint_arb = (left_arb + reverse_arb) / 2
    time = arb(fmpq(7, 2))
    cardinality = arb_mat([[state.bit_count()] for state in range(1, 16)])
    full_start = arb_mat([[0] * 14 + [1]])
    transient_gap = (
        2 * full_start * (time * midpoint_arb).exp() * cardinality
        - full_start * (time * left_arb).exp() * cardinality
        - full_start * (time * reverse_arb).exp() * cardinality
    )[0, 0]
    assert transient_gap.upper() < 0
    assert transient_gap.lower() < arb(fmpq(-36404, 1_000_000))
    assert transient_gap.upper() > arb(fmpq(-36405, 1_000_000))

    print("PASS: exact inverse-degree divergence identity")
    print("PASS: exact K|A| = -(r-1)q(A)/2 identity")
    print("PASS: full-state initial midpoint curvature = sum(q_i^2)/4")
    print("PASS: exact statewise curvature counterexample -1/72")
    print("PASS: exact in/out arborescence representation")
    print("PASS: exact single-tree reversal obstruction -2/855")
    print("PASS: Arb-certified full-start transient star counterexample")
    print("transient midpoint gap at t=7/2:", transient_gap)


if __name__ == "__main__":
    main()
