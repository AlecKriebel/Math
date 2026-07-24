#!/usr/bin/env python3
"""Independently reconstruct and validate a delete-three/add-four SAT model."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import tempfile
from pathlib import Path
from typing import Sequence


CHECKER_ID = "ramsey55_delete3_add4_model_reconstruction_check_v1"
PIPELINE_ID = "ramsey55_pinned_glucose_streaming_zstd_lrat_pipeline_v1"
INPUT_ORDER = 42
CORE_ORDER = 39
ADDED_COUNT = 4
OUTPUT_ORDER = 43
VARIABLE_COUNT = 162


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
    bit_count = order * (order - 1) // 2
    payload_count = (bit_count + 5) // 6
    if order < 0 or order > 62 or len(text) != payload_count + 1:
        raise ValueError("not canonical short graph6")
    payload = [byte - 63 for byte in text[1:]]
    if any(value < 0 or value > 63 for value in payload):
        raise ValueError("invalid graph6 payload")
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


def encode_short_graph6(adjacency: Sequence[int]) -> bytes:
    bits = [
        (adjacency[left] >> right) & 1
        for right in range(1, len(adjacency))
        for left in range(right)
    ]
    while len(bits) % 6:
        bits.append(0)
    payload: list[int] = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        payload.append(value + 63)
    return bytes([len(adjacency) + 63, *payload]) + b"\n"


def induced_core(
    adjacency: Sequence[int], deleted: Sequence[int]
) -> tuple[list[int], tuple[int, ...]]:
    if len(adjacency) != INPUT_ORDER:
        raise ValueError("catalog graph is not order 42")
    retained = tuple(vertex for vertex in range(INPUT_ORDER) if vertex not in deleted)
    core = [0] * CORE_ORDER
    for new_left, old_left in enumerate(retained):
        for new_right in range(new_left + 1, CORE_ORDER):
            old_right = retained[new_right]
            if (adjacency[old_left] >> old_right) & 1:
                core[new_left] |= 1 << new_right
                core[new_right] |= 1 << new_left
    return core, retained


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


def variable_edge(variable: int) -> tuple[int, int]:
    if variable < 1 or variable > VARIABLE_COUNT:
        raise ValueError("model variable is outside 1..162")
    if variable <= ADDED_COUNT * CORE_ORDER:
        zero = variable - 1
        added_index, core_vertex = divmod(zero, CORE_ORDER)
        return core_vertex, CORE_ORDER + added_index
    pair_rank = variable - ADDED_COUNT * CORE_ORDER - 1
    pairs = tuple(itertools.combinations(range(ADDED_COUNT), 2))
    left, right = pairs[pair_rank]
    return CORE_ORDER + left, CORE_ORDER + right


def model_satisfies_cnf(
    path: Path, true_variables: set[int]
) -> tuple[int, int]:
    variable_count: int | None = None
    declared_clauses: int | None = None
    clauses = 0
    pending = False
    satisfied = False
    with path.open("r", encoding="ascii") as stream:
        for line_number, raw in enumerate(stream, start=1):
            fields = raw.split()
            if not fields or fields[0] == "c":
                continue
            if fields[0] == "p":
                if variable_count is not None or len(fields) != 4:
                    raise ValueError(f"bad DIMACS header at line {line_number}")
                if fields[1] != "cnf":
                    raise ValueError("DIMACS is not CNF")
                variable_count = int(fields[2])
                declared_clauses = int(fields[3])
                continue
            if variable_count is None:
                raise ValueError("clause precedes DIMACS header")
            for field in fields:
                literal = int(field)
                if literal == 0:
                    clauses += 1
                    if not pending or not satisfied:
                        raise ValueError(f"model falsifies clause {clauses}")
                    pending = False
                    satisfied = False
                else:
                    if abs(literal) < 1 or abs(literal) > variable_count:
                        raise ValueError("literal outside DIMACS variable range")
                    pending = True
                    satisfied = satisfied or (
                        (literal > 0) == (abs(literal) in true_variables)
                    )
    if (
        variable_count != VARIABLE_COUNT
        or declared_clauses is None
        or clauses != declared_clauses
        or pending
    ):
        raise ValueError("DIMACS counts or termination are invalid")
    return variable_count, clauses


def atomic_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=path.name + ".",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as stream:
            temporary = stream.name
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)


def verify(args: argparse.Namespace) -> tuple[dict, bytes]:
    deleted = parse_deleted(args.delete)
    catalog_record = selected_line(args.catalog, args.line)
    catalog_graph = decode_short_graph6(catalog_record)
    core, retained = induced_core(catalog_graph, deleted)
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    result = json.loads(args.solver_result.read_text(encoding="utf-8"))
    if not isinstance(metadata, dict) or not isinstance(result, dict):
        raise ValueError("metadata and solver result must be objects")
    if (
        result.get("pipeline") != PIPELINE_ID
        or result.get("status") != "SAT"
        or result.get("model_valid") is not True
        or result.get("cnf_sha256") != sha256(args.cnf)
    ):
        raise ValueError("solver result is not a matching pipeline SAT result")
    if (
        metadata.get("cnf_sha256") != sha256(args.cnf)
        or metadata.get("catalog_sha256") != sha256(args.catalog)
        or metadata.get("catalog_line") != args.line
        or metadata.get("deleted_original_labels") != list(deleted)
        or metadata.get("retained_original_labels") != list(retained)
        or metadata.get("variable_count") != VARIABLE_COUNT
    ):
        raise ValueError("CNF metadata bindings do not match reconstruction")
    true_list = result.get("true_variables")
    if (
        not isinstance(true_list, list)
        or any(type(value) is not int for value in true_list)
        or true_list != sorted(set(true_list))
        or any(value < 1 or value > VARIABLE_COUNT for value in true_list)
    ):
        raise ValueError("true-variable list is not canonical")
    worker = result.get("solver_result")
    if (
        not isinstance(worker, dict)
        or worker.get("true_variables") != true_list
        or worker.get("status") != "SAT"
        or worker.get("variable_count") != VARIABLE_COUNT
        or worker.get("cnf_sha256") != sha256(args.cnf)
    ):
        raise ValueError("nested SAT worker result is inconsistent")
    true_variables = set(true_list)
    _, clause_count = model_satisfies_cnf(args.cnf, true_variables)

    graph = list(core) + [0] * ADDED_COUNT
    for variable in true_variables:
        left, right = variable_edge(variable)
        graph[left] |= 1 << right
        graph[right] |= 1 << left
    counts = forbidden_counts(graph)
    if counts != (0, 0):
        raise ValueError(f"reconstructed graph has forbidden counts {counts}")
    graph6 = encode_short_graph6(graph)
    output = {
        "schema": "ramsey55.delete3_add4_model_reconstruction_check.v1",
        "checker": CHECKER_ID,
        "checker_source_sha256": sha256(Path(__file__)),
        "valid": True,
        "catalog_path": str(args.catalog.resolve()),
        "catalog_sha256": sha256(args.catalog),
        "catalog_line": args.line,
        "catalog_graph6_sha256": hashlib.sha256(catalog_record).hexdigest(),
        "deleted_original_labels": list(deleted),
        "retained_original_labels": list(retained),
        "cnf_path": str(args.cnf.resolve()),
        "cnf_sha256": sha256(args.cnf),
        "metadata_path": str(args.metadata.resolve()),
        "metadata_sha256": sha256(args.metadata),
        "solver_result_path": str(args.solver_result.resolve()),
        "solver_result_sha256": sha256(args.solver_result),
        "variable_count": VARIABLE_COUNT,
        "clause_count": clause_count,
        "true_variable_count": len(true_variables),
        "graph_order": OUTPUT_ORDER,
        "graph_edge_count": sum(value.bit_count() for value in graph) // 2,
        "graph_forbidden_counts": {"clique_5": 0, "independent_5": 0},
        "graph_path": str(args.graph_output.resolve()),
        "graph_sha256": hashlib.sha256(graph6).hexdigest(),
    }
    return output, graph6


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--line", type=int, required=True)
    parser.add_argument("--delete", required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--solver-result", type=Path, required=True)
    parser.add_argument("--graph-output", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.resolve() == args.graph_output.resolve():
        raise SystemExit("graph and checker result paths must differ")
    for output in (args.output, args.graph_output):
        if output.exists():
            raise SystemExit(f"refusing to overwrite {output}")
    try:
        result, graph6 = verify(args)
    except Exception as error:
        failure = {
            "schema": "ramsey55.delete3_add4_model_reconstruction_check.v1",
            "checker": CHECKER_ID,
            "checker_source_sha256": sha256(Path(__file__)),
            "valid": False,
            "error": f"{type(error).__name__}: {error}",
        }
        atomic_bytes(
            args.output,
            (json.dumps(failure, sort_keys=True, indent=2) + "\n").encode(),
        )
        print(json.dumps(failure, sort_keys=True))
        return 1
    atomic_bytes(args.graph_output, graph6)
    atomic_bytes(
        args.output,
        (json.dumps(result, sort_keys=True, indent=2) + "\n").encode(),
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
