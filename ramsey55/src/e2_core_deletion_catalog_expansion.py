#!/usr/bin/env python3
"""Turn shared-core E=2 near misses into verified order-42 catalog seeds.

If the only forbidden five-sets of an order-43 graph have the same colour
and intersect in four vertices, deleting any vertex of their common core
destroys both conflicts.  The four resulting order-42 graphs are therefore
Ramsey(5,5) graphs.  This tool verifies that implication directly, labels the
derived graphs with a pinned nauty ``labelg``, and compares their isomorphism
classes (also modulo complementation) with an input catalog.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from graph_io import complement, decode_graph6, encode_graph6, validate_simple  # noqa: E402


SCHEMA = "ramsey55.e2_core_deletion_catalog_expansion.v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def data_lines(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(encoding="ascii").splitlines()
        if line.strip() and not line.startswith("#") and not line.startswith(">>")
    ]


def homogeneous_five_sets(adjacency: list[int]) -> list[tuple[str, tuple[int, ...]]]:
    """Directly inspect all ten pairs of every five-set."""
    validate_simple(adjacency)
    result: list[tuple[str, tuple[int, ...]]] = []
    for vertices in itertools.combinations(range(len(adjacency)), 5):
        edge_count = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
        if edge_count == 10:
            result.append(("clique", vertices))
        elif edge_count == 0:
            result.append(("independent", vertices))
    return result


def contains_clique(adjacency: list[int], needed: int) -> bool:
    """Independent recursive-bitset existence check."""

    def search(candidates: int, remaining: int) -> bool:
        if remaining == 0:
            return True
        if candidates.bit_count() < remaining:
            return False
        while candidates:
            if candidates.bit_count() < remaining:
                return False
            bit = candidates & -candidates
            vertex = bit.bit_length() - 1
            candidates ^= bit
            if search(candidates & adjacency[vertex], remaining - 1):
                return True
        return False

    return search((1 << len(adjacency)) - 1, needed)


def bitset_ramsey_valid(adjacency: list[int]) -> bool:
    return not contains_clique(adjacency, 5) and not contains_clique(
        complement(adjacency), 5
    )


def delete_vertex(adjacency: list[int], removed: int) -> list[int]:
    vertices = [vertex for vertex in range(len(adjacency)) if vertex != removed]
    relabel = {old: new for new, old in enumerate(vertices)}
    result = [0] * len(vertices)
    for old_left in vertices:
        left = relabel[old_left]
        for old_right in vertices:
            if old_left < old_right and (adjacency[old_left] >> old_right) & 1:
                right = relabel[old_right]
                result[left] |= 1 << right
                result[right] |= 1 << left
    validate_simple(result)
    return result


def canonicalize_batch(graphs: list[str], labelg: Path) -> list[str]:
    if not graphs:
        return []
    with tempfile.TemporaryDirectory(prefix="ramsey55-e2-labelg.") as directory:
        temporary = Path(directory)
        source = temporary / "input.g6"
        target = temporary / "canonical.g6"
        source.write_text("".join(graph + "\n" for graph in graphs), encoding="ascii")
        completed = subprocess.run(
            [str(labelg), "-q", "-g", str(source), str(target)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"labelg failed ({completed.returncode}): {completed.stderr}"
            )
        canonical = data_lines(target)
    if len(canonical) != len(graphs):
        raise RuntimeError("labelg output count does not match its input")
    if any(len(decode_graph6(graph)) != 42 for graph in canonical):
        raise RuntimeError("labelg changed an input graph order")
    return canonical


def parse_line(path: Path) -> int:
    stem = path.stem
    if not stem.startswith("line_") or not stem[5:].isdigit():
        raise ValueError(f"candidate name does not encode a catalog line: {path}")
    return int(stem[5:])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--labelg", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--derived-g6", type=Path, required=True)
    args = parser.parse_args()

    candidate_paths = sorted(args.candidates.glob("line_*.g6"))
    if not candidate_paths:
        raise ValueError("candidate directory contains no line_*.g6 files")
    if not args.labelg.is_file():
        raise ValueError("labelg executable is missing")

    raw_records: list[dict[str, object]] = []
    derived_adjacencies: list[list[int]] = []
    for candidate_path in candidate_paths:
        lines = data_lines(candidate_path)
        if len(lines) != 1:
            raise ValueError(f"expected one graph in {candidate_path}")
        adjacency = decode_graph6(lines[0])
        if len(adjacency) != 43:
            raise ValueError(f"expected order 43 in {candidate_path}")
        conflicts = homogeneous_five_sets(adjacency)
        if (
            len(conflicts) != 2
            or conflicts[0][0] != conflicts[1][0]
            or len(set(conflicts[0][1]) & set(conflicts[1][1])) != 4
        ):
            raise ValueError(
                f"{candidate_path} lacks the required same-colour E=2 geometry"
            )
        common_core = sorted(set(conflicts[0][1]) & set(conflicts[1][1]))
        for removed in common_core:
            derived = delete_vertex(adjacency, removed)
            direct_conflicts = homogeneous_five_sets(derived)
            bitset_valid = bitset_ramsey_valid(derived)
            if direct_conflicts or not bitset_valid:
                raise AssertionError("derived order-42 graph failed verification")
            derived_index = len(derived_adjacencies)
            derived_adjacencies.append(derived)
            raw_records.append(
                {
                    "catalog_line": parse_line(candidate_path),
                    "candidate_path": str(candidate_path),
                    "candidate_sha256": sha256_file(candidate_path),
                    "conflict_colour": conflicts[0][0],
                    "conflict_sets": [list(item[1]) for item in conflicts],
                    "common_core": common_core,
                    "removed_vertex": removed,
                    "derived_index": derived_index,
                    "derived_graph6": encode_graph6(derived),
                    "derived_sha256": hashlib.sha256(
                        (encode_graph6(derived) + "\n").encode("ascii")
                    ).hexdigest(),
                    "direct_forbidden_count": 0,
                    "recursive_bitset_valid": True,
                    "edge_count": sum(row.bit_count() for row in derived) // 2,
                    "degree_sequence": sorted(row.bit_count() for row in derived),
                }
            )

    catalog_graphs = data_lines(args.catalog)
    if any(len(decode_graph6(graph)) != 42 for graph in catalog_graphs):
        raise ValueError("catalog contains a graph of order other than 42")

    all_graphs = catalog_graphs + [
        encode_graph6(adjacency) for adjacency in derived_adjacencies
    ]
    all_complements = [
        encode_graph6(complement(decode_graph6(graph))) for graph in all_graphs
    ]
    canonical = canonicalize_batch(all_graphs, args.labelg)
    canonical_complements = canonicalize_batch(all_complements, args.labelg)
    normalized = [
        min(graph, dual)
        for graph, dual in zip(canonical, canonical_complements, strict=True)
    ]

    catalog_count = len(catalog_graphs)
    catalog_iso_lines: dict[str, list[int]] = defaultdict(list)
    catalog_dual_lines: dict[str, list[int]] = defaultdict(list)
    for line, (graph, dual_key) in enumerate(
        zip(canonical[:catalog_count], normalized[:catalog_count], strict=True),
        start=1,
    ):
        catalog_iso_lines[graph].append(line)
        catalog_dual_lines[dual_key].append(line)

    derived_canonical = canonical[catalog_count:]
    derived_normalized = normalized[catalog_count:]
    for record, graph, dual_graph, dual_key in zip(
        raw_records,
        derived_canonical,
        canonical_complements[catalog_count:],
        derived_normalized,
        strict=True,
    ):
        record.update(
            {
                "canonical_graph6": graph,
                "canonical_complement_graph6": dual_graph,
                "complement_normalized_key": dual_key,
                "catalog_isomorphic_lines": catalog_iso_lines.get(graph, []),
                "catalog_isomorphic_or_complement_lines": catalog_dual_lines.get(
                    dual_key, []
                ),
                "novel_vs_catalog_isomorphism": graph not in catalog_iso_lines,
                "novel_vs_catalog_modulo_complement": dual_key
                not in catalog_dual_lines,
            }
        )

    iso_groups: dict[str, list[int]] = defaultdict(list)
    dual_groups: dict[str, list[int]] = defaultdict(list)
    for index, (graph, dual_key) in enumerate(
        zip(derived_canonical, derived_normalized, strict=True)
    ):
        iso_groups[graph].append(index)
        dual_groups[dual_key].append(index)

    novel_iso = sorted(
        {graph for graph in derived_canonical if graph not in catalog_iso_lines}
    )
    novel_dual = sorted(
        {key for key in derived_normalized if key not in catalog_dual_lines}
    )
    args.derived_g6.parent.mkdir(parents=True, exist_ok=True)
    args.derived_g6.write_text(
        "".join(graph + "\n" for graph in novel_dual), encoding="ascii"
    )

    result = {
        "schema": SCHEMA,
        "status": "COMPLETE",
        "evidence": "CERTIFIED_FINITE_CORPUS_TRANSFORMATION",
        "claim_boundary": (
            "Every recorded deletion is a dual-verified order-42 Ramsey graph; "
            "catalog novelty is relative only to the supplied 328-line catalog."
        ),
        "inputs": {
            "candidate_directory": str(args.candidates),
            "candidate_count": len(candidate_paths),
            "candidate_corpus_sha256": hashlib.sha256(
                b"".join(path.read_bytes() for path in candidate_paths)
            ).hexdigest(),
            "catalog": str(args.catalog),
            "catalog_count": catalog_count,
            "catalog_sha256": sha256_file(args.catalog),
            "labelg": str(args.labelg),
            "labelg_sha256": sha256_file(args.labelg),
        },
        "derived_record_count": len(raw_records),
        "derived_isomorphism_class_count": len(iso_groups),
        "derived_modulo_complement_class_count": len(dual_groups),
        "catalog_isomorphism_novel_class_count": len(novel_iso),
        "catalog_modulo_complement_novel_class_count": len(novel_dual),
        "novel_modulo_complement_graphs": novel_dual,
        "derived_g6": str(args.derived_g6),
        "records": raw_records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({key: value for key, value in result.items() if key != "records"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
