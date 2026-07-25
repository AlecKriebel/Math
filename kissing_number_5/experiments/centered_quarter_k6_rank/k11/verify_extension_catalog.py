#!/usr/bin/env python3
"""Verify completeness of the per-source K10-to-K11 extension catalog."""

from __future__ import annotations

from collections import defaultdict
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_PATH = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
K10_PATH = HERE.parent / "k10" / "direct_k10_triangle_extension.json"
CERTIFICATE_PATH = HERE / "direct_k11_triangle_extension.json"
CATALOG_PATH = HERE / "results" / "direct_k11_all_extensions.csv"
DEDUPLICATED_PATH = HERE / "results" / "direct_k11_from_51.csv"
VALUES = (-4, -3, -2, -1, 0, 1, 2)
VALUE_INDEX = {value: index for index, value in enumerate(VALUES)}
PAIRS10 = tuple(itertools.combinations(range(10), 2))
PAIRS11 = tuple(itertools.combinations(range(11), 2))
PAIR_INDEX11 = {pair: index for index, pair in enumerate(PAIRS11)}
PERMUTATIONS = {
    size: tuple(itertools.permutations(range(size))) for size in range(1, 6)
}
EDGE_KEY10 = (
    "edge_color_indices_01_02_03_04_05_06_07_08_09_12_13_14_15_16_"
    "17_18_19_23_24_25_26_27_28_29_34_35_36_37_38_39_45_46_47_"
    "48_49_56_57_58_59_67_68_69_78_79_89"
)


def determinant(matrix: list[list[int]]) -> int:
    size = len(matrix)
    total = 0
    for permutation in PERMUTATIONS[size]:
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


def adjugate(matrix: list[list[int]]) -> list[list[int]]:
    size = len(matrix)
    answer = [[0] * size for _ in range(size)]
    for row in range(size):
        for column in range(size):
            minor = [
                [matrix[i][j] for j in range(size) if j != row]
                for i in range(size)
                if i != column
            ]
            answer[row][column] = (
                (-1 if (row + column) % 2 else 1) * determinant(minor)
            )
    return answer


def scaled_gram10(edges: tuple[int, ...]) -> list[list[int]]:
    matrix = [[4 if i == j else 0 for j in range(10)] for i in range(10)]
    for (i, j), color in zip(PAIRS10, edges, strict=True):
        matrix[i][j] = VALUES[color]
        matrix[j][i] = VALUES[color]
    return matrix


def triangle_feature(
    edges: tuple[int, ...],
    triple_index: dict[tuple[int, int, int], int],
) -> tuple[int, ...]:
    result = []
    for i, j, k in itertools.combinations(range(11), 3):
        colors = tuple(
            sorted(
                (
                    edges[PAIR_INDEX11[(i, j)]],
                    edges[PAIR_INDEX11[(i, k)]],
                    edges[PAIR_INDEX11[(j, k)]],
                )
            )
        )
        result.append(triple_index[colors])
    return tuple(sorted(result))


def enumerate_edges(base_edges: tuple[int, ...]) -> set[tuple[int, ...]]:
    gram = scaled_gram10(base_edges)
    choice = None
    for indices in itertools.combinations(range(10), 5):
        base = [[gram[i][j] for j in indices] for i in indices]
        base_determinant = determinant(base)
        if base_determinant > 0:
            omitted = tuple(index for index in range(10) if index not in indices)
            choice = indices, omitted, base, base_determinant
            break
    assert choice is not None
    indices, omitted, base, base_determinant = choice
    adj = adjugate(base)
    omitted_correlations = [
        [gram[index][vertex] for index in indices] for vertex in omitted
    ]

    answer = set()
    for color_vector in itertools.product(range(7), repeat=5):
        values = [VALUES[color] for color in color_vector]
        if (
            sum(
                values[i] * adj[i][j] * values[j]
                for i in range(5)
                for j in range(5)
            )
            != 4 * base_determinant
        ):
            continue
        forced_colors = []
        for correlations in omitted_correlations:
            numerator = sum(
                correlations[i] * adj[i][j] * values[j]
                for i in range(5)
                for j in range(5)
            )
            if numerator % base_determinant:
                break
            value = numerator // base_determinant
            if value not in VALUE_INDEX:
                break
            forced_colors.append(VALUE_INDEX[value])
        if len(forced_colors) != 5:
            continue
        new_colors: list[int | None] = [None] * 10
        for index, color in zip(indices, color_vector, strict=True):
            new_colors[index] = color
        for index, color in zip(omitted, forced_colors, strict=True):
            new_colors[index] = color
        edges = [0] * 55
        for pair, color in zip(PAIRS10, base_edges, strict=True):
            edges[PAIR_INDEX11[pair]] = color
        for index, color in enumerate(new_colors):
            assert color is not None
            edges[PAIR_INDEX11[(index, 10)]] = color
        edges_tuple = tuple(edges)
        assert edges_tuple not in answer
        answer.add(edges_tuple)
    return answer


def verify() -> dict[str, object]:
    source = json.loads(SOURCE_PATH.read_text())
    k10_bytes = K10_PATH.read_bytes()
    k10 = json.loads(k10_bytes)
    certificate = json.loads(CERTIFICATE_PATH.read_text())
    assert certificate["generation_k10_sha256"] == hashlib.sha256(
        k10_bytes
    ).hexdigest()
    assert certificate["generation_k10_sha256"] == (
        "542f3061bfe282d98580955e62e756bfd9646890a45747f0baad8b11f750cc28"
    )
    catalog_bytes = CATALOG_PATH.read_bytes()
    assert certificate["exhaustive_extension_catalog_sha256"] == (
        hashlib.sha256(catalog_bytes).hexdigest()
    )
    assert certificate["exhaustive_extension_catalog_sha256"] == (
        "6b4c5a53fbeca07875fff71e1b8836ff9426551b3ba6e4318e72a8dd5afe74d2"
    )
    deduplicated_bytes = DEDUPLICATED_PATH.read_bytes()
    assert certificate["discovery_catalog_sha256"] == hashlib.sha256(
        deduplicated_bytes
    ).hexdigest()
    assert certificate["discovery_catalog_sha256"] == (
        "e2ca3da3dc157ea8d02ec92e5b6e5599d30671cf856b524a0fc996af1f7294ce"
    )

    triple_index = {
        tuple(triple): index
        for index, triple in enumerate(source["triple_orbits"])
    }
    rows_by_source: dict[
        int, set[tuple[int, ...]]
    ] = defaultdict(set)
    first_by_feature: dict[tuple[int, ...], tuple[int, ...]] = {}
    lines = catalog_bytes.decode().splitlines()
    assert lines[0] == (
        "# source_k10_atoms=51 rank_five_labeled=1642 "
        "fields=source_atom_index_plus_55_edges_plus_165_triangle_indices"
    )
    for line in lines[1:]:
        fields = tuple(map(int, line.split(",")))
        assert len(fields) == 221
        atom_index = fields[0]
        edges = fields[1:56]
        feature = fields[56:]
        assert 0 <= atom_index < 51
        assert all(0 <= color < 7 for color in edges)
        assert feature == triangle_feature(edges, triple_index)
        assert edges not in rows_by_source[atom_index]
        rows_by_source[atom_index].add(edges)
        first_by_feature.setdefault(feature, edges)
    assert len(lines) == 1643
    assert sum(map(len, rows_by_source.values())) == 1642

    source_atoms = k10["atoms"]
    assert len(source_atoms) == 51
    per_source_counts = []
    for atom_index, atom in enumerate(source_atoms):
        base_edges = tuple(atom[EDGE_KEY10])
        expected = enumerate_edges(base_edges)
        observed = rows_by_source[atom_index]
        assert expected == observed
        per_source_counts.append(len(expected))
    assert sum(per_source_counts) == 1642

    deduplicated_lines = deduplicated_bytes.decode().splitlines()
    assert deduplicated_lines[0] == (
        "# source_k10_atoms=51 rank_five_labeled=1642 "
        "distinct_triangle_count_vectors=1508"
    )
    deduplicated = {}
    for line in deduplicated_lines[1:]:
        fields = tuple(map(int, line.split(",")))
        assert len(fields) == 220
        edges, feature = fields[:55], fields[55:]
        assert feature not in deduplicated
        deduplicated[feature] = edges
    assert deduplicated == first_by_feature
    assert len(deduplicated) == 1508

    return {
        "status": "PASS",
        "scope": (
            "all grid PSD rank-five K11 extensions of the 51 selected "
            "labeled K10 atoms"
        ),
        "source_atoms": len(source_atoms),
        "labeled_extensions": sum(per_source_counts),
        "distinct_triangle_count_vectors": len(deduplicated),
        "minimum_extensions_per_source": min(per_source_counts),
        "maximum_extensions_per_source": max(per_source_counts),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
