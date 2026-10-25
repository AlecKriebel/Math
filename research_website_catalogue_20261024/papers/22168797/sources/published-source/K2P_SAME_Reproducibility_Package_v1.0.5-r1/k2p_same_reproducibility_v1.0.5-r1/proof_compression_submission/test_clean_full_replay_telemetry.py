#!/usr/bin/env python3
"""Focused fail-closed tests for the clean full-replay telemetry producer."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
PRODUCER = HERE / "build_clean_full_replay_telemetry.py"
SOURCE_FILES = (
    "proof_compression_submission/article/main.tex",
    "proof_compression_submission/article/references.bib",
    "proof_compression_submission/supplement/supplement.tex",
    "proof_compression_submission/supplement/compression_tables.tex",
    "proof_compression_submission/supplement/certificate_appendix.tex",
)
EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()
INTENTIONAL_MUTATION_NAME = "four_port_exact_rank_staged_atlas_omission_mutation"
RESTORATION_LAYER_NAME = "corrected_restoration_independent_full_replay"
RESTORATION_SEMANTIC_COMMAND = (
    "<qualified-python>",
    "-B",
    "work/restoration_sign_reclassification/verify_corrected_restoration_forest.py",
    "--certificate",
    "work/restoration_sign_reclassification/corrected_restoration_forest.json",
    "--crosswalk",
    "work/restoration_sign_reclassification/corrected_restoration_historical_crosswalk.json",
    "--report",
    "<external-report-path>",
)
RESTORATION_SOURCE_FILES = (
    "work/restoration_sign_reclassification/verify_corrected_restoration_forest.py",
    "work/restoration_sign_reclassification/corrected_restoration_forest.json",
    "work/restoration_sign_reclassification/corrected_restoration_historical_crosswalk.json",
)
EXPECTED_LAYER_NAMES = (
    "promotion_manuscript_guard",
    "full_map_domain_reseal",
    "corrected_universe_independent_replay",
    "three_port_no_assert",
    "domain_rooting",
    "quartet_sign_logic",
    "quartet_terminal_bindings",
    "raw_displayed_quartet_direction",
    "canonicalizer_completeness_structural",
    "graph_derived_parameter_transports_structural",
    "bridge_marginal_gluing",
    "analytic_adversarial_audit",
    "global_component_scale_audit",
    "raw4_corrected_overlay_independent",
    "theta2_full_map_independent",
    "four_port_raw_structural_provenance",
    "four_port_direct36",
    "theta2_structural_provenance",
    "cycle_three_port_authoritative_promotion",
    "corrected_probe_independent_streaming_replay",
    "corrected_probe_site_transport_partition",
    "weak_sharpness_primary",
    "weak_sharpness_independent",
    "canonicalizer_completeness_full",
    "graph_derived_parameter_transports_full",
    RESTORATION_LAYER_NAME,
    "corrected_universe_cross_layer_mutations",
    "raw4_full_map_Ti_truth",
    "theta2_full_map_Ti_truth",
    "composite_domain_reseal_diff",
    INTENTIONAL_MUTATION_NAME,
    "four_port_exact_rank_import_preflight",
    "four_port_exact_rank_full",
    "raw4_corrected_overlay_full_regeneration",
    "four_port_raw_full_regeneration_provenance",
    "four_port_direct36_full",
    "theta2_full_regeneration_provenance",
    "corrected_probe_full_primitive_regeneration",
    "corrected_probe_full_independent_replay",
    "corrected_probe_full_site_transport_partition",
    "corrected_probe_independent_primitive_graph_full",
)


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def run(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


class Fixture:
    def __init__(self, base: Path) -> None:
        self.base = base
        self.checkout = base / "checkout"
        self.checkout.mkdir()
        self.project_in_repo = "research/programs/k2p_fixture"
        self.project = self.checkout / self.project_in_repo
        self.report = base / "report.json"
        self.time_l = base / "time-l.txt"
        self.output = base / "telemetry.json"
        require_ok(run(["git", "init", "-q"], self.checkout))
        require_ok(run(["git", "config", "user.name", "Telemetry Test"], self.checkout))
        require_ok(run(["git", "config", "user.email", "test@example.invalid"], self.checkout))
        for index, relative in enumerate(SOURCE_FILES):
            path = self.project / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"source {index}\n", encoding="utf-8")
        for index, relative in enumerate(RESTORATION_SOURCE_FILES):
            path = self.project / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"restoration source {index}\n", encoding="utf-8")
        self.write_lock()
        self.commit = self.commit_all("fixture")
        branch_result = run(["git", "branch", "--show-current"], self.checkout)
        require_ok(branch_result)
        self.branch = branch_result.stdout.strip()
        require_ok(run(["git", "checkout", "--detach", "-q", self.commit], self.checkout))
        self.write_report()
        self.time_l.write_text(
            """       3.50 real         3.10 user         0.20 sys
  1000000  maximum resident set size
       10  page reclaims
        2  page faults
        0  swaps
   500000  maximum memory footprint
""",
            encoding="utf-8",
        )

    def write_lock(self, *, valid_payload: bool = True) -> None:
        path = self.project / "work/final_theorem_release/RELEASE_LOCK.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        value = {
            "blockers": [],
            "missing_required_files": [],
            "promotion_ready": True,
            "schema": "k2p-principal-d-plus-final-theorem-release-lock-v1",
        }
        value["payload_sha256"] = canonical_hash(value) if valid_payload else "0" * 64
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def commit_all(self, message: str) -> str:
        require_ok(run(["git", "add", "."], self.checkout))
        require_ok(run(["git", "commit", "-q", "-m", message], self.checkout))
        result = run(["git", "rev-parse", "HEAD"], self.checkout)
        require_ok(result)
        return result.stdout.strip()

    def lock_payload(self) -> str:
        return json.loads(
            (self.project / "work/final_theorem_release/RELEASE_LOCK.json").read_text()
        )["payload_sha256"]

    def write_report(self, **changes: object) -> None:
        report = {
            "blockers": [],
            "elapsed_seconds": 3.25,
            "layer_replays": self.valid_layers(),
            "lock_payload_sha256": self.lock_payload(),
            "mode": "full",
            "optimized_mode": False,
            "promotion_ready": True,
            "runtime": {"networkx": "3.5", "python": "3.14.6", "sympy": "1.14.0"},
            "schema": "k2p-principal-d-plus-final-theorem-replay-report-v1",
            "status": "PASS",
        }
        report.update(changes)
        self.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    def valid_layers(
        self, extra: list[dict[str, object]] | None = None
    ) -> list[dict[str, object]]:
        replacement = None if not extra else extra[0]
        restoration = {
            "command_sha256": canonical_hash(RESTORATION_SEMANTIC_COMMAND),
            "elapsed_seconds": 1.0,
            "name": RESTORATION_LAYER_NAME,
            "returncode": 0,
            "source_sha256": {
                relative: hashlib.sha256(
                    (self.project / relative).read_bytes()
                ).hexdigest()
                for relative in RESTORATION_SOURCE_FILES
            },
            "status": "PASS",
            "stderr_sha256": EMPTY_SHA256,
            "stdout_sha256": EMPTY_SHA256,
        }
        layers = []
        for name in EXPECTED_LAYER_NAMES:
            if name == RESTORATION_LAYER_NAME:
                layers.append(restoration)
            elif name == INTENTIONAL_MUTATION_NAME:
                layers.append(
                    replacement
                    or {
                        "elapsed_seconds": 0.4,
                        "name": INTENTIONAL_MUTATION_NAME,
                        "observed_nonzero_returncode": 1,
                        "status": "PASS",
                        "stderr_sha256": EMPTY_SHA256,
                        "stdout_sha256": EMPTY_SHA256,
                    }
                )
            else:
                layers.append(
                    {
                        "elapsed_seconds": 0.05,
                        "name": name,
                        "returncode": 0,
                        "status": "PASS",
                        "stderr_sha256": EMPTY_SHA256,
                        "stdout_sha256": EMPTY_SHA256,
                    }
                )
        return layers

    def command(self, mode: str, *extra: str) -> list[str]:
        return [
            sys.executable,
            "-B",
            str(PRODUCER),
            mode,
            "--checkout-root",
            str(self.checkout),
            "--project-in-repo",
            self.project_in_repo,
            "--source-commit",
            self.commit,
            "--report",
            str(self.report),
            "--time-l",
            str(self.time_l),
            "--output",
            str(self.output),
            *extra,
        ]


def require_ok(result: subprocess.CompletedProcess[str]) -> None:
    if result.returncode != 0:
        raise AssertionError(f"command failed\nstdout={result.stdout}\nstderr={result.stderr}")


class TelemetryProducerTests(unittest.TestCase):
    def fixture(self) -> tuple[tempfile.TemporaryDirectory[str], Fixture]:
        temporary = tempfile.TemporaryDirectory(prefix="k2p-telemetry-test-")
        return temporary, Fixture(Path(temporary.name))

    def test_write_then_exact_check(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            require_ok(run(fixture.command("--write")))
            value = json.loads(fixture.output.read_text())
            self.assertEqual(value["schema"], "k2p-final-clean-full-replay-telemetry-v1")
            self.assertEqual(value["git_commit"], fixture.commit)
            self.assertEqual(value["project_in_repo"], fixture.project_in_repo)
            self.assertNotIn("completed_utc", value)
            self.assertEqual(len(value["submission_sources"]), 5)
            first_source = fixture.project / SOURCE_FILES[0]
            self.assertEqual(
                value["submission_sources"][SOURCE_FILES[0]]["sha256"],
                hashlib.sha256(first_source.read_bytes()).hexdigest(),
            )
            self.assertEqual(value["report"]["layer_count"], 41)
            self.assertEqual(value["release_lock"]["payload_sha256"], fixture.lock_payload())
            require_ok(run(fixture.command("--check")))

    def test_attached_or_dirty_checkout_is_rejected(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            require_ok(run(["git", "switch", "-q", fixture.branch], fixture.checkout))
            attached = run(fixture.command("--write"))
            self.assertNotEqual(attached.returncode, 0)
            self.assertIn("DETACHED_HEAD_REQUIRED", attached.stderr)
            require_ok(run(["git", "checkout", "--detach", "-q", fixture.commit], fixture.checkout))
            (fixture.project / SOURCE_FILES[0]).write_text("dirty\n")
            dirty = run(fixture.command("--write"))
            self.assertNotEqual(dirty.returncode, 0)
            self.assertIn("DIRTY_CHECKOUT", dirty.stderr)

    def test_wrong_commit_and_bad_lock_payload_are_rejected(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            wrong = fixture.command("--write")
            wrong[wrong.index(fixture.commit)] = "0" * 40
            result = run(wrong)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("SOURCE_COMMIT_MISMATCH", result.stderr)

            fixture.write_lock(valid_payload=False)
            fixture.commit = fixture.commit_all("invalid lock")
            require_ok(run(["git", "checkout", "--detach", "-q", fixture.commit], fixture.checkout))
            fixture.write_report()
            result = run(fixture.command("--write"))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("RELEASE_LOCK_PAYLOAD_MISMATCH", result.stderr)

    def test_nonpassing_report_and_malformed_time_are_rejected(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            fixture.write_report(status="BLOCKED")
            result = run(fixture.command("--write"))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("FULL_REPLAY_REPORT_NOT_PASS", result.stderr)
            fixture.write_report()
            fixture.time_l.write_text("3.50 real 3.10 user 0.20 sys\n")
            result = run(fixture.command("--write"))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("TIME_L_MAXIMUM_RESIDENT_INVALID", result.stderr)

    def test_peak_memory_footprint_label_is_supported(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            fixture.time_l.write_text(
                fixture.time_l.read_text().replace(
                    "maximum memory footprint", "peak memory footprint"
                )
            )
            require_ok(run(fixture.command("--write")))
            value = json.loads(fixture.output.read_text())
            self.assertEqual(value["time_l"]["peak_memory_footprint_bytes"], 500000)

    def test_posix_time_prefix_is_supported(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            fixture.time_l.write_text(
                """real 3.50
user 3.10
sys 0.20
  1000000  maximum resident set size
       10  page reclaims
        2  page faults
        0  swaps
   500000  peak memory footprint
""",
                encoding="utf-8",
            )
            require_ok(run(fixture.command("--write")))
            value = json.loads(fixture.output.read_text())
            self.assertEqual(value["time_l"]["real_seconds"], 3.5)
            self.assertEqual(value["time_l"]["user_seconds"], 3.1)
            self.assertEqual(value["time_l"]["system_seconds"], 0.2)

    def test_exact_intentional_mutation_layer_is_accepted(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            mutation_row = {
                "elapsed_seconds": 0.4,
                "name": INTENTIONAL_MUTATION_NAME,
                "observed_nonzero_returncode": 1,
                "status": "PASS",
                "stderr_sha256": EMPTY_SHA256,
                "stdout_sha256": EMPTY_SHA256,
            }
            fixture.write_report(layer_replays=fixture.valid_layers([mutation_row]))
            require_ok(run(fixture.command("--write")))
            value = json.loads(fixture.output.read_text())
            self.assertEqual(value["report"]["layer_count"], 41)

    def test_malformed_intentional_mutation_layers_are_rejected(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            valid = {
                "elapsed_seconds": 0.4,
                "name": INTENTIONAL_MUTATION_NAME,
                "observed_nonzero_returncode": 1,
                "status": "PASS",
                "stderr_sha256": EMPTY_SHA256,
                "stdout_sha256": EMPTY_SHA256,
            }
            cases: list[tuple[str, dict[str, object], str]] = []

            missing_observed = dict(valid)
            missing_observed.pop("observed_nonzero_returncode")
            cases.append(
                (
                    "missing observed return code",
                    missing_observed,
                    "FULL_REPLAY_INTENTIONAL_MUTATION_SCHEMA_INVALID",
                )
            )

            ordinary_returncode_added = dict(valid)
            ordinary_returncode_added["returncode"] = 0
            cases.append(
                (
                    "ordinary return code added",
                    ordinary_returncode_added,
                    "FULL_REPLAY_INTENTIONAL_MUTATION_SCHEMA_INVALID",
                )
            )

            wrong_observed = dict(valid)
            wrong_observed["observed_nonzero_returncode"] = 2
            cases.append(
                (
                    "wrong observed return code",
                    wrong_observed,
                    "FULL_REPLAY_INTENTIONAL_MUTATION_RETURNCODE_INVALID",
                )
            )

            boolean_observed = dict(valid)
            boolean_observed["observed_nonzero_returncode"] = True
            cases.append(
                (
                    "boolean observed return code",
                    boolean_observed,
                    "FULL_REPLAY_INTENTIONAL_MUTATION_RETURNCODE_INVALID",
                )
            )

            unknown_mutation = dict(valid)
            unknown_mutation["name"] = "unlicensed_expected_failure_mutation"
            cases.append(
                (
                    "unlicensed mutation name",
                    unknown_mutation,
                    "FULL_REPLAY_ORDINARY_LAYER_SCHEMA_INVALID",
                )
            )

            ordinary_boolean_returncode = {
                "elapsed_seconds": 0.4,
                "name": "ordinary_full_layer",
                "returncode": False,
                "status": "PASS",
                "stderr_sha256": EMPTY_SHA256,
                "stdout_sha256": EMPTY_SHA256,
            }
            cases.append(
                (
                    "ordinary boolean return code",
                    ordinary_boolean_returncode,
                    "FULL_REPLAY_LAYER_RETURNCODE",
                )
            )

            ordinary_with_mutation_field = {
                "elapsed_seconds": 0.4,
                "name": "ordinary_full_layer",
                "observed_nonzero_returncode": 1,
                "status": "PASS",
                "stderr_sha256": EMPTY_SHA256,
                "stdout_sha256": EMPTY_SHA256,
            }
            cases.append(
                (
                    "ordinary layer uses mutation schema",
                    ordinary_with_mutation_field,
                    "FULL_REPLAY_ORDINARY_LAYER_SCHEMA_INVALID",
                )
            )

            for label, row, expected in cases:
                with self.subTest(label=label):
                    fixture.write_report(layer_replays=fixture.valid_layers([row]))
                    result = run(fixture.command("--write"))
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(expected, result.stderr)

    def test_restoration_command_and_source_bindings_fail_closed(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            base = fixture.valid_layers()
            restoration_index = EXPECTED_LAYER_NAMES.index(RESTORATION_LAYER_NAME)
            attacks: list[tuple[str, list[dict[str, object]], str]] = []

            wrong_command = json.loads(json.dumps(base))
            wrong_command[restoration_index]["command_sha256"] = "0" * 64
            attacks.append(
                (
                    "wrong semantic command",
                    wrong_command,
                    "FULL_REPLAY_RESTORATION_COMMAND_HASH_INVALID",
                )
            )

            wrong_source = json.loads(json.dumps(base))
            first_source = RESTORATION_SOURCE_FILES[0]
            wrong_source[restoration_index]["source_sha256"][first_source] = "0" * 64
            attacks.append(
                (
                    "wrong source hash",
                    wrong_source,
                    "FULL_REPLAY_RESTORATION_SOURCE_HASH_INVALID",
                )
            )

            missing = json.loads(json.dumps(base))
            missing[restoration_index] = {
                "elapsed_seconds": 0.05,
                "name": "replacement_ordinary_layer",
                "returncode": 0,
                "status": "PASS",
                "stderr_sha256": EMPTY_SHA256,
                "stdout_sha256": EMPTY_SHA256,
            }
            attacks.append(
                (
                    "missing restoration layer",
                    missing,
                    "FULL_REPLAY_RESTORATION_LAYER_MISSING",
                )
            )

            for label, layers, expected in attacks:
                with self.subTest(label=label):
                    fixture.write_report(layer_replays=layers)
                    result = run(fixture.command("--write"))
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(expected, result.stderr)

    def test_count_preserving_layer_substitution_is_rejected(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            layers = fixture.valid_layers()
            cycle_index = EXPECTED_LAYER_NAMES.index(
                "cycle_three_port_authoritative_promotion"
            )
            layers[cycle_index]["name"] = "cycle_three_port_structural_provenance"
            fixture.write_report(layer_replays=layers)
            result = run(fixture.command("--write"))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("FULL_REPLAY_LAYER_SEQUENCE_INVALID", result.stderr)

    def test_project_in_repo_prefix_fails_closed(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            wrong = run(
                fixture.command(
                    "--write", "--project-in-repo", "research/programs/not-k2p"
                )
            )
            self.assertNotEqual(wrong.returncode, 0)
            self.assertIn("CHECKOUT_FILE_MISSING", wrong.stderr)
            unsafe = run(
                fixture.command("--write", "--project-in-repo", "../k2p_fixture")
            )
            self.assertNotEqual(unsafe.returncode, 0)
            self.assertIn("UNSAFE_PROJECT_IN_REPO", unsafe.stderr)

    def test_output_replacement_is_explicit_and_drift_fails_check(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            fixture.output.write_text("{}\n")
            result = run(fixture.command("--write"))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("OUTPUT_EXISTS_DIFFERENT_USE_REPLACE_EXISTING", result.stderr)
            require_ok(run(fixture.command("--write", "--replace-existing")))
            fixture.output.write_text("{}\n")
            result = run(fixture.command("--check"))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("TELEMETRY_OUTPUT_DRIFT", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
