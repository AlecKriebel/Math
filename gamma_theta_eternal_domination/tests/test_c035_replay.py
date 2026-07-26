from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


CAMPAIGN = Path(__file__).resolve().parents[1]
MODULE_PATH = CAMPAIGN / "repro/c035/replay.py"
SPEC = importlib.util.spec_from_file_location("c035_replay", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
c035 = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = c035
SPEC.loader.exec_module(c035)


class C035ReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.metadata = c035.verify_metadata(CAMPAIGN)

    def test_lock_is_self_pinned_and_claim_specific(self) -> None:
        payload = (CAMPAIGN / "repro/c035/accepted_artifacts.json").read_bytes()
        self.assertEqual(hashlib.sha256(payload).hexdigest(), c035.LOCK_SHA256)
        lock = c035.strict_json_bytes(payload, "lock")
        self.assertEqual(lock["claim_id"], "C-035")
        self.assertEqual(lock["accepted_commit"], c035.ACCEPTED_COMMIT)
        self.assertEqual(lock["schema"], c035.LOCK_SCHEMA)

    def test_real_fast_mode_is_explicitly_nonclaiming(self) -> None:
        report = self.metadata.report
        self.assertEqual(report["status"], "PASS_METADATA_ONLY")
        self.assertEqual(report["claim_status"], "NO_MATHEMATICAL_CLAIM")
        self.assertFalse(report["proofs_freshly_replayed"])
        self.assertIn("NO_MATHEMATICAL_CLAIM", report["warning"])
        self.assertEqual(set(report["branch_bindings"]), {"C5", "C7", "C9"})
        self.assertGreaterEqual(report["locked_artifact_count"], 80)
        self.assertEqual(
            report["non_git_anchored_artifacts"],
            [
                "repro/c035/accepted_artifacts.json",
                "repro/c035/replay.py",
                "tools/drat_trim_2023_05_22/drat-trim",
                "tools/drat_trim_2023_05_22/drat-trim.c",
            ],
        )
        self.assertEqual(
            report["theorem_scope"]["universal_conjecture_resolved"], False
        )

    def test_strict_json_rejects_duplicates_nonfinite_and_noise(self) -> None:
        for payload in (
            b'{"x":1,"x":2}\n',
            b'{"x":NaN}\n',
            b'{"x":1}\nnoise\n',
            b"\xef\xbb\xbf{}\n",
        ):
            with self.subTest(payload=payload):
                with self.assertRaises(c035.ReplayFailure):
                    c035.strict_json_bytes(payload, "mutation")

    def test_manifest_parser_rejects_duplicate_ids_and_scope_mutation(self) -> None:
        payload = (CAMPAIGN / "results/manifest.csv").read_bytes()
        rows = c035.parse_manifest_bytes(payload, "manifest")
        lock = c035.strict_json_bytes(
            (CAMPAIGN / "repro/c035/accepted_artifacts.json").read_bytes(),
            "lock",
        )
        c035.validate_manifest_rows(rows, lock["manifest_rows"], "manifest")

        duplicated = payload + next(
            line
            for line in payload.splitlines(keepends=True)
            if line.startswith(b"ART-220,")
        )
        with self.assertRaises(c035.ReplayFailure):
            c035.parse_manifest_bytes(duplicated, "duplicate manifest")

        mutated = copy.deepcopy(rows)
        mutated["ART-220"]["outcome"] = "UNIVERSAL_RESOLUTION"
        with self.assertRaises(c035.ReplayFailure):
            c035.validate_manifest_rows(
                mutated, lock["manifest_rows"], "mutated manifest"
            )

    def test_c5_fresh_validators_require_exact_status_and_output(self) -> None:
        postrun_payload = (
            CAMPAIGN
            / "reviews/hole5_binary_production_postrun_hostile_probe_log.json"
        ).read_bytes()
        postrun = c035.strict_json_bytes(postrun_payload, "postrun")
        accepted = c035._validate_c5_postrun_fresh(
            postrun, hashlib.sha256(postrun_payload).hexdigest()
        )
        self.assertEqual(accepted["status"], c035.C5_ACTIVATING_VERDICT)
        mutated = copy.deepcopy(postrun)
        mutated["verdict"] = "PASS"
        with self.assertRaises(c035.ReplayFailure):
            c035._validate_c5_postrun_fresh(
                mutated, hashlib.sha256(postrun_payload).hexdigest()
            )

        package_payload = (
            CAMPAIGN / "results/logs/hole5-binary-run-package-audit.json"
        ).read_bytes()
        package = c035.strict_json_bytes(package_payload, "package")
        accepted = c035._validate_c5_package_fresh(
            package, hashlib.sha256(package_payload).hexdigest()
        )
        self.assertEqual(accepted["status"], "PASS_EXACT_RETAINED_PACKAGE")
        mutated = copy.deepcopy(package)
        mutated["proof_evidence"]["readonly_replay"]["checker"][
            "verified_status_count"
        ] = 2
        with self.assertRaises(c035.ReplayFailure):
            c035._validate_c5_package_fresh(
                mutated, hashlib.sha256(package_payload).hexdigest()
            )

    def test_c7_fresh_validator_requires_actual_checker_replay(self) -> None:
        good = {
            "certificate_sha256": c035.C7_CERTIFICATE_SHA256,
            "addition_only_proof_sha256": c035.C7_PROOF_SHA256,
            "addition_only_proof_size_bytes": 18093724,
            "addition_count": 284317,
            "deleted_record_count": 263162,
            "strict_checker_replayed": True,
            "strict_checker_warning_free": True,
            "strict_checker_rup_only": True,
        }
        accepted = c035._validate_c7_fresh(good, "a" * 64)
        self.assertEqual(accepted["status"], "VERIFIED_FINITE_CERTIFICATE")
        for key, value in (
            ("strict_checker_replayed", False),
            ("strict_checker_warning_free", False),
            ("strict_checker_rup_only", False),
            ("addition_count", 284316),
        ):
            with self.subTest(key=key):
                bad = dict(good)
                bad[key] = value
                with self.assertRaises(c035.ReplayFailure):
                    c035._validate_c7_fresh(bad, "a" * 64)

    def test_c9_fresh_validator_requires_exact_verified_marker_census(self) -> None:
        good = {
            "schema": "gamma-theta-hole9-orphan-recovery-v1",
            "status": "audit_passed_pending_hostile_review",
            "cnf_sha256": c035.C9_CNF_SHA256,
            "addition_only_proof_sha256": c035.C9_PROOF_SHA256,
            "checker_exit_code": 0,
            "checker_flags": ["-I", "-f", "-W", "-U", "-t", "60"],
            "exact_verified_line_count": 1,
            "warning_count": 0,
        }
        accepted = c035._validate_c9_fresh(good, "b" * 64)
        self.assertEqual(
            accepted["status"], "AUDIT_PASSED_THEN_ACCEPTED_BY_C028_REVIEW"
        )
        for key, value in (
            ("status", "verified_pending_hostile_review"),
            ("checker_exit_code", 20),
            ("exact_verified_line_count", 2),
            ("warning_count", 1),
        ):
            with self.subTest(key=key):
                bad = dict(good)
                bad[key] = value
                with self.assertRaises(c035.ReplayFailure):
                    c035._validate_c9_fresh(bad, "b" * 64)

    def test_full_mode_has_four_sequential_clean_room_audits(self) -> None:
        specs = c035.full_audit_specs(CAMPAIGN)
        self.assertEqual(
            [spec.name for spec in specs],
            [
                "c5_postrun_clean_room",
                "c5_retained_package_clean_room",
                "c7_sealed_addition_only",
                "c9_sealed_orphan_recovery",
            ],
        )
        for spec in specs:
            self.assertEqual(spec.arguments[1:3], ("-I", "-B"))
            self.assertNotIn("/src/synthesis_k3/", " ".join(spec.arguments))
        self.assertIn("--replay-checker", specs[2].arguments)
        self.assertEqual(
            specs[3].arguments[-2],
            "--drat-trim",
        )

    def test_full_composition_promotes_only_after_all_four_audits(self) -> None:
        calls: list[str] = []

        def fake_audit(spec: object, **_keywords: object) -> dict[str, object]:
            calls.append(spec.name)
            return {
                "status": f"PASS_{spec.name}",
                "exit_code": 0,
                "stderr_sha256": c035.EMPTY_SHA256,
            }

        gate = {
            "available_memory_bytes": 8 << 30,
            "disk_free_bytes": 8 << 30,
            "logical_cpu_count": 10,
            "maximum_one_minute_load": 7.5,
            "minimum_available_memory_bytes": 3 << 30,
            "minimum_disk_free_bytes": 1 << 30,
            "one_minute_load": 1.0,
        }
        with patch.object(
            c035, "run_isolated_audit", side_effect=fake_audit
        ), patch.object(c035, "_resource_gate", return_value=gate), patch.object(
            c035,
            "verify_snapshots_unchanged",
            return_value=self.metadata.snapshots,
        ):
            report = c035.run_full_replay(
                CAMPAIGN,
                self.metadata,
                timeout_seconds=1200,
                minimum_available_mib=3072,
                minimum_disk_mib=1024,
                maximum_one_minute_load=7.5,
                scratch_parent=None,
            )
        self.assertEqual(
            calls,
            [
                "c5_postrun_clean_room",
                "c5_retained_package_clean_room",
                "c7_sealed_addition_only",
                "c9_sealed_orphan_recovery",
            ],
        )
        self.assertEqual(report["status"], "PASS_FULL_C035_REPLAY")
        self.assertEqual(report["claim_status"], "CERTIFIED-FINITE")
        self.assertTrue(report["proofs_freshly_replayed"])
        self.assertEqual(len(report["resource_gates"]), 4)

        def fail_third(spec: object, **_keywords: object) -> dict[str, object]:
            if spec.name == "c7_sealed_addition_only":
                raise c035.ReplayFailure("forced C7 rejection")
            return {"status": "PASS"}

        with patch.object(
            c035, "run_isolated_audit", side_effect=fail_third
        ), patch.object(c035, "_resource_gate", return_value=gate):
            with self.assertRaisesRegex(c035.ReplayFailure, "forced C7 rejection"):
                c035.run_full_replay(
                    CAMPAIGN,
                    self.metadata,
                    timeout_seconds=1200,
                    minimum_available_mib=3072,
                    minimum_disk_mib=1024,
                    maximum_one_minute_load=7.5,
                    scratch_parent=None,
                )

    def test_isolated_child_requires_clean_json_and_empty_stderr(self) -> None:
        def validator(
            result: dict[str, object], stdout_sha256: str
        ) -> dict[str, object]:
            c035.require(result == {"status": "EXACT_PASS"}, "child status")
            return {"status": "EXACT_PASS", "stdout_sha256": stdout_sha256}

        spec = c035.AuditSpec(
            "tiny",
            (
                str(Path(sys.executable).resolve()),
                "-I",
                "-B",
                "-c",
                'import json; print(json.dumps({"status":"EXACT_PASS"}))',
            ),
            validator,
        )
        with tempfile.TemporaryDirectory() as raw:
            result = c035.run_isolated_audit(
                spec,
                root=CAMPAIGN,
                scratch_root=Path(raw),
                timeout_seconds=60,
            )
            self.assertEqual(result["exit_code"], 0)
            self.assertEqual(result["stderr_sha256"], c035.EMPTY_SHA256)
            self.assertEqual(
                (Path(raw) / "tiny").stat().st_mode & 0o777,
                0o700,
            )

    def test_cpu_load_gate_is_fail_closed_and_reported(self) -> None:
        with tempfile.TemporaryDirectory() as raw, patch.object(
            c035, "_available_memory_bytes", return_value=8 << 30
        ), patch.object(c035, "_logical_cpu_count", return_value=10), patch.object(
            c035, "_one_minute_load", return_value=8.0
        ):
            with self.assertRaisesRegex(
                c035.ReplayFailure, "one-minute CPU-load gate"
            ):
                c035._resource_gate(
                    Path(raw),
                    minimum_available_mib=3072,
                    minimum_disk_mib=512,
                    maximum_one_minute_load=7.5,
                )

        with tempfile.TemporaryDirectory() as raw, patch.object(
            c035, "_available_memory_bytes", return_value=8 << 30
        ), patch.object(c035, "_logical_cpu_count", return_value=10), patch.object(
            c035, "_one_minute_load", return_value=7.0
        ):
            report = c035._resource_gate(
                Path(raw),
                minimum_available_mib=3072,
                minimum_disk_mib=512,
                maximum_one_minute_load=7.5,
            )
            self.assertEqual(report["logical_cpu_count"], 10)
            self.assertEqual(report["one_minute_load"], 7.0)
            self.assertEqual(report["maximum_one_minute_load"], 7.5)

    def test_default_load_ceiling_is_below_logical_cpu_count(self) -> None:
        with patch.object(c035, "_logical_cpu_count", return_value=10):
            self.assertEqual(c035.default_maximum_one_minute_load(), 7.5)
        for bad in (float("nan"), float("inf"), 0.0, 10.0):
            with self.subTest(bad=bad), tempfile.TemporaryDirectory() as raw, patch.object(
                c035, "_logical_cpu_count", return_value=10
            ):
                with self.assertRaises(c035.ReplayFailure):
                    c035._resource_gate(
                        Path(raw),
                        minimum_available_mib=3072,
                        minimum_disk_mib=512,
                        maximum_one_minute_load=bad,
                    )

    def test_output_creation_is_exclusive(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            output = Path(raw) / "report.json"
            c035.write_new_file(output, b"first\n")
            self.assertEqual(output.read_bytes(), b"first\n")
            with self.assertRaises(c035.ReplayFailure):
                c035.write_new_file(output, b"second\n")
            self.assertEqual(output.read_bytes(), b"first\n")

            dangling = Path(raw) / "dangling.json"
            victim = Path(raw) / "victim.json"
            dangling.symlink_to(victim)
            with self.assertRaises(c035.ReplayFailure):
                c035.write_new_file(dangling, b"hostile\n")
            self.assertFalse(victim.exists())

    def test_snapshot_guard_detects_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            path = root / "artifact"
            path.write_bytes(b"accepted")
            before = c035.snapshot_file(root, "artifact")
            expected = {
                "artifact": c035.ExpectedFile(
                    "artifact", len(b"accepted"), hashlib.sha256(b"accepted").hexdigest()
                )
            }
            path.write_bytes(b"mutated!")
            with self.assertRaises(c035.ReplayFailure):
                c035.verify_snapshots_unchanged(
                    root, {"artifact": before}, expected
                )

    def test_replay_source_has_no_search_or_synthesis_import(self) -> None:
        tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
        imported: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module is not None:
                imported.append(node.module)
        forbidden = (
            "synthesis_k3",
            "verifier_a",
            "verifier_b",
            "evaluation_checker",
            "search",
        )
        self.assertFalse(
            any(name.startswith(forbidden) for name in imported),
            imported,
        )


if __name__ == "__main__":
    unittest.main()
