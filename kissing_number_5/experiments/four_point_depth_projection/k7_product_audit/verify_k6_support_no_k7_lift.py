#!/usr/bin/env python3
"""Exact exhaustive obstruction to lifting the 74-orbit K6 distribution.

The 74 positive K6 orbit representatives are expanded under all 720
vertex permutations.  Two supported labeled K6 faces are glued over their
common labeled K5, and all seven colors are tried on the sole missing K7
edge.  This covers every seven-colored complete graph K7 whose two chosen
K6 faces lie in the target support.  Every K7 in an exact nonnegative lift
would have all seven faces in that support.

The main enumeration uses faces deleting 6 and 5.  A second enumeration,
using faces deleting 0 and 1, is an exact coordinate-independent
cross-check.  The script uses only the Python standard library.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
K6_CERTIFICATE = HERE.parent / "k6_product_audit" / "productpool_extension.json"
RESULT_CERTIFICATE = HERE / "k6_support_no_k7_lift.json"
AVAILABLE_K7_POOL = (
    ROOT
    / "experiments"
    / "centered_quarter_k6_rank"
    / "k7"
    / "results"
    / "direct_k7_from_51.csv"
)

K6_SHA256 = (
    "def805e0c73fb5a5306f230ad21866a5b0fcab1a3708f6f7daaa3b175dc54991"
)
AVAILABLE_K7_POOL_SHA256 = (
    "16cee0b4f7b6b7655990a74f7ffef104c4aef43d5074696cbbb1bcf413d1a623"
)
AVAILABLE_K7_POOL_HEADER = (
    "# source_k6_atoms=51 rank_five_labeled=2012 "
    "distinct_triangle_count_vectors=1782"
)

PAIRS6 = tuple(itertools.combinations(range(6), 2))
PAIRS7 = tuple(itertools.combinations(range(7), 2))
PAIR_INDEX7 = {pair: index for index, pair in enumerate(PAIRS7)}
PERMUTATIONS6 = tuple(itertools.permutations(range(6)))
EDGE_KEY = (
    "edge_color_indices_"
    "01_02_03_04_05_12_13_14_15_23_24_25_34_35_45"
)

# Positions of each K6 face in a K7 edge tuple.  The K6 local labels are
# assigned in increasing order of the six retained global labels.
FACE_INDICES = tuple(
    tuple(
        PAIR_INDEX7[tuple(sorted((vertices[i], vertices[j])))]
        for i, j in PAIRS6
    )
    for deleted in range(7)
    for vertices in [
        tuple(vertex for vertex in range(7) if vertex != deleted)
    ]
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permute_k6(
    edges: tuple[int, ...], permutation: tuple[int, ...]
) -> tuple[int, ...]:
    by_pair = dict(zip(PAIRS6, edges))
    return tuple(
        by_pair[tuple(sorted((permutation[first], permutation[second])))]
        for first, second in PAIRS6
    )


def expand_labeled_support(
    representatives: tuple[tuple[int, ...], ...],
) -> tuple[dict[tuple[int, ...], int], Counter[int]]:
    """Expand disjoint unlabeled S6 orbits to their labeled elements."""

    labeled_to_orbit: dict[tuple[int, ...], int] = {}
    orbit_sizes: Counter[int] = Counter()
    for orbit_index, representative in enumerate(representatives):
        assert len(representative) == 15
        orbit = {
            permute_k6(representative, permutation)
            for permutation in PERMUTATIONS6
        }
        orbit_sizes[len(orbit)] += 1
        for edges in orbit:
            # Distinct certificate atoms must be distinct unlabeled orbits.
            assert edges not in labeled_to_orbit
            labeled_to_orbit[edges] = orbit_index
    return labeled_to_orbit, orbit_sizes


def face_tuple(edges7: tuple[int, ...], deleted: int) -> tuple[int, ...]:
    return tuple(edges7[index] for index in FACE_INDICES[deleted])


def overlap_key_for_face(
    edges6: tuple[int, ...],
    deleted_face_vertex: int,
    other_deleted_vertex: int,
) -> tuple[int, ...]:
    """Restriction of one K6 face to the common global K5."""

    face_vertices = tuple(
        vertex for vertex in range(7) if vertex != deleted_face_vertex
    )
    local_index = {
        global_vertex: index
        for index, global_vertex in enumerate(face_vertices)
    }
    overlap = tuple(
        vertex
        for vertex in range(7)
        if vertex not in (deleted_face_vertex, other_deleted_vertex)
    )
    edge_map = dict(zip(PAIRS6, edges6))
    return tuple(
        edge_map[
            tuple(
                sorted(
                    (
                        local_index[first],
                        local_index[second],
                    )
                )
            )
        ]
        for first, second in itertools.combinations(overlap, 2)
    )


def enumerate_for_face_pair(
    labeled_to_orbit: dict[tuple[int, ...], int],
    deleted_first: int,
    deleted_second: int,
    color_count: int = 7,
) -> dict[str, object]:
    """Exhaust every gluing for one fixed pair of K6 faces."""

    assert deleted_first != deleted_second
    first_by_overlap: dict[
        tuple[int, ...], list[tuple[int, ...]]
    ] = defaultdict(list)
    second_by_overlap: dict[
        tuple[int, ...], list[tuple[int, ...]]
    ] = defaultdict(list)
    for edges in labeled_to_orbit:
        first_by_overlap[
            overlap_key_for_face(
                edges, deleted_first, deleted_second
            )
        ].append(edges)
        second_by_overlap[
            overlap_key_for_face(
                edges, deleted_second, deleted_first
            )
        ].append(edges)

    assert set(first_by_overlap) == set(second_by_overlap)
    key_size_histogram: Counter[int] = Counter()
    ordered_pairs = 0
    support_face_histogram: Counter[int] = Counter()
    compatible = 0
    missing_position = PAIR_INDEX7[
        tuple(sorted((deleted_first, deleted_second)))
    ]
    for key in first_by_overlap:
        first_group = first_by_overlap[key]
        second_group = second_by_overlap[key]
        # S6 invariance makes the two group sizes equal.  Assert this rather
        # than silently using a square in the ordered-pair count.
        assert len(first_group) == len(second_group)
        key_size_histogram[len(first_group)] += 1
        ordered_pairs += len(first_group) * len(second_group)
        for first_face in first_group:
            for second_face in second_group:
                partial = [-1] * 21
                for position, color in zip(
                    FACE_INDICES[deleted_first], first_face
                ):
                    partial[position] = color
                for position, color in zip(
                    FACE_INDICES[deleted_second], second_face
                ):
                    if partial[position] != -1:
                        assert partial[position] == color
                    partial[position] = color
                assert partial.count(-1) == 1
                assert partial[missing_position] == -1
                for last_color in range(color_count):
                    partial[missing_position] = last_color
                    edges7 = tuple(partial)
                    supported_faces = sum(
                        face_tuple(edges7, deleted)
                        in labeled_to_orbit
                        for deleted in range(7)
                    )
                    support_face_histogram[supported_faces] += 1
                    compatible += int(supported_faces == 7)

    return {
        "deleted_face_pair": [deleted_first, deleted_second],
        "overlap_keys": len(first_by_overlap),
        "overlap_group_size_histogram": dict(
            sorted(key_size_histogram.items())
        ),
        "compatible_ordered_k6_face_pairs": ordered_pairs,
        "last_edge_color_trials": color_count * ordered_pairs,
        "supported_face_count_histogram": dict(
            sorted(support_face_histogram.items())
        ),
        "support_compatible_labeled_k7": compatible,
    }


def scan_available_pool(
    pool_path: Path,
    labeled_to_orbit: dict[tuple[int, ...], int],
) -> dict[str, object]:
    """Redundant scan of the existing incomplete 1,782-row K7 pool."""

    assert digest(pool_path) == AVAILABLE_K7_POOL_SHA256
    histogram: Counter[int] = Counter()
    rows = 0
    with pool_path.open() as stream:
        header = next(stream).rstrip("\n")
        assert header == AVAILABLE_K7_POOL_HEADER
        for line in stream:
            fields = tuple(int(value) for value in line.split(","))
            assert len(fields) == 56
            edges7 = fields[:21]
            assert all(0 <= color < 7 for color in edges7)
            supported = sum(
                face_tuple(edges7, deleted) in labeled_to_orbit
                for deleted in range(7)
            )
            histogram[supported] += 1
            rows += 1
    assert rows == 1782
    assert dict(sorted(histogram.items())) == {
        0: 1607,
        1: 168,
        2: 7,
    }
    return {
        "sha256": AVAILABLE_K7_POOL_SHA256,
        "rows": rows,
        "supported_k6_face_histogram": dict(sorted(histogram.items())),
        "maximum_supported_k6_faces": max(histogram),
        "scope": (
            "redundant incomplete-pool scan; not the completeness argument"
        ),
    }


def verify(
    k6_path: Path = K6_CERTIFICATE,
    result_path: Path = RESULT_CERTIFICATE,
    pool_path: Path = AVAILABLE_K7_POOL,
) -> dict[str, object]:
    assert digest(k6_path) == K6_SHA256
    source = json.loads(k6_path.read_text())
    result_certificate = json.loads(result_path.read_text())
    assert source["schema"] == "kissing5.rank5_k6_product_extension.v1"
    assert result_certificate["schema"] == (
        "kissing5.k6_product_support_no_k7_lift.v1"
    )
    assert result_certificate["source_k6_sha256"] == K6_SHA256

    atoms = source["atoms"]
    weights = tuple(Q(atom["weight"]) for atom in atoms)
    assert len(atoms) == source["positive_atom_count"] == 74
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == 1
    representatives = tuple(tuple(atom[EDGE_KEY]) for atom in atoms)
    assert all(
        len(edges) == 15 and all(0 <= color < 7 for color in edges)
        for edges in representatives
    )

    labeled_to_orbit, orbit_sizes = expand_labeled_support(
        representatives
    )
    assert len(labeled_to_orbit) == 49800
    assert dict(sorted(orbit_sizes.items())) == {
        120: 1,
        360: 8,
        720: 65,
    }

    primary = enumerate_for_face_pair(labeled_to_orbit, 6, 5)
    crosscheck = enumerate_for_face_pair(labeled_to_orbit, 0, 1)
    expected_gluing = {
        "overlap_keys": 40696,
        "overlap_group_size_histogram": {
            1: 33940,
            2: 5470,
            3: 600,
            4: 540,
            6: 130,
            8: 15,
            60: 1,
        },
        "compatible_ordered_k6_face_pairs": 79100,
        "last_edge_color_trials": 553700,
        "supported_face_count_histogram": {
            2: 550820,
            3: 1560,
            4: 1320,
        },
        "support_compatible_labeled_k7": 0,
    }
    for report in (primary, crosscheck):
        for key, expected in expected_gluing.items():
            assert report[key] == expected

    pool_report = scan_available_pool(pool_path, labeled_to_orbit)

    # With no support-compatible K7, the K7-to-K6 face-count matrix has no
    # columns.  The target vector is b_i=7*w_i.  Thus y=-e_0 has vacuous
    # nonnegative column pairings and a strictly negative target pairing.
    target_pairing = -7 * weights[0]
    assert target_pairing == -Q(
        462937922730878632368908435955017028641430479,
        6373923427690822467663452332372800000000000000,
    )
    assert target_pairing < 0

    expected_certificate_enumeration = {
        "k6_orbits": 74,
        "labeled_k6_support": 49800,
        "k6_orbit_size_histogram": {
            "120": 1,
            "360": 8,
            "720": 65,
        },
        "common_labeled_k5_keys": 40696,
        "common_k5_group_size_histogram": {
            "1": 33940,
            "2": 5470,
            "3": 600,
            "4": 540,
            "6": 130,
            "8": 15,
            "60": 1,
        },
        "compatible_ordered_k6_face_pairs": 79100,
        "last_edge_color_trials": 553700,
        "supported_face_count_histogram": {
            "2": 550820,
            "3": 1560,
            "4": 1320,
        },
        "support_compatible_labeled_k7": 0,
    }
    assert (
        result_certificate["complete_support_enumeration"]
        == expected_certificate_enumeration
    )
    assert result_certificate["farkas_certificate"] == {
        "dual_vector": "-e_0",
        "column_pairings": [],
        "target_pairing": str(target_pairing),
    }
    assert result_certificate["available_k7_pool_crosscheck"] == {
        "sha256": AVAILABLE_K7_POOL_SHA256,
        "rows": 1782,
        "supported_k6_face_histogram": {
            "0": 1607,
            "1": 168,
            "2": 7,
        },
        "maximum_supported_k6_faces": 2,
    }

    return {
        "status": "PASS",
        "scope": (
            "complete seven-color K7 support obstruction for the exact "
            "74-orbit K6 product extension; no Gram/rank assumptions needed"
        ),
        "source_k6_sha256": K6_SHA256,
        "k6_orbits": len(representatives),
        "labeled_k6_support": len(labeled_to_orbit),
        "k6_orbit_size_histogram": dict(sorted(orbit_sizes.items())),
        "primary_gluing": primary,
        "opposite_face_pair_crosscheck": crosscheck,
        "support_compatible_labeled_k7": 0,
        "farkas_target_pairing": str(target_pairing),
        "available_k7_pool_crosscheck": pool_report,
        "conclusion": (
            "no nonnegative K7 distribution has the exact symmetric "
            "74-orbit K6 marginal"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
