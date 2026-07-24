#!/usr/bin/env python3
"""Exact verifier for the first interior shadow after excluding X=2.

This verifies the finite centered quarter-grid relaxation used by the
degree-count search with harmonic degree zero and pair degree sixty.  The
verified object is a pair/triple/row pseudomarginal, not a labeled Gram
matrix or a spherical code.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "iteration_exclude_x2.json"
ENDPOINT_VERIFIER_PATH = HERE / "verify_endpoint.py"
SPEC = importlib.util.spec_from_file_location(
    "endpoint_verifier", ENDPOINT_VERIFIER_PATH
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load endpoint verifier")
endpoint = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(endpoint)


class VerificationError(RuntimeError):
    """Raised when an exact interior-shadow check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def gegenbauer_5(value: Q, maximum_degree: int) -> list[Q]:
    result = [Q(1)]
    if maximum_degree:
        result.append(value)
    for degree in range(2, maximum_degree + 1):
        result.append(
            (
                (2 * degree + 1) * value * result[-1]
                - (degree - 1) * result[-2]
            )
            / (degree + 2)
        )
    return result


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


def exact_psd(matrix: list[list[Q]]) -> tuple[int, list[Q]]:
    """Prove PSD by exact symmetric Schur-complement elimination."""

    size = len(matrix)
    require(
        all(len(row) == size for row in matrix),
        "PSD matrix is not square",
    )
    require(
        all(matrix[i][j] == matrix[j][i] for i in range(size) for j in range(size)),
        "PSD matrix is not symmetric",
    )
    work = [row[:] for row in matrix]
    pivots: list[Q] = []
    while work:
        require(
            all(work[index][index] >= 0 for index in range(len(work))),
            "negative diagonal encountered in exact PSD elimination",
        )
        pivot_index = next(
            (
                index
                for index in range(len(work))
                if work[index][index] > 0
            ),
            None,
        )
        if pivot_index is None:
            require(
                all(value == 0 for row in work for value in row),
                "zero diagonal with nonzero off-diagonal entry",
            )
            break
        if pivot_index:
            work[0], work[pivot_index] = work[pivot_index], work[0]
            for row in work:
                row[0], row[pivot_index] = row[pivot_index], row[0]
        pivot = work[0][0]
        pivots.append(pivot)
        work = [
            [
                work[i][j] - work[i][0] * work[0][j] / pivot
                for j in range(1, len(work))
            ]
            for i in range(1, len(work))
        ]
    return len(pivots), pivots


def degree_types() -> list[tuple[int, ...]]:
    """Rebuild exactly the 9,882 row types used by the search."""

    answer = []
    for d0 in range(2):
        for d1 in range(41 - d0):
            for d2 in range(41 - d0 - d1):
                for d3 in range(41 - d0 - d1 - d2):
                    remainder = 40 - d0 - d1 - d2 - d3
                    for d5 in range(remainder + 1):
                        twice_d6 = (
                            -4 + 4 * d0 + 3 * d1 + 2 * d2 + d3 - d5
                        )
                        if twice_d6 < 0 or twice_d6 % 2:
                            continue
                        d6 = twice_d6 // 2
                        d4 = remainder - d5 - d6
                        if d4 < 0:
                            continue
                        degree = (d0, d1, d2, d3, d4, d5, d6)
                        if sum(degree[:4]) < 7 or d5 + d6 < 6:
                            continue
                        if d6 > 15 or d1 > 5:
                            continue
                        if d0 and not (
                            d1 == 0 and d2 == d6 and d3 == d5
                        ):
                            continue
                        answer.append(degree)
    return answer


def capacity_slacks(
    nodes: list[Q],
    orbits: list[tuple[int, int, int]],
    edge_counts: list[int],
    triple_counts: list[int],
) -> tuple[list[int], list[int]]:
    nonpositive = tuple(
        index for index, node in enumerate(nodes) if node <= 0
    )
    positive = tuple(
        index for index, node in enumerate(nodes) if node > 0
    )
    stratified = []
    for lower in range(len(nonpositive)):
        for upper in range(lower, len(nonpositive)):
            base_indices = nonpositive[lower : upper + 1]
            base_set = set(base_indices)
            base_upper = nodes[base_indices[-1]]
            for high_index in positive:
                high = nodes[high_index]
                if base_upper == -1:
                    capacity = 0
                else:
                    capacity = common_pair_capacity(
                        2 * high * high / (1 + base_upper)
                    )
                if capacity is None:
                    continue
                left = sum(
                    count
                    * sum(
                        triple[position] in base_set
                        and all(
                            nodes[triple[other]] >= high
                            for other in range(3)
                            if other != position
                        )
                        for position in range(3)
                    )
                    for triple, count in zip(orbits, triple_counts)
                )
                right = capacity * sum(
                    edge_counts[index] for index in base_indices
                )
                require(left <= right, "stratified capacity violation")
                stratified.append(right - left)

    weighted = []
    for high_index in positive:
        high = nodes[high_index]
        capacities: dict[int, int] = {}
        for base_index, base in enumerate(nodes):
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
            count
            * sum(
                triple[position] in capacities
                and all(
                    nodes[triple[other]] >= high
                    for other in range(3)
                    if other != position
                )
                for position in range(3)
            )
            for triple, count in zip(orbits, triple_counts)
        )
        right = sum(
            capacity * edge_counts[index]
            for index, capacity in capacities.items()
        )
        require(left <= right, "weighted capacity violation")
        weighted.append(right - left)
    return stratified, weighted


def radial_zero_matrix(
    edge_counts: list[int],
    triple_counts: list[int],
    orbits: list[tuple[int, int, int]],
) -> list[list[Q]]:
    alpha = [Q(2 * count, 41) for count in edge_counts]
    nu = [Q(6 * count, 41) for count in triple_counts]
    matrix = [[Q(0) for _ in range(8)] for _ in range(8)]
    matrix[7][7] = 1
    for index, weight in enumerate(alpha):
        matrix[index][index] += weight
        matrix[index][7] += weight
        matrix[7][index] += weight
    for triple, weight in zip(orbits, nu):
        ordered = set(itertools.permutations(triple))
        coefficient = weight / len(ordered)
        for first, second, _third in ordered:
            matrix[first][second] += coefficient
    return matrix


def frame_matrices(
    nodes: list[Q], edge_counts: list[int]
) -> list[tuple[tuple[int, ...], list[list[Q]]]]:
    dimensions = (1, 5, 14, 30)
    subsets = (
        (1,),
        (0, 1),
        (2,),
        (0, 2),
        (1, 2),
        (0, 1, 2),
        (3,),
        (0, 3),
        (1, 3),
        (0, 1, 3),
    )
    values = [gegenbauer_5(node, 3) for node in nodes]
    alpha = [Q(2 * count, 41) for count in edge_counts]
    answer = []
    for subset in subsets:
        rank = sum(dimensions[index] for index in subset)
        constant = 1 - Q(41, rank)
        matrix = [
            [
                constant
                + sum(
                    mass * values[index][first] * values[index][second]
                    for index, mass in enumerate(alpha)
                )
                for second in subset
            ]
            for first in subset
        ]
        answer.append((subset, matrix))
    return answer


def verify(source_path: Path = SOURCE) -> dict[str, object]:
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    require(
        source["schema"]
        == "kissing5.centered_global_degree_count_cutting_plane.v1",
        "wrong source schema",
    )
    require(source["harmonic_degree"] == 0, "wrong harmonic degree")
    require(source["pair_degree"] == 60, "wrong pair degree")
    require(source["excluded_spectral_x"] == [2], "X=2 was not excluded")
    require(
        source["iterations"][0]["status"] == "Optimal",
        "stored discovery status changed",
    )

    colors = list(range(-4, 3))
    nodes = [Q(color, 4) for color in colors]
    orbits = endpoint.feasible_orbits(nodes)
    require(len(orbits) == 51, "wrong triangle orbit count")
    edge_counts = source["final_edge_counts"]
    triple_counts = source["final_triple_counts"]
    require(
        all(isinstance(value, int) and value >= 0 for value in edge_counts),
        "invalid edge counts",
    )
    require(
        all(isinstance(value, int) and value >= 0 for value in triple_counts),
        "invalid triple counts",
    )
    require(sum(edge_counts) == 820, "wrong edge total")
    require(
        sum(color * count for color, count in zip(colors, edge_counts))
        == -82,
        "edge counts violate centering",
    )
    require(edge_counts[0] <= 18, "too many antipodal pairs")
    require(
        edge_counts[0] + edge_counts[1] >= 23,
        "deep-edge lower bound fails",
    )
    require(sum(triple_counts) == 10660, "wrong triple total")
    for index in range(7):
        require(
            sum(
                count * triple.count(index)
                for triple, count in zip(orbits, triple_counts)
            )
            == 39 * edge_counts[index],
            "edge-triple incidence mismatch",
        )

    edge_square_sum = sum(
        color * color * count
        for color, count in zip(colors, edge_counts)
    )
    triangle_product_sum = sum(
        count
        * colors[triple[0]]
        * colors[triple[1]]
        * colors[triple[2]]
        for triple, count in zip(orbits, triple_counts)
    )
    x_value = 5 * edge_square_sum - 11808
    y_value = (
        3636864
        - 2160 * edge_square_sum
        + 75 * triangle_product_sum
    )
    require(
        (edge_square_sum, triangle_product_sum, x_value, y_value)
        == (2364, 19591, 12, -51),
        "wrong interior trace invariants",
    )
    spectral_residual = 9 * x_value**3 - 2 * y_value**2
    require(spectral_residual == 10350 > 0, "spectral point is not interior")
    bound = math.isqrt(9 * x_value**3 // 2)
    residue = (3636864 - 2160 * edge_square_sum) % 75
    congruent_values = [
        value
        for value in range(-bound, bound + 1)
        if value % 75 == residue
    ]
    require(
        congruent_values == [-51, 24],
        "wrong cubic congruence alternatives at X=12",
    )
    require(abs(Q(y_value, 800)) <= 8 * Q(x_value, 40), "outer band fails")

    types = degree_types()
    require(len(types) == 9882, "wrong row-type universe")
    stored_type_counts = source["final_degree_type_counts"]
    require(
        len(stored_type_counts) == len(types)
        and all(
            isinstance(value, int) and value >= 0
            for value in stored_type_counts
        ),
        "invalid full row-type vector",
    )
    active_from_full = {
        degree: count
        for degree, count in zip(types, stored_type_counts)
        if count
    }
    active_from_record = {
        tuple(record["degree"]): record["count"]
        for record in source["iterations"][0]["active_degree_types"]
    }
    require(
        active_from_full == active_from_record,
        "active row list differs from full row vector",
    )
    require(sum(stored_type_counts) == 41, "wrong row count")
    for index in range(7):
        require(
            sum(
                count * degree[index]
                for degree, count in active_from_full.items()
            )
            == 2 * edge_counts[index],
            "row first moment mismatch",
        )
    target_second = endpoint.row_second_moments(
        edge_counts, triple_counts, orbits
    )
    for first in range(7):
        for second in range(first, 7):
            require(
                sum(
                    count * degree[first] * degree[second]
                    for degree, count in active_from_full.items()
                )
                == target_second[first, second],
                "row second moment mismatch",
            )

    pair_sequences = [gegenbauer_5(node, 60) for node in nodes]
    pair_moments = []
    for degree in range(61):
        moment = Q(41) + 2 * sum(
            count * pair_sequences[index][degree]
            for index, count in enumerate(edge_counts)
        )
        require(moment >= 0, f"negative pair moment in degree {degree}")
        pair_moments.append(moment)
    require(pair_moments[1] == 0, "degree-one centering moment is not zero")

    stratified, weighted = capacity_slacks(
        nodes, orbits, edge_counts, triple_counts
    )
    require(
        len(stratified) == 18 and len(weighted) == 2,
        "wrong capacity-row count",
    )

    radial_rank, radial_pivots = exact_psd(
        radial_zero_matrix(edge_counts, triple_counts, orbits)
    )
    require(radial_rank == 6, "degree-zero radial matrix has wrong rank")
    frame_records = []
    for subset, matrix in frame_matrices(nodes, edge_counts):
        rank, pivots = exact_psd(matrix)
        frame_records.append(
            {
                "subset": list(subset),
                "rank": rank,
                "minimum_positive_pivot": (
                    None if not pivots else str(min(pivots))
                ),
            }
        )

    return {
        "status": "exact interior pseudomarginal verified",
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "edge_counts": edge_counts,
        "Q": edge_square_sum,
        "P": triangle_product_sum,
        "X_equals_40V": x_value,
        "Y_equals_800D": y_value,
        "spectral_residual": spectral_residual,
        "admissible_Y_from_congruence_and_skew": congruent_values,
        "active_row_types": len(active_from_full),
        "active_triangle_types": sum(value > 0 for value in triple_counts),
        "minimum_pair_moment_degrees_2_to_60": str(
            min(pair_moments[2:])
        ),
        "minimum_stratified_capacity_slack": min(stratified),
        "minimum_weighted_capacity_slack": min(weighted),
        "radial_degree_zero_rank": radial_rank,
        "radial_minimum_positive_pivot": str(min(radial_pivots)),
        "frame_blocks": frame_records,
        "scope": (
            "centered quarter-grid finite relaxation only; not a Gram "
            "matrix or spherical code"
        ),
    }


def main() -> None:
    try:
        result = verify()
    except (
        KeyError,
        TypeError,
        ValueError,
        VerificationError,
        endpoint.VerificationError,
    ) as error:
        print(f"verification failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
