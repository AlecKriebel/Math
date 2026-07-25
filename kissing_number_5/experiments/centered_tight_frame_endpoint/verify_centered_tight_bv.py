#!/usr/bin/env python3
"""Exact verifier for the centered tight-frame BV pseudodistribution.

The certificate is a rational pair/triple pseudodistribution.  It is not a
Gram matrix or a spherical code.  Only the Python standard library is used,
and every finite calculation is performed with ``fractions.Fraction``.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "centered_tight_bv_pseudodistribution.json"


def zero_matrix(size: int) -> list[list[Q]]:
    return [[Q(0) for _ in range(size)] for _ in range(size)]


def symmetric(matrix: list[list[Q]]) -> bool:
    return all(
        matrix[i][j] == matrix[j][i]
        for i in range(len(matrix))
        for j in range(len(matrix))
    )


def matrix_vector(
    matrix: list[list[Q]], vector: list[Q]
) -> list[Q]:
    return [
        sum(entry * value for entry, value in zip(row, vector))
        for row in matrix
    ]


def ldl_pivots(matrix: list[list[Q]]) -> list[Q]:
    """Exact unpivoted LDL^T pivots."""

    size = len(matrix)
    lower = zero_matrix(size)
    pivots: list[Q] = []
    for i in range(size):
        lower[i][i] = 1
        for j in range(i):
            assert pivots[j] != 0
            lower[i][j] = (
                matrix[i][j]
                - sum(
                    lower[i][h] * lower[j][h] * pivots[h]
                    for h in range(j)
                )
            ) / pivots[j]
        pivots.append(
            matrix[i][i]
            - sum(lower[i][h] ** 2 * pivots[h] for h in range(i))
        )
    return pivots


def determinant(matrix: list[list[Q]]) -> Q:
    """Exact determinant by fraction-preserving Gaussian elimination."""

    work = [row[:] for row in matrix]
    answer = Q(1)
    for column in range(len(work)):
        pivot = next(
            (
                row
                for row in range(column, len(work))
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        pivot_value = work[column][column]
        answer *= pivot_value
        for row in range(column + 1, len(work)):
            multiplier = work[row][column] / pivot_value
            for entry in range(column + 1, len(work)):
                work[row][entry] -= multiplier * work[column][entry]
    return answer


def inverse(matrix: list[list[Q]]) -> list[list[Q]]:
    """Exact Gauss--Jordan inverse."""

    size = len(matrix)
    work = [
        row[:] + [Q(i == j) for j in range(size)]
        for i, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            row
            for row in range(column, size)
            if work[row][column] != 0
        )
        work[column], work[pivot] = work[pivot], work[column]
        scale = work[column][column]
        work[column] = [value / scale for value in work[column]]
        for row in range(size):
            if row == column:
                continue
            scale = work[row][column]
            if scale:
                work[row] = [
                    value - scale * pivot_value
                    for value, pivot_value in zip(
                        work[row], work[column]
                    )
                ]
    return [row[size:] for row in work]


def ceil_sqrt_fraction(value: Q) -> int:
    """Least integer n with n^2 >= value, without floating point."""

    assert value > 0
    answer = math.isqrt(value.numerator // value.denominator)
    while answer * answer * value.denominator < value.numerator:
        answer += 1
    while (
        answer
        and (answer - 1) ** 2 * value.denominator >= value.numerator
    ):
        answer -= 1
    return answer


def gegenbauer_5_sequence(t: Q, maximum_degree: int) -> list[Q]:
    """Normalized dimension-five Gegenbauer values P_0(t),...,P_m(t)."""

    values = [Q(1)]
    if maximum_degree == 0:
        return values
    values.append(t)
    for degree in range(2, maximum_degree + 1):
        values.append(
            (
                (2 * degree + 1) * t * values[-1]
                - (degree - 1) * values[-2]
            )
            / (degree + 2)
        )
    return values


def normalized_transverse_sequences(
    area: Q, displacement: Q, maximum_index: int
) -> tuple[list[Q], list[Q]]:
    """Rational parity-normalized dimension-four transverse kernels.

    If z=displacement/sqrt(area), the even entries are P_(2m)^(4)(z)
    and the odd entries are sqrt(area) P_(2m+1)^(4)(z).
    """

    assert area > 0
    transformed = 4 * displacement * displacement / area - 2
    even = [Q(1), (4 * displacement * displacement / area - 1) / 3]
    odd = [displacement, 2 * displacement**3 / area - displacement]
    while len(even) <= maximum_index:
        degree = 2 * (len(even) - 1)
        even.append(
            (
                transformed * (degree + 1) * even[-1]
                - (degree - 1) * even[-2]
            )
            / (degree + 3)
        )
    while len(odd) <= maximum_index:
        degree = 2 * (len(odd) - 1) + 1
        odd.append(
            (
                transformed * (degree + 1) * odd[-1]
                - (degree - 1) * odd[-2]
            )
            / (degree + 3)
        )
    return even, odd


def harmonic_dimension(degree: int) -> int:
    first = math.comb(degree + 4, 4)
    second = math.comb(degree + 2, 4) if degree >= 2 else 0
    return first - second


def common_pair_capacity(projected: Q) -> int | None:
    """Exact endpoint convention for the projected S^2 cap bound."""

    if projected > 1:
        return 0
    if projected > Q(3, 4):
        return 1
    if projected > Q(2, 3):
        return 2
    if projected > Q(5, 8):
        return 3
    if projected > Q(1, 2):
        return 4
    if projected == Q(1, 2):
        return 6
    return None


def rank_kernel_specs() -> tuple[
    tuple[str, tuple[tuple[int, Q], ...]], ...
]:
    """The 27 low-degree harmonic combinations of rank below 41."""

    return (
        ("H1", ((1, Q(1)),)),
        ("H2", ((2, Q(1)),)),
        ("H3", ((3, Q(1)),)),
        ("H0+5H1", ((0, Q(1, 6)), (1, Q(5, 6)))),
        ("H0-5H1", ((0, Q(1, 6)), (1, Q(-5, 6)))),
        ("H0+14H2", ((0, Q(1, 15)), (2, Q(14, 15)))),
        ("H0-14H2", ((0, Q(1, 15)), (2, Q(-14, 15)))),
        ("5H1+14H2", ((1, Q(5, 19)), (2, Q(14, 19)))),
        ("5H1-14H2", ((1, Q(5, 19)), (2, Q(-14, 19)))),
        ("H0+H1", ((0, Q(1, 2)), (1, Q(1, 2)))),
        ("H0-H1", ((0, Q(1, 2)), (1, Q(-1, 2)))),
        ("H0+H2", ((0, Q(1, 2)), (2, Q(1, 2)))),
        ("H0-H2", ((0, Q(1, 2)), (2, Q(-1, 2)))),
        ("H1+H2", ((1, Q(1, 2)), (2, Q(1, 2)))),
        ("H1-H2", ((1, Q(1, 2)), (2, Q(-1, 2)))),
        (
            "H0+5H1+14H2",
            ((0, Q(1, 20)), (1, Q(1, 4)), (2, Q(7, 10))),
        ),
        (
            "H0+5H1-14H2",
            ((0, Q(1, 20)), (1, Q(1, 4)), (2, Q(-7, 10))),
        ),
        (
            "H0-5H1+14H2",
            ((0, Q(1, 20)), (1, Q(-1, 4)), (2, Q(7, 10))),
        ),
        (
            "H0-5H1-14H2",
            ((0, Q(1, 20)), (1, Q(-1, 4)), (2, Q(-7, 10))),
        ),
        ("H0+30H3", ((0, Q(1, 31)), (3, Q(30, 31)))),
        ("H0-30H3", ((0, Q(1, 31)), (3, Q(-30, 31)))),
        ("5H1+30H3", ((1, Q(1, 7)), (3, Q(6, 7)))),
        ("5H1-30H3", ((1, Q(1, 7)), (3, Q(-6, 7)))),
        (
            "H0+5H1+30H3",
            ((0, Q(1, 36)), (1, Q(5, 36)), (3, Q(5, 6))),
        ),
        (
            "H0+5H1-30H3",
            ((0, Q(1, 36)), (1, Q(5, 36)), (3, Q(-5, 6))),
        ),
        (
            "H0-5H1+30H3",
            ((0, Q(1, 36)), (1, Q(-5, 36)), (3, Q(5, 6))),
        ),
        (
            "H0-5H1-30H3",
            ((0, Q(1, 36)), (1, Q(-5, 36)), (3, Q(-5, 6))),
        ),
    )


def verify(source_path: Path = CERTIFICATE) -> dict[str, object]:
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    assert source["schema"] == (
        "centered-tight-bv-all-harmonic-pseudodistribution-v1"
    )
    assert source["status"] == "COMPUTATIONALLY CERTIFIED"
    assert source["scope"] == (
        "Exact pair/triple pseudodistribution; "
        "not a Gram matrix or spherical code."
    )
    assert source["known_failure"] == (
        "Violates four corrected exact-stratum common-pair "
        "capacity inequalities."
    )
    assert source["dimension"] == 5 and source["cardinality"] == 41
    assert Q(source["maximum_inner_product"]) == Q(1, 2)

    nodes = [Q(value) for value in source["nodes"]]
    alpha = [Q(value) for value in source["alpha"]]
    triples = [tuple(item) for item in source["triple_orbits"]]
    nu = [Q(value) for value in source["nu"]]
    assert nodes == [
        Q(-4, 5),
        Q(-3, 4),
        Q(-1, 2),
        Q(-7, 20),
        Q(-3, 10),
        Q(-1, 4),
        Q(-3, 20),
        Q(-1, 20),
        Q(0),
        Q(3, 10),
        Q(1, 2),
    ]
    assert alpha == [2, 2, 4, 2, 2, 2, 2, 8, 2, 2, 12]
    assert len(triples) == len(nu) == 246
    assert all(weight > 0 for weight in alpha + nu)
    assert sum(alpha) == 40 and sum(nu) == 40 * 39

    feasible = []
    for triple in itertools.combinations_with_replacement(range(11), 3):
        u, v, t = (nodes[index] for index in triple)
        determinant_3 = 1 + 2 * u * v * t - u * u - v * v - t * t
        if determinant_3 >= 0:
            feasible.append(triple)
    assert triples == feasible
    for index in range(11):
        marginal = sum(
            weight * Q(triple.count(index), 3)
            for triple, weight in zip(triples, nu)
        )
        assert marginal == 39 * alpha[index]

    # Exact centered/tight pair moments and exact cubic trace endpoint.
    pair_first = sum(weight * node for weight, node in zip(alpha, nodes))
    pair_second = sum(
        weight * node * node for weight, node in zip(alpha, nodes)
    )
    triple_cycle = sum(
        weight * nodes[i] * nodes[j] * nodes[k]
        for weight, (i, j, k) in zip(nu, triples)
    )
    assert pair_first == -1
    assert pair_second == Q(36, 5)
    assert triple_cycle == Q(1116, 25)
    trace_one = Q(41)
    trace_two = Q(41) * (1 + pair_second)
    trace_three = Q(41) * (
        1 + 3 * pair_second + triple_cycle
    )
    assert trace_two == Q(1681, 5)
    assert trace_three == Q(68921, 25)
    assert trace_two == 5 * Q(41, 5) ** 2
    assert trace_three == 5 * Q(41, 5) ** 3

    # Ordinary two-point harmonic inequalities in every degree.
    pair_sequences = [
        gegenbauer_5_sequence(node, 89) for node in nodes
    ]
    pair_moments = []
    for degree in range(90):
        moment = 1 + sum(
            alpha[index] * pair_sequences[index][degree]
            for index in range(11)
        )
        pair_moments.append(moment)
        assert moment >= 0
    assert pair_moments[1] == pair_moments[2] == 0
    assert min(pair_moments[3:]) == Q(21, 1600)

    reciprocal_sqrt_upper_bounds = {
        Q(-4, 5): Q(5, 3),
        Q(-3, 4): Q(8, 5),
        Q(-1, 2): Q(7, 6),
        Q(-7, 20): Q(15, 14),
        Q(-3, 10): Q(21, 20),
        Q(-1, 4): Q(21, 20),
        Q(-3, 20): Q(51, 50),
        Q(-1, 20): Q(501, 500),
        Q(0): Q(1),
        Q(3, 10): Q(21, 20),
        Q(1, 2): Q(7, 6),
    }
    for node, upper in reciprocal_sqrt_upper_bounds.items():
        assert upper * upper * (1 - node * node) >= 1
    weighted_pair_tail = sum(
        weight * reciprocal_sqrt_upper_bounds[node]
        for weight, node in zip(alpha, nodes)
    )
    assert weighted_pair_tail == Q(79973, 1750)
    assert 2 * weighted_pair_tail < 92
    # Bernstein's derivative inequality now proves strict positivity for
    # every degree k>=90.

    # Build the k=0 radial block.  An orbit weight is spread uniformly over
    # its distinct ordered permutations.
    node_w_zero = zero_matrix(11)
    for index, weight in enumerate(alpha):
        node_w_zero[index][index] += weight
    ordered_orbits: list[
        tuple[int, int, Q, Q, Q, Q]
    ] = []
    coefficient_matrices: dict[
        tuple[Q, Q], list[list[Q]]
    ] = {}
    index_of = {node: index for index, node in enumerate(nodes)}
    for triple, weight in zip(triples, nu):
        values = tuple(nodes[index] for index in triple)
        orbit = sorted(set(itertools.permutations(values)))
        coefficient = weight / len(orbit)
        for u, v, t in orbit:
            i, j = index_of[u], index_of[v]
            node_w_zero[i][j] += coefficient
            area = (1 - u * u) * (1 - v * v)
            displacement = t - u * v
            delta = area - displacement * displacement
            assert area > 0 and delta >= 0
            coefficient_matrix = coefficient_matrices.setdefault(
                (area, displacement), zero_matrix(11)
            )
            coefficient_matrix[i][j] += coefficient
            ordered_orbits.append(
                (i, j, coefficient, area, displacement, delta)
            )
    assert symmetric(node_w_zero)
    assert all(
        symmetric(matrix) for matrix in coefficient_matrices.values()
    )
    assert matrix_vector(node_w_zero, [Q(1)] * 11) == [
        40 * weight for weight in alpha
    ]

    # Eliminating the appended diagonal atom with the fixed-cardinality
    # kernel sends the full centered radial function u to u+1/40 and the
    # full tight radial function u^2-1/5 to u^2-9/50.
    centered_node_kernel = [node + Q(1, 40) for node in nodes]
    tight_node_kernel = [
        node * node - Q(9, 50) for node in nodes
    ]
    assert matrix_vector(
        node_w_zero, centered_node_kernel
    ) == [Q(0)] * 11
    assert matrix_vector(
        node_w_zero, tight_node_kernel
    ) == [Q(0)] * 11
    assert (
        centered_node_kernel[0] * tight_node_kernel[1]
        - centered_node_kernel[1] * tight_node_kernel[0]
    ) != 0
    w_zero_reduced = [row[2:] for row in node_w_zero[2:]]
    w_zero_pivots = ldl_pivots(w_zero_reduced)
    assert all(pivot > 0 for pivot in w_zero_pivots)

    # Append the diagonal atom u=1.  The two node kernels and the
    # fixed-cardinality kernel prove nullity at least three, while the
    # positive 9-by-9 principal block proves rank at least nine.
    full_w_zero = zero_matrix(12)
    for i in range(11):
        for j in range(11):
            full_w_zero[i][j] = node_w_zero[i][j]
        full_w_zero[i][-1] = alpha[i]
        full_w_zero[-1][i] = alpha[i]
    full_w_zero[-1][-1] = 1
    fixed_size_kernel = [Q(-1, 40)] * 11 + [Q(1)]
    full_centered_kernel = nodes + [Q(1)]
    full_tight_kernel = [
        node * node - Q(1, 5) for node in nodes
    ] + [Q(4, 5)]
    assert matrix_vector(full_w_zero, fixed_size_kernel) == [Q(0)] * 12
    assert matrix_vector(
        full_w_zero, full_centered_kernel
    ) == [Q(0)] * 12
    assert matrix_vector(
        full_w_zero, full_tight_kernel
    ) == [Q(0)] * 12
    assert determinant(
        [
            [
                fixed_size_kernel[index],
                full_centered_kernel[index],
                full_tight_kernel[index],
            ]
            for index in (0, 1, 11)
        ]
    ) != 0

    # Finite exact verification of every positive-degree radial block
    # through degree 186.  The parity normalization is a diagonal
    # congruence of the usual Bachoc--Vallentin block.
    finite_through = 186
    maximum_index = finite_through // 2 + 1
    transverse_sequences = {
        key: normalized_transverse_sequences(*key, maximum_index)
        for key in coefficient_matrices
    }
    minimum_finite_pivot: tuple[Q, int, int] | None = None
    w_one_kernel_one = [Q(1)] * 11
    w_one_kernel_two = nodes
    # Tightness gives the all-ones kernel in the unscaled W_2 block.
    # The parity normalization divides row i by (1-u_i^2), so its kernel
    # becomes the vector (1-u_i^2) in these coordinates.
    w_two_kernel = [1 - node * node for node in nodes]
    for degree in range(1, finite_through + 1):
        parity = degree % 2
        sequence_index = degree // 2
        matrix = zero_matrix(11)
        for i, node in enumerate(nodes):
            matrix[i][i] = alpha[i]
            if parity:
                matrix[i][i] *= 1 - node * node
        for key, coefficient_matrix in coefficient_matrices.items():
            kernel_value = transverse_sequences[key][parity][sequence_index]
            for i in range(11):
                for j in range(11):
                    matrix[i][j] += (
                        coefficient_matrix[i][j] * kernel_value
                    )
        assert symmetric(matrix)
        if degree == 1:
            assert (
                w_one_kernel_one[0] * w_one_kernel_two[1]
                - w_one_kernel_one[1] * w_one_kernel_two[0]
            ) != 0
            assert matrix_vector(matrix, w_one_kernel_one) == [Q(0)] * 11
            assert matrix_vector(matrix, w_one_kernel_two) == [Q(0)] * 11
            reduced = [row[2:] for row in matrix[2:]]
        elif degree == 2:
            assert matrix_vector(matrix, w_two_kernel) == [Q(0)] * 11
            reduced = [row[1:] for row in matrix[1:]]
        else:
            reduced = matrix
        pivots = ldl_pivots(reduced)
        assert all(pivot > 0 for pivot in pivots)
        for index, pivot in enumerate(pivots):
            candidate = (pivot, degree, index)
            if (
                minimum_finite_pivot is None
                or candidate[0] < minimum_finite_pivot[0]
            ):
                minimum_finite_pivot = candidate
    assert minimum_finite_pivot is not None

    # Exact limiting matrices and analytic all-degree tail.  The only
    # nondecaying contributions are determinant-zero transverse triples.
    limits = [zero_matrix(11), zero_matrix(11)]
    tail_bounds = [zero_matrix(11), zero_matrix(11)]
    for i, node in enumerate(nodes):
        limits[0][i][i] += alpha[i]
        limits[1][i][i] += alpha[i] * (1 - node * node)
    boundary_terms = 0
    for i, j, coefficient, area, displacement, delta in ordered_orbits:
        if delta == 0:
            boundary_terms += 1
            limits[0][i][j] += coefficient
            limits[1][i][j] += coefficient * displacement
        else:
            tail_bounds[0][i][j] += coefficient * ceil_sqrt_fraction(
                area / delta
            )
            tail_bounds[1][i][j] += coefficient * ceil_sqrt_fraction(
                area * area / delta
            )
    assert boundary_terms == 4
    tail_constants = []
    for parity in (0, 1):
        assert symmetric(limits[parity])
        assert symmetric(tail_bounds[parity])
        pivots = ldl_pivots(limits[parity])
        assert all(pivot > 0 for pivot in pivots)
        limit_inverse = inverse(limits[parity])
        tail_row_sums = [sum(row) for row in tail_bounds[parity]]
        constant = max(
            sum(
                abs(limit_inverse[i][h]) * tail_row_sums[h]
                for h in range(11)
            )
            for i in range(11)
        )
        tail_constants.append(constant)
    assert tail_constants[0] < 141
    assert tail_constants[1] < 186
    # For k>=187, the entrywise remainder and the infinity-norm Neumann
    # criterion give ||L^{-1}(W_k-L)||_infinity < 1.  Thus W_k is positive
    # definite.  Together with the finite loop this covers every k>=1.

    # All Cohn--de Laat--Leijenhorst style two-point frame matrices using
    # harmonic degrees 0,1,2,3 and total feature rank below 41.
    dimensions = (1, 5, 14, 30)
    polynomial_values = [
        gegenbauer_5_sequence(node, 3) for node in nodes
    ]
    frame_subsets = []
    for mask in range(1, 1 << 4):
        degrees = tuple(i for i in range(4) if mask & (1 << i))
        rank = sum(dimensions[i] for i in degrees)
        if rank >= 41:
            continue
        matrix = [
            [
                1
                + sum(
                    alpha[index]
                    * polynomial_values[index][first]
                    * polynomial_values[index][second]
                    for index in range(11)
                )
                - Q(41, rank)
                for second in degrees
            ]
            for first in degrees
        ]
        for size in range(1, len(matrix) + 1):
            for subset in itertools.combinations(range(len(matrix)), size):
                minor = determinant(
                    [[matrix[i][j] for j in subset] for i in subset]
                )
                assert minor >= 0
        frame_subsets.append(degrees)
    assert len(frame_subsets) == 11

    # Twenty-seven exact centered-skew harmonic trace/rank inequalities.
    minimum_positive_rank_residual: tuple[Q, str] | None = None
    zero_rank_residuals = []
    h_two_centered_third = None
    for name, weights in rank_kernel_specs():
        rank = sum(harmonic_dimension(degree) for degree, _ in weights)
        diagonal = sum(coefficient for _degree, coefficient in weights)
        values = [
            sum(
                coefficient * polynomial_values[index][degree]
                for degree, coefficient in weights
            )
            for index in range(11)
        ]
        trace_one_kernel = Q(41) * diagonal
        pair_square = sum(
            mass * value * value for mass, value in zip(alpha, values)
        )
        trace_two_kernel = (
            Q(41) * diagonal**2 + Q(41) * pair_square
        )
        trace_three_kernel = (
            Q(41) * diagonal**3
            + Q(123) * diagonal * pair_square
            + Q(41)
            * sum(
                mass * values[i] * values[j] * values[k]
                for mass, (i, j, k) in zip(nu, triples)
            )
        )
        variance = (
            trace_two_kernel - trace_one_kernel**2 / rank
        )
        centered_third = (
            trace_three_kernel
            - 3 * trace_one_kernel * trace_two_kernel / rank
            + 2 * trace_one_kernel**3 / rank**2
        )
        residual = (
            (rank - 2) ** 2 * variance**3
            - rank * (rank - 1) * centered_third**2
        )
        assert variance >= 0 and residual >= 0
        if name == "H2":
            h_two_centered_third = centered_third
        if residual == 0:
            zero_rank_residuals.append(name)
        else:
            candidate = (residual, name)
            if (
                minimum_positive_rank_residual is None
                or candidate[0] < minimum_positive_rank_residual[0]
            ):
                minimum_positive_rank_residual = candidate
    assert h_two_centered_third == Q(17, 50)
    assert zero_rank_residuals == [
        "H1",
        "H0+5H1",
        "H0-5H1",
        "H0+H1",
        "H0-H1",
    ]
    assert minimum_positive_rank_residual is not None

    # Adversarial scope audit: this pseudodistribution does not satisfy the
    # corrected exact-stratum common-pair capacity hierarchy.  Record the
    # four failures exactly rather than silently claiming the stronger
    # relaxation.
    nonpositive = tuple(
        index for index, node in enumerate(nodes) if node <= 0
    )
    positive = tuple(
        index for index, node in enumerate(nodes) if node > 0
    )
    capacity_rows = []
    for lower in range(len(nonpositive)):
        for upper in range(lower, len(nonpositive)):
            base_indices = nonpositive[lower : upper + 1]
            base_set = set(base_indices)
            base_upper = nodes[base_indices[-1]]
            for high_index in positive:
                high = nodes[high_index]
                capacity = common_pair_capacity(
                    2 * high * high / (1 + base_upper)
                )
                if capacity is None:
                    continue
                left = sum(
                    mass
                    * sum(
                        triple[position] in base_set
                        and all(
                            nodes[triple[other]] >= high
                            for other in range(3)
                            if other != position
                        )
                        for position in range(3)
                    )
                    for triple, mass in zip(triples, nu)
                )
                right = (
                    3
                    * capacity
                    * sum(alpha[index] for index in base_indices)
                )
                capacity_rows.append(
                    (
                        right - left,
                        nodes[base_indices[0]],
                        base_upper,
                        high,
                        capacity,
                    )
                )
    assert len(capacity_rows) == 48
    failed_capacity_rows = [
        row for row in capacity_rows if row[0] < 0
    ]
    assert [
        (lower, upper, high, capacity)
        for _slack, lower, upper, high, capacity
        in failed_capacity_rows
    ] == [
        (Q(-1, 2), Q(-7, 20), Q(1, 2), 1),
        (Q(-7, 20), Q(-7, 20), Q(1, 2), 1),
        (Q(-7, 20), Q(-3, 10), Q(1, 2), 2),
        (Q(-3, 10), Q(-3, 10), Q(1, 2), 2),
    ]

    weighted_capacity_rows = []
    for high_index in positive:
        high = nodes[high_index]
        capacities: dict[int, int] = {}
        for base_index, base in enumerate(nodes):
            if base <= 0:
                capacity = common_pair_capacity(
                    2 * high * high / (1 + base)
                )
                if capacity is None:
                    continue
            elif high == Q(1, 2):
                capacity = 7
            else:
                continue
            capacities[base_index] = capacity
        left = sum(
            mass
            * sum(
                triple[position] in capacities
                and all(
                    nodes[triple[other]] >= high
                    for other in range(3)
                    if other != position
                )
                for position in range(3)
            )
            for triple, mass in zip(triples, nu)
        )
        right = 3 * sum(
            capacity * alpha[index]
            for index, capacity in capacities.items()
        )
        weighted_capacity_rows.append((right - left, high))
    assert len(weighted_capacity_rows) == 2
    assert all(slack >= 0 for slack, _high in weighted_capacity_rows)

    return {
        "status": "PASS",
        "scope": (
            "exact centered/tight pair-triple relaxation witness; "
            "not a Gram matrix or code"
        ),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "support_nodes": len(nodes),
        "positive_triple_orbits": len(nu),
        "pair_first_moment": str(pair_first),
        "pair_second_moment": str(pair_second),
        "triple_cycle_moment": str(triple_cycle),
        "w0_rank": 9,
        "w1_rank": 9,
        "w2_rank": 10,
        "finite_bv_check": f"1..{finite_through}",
        "analytic_bv_tail": "k>=187",
        "minimum_finite_ldl_pivot": str(minimum_finite_pivot[0]),
        "minimum_finite_ldl_pivot_degree": minimum_finite_pivot[1],
        "even_tail_constant": str(tail_constants[0]),
        "odd_tail_constant": str(tail_constants[1]),
        "ordinary_pair_exact_check": "0..89",
        "ordinary_pair_analytic_tail": "k>=90",
        "minimum_positive_pair_moment": str(min(pair_moments[3:])),
        "frame_subsets_checked": len(frame_subsets),
        "sharp_harmonic_rank_cuts_checked": len(rank_kernel_specs()),
        "zero_rank_cut_residuals": zero_rank_residuals,
        "minimum_positive_rank_cut_residual": str(
            minimum_positive_rank_residual[0]
        ),
        "minimum_positive_rank_cut_kernel": (
            minimum_positive_rank_residual[1]
        ),
        "stratified_capacity_rows_audited": len(capacity_rows),
        "stratified_capacity_failures": len(failed_capacity_rows),
        "minimum_stratified_capacity_slack": str(
            min(row[0] for row in capacity_rows)
        ),
        "weighted_capacity_rows_audited": len(weighted_capacity_rows),
        "minimum_weighted_capacity_slack": str(
            min(row[0] for row in weighted_capacity_rows)
        ),
    }


def main() -> None:
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
