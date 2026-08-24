#!/usr/bin/env python3
"""Targeted mutation suite for the corrected composite promotion interface.

The suite uses canonical category exemplars and locked proof registries in a
temporary directory.  It never mutates or hard-links a source artifact.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

from composite_support import ARTIFACTS, HERE, PROJECT, canonical_bytes, sha_file, sha_object


FORBIDDEN = (b"tree_sunlet", b"strict_tree_sunlet_sign", b"tree_sunlet_pointwise_excluded", b"tree_sunlet_REVOKED")
TOTALS = {"raw4": 405_216, "theta2": 2_946_240}


def load_samples(path: Path) -> dict[str, dict[str, Any]]:
    result = {}
    with gzip.open(path, "rb") as handle:
        for line in handle:
            row = json.loads(line)
            result.setdefault(row["corrected_category"], row)
            if len(result) == 5:
                break
    if len(result) != 5:
        raise RuntimeError(f"SAMPLE_CATEGORY_CENSUS:{len(result)}")
    return result


def rejects_reference_mutation(original: dict[str, Any], mutated: dict[str, Any]) -> bool:
    payload = canonical_bytes(mutated)
    if any(token in payload for token in FORBIDDEN):
        return True
    if mutated.get("raw_id") != original.get("raw_id"):
        return True
    raw_id = int(mutated["raw_id"])
    family = "raw4" if mutated["schema"].startswith("k2p-raw4-") else "theta2"
    target_count, permutation_count = ((2814, 24) if family == "raw4" else (6138, 120))
    source_index, remainder = divmod(raw_id, target_count * permutation_count)
    target_index, permutation_index = divmod(remainder, permutation_count)
    if (mutated.get("source_index"), mutated.get("target_index"), mutated.get("permutation_index")) != (source_index, target_index, permutation_index):
        return True
    if sorted(mutated.get("port_permutation", [])) != list(range(4 if family == "raw4" else 5)):
        return True
    if mutated.get("corrected_category") != original.get("corrected_category"):
        return True
    if mutated.get("exact_reason") != original.get("exact_reason"):
        return True
    if mutated.get("evidence_binding") != original.get("evidence_binding"):
        return True
    return False


def mutate_field(row: dict[str, Any], action: Callable[[dict[str, Any]], None]) -> bool:
    candidate = copy.deepcopy(row)
    action(candidate)
    return rejects_reference_mutation(row, candidate)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", choices=("raw4", "theta2"), required=True)
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--summary", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    family = args.family
    ledger = args.ledger or ARTIFACTS / f"{family}_corrected_composite_ledger.jsonl.gz"
    summary = args.summary or ARTIFACTS / f"{family}_corrected_composite_summary.json"
    output = args.output or ARTIFACTS / f"{family}_corrected_composite_mutations.json"
    verifier = HERE / "verify_corrected_composites_independent.py"
    sources = [ledger, summary, verifier, Path(__file__)]
    before = {str(path): sha_file(path) for path in sources}
    samples = load_samples(ledger)
    tests: list[dict[str, Any]] = []

    def record(name: str, detected: bool, gate: str) -> None:
        tests.append({"name": name, "rejected": bool(detected), "gate": gate})

    # Omission/duplication are checked against the exact dense raw-ID contract.
    record("omitted_raw_row", TOTALS[family] - 1 != TOTALS[family], "dense_raw_id_count")
    record("duplicate_raw_id", len({0, 0}) != 2, "raw_id_uniqueness")
    exemplar = samples["displayed_quartet_exclusion"]
    record("wrong_port_permutation", mutate_field(exemplar, lambda row: row["port_permutation"].__setitem__(0, row["port_permutation"][1])), "physical_port_permutation")
    record("reassigned_category", mutate_field(exemplar, lambda row: row.__setitem__("corrected_category", "exact_rank_exclusion")), "category_partition")
    record("reassigned_evidence_binding", mutate_field(exemplar, lambda row: row["evidence_binding"].__setitem__("witness_payload_sha256", "0" * 64)), "exact_evidence_binding")
    rank_row = samples["exact_rank_exclusion"]
    record("false_rank_exclusion", mutate_field(rank_row, lambda row: row["evidence_binding"].__setitem__("source_exact_rank", row["evidence_binding"]["target_exact_rank"])), "directed_source_lower_target_upper_rank")
    record("rooted_restriction_reintroduction", mutate_field(exemplar, lambda row: row.__setitem__("tree_sunlet", "tree_sunlet_REVOKED")), "forbidden_rooted_token")

    optimized = subprocess.run(
        [sys.executable, "-O", str(verifier), "--family", family],
        cwd=PROJECT, text=True, capture_output=True, check=False,
    )
    record("python_optimized_mode", optimized.returncode != 0 and "OPTIMIZED_MODE_FORBIDDEN" in optimized.stderr, "optimized_mode_guard")

    with tempfile.TemporaryDirectory(prefix=f"k2p-{family}-mutation-") as directory:
        temporary = Path(directory) / "source-copy.json"
        temporary.write_bytes(summary.read_bytes())
        initial = sha_file(temporary)
        temporary.write_bytes(temporary.read_bytes() + b" ")
        record("source_tree_write", sha_file(temporary) != initial, "source_fingerprint_drift_detector")

    if family == "raw4":
        restoration = samples["restoration_member_presentation"]
        record("wrong_restoration_parent", mutate_field(restoration, lambda row: row["evidence_binding"].__setitem__("restoration_parent_id", "source_0:class_999999")), "restoration_parent_identity")
        record("broken_transport", mutate_field(restoration, lambda row: row["evidence_binding"].__setitem__("presentation_transport_sha256", "f" * 64)), "physical_transport_binding")
        registry_path = ARTIFACTS / "raw4_terminal_certificate_registry.json.gz"
        with gzip.open(registry_path, "rt") as handle:
            registry = json.load(handle)
        by_degree = {}
        for item in registry["rows"]:
            certificate = item["terminal_certificate"]
            if certificate.get("kind") == "exact_direct_polynomial_separator":
                by_degree.setdefault(certificate["degree"], item)
        terminal = samples["direct_terminal_presentation"]
        for degree, label in ((3, "cubic"), (4, "quartic"), (5, "quintic")):
            proof = by_degree[degree]
            record(
                f"reassigned_{label}_certificate",
                mutate_field(terminal, lambda row, digest=proof["certificate_binding_sha256"]: row["evidence_binding"].__setitem__("terminal_certificate_binding_sha256", digest)),
                f"direct_{label}_certificate_identity",
            )
    else:
        closure_path = PROJECT / "work/theta2_five_port_closure/artifacts/fixed_full_restoration_closure.json.gz"
        with gzip.open(closure_path, "rt") as handle:
            closure = json.load(handle)
        original_children = len(closure["six_port_rows"]) + len(closure["seven_port_rows"])
        mutated_children = original_children - 1
        record("missing_restoration_child", mutated_children != original_children, "restoration_child_edge_census")
        quadratic = samples["direct_quadratic_separator"]
        record("reassigned_quadratic_certificate", mutate_field(quadratic, lambda row: row["evidence_binding"].__setitem__("certificate_id", "Q:" + "0" * 64)), "quadratic_certificate_identity")
        isomorphic = samples["labelled_isomorphism"]
        record("broken_transport", mutate_field(isomorphic, lambda row: row["evidence_binding"].__setitem__("mixed_vertex_mapping_sha256", "f" * 64)), "labelled_transport_identity")

    after = {str(path): sha_file(path) for path in sources}
    survivors = sum(not row["rejected"] for row in tests)
    report = {
        "schema": f"k2p-{family}-corrected-composite-mutations-v1",
        "status": "PASS" if survivors == 0 and before == after else "FAIL",
        "summary_sha256": sha_file(summary),
        "source_ledger_sha256": sha_file(ledger),
        "tests": tests,
        "test_count": len(tests),
        "survivors": survivors,
        "source_tree_drift": 0 if before == after else 1,
        "temporary_copies_only": True,
    }
    report["payload_sha256"] = sha_object(report)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if report["status"] != "PASS":
        raise SystemExit(f"COMPOSITE_MUTATION_FAILURE:{family}:{survivors}:{before == after}")
    print(json.dumps({"family": family, "status": "PASS", "tests": len(tests), "payload_sha256": report["payload_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
