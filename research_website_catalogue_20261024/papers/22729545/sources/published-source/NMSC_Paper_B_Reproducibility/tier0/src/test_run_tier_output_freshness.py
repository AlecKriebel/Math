#!/usr/bin/env python3
"""Regression: a silent/no-op job may not reuse a stale PASS output."""

from __future__ import annotations

import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

from run_tier import (
    Job,
    execute_job,
    fingerprint,
    interpreter_identifier,
    recorded_job_command,
    recorded_runner_invocation,
)


class FreshOutputRegression(unittest.TestCase):
    def test_silent_success_without_fresh_output_is_blocking(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "stale.json"
            checkpoint = root / "checkpoint.json"
            output.write_text(
                json.dumps(
                    {
                        "schema_version": "nmsc-local-certificate-v3",
                        "job": "silent_noop",
                        "case_id": "0" * 24,
                        "input_hash": "0" * 64,
                        "status": "PASS",
                        "graph": {"stale": True},
                        "system": None,
                        "exact_witness": {"stale": True},
                        "declared_quotient_orbit": None,
                        "notes": "This stale record must be removed before execution.",
                    }
                )
            )
            job = Job(
                "silent_noop",
                (sys.executable, "-c", "pass"),
                output,
                "silent_noop",
                1,
            )
            log = io.StringIO()
            with self.assertRaises(SystemExit):
                execute_job(
                    root=root,
                    tier=0,
                    job=job,
                    checkpoint=checkpoint,
                    current_fingerprint={"regression": "silent-noop"},
                    log=log,
                )
            self.assertFalse(output.exists())
            state = json.loads(checkpoint.read_text())
            self.assertEqual(state["status"], "failed")
            self.assertEqual(state["returncode"], 0)
            self.assertNotIn(str(Path(sys.executable).resolve()), log.getvalue())
            self.assertIn(interpreter_identifier(), log.getvalue())

    def test_recorded_commands_and_fingerprints_are_location_independent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            (root / "environment.lock").write_text("python>=3.11,<3.14\n")
            (root / "requirements.lock").write_text("sympy==1.14.0\n")
            script = root / "src" / "worker.py"
            output = root / "outputs" / "worker.json"
            script.parent.mkdir()
            output.parent.mkdir()
            script.write_text("pass\n")
            job = Job(
                "portable",
                (
                    sys.executable,
                    str(script),
                    "--out",
                    str(output),
                ),
                output,
                "portable",
                1,
            )
            recorded = recorded_job_command(root, job)
            self.assertEqual(recorded[0], interpreter_identifier())
            self.assertEqual(recorded[1:], ["src/worker.py", "--out", "outputs/worker.json"])
            replay = fingerprint(root, job, {"src/worker.py": "a" * 64})
            encoded = json.dumps(replay, sort_keys=True)
            self.assertNotIn(str(root), encoded)
            self.assertNotIn(str(Path(sys.executable).resolve()), encoded)
            invocation = recorded_runner_invocation(
                root,
                [str(root / "src" / "run_tier.py"), "--tier", "0", "--root", str(root)],
            )
            self.assertEqual(
                invocation,
                [
                    interpreter_identifier(),
                    "src/run_tier.py",
                    "--tier",
                    "0",
                    "--root",
                    ".",
                ],
            )


if __name__ == "__main__":
    unittest.main()
