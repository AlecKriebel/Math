#!/usr/bin/env python3
"""Run the final-theorem release composite validator on the local package."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from composite_support import ARTIFACTS, HERE, PROJECT, sha_file, sha_object


def main() -> None:
    release_path = PROJECT / "work/final_theorem_release/release_common.py"
    spec = importlib.util.spec_from_file_location("composite_release_contract", release_path)
    if spec is None or spec.loader is None:
        raise SystemExit("RELEASE_COMMON_IMPORT_FAIL")
    release = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = release
    spec.loader.exec_module(release)
    paths = {
        "corrected_composite_generator": HERE / "generate_corrected_composites.py",
        "corrected_composite_independent_verifier": HERE / "verify_corrected_composites_independent.py",
        "corrected_composite_mutation_runner": HERE / "run_composite_mutations.py",
        "restoration_v3_forest_certificate": PROJECT / "work/restoration_sign_reclassification/corrected_restoration_forest.json",
        "raw4_terminal_certificate_registry": ARTIFACTS / "raw4_terminal_certificate_registry.json.gz",
        "raw4_full_map_truth_certificate": PROJECT / "work/adversarial_proof_review/raw4_tree_sunlet_full_map_certificate.json",
        "corrected_overlay": PROJECT / "work/raw4_sign_reclassification/raw4_corrected_terminal_ledger.json",
        "theta2_full_map_truth_certificate": PROJECT / "work/adversarial_proof_review/theta2_tree_sunlet_full_map_certificate.json",
    }
    for family in ("raw4", "theta2"):
        paths.update(
            {
                f"{family}_corrected_composite_ledger": ARTIFACTS / f"{family}_corrected_composite_ledger.jsonl.gz",
                f"{family}_corrected_composite_summary": ARTIFACTS / f"{family}_corrected_composite_summary.json",
                f"{family}_corrected_composite_replay": ARTIFACTS / f"{family}_corrected_composite_independent_replay.json",
                f"{family}_corrected_composite_mutation_report": ARTIFACTS / f"{family}_corrected_composite_mutations.json",
            }
        )
    raw4 = release.validate_composite_primitive_summary(
        "raw4", paths, release.RAW_FOUR_TOTAL, release.RAW4_COMPOSITE_CATEGORY_COUNTS
    )
    theta2 = release.validate_composite_primitive_summary(
        "theta2", paths, release.THETA2_TOTAL, release.THETA2_COMPOSITE_CATEGORY_COUNTS
    )
    report = {
        "schema": "k2p-corrected-composites-release-contract-replay-v1",
        "status": "PASS",
        "release_common_sha256": sha_file(release_path),
        "validator_sha256": sha_file(Path(__file__)),
        "raw4": raw4,
        "theta2": theta2,
        "unresolved": 0,
    }
    report["payload_sha256"] = sha_object(report)
    output = ARTIFACTS / "release_contract_replay.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "payload_sha256": report["payload_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
