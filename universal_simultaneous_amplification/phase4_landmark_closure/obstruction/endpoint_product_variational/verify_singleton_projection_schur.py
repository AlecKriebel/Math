#!/usr/bin/env python3
"""Exact singleton projection and higher-correlation obstruction.

Projecting the two subset-chain Poisson equations onto singleton indicators
does not close on the original vertex space.  This verifier derives and
checks the exact projected system after orthogonally removing from every
pair indicator its constant and singleton components.  The only remaining
forcing consists of genuine pair residuals.

It also tests the natural frozen-midpoint weak-orientation response.  That
vertex response is not self-adjoint in conductance geometry, already on a
weighted three-path.  This rules out the proposed self-adjoint-PSD closure;
it does not refute positivity of the response's symmetric quadratic part or
the open physical orientation inequality.
"""

from __future__ import annotations

from fractions import Fraction as F

from verify_original_graph_poisson_pairing import (
    interpolate,
    mat_vec,
    poisson_solution,
)
from verify_root_marked_tree_transform import generators, solve, stationary


R = F(3, 2)
A = R - 1


def transpose(matrix):
    return [list(column) for column in zip(*matrix)]


def matrix_product(first, second):
    return [
        [
            sum(
                (first[i][k] * second[k][j] for k in range(len(second))),
                F(0),
            )
            for j in range(len(second[0]))
        ]
        for i in range(len(first))
    ]


def matrix_sum(first, second):
    return [
        [first[i][j] + second[i][j] for j in range(len(first[0]))]
        for i in range(len(first))
    ]


def matrix_difference(first, second):
    return [
        [first[i][j] - second[i][j] for j in range(len(first[0]))]
        for i in range(len(first))
    ]


def inner(mu, first, second):
    return sum(
        (mu[i] * first[i] * second[i] for i in range(len(mu))), F(0)
    )


def centered_poisson(midpoint, mu, right):
    """Return y=(-M)^# right in the gauge <y>_mu=0."""
    size = len(midpoint)
    mean = sum((mu[i] * right[i] for i in range(size)), F(0))
    centered = [value - mean for value in right]
    system = [[-midpoint[i][j] for j in range(size)] for i in range(size)]
    system[-1] = mu[:]
    centered[-1] = F(0)
    answer = solve(system, centered)
    assert sum((mu[i] * answer[i] for i in range(size)), F(0)) == 0
    applied = mat_vec([[-value for value in row] for row in midpoint], answer)
    assert applied == [value - mean for value in right]
    return answer


def pair_list(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def moments(mu, function, n):
    size = len(mu)
    singleton = [
        sum(
            (
                mu[state - 1] * function[state - 1]
                for state in range(1, size + 1)
                if (state >> vertex) & 1
            ),
            F(0),
        )
        for vertex in range(n)
    ]
    pair = []
    for first, second in pair_list(n):
        pair.append(
            sum(
                (
                    mu[state - 1] * function[state - 1]
                    for state in range(1, size + 1)
                    if (state >> first) & 1 and (state >> second) & 1
                ),
                F(0),
            )
        )
    return singleton, pair


def projection_data(mu, n):
    """Return singleton Gram matrix and pair-on-singleton projection Lambda."""
    size = len(mu)
    singleton_mean = sum(
        (mu[state - 1] for state in range(1, size + 1) if state & 1),
        F(0),
    )
    pair_mean = sum(
        (
            mu[state - 1]
            for state in range(1, size + 1)
            if state & 1 and state & 2
        ),
        F(0),
    )
    centered_singletons = [
        [F((state >> vertex) & 1) - singleton_mean for state in range(1, size + 1)]
        for vertex in range(n)
    ]
    gram = [
        [inner(mu, centered_singletons[i], centered_singletons[j]) for j in range(n)]
        for i in range(n)
    ]
    projection = []
    residual_vectors = []
    for first, second in pair_list(n):
        centered_pair = [
            F(((state >> first) & 1) * ((state >> second) & 1)) - pair_mean
            for state in range(1, size + 1)
        ]
        covariance = [
            inner(mu, centered_singletons[vertex], centered_pair)
            for vertex in range(n)
        ]
        coefficients = solve(gram, covariance)
        projection.append(coefficients)
        residual = [
            centered_pair[state]
            - sum(
                (
                    coefficients[vertex] * centered_singletons[vertex][state]
                    for vertex in range(n)
                ),
                F(0),
            )
            for state in range(size)
        ]
        assert all(
            inner(mu, residual, centered_singletons[vertex]) == 0
            for vertex in range(n)
        )
        residual_vectors.append(residual)
    return singleton_mean, gram, projection, residual_vectors


def projected_matrices(weights):
    """Matrices for <x_i,-Mf> and <x_i,Kf> in first/pair moments."""
    n = len(weights)
    degree = [sum(row) for row in weights]
    p = [[F(0) for _ in range(n)] for _ in range(n)]
    delta = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            p[i][j] = F(weights[i][j], 2) * (
                F(1, degree[i]) + F(1, degree[j])
            )
            delta[i][j] = F(weights[i][j]) * (
                F(1, degree[i]) - F(1, degree[j])
            )
    q = [sum(row, F(0)) for row in delta]
    pairs = pair_list(n)
    pair_index = {edge: index for index, edge in enumerate(pairs)}
    first = [[F(0) for _ in range(n)] for _ in range(n)]
    first_pair = [[F(0) for _ in pairs] for _ in range(n)]
    defect = [[F(0) for _ in range(n)] for _ in range(n)]
    defect_pair = [[F(0) for _ in pairs] for _ in range(n)]
    for i in range(n):
        first[i][i] = sum(p[i], F(0))
        defect[i][i] = q[i]
        for j in range(n):
            if i == j:
                continue
            if weights[i][j]:
                first[i][j] -= R * p[i][j]
            defect[i][j] -= R * delta[i][j] / 2
            edge = (min(i, j), max(i, j))
            index = pair_index[edge]
            if weights[i][j]:
                first_pair[i][index] += R * p[i][j]
            defect_pair[i][index] += (
                R * delta[i][j] / 2 + R * q[j]
            )
    return q, first, first_pair, defect, defect_pair


def projected_system_check(weights, s):
    left, reverse = generators(weights)
    midpoint = interpolate(left, reverse, F(0))
    defect_generator = [
        [(left[i][j] - reverse[i][j]) / 2 for j in range(len(left))]
        for i in range(len(left))
    ]
    plus = interpolate(left, reverse, s)
    minus = interpolate(left, reverse, -s)
    plus_law = stationary(plus)
    minus_law = stationary(minus)
    n = len(weights)
    size = (1 << n) - 1
    rank = [F(state.bit_count()) for state in range(1, size + 1)]
    mu = [A ** state.bit_count() for state in range(1, size + 1)]
    mu = [value / sum(mu, F(0)) for value in mu]
    plus_potential, _ = poisson_solution(plus, plus_law, mu, rank)
    minus_potential, _ = poisson_solution(minus, minus_law, mu, rank)
    summed = [
        minus_potential[i] + plus_potential[i] for i in range(size)
    ]
    difference = [
        minus_potential[i] - plus_potential[i] for i in range(size)
    ]
    singleton_mean, _, projection, residual_vectors = projection_data(mu, n)
    q, first, first_pair, defect, defect_pair = projected_matrices(weights)
    first_effective = matrix_sum(first, matrix_product(first_pair, projection))
    defect_effective = matrix_sum(
        defect, matrix_product(defect_pair, projection)
    )
    # Centering x_i introduces -E_mu(x_i)<V,f>, a rank-one correction.
    centered_defect = [row[:] for row in defect_effective]
    for i in range(n):
        for j in range(n):
            centered_defect[i][j] -= singleton_mean * R * q[j]

    z_sum, pair_sum = moments(mu, summed, n)
    z_difference, pair_difference = moments(mu, difference, n)
    eta_sum = [
        pair_sum[edge]
        - sum((projection[edge][i] * z_sum[i] for i in range(n)), F(0))
        for edge in range(len(pair_sum))
    ]
    eta_difference = [
        pair_difference[edge]
        - sum(
            (projection[edge][i] * z_difference[i] for i in range(n)), F(0)
        )
        for edge in range(len(pair_difference))
    ]
    # Check eta directly against the orthogonal pair-residual vectors.
    assert eta_sum == [inner(mu, residual, summed) for residual in residual_vectors]
    assert eta_difference == [
        inner(mu, residual, difference) for residual in residual_vectors
    ]

    # The exact centered singleton equations.  The first row corresponds to
    # the sum Poisson equation, the second to the difference equation.
    covariance_rank = inner(
        mu,
        [F((state >> 0) & 1) - singleton_mean for state in range(1, size + 1)],
        rank,
    )
    sum_left = [
        value + s * other
        for value, other in zip(
            mat_vec(first_effective, z_sum),
            mat_vec(centered_defect, z_difference),
        )
    ]
    sum_forcing = [
        first_value + s * second_value
        for first_value, second_value in zip(
            mat_vec(first_pair, eta_sum),
            mat_vec(defect_pair, eta_difference),
        )
    ]
    assert [sum_left[i] + sum_forcing[i] for i in range(n)] == [
        2 * covariance_rank
    ] * n

    difference_left = [
        value + s * other
        for value, other in zip(
            mat_vec(first_effective, z_difference),
            mat_vec(centered_defect, z_sum),
        )
    ]
    difference_forcing = [
        first_value + s * second_value
        for first_value, second_value in zip(
            mat_vec(first_pair, eta_difference),
            mat_vec(defect_pair, eta_sum),
        )
    ]
    assert [
        difference_left[i] + difference_forcing[i] for i in range(n)
    ] == [F(0)] * n

    # On the audited instances the 2n-dimensional effective block is
    # nonsingular, so the exact pair-residual forcing reconstructs the
    # singleton response.  The balance identities above do not require this
    # auxiliary nonsingularity assertion universally.
    block = []
    for i in range(n):
        block.append(first_effective[i] + [s * value for value in centered_defect[i]])
    for i in range(n):
        block.append([s * value for value in centered_defect[i]] + first_effective[i])
    block_right = [
        2 * covariance_rank - sum_forcing[i] for i in range(n)
    ] + [-difference_forcing[i] for i in range(n)]
    reconstructed = solve(block, block_right)
    assert reconstructed == z_sum + z_difference

    # Direct operator audit of the two projected identities.
    for function, z, pair_moment in (
        (summed, z_sum, pair_sum),
        (difference, z_difference, pair_difference),
    ):
        direct_midpoint = [
            inner(
                mu,
                [F((state >> i) & 1) for state in range(1, size + 1)],
                mat_vec([[-value for value in row] for row in midpoint], function),
            )
            for i in range(n)
        ]
        direct_defect = [
            inner(
                mu,
                [F((state >> i) & 1) for state in range(1, size + 1)],
                mat_vec(defect_generator, function),
            )
            for i in range(n)
        ]
        assert direct_midpoint == [
            first_value + pair_value
            for first_value, pair_value in zip(
                mat_vec(first, z), mat_vec(first_pair, pair_moment)
            )
        ]
        assert direct_defect == [
            first_value + pair_value
            for first_value, pair_value in zip(
                mat_vec(defect, z), mat_vec(defect_pair, pair_moment)
            )
        ]
    return eta_sum, eta_difference


def atomic_defect(weights, vertex_field):
    """K_g from delta_ij=w_ij(g_i-g_j), assembled on every local triangle."""
    n = len(weights)
    size = (1 << n) - 1
    answer = [[F(0) for _ in range(size)] for _ in range(size)]
    block = (
        (R, -1, -A),
        (1, -R, A),
        (1, -1, 0),
    )
    for first, second in pair_list(n):
        if not weights[first][second]:
            continue
        delta = F(weights[first][second]) * (
            vertex_field[first] - vertex_field[second]
        )
        for outside in range(1 << n):
            if (outside >> first) & 1 or (outside >> second) & 1:
                continue
            states = (
                outside | (1 << first),
                outside | (1 << second),
                outside | (1 << first) | (1 << second),
            )
            for i in range(3):
                for j in range(3):
                    answer[states[i] - 1][states[j] - 1] += delta * block[i][j] / 2
    assert all(sum(row, F(0)) == 0 for row in answer)
    return answer


def weak_vertex_response(weights):
    """Z_0 g=<x,-(-M)^# K_g (-M)^# k>_mu."""
    left, reverse = generators(weights)
    midpoint = interpolate(left, reverse, F(0))
    n = len(weights)
    size = (1 << n) - 1
    mu = [A ** state.bit_count() for state in range(1, size + 1)]
    mu = [value / sum(mu, F(0)) for value in mu]
    rank = [F(state.bit_count()) for state in range(1, size + 1)]
    phi = centered_poisson(midpoint, mu, rank)
    response = [[F(0) for _ in range(n)] for _ in range(n)]
    for field_vertex in range(n):
        field = [F(int(i == field_vertex)) for i in range(n)]
        defect = atomic_defect(weights, field)
        forcing = [-value for value in mat_vec(defect, phi)]
        potential = centered_poisson(midpoint, mu, forcing)
        singleton, _ = moments(mu, potential, n)
        for i in range(n):
            response[i][field_vertex] = singleton[i]
    laplacian = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        laplacian[i][i] = F(sum(weights[i]))
        for j in range(n):
            if i != j:
                laplacian[i][j] = -F(weights[i][j])
    return matrix_product(laplacian, response)


def main() -> None:
    weighted_path = (
        (0, 0, 1),
        (0, 0, 17),
        (1, 17, 0),
    )
    eta_sum, eta_difference = projected_system_check(weighted_path, F(1))
    assert any(value for value in eta_sum + eta_difference)
    print("PASS: exact singleton/pair-residual projection on weighted P3")

    curvature_witness = (
        (0, 1, 1, 1),
        (1, 0, 0, 0),
        (1, 0, 0, 3),
        (1, 0, 3, 0),
    )
    projected_system_check(curvature_witness, F(2, 3))
    print("PASS: exact projected system on the curvature K4 witness")

    all_mark_witness = (
        (0, 1000, 1, 0, 10),
        (1000, 0, 0, 1000, 10000),
        (1, 0, 0, 1, 1000),
        (0, 1000, 1, 0, 1),
        (10, 10000, 1000, 1, 0),
    )
    projected_system_check(all_mark_witness, F(1, 2))
    print("PASS: exact projected system on the all-root-mark witness")

    rank_tail_witness = (
        (0, 2, 227000, 0, 0),
        (2, 0, 536000, 5, 85),
        (227000, 536000, 0, 941000, 650000),
        (0, 5, 941000, 0, 1),
        (0, 85, 650000, 1, 0),
    )
    projected_system_check(rank_tail_witness, F(1, 5))
    print("PASS: exact projected system on the rank-tail witness")

    # The natural frozen-midpoint linear map fails self-adjointness already
    # on weighted P3.
    path_response = weak_vertex_response(weighted_path)
    path_asymmetry = matrix_difference(path_response, transpose(path_response))
    asymmetry = F(156672, 1200325)
    assert path_asymmetry[0][1] == asymmetry
    assert path_asymmetry[0][2] == -asymmetry
    assert path_asymmetry[1][2] == asymmetry
    print("PASS: exact non-self-adjoint weak vertex response on weighted P3")
    print("weak-response cyclic asymmetry:", asymmetry)
    print("STATUS: global physical Dirichlet sign remains OPEN")


if __name__ == "__main__":
    main()
