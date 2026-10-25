#!/usr/bin/env python3
"""Adversarial mutations for the theta2 five-port closure verifier."""

from __future__ import annotations

import argparse
import copy
import gzip
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import verify_theta2_ledger as verifier
from theta2_common import ARTIFACT_ROOT, atomic_json, fail


def expect_rejected(name, function, expected_prefix: str):
    try:
        function()
    except SystemExit as exc:
        message = str(exc)
        if not message.startswith(expected_prefix):
            fail("THETA2_MUTATION_WRONG_FAILURE", (name, message))
        print(f"THETA2_MUTATION_REJECTED name={name} reason={message}")
        return
    fail("THETA2_MUTATION_SURVIVED", name)


def mutate_raw_ledger(source: Path, target: Path, mode: str):
    """Create a pure one-row omission or duplication while preserving all others."""
    with gzip.open(source, "rb") as incoming:
        with target.open("wb") as raw:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as outgoing:
                for ordinal, line in enumerate(incoming):
                    if ordinal == 17 and mode == "omit":
                        continue
                    outgoing.write(line)
                    if ordinal == 17 and mode == "duplicate":
                        outgoing.write(line)


def optimized_mode_rejected(script: Path) -> bool:
    environment = dict(os.environ)
    environment["PYTHONOPTIMIZE"] = "1"
    result = subprocess.run(
        [sys.executable, "-O", "-B", str(script), "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=environment,
        check=False,
    )
    return result.returncode != 0 and b"OPTIMIZED_MODE_FORBIDDEN" in (
        result.stdout + result.stderr
    )


def main() -> None:
    if not __debug__:
        fail("THETA2_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", type=Path, default=ARTIFACT_ROOT)
    parser.add_argument(
        "--report",
        type=Path,
        default=ARTIFACT_ROOT / "mutation_report.json",
    )
    args = parser.parse_args()
    artifact_root = args.artifact_root.resolve()

    rank_payload = verifier.read_gzip_json(
        artifact_root / "exact_rank_certificates.json.gz"
    )
    proof_payload = verifier.read_gzip_json(
        artifact_root / "direct_proof_certificates.json.gz"
    )
    class_payload = verifier.read_gzip_json(
        artifact_root / "class_partition.json.gz"
    )
    restoration_payload = verifier.read_gzip_json(
        artifact_root / "fixed_full_restoration_closure.json.gz"
    )
    rank_catalog = verifier.validate_rank_payload(rank_payload)
    topology, quadratics, isomorphisms, anchors = verifier.validate_proof_payload(
        proof_payload
    )
    classes = verifier.validate_classes(
        class_payload, rank_catalog, quadratics, isomorphisms, anchors
    )
    verifier.validate_restoration_payload(
        restoration_payload, class_payload, classes
    )

    def wrong_legacy_compiler_binding():
        mutated = copy.deepcopy(rank_payload)
        mutated["compiler_sha256"] = "0" * 64
        verifier.validate_rank_payload(mutated)

    expect_rejected(
        "wrong_legacy_compiler_binding",
        wrong_legacy_compiler_binding,
        "THETA2_RANK_LEGACY_COMPILER_BINDING_FAIL",
    )

    def wrong_legacy_canonicalizer_binding():
        mutated = copy.deepcopy(restoration_payload)
        mutated["bindings"]["canonicalizer_sha256"] = "0" * 64
        verifier.validate_restoration_payload(mutated, class_payload, classes)

    expect_rejected(
        "wrong_legacy_canonicalizer_binding",
        wrong_legacy_canonicalizer_binding,
        "THETA2_RESTORATION_LEGACY_CANONICALIZER_BINDING_FAIL",
    )

    def corrupt_topology_witness():
        mutated = copy.deepcopy(proof_payload)
        identifier = next(iter(mutated["topology_witnesses"]))
        mutated["topology_witnesses"][identifier]["zero_on"] = "target"
        verifier.validate_proof_payload(mutated)

    expect_rejected(
        "topology_witness_corruption",
        corrupt_topology_witness,
        "THETA2_TOPOLOGY_WITNESS_ID_FAIL",
    )

    def false_rank_exclusion():
        mutated = copy.deepcopy(class_payload)
        row = next(row for row in mutated["classes"] if row["category"] == "isomorphic")
        row["category"] = "rank_excluded"
        row["certificate_id"] = f"R:{row['target_descriptor_sha256']}"
        verifier.validate_classes(
            mutated, rank_catalog, quadratics, isomorphisms, anchors
        )

    expect_rejected(
        "false_rank_exclusion",
        false_rank_exclusion,
        "THETA2_FALSE_RANK_EXCLUSION",
    )

    def retained_class_reassignment():
        mutated = copy.deepcopy(class_payload)
        rows = [row for row in mutated["classes"] if row["category"] == "quadratic_separated"]
        rows[0]["certificate_id"], rows[1]["certificate_id"] = (
            rows[1]["certificate_id"],
            rows[0]["certificate_id"],
        )
        verifier.validate_classes(
            mutated, rank_catalog, quadratics, isomorphisms, anchors
        )

    expect_rejected(
        "retained_class_reassignment",
        retained_class_reassignment,
        "THETA2_CLASS_QUADRATIC_REFERENCE_FAIL",
    )

    def quadratic_coefficient_corruption():
        mutated = copy.deepcopy(proof_payload)
        identifier = next(iter(mutated["quadratic_certificates"]))
        mutated["quadratic_certificates"][identifier]["coefficients"][0] += 1
        verifier.validate_proof_payload(mutated)

    expect_rejected(
        "quadratic_coefficient_corruption",
        quadratic_coefficient_corruption,
        "THETA2_QUADRATIC_CERTIFICATE_SHAPE_FAIL",
    )

    def isomorphism_mapping_corruption():
        mutated = copy.deepcopy(proof_payload)
        identifier = next(iter(mutated["isomorphism_certificates"]))
        mutated["isomorphism_certificates"][identifier][
            "mixed_vertex_mapping_source_to_target"
        ][0][1] += "_mutated"
        verifier.validate_proof_payload(mutated)

    expect_rejected(
        "isomorphism_mapping_corruption",
        isomorphism_mapping_corruption,
        "THETA2_ISOMORPHISM_CERTIFICATE_SHAPE_FAIL",
    )

    def anchor_omission():
        mutated = copy.deepcopy(proof_payload)
        mutated["isomorphic_terminal_anchors"].pop()
        verifier.validate_proof_payload(mutated)

    expect_rejected(
        "isomorphic_anchor_omission",
        anchor_omission,
        "THETA2_ISOMORPHIC_ANCHOR_CENSUS_FAIL",
    )

    def restoration_root_omission():
        mutated = copy.deepcopy(restoration_payload)
        mutated["restoration_roots"].pop()
        verifier.validate_restoration_payload(mutated, class_payload, classes)

    expect_rejected(
        "restoration_root_omission",
        restoration_root_omission,
        "THETA2_RESTORATION_COLLECTION_SHAPE_FAIL",
    )

    def six_port_row_duplication():
        mutated = copy.deepcopy(restoration_payload)
        mutated["six_port_rows"].append(
            copy.deepcopy(mutated["six_port_rows"][0])
        )
        verifier.validate_restoration_payload(mutated, class_payload, classes)

    expect_rejected(
        "six_port_row_duplication",
        six_port_row_duplication,
        "THETA2_RESTORATION_COLLECTION_SHAPE_FAIL",
    )

    def seven_port_row_omission():
        mutated = copy.deepcopy(restoration_payload)
        mutated["seven_port_rows"].pop()
        verifier.validate_restoration_payload(mutated, class_payload, classes)

    expect_rejected(
        "seven_port_row_omission",
        seven_port_row_omission,
        "THETA2_RESTORATION_COLLECTION_SHAPE_FAIL",
    )

    def restoration_false_isomorphism():
        mutated = copy.deepcopy(restoration_payload)
        row = next(
            row
            for row in mutated["six_port_rows"]
            if row["category"] == "quartet_pointwise_excluded"
        )
        valid = next(iter(mutated["isomorphism_certificates"]))
        row["category"] = "isomorphic"
        row["certificate_id"] = valid
        verifier.validate_restoration_payload(mutated, class_payload, classes)

    expect_rejected(
        "restoration_false_isomorphism",
        restoration_false_isomorphism,
        "THETA2_RESTORATION_FIRST_ISOMORPHISM_REFERENCE_FAIL",
    )

    def restoration_mapping_corruption():
        mutated = copy.deepcopy(restoration_payload)
        identifier = next(iter(mutated["isomorphism_certificates"]))
        mutated["isomorphism_certificates"][identifier][
            "mixed_vertex_mapping_source_to_target"
        ][0][1] += "_mutated"
        verifier.validate_restoration_payload(mutated, class_payload, classes)

    expect_rejected(
        "restoration_mapping_corruption",
        restoration_mapping_corruption,
        "THETA2_RESTORATION_ISOMORPHISM_CERTIFICATE_FAIL",
    )

    def restoration_role_drift():
        mutated = copy.deepcopy(restoration_payload)
        mutated["restoration_roots"][0]["dummy_roles"][0] += "_mutated"
        verifier.validate_restoration_payload(mutated, class_payload, classes)

    expect_rejected(
        "restoration_role_drift",
        restoration_role_drift,
        "THETA2_RESTORATION_ANCHOR_ID_FAIL",
    )

    with tempfile.TemporaryDirectory(prefix="k2p_theta2_mutations_") as temporary:
        temporary_root = Path(temporary)
        original_ledger = artifact_root / "raw_directional_ledger.jsonl.gz"
        for mode, expected in (
            ("omit", "THETA2_LEDGER_RAW_COORDINATE_FAIL"),
            ("duplicate", "THETA2_LEDGER_RAW_COORDINATE_FAIL"),
        ):
            mutated_path = temporary_root / f"raw_{mode}.jsonl.gz"
            mutate_raw_ledger(original_ledger, mutated_path, mode)
            expect_rejected(
                f"raw_row_{mode}",
                lambda path=mutated_path: verifier.validate_ledger(
                    path, classes, topology
                ),
                expected,
            )

    for script_name in (
        "generate_theta2_ledger.py",
        "verify_theta2_ledger.py",
    ):
        script = Path(__file__).with_name(script_name)
        if not optimized_mode_rejected(script):
            fail("THETA2_OPTIMIZED_MODE_MUTATION_SURVIVED", script_name)
        print(f"THETA2_MUTATION_REJECTED name=optimized_mode:{script_name}")

    report = {
        "schema": "k2p-theta2-five-port-mutation-report-v1",
        "status": "PASS",
        "mutations_rejected": 18,
        "survivors": 0,
        "tests": [
            "wrong_legacy_compiler_binding",
            "wrong_legacy_canonicalizer_binding",
            "topology_witness_corruption",
            "false_rank_exclusion",
            "retained_class_reassignment",
            "quadratic_coefficient_corruption",
            "isomorphism_mapping_corruption",
            "isomorphic_anchor_omission",
            "restoration_root_omission",
            "six_port_row_duplication",
            "seven_port_row_omission",
            "restoration_false_isomorphism",
            "restoration_mapping_corruption",
            "restoration_role_drift",
            "raw_row_omit",
            "raw_row_duplicate",
            "optimized_mode:generate_theta2_ledger.py",
            "optimized_mode:verify_theta2_ledger.py",
        ],
    }
    print("THETA2_MUTATION_SUITE_PASS rejected=18 survivors=0")
    atomic_json(args.report.resolve(), report)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
