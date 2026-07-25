#!/usr/bin/env python3
"""Independent exact geometry/marginal audit of the K7 product candidate.

This script imports neither candidate verifier nor discovery code.  It uses
ordinary rational Gaussian elimination for every principal minor.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SOURCE = ROOT / "certificates/centered_quarter_bv_pseudodistribution.json"
CANDIDATE = (
    ROOT
    / "experiments/four_point_depth_projection/k7_product_audit/"
    "candidate_k7_product_extension.json"
)
POOL = (
    ROOT
    / "experiments/centered_quarter_k6_rank/k7/results/"
    "direct_k7_from_51.csv"
)
FROZEN_K6 = (
    ROOT
    / "experiments/four_point_depth_projection/k6_product_audit/"
    "productpool_extension.json"
)
EXPECTED_HASHES = {
    SOURCE: "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550",
    CANDIDATE: "1b5e262592e1872cfe9f26b344d82da5066d8332efc5104a34a433d9d5564b00",
    POOL: "16cee0b4f7b6b7655990a74f7ffef104c4aef43d5074696cbbb1bcf413d1a623",
    FROZEN_K6: "def805e0c73fb5a5306f230ad21866a5b0fcab1a3708f6f7daaa3b175dc54991",
}
EXPECTED_OUTSIDE_MASS = Fraction(
    3936200435868713179173616576291348691773640557,
    4107356591051568933699186942558000000000000000,
)
PAIRS7 = tuple(itertools.combinations(range(7), 2))
PAIR_INDEX7 = {pair: index for index, pair in enumerate(PAIRS7)}
PAIRS6 = tuple(itertools.combinations(range(6), 2))
PERMUTATIONS6 = tuple(itertools.permutations(range(6)))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    work = [row[:] for row in matrix]
    sign = 1
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
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign = -sign
        pivot_value = work[column][column]
        for row in range(column + 1, len(work)):
            multiplier = work[row][column] / pivot_value
            for other_column in range(column, len(work)):
                work[row][other_column] -= (
                    multiplier * work[column][other_column]
                )
    answer = Fraction(sign)
    for index in range(len(work)):
        answer *= work[index][index]
    return answer


def canonical_k6(edges: tuple[int, ...]) -> tuple[int, ...]:
    by_pair = dict(zip(PAIRS6, edges))
    return min(
        tuple(
            by_pair[tuple(sorted((permutation[i], permutation[j])))]
            for i, j in PAIRS6
        )
        for permutation in PERMUTATIONS6
    )


def deleted_k6_face(edges: tuple[int, ...], deleted: int) -> tuple[int, ...]:
    kept = tuple(vertex for vertex in range(7) if vertex != deleted)
    return tuple(
        edges[
            PAIR_INDEX7[
                tuple(sorted((kept[first], kept[second])))
            ]
        ]
        for first, second in PAIRS6
    )


def main() -> None:
    for path, expected in EXPECTED_HASHES.items():
        require(digest(path) == expected, f"hash mismatch: {path}")
    source = json.loads(SOURCE.read_text())
    candidate = json.loads(CANDIDATE.read_text())
    frozen_k6 = json.loads(FROZEN_K6.read_text())
    require(
        candidate["schema"] == "kissing5.rank5_k7_product_extension.v1",
        "candidate schema",
    )
    require(candidate["positive_atom_count"] == 53, "candidate atom count")

    atoms = candidate["atoms"]
    active = tuple(candidate["active_pool_indices"])
    require(len(atoms) == len(active) == len(set(active)) == 53, "active set")
    edge_key = next(
        key for key in atoms[0] if key.startswith("edge_color_indices_")
    )
    pool_lines = POOL.read_text().splitlines()
    require(
        pool_lines[0]
        == (
            "# source_k6_atoms=51 rank_five_labeled=2012 "
            "distinct_triangle_count_vectors=1782"
        ),
        "pool header",
    )
    for pool_index, atom in zip(active, atoms):
        fields = tuple(map(int, pool_lines[pool_index + 1].split(",")))
        require(
            tuple(atom[edge_key]) == fields[:21]
            and tuple(atom["triangle_orbit_indices"]) == fields[21:],
            f"pool row {pool_index}",
        )

    grid = tuple(Fraction(value) for value in source["grid"])
    require(max(grid) == Fraction(1, 2), "grid upper endpoint")
    triple_index = {
        tuple(triple): index
        for index, triple in enumerate(source["triple_orbits"])
    }
    require(len(triple_index) == 51, "triangle orbit count")
    weights = tuple(Fraction(atom["weight"]) for atom in atoms)
    require(all(weight > 0 for weight in weights), "positive weights")
    require(sum(weights) == 1, "weight normalization")

    edge_counts = [Fraction(0)] * 7
    triangle_counts = [Fraction(0)] * 51
    principal_minors = 0
    minimum_positive_fifth: Fraction | None = None
    induced_k6: dict[tuple[int, ...], Fraction] = defaultdict(Fraction)
    for atom_index, (atom, weight) in enumerate(zip(atoms, weights)):
        edges = tuple(atom[edge_key])
        require(
            len(edges) == 21 and all(0 <= color < 7 for color in edges),
            f"atom {atom_index} edge colors",
        )
        gram = [
            [Fraction(1 if i == j else 0) for j in range(7)]
            for i in range(7)
        ]
        for (first, second), color in zip(PAIRS7, edges):
            gram[first][second] = gram[second][first] = grid[color]
        rank_five = False
        for order in range(1, 8):
            for indices in itertools.combinations(range(7), order):
                value = determinant(
                    [[gram[i][j] for j in indices] for i in indices]
                )
                principal_minors += 1
                require(value >= 0, f"atom {atom_index}: negative minor")
                if order >= 6:
                    require(value == 0, f"atom {atom_index}: rank above five")
                if order == 5 and value > 0:
                    rank_five = True
                    if (
                        minimum_positive_fifth is None
                        or value < minimum_positive_fifth
                    ):
                        minimum_positive_fifth = value
        require(rank_five, f"atom {atom_index}: rank below five")

        feature = []
        for first, second, third in itertools.combinations(range(7), 3):
            colors = tuple(
                sorted(
                    (
                        edges[PAIR_INDEX7[(first, second)]],
                        edges[PAIR_INDEX7[(first, third)]],
                        edges[PAIR_INDEX7[(second, third)]],
                    )
                )
            )
            require(colors in triple_index, "unknown triangle type")
            feature.append(triple_index[colors])
        require(
            tuple(sorted(feature)) == tuple(atom["triangle_orbit_indices"]),
            f"atom {atom_index}: triangle feature",
        )
        for color, multiplicity in Counter(edges).items():
            edge_counts[color] += weight * multiplicity
        for triangle, multiplicity in Counter(feature).items():
            triangle_counts[triangle] += weight * multiplicity
        for deleted in range(7):
            face = deleted_k6_face(edges, deleted)
            induced_k6[canonical_k6(face)] += weight / 7

    alpha = tuple(Fraction(value) for value in source["alpha"])
    nu = tuple(Fraction(value) for value in source["nu"])
    require(
        edge_counts == [Fraction(21, 40) * value for value in alpha],
        "edge marginal",
    )
    require(
        triangle_counts == [Fraction(35, 1560) * value for value in nu],
        "triangle marginal",
    )
    require(principal_minors == 53 * (2**7 - 1), "principal minor count")
    require(minimum_positive_fifth == Fraction(3, 512), "fifth minor")
    require(sum(induced_k6.values()) == 1, "induced K6 mass")

    frozen_atoms = frozen_k6["atoms"]
    frozen_edge_key = next(
        key
        for key in frozen_atoms[0]
        if key.startswith("edge_color_indices_")
    )
    frozen_support = {
        canonical_k6(tuple(atom[frozen_edge_key])) for atom in frozen_atoms
    }
    require(len(frozen_support) == 74, "frozen K6 support")
    common_support = set(induced_k6) & frozen_support
    outside_mass = sum(
        (
            weight
            for orbit, weight in induced_k6.items()
            if orbit not in frozen_support
        ),
        Fraction(0),
    )
    require(outside_mass == EXPECTED_OUTSIDE_MASS, "outside-support mass")

    print(
        json.dumps(
            {
                "status": "PASS",
                "candidate_sha256": digest(CANDIDATE),
                "method": "independent rational Gaussian elimination",
                "positive_atoms": len(atoms),
                "all_principal_minors_checked": principal_minors,
                "rank_of_every_atom": 5,
                "minimum_positive_normalized_fifth_minor": str(
                    minimum_positive_fifth
                ),
                "edge_marginal": "exact alpha/40",
                "triangle_marginal": "exact nu/1560",
                "induced_k6_orbits": len(induced_k6),
                "frozen_k6_orbits_met": len(common_support),
                "induced_mass_outside_frozen_k6_support": str(outside_mass),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
