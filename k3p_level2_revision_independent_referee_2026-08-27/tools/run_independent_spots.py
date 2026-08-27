#!/usr/bin/env python3
"""Run the frozen referee-authored spot checks once and preserve evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time


FROZEN = (
    (
        "check_three_leaf_geometry.py",
        "eaf0c29e630f2e53da34544b9d03ccf6d163e350f38302d6ba9b41d91d209a29",
        "three_leaf_geometry.json",
        False,
    ),
    (
        "check_bridge_gluing.py",
        "1be1d2a43330ed709adb4618c5062dd80e42af2ea6256fbf368632a916472755",
        "bridge_gluing.json",
        False,
    ),
    (
        "check_jc_endpoint_certificate.py",
        "4541f41475ebe2299019c96727133b2fd729fdb9f538d4e2fab3640a6856c158",
        "jc_endpoint_certificate.json",
        True,
    ),
    (
        "check_four_port_witnesses.py",
        "617af6091b0e63cf712b744fc30fe5ca5fc6f735e68ecd7adcfbef69d8839aa0",
        "four_port_witnesses.json",
        True,
    ),
    (
        "check_restoration_probe_census.py",
        "5ea78d1ae14fd14922a2168ddd77102d8103ad0f738daa9e9d5423c98f9b4ce7",
        "restoration_probe_census.json",
        True,
    ),
    (
        "check_probe_semantic_samples.py",
        "94b55315840d5bd631701e45ce1b273e6c8c419d9d90eda59a65cf0eeaa8e92f",
        "probe_semantic_samples.json",
        True,
    ),
    (
        "check_krawczyk_box.py",
        "d224151afd9bc9fc00833eb2d3a487bfe951d706eaa6e6683b028dbad07c95ba",
        "krawczyk_box.json",
        True,
    ),
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    if not __debug__:
        raise SystemExit("optimized Python is forbidden")
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, required=True)
    parser.add_argument("--checks-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    package_root = args.package_root.resolve(strict=True)
    checks_root = args.checks_root.resolve(strict=True)
    output_dir = args.output_dir.resolve()
    if package_root not in output_dir.parents:
        raise SystemExit("output directory must be beneath the copied package")
    if output_dir.exists():
        raise SystemExit(f"refusing to reuse output directory: {output_dir}")
    output_dir.mkdir(parents=True)

    expected_python = package_root / ".venv" / "bin" / "python"
    if Path(sys.executable).resolve() != expected_python.resolve(strict=True):
        raise SystemExit("runner must use the copied package's pinned interpreter")

    frozen_records = []
    for filename, expected_hash, output_name, needs_package in FROZEN:
        source = checks_root / filename
        actual_hash = digest(source)
        if actual_hash != expected_hash:
            raise SystemExit(
                f"frozen checker hash mismatch: {filename}: {actual_hash} != {expected_hash}"
            )
        frozen_records.append(
            {
                "path": str(source),
                "sha256": actual_hash,
                "expected_output": output_name,
                "uses_package_input": needs_package,
            }
        )

    environment = {
        "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
        "LC_ALL": "C",
        "LANG": "C",
        "TZ": "UTC",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    transcript = output_dir / "transcript.log"
    reports = []
    suite_start = time.perf_counter()
    with transcript.open("w", encoding="utf-8") as log:
        for filename, expected_hash, output_name, needs_package in FROZEN:
            source = checks_root / filename
            command = [str(expected_python), str(source)]
            if needs_package:
                command.extend(["--package-root", str(package_root)])
            command.extend(["--output-dir", str(output_dir)])
            log.write(f"COMMAND {json.dumps(command)}\n")
            log.flush()
            started = time.perf_counter()
            completed = subprocess.run(
                command,
                cwd=package_root,
                env=environment,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            elapsed = time.perf_counter() - started
            log.write("STDOUT-BEGIN\n")
            log.write(completed.stdout)
            if completed.stdout and not completed.stdout.endswith("\n"):
                log.write("\n")
            log.write("STDOUT-END\nSTDERR-BEGIN\n")
            log.write(completed.stderr)
            if completed.stderr and not completed.stderr.endswith("\n"):
                log.write("\n")
            log.write(f"STDERR-END\nEXIT {completed.returncode}\nELAPSED {elapsed:.9f}\n")
            log.flush()
            if completed.returncode != 0:
                raise SystemExit(f"spot checker failed: {filename}")
            output_path = output_dir / output_name
            if not output_path.is_file():
                raise SystemExit(f"spot checker omitted output: {output_name}")
            payload = output_path.read_text(encoding="utf-8")
            try:
                parsed = json.loads(payload)
                stdout_parsed = json.loads(completed.stdout)
            except json.JSONDecodeError as error:
                raise SystemExit(f"invalid JSON from {filename}: {error}") from error
            if parsed != stdout_parsed:
                raise SystemExit(f"stdout/file payload mismatch: {filename}")
            reports.append(
                {
                    "checker": filename,
                    "checker_sha256": expected_hash,
                    "elapsed_seconds": elapsed,
                    "exit_code": completed.returncode,
                    "output": output_name,
                    "output_bytes": output_path.stat().st_size,
                    "output_sha256": digest(output_path),
                    "top_level_keys": sorted(parsed),
                    "status": "PASS",
                    "stdout_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(),
                    "stderr_sha256": hashlib.sha256(completed.stderr.encode()).hexdigest(),
                }
            )

    report_path = output_dir / "suite_report.json"
    report = {
        "schema": "k3p-independent-referee-spot-suite-v1",
        "status": "PASS",
        "command_count": len(reports),
        "elapsed_seconds": time.perf_counter() - suite_start,
        "runtime": {
            "python": sys.version,
            "executable": str(expected_python),
            "executable_sha256": digest(expected_python.resolve(strict=True)),
            "platform": platform.platform(),
        },
        "isolation_expectation": (
            "This runner records results but does not provide isolation itself; "
            "the invoking operating-system sandbox is the enforcement boundary."
        ),
        "frozen_checkers": frozen_records,
        "commands": reports,
    }
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    ledger = output_dir / "SHA256SUMS_AUDIT"
    evidence = sorted(
        path for path in output_dir.iterdir()
        if path.is_file() and path.name != ledger.name
    )
    ledger.write_text(
        "".join(f"{digest(path)}  {path.name}\n" for path in evidence),
        encoding="utf-8",
    )
    print(json.dumps({"status": "PASS", "report": str(report_path), "ledger": str(ledger)}))


if __name__ == "__main__":
    main()
