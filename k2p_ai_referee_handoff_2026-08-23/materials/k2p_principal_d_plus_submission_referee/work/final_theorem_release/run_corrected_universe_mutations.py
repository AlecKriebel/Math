#!/usr/bin/env python3
"""Fail-closed mutations for the unified five-family certificate."""

from __future__ import annotations

import argparse
import copy
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

from release_common import (
    HERE,
    PROJECT,
    corrected_locator,
    locator_artifacts,
    load_json,
    require,
    sha_file,
    sha_object,
)


CERTIFICATE = HERE / "corrected_universe_certificate.json"
VERIFIER = HERE / "verify_corrected_universe_independent.py"
DEFAULT_OUTPUT = HERE / "corrected_universe_mutation_report.json"


def qualified_python() -> str:
    candidate = PROJECT / ".venv/bin/python"
    return str(candidate if candidate.is_file() else Path(sys.executable))


def fingerprint() -> dict[str, str]:
    paths = locator_artifacts(corrected_locator())
    return {role: sha_file(path) for role, path in sorted(paths.items())}


def seal(certificate: dict[str, Any]) -> None:
    certificate.pop("payload_sha256", None)
    certificate["payload_sha256"] = sha_object(certificate)


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def set_zero_digest(container: dict[str, Any], field: str) -> None:
    container[field] = "0" * 64


def mutation_cases() -> list[tuple[str, Callable[[dict[str, Any]], None]]]:
    return [
        ("omitted_raw_row", lambda c: c["families"]["raw4"].__setitem__("input_count", c["families"]["raw4"]["input_count"] - 1)),
        ("false_rank_exclusion", lambda c: c["families"]["raw4"]["output_category_counts"].update({"exact_rank_exclusion": c["families"]["raw4"]["output_category_counts"]["exact_rank_exclusion"] + 1, "displayed_quartet_exclusion": c["families"]["raw4"]["output_category_counts"]["displayed_quartet_exclusion"] - 1})),
        ("missing_child", lambda c: c["families"]["restoration"]["generated_children"].__setitem__("count", c["families"]["restoration"]["generated_children"]["count"] - 1)),
        ("wrong_parent", lambda c: set_zero_digest(c["restoration_forest"], "class_parent_id_hash_root")),
        ("broken_transport", lambda c: set_zero_digest(c["restoration_forest"], "transport_restriction_hash_root")),
        ("reassigned_quadratic_certificate", lambda c: set_zero_digest(c["artifact_sha256"], "theta2_corrected_composite_summary")),
        ("reassigned_cubic_certificate", lambda c: set_zero_digest(c["artifact_sha256"], "raw4_terminal_certificate_registry")),
        ("reassigned_quartic_certificate", lambda c: c["artifact_sha256"].__setitem__("raw4_terminal_certificate_registry", "1" * 64)),
        ("reassigned_quintic_certificate", lambda c: c["artifact_sha256"].__setitem__("raw4_terminal_certificate_registry", "2" * 64)),
        ("raw4424_false_tree_sunlet_reintroduction", lambda c: c["families"]["raw4"].__setitem__("forbidden_rooted_reason_count", 1)),
        ("rooted_restriction_reintroduction", lambda c: c.__setitem__("rooted_reason_count", 1)),
        ("source_tree_write", lambda c: set_zero_digest(c, "source_tree_fingerprint_sha256")),
        ("omitted_probe_one_port_row", lambda c: c["probe_coherence"]["one_port"].__setitem__("raw_pair_count", c["probe_coherence"]["one_port"]["raw_pair_count"] - 1)),
        ("omitted_probe_two_port_parent", lambda c: c["probe_coherence"]["two_port"].__setitem__("parent_count", c["probe_coherence"]["two_port"]["parent_count"] - 1)),
        ("omitted_probe_two_port_row", lambda c: c["probe_coherence"]["two_port"].__setitem__("raw_pair_count", c["probe_coherence"]["two_port"]["raw_pair_count"] - 1)),
        ("wrong_probe_parent", lambda c: set_zero_digest(c["probe_coherence"]["two_port"], "parent_inventory_hash_root")),
        ("broken_probe_transport", lambda c: set_zero_digest(c["probe_coherence"], "transport_restriction_hash_root")),
        ("broken_probe_restriction", lambda c: set_zero_digest(c["probe_coherence"]["parent_restriction_registry"], "ordered_hash_root")),
        ("reassigned_probe_Ti_certificate", lambda c: set_zero_digest(c["probe_coherence"], "separation_registry_payload_sha256")),
        ("reversed_probe_order_class", lambda c: c["probe_coherence"]["two_port"].__setitem__("reversed_marginals_missing", 1)),
        ("inconsistent_probe_global_triangle", lambda c: c["probe_coherence"].__setitem__("incoherent", 1)),
    ]


def main() -> int:
    if not __debug__:
        raise SystemExit("CORRECTED_UNIVERSE_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    args = parser.parse_args()
    require(args.timeout_seconds > 0, "UNIFIED_MUTATION_TIMEOUT_FAIL")
    source = load_json(CERTIFICATE)
    before = fingerprint()
    results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="k2p-unified-mutations-") as directory:
        root = Path(directory)
        for ordinal, (name, mutate) in enumerate(mutation_cases()):
            candidate = copy.deepcopy(source)
            mutate(candidate)
            seal(candidate)
            path = root / f"{ordinal:02d}-{name}.json"
            output = root / f"{ordinal:02d}-{name}-replay.json"
            write_json(path, candidate)
            result = subprocess.run(
                [
                    qualified_python(),
                    "-B",
                    str(VERIFIER),
                    "--certificate",
                    str(path),
                    "--output",
                    str(output),
                ],
                cwd=PROJECT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=args.timeout_seconds,
                check=False,
            )
            combined = result.stdout + result.stderr
            require(result.returncode != 0, "UNIFIED_MUTATION_SURVIVED", name)
            require("CORRECTED_UNIVERSE_REPLAY_FAIL" in combined, "UNIFIED_MUTATION_WRONG_REJECTION", name)
            results.append({"name": name, "rejected": True, "returncode": result.returncode})
        optimized = subprocess.run(
            [qualified_python(), "-O", "-B", str(VERIFIER)],
            cwd=PROJECT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=args.timeout_seconds,
            check=False,
        )
        optimized_output = optimized.stdout + optimized.stderr
        require(optimized.returncode != 0, "UNIFIED_OPTIMIZED_MODE_SURVIVED")
        require("CORRECTED_UNIVERSE_REPLAY_OPTIMIZED_MODE_FORBIDDEN" in optimized_output, "UNIFIED_OPTIMIZED_MODE_WRONG_REJECTION")
        results.append({"name": "optimized_mode", "rejected": True, "returncode": optimized.returncode})
    after = fingerprint()
    require(before == after, "UNIFIED_MUTATION_SOURCE_TREE_DRIFT")
    report = {
        "schema": "k2p-corrected-finite-universe-mutations-v2",
        "status": "PASS",
        "source_certificate_sha256": sha_file(CERTIFICATE),
        "source_verifier_sha256": sha_file(VERIFIER),
        "temporary_copies_only": True,
        "test_count": len(results),
        "survivors": 0,
        "source_tree_drift": 0,
        "tests": results,
    }
    report["payload_sha256"] = sha_object(report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_json(args.output, report)
    print(json.dumps({"status": "PASS", "tests": len(results), "payload_sha256": report["payload_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        raise SystemExit(f"CORRECTED_UNIVERSE_MUTATIONS_FAIL:{error}") from error
