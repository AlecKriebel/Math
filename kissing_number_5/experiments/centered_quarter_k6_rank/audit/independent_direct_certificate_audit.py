#!/usr/bin/env python3
"""Independent exact audit of the direct K8 and K9 local certificates.

This intentionally does not import either shipped verifier.  It uses rational
Gaussian elimination, rather than Bareiss elimination, for every principal
minor of every stored atom.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_PATH = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
EXPECTED_SOURCE_HASH = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)
CASES = {
    8: {
        "path": (
            ROOT
            / "experiments/centered_quarter_k6_rank/k8/"
            "direct_k8_triangle_extension.json"
        ),
        "hash": "9499977c14f3de72cd0b55d83872a645f2727f120182d010967832106b65b195",
    },
    9: {
        "path": (
            ROOT
            / "experiments/centered_quarter_k6_rank/k9/"
            "direct_k9_triangle_extension.json"
        ),
        "hash": "b0ead73d99ea050a002a36bfd78f549348d37d19244c147228bee26ad692b148",
    },
    10: {
        "path": (
            ROOT
            / "experiments/centered_quarter_k6_rank/k10/"
            "direct_k10_triangle_extension.json"
        ),
        "hash": "542f3061bfe282d98580955e62e756bfd9646890a45747f0baad8b11f750cc28",
    },
    11: {
        "path": (
            ROOT
            / "experiments/centered_quarter_k6_rank/k11/"
            "direct_k11_triangle_extension.json"
        ),
        "hash": "f02f52aed4d843434ef6b16c31d03e6176f0566d0a9fa12d02b50b0ec0aee54a",
    },
}


def require(condition: bool, message: str) -> None:
    """Raise even when Python assertions have been disabled."""
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    """Exact determinant by ordinary rational Gaussian elimination."""
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


def audit_case(
    size: int,
    source: dict[str, object],
    grid: tuple[Fraction, ...],
    triple_index: dict[tuple[int, int, int], int],
) -> dict[str, object]:
    path = CASES[size]["path"]
    require(isinstance(path, Path), "invalid case path")
    require(sha256(path) == CASES[size]["hash"], f"K{size} hash mismatch")
    certificate = json.loads(path.read_text())
    atoms = certificate["atoms"]
    require(len(atoms) == 51, f"K{size} atom count")
    edge_key = next(
        key for key in atoms[0] if key.startswith("edge_color_indices_")
    )
    pairs = tuple(itertools.combinations(range(size), 2))
    pair_index = {pair: index for index, pair in enumerate(pairs)}
    weights = [Fraction(atom["weight"]) for atom in atoms]
    require(all(weight > 0 for weight in weights), f"K{size} positivity")
    require(sum(weights) == 1, f"K{size} weight normalization")

    edge_counts = [Fraction(0) for _ in grid]
    triangle_counts = [Fraction(0) for _ in triple_index]
    feature_set: set[tuple[int, ...]] = set()
    principal_minor_count = 0
    minimum_positive_fifth: Fraction | None = None

    for atom_index, (atom, weight) in enumerate(zip(atoms, weights)):
        edges = tuple(atom[edge_key])
        require(len(edges) == len(pairs), f"K{size} atom {atom_index} edges")
        require(
            all(isinstance(color, int) and 0 <= color < len(grid) for color in edges),
            f"K{size} atom {atom_index} color range",
        )
        gram = [
            [Fraction(1 if i == j else 0) for j in range(size)]
            for i in range(size)
        ]
        for (i, j), color in zip(pairs, edges):
            gram[i][j] = gram[j][i] = grid[color]

        positive_fifth = False
        for order in range(1, size + 1):
            for indices in itertools.combinations(range(size), order):
                minor = determinant(
                    [[gram[i][j] for j in indices] for i in indices]
                )
                principal_minor_count += 1
                require(
                    minor >= 0,
                    f"K{size} atom {atom_index}: negative principal minor",
                )
                if order >= 6:
                    require(
                        minor == 0,
                        f"K{size} atom {atom_index}: rank exceeds five",
                    )
                if order == 5 and minor > 0:
                    positive_fifth = True
                    if (
                        minimum_positive_fifth is None
                        or minor < minimum_positive_fifth
                    ):
                        minimum_positive_fifth = minor
        require(positive_fifth, f"K{size} atom {atom_index}: rank below five")

        feature = []
        for i, j, k in itertools.combinations(range(size), 3):
            colors = tuple(
                sorted(
                    (
                        edges[pair_index[(i, j)]],
                        edges[pair_index[(i, k)]],
                        edges[pair_index[(j, k)]],
                    )
                )
            )
            require(colors in triple_index, f"K{size}: unknown triangle type")
            feature.append(triple_index[colors])
        feature.sort()
        feature_tuple = tuple(feature)
        require(
            feature_tuple == tuple(atom["triangle_orbit_indices"]),
            f"K{size} atom {atom_index}: stored triangle feature",
        )
        feature_set.add(feature_tuple)
        for color, multiplicity in Counter(edges).items():
            edge_counts[color] += weight * multiplicity
        for triangle, multiplicity in Counter(feature_tuple).items():
            triangle_counts[triangle] += weight * multiplicity

    alpha = [Fraction(value) for value in source["alpha"]]
    nu = [Fraction(value) for value in source["nu"]]
    edges_per_atom = size * (size - 1) // 2
    triangles_per_atom = size * (size - 1) * (size - 2) // 6
    require(
        edge_counts
        == [Fraction(edges_per_atom, 40) * value for value in alpha],
        f"K{size} edge marginal",
    )
    require(
        triangle_counts
        == [Fraction(triangles_per_atom, 1560) * value for value in nu],
        f"K{size} triangle marginal",
    )
    require(len(feature_set) == 51, f"K{size} distinct feature count")
    require(minimum_positive_fifth is not None, f"K{size} fifth minor")
    return {
        "certificate_sha256": sha256(path),
        "positive_atoms": len(atoms),
        "all_principal_minors_checked": principal_minor_count,
        "rank_of_every_atom": 5,
        "minimum_positive_normalized_fifth_minor": str(
            minimum_positive_fifth
        ),
        "edge_marginal": "exact alpha/40",
        "triangle_marginal": "exact nu/1560",
    }


def main() -> None:
    require(sha256(SOURCE_PATH) == EXPECTED_SOURCE_HASH, "source hash mismatch")
    source = json.loads(SOURCE_PATH.read_text())
    grid = tuple(Fraction(value) for value in source["grid"])
    require(max(grid) == Fraction(1, 2), "grid boundary mismatch")
    require(sum(map(Fraction, source["alpha"])) == 40, "alpha normalization")
    require(sum(map(Fraction, source["nu"])) == 1560, "nu normalization")
    triple_index = {
        tuple(triple): index
        for index, triple in enumerate(source["triple_orbits"])
    }
    require(len(triple_index) == 51, "triangle orbit count")
    result = {
        "status": "PASS",
        "method": "independent rational Gaussian elimination",
        "source_sha256": sha256(SOURCE_PATH),
        **{
            f"K{size}": audit_case(size, source, grid, triple_index)
            for size in CASES
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
