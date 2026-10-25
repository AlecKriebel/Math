#!/usr/bin/env python3
"""Run Paper B's exact regression suite with explicit skip/failure accounting."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest
import warnings


ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "code"
REPORT = ROOT / "certificates" / "exact_test_report.json"


def names(records: list[tuple[unittest.case.TestCase, str]]) -> list[str]:
    return [test.id() for test, _ in records]


def main() -> None:
    warnings.simplefilter("error")
    sys.path.insert(0, str(CODE))
    suite = unittest.defaultTestLoader.discover(
        str(CODE), pattern="test_exact.py", top_level_dir=str(CODE)
    )
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
    failures = names(result.failures)
    errors = names(result.errors)
    skipped = names(result.skipped)
    expected_failures = names(result.expectedFailures)
    unexpected_successes = [test.id() for test in result.unexpectedSuccesses]
    test_module = sys.modules.get("test_exact")
    joint_certificate = getattr(
        getattr(test_module, "ExposureDecoratedCoreRegressionTests", None),
        "certificate",
        {},
    )
    exposure_loss_certificate = getattr(
        getattr(test_module, "ExposureLossStorageTests", None),
        "certificate",
        {},
    )
    exposure_loss_class = getattr(test_module, "ExposureLossStorageTests", None)
    exposure_loss_test_count = sum(
        1
        for name in dir(exposure_loss_class)
        if name.startswith("test_") and callable(getattr(exposure_loss_class, name))
    ) if exposure_loss_class is not None else 0
    joint_summary = {
        "coverage_scope": joint_certificate.get("coverage_scope"),
        "fixed_sample_count": joint_certificate.get("fixed_sample_count"),
        "incomparable_order_case_count": joint_certificate.get(
            "incomparable_order_case_count"
        ),
        "incomparable_order_realization_count": joint_certificate.get(
            "incomparable_order_realization_count"
        ),
        "joint_configuration_count": joint_certificate.get(
            "joint_configuration_count"
        ),
        "normalized_collision_pair_count": joint_certificate.get(
            "normalized_collision_pair_count"
        ),
        "normalized_signature_count": joint_certificate.get(
            "normalized_signature_count"
        ),
        "per_core_joint_configuration_counts": joint_certificate.get(
            "per_core_joint_configuration_counts"
        ),
        "raw_joint_carrier_count": joint_certificate.get(
            "raw_joint_carrier_count"
        ),
        "relative_label_placement_count": joint_certificate.get(
            "relative_label_orbit_audit", {}
        ).get("relative_label_placement_count"),
        "repair_count": joint_certificate.get("repair_count"),
        "simultaneous_both_hidden_configuration_count": joint_certificate.get(
            "simultaneous_both_hidden_configuration_count"
        ),
        "structural_realizable_cone_count": joint_certificate.get(
            "structural_realizable_cone_count"
        ),
        "unacceptable_collision_count": len(
            joint_certificate.get("unacceptable_collisions", ())
        ),
        "unclassified_collision_count": len(
            joint_certificate.get("unclassified_quotient_collisions", ())
        ),
        "unclassified_split_count": len(
            joint_certificate.get("unclassified_quotient_splits", ())
        ),
    }
    exposure_loss_summary = {
        "all_equal_child_epochs_q3_compressed": exposure_loss_certificate.get(
            "all_equal_child_epochs_q3_compressed"
        ),
        "all_full_equal_first_chamber_records_exact": (
            exposure_loss_certificate.get(
                "all_full_equal_first_chamber_records_exact"
            )
        ),
        "all_joint_reattachments_exact": exposure_loss_certificate.get(
            "all_joint_reattachments_exact"
        ),
        "all_records_match_total_observations": exposure_loss_certificate.get(
            "all_records_match_total_observations"
        ),
        "equal_child_epoch_count": exposure_loss_certificate.get(
            "equal_child_epoch_count"
        ),
        "full_equal_first_chamber_count": exposure_loss_certificate.get(
            "full_equal_first_chamber_count"
        ),
        "full_equal_first_q_half_count": exposure_loss_certificate.get(
            "full_equal_first_q_half_count"
        ),
        "repair_count": exposure_loss_certificate.get("repair_count"),
        "swapped_physical_q_assignment_exact": exposure_loss_certificate.get(
            "swapped_physical_q_assignment_exact"
        ),
    }
    regression_certificates_clean = (
        joint_summary["coverage_scope"] is not None
        and joint_summary["unacceptable_collision_count"] == 0
        and joint_summary["unclassified_collision_count"] == 0
        and joint_summary["unclassified_split_count"] == 0
        and exposure_loss_summary["all_equal_child_epochs_q3_compressed"] is True
        and exposure_loss_summary[
            "all_full_equal_first_chamber_records_exact"
        ] is True
        and exposure_loss_summary["all_joint_reattachments_exact"] is True
        and exposure_loss_summary[
            "all_records_match_total_observations"
        ] is True
        and exposure_loss_summary["swapped_physical_q_assignment_exact"] is True
    )
    clean = (
        result.testsRun > 0
        and result.wasSuccessful()
        and not skipped
        and not expected_failures
        and not unexpected_successes
        and exposure_loss_test_count == 13
        and regression_certificates_clean
    )
    report = {
        "errors": errors,
        "expected_failures": expected_failures,
        "failures": failures,
        "skipped": skipped,
        "status": "PASS" if clean else "FAIL",
        "suite": "paper-b-exact-regression-v5",
        "tests_total": result.testsRun,
        "unexpected_successes": unexpected_successes,
        "exposure_loss_tests_total": exposure_loss_test_count,
        "exposure_loss_tests_status": (
            "PASS" if clean and exposure_loss_test_count == 13 else "FAIL"
        ),
        "fixed_x_s_s_joint_structural_regression": joint_summary,
        "exposure_loss_joint_lift_regression": exposure_loss_summary,
    }
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if not clean:
        raise SystemExit(1)
    print(
        f"PAPER_B_EXACT_SUITE_PASS tests={result.testsRun} skipped=0 "
        "expected_failures=0 unexpected_successes=0 "
        f"exposure_loss={exposure_loss_test_count}/13"
    )


if __name__ == "__main__":
    main()
