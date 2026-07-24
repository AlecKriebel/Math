#!/usr/bin/env python3
"""Independent exact verifier for the finite fixed-support K6 obstruction."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BV_PATH = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
K5_PATH = ROOT / "certificates" / "centered_quarter_k5_extension.json"
OBSTRUCTION_PATH = Path(__file__).with_name("fixed_support_obstruction.json")
PAIRS = {
    size: tuple(
        (i, j) for i in range(size) for j in range(i + 1, size)
    )
    for size in (5, 6)
}
PAIR_INDEX_6 = {pair: index for index, pair in enumerate(PAIRS[6])}
K4_EDGE_INDICES_IN_K5 = (0, 1, 2, 4, 5, 7)
FACE_INDICES = tuple(
    tuple(
        PAIR_INDEX_6[tuple(sorted((vertices[i], vertices[j])))]
        for i, j in PAIRS[5]
    )
    for deleted in range(6)
    for vertices in [
        tuple(vertex for vertex in range(6) if vertex != deleted)
    ]
)
SCALED_VALUES = (-4, -3, -2, -1, 0, 1, 2)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permute_edges(
    edges: tuple[int, ...], permutation: tuple[int, ...]
) -> tuple[int, ...]:
    pairs = PAIRS[len(permutation)]
    by_pair = {pair: color for pair, color in zip(pairs, edges, strict=True)}
    return tuple(
        by_pair[tuple(sorted((permutation[i], permutation[j])))]
        for i, j in pairs
    )


def labeled_orbit(edges: tuple[int, ...], size: int) -> set[tuple[int, ...]]:
    return {
        permute_edges(edges, permutation)
        for permutation in itertools.permutations(range(size))
    }


def determinant(matrix: tuple[tuple[int, ...], ...]) -> int:
    """Leibniz determinant, independent of the discovery Bareiss code."""

    size = len(matrix)
    total = 0
    for permutation in itertools.permutations(range(size)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(size)
            for j in range(i + 1, size)
        )
        product = 1
        for i in range(size):
            product *= matrix[i][permutation[i]]
        total += (-1 if inversions % 2 else 1) * product
    return total


def gram(edges: tuple[int, ...], size: int) -> tuple[tuple[int, ...], ...]:
    matrix = [[4 if i == j else 0 for j in range(size)] for i in range(size)]
    for (i, j), color in zip(PAIRS[size], edges, strict=True):
        matrix[i][j] = SCALED_VALUES[color]
        matrix[j][i] = SCALED_VALUES[color]
    return tuple(tuple(row) for row in matrix)


def principal_minors_nonnegative(edges: tuple[int, ...], size: int) -> bool:
    matrix = gram(edges, size)
    for order in range(1, size + 1):
        for indices in itertools.combinations(range(size), order):
            principal = tuple(
                tuple(matrix[i][j] for j in indices) for i in indices
            )
            if determinant(principal) < 0:
                return False
    return True


def face(edges: tuple[int, ...], deleted: int) -> tuple[int, ...]:
    return tuple(edges[index] for index in FACE_INDICES[deleted])


def canonical(edges: tuple[int, ...]) -> tuple[int, ...]:
    return min(labeled_orbit(edges, 6))


def verify() -> dict[str, object]:
    bv = json.loads(BV_PATH.read_text())
    k5 = json.loads(K5_PATH.read_text())
    certificate = json.loads(OBSTRUCTION_PATH.read_text())
    assert certificate["schema"] == (
        "kissing5.centered_quarter_k6_fixed_support_obstruction.v1"
    )
    assert certificate["source_bv_sha256"] == sha256(BV_PATH) == (
        "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
    )
    assert certificate["source_k5_sha256"] == sha256(K5_PATH) == (
        "133e8b502653b3bb1e1c4c3eb6c0452705020f65128959dc9d0cb34a8c0645ef"
    )
    assert k5["source_sha256"] == certificate["source_bv_sha256"]
    assert bv["grid"] == certificate["grid"]

    representatives = [
        tuple(
            atom[
                "edge_color_indices_01_02_03_04_12_13_14_23_24_34"
            ]
        )
        for atom in k5["atoms"]
    ]
    weights = [Q(atom["weight"]) for atom in k5["atoms"]]
    assert len(representatives) == len(weights) == 51
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == 1
    assert all(
        principal_minors_nonnegative(representative, 5)
        for representative in representatives
    )

    labeled_to_orbit: dict[tuple[int, ...], int] = {}
    orbit_sizes = []
    for orbit_index, representative in enumerate(representatives):
        orbit = labeled_orbit(representative, 5)
        orbit_sizes.append(len(orbit))
        for edges in orbit:
            assert edges not in labeled_to_orbit
            labeled_to_orbit[edges] = orbit_index
    assert len(labeled_to_orbit) == 2940

    by_k4: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for edges in labeled_to_orbit:
        key = tuple(edges[index] for index in K4_EDGE_INDICES_IN_K5)
        by_k4[key].append(edges)
    ordered_pairs = sum(len(group) ** 2 for group in by_k4.values())
    assert len(by_k4) == 1938
    assert ordered_pairs == 6942

    # Face deleting 5 supplies positions FACE_INDICES[5].  Face deleting 4
    # supplies FACE_INDICES[4].  Their common K4 agrees by construction; the
    # only still-unassigned edge is 45, at global position 14.
    compatible = 0
    determinant_zero = 0
    orbit_representatives: set[tuple[int, ...]] = set()
    for group in by_k4.values():
        for first in group:
            for second in group:
                base = [-1] * 15
                for position, color in zip(
                    FACE_INDICES[5], first, strict=True
                ):
                    base[position] = color
                for position, color in zip(
                    FACE_INDICES[4], second, strict=True
                ):
                    if base[position] != -1:
                        assert base[position] == color
                    base[position] = color
                assert base.count(-1) == 1 and base[14] == -1
                for last_color in range(7):
                    base[14] = last_color
                    edges = tuple(base)
                    face_orbits = []
                    for deleted in range(6):
                        orbit = labeled_to_orbit.get(face(edges, deleted))
                        if orbit is None:
                            break
                        face_orbits.append(orbit)
                    if len(face_orbits) != 6:
                        continue
                    compatible += 1
                    matrix = gram(edges, 6)
                    full_determinant = determinant(matrix)
                    if full_determinant != 0:
                        continue
                    determinant_zero += 1
                    assert principal_minors_nonnegative(edges, 6)
                    orbit_representatives.add(canonical(edges))

    assert compatible == determinant_zero == 240
    assert len(orbit_representatives) == 4
    calculated_orbits = []
    calculated_orbit_sizes = []
    for edges in sorted(orbit_representatives):
        counts = Counter(
            labeled_to_orbit[face(edges, deleted)] for deleted in range(6)
        )
        calculated_orbits.append(
            {
                "edge_color_indices_01_02_03_04_05_12_13_14_15_23_24_25_34_35_45": list(
                    edges
                ),
                "k5_face_orbit_counts": {
                    str(index): count for index, count in sorted(counts.items())
                },
            }
        )
        calculated_orbit_sizes.append(len(labeled_orbit(edges, 6)))
    assert calculated_orbits == certificate["k6_orbits"]
    assert calculated_orbit_sizes == [60, 60, 60, 60]

    enumeration = certificate["enumeration"]
    assert enumeration == {
        "method": (
            "join two labeled supported K5 faces over their common labeled "
            "K4 face, try all seven colors on the remaining edge, and check "
            "the other four K5 faces"
        ),
        "k5_orbits": 51,
        "labeled_k5_support": 2940,
        "k4_keys": 1938,
        "compatible_ordered_k5_face_pairs": 6942,
        "pre_support_k6_color_trials": 48594,
        "support_compatible_labeled_k6": 240,
        "determinant_zero_labeled_k6": 240,
        "rank_at_most_five_k6_orbits": 4,
        "rank_at_most_five_orbit_sizes": [60, 60, 60, 60],
    }

    # Exact finite Farkas certificate for A z = b, z >= 0.  Here A has the
    # four K5 face-count columns and b_i=6*w_i.  With y=-e_1, A^T y=0 while
    # b^T y=-6*w_1<0.
    face_counts = [
        Counter(
            labeled_to_orbit[face(edges, deleted)] for deleted in range(6)
        )
        for edges in sorted(orbit_representatives)
    ]
    assert all(counts[1] == 0 for counts in face_counts)
    target_pairing = -6 * weights[1]
    assert weights[1] == Q(193319639973, 2080000000000)
    assert target_pairing == -Q(579958919919, 1040000000000)
    farkas = certificate["farkas_certificate"]
    assert farkas["dual_vector"] == "-e_1"
    assert [Q(value) for value in farkas["column_pairings"]] == [Q(0)] * 4
    assert Q(farkas["target_pairing"]) == target_pairing < 0

    return {
        "status": "PASS",
        "scope": "particular 51-orbit K5 support and exact weights only",
        "labeled_k5_support": len(labeled_to_orbit),
        "k6_trials_after_k4_join": 7 * ordered_pairs,
        "support_compatible_labeled_k6": compatible,
        "rank_at_most_five_k6_orbits": len(orbit_representatives),
        "k5_face_types_represented": [0, 21, 39, 46],
        "farkas_target_pairing": str(target_pairing),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
