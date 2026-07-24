#!/usr/bin/env python3
"""Exact verifier for the centered quarter-grid all-harmonic BV barrier.

Only the Python standard library is used.  The object verified here is a
pair/triple pseudodistribution, not a Gram matrix or spherical code.
"""

from __future__ import annotations

from fractions import Fraction as Q
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path


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


def inverse(matrix: list[list[Q]]) -> list[list[Q]]:
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


def rank_kernel_specs() -> tuple[tuple[str, tuple[tuple[int, Q], ...]], ...]:
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


def verify(source_path: Path, tail_path: Path) -> dict[str, object]:
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    tail = json.loads(tail_path.read_text())
    assert source["schema"] == (
        "kissing5.centered_quarter_bv_pseudodistribution.v1"
    )
    assert tail["schema"] == (
        "kissing5.centered_quarter_bv_all_harmonics.v1"
    )
    assert tail["source_certificate"] == source_path.name
    assert tail["source_sha256"] == hashlib.sha256(source_bytes).hexdigest()
    assert source["dimension"] == 5 and source["cardinality"] == 41
    assert Q(source["maximum_inner_product"]) == Q(1, 2)

    grid = [Q(value) for value in source["grid"]]
    alpha = [Q(value) for value in source["alpha"]]
    triples = [tuple(item) for item in source["triple_orbits"]]
    nu = [Q(value) for value in source["nu"]]
    assert grid == [
        Q(-1),
        Q(-3, 4),
        Q(-1, 2),
        Q(-1, 4),
        Q(0),
        Q(1, 4),
        Q(1, 2),
    ]
    assert all(value > 0 for value in alpha + nu)
    assert sum(alpha) == 40 and sum(nu) == 40 * 39
    assert 1 + sum(weight * node for weight, node in zip(alpha, grid)) == 0

    feasible = []
    for triple in itertools.combinations_with_replacement(range(7), 3):
        u, v, t = (grid[index] for index in triple)
        if 1 + 2 * u * v * t - u * u - v * v - t * t >= 0:
            feasible.append(triple)
    assert triples == feasible
    for index in range(7):
        marginal = sum(
            weight * Q(triple.count(index), 3)
            for triple, weight in zip(triples, nu)
        )
        assert marginal == 39 * alpha[index]

    negative_mass = sum(
        weight
        for node, weight in zip(grid, alpha)
        if node < Q(-1, 300)
    )
    positive_mass = sum(
        weight
        for node, weight in zip(grid, alpha)
        if node > Q(1, 300)
    )
    assert negative_mass > 7 and positive_mass > 6

    capacity_slacks: list[Q] = []
    nonpositive_indices = tuple(
        index for index, node in enumerate(grid) if node <= 0
    )
    positive_indices = tuple(
        index for index, node in enumerate(grid) if node > 0
    )
    for lower in range(len(nonpositive_indices)):
        for upper in range(lower, len(nonpositive_indices)):
            base_indices = nonpositive_indices[lower : upper + 1]
            base_set = set(base_indices)
            base_upper = grid[base_indices[-1]]
            for high_index in positive_indices:
                high = grid[high_index]
                if base_upper == -1:
                    capacity = 0
                else:
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
                            grid[triple[other]] >= high
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
                assert left <= right
                capacity_slacks.append(right - left)

    weighted_capacity_slacks: list[Q] = []
    for high_index in positive_indices:
        high = grid[high_index]
        capacities: dict[int, int] = {}
        for base_index, base in enumerate(grid):
            if base == -1:
                capacity = 0
            elif base <= 0:
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
                    grid[triple[other]] >= high
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
        assert left <= right
        weighted_capacity_slacks.append(right - left)
    assert len(capacity_slacks) == 18
    assert len(weighted_capacity_slacks) == 2

    extended_grid = grid + [Q(1)]
    w_zero = zero_matrix(8)
    w_zero[-1][-1] = 1
    for index, weight in enumerate(alpha):
        w_zero[index][index] += weight
        w_zero[index][-1] += weight
        w_zero[-1][index] += weight
    for triple, weight in zip(triples, nu):
        values = tuple(grid[index] for index in triple)
        orbit = sorted(set(itertools.permutations(values)))
        for u, v, _t in orbit:
            w_zero[extended_grid.index(u)][extended_grid.index(v)] += (
                weight / len(orbit)
            )
    assert symmetric(w_zero)
    fixed_size_kernel = [Q(-1, 40)] * 7 + [Q(1)]
    centered_kernel = grid + [Q(1)]
    assert matrix_vector(w_zero, fixed_size_kernel) == [Q(0)] * 8
    assert matrix_vector(w_zero, centered_kernel) == [Q(0)] * 8
    assert fixed_size_kernel != centered_kernel
    w_zero_reduced = [row[:6] for row in w_zero[:6]]
    w_zero_pivots = ldl_pivots(w_zero_reduced)
    assert all(pivot > 0 for pivot in w_zero_pivots)

    active_grid = grid[1:]
    active_index = {value: index for index, value in enumerate(active_grid)}
    coefficient_matrices: dict[tuple[Q, Q], list[list[Q]]] = {}
    ordered_terms: list[tuple[int, int, Q, Q, Q, Q]] = []
    for triple, weight in zip(triples, nu):
        values = tuple(grid[index] for index in triple)
        orbit = sorted(set(itertools.permutations(values)))
        coefficient = weight / len(orbit)
        for u, v, t in orbit:
            if u not in active_index or v not in active_index:
                continue
            i, j = active_index[u], active_index[v]
            area = (1 - u * u) * (1 - v * v)
            displacement = t - u * v
            delta = area - displacement * displacement
            assert area > 0 and delta >= 0
            matrix = coefficient_matrices.setdefault(
                (area, displacement), zero_matrix(6)
            )
            matrix[i][j] += coefficient
            ordered_terms.append(
                (i, j, coefficient, area, displacement, delta)
            )
    assert all(symmetric(matrix) for matrix in coefficient_matrices.values())

    finite_through = tail["finite_harmonic_check_through"]
    analytic_from = tail["analytic_harmonic_tail_from"]
    assert finite_through >= 1 and analytic_from == finite_through + 1
    maximum_index = finite_through // 2 + 1
    sequences = {
        key: normalized_transverse_sequences(*key, maximum_index)
        for key in coefficient_matrices
    }
    minimum_pivot: tuple[Q, int, int] | None = None
    w_one_rank = None
    for degree in range(1, finite_through + 1):
        parity = degree % 2
        sequence_index = degree // 2
        matrix = zero_matrix(6)
        for i, q in enumerate(active_grid):
            matrix[i][i] = alpha[i + 1]
            if parity:
                matrix[i][i] *= 1 - q * q
        for key, coefficient_matrix in coefficient_matrices.items():
            kernel_value = sequences[key][parity][sequence_index]
            for i in range(6):
                for j in range(6):
                    matrix[i][j] += (
                        coefficient_matrix[i][j] * kernel_value
                    )
        assert symmetric(matrix)
        if degree == 1:
            assert matrix_vector(matrix, [Q(1)] * 6) == [Q(0)] * 6
            reduced = [row[:5] for row in matrix[:5]]
            pivots = ldl_pivots(reduced)
            assert all(pivot > 0 for pivot in pivots)
            w_one_rank = 5
        else:
            pivots = ldl_pivots(matrix)
            assert all(pivot > 0 for pivot in pivots)
        for index, pivot in enumerate(pivots):
            candidate = (pivot, degree, index)
            if minimum_pivot is None or candidate[0] < minimum_pivot[0]:
                minimum_pivot = candidate
    assert minimum_pivot is not None and w_one_rank == 5

    limits = [zero_matrix(6), zero_matrix(6)]
    tail_bounds = [zero_matrix(6), zero_matrix(6)]
    for i, q in enumerate(active_grid):
        limits[0][i][i] += alpha[i + 1]
        limits[1][i][i] += alpha[i + 1] * (1 - q * q)
    for i, j, coefficient, area, displacement, delta in ordered_terms:
        if delta == 0:
            limits[0][i][j] += coefficient
            limits[1][i][j] += coefficient * displacement
        else:
            tail_bounds[0][i][j] += coefficient * ceil_sqrt_fraction(
                area / delta
            )
            tail_bounds[1][i][j] += coefficient * ceil_sqrt_fraction(
                area * area / delta
            )

    tail_constants = []
    for parity in (0, 1):
        pivots = ldl_pivots(limits[parity])
        assert all(pivot > 0 for pivot in pivots)
        limit_inverse = inverse(limits[parity])
        row_bounds = [sum(row) for row in tail_bounds[parity]]
        constant = max(
            sum(
                abs(limit_inverse[i][h]) * row_bounds[h]
                for h in range(6)
            )
            for i in range(6)
        )
        assert constant < analytic_from
        tail_constants.append(constant)

    pair_finite = tail["pair_finite_check_through"]
    pair_tail_from = tail["pair_analytic_tail_from"]
    assert pair_finite >= 1 and pair_tail_from == pair_finite + 1
    pair_sequences = [
        gegenbauer_5_sequence(node, pair_finite) for node in grid
    ]
    minimum_pair: tuple[Q, int] | None = None
    for degree in range(1, pair_finite + 1):
        moment = 1 + sum(
            alpha[index] * pair_sequences[index][degree]
            for index in range(7)
        )
        if degree == 1:
            assert moment == 0
        else:
            assert moment > 0
            candidate = (moment, degree)
            if minimum_pair is None or candidate[0] < minimum_pair[0]:
                minimum_pair = candidate
    assert minimum_pair is not None

    inverse_bounds = [
        Q(value)
        for value in tail["pair_interior_inverse_three_halves_bounds"]
    ]
    assert len(inverse_bounds) == 6
    for node, upper in zip(active_grid, inverse_bounds):
        q = 1 - node * node
        assert upper > 0 and upper**2 * q**3 >= 1
    weighted_pair_bound = sum(
        alpha[index + 1] * inverse_bounds[index]
        for index in range(6)
    )
    endpoint_margin = 1 - alpha[0]
    assert endpoint_margin > 0
    assert Q(44, 7) < Q(251, 100) ** 2
    analytic_constant = Q(22, 7) ** 2 * Q(251, 100) / 4
    assert analytic_constant < Q(31, 5)
    normalized_pair_tail = (
        Q(31, 5) * weighted_pair_bound / endpoint_margin
    )
    assert normalized_pair_tail**2 < pair_tail_from**3

    gegenbauer_values = {
        node: gegenbauer_5_sequence(node, 3) for node in grid
    }
    minimum_rank_residual: tuple[Q, str] | None = None
    for name, weights in rank_kernel_specs():
        rank = sum(harmonic_dimension(degree) for degree, _ in weights)
        diagonal = sum(coefficient for _degree, coefficient in weights)
        values = [
            sum(
                coefficient * gegenbauer_values[node][degree]
                for degree, coefficient in weights
            )
            for node in grid
        ]
        trace_one = Q(41) * diagonal
        pair_square = sum(
            mass * value * value for mass, value in zip(alpha, values)
        )
        trace_two = Q(41) * diagonal**2 + Q(41) * pair_square
        trace_three = (
            Q(41) * diagonal**3
            + Q(123) * diagonal * pair_square
            + Q(41)
            * sum(
                mass * values[i] * values[j] * values[k]
                for mass, (i, j, k) in zip(nu, triples)
            )
        )
        variance = trace_two - trace_one**2 / rank
        centered_third = (
            trace_three
            - 3 * trace_one * trace_two / rank
            + 2 * trace_one**3 / rank**2
        )
        residual = (
            (rank - 2) ** 2 * variance**3
            - rank * (rank - 1) * centered_third**2
        )
        assert variance >= 0 and residual > 0
        candidate = (residual, name)
        if (
            minimum_rank_residual is None
            or candidate[0] < minimum_rank_residual[0]
        ):
            minimum_rank_residual = candidate
    assert minimum_rank_residual is not None

    return {
        "status": "PASS",
        "scope": "exact pair/triple relaxation witness; not a code",
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "w0_rank": 6,
        "w1_rank": 5,
        "finite_harmonic_check": f"1..{finite_through}",
        "analytic_harmonic_tail": f"k>={analytic_from}",
        "minimum_finite_ldl_pivot": str(minimum_pivot[0]),
        "minimum_finite_ldl_pivot_degree": minimum_pivot[1],
        "even_tail_constant": str(tail_constants[0]),
        "odd_tail_constant": str(tail_constants[1]),
        "pair_moment_degree_one": "0",
        "minimum_positive_finite_pair_moment": str(minimum_pair[0]),
        "minimum_positive_finite_pair_moment_degree": minimum_pair[1],
        "pair_analytic_tail": f"k>={pair_tail_from}",
        "robust_negative_pair_mass": str(negative_mass),
        "robust_positive_pair_mass": str(positive_mass),
        "stratified_common_pair_rows_checked": len(capacity_slacks),
        "minimum_stratified_common_pair_slack": str(min(capacity_slacks)),
        "weighted_common_pair_rows_checked": len(weighted_capacity_slacks),
        "minimum_weighted_common_pair_slack": str(
            min(weighted_capacity_slacks)
        ),
        "sharp_harmonic_rank_cuts_checked": len(rank_kernel_specs()),
        "minimum_rank_cut_residual": str(minimum_rank_residual[0]),
        "minimum_rank_cut_kernel": minimum_rank_residual[1],
    }


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=(
            root
            / "certificates"
            / "centered_quarter_bv_pseudodistribution.json"
        ),
    )
    parser.add_argument(
        "--tail",
        type=Path,
        default=(
            root
            / "certificates"
            / "centered_quarter_bv_all_harmonics.json"
        ),
    )
    args = parser.parse_args()
    report = verify(
        args.source,
        args.tail,
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
