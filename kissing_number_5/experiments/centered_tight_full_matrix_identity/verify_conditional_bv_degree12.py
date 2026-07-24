#!/usr/bin/env python3
"""Exact verifier for a degree-12 conditional/BV pseudodistribution.

The input stores rounded values for 246 triple-orbit weights and identifies
40 pivot weights.  This verifier leaves the nonpivot weights at their stored
rational values and solves exactly for the pivots from 40 conditional moment
equations.  It then checks every conditional equation, every capacity row,
and the full-radial Bachoc--Vallentin blocks through degree 12.

Only Python's standard library and ``fractions.Fraction`` are used.  The
verified object is a pair/triple pseudodistribution, not a labeled matrix or
a spherical code.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
RATIONALIZATION = HERE / "conditional_bv_degree12_rationalization.json"
PAIR_SOURCE = (
    HERE.parent
    / "centered_tight_frame_endpoint"
    / "centered_tight_bv_pseudodistribution.json"
)


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


def principal(
    matrix: list[list[Q]], indices: list[int] | tuple[int, ...]
) -> list[list[Q]]:
    return [[matrix[i][j] for j in indices] for i in indices]


def solve_square(
    matrix: list[list[Q]], right_hand_side: list[Q]
) -> list[Q]:
    """Solve a nonsingular rational square system by Gauss--Jordan."""

    size = len(matrix)
    assert size == len(right_hand_side)
    assert all(len(row) == size for row in matrix)
    work = [
        row[:] + [right_hand_side[index]]
        for index, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if work[row][column] != 0
            ),
            None,
        )
        assert pivot is not None
        work[column], work[pivot] = work[pivot], work[column]
        pivot_value = work[column][column]
        work[column] = [
            value / pivot_value for value in work[column]
        ]
        for row in range(size):
            if row == column:
                continue
            multiplier = work[row][column]
            if multiplier:
                work[row] = [
                    value - multiplier * pivot_entry
                    for value, pivot_entry in zip(
                        work[row], work[column]
                    )
                ]
    return [row[-1] for row in work]


def ldl_pivots(matrix: list[list[Q]]) -> list[Q]:
    """Return the exact unpivoted LDL^T pivots."""

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
    """Exact determinant by rational Gaussian elimination."""

    size = len(matrix)
    assert all(len(row) == size for row in matrix)
    work = [row[:] for row in matrix]
    answer = Q(1)
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
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
        for row in range(column + 1, size):
            multiplier = work[row][column] / pivot_value
            for entry in range(column + 1, size):
                work[row][entry] -= (
                    multiplier * work[column][entry]
                )
    return answer


def normalized_transverse_sequences(
    area: Q, displacement: Q, maximum_index: int
) -> tuple[list[Q], list[Q]]:
    """Parity-normalized dimension-four transverse Gegenbauer kernels.

    If ``z=displacement/sqrt(area)``, the even entries are
    ``P_(2m)^(4)(z)`` and the odd entries are
    ``sqrt(area) P_(2m+1)^(4)(z)``.
    """

    assert area > 0
    transformed = 4 * displacement * displacement / area - 2
    even = [
        Q(1),
        (4 * displacement * displacement / area - 1) / 3,
    ]
    odd = [
        displacement,
        2 * displacement**3 / area - displacement,
    ]
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


def conditional_rows(
    nodes: list[Q],
    triples: list[tuple[int, int, int]],
    alpha: list[Q],
) -> list[tuple[list[Q], Q, str]]:
    """The total row and four type-conditional rows for each base node."""

    rows = [([Q(1)] * len(triples), Q(1560), "total")]
    for base_index, base in enumerate(nodes):
        coefficients: list[list[Q]] = [[], [], [], []]
        for triple in triples:
            values = tuple(nodes[index] for index in triple)
            orbit = sorted(set(itertools.permutations(values)))
            accumulators = [Q(0)] * 4
            for u, v, t in orbit:
                if t == base:
                    accumulators[0] += 1
                    accumulators[1] += u
                    accumulators[2] += u * u
                    accumulators[3] += u * v
            for row, value in zip(coefficients, accumulators):
                row.append(value / len(orbit))
        targets = (
            39 * alpha[base_index],
            alpha[base_index] * (-1 - base),
            alpha[base_index] * (Q(36, 5) - base * base),
            alpha[base_index] * Q(31, 5) * base,
        )
        for name, row, target in zip(
            ("mass", "first", "square", "cross"),
            coefficients,
            targets,
        ):
            rows.append((row, target, f"{base_index}:{name}"))
    return rows


def reconstruct_weights(
    rows: list[tuple[list[Q], Q, str]],
    record: dict[str, object],
) -> tuple[list[Q], Q]:
    """Reconstruct all orbit weights from exact free and pivot data."""

    denominator = int(record["round_denominator"])
    numerators = [int(value) for value in record["rounded_numerators"]]
    pivots = [int(value) for value in record["pivot_columns"]]
    independent_rows = [
        int(value) for value in record["independent_rows"]
    ]
    assert denominator > 0
    assert len(numerators) == len(rows[0][0]) == 246
    assert len(pivots) == len(set(pivots)) == 40
    assert len(independent_rows) == len(set(independent_rows)) == 40
    assert all(0 <= column < len(numerators) for column in pivots)
    assert all(0 <= row < len(rows) for row in independent_rows)

    rounded = [Q(numerator, denominator) for numerator in numerators]
    weights = rounded[:]
    pivot_set = set(pivots)
    free_columns = [
        column
        for column in range(len(weights))
        if column not in pivot_set
    ]
    matrix = [
        [rows[row][0][column] for column in pivots]
        for row in independent_rows
    ]
    right_hand_side = [
        rows[row][1]
        - sum(
            rows[row][0][column] * weights[column]
            for column in free_columns
        )
        for row in independent_rows
    ]
    solved = solve_square(matrix, right_hand_side)
    for column, value in zip(pivots, solved):
        weights[column] = value

    assert all(
        sum(coefficient * weight for coefficient, weight in zip(row, weights))
        == target
        for row, target, _name in rows
    )
    assert all(weight > 0 for weight in weights)
    maximum_correction = max(
        abs(weights[column] - rounded[column]) for column in pivots
    )
    return weights, maximum_correction


def common_pair_capacity(projected: Q) -> int | None:
    """Exact endpoint convention for the projected S^2 cap rows."""

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


def capacity_slacks(
    nodes: list[Q],
    alpha: list[Q],
    triples: list[tuple[int, int, int]],
    weights: list[Q],
) -> tuple[list[Q], list[Q], list[Q]]:
    """Evaluate the 48 stratified rows and two weighted rows exactly."""

    nonpositive = tuple(
        index for index, node in enumerate(nodes) if node <= 0
    )
    positive = tuple(
        index for index, node in enumerate(nodes) if node > 0
    )
    stratified: list[Q] = []
    stratified_positive_bound: list[Q] = []
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
                    weight
                    * sum(
                        triple[position] in base_set
                        and all(
                            nodes[triple[other]] >= high
                            for other in range(3)
                            if other != position
                        )
                        for position in range(3)
                    )
                    for triple, weight in zip(triples, weights)
                )
                right = (
                    3
                    * capacity
                    * sum(alpha[index] for index in base_indices)
                )
                slack = right - left
                assert slack >= 0
                stratified.append(slack)
                if right > 0:
                    stratified_positive_bound.append(slack)
    assert len(stratified) == 48

    weighted: list[Q] = []
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
            weight
            * sum(
                triple[position] in capacities
                and all(
                    nodes[triple[other]] >= high
                    for other in range(3)
                    if other != position
                )
                for position in range(3)
            )
            for triple, weight in zip(triples, weights)
        )
        right = 3 * sum(
            capacity * alpha[index]
            for index, capacity in capacities.items()
        )
        slack = right - left
        assert slack >= 0
        weighted.append(slack)
    assert len(weighted) == 2
    return stratified, stratified_positive_bound, weighted


def verify(
    rationalization_path: Path = RATIONALIZATION,
    pair_source_path: Path = PAIR_SOURCE,
) -> dict[str, object]:
    source_bytes = pair_source_path.read_bytes()
    source = json.loads(source_bytes)
    record_bytes = rationalization_path.read_bytes()
    record = json.loads(record_bytes)

    assert record["schema"] == (
        "centered-tight-conditional-bv-degree12-rationalization-v1"
    )
    assert record["status"] == (
        "EXACT RATIONAL RECONSTRUCTION DATA; VERIFIER DETERMINES CLAIMS"
    )
    assert record["source_pair_certificate"] == pair_source_path.name
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    assert record["source_pair_sha256"] == source_hash
    assert record["maximum_bv_degree"] == 12

    nodes = [Q(value) for value in source["nodes"]]
    alpha = [Q(value) for value in source["alpha"]]
    triples = [tuple(item) for item in source["triple_orbits"]]
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
    assert sum(alpha) == 40
    feasible = []
    for triple in itertools.combinations_with_replacement(
        range(len(nodes)), 3
    ):
        u, v, t = (nodes[index] for index in triple)
        if 1 + 2 * u * v * t - u * u - v * v - t * t >= 0:
            feasible.append(triple)
    assert triples == feasible
    assert len(triples) == 246

    rows = conditional_rows(nodes, triples, alpha)
    assert len(rows) == 45
    weights, maximum_correction = reconstruct_weights(rows, record)
    assert sum(weights) == 1560

    # Exact pair and triple moments forced by the conditional equations.
    assert sum(weight * node for weight, node in zip(alpha, nodes)) == -1
    assert sum(
        weight * node * node for weight, node in zip(alpha, nodes)
    ) == Q(36, 5)
    triple_cycle = sum(
        weight * nodes[i] * nodes[j] * nodes[k]
        for weight, (i, j, k) in zip(weights, triples)
    )
    assert triple_cycle == Q(1116, 25)

    negative_mass = sum(
        weight
        for weight, node in zip(alpha, nodes)
        if node < Q(-1, 300)
    )
    positive_mass = sum(
        weight
        for weight, node in zip(alpha, nodes)
        if node > Q(1, 300)
    )
    assert negative_mass >= 7
    assert positive_mass >= 7
    stratified, positive_bound_slacks, weighted = capacity_slacks(
        nodes, alpha, triples, weights
    )

    # Build the full k=0 block and the coefficient matrices for k>=1.
    full_zero = zero_matrix(12)
    node_zero = zero_matrix(11)
    for index, weight in enumerate(alpha):
        node_zero[index][index] += weight
        full_zero[index][-1] = weight
        full_zero[-1][index] = weight
    full_zero[-1][-1] = 1
    coefficient_matrices: dict[
        tuple[Q, Q], list[list[Q]]
    ] = {}
    index_of = {node: index for index, node in enumerate(nodes)}
    for triple, weight in zip(triples, weights):
        values = tuple(nodes[index] for index in triple)
        orbit = sorted(set(itertools.permutations(values)))
        coefficient = weight / len(orbit)
        for u, v, t in orbit:
            i, j = index_of[u], index_of[v]
            node_zero[i][j] += coefficient
            area = (1 - u * u) * (1 - v * v)
            displacement = t - u * v
            assert area > 0
            assert area - displacement * displacement >= 0
            coefficient_matrix = coefficient_matrices.setdefault(
                (area, displacement), zero_matrix(11)
            )
            coefficient_matrix[i][j] += coefficient
    assert symmetric(node_zero)
    assert all(
        symmetric(matrix) for matrix in coefficient_matrices.values()
    )
    for i in range(11):
        for j in range(11):
            full_zero[i][j] = node_zero[i][j]
    assert symmetric(full_zero)
    assert matrix_vector(node_zero, [Q(1)] * 11) == [
        40 * weight for weight in alpha
    ]

    fixed_size_kernel = [Q(-1, 40)] * 11 + [Q(1)]
    centered_kernel = nodes + [Q(1)]
    tight_kernel = [
        node * node - Q(1, 5) for node in nodes
    ] + [Q(4, 5)]
    zero_kernels = (
        fixed_size_kernel,
        centered_kernel,
        tight_kernel,
    )
    for kernel in zero_kernels:
        assert matrix_vector(full_zero, kernel) == [Q(0)] * 12
    assert determinant(
        [
            [kernel[index] for kernel in zero_kernels]
            for index in (0, 1, 11)
        ]
    ) != 0

    # Three independent kernels give rank at most nine.  A positive
    # 9-by-9 principal block gives rank at least nine and nine positive
    # eigenvalues, proving the full 12-by-12 block is PSD.
    zero_complement = list(range(3, 12))
    zero_pivots = ldl_pivots(principal(full_zero, zero_complement))
    assert all(pivot > 0 for pivot in zero_pivots)
    minimum_pivot = (min(zero_pivots), 0)

    maximum_checked = int(record["maximum_bv_degree"])
    sequences = {
        key: normalized_transverse_sequences(
            *key, (maximum_checked + 1) // 2
        )
        for key in coefficient_matrices
    }
    degree_blocks: dict[int, list[list[Q]]] = {}
    for degree in range(1, maximum_checked + 2):
        matrix = zero_matrix(11)
        for i, node in enumerate(nodes):
            matrix[i][i] = alpha[i]
            if degree % 2:
                matrix[i][i] *= 1 - node * node
        parity = degree % 2
        sequence_index = degree // 2
        for key, coefficient_matrix in coefficient_matrices.items():
            kernel_value = sequences[key][parity][sequence_index]
            for i in range(11):
                for j in range(11):
                    matrix[i][j] += (
                        coefficient_matrix[i][j] * kernel_value
                    )
        assert symmetric(matrix)
        degree_blocks[degree] = matrix

        if degree > maximum_checked:
            continue
        if degree == 1:
            first_kernel = [Q(1)] * 11
            second_kernel = nodes
            assert matrix_vector(matrix, first_kernel) == [Q(0)] * 11
            assert matrix_vector(matrix, second_kernel) == [Q(0)] * 11
            assert nodes[0] != nodes[1]
            complement = list(range(2, 11))
        elif degree == 2:
            kernel = [1 - node * node for node in nodes]
            assert matrix_vector(matrix, kernel) == [Q(0)] * 11
            assert kernel[0] != 0
            complement = list(range(1, 11))
        else:
            complement = list(range(11))
        pivots = ldl_pivots(principal(matrix, complement))
        assert all(pivot > 0 for pivot in pivots)
        candidate = (min(pivots), degree)
        if candidate[0] < minimum_pivot[0]:
            minimum_pivot = candidate

    # This particular exact witness does not pass the next block.  A
    # negative order-three principal minor is a strict, exact failure.
    degree_thirteen_indices = (2, 7, 10)
    degree_thirteen_minor = determinant(
        principal(
            degree_blocks[maximum_checked + 1],
            degree_thirteen_indices,
        )
    )
    assert degree_thirteen_minor < 0

    return {
        "status": "PASS",
        "scope": (
            "exact conditional/capacity/full-radial BV relaxation "
            "through degree 12; not a labeled matrix or code"
        ),
        "source_pair_sha256": source_hash,
        "rationalization_sha256": hashlib.sha256(
            record_bytes
        ).hexdigest(),
        "positive_triple_orbits": len(weights),
        "conditional_rows_checked": len(rows),
        "conditional_base_types_checked": len(nodes),
        "maximum_pivot_correction": str(maximum_correction),
        "triple_cycle_moment": str(triple_cycle),
        "robust_negative_pair_mass": str(negative_mass),
        "robust_positive_pair_mass": str(positive_mass),
        "stratified_capacity_rows": len(stratified),
        "minimum_positive_bound_stratified_slack": str(
            min(positive_bound_slacks)
        ),
        "weighted_capacity_rows": len(weighted),
        "minimum_weighted_capacity_slack": str(min(weighted)),
        "maximum_bv_degree_verified": maximum_checked,
        "minimum_bv_ldl_pivot": str(minimum_pivot[0]),
        "minimum_bv_ldl_pivot_degree": minimum_pivot[1],
        "degree_13_negative_principal_indices": list(
            degree_thirteen_indices
        ),
        "degree_13_negative_principal_minor": str(
            degree_thirteen_minor
        ),
        "conclusion": (
            "the type-conditional relaxation remains feasible after "
            "capacities and full-radial BV positivity through degree 12"
        ),
    }


def main() -> None:
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
