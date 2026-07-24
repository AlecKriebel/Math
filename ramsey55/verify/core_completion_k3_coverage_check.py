#!/usr/bin/env python3
"""Independently check that a 43-vertex candidate lies in a fixed-core space."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import tempfile
from pathlib import Path
from typing import Sequence


CHECKER_ID = "ramsey55_delete3_add4_candidate_coverage_check_v1"
INPUT_ORDER = 42
OUTPUT_ORDER = 43


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def parse_deleted(text: str) -> tuple[int, int, int]:
    try:
        values = tuple(int(item) for item in text.split(","))
    except ValueError as error:
        raise ValueError("delete value is not an integer triple") from error
    if (
        len(values) != 3
        or values != tuple(sorted(set(values)))
        or any(value < 0 or value >= INPUT_ORDER for value in values)
    ):
        raise ValueError("delete value must be three increasing labels in 0..41")
    return values


def selected_line(path: Path, line_number: int) -> bytes:
    lines = [
        line.strip()
        for line in path.read_bytes().splitlines()
        if line.strip() and not line.lstrip().startswith(b"#")
    ]
    if line_number < 1 or line_number > len(lines):
        raise ValueError("catalog line is out of range")
    return lines[line_number - 1] + b"\n"


def decode_short_graph6(raw: bytes) -> list[int]:
    text = raw.strip()
    if text.startswith(b">>graph6<<"):
        text = text[len(b">>graph6<<") :]
    if not text:
        raise ValueError("empty graph6")
    order = text[0] - 63
    if order < 0 or order > 62:
        raise ValueError("not canonical short graph6")
    bit_count = order * (order - 1) // 2
    payload_count = (bit_count + 5) // 6
    if len(text) != payload_count + 1:
        raise ValueError("non-canonical graph6 length")
    payload = [byte - 63 for byte in text[1:]]
    if any(value < 0 or value > 63 for value in payload):
        raise ValueError("invalid graph6 payload byte")
    if bit_count % 6 and payload:
        unused = 6 - bit_count % 6
        if payload[-1] & ((1 << unused) - 1):
            raise ValueError("nonzero graph6 padding")
    adjacency = [0] * order
    bit_index = 0
    for right in range(1, order):
        for left in range(right):
            value = payload[bit_index // 6]
            bit = (value >> (5 - bit_index % 6)) & 1
            bit_index += 1
            if bit:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
    return adjacency


def forbidden_counts(adjacency: Sequence[int]) -> tuple[int, int]:
    cliques = 0
    independents = 0
    for vertices in itertools.combinations(range(len(adjacency)), 5):
        edge_count = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
        cliques += edge_count == 10
        independents += edge_count == 0
    return cliques, independents


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            prefix=path.name + ".",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as stream:
            temporary = stream.name
            json.dump(payload, stream, sort_keys=True, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)


def verify(args: argparse.Namespace) -> dict:
    deleted = parse_deleted(args.delete)
    catalog_record = selected_line(args.catalog, args.line)
    candidate_record = args.candidate.read_bytes()
    if not candidate_record.endswith(b"\n") or candidate_record.count(b"\n") != 1:
        raise ValueError("candidate must be exactly one newline-terminated record")
    catalog_graph = decode_short_graph6(catalog_record)
    candidate_graph = decode_short_graph6(candidate_record)
    if len(catalog_graph) != INPUT_ORDER:
        raise ValueError("catalog graph is not order 42")
    if len(candidate_graph) != OUTPUT_ORDER:
        raise ValueError("candidate graph is not order 43")

    retained = tuple(vertex for vertex in range(INPUT_ORDER) if vertex not in deleted)
    changed_old_pairs: list[list[int]] = []
    uncovered_changed_pairs: list[list[int]] = []
    checked_fixed_pairs = 0
    for left, right in itertools.combinations(range(INPUT_ORDER), 2):
        old_value = (catalog_graph[left] >> right) & 1
        new_value = (candidate_graph[left] >> right) & 1
        if left in retained and right in retained:
            checked_fixed_pairs += 1
            if old_value != new_value:
                uncovered_changed_pairs.append([left, right])
        if old_value != new_value:
            changed_old_pairs.append([left, right])
    if checked_fixed_pairs != 39 * 38 // 2:
        raise AssertionError("wrong fixed-pair coverage count")
    if uncovered_changed_pairs:
        raise ValueError(
            f"{len(uncovered_changed_pairs)} changed pairs escape deleted labels"
        )

    catalog_counts = forbidden_counts(catalog_graph)
    candidate_counts = forbidden_counts(candidate_graph)
    record = json.loads(args.candidate_record.read_text(encoding="utf-8"))
    if not isinstance(record, dict):
        raise ValueError("candidate result record is not an object")
    essential_record = {
        "status": "SEARCHED_INVALID_CANDIDATE",
        "catalog_line": args.line,
        "graph_path": str(args.candidate.resolve()),
        "graph_sha256": sha256(args.candidate),
        "C5": candidate_counts[0],
        "I5": candidate_counts[1],
        "E": sum(candidate_counts),
        "returncode": 0,
    }
    differing_record = sorted(
        key
        for key, expected in essential_record.items()
        if record.get(key) != expected
    )
    if differing_record:
        raise ValueError(f"candidate result differs on keys: {differing_record}")

    changed_incident_counts = {
        str(vertex): sum(vertex in pair for pair in changed_old_pairs)
        for vertex in deleted
    }
    return {
        "schema": "ramsey55.delete3_add4_candidate_coverage_check.v1",
        "checker": CHECKER_ID,
        "checker_source_sha256": sha256(Path(__file__)),
        "valid": True,
        "catalog_path": str(args.catalog.resolve()),
        "catalog_sha256": sha256(args.catalog),
        "catalog_line": args.line,
        "catalog_graph6_sha256": hashlib.sha256(catalog_record).hexdigest(),
        "catalog_forbidden_counts": {
            "clique_5": catalog_counts[0],
            "independent_5": catalog_counts[1],
        },
        "candidate_path": str(args.candidate.resolve()),
        "candidate_sha256": sha256(args.candidate),
        "candidate_result_path": str(args.candidate_record.resolve()),
        "candidate_result_sha256": sha256(args.candidate_record),
        "candidate_forbidden_counts": {
            "clique_5": candidate_counts[0],
            "independent_5": candidate_counts[1],
        },
        "deleted_original_labels": list(deleted),
        "retained_original_labels": list(retained),
        "fixed_pair_count": checked_fixed_pairs,
        "fixed_pairs_matching_catalog": checked_fixed_pairs,
        "uncovered_changed_pair_count": 0,
        "changed_catalog_pair_count": len(changed_old_pairs),
        "changed_catalog_pairs": changed_old_pairs,
        "changed_pair_incident_counts_by_deleted_label": changed_incident_counts,
        "new_vertex_label": 42,
        "new_vertex_pair_count": 42,
        "unknown_pair_count": 3 * 39 + 3 + 42,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--line", type=int, required=True)
    parser.add_argument("--delete", required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--candidate-record", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output is not None and args.output.exists():
        raise SystemExit(f"refusing to overwrite {args.output}")
    try:
        result = verify(args)
    except Exception as error:
        failure = {
            "schema": "ramsey55.delete3_add4_candidate_coverage_check.v1",
            "checker": CHECKER_ID,
            "checker_source_sha256": sha256(Path(__file__)),
            "valid": False,
            "error": f"{type(error).__name__}: {error}",
        }
        if args.output is not None:
            atomic_json(args.output, failure)
        print(json.dumps(failure, sort_keys=True))
        return 1
    if args.output is not None:
        atomic_json(args.output, result)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
