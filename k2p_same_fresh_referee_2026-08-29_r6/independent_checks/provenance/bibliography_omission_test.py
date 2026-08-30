#!/usr/bin/env python3
"""Confirm the outer submission-manifest producer rejects a missing BibTeX file."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="k2p-bib-omission-", dir=args.scratch) as raw:
        destination = Path(raw) / "project"
        copy = subprocess.run(
            ["cp", "-cR", str(args.project.resolve()), str(destination)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        if copy.returncode != 0:
            raise SystemExit(f"copy failed: {copy.stderr.decode(errors='replace')}")
        bibliography = destination / "proof_compression_submission/article/references.bib"
        bibliography.unlink()
        command = [
            str(args.python.resolve()), "-B",
            "proof_compression_submission/crosswalk/build_revised_referee_bundle.py",
            "--check",
        ]
        result = subprocess.run(
            command, cwd=destination, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, check=False,
        )
        diagnostic = (result.stdout + result.stderr).decode("utf-8", "replace")
        passed = (
            result.returncode == 1
            and "proof_compression_submission/article/references.bib" in diagnostic
            and ("missing" in diagnostic.lower() or "required" in diagnostic.lower())
        )
    report = {
        "schema": "k2p-r6-bibliography-omission-test-v1",
        "status": "PASS" if passed else "FAIL",
        "expected_exit_status": 1,
        "observed_exit_status": result.returncode,
        "bibliography_path": "proof_compression_submission/article/references.bib",
        "diagnostic": diagnostic.strip(),
        "diagnostic_mentions_missing_bibliography": passed,
        "success_artifact_possible": False,
    }
    report["payload_sha256"] = hashlib.sha256(
        json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
