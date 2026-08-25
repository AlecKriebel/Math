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
            "layer_replays": [
                {
                    "elapsed_seconds": 3.0,
                    "name": "fake_full_layer",
                    "returncode": 0,
                    "status": "PASS",
                    "stderr_sha256": EMPTY_SHA256,
                    "stdout_sha256": EMPTY_SHA256,
                }
            ],
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
            self.assertEqual(value["report"]["layer_count"], 1)
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
