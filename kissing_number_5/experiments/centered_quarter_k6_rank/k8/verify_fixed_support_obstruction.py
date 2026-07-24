#!/usr/bin/env python3
"""Exact verifier for nonextension of the frozen K7 support to K8."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE_PATH = HERE.parent / "k7" / "direct_k7_triangle_extension.json"
CERTIFICATE_PATH = HERE / "fixed_support_obstruction.json"
PAIRS7 = tuple(itertools.combinations(range(7), 2))
PAIRS8 = tuple(itertools.combinations(range(8), 2))
PAIR_INDEX8 = {pair: index for index, pair in enumerate(PAIRS8)}
K6_INDICES_IN_K7 = tuple(
    index for index, (_i, j) in enumerate(PAIRS7) if j < 6
)
FACE_INDICES = tuple(
    tuple(
        PAIR_INDEX8[tuple(sorted((vertices[i], vertices[j])))]
        for i, j in PAIRS7
    )
    for deleted in range(8)
    for vertices in [
        tuple(vertex for vertex in range(8) if vertex != deleted)
    ]
)


def permute_edges(
    edges: tuple[int, ...], permutation: tuple[int, ...]
) -> tuple[int, ...]:
    by_pair = {
        pair: color for pair, color in zip(PAIRS7, edges, strict=True)
    }
    return tuple(
        by_pair[tuple(sorted((permutation[i], permutation[j])))]
        for i, j in PAIRS7
    )


def verify() -> dict[str, object]:
    source_bytes = SOURCE_PATH.read_bytes()
    source = json.loads(source_bytes)
    certificate = json.loads(CERTIFICATE_PATH.read_text())
    assert certificate["schema"] == (
        "kissing5.centered_quarter_k8_fixed_k7_support_obstruction.v1"
    )
    assert certificate["source_k7_sha256"] == hashlib.sha256(
        source_bytes
    ).hexdigest()
    assert certificate["source_k7_sha256"] == (
        "e666aea9882e10b25be7d73bd288a959f3df7bf8dd8f68dc6bb02f2fdf96ce19"
    )

    edge_key = (
        "edge_color_indices_01_02_03_04_05_06_12_13_14_15_16_"
        "23_24_25_26_34_35_36_45_46_56"
    )
    representatives = [tuple(atom[edge_key]) for atom in source["atoms"]]
    weights = [Q(atom["weight"]) for atom in source["atoms"]]
    assert len(representatives) == len(weights) == 51
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == 1

    labeled_to_orbit: dict[tuple[int, ...], int] = {}
    orbit_sizes = []
    for orbit_index, representative in enumerate(representatives):
        orbit = {
            permute_edges(representative, permutation)
            for permutation in itertools.permutations(range(7))
        }
        orbit_sizes.append(len(orbit))
        for edges in orbit:
            assert edges not in labeled_to_orbit
            labeled_to_orbit[edges] = orbit_index
    assert len(labeled_to_orbit) == 221340
    assert Counter(orbit_sizes) == {
        840: 1,
        1260: 1,
        2520: 11,
        5040: 38,
    }

    by_k6: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for edges in labeled_to_orbit:
        key = tuple(edges[index] for index in K6_INDICES_IN_K7)
        by_k6[key].append(edges)
    group_size_distribution = Counter(map(len, by_k6.values()))
    ordered_pairs = sum(len(group) ** 2 for group in by_k6.values())
    assert len(by_k6) == 192045
    assert group_size_distribution == {
        1: 168660,
        2: 19080,
        3: 3600,
        4: 360,
        6: 240,
        8: 105,
    }
    assert ordered_pairs == 298500

    compatible = 0
    for group in by_k6.values():
        for first in group:
            for second in group:
                base = [-1] * 28
                for position, color in zip(
                    FACE_INDICES[7], first, strict=True
                ):
                    base[position] = color
                for position, color in zip(
                    FACE_INDICES[6], second, strict=True
                ):
                    if base[position] != -1:
                        assert base[position] == color
                    base[position] = color
                assert base.count(-1) == 1 and base[27] == -1
                for last_color in range(7):
                    base[27] = last_color
                    edges = tuple(base)
                    if all(
                        tuple(edges[index] for index in FACE_INDICES[deleted])
                        in labeled_to_orbit
                        for deleted in range(8)
                    ):
                        compatible += 1
    assert compatible == 0

    enumeration = certificate["enumeration"]
    assert enumeration == {
        "method": (
            "join two labeled supported K7 faces over their common labeled "
            "K6 face, try all seven colors on the remaining edge, and check "
            "the other six K7 faces"
        ),
        "k7_orbits": 51,
        "labeled_k7_support": 221340,
        "orbit_size_distribution": {
            "840": 1,
            "1260": 1,
            "2520": 11,
            "5040": 38,
        },
        "k6_overlap_keys": 192045,
        "overlap_group_size_distribution": {
            "1": 168660,
            "2": 19080,
            "3": 3600,
            "4": 360,
            "6": 240,
            "8": 105,
        },
        "compatible_ordered_k7_face_pairs": 298500,
        "pre_support_k8_color_trials": 2089500,
        "support_compatible_labeled_k8": 0,
        "rank_at_most_five_k8_orbits": 0,
    }

    assert weights[50] == Q(1142575236831, 520000000000000)
    target_pairing = -8 * weights[50]
    assert target_pairing == -Q(1142575236831, 65000000000000)
    farkas = certificate["farkas_certificate"]
    assert farkas["dual_vector"] == "-e_50"
    assert farkas["column_pairings"] == []
    assert Q(farkas["target_pairing"]) == target_pairing < 0

    return {
        "status": "PASS",
        "scope": "particular frozen 51-orbit K7 distribution only",
        "labeled_k7_support": len(labeled_to_orbit),
        "k8_trials_after_k6_join": 7 * ordered_pairs,
        "support_compatible_labeled_k8": compatible,
        "farkas_target_pairing": str(target_pairing),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
