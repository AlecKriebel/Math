#!/usr/bin/env python3
"""Run both independent graph verifiers over a graph6 catalog.

This is an orchestration layer only.  It deliberately invokes the existing
Python exhaustive-five-subset verifier and the independently implemented C++
recursive-bitset verifier as separate processes, then cross-checks their
outputs without importing either verification core.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path


CHECKER_ID = "ramsey55_catalog_dual_verifier_orchestrator_v1"
ROOT = Path(__file__).resolve().parents[1]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_json_stdout(completed: subprocess.CompletedProcess[str], label: str) -> dict:
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    if completed.returncode != 0:
        raise RuntimeError(
            f"{label} exited {completed.returncode}: {completed.stderr.strip()}"
        )
    if len(lines) != 1:
        raise RuntimeError(f"{label} did not emit exactly one JSON line")
    try:
        result = json.loads(lines[0])
    except json.JSONDecodeError as error:
        raise RuntimeError(f"{label} emitted invalid JSON: {error}") from error
    if not isinstance(result, dict):
        raise RuntimeError(f"{label} JSON is not an object")
    return result


def verify_one(
    index: int,
    graph6: str,
    catalog: Path,
    python_executable: Path,
    python_verifier: Path,
    cpp_verifier: Path,
) -> dict:
    line_number = index + 1
    python_run = subprocess.run(
        (
            str(python_executable),
            str(python_verifier),
            str(catalog),
            "--line",
            str(line_number),
            "--k",
            "5",
        ),
        check=False,
        capture_output=True,
        text=True,
    )
    python_result = parse_json_stdout(python_run, f"Python verifier line {line_number}")
    cpp_run = subprocess.run(
        (
            str(cpp_verifier),
            str(catalog),
            "--line",
            str(line_number),
            "--k",
            "5",
        ),
        check=False,
        capture_output=True,
        text=True,
    )
    cpp_result = parse_json_stdout(cpp_run, f"C++ verifier line {line_number}")

    valid = (
        python_result.get("valid") is True
        and python_result.get("n") == 42
        and python_result.get("clique_count") == 0
        and python_result.get("independent_count") == 0
        and cpp_result.get("valid") is True
        and cpp_result.get("n") == 42
        and cpp_result.get("clique_k_found") is False
        and cpp_result.get("independent_k_found") is False
        and cpp_result.get("edge_count") == python_result.get("edge_count")
        and cpp_result.get("degree_sequence") == python_result.get("degree_sequence")
    )
    return {
        "catalog_index_zero_based": index,
        "catalog_line_one_based": line_number,
        "graph6_sha256": sha256_bytes((graph6 + "\n").encode("ascii")),
        "edge_count": python_result.get("edge_count"),
        "degree_sequence": python_result.get("degree_sequence"),
        "python_clique_count": python_result.get("clique_count"),
        "python_independent_count": python_result.get("independent_count"),
        "cpp_clique_found": cpp_result.get("clique_k_found"),
        "cpp_independent_found": cpp_result.get("independent_k_found"),
        "valid": valid,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-count", type=int, default=328)
    parser.add_argument("--expected-sha256")
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--python", type=Path, default=Path(sys.executable))
    parser.add_argument(
        "--python-verifier",
        type=Path,
        default=ROOT / "verify" / "exhaustive_verify.py",
    )
    parser.add_argument(
        "--cpp-verifier",
        type=Path,
        default=ROOT / "build" / "bitset_verify",
    )
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error("--jobs must be positive")

    started = time.monotonic()
    catalog_bytes = args.catalog.read_bytes()
    catalog_sha256 = sha256_bytes(catalog_bytes)
    if args.expected_sha256 and catalog_sha256 != args.expected_sha256:
        raise SystemExit("catalog SHA-256 does not match --expected-sha256")
    try:
        text = catalog_bytes.decode("ascii")
    except UnicodeDecodeError as error:
        raise SystemExit(f"catalog is not ASCII: {error}") from error
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) != args.expected_count:
        raise SystemExit(
            f"catalog has {len(lines)} data lines, expected {args.expected_count}"
        )
    if len(set(lines)) != len(lines):
        raise SystemExit("catalog contains duplicate graph6 lines")
    for line_number, line in enumerate(lines, 1):
        if line.startswith("#") or line.startswith(">>"):
            raise SystemExit(f"unexpected non-data line {line_number}")

    results: list[dict | None] = [None] * len(lines)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = {
            executor.submit(
                verify_one,
                index,
                graph6,
                args.catalog,
                args.python,
                args.python_verifier,
                args.cpp_verifier,
            ): index
            for index, graph6 in enumerate(lines)
        }
        for future in concurrent.futures.as_completed(futures):
            index = futures[future]
            results[index] = future.result()

    checked = [entry for entry in results if entry is not None]
    valid_count = sum(entry["valid"] is True for entry in checked)
    edge_histogram: dict[str, int] = {}
    for entry in checked:
        key = str(entry["edge_count"])
        edge_histogram[key] = edge_histogram.get(key, 0) + 1
    output = {
        "checker": CHECKER_ID,
        "catalog_path": str(args.catalog),
        "catalog_sha256": catalog_sha256,
        "catalog_bytes": len(catalog_bytes),
        "graph_count": len(lines),
        "unique_graph6_count": len(set(lines)),
        "valid_count": valid_count,
        "invalid_count": len(lines) - valid_count,
        "all_valid": valid_count == len(lines),
        "edge_count_histogram": edge_histogram,
        "jobs": args.jobs,
        "python_executable": str(args.python),
        "python_verifier": str(args.python_verifier),
        "python_verifier_sha256": sha256_bytes(args.python_verifier.read_bytes()),
        "cpp_verifier": str(args.cpp_verifier),
        "cpp_verifier_sha256": sha256_bytes(args.cpp_verifier.read_bytes()),
        "runtime_seconds": time.monotonic() - started,
        "graphs": checked,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(output, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "checker": CHECKER_ID,
                "status": "PASS" if output["all_valid"] else "FAIL",
                "graph_count": len(lines),
                "valid_count": valid_count,
                "runtime_seconds": output["runtime_seconds"],
                "output": str(args.output),
            },
            sort_keys=True,
        )
    )
    return 0 if output["all_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
