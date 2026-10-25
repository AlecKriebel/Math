#!/usr/bin/env python3
"""Fail-closed mutations for the cycle restoration package."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from cycle_common import (
    DEFAULT_ARTIFACT_ROOT,
    atomic_json,
    canonical_json_bytes,
    deterministic_gzip,
    read_json,
    sha_file,
    sha_object,
)


HERE = Path(__file__).resolve().parent
VERIFIER = HERE / "verify_cycle_closure.py"


def resign_summary(root: Path, name: str, metadata: dict | None = None) -> None:
    path = root / "cycle_three_port_summary.json"
    summary = read_json(path)
    if metadata is None:
        target = root / name
        metadata = {"sha256": sha_file(target), "bytes": target.stat().st_size}
    summary["artifacts"][name] = metadata
    summary.pop("payload_sha256", None)
    summary["payload_sha256"] = sha_object(summary)
    atomic_json(path, summary)


def rewrite_gzip(root: Path, name: str, mutation) -> None:
    source = root / name
    temporary_plain = root / f".{name}.rows.tmp"
    # Stream through deterministic_gzip without retaining the 229 MB plain
    # full ledger in memory.
    def rows():
        with gzip.open(source, "rb") as handle:
            for index, line in enumerate(handle):
                row = json.loads(line)
                replacement = mutation(index, row)
                if replacement is None:
                    continue
                yield canonical_json_bytes(replacement) + b"\n"

    metadata = deterministic_gzip(temporary_plain, rows())
    os.replace(temporary_plain, source)
    metadata["sha256"] = sha_file(source)
    resign_summary(root, name, metadata)


def mutate_json(root: Path, name: str, mutation) -> None:
    path = root / name
    payload = read_json(path)
    mutation(payload)
    atomic_json(path, payload)
    resign_summary(root, name)


def run_verifier(root: Path, optimized: bool = False) -> subprocess.CompletedProcess:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command += ["-B", str(VERIFIER), "--artifact-root", str(root)]
    environment = dict(os.environ)
    environment["PYTHONHASHSEED"] = "0"
    return subprocess.run(
        command,
        cwd=HERE.parents[1],
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=900,
    )


def expect_rejected(source: Path, name: str, mutate) -> dict:
    with tempfile.TemporaryDirectory(prefix=f"k2p_cycle_{name}_") as temporary:
        root = Path(temporary) / "artifacts"
        shutil.copytree(source, root)
        mutate(root)
        completed = run_verifier(root)
        if completed.returncode == 0:
            raise RuntimeError(f"mutation accepted: {name}")
        return {
            "name": name,
            "status": "REJECTED",
            "returncode": completed.returncode,
            "output_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(),
            "output_tail": completed.stdout.strip()[-240:],
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", type=Path, default=DEFAULT_ARTIFACT_ROOT)
    parser.add_argument("--output", type=Path, default=HERE / "mutation_certificate.json")
    args = parser.parse_args()
    source = args.artifact_root
    tests = []

    tests.append(
        expect_rejected(
            source,
            "omitted_base_raw_record",
            lambda root: rewrite_gzip(
                root,
                "base_raw_ledger.jsonl.gz",
                lambda index, row: None if index == 0 else row,
            ),
        )
    )

    def omit_role(root):
        def mutation(index, row):
            if index == 0:
                row["dummy_roles"] = row["dummy_roles"][1:]
            return row
        rewrite_gzip(root, "restoration_roots.jsonl.gz", mutation)

    tests.append(expect_rejected(source, "omitted_restoration_role", omit_role))

    def wrong_placement(root):
        def mutation(index, row):
            if index == 0:
                row["source_placement_path"][0] = 99
            return row
        rewrite_gzip(root, "full_completion_ledger.jsonl.gz", mutation)

    tests.append(expect_rejected(source, "wrong_source_placement", wrong_placement))

    def reassign_quadratic(root):
        def mutation(payload):
            keys = sorted(payload["certificates"])
            left, right = keys[0], keys[1]
            left_content = payload["certificates"][left]
            right_content = payload["certificates"][right]
            left_content["source_descriptor_sha256"] = right_content[
                "source_descriptor_sha256"
            ]
            left_content["target_descriptor_sha256"] = right_content[
                "target_descriptor_sha256"
            ]
        mutate_json(root, "quadratic_certificates.json", mutation)

    tests.append(expect_rejected(source, "reassigned_quadratic_certificate", reassign_quadratic))

    def break_transport(root):
        def mutation(payload):
            key = sorted(payload["certificates"])[0]
            mapping = payload["certificates"][key][
                "incidence_node_mapping_source_to_target"
            ]
            mapping[0][1] = "('mutated_target_node',)"
        mutate_json(root, "transport_certificates.json", mutation)

    tests.append(expect_rejected(source, "broken_transport_mapping", break_transport))

    optimized = run_verifier(source, optimized=True)
    if optimized.returncode != 0:
        raise RuntimeError(f"optimized replay failed: {optimized.stdout[-500:]}")
    tests.append(
        {
            "name": "python_optimized_mode_full_replay",
            "status": "PASS",
            "returncode": optimized.returncode,
            "output_sha256": hashlib.sha256(optimized.stdout.encode()).hexdigest(),
            "output_tail": optimized.stdout.strip()[-240:],
        }
    )

    report = {
        "schema": "k2p-cycle-three-port-mutation-suite-v1",
        "status": "PASS",
        "tests": tests,
        "rejected_mutations": 5,
        "optimized_full_replays": 1,
        "verifier_sha256": sha_file(VERIFIER),
        "artifact_summary_sha256": sha_file(source / "cycle_three_port_summary.json"),
    }
    report["payload_sha256"] = sha_object(report)
    atomic_json(args.output, report)
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
