#!/usr/bin/env python3
"""Run the frozen referee-authored spot checks once and preserve evidence."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.metadata
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
        "54e83dc6442308c55524ca8246a4b643a3663abdce3cc97032fee8cea64296c6",
        "four_port_witnesses.json",
        True,
    ),
    (
        "check_restoration_probe_census.py",
        "511c0d5832c38c2ee21eb8a82d1aad8a20f40d687364bf7121c83d0502c4119f",
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

BOUND_INPUTS = {
    "PACKAGE_MANIFEST.json": "fa2131e8a64f0caa40b95f67dbc2d635b12f45f33de50e5665a5a722fd5c676e",
    "SHA256SUMS": "44904efa2e59708a0911ada912ed1b76352e7fb3035c1e5b1fb8fdeb1846f602",
    "proof_package/ARCHIVE_MANIFEST.json": "8d93fa19139bdd6b2df4f88e56560a8a519399b1382e9fdd311821c1552e675d",
    "proof_package/reproducibility/requirements.txt": "5a731eb61d5928e5b724c065e64d64af03804d25e25b49928f369d9d6b4da95b",
}

README_SHA256 = "0314091f40d1b503fe8b4d8421b8a2e5fac9975371b54d79ad64a103ce8b1db9"
SANDBOX_SHA256 = "d0fc1c924878d95b9fc4eabac574f2a466d46d3bbfa237ba01efe143fd79c0c0"
SOURCE_COMMIT = "76a097fbc4ddadf23ba0119a371c5ac29f4802b1"
PYTHON_SHA256 = "b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf"
RUNTIME_PACKAGES = {
    "mpmath": ("1.3.0", "b241584d2c1fc0304b0a1015ea923749d7b0800411dd406dcab7c82bf25d9fe8"),
    "networkx": ("3.5", "292d3a17bb01625088feb7522303784f4377621e6fca235aefa32630764e1f21"),
    "numpy": ("2.5.2", "09295a80660f17925ae23765ce8cbd7ff7ceae968d5f2f89349f1cb74c0b9e11"),
    "sympy": ("1.14.0", "4e9476348ba105feab28d82f5bcf6cdba2e3e84de6e059bbfe7a13728c0a4ab0"),
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def verify_package_ledger(package_root: Path) -> dict[str, object]:
    manifest_path = package_root / "PACKAGE_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    payload = manifest.get("payload")
    if not isinstance(payload, list):
        raise SystemExit("package manifest payload is not a list")
    records = {}
    for row in payload:
        if not isinstance(row, dict) or set(row) != {"path", "bytes", "sha256"}:
            raise SystemExit("malformed package manifest payload row")
        relative = row["path"]
        relative_path = Path(relative)
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise SystemExit(f"unsafe package manifest path: {relative}")
        if relative in records:
            raise SystemExit(f"duplicate package manifest path: {relative}")
        records[relative] = row
    if len(records) != manifest.get("payload_file_count"):
        raise SystemExit("package manifest file count mismatch")
    if sum(row["bytes"] for row in records.values()) != manifest.get("payload_bytes"):
        raise SystemExit("package manifest byte count mismatch")

    ledger = {}
    for line in (package_root / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        if len(line) < 67 or line[64:66] != "  ":
            raise SystemExit("malformed package checksum line")
        expected_hash, relative = line[:64], line[66:]
        if relative in ledger:
            raise SystemExit(f"duplicate package checksum path: {relative}")
        ledger[relative] = expected_hash
    if ledger.pop("PACKAGE_MANIFEST.json", None) != digest(manifest_path):
        raise SystemExit("package manifest self-binding mismatch")
    if set(ledger) != set(records):
        raise SystemExit("package manifest/checksum path-set mismatch")

    for relative, row in records.items():
        path = package_root / relative
        if path.is_symlink() or not path.is_file():
            raise SystemExit(f"sealed payload is not a regular file: {relative}")
        try:
            path.resolve(strict=True).relative_to(package_root)
        except ValueError as error:
            raise SystemExit(f"sealed path escapes package: {relative}") from error
        if path.stat().st_size != row["bytes"]:
            raise SystemExit(f"sealed payload byte mismatch: {relative}")
        actual_hash = digest(path)
        if actual_hash != row["sha256"] or actual_hash != ledger[relative]:
            raise SystemExit(f"sealed payload hash mismatch: {relative}")
    return {
        "payload_file_count": len(records),
        "payload_bytes": sum(row["bytes"] for row in records.values()),
        "proof_source_commit": manifest.get("proof_source_commit"),
        "package_builder_commit": manifest.get("package_builder_commit"),
        "manifest_sha256": digest(manifest_path),
        "checksum_ledger_sha256": digest(package_root / "SHA256SUMS"),
    }


def main() -> None:
    if not __debug__:
        raise SystemExit("optimized Python is forbidden")
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, required=True)
    parser.add_argument("--checks-root", type=Path, required=True)
    parser.add_argument("--sandbox-profile", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    package_root = args.package_root.resolve(strict=True)
    checks_root = args.checks_root.resolve(strict=True)
    sandbox_profile = args.sandbox_profile.resolve(strict=True)
    output_dir = args.output_dir.resolve()
    review_runs_root = package_root / "review_runs"
    if review_runs_root not in output_dir.parents:
        raise SystemExit("output directory must be beneath copied-package review_runs")
    if output_dir.exists():
        raise SystemExit(f"refusing to reuse output directory: {output_dir}")

    outer_environment = {
        "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
        "LC_ALL": "C",
        "LANG": "C",
        "TZ": "UTC",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0",
        "K3P_REFEREE_CONFIRM_SPOTS": "YES",
        "__CF_USER_TEXT_ENCODING": "0x1F5:0:0",
    }
    unexpected = set(os.environ) - set(outer_environment)
    if unexpected:
        raise SystemExit(f"unexpected inherited environment keys: {sorted(unexpected)}")
    for name, expected in outer_environment.items():
        if os.environ.get(name) != expected:
            raise SystemExit(f"outer environment must set {name}={expected}")

    expected_python = package_root / ".venv" / "bin" / "python"
    if Path(sys.executable) != expected_python:
        raise SystemExit("runner must use the copied package's pinned interpreter")
    expected_prefix = package_root / ".venv"
    if Path(sys.prefix) != expected_prefix:
        raise SystemExit("runner sys.prefix is not the copied package virtual environment")
    if Path(sys.base_prefix).resolve() == Path(sys.prefix).resolve():
        raise SystemExit("runner is not in an isolated virtual environment")
    if sys.version_info[:3] != (3, 14, 6):
        raise SystemExit("runner requires exact Python 3.14.6")
    if digest(expected_python.resolve(strict=True)) != PYTHON_SHA256:
        raise SystemExit("pinned Python binary hash mismatch")
    packages = {}
    for name, (expected_version, expected_hash) in RUNTIME_PACKAGES.items():
        module = importlib.import_module(name)
        module_path = Path(module.__file__).resolve(strict=True)
        actual_version = importlib.metadata.version(name)
        actual_hash = digest(module_path)
        if actual_version != expected_version or actual_hash != expected_hash:
            raise SystemExit(f"pinned runtime package mismatch: {name}")
        packages[name] = {
            "version": actual_version,
            "module_file": str(module_path),
            "module_file_sha256": actual_hash,
        }

    bound_inputs = []
    for relative, expected_hash in BOUND_INPUTS.items():
        path = package_root / relative
        actual_hash = digest(path)
        if actual_hash != expected_hash:
            raise SystemExit(
                f"bound package input mismatch: {relative}: {actual_hash} != {expected_hash}"
            )
        bound_inputs.append(
            {"path": relative, "bytes": path.stat().st_size, "sha256": actual_hash}
        )
    package_manifest = json.loads((package_root / "PACKAGE_MANIFEST.json").read_text())
    if package_manifest.get("proof_source_commit") != SOURCE_COMMIT:
        raise SystemExit("unexpected proof source commit")
    if package_manifest.get("package_builder_commit") != SOURCE_COMMIT:
        raise SystemExit("unexpected package builder commit")
    pre_run_integrity = verify_package_ledger(package_root)

    readme = checks_root / "README.md"
    if digest(readme) != README_SHA256:
        raise SystemExit("independent-check README hash mismatch")
    if digest(sandbox_profile) != SANDBOX_SHA256:
        raise SystemExit("sandbox profile hash mismatch")

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

    output_dir.mkdir(parents=True)

    environment = {
        "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
        "LC_ALL": "C",
        "LANG": "C",
        "TZ": "UTC",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0",
        "__CF_USER_TEXT_ENCODING": "0x1F5:0:0",
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
            if not isinstance(parsed, dict):
                raise SystemExit(f"spot checker did not emit a JSON object: {filename}")
            if payload != completed.stdout or parsed != stdout_parsed:
                raise SystemExit(f"stdout/file payload mismatch: {filename}")
            if completed.stderr:
                raise SystemExit(f"unexpected stderr from spot checker: {filename}")
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

    expected_names = {"transcript.log"} | {item[2] for item in FROZEN}
    actual_names = {path.name for path in output_dir.iterdir()}
    if actual_names != expected_names:
        raise SystemExit(
            f"unexpected spot-suite output set: {sorted(actual_names ^ expected_names)}"
        )
    if any(path.is_symlink() or not path.is_file() for path in output_dir.iterdir()):
        raise SystemExit("spot-suite output contains a symlink or non-file object")

    post_run_integrity = verify_package_ledger(package_root)
    if post_run_integrity != pre_run_integrity:
        raise SystemExit("sealed package identity changed during the spot suite")
    for filename, expected_hash, _, _ in FROZEN:
        if digest(checks_root / filename) != expected_hash:
            raise SystemExit(f"checker changed during execution: {filename}")
    for row in reports:
        if digest(output_dir / row["output"]) != row["output_sha256"]:
            raise SystemExit(f"spot-check output changed during execution: {row['output']}")

    report_path = output_dir / "suite_report.json"
    runner_path = Path(__file__).resolve(strict=True)
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
            "packages": packages,
        },
        "invocation": {
            "argv": sys.argv,
            "cwd": str(Path.cwd()),
            "confirmation_variable": "K3P_REFEREE_CONFIRM_SPOTS=YES",
            "validated_inherited_environment": outer_environment,
            "subprocess_environment": environment,
            "runner_path": str(runner_path),
            "runner_sha256": digest(runner_path),
            "sandbox_profile": str(sandbox_profile),
            "sandbox_profile_sha256": digest(sandbox_profile),
        },
        "package_identity": {
            "proof_source_commit": SOURCE_COMMIT,
            "package_builder_commit": SOURCE_COMMIT,
            "bound_inputs": bound_inputs,
            "independent_check_readme_sha256": README_SHA256,
            "pre_run_integrity": pre_run_integrity,
            "post_run_integrity": post_run_integrity,
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
