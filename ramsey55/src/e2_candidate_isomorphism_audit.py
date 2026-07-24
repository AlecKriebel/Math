#!/usr/bin/env python3
"""Audit isomorphism and complement-isomorphism classes of E=2 candidates."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from e2_core_deletion_catalog_expansion import (  # noqa: E402
    data_lines,
    homogeneous_five_sets,
)
from graph_io import complement, decode_graph6, encode_graph6  # noqa: E402


SCHEMA = "ramsey55.e2_candidate_isomorphism_audit.v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def canonicalize(graphs: list[str], labelg: Path, sparse: bool) -> list[str]:
    with tempfile.TemporaryDirectory(prefix="ramsey55-e2-iso.") as directory:
        temporary = Path(directory)
        source = temporary / "input.g6"
        target = temporary / "output.g6"
        source.write_text("".join(graph + "\n" for graph in graphs), encoding="ascii")
        command = [str(labelg), "-q", "-g"]
        if sparse:
            command.append("-S")
        command.extend([str(source), str(target)])
        completed = subprocess.run(
            command,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"labelg {'sparse' if sparse else 'dense'} failed: "
                f"{completed.stderr}"
            )
        result = data_lines(target)
    if len(result) != len(graphs):
        raise RuntimeError("labelg output count mismatch")
    return result


def partition(labels: list[str]) -> list[list[int]]:
    groups: dict[str, list[int]] = defaultdict(list)
    for index, label in enumerate(labels):
        groups[label].append(index)
    return sorted(sorted(group) for group in groups.values())


def normalized_labels(graphs: list[str], duals: list[str]) -> list[str]:
    return [min(graph, dual) for graph, dual in zip(graphs, duals, strict=True)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--labelg", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    paths = sorted(args.candidates.glob("line_*.g6"))
    if not paths:
        raise ValueError("no line_*.g6 candidates found")
    graphs: list[str] = []
    records: list[dict[str, object]] = []
    for path in paths:
        lines = data_lines(path)
        if len(lines) != 1:
            raise ValueError(f"expected exactly one graph in {path}")
        adjacency = decode_graph6(lines[0])
        conflicts = homogeneous_five_sets(adjacency)
        if (
            len(adjacency) != 43
            or len(conflicts) != 2
            or conflicts[0][0] != conflicts[1][0]
            or len(set(conflicts[0][1]) & set(conflicts[1][1])) != 4
        ):
            raise ValueError(f"candidate fails the exact E=2 geometry: {path}")
        line = int(path.stem.removeprefix("line_"))
        graphs.append(lines[0])
        records.append(
            {
                "catalog_line": line,
                "path": str(path),
                "sha256": sha256_file(path),
                "conflict_colour": conflicts[0][0],
                "conflict_sets": [list(item[1]) for item in conflicts],
            }
        )

    dual_graphs = [
        encode_graph6(complement(decode_graph6(graph))) for graph in graphs
    ]
    dense = canonicalize(graphs, args.labelg, sparse=False)
    dense_dual = canonicalize(dual_graphs, args.labelg, sparse=False)
    sparse = canonicalize(graphs, args.labelg, sparse=True)
    sparse_dual = canonicalize(dual_graphs, args.labelg, sparse=True)
    dense_partition = partition(dense)
    sparse_partition = partition(sparse)
    dense_dual_partition = partition(normalized_labels(dense, dense_dual))
    sparse_dual_partition = partition(normalized_labels(sparse, sparse_dual))
    if dense_partition != sparse_partition:
        raise AssertionError("dense and sparse labelg isomorphism partitions differ")
    if dense_dual_partition != sparse_dual_partition:
        raise AssertionError(
            "dense and sparse labelg complement-isomorphism partitions differ"
        )

    def group_record(group: list[int]) -> dict[str, object]:
        return {
            "size": len(group),
            "catalog_lines": [records[index]["catalog_line"] for index in group],
            "conflict_colours": sorted(
                {str(records[index]["conflict_colour"]) for index in group}
            ),
        }

    result = {
        "schema": SCHEMA,
        "status": "CERTIFIED_FINITE_CORPUS_CLASSIFICATION",
        "claim_boundary": (
            "This classifies only the supplied 22 labeled E=2 candidates; it "
            "does not classify all order-43 near misses or Ramsey graphs."
        ),
        "candidate_count": len(graphs),
        "candidate_corpus_sha256": hashlib.sha256(
            b"".join(path.read_bytes() for path in paths)
        ).hexdigest(),
        "labelg_path": str(args.labelg),
        "labelg_sha256": sha256_file(args.labelg),
        "dense_sparse_isomorphism_partition_match": True,
        "dense_sparse_complement_partition_match": True,
        "isomorphism_class_count": len(dense_partition),
        "isomorphism_classes": [group_record(group) for group in dense_partition],
        "modulo_complement_class_count": len(dense_dual_partition),
        "modulo_complement_classes": [
            group_record(group) for group in dense_dual_partition
        ],
        "records": records,
        "valid": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({key: value for key, value in result.items() if key != "records"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
