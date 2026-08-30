#!/usr/bin/env python3
"""Run bounded referee-authored checks against the fourth revision."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
PACKAGE = AUDIT / "package_copy"
FROZEN_CHECKS = Path(
    "/Users/alec/Documents/Math/"
    "k3p_level2_second_revision_referee_2026-08-28/independent_checks"
)
OUTPUT = HERE / "results/fresh_spots_20260829_fourth"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to reuse {OUTPUT}")
    OUTPUT.mkdir(parents=True)
    commands = [
        ("three_leaf_geometry", "check_three_leaf_geometry.py",
         ["--output-dir", str(OUTPUT)]),
        ("bridge_gluing", "check_bridge_gluing.py",
         ["--output-dir", str(OUTPUT)]),
        ("four_port_witnesses", "check_four_port_witnesses.py",
         ["--package-root", str(PACKAGE), "--output-dir", str(OUTPUT)]),
        ("restoration_probe_census", "check_restoration_probe_census.py",
         ["--package-root", str(PACKAGE), "--output-dir", str(OUTPUT)]),
        ("probe_semantic_samples", "check_probe_semantic_samples.py",
         ["--package-root", str(PACKAGE), "--output-dir", str(OUTPUT)]),
        ("krawczyk_box", "check_krawczyk_box.py",
         ["--package-root", str(PACKAGE), "--output-dir", str(OUTPUT)]),
        ("revised_cut", "check_revised_cut.py",
         ["--output", str(OUTPUT / "revised_cut.json")]),
    ]
    manifest = PACKAGE / "PACKAGE_MANIFEST.json"
    sums = PACKAGE / "SHA256SUMS"
    before = {"manifest": sha256(manifest), "sums": sha256(sums)}
    transcript_path = OUTPUT / "transcript.log"
    records = []
    started_all = time.monotonic()
    with transcript_path.open("x", encoding="utf-8") as transcript:
        transcript.write(json.dumps({
            "schema": "k3p-fourth-revision-referee-spots-v1",
            "started_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "package": str(PACKAGE),
            "python": sys.executable,
            "environment_keys": sorted(os.environ),
            "independence_boundary": (
                "frozen referee-owned scripts; reviewed-package modules are not imported"
            ),
        }, sort_keys=True) + "\n")
        for name, filename, arguments in commands:
            script = FROZEN_CHECKS / filename
            command = [sys.executable, str(script), *arguments]
            started = time.monotonic()
            result = subprocess.run(
                command, cwd=HERE, text=True, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, check=False, timeout=3_600,
                env=dict(os.environ),
            )
            elapsed = time.monotonic() - started
            transcript.write(f"\nCOMMAND {name}\n")
            transcript.write(json.dumps(command) + "\n")
            transcript.write(result.stdout)
            transcript.flush()
            record = {
                "name": name,
                "script": str(script),
                "script_sha256": sha256(script),
                "returncode": result.returncode,
                "elapsed_seconds": elapsed,
                "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
                "status": "PASS" if result.returncode == 0 else "FAIL",
            }
            records.append(record)
            if result.returncode != 0:
                raise SystemExit((name, result.returncode, result.stdout[-2000:]))
    after = {"manifest": sha256(manifest), "sums": sha256(sums)}
    report = {
        "schema": "k3p-fourth-revision-referee-spot-suite-v1",
        "status": "PASS",
        "check_count": len(records),
        "checks": records,
        "package_outer_seal_before": before,
        "package_outer_seal_after": after,
        "package_outer_seal_unchanged": before == after,
        "elapsed_seconds": time.monotonic() - started_all,
        "transcript": {
            "path": str(transcript_path),
            "sha256": sha256(transcript_path),
            "bytes": transcript_path.stat().st_size,
        },
    }
    report_path = OUTPUT / "SUITE_REPORT.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": report["status"], "checks": report["check_count"],
        "elapsed_seconds": report["elapsed_seconds"],
        "report_sha256": sha256(report_path),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
