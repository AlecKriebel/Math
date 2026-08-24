#!/usr/bin/env python3
"""Targeted fail-closed mutation tests for the compressed release verifier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable

import verify_compressed_release as verifier


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "results/COMPRESSION_MUTATION_RESULT.json"


class MutationFailure(RuntimeError):
    pass


def need(condition: bool, code: str, detail: Any | None = None) -> None:
    if not condition:
        raise MutationFailure(code if detail is None else f"{code}:{detail}")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def reseal(value: dict[str, Any]) -> None:
    value.pop("payload_sha256", None)
    value["payload_sha256"] = object_sha(value)


def seal(payload: dict[str, Any]) -> dict[str, Any]:
    need("payload_sha256" not in payload, "ALREADY_SEALED")
    return {**payload, "payload_sha256": object_sha(payload)}


def omitted_raw_record(bundle: dict[str, dict[str, Any]]) -> None:
    raw4 = bundle["baseline"]["finite_universes"]["raw4"]
    raw4["rows"] -= 1
    raw4["category_counts"]["displayed_quartet_exclusion"] -= 1
    reseal(bundle["baseline"])


def false_rank_exclusion(bundle: dict[str, dict[str, Any]]) -> None:
    categories = bundle["baseline"]["finite_universes"]["raw4"]["category_counts"]
    categories["exact_rank_exclusion"] += 1
    categories["displayed_quartet_exclusion"] -= 1
    reseal(bundle["baseline"])


def missing_restoration_child(bundle: dict[str, dict[str, Any]]) -> None:
    bundle["restoration"]["census"]["first_children"] -= 1
    reseal(bundle["restoration"])


def wrong_restoration_parent(bundle: dict[str, dict[str, Any]]) -> None:
    bundle["restoration"]["coverage"]["canonical_parent_assignment_sha256"] = "0" * 64
    reseal(bundle["restoration"])


def broken_probe_transport(bundle: dict[str, dict[str, Any]]) -> None:
    transport = bundle["probe"]["transport_coherence"]
    transport["exact_transport_records"] -= 1
    transport["missing_exact_transports"] = 1
    reseal(bundle["probe"])


def cubic_reassigned_as_quartic(bundle: dict[str, dict[str, Any]]) -> None:
    bundle["templates"]["direct36"]["base_formulas"]["theta3_cubic"]["degree"] = 4
    reseal(bundle["templates"])


def quartic_reassigned_as_quintic(bundle: dict[str, dict[str, Any]]) -> None:
    bundle["templates"]["direct36"]["base_formulas"]["lower_theta_quartics"]["degree"] = 5
    reseal(bundle["templates"])


def quintic_reassigned_as_cubic(bundle: dict[str, dict[str, Any]]) -> None:
    bundle["templates"]["direct36"]["base_formulas"]["theta0_quintic"]["degree"] = 3
    reseal(bundle["templates"])


def swapped_high_degree_family_assignments(bundle: dict[str, dict[str, Any]]) -> None:
    counts = bundle["templates"]["direct36"]["family_record_counts"]
    counts["theta0_quintic_port_orbit"] = 21
    counts["lower_theta_quartic"] = 13
    reseal(bundle["templates"])


def promoted_partial_result(bundle: dict[str, dict[str, Any]]) -> None:
    bundle["result"]["status"] = "PC-COMPLETE"
    reseal(bundle["result"])


MUTATIONS: tuple[tuple[str, Callable[[dict[str, dict[str, Any]]], None], str], ...] = (
    ("omitted_raw_record", omitted_raw_record, "RAW4_ROWS"),
    ("false_rank_exclusion", false_rank_exclusion, "RAW4_CATEGORY_CENSUS"),
    ("missing_restoration_child", missing_restoration_child, "RESTORATION_CENSUS"),
    ("wrong_restoration_parent", wrong_restoration_parent, "RESTORATION_PARENT_ASSIGNMENT_ROOT"),
    ("broken_probe_transport", broken_probe_transport, "PROBE_TRANSPORT_CENSUS"),
    ("cubic_reassigned_as_quartic", cubic_reassigned_as_quartic, "DIRECT36_CUBIC_DEGREE"),
    ("quartic_reassigned_as_quintic", quartic_reassigned_as_quintic, "DIRECT36_QUARTIC_DEGREE"),
    ("quintic_reassigned_as_cubic", quintic_reassigned_as_cubic, "DIRECT36_QUINTIC_DEGREE"),
    ("swapped_high_degree_family_assignments", swapped_high_degree_family_assignments, "DIRECT36_FAMILY_COUNTS"),
    ("promoted_partial_result", promoted_partial_result, "RESULT_STATUS"),
)


def run_mutation(
    pristine: dict[str, dict[str, Any]],
    name: str,
    mutate: Callable[[dict[str, dict[str, Any]]], None],
    expected_code: str,
) -> dict[str, Any]:
    candidate = copy.deepcopy(pristine)
    mutate(candidate)
    observed: str | None = None
    try:
        verifier.verify_bundle(
            candidate,
            enforce_expected_payloads=False,
            verify_files=False,
        )
    except verifier.VerificationFailure as error:
        observed = str(error).split(":", 1)[0]
    need(observed is not None, "MUTATION_ACCEPTED", name)
    need(observed == expected_code, "MUTATION_WRONG_FAILURE", f"{name}:{observed}")
    return {
        "mutation_id": name,
        "expected_failure_code": expected_code,
        "observed_failure_code": observed,
        "status": "REJECTED_AS_REQUIRED",
    }


def optimized_mode_mutation() -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, "-O", str(ROOT / "verify_compressed_release.py"), "--check"],
        cwd=ROOT.parent,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    need(completed.returncode != 0, "OPTIMIZED_MODE_ACCEPTED")
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    need(bool(lines), "OPTIMIZED_MODE_EMPTY_STDOUT")
    report = json.loads(lines[-1])
    need(isinstance(report, dict), "OPTIMIZED_MODE_REPORT")
    need(report.get("status") == "FAIL", "OPTIMIZED_MODE_STATUS")
    need(report.get("error") == "OPTIMIZED_PYTHON_FORBIDDEN", "OPTIMIZED_MODE_ERROR")
    return {
        "mutation_id": "optimized_python",
        "expected_failure_code": "OPTIMIZED_PYTHON_FORBIDDEN",
        "observed_failure_code": report["error"],
        "status": "REJECTED_AS_REQUIRED",
    }


def build_result() -> tuple[dict[str, Any], float]:
    started = time.perf_counter()
    pristine = verifier.load_bundle()
    verifier.verify_bundle(pristine)
    rows = [run_mutation(pristine, *mutation) for mutation in MUTATIONS]
    rows.append(optimized_mode_mutation())
    elapsed = time.perf_counter() - started
    result = seal(
        {
            "schema": "k2p-pc-partial-compression-mutation-result-v1",
            "status": "PASS",
            "base_verifier_status": "PASS",
            "mutations": rows,
            "accepted_mutations": 0,
            "rejected_mutations": len(rows),
            "target_families": [
                "omitted raw records",
                "false rank exclusions",
                "missing restoration children",
                "wrong restoration parents",
                "broken probe transports",
                "reassigned cubic/quartic/quintic certificates",
                "improper PC-PARTIAL promotion",
                "optimized Python",
            ],
        }
    )
    return result, elapsed


def load_existing() -> dict[str, Any]:
    need(OUTPUT.is_file() and not OUTPUT.is_symlink(), "RESULT_MISSING")
    value = json.loads(OUTPUT.read_text(encoding="utf-8"))
    need(isinstance(value, dict), "RESULT_NOT_OBJECT")
    observed = value.get("payload_sha256")
    payload = dict(value)
    payload.pop("payload_sha256", None)
    need(observed == object_sha(payload), "RESULT_SEAL")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    need(__debug__ and sys.flags.optimize == 0, "OPTIMIZED_PYTHON_FORBIDDEN")
    args = parse_args()
    result, elapsed = build_result()
    if args.write:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(
            json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    else:
        need(load_existing() == result, "RESULT_REPLAY_MISMATCH")
    print(
        json.dumps(
            {
                "mutations": len(result["mutations"]),
                "payload_sha256": result["payload_sha256"],
                "runtime_seconds": round(elapsed, 3),
                "status": "PASS",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (MutationFailure, json.JSONDecodeError) as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}, sort_keys=True))
        raise SystemExit(1)
