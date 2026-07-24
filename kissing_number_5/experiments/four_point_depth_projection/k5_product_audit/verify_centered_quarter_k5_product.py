#!/usr/bin/env python3
"""Exact audit of the centered quarter-grid K5 extension.

The audit expands every stored K5 atom under S_5 and tests the universal
edge-conditioned inequality

    (H_e - 7) (M_e - Gamma_e) >= 0.

Only Python standard-library integer and Fraction arithmetic is used.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, permutations
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
EXTENSION = ROOT / "certificates" / "centered_quarter_k5_extension.json"
CERTIFICATE = Path(__file__).with_name("centered_quarter_k5_product_audit.json")

SOURCE_SHA256 = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)
EXTENSION_SHA256 = (
    "133e8b502653b3bb1e1c4c3eb6c0452705020f65128959dc9d0cb34a8c0645ef"
)

N = 41
DELTA = Q(1, 300)
EDGE_POSITIONS = (
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 3),
    (2, 4),
    (3, 4),
)
VERTEX_PERMUTATIONS = tuple(permutations(range(5)))


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def parse_q(value: object) -> Q:
    return Q(str(value))


def display(value: Q) -> str:
    return str(value)


def relabel(edge_colors: tuple[int, ...], permutation: tuple[int, ...]) -> tuple[int, ...]:
    """Relabel a colored K5 by the old-to-new vertex permutation."""

    old = dict(zip(EDGE_POSITIONS, edge_colors))
    new = {
        tuple(sorted((permutation[i], permutation[j]))): color
        for (i, j), color in old.items()
    }
    return tuple(new[edge] for edge in EDGE_POSITIONS)


def orbit(edge_colors: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        sorted(
            {
                relabel(edge_colors, permutation)
                for permutation in VERTEX_PERMUTATIONS
            }
        )
    )


def triangle_types(edge_colors: tuple[int, ...]) -> tuple[tuple[int, int, int], ...]:
    edge = dict(zip(EDGE_POSITIONS, edge_colors))
    return tuple(
        tuple(sorted((edge[(i, j)], edge[(i, k)], edge[(j, k)])))
        for i in range(5)
        for j in range(i + 1, 5)
        for k in range(j + 1, 5)
    )


def determinant(matrix: list[list[Q]]) -> Q:
    """Fraction-free Gaussian determinant with exact row swaps."""

    size = len(matrix)
    work = [row[:] for row in matrix]
    sign = 1
    previous = Q(1)
    for pivot_index in range(size - 1):
        pivot_row = next(
            (
                row
                for row in range(pivot_index, size)
                if work[row][pivot_index] != 0
            ),
            None,
        )
        if pivot_row is None:
            return Q(0)
        if pivot_row != pivot_index:
            work[pivot_index], work[pivot_row] = (
                work[pivot_row],
                work[pivot_index],
            )
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                work[row][column] = (
                    pivot * work[row][column]
                    - work[row][pivot_index] * work[pivot_index][column]
                ) / previous
        previous = pivot
    return Q(sign) * work[-1][-1]


def gram_is_psd(edge_colors: tuple[int, ...], grid: tuple[Q, ...]) -> bool:
    matrix = [[Q(1) if i == j else Q(0) for j in range(5)] for i in range(5)]
    for (i, j), color in zip(EDGE_POSITIONS, edge_colors):
        matrix[i][j] = grid[color]
        matrix[j][i] = grid[color]
    return all(
        determinant([[matrix[i][j] for j in indices] for i in indices]) >= 0
        for size in range(1, 6)
        for indices in combinations(range(5), size)
    )


def capacity_from_p(p: Q) -> int | None:
    """The exact nonpositive-base projection hierarchy."""

    if p > 1:
        return 0
    if p > Q(3, 4):
        return 1
    if p > Q(2, 3):
        return 2
    if p > Q(5, 8):
        return 3
    if p > Q(1, 2):
        return 4
    if p == Q(1, 2):
        return 6
    return None


def applicable_capacity(q: Q, b: Q) -> tuple[Q | None, int, str] | None:
    """Return every nontrivial proved capacity available on this grid."""

    assert -1 < q <= Q(1, 2)
    assert 0 < b <= Q(1, 2)
    if q <= 0:
        p = 2 * b * b / (1 + q)
        capacity = capacity_from_p(p)
        if capacity is not None:
            return p, capacity, "nonpositive-base projection hierarchy"
    if b == Q(1, 2) and q > 0:
        return None, 7, "universal common-contact cap A(3,1/4)=7"
    return None


def local_statistics(
    edge_colors: tuple[int, ...],
    grid: tuple[Q, ...],
    q: Q,
    b: Q,
) -> tuple[int, int, int, int]:
    """Return (D,H,Gamma,H*Gamma), summed over base edges of color q."""

    edge = {
        pair: grid[color] for pair, color in zip(EDGE_POSITIONS, edge_colors)
    }
    base_count = depth_count = common_count = product_count = 0
    for y, z in EDGE_POSITIONS:
        if edge[(y, z)] != q:
            continue
        base_count += 1
        local_depth = 0
        local_common = 0
        for x in range(5):
            if x in (y, z):
                continue
            a = edge[tuple(sorted((x, y)))]
            c = edge[tuple(sorted((x, z)))]

            # Evaluate the strict radical comparison without a square root.
            # Its left side must first be negative; squaring then preserves
            # the strict inequality.  The quarter-grid simplification is
            # checked independently rather than assumed.
            incident_sum = a + c
            exact_depth_test = (
                incident_sum < 0
                and incident_sum * incident_sum
                > DELTA * DELTA * (2 + 2 * q)
            )
            assert 4 * incident_sum == int(4 * incident_sum)
            assert exact_depth_test == (incident_sum <= Q(-1, 4))
            if exact_depth_test:
                local_depth += 1
            if a >= b and c >= b:
                local_common += 1

        # The two selected sets are disjoint because b>0.
        assert local_depth + local_common <= 3
        depth_count += local_depth
        common_count += local_common
        product_count += local_depth * local_common
    return base_count, depth_count, common_count, product_count


def reconstruct_labeled_measure(
    source: dict[str, object],
    extension: dict[str, object],
) -> tuple[
    tuple[Q, ...],
    dict[tuple[int, ...], Q],
    Counter[int],
]:
    grid = tuple(parse_q(value) for value in source["grid"])
    atoms = extension["atoms"]
    assert len(atoms) == 51

    labeled_weights: dict[tuple[int, ...], Q] = {}
    canonical_orbits: set[tuple[int, ...]] = set()
    orbit_sizes: Counter[int] = Counter()
    total_weight = Q(0)

    for atom in atoms:
        weight = parse_q(atom["weight"])
        assert weight > 0
        total_weight += weight
        edge_colors = tuple(
            atom[
                "edge_color_indices_01_02_03_04_12_13_14_23_24_34"
            ]
        )
        assert len(edge_colors) == 10
        assert all(0 <= color < len(grid) for color in edge_colors)
        assert gram_is_psd(edge_colors, grid)

        labeled_orbit = orbit(edge_colors)
        canonical = labeled_orbit[0]
        assert canonical not in canonical_orbits
        canonical_orbits.add(canonical)
        orbit_sizes[len(labeled_orbit)] += 1
        per_label_weight = weight / len(labeled_orbit)
        for labeled_atom in labeled_orbit:
            assert labeled_atom not in labeled_weights
            labeled_weights[labeled_atom] = per_label_weight

    assert total_weight == 1
    assert sum(labeled_weights.values(), Q(0)) == 1
    assert len(labeled_weights) == 2940
    assert orbit_sizes == Counter({10: 3, 30: 11, 60: 31, 120: 6})

    # Independently recover the pair and triangle marginals.
    edge_marginal = [Q(0) for _ in grid]
    triples = tuple(tuple(item) for item in source["triple_orbits"])
    triple_index = {triple: index for index, triple in enumerate(triples)}
    triangle_marginal = [Q(0) for _ in triples]
    for labeled_atom, weight in labeled_weights.items():
        for color in labeled_atom:
            edge_marginal[color] += weight
        for triangle in triangle_types(labeled_atom):
            triangle_marginal[triple_index[triangle]] += weight
    alpha = tuple(parse_q(value) for value in source["alpha"])
    nu = tuple(parse_q(value) for value in source["nu"])
    assert edge_marginal == [value / 4 for value in alpha]
    assert triangle_marginal == [value / 156 for value in nu]
    return grid, labeled_weights, orbit_sizes


def evaluate_rows(
    grid: tuple[Q, ...],
    labeled_weights: dict[tuple[int, ...], Q],
) -> list[dict[str, object]]:
    product_repetitions = N - 4
    triple_repetitions = comb(N - 3, 2)
    edge_repetitions = comb(N - 2, 3)
    assert (product_repetitions, triple_repetitions, edge_repetitions) == (
        37,
        703,
        9139,
    )
    assert edge_repetitions // product_repetitions == 247
    assert edge_repetitions // triple_repetitions == 13

    rows: list[dict[str, object]] = []
    for q in grid:
        if q <= -1:
            continue
        for b in grid:
            if b <= 0:
                continue
            capacity_data = applicable_capacity(q, b)
            if capacity_data is None:
                continue
            p, capacity, theorem = capacity_data

            totals = [Q(0), Q(0), Q(0), Q(0)]
            for labeled_atom, weight in labeled_weights.items():
                statistics = local_statistics(labeled_atom, grid, q, b)
                for index, value in enumerate(statistics):
                    totals[index] += weight * value
            base_mass, depth_mass, common_mass, product_mass = totals

            normalized_left = product_mass / product_repetitions
            normalized_right = (
                Q(capacity) * depth_mass / triple_repetitions
                + 7 * common_mass / triple_repetitions
                - Q(7 * capacity) * base_mass / edge_repetitions
            )
            normalized_slack = normalized_right - normalized_left

            # Multiplication by 9139 gives the cleaner equivalent row
            # 247 P <= 13 M H + 91 Gamma - 7 M D.
            scaled_left = 247 * product_mass
            scaled_right = (
                Q(13 * capacity) * depth_mass
                + 91 * common_mass
                - Q(7 * capacity) * base_mass
            )
            scaled_slack = scaled_right - scaled_left
            assert scaled_slack == edge_repetitions * normalized_slack

            rows.append(
                {
                    "base_inner_product": display(q),
                    "positive_threshold": display(b),
                    "projection_parameter": None if p is None else display(p),
                    "capacity": capacity,
                    "capacity_source": theorem,
                    "D_expected_base_edges": display(base_mass),
                    "H_expected_local_depth_incidences": display(depth_mass),
                    "Gamma_expected_local_common_incidences": display(common_mass),
                    "P_expected_local_depth_common_product": display(product_mass),
                    "scaled_left_247P": display(scaled_left),
                    "scaled_right_13MH_plus_91Gamma_minus_7MD": display(
                        scaled_right
                    ),
                    "scaled_slack_right_minus_left": display(scaled_slack),
                    "normalized_slack_right_minus_left": display(
                        normalized_slack
                    ),
                    "violated": scaled_slack < 0,
                }
            )
    return rows


def verify(
    source_path: Path = SOURCE,
    extension_path: Path = EXTENSION,
    certificate_path: Path = CERTIFICATE,
) -> dict[str, object]:
    assert digest(source_path) == SOURCE_SHA256
    assert digest(extension_path) == EXTENSION_SHA256
    source = json.loads(source_path.read_text())
    extension = json.loads(extension_path.read_text())
    certificate = json.loads(certificate_path.read_text())
    assert source["schema"] == "kissing5.centered_quarter_bv_pseudodistribution.v1"
    assert extension["schema"] == "kissing5.centered_quarter_k5_extension.v1"
    assert certificate["schema"] == "kissing5.centered_quarter_k5_product_audit.v1"
    assert certificate["source_sha256"] == SOURCE_SHA256
    assert certificate["extension_sha256"] == EXTENSION_SHA256
    assert certificate["cardinality"] == N
    assert parse_q(certificate["depth_threshold"]) == DELTA
    assert certificate["status"] == "REFUTED_BY_TWO_EXACT_PRODUCT_ROWS"

    grid, labeled_weights, orbit_sizes = reconstruct_labeled_measure(
        source, extension
    )
    assert certificate["orbit_reconstruction"] == {
        "positive_orbits": 51,
        "distinct_labeled_atoms": 2940,
        "orbit_size_histogram": {
            "10": 3,
            "30": 11,
            "60": 31,
            "120": 6,
        },
    }
    rows = evaluate_rows(grid, labeled_weights)
    assert rows == certificate["rows"]
    violated = [
        (
            row["base_inner_product"],
            row["positive_threshold"],
            row["capacity"],
        )
        for row in rows
        if row["violated"]
    ]
    assert violated == [("-1/2", "1/2", 1), ("-1/4", "1/2", 3)]
    assert certificate["violated_rows"] == [
        {
            "base_inner_product": q,
            "positive_threshold": b,
            "capacity": capacity,
        }
        for q, b, capacity in violated
    ]

    return {
        "status": "PASS",
        "audit_conclusion": (
            "the stored K5 extension violates two universal "
            "edge-conditioned depth/capacity product rows"
        ),
        "source_sha256": SOURCE_SHA256,
        "extension_sha256": EXTENSION_SHA256,
        "positive_orbits": len(extension["atoms"]),
        "distinct_labeled_atoms": len(labeled_weights),
        "orbit_size_histogram": dict(sorted(orbit_sizes.items())),
        "applicable_rows": len(rows),
        "violated_rows": violated,
        "strongest_normalized_slack": min(
            parse_q(row["normalized_slack_right_minus_left"]) for row in rows
        ),
    }


def main() -> None:
    report = verify()
    print(
        json.dumps(
            {
                key: display(value) if isinstance(value, Q) else value
                for key, value in report.items()
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
