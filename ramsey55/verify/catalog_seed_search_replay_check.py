#!/usr/bin/env python3
"""Independently replay and summarize a preregistered catalog-seed search batch."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import statistics
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CHECKER_ID = "ramsey55_catalog_seed_search_independent_replay_v1"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def checked_json(data: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(data)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"{label} did not emit one JSON value") from error
    if not isinstance(value, dict):
        raise ValueError(f"{label} JSON root is not an object")
    return value


def normalized_search_json(text: str) -> tuple[dict[str, Any], str]:
    graph_marker = ',"graph6":"'
    output_marker = '","output":'
    if text.count(graph_marker) != 1:
        raise ValueError("search stdout does not contain exactly one graph6 field")
    start = text.index(graph_marker) + len(graph_marker)
    end = text.find(output_marker, start)
    if end < 0 or text.find(output_marker, end + 1) >= 0:
        raise ValueError("search stdout graph6/output boundary is ambiguous")
    raw_graph6 = text[start:end]
    if (
        not raw_graph6
        or '"' in raw_graph6
        or any(not 63 <= ord(character) <= 126 for character in raw_graph6)
    ):
        raise ValueError("search stdout graph6 bytes are invalid")
    normalized = (
        text[:start]
        + json.dumps(raw_graph6, ensure_ascii=True)[1:-1]
        + text[end:]
    )
    value = json.loads(normalized)
    if not isinstance(value, dict) or value.get("graph6") != raw_graph6:
        raise ValueError("normalized search stdout is inconsistent")
    return value, raw_graph6


def decode_short_graph6(raw: str) -> tuple[int, ...]:
    if not raw:
        raise ValueError("empty graph6")
    order = ord(raw[0]) - 63
    if order != 43:
        raise ValueError("expected a short order-43 graph6 record")
    bits: list[int] = []
    for character in raw[1:]:
        value = ord(character) - 63
        if not 0 <= value < 64:
            raise ValueError("invalid graph6 payload")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edge_count = order * (order - 1) // 2
    if len(bits) < edge_count or any(bits[edge_count:]):
        raise ValueError("truncated graph6 or nonzero graph6 padding")
    return tuple(bits[:edge_count])


def run_verifier(command: list[str], timeout: float) -> tuple[int, bytes, bytes]:
    completed = subprocess.run(
        command,
        capture_output=True,
        check=False,
        timeout=timeout,
    )
    return completed.returncode, completed.stdout, completed.stderr


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--verifier-time-limit", type=float, default=60.0)
    args = parser.parse_args()
    if args.jobs < 1 or args.verifier_time_limit <= 0:
        raise SystemExit("jobs and verifier time limit must be positive")
    if args.output.exists():
        raise SystemExit(f"refusing to overwrite {args.output}")

    plan = checked_json(args.plan.read_bytes(), "plan")
    summary = checked_json(args.summary.read_bytes(), "summary")
    if (
        plan.get("schema") != "ramsey55.catalog_seed_search_plan.v1"
        or plan.get("status") != "PREREGISTERED_BEFORE_EXECUTION"
    ):
        raise SystemExit("unexpected plan schema or status")
    for label in (
        "catalog",
        "search",
        "exhaustive_verifier",
        "bitset_verifier",
        "runner",
        "selected_lines",
    ):
        record = plan.get(label)
        if not isinstance(record, dict):
            raise SystemExit(f"missing plan record {label}")
        path = ROOT / str(record.get("path"))
        if not path.is_file() or sha256_file(path) != record.get("sha256"):
            raise SystemExit(f"plan path/hash mismatch for {label}")

    lines_path = ROOT / str(plan["selected_lines"]["path"])
    lines = [
        int(line)
        for line in lines_path.read_text(encoding="ascii").splitlines()
        if line.strip()
    ]
    if (
        lines != sorted(set(lines))
        or len(lines) != plan["selected_lines"].get("count")
        or not lines
    ):
        raise SystemExit("selected-line coverage is malformed")
    expected_names = {
        f"line_{line:03d}{suffix}"
        for line in lines
        for suffix in (".g6", ".result.json")
    }
    actual_names = {
        path.name for path in args.output_dir.iterdir() if path.is_file()
    }
    if actual_names != expected_names:
        raise SystemExit("batch output file set is not exact")

    exhaustive = ROOT / str(plan["exhaustive_verifier"]["path"])
    bitset = ROOT / str(plan["bitset_verifier"]["path"])
    seed_base = int(plan["configuration"]["seed_base"])

    def replay(line: int) -> tuple[dict[str, Any], tuple[int, ...], str]:
        graph = args.output_dir / f"line_{line:03d}.g6"
        record_path = args.output_dir / f"line_{line:03d}.result.json"
        graph_bytes = graph.read_bytes()
        raw_graph6 = graph_bytes.decode("ascii").removesuffix("\n")
        if graph_bytes != (raw_graph6 + "\n").encode("ascii"):
            raise ValueError(f"line {line} graph is not one exact graph6 line")
        graph_sha256 = sha256_bytes(graph_bytes)
        record = checked_json(record_path.read_bytes(), f"record {line}")
        search, stdout_graph6 = normalized_search_json(str(record.get("stdout")))
        if (
            record.get("catalog_line") != line
            or record.get("seed") != seed_base + line
            or record.get("status") != "SEARCHED_INVALID_CANDIDATE"
            or record.get("returncode") != 0
            or record.get("graph_sha256") != graph_sha256
            or stdout_graph6 != raw_graph6
            or search.get("seed") != seed_base + line
            or search.get("seed_line") != line
            or search.get("E") != record.get("E")
            or search.get("C5") != record.get("C5")
            or search.get("I5") != record.get("I5")
            or record.get("E") != record.get("C5") + record.get("I5")
        ):
            raise ValueError(f"line {line} record/search binding failed")

        python_code, python_stdout, python_stderr = run_verifier(
            [sys.executable, str(exhaustive), str(graph)],
            args.verifier_time_limit,
        )
        bitset_code, bitset_stdout, bitset_stderr = run_verifier(
            [str(bitset), str(graph)],
            args.verifier_time_limit,
        )
        python_result = checked_json(python_stdout, f"Python verifier {line}")
        bitset_result = checked_json(bitset_stdout, f"bitset verifier {line}")
        if (
            python_code != 1
            or bitset_code != 1
            or python_stderr
            or bitset_stderr
            or python_result.get("input_sha256") != graph_sha256
            or python_result.get("n") != 43
            or python_result.get("k") != 5
            or python_result.get("clique_count") != record.get("C5")
            or python_result.get("independent_count") != record.get("I5")
            or python_result.get("objective") != record.get("E")
            or python_result.get("valid") is not False
            or bitset_result.get("n") != 43
            or bitset_result.get("k") != 5
            or bitset_result.get("clique_k_found")
            != (record.get("C5") > 0)
            or bitset_result.get("independent_k_found")
            != (record.get("I5") > 0)
            or bitset_result.get("valid") is not False
            or python_result.get("edge_count")
            != bitset_result.get("edge_count")
            or python_result.get("edge_count") != record.get("edge_count")
            or python_result.get("degree_sequence")
            != bitset_result.get("degree_sequence")
            or python_result.get("degree_sequence")
            != search.get("degree_sequence")
        ):
            raise ValueError(f"line {line} independent verifier replay failed")
        manifest = {
            "line": line,
            "graph_sha256": graph_sha256,
            "record_sha256": sha256_file(record_path),
            "python_result_sha256": sha256_bytes(python_stdout),
            "bitset_result_sha256": sha256_bytes(bitset_stdout),
            "C5": record["C5"],
            "I5": record["I5"],
            "E": record["E"],
            "edge_count": record["edge_count"],
        }
        return manifest, decode_short_graph6(raw_graph6), raw_graph6

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
        replayed = list(executor.map(replay, lines))
    manifests = [record for record, _, _ in replayed]
    bit_vectors = [bits for _, bits, _ in replayed]
    raw_graphs = [raw for _, _, raw in replayed]
    distances = [
        sum(left != right for left, right in zip(bit_vectors[i], bit_vectors[j]))
        for i in range(len(bit_vectors))
        for j in range(i + 1, len(bit_vectors))
    ]
    status_counts = {"SEARCHED_INVALID_CANDIDATE": len(lines)}
    configuration = plan["configuration"]
    if (
        summary.get("schema") != "ramsey55.catalog_seed_search_batch.v1"
        or summary.get("status") != "COMPLETE_NO_CONSTRUCTION"
        or summary.get("plan_sha256") != sha256_file(args.plan)
        or summary.get("record_count") != len(lines)
        or summary.get("requested_count") != len(lines)
        or summary.get("searched_lines") != lines
        or summary.get("best_E") != min(record["E"] for record in manifests)
        or summary.get("best_lines") != lines
        or summary.get("status_counts") != status_counts
        or summary.get("exact_line_coverage") is not True
        or summary.get("exact_record_coverage") is not True
        or any(
            summary.get("configuration", {}).get(key) != value
            for key, value in configuration.items()
        )
    ):
        raise SystemExit("summary/plan/record aggregate binding failed")

    manifest_text = "".join(
        (
            f"{record['line']} {record['graph_sha256']} {record['record_sha256']} "
            f"{record['python_result_sha256']} {record['bitset_result_sha256']}\n"
        )
        for record in manifests
    ).encode("ascii")
    distributions: dict[str, int] = {}
    for record in manifests:
        key = f"C5={record['C5']},I5={record['I5']}"
        distributions[key] = distributions.get(key, 0) + 1
    result = {
        "checker": CHECKER_ID,
        "status": "PASS",
        "checker_source_sha256": sha256_file(Path(__file__)),
        "plan_path": str(args.plan.resolve()),
        "plan_sha256": sha256_file(args.plan),
        "summary_path": str(args.summary.resolve()),
        "summary_sha256": sha256_file(args.summary),
        "catalog_sha256": plan["catalog"]["sha256"],
        "runner_sha256": plan["runner"]["sha256"],
        "search_sha256": plan["search"]["sha256"],
        "python_verifier_sha256": plan["exhaustive_verifier"]["sha256"],
        "bitset_verifier_sha256": plan["bitset_verifier"]["sha256"],
        "selected_lines_sha256": plan["selected_lines"]["sha256"],
        "checked_graph_count": len(manifests),
        "python_exact_replay_count": len(manifests),
        "bitset_replay_count": len(manifests),
        "objective_distribution": distributions,
        "raw_graph6_unique_count": len(set(raw_graphs)),
        "graph_sha256_unique_count": len(
            {record["graph_sha256"] for record in manifests}
        ),
        "pairwise_labeled_edge_hamming": {
            "edge_dimension": 903,
            "pair_count": len(distances),
            "minimum": min(distances),
            "median": statistics.median(distances),
            "mean": statistics.fmean(distances),
            "maximum": max(distances),
        },
        "edge_count_range": {
            "minimum": min(record["edge_count"] for record in manifests),
            "maximum": max(record["edge_count"] for record in manifests),
        },
        "verifier_manifest_sha256": sha256_bytes(manifest_text),
        "records": manifests,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
