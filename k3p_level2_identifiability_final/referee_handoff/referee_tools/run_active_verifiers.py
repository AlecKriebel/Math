#!/usr/bin/env python3
"""Run the active mathematical checks in copied, Git-free workspaces."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time


sys.dont_write_bytecode = True


class ReviewFailure(RuntimeError):
    pass


def require(condition: bool, message: object) -> None:
    if not condition:
        raise ReviewFailure(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def ignored_snapshot_path(relative: str) -> bool:
    parts = Path(relative).parts
    return (
        relative.startswith("release/work/")
        or (parts and parts[0] == ".venv")
    )


def snapshot(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if ignored_snapshot_path(relative):
            continue
        require(not path.is_symlink(),
                ("unexpected workspace symlink", relative))
        if path.is_dir():
            continue
        require(path.is_file(), ("unexpected workspace object", relative))
        result[relative] = sha256_file(path)
    return result


def drift(before: dict[str, str], after: dict[str, str]) -> dict[str, object]:
    before_keys, after_keys = set(before), set(after)
    changed = sorted(path for path in before_keys & after_keys
                     if before[path] != after[path])
    return {
        "added": sorted(after_keys - before_keys),
        "removed": sorted(before_keys - after_keys),
        "changed": [
            {"path": path, "before_sha256": before[path],
             "after_sha256": after[path]}
            for path in changed
        ],
    }


def load_plan(package_root: Path) -> dict:
    path = package_root / "referee_tools/ACTIVE_VERIFIER_PLAN.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    require(value.get("schema") == "k3p-independent-referee-plan-v1",
            "active verifier plan schema")
    return value


def deterministic_environment(workspace: Path) -> dict[str, str]:
    manifest = json.loads((workspace / "ARCHIVE_MANIFEST.json").read_text())
    environment = dict(os.environ)
    environment.update({
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0",
        "LC_ALL": "C",
        "LANG": "C",
        "TZ": "UTC",
        "SOURCE_DATE_EPOCH": str(manifest["source_date_epoch"]),
    })
    temporary = workspace / "release/work/referee_tmp"
    temporary.mkdir(parents=True, exist_ok=True)
    (workspace / "release/work/regeneration_ephemeral").mkdir(
        parents=True, exist_ok=True
    )
    environment["TMPDIR"] = str(temporary.resolve())
    return environment


def check_python(python: Path) -> None:
    require(python.is_file() and os.access(python, os.X_OK),
            ("Python interpreter is not executable", str(python)))
    result = subprocess.run(
        [str(python), "-c",
         "import mpmath, networkx, numpy, sympy; print('DEPENDENCIES_OK')"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        check=False, timeout=60,
    )
    require(result.returncode == 0 and "DEPENDENCIES_OK" in result.stdout,
            ("required Python dependencies unavailable", result.stdout[-2000:]))


def runtime_metadata(python: Path, package_root: Path) -> dict[str, object]:
    script = """
import importlib, json, platform, sys
packages = {}
for name in ('mpmath', 'networkx', 'numpy', 'sympy'):
    module = importlib.import_module(name)
    packages[name] = {
        'version': str(getattr(module, '__version__', 'UNKNOWN')),
        'module_file': str(getattr(module, '__file__', '')),
    }
print(json.dumps({
    'python_version': sys.version,
    'python_executable': sys.executable,
    'platform': platform.platform(),
    'machine': platform.machine(),
    'processor': platform.processor(),
    'packages': packages,
}, sort_keys=True))
"""
    result = subprocess.run(
        [str(python), "-c", script], stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True, check=False, timeout=60,
    )
    require(result.returncode == 0, ("runtime metadata failed", result.stdout))
    value = json.loads(result.stdout)
    for record in value["packages"].values():
        module_file = Path(record["module_file"])
        require(module_file.is_file(), ("package module file missing", module_file))
        record["module_file_sha256"] = sha256_file(module_file)
    executable = Path(os.path.realpath(python))
    require(executable.is_file(), ("interpreter file missing", executable))
    value["python_executable_sha256"] = sha256_file(executable)
    requirements = package_root / "proof_package/reproducibility/requirements.txt"
    require(requirements.is_file(), "requirements file missing")
    value["requirements_sha256"] = sha256_file(requirements)
    return value


def run_command(command: dict, *, workspace: Path, environment: dict[str, str],
                transcript) -> dict[str, object]:
    name = command["name"]
    argv = command["argv"]
    sentinel = command.get("sentinel")
    timeout_seconds = command["timeout_seconds"]
    transcript.write(f"\nCOMMAND {name}\n")
    transcript.write("ARGV " + json.dumps(argv) + "\n")
    transcript.flush()
    output_start = transcript.tell()
    started = time.monotonic()
    process = subprocess.Popen(
        argv, cwd=workspace, env=environment, text=True,
        stdout=transcript, stderr=subprocess.STDOUT, start_new_session=True,
    )
    try:
        returncode = process.wait(timeout=timeout_seconds)
    except subprocess.TimeoutExpired as error:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()
        raise ReviewFailure(("command timeout", name, timeout_seconds)) from error
    elapsed = time.monotonic() - started
    transcript.flush()
    output_end = transcript.tell()
    transcript.seek(output_start)
    output = transcript.read(output_end - output_start)
    transcript.seek(output_end)
    require(returncode == 0, ("command failed", name, returncode, output[-4000:]))
    require(sentinel is None or sentinel in output,
            ("command sentinel missing", name, sentinel, output[-4000:]))
    record = {
        "name": name,
        "argv": argv,
        "exit_code": returncode,
        "sentinel": sentinel,
        "sentinel_seen": sentinel is None or sentinel in output,
        "elapsed_seconds": elapsed,
        "stdout_sha256": sha256_bytes(output.encode("utf-8")),
        "status": "PASS",
    }
    transcript.write("RESULT " + json.dumps(record, sort_keys=True) + "\n")
    transcript.flush()
    print(json.dumps({"command": name, "elapsed_seconds": elapsed,
                      "status": "PASS"}, sort_keys=True), flush=True)
    return record


def verify_commands(plan: dict, python: Path) -> list[dict]:
    result = []
    for row in plan["verify_commands"]:
        argv = [str(python) if value == "{python}" else value
                for value in row["argv"]]
        result.append({**row, "argv": argv})
    return result


def import_regeneration_module(workspace: Path):
    reproducibility = workspace / "reproducibility"
    sys.path.insert(0, str(reproducibility))
    try:
        spec = importlib.util.spec_from_file_location(
            "k3p_referee_release_suite", reproducibility / "run_release_suite.py"
        )
        require(spec is not None and spec.loader is not None,
                "cannot load regeneration plan")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.pop(0)


def regeneration_commands(plan: dict, python: Path,
                          workspace: Path) -> list[dict]:
    module = import_regeneration_module(workspace)
    original = module.regeneration_commands(str(python), True)
    excluded = {row["name"] for row in plan["regeneration"]["excluded_commands"]}
    commands = [command for command in original if command.name not in excluded]
    names = [command.name for command in commands]
    require(len(original) == plan["regeneration"]["original_command_count"] and
            len(commands) == plan["regeneration"]["mathematical_command_count"] and
            names == plan["regeneration"]["ordered_names"],
            ("regeneration plan drift", len(original), len(commands), names))
    result = []
    for command in commands:
        argv = list(command.argv)
        if command.name == "integrated_fresh_independent_replay":
            require("--no-write-report" in argv,
                    "integrated regeneration report override drift")
            argv.remove("--no-write-report")
            argv.extend([
                "--report", "release/work/referee_integrated_fresh_report.json"
            ])
        result.append({
            "name": command.name,
            "argv": argv,
            "sentinel": command.sentinel,
            "timeout_seconds": command.timeout_seconds,
        })
    return result


def normalize_primary_report(value: object, project_root: str) -> object:
    if isinstance(value, dict):
        return {key: normalize_primary_report(item, project_root)
                for key, item in value.items()}
    if isinstance(value, list):
        return [normalize_primary_report(item, project_root) for item in value]
    if isinstance(value, str):
        return value.replace(project_root, "{PROJECT_ROOT}")
    return value


def normalized_primary_report(value: dict, project_root: str) -> dict:
    normalized = normalize_primary_report(value, project_root)
    require(isinstance(normalized, dict), "normalized primary report object")
    python_record = normalized.get("python")
    require(isinstance(python_record, dict) and
            isinstance(python_record.get("executable"), str),
            "primary report Python record")
    python_record["executable"] = "{PYTHON_EXECUTABLE}"
    return normalized


def preserve_and_restore_primary_report(*, workspace: Path, phase_root: Path,
                                        package_root: Path,
                                        canonical_bytes: bytes,
                                        label: str) -> dict[str, object]:
    relative = "reproducibility/primary_gate_report.json"
    path = workspace / relative
    require(path.is_file(), ("missing regenerated primary report", relative))
    current_bytes = path.read_bytes()
    canonical = json.loads(canonical_bytes)
    current = json.loads(current_bytes)
    canonical_root = canonical.get("project_root")
    current_root = current.get("project_root")
    require(isinstance(canonical_root, str) and canonical_root and
            isinstance(current_root, str) and current_root and
            normalized_primary_report(canonical, canonical_root) ==
            normalized_primary_report(current, current_root),
            "regenerated primary report differs beyond declared runtime paths")
    evidence = phase_root / f"{label}.json"
    evidence.write_bytes(current_bytes)
    path.write_bytes(canonical_bytes)
    return {
        "path": evidence.relative_to(package_root).as_posix(),
        "bytes": evidence.stat().st_size,
        "sha256": sha256_file(evidence),
        "semantic_relation": (
            "canonical report modulo project-root and interpreter paths"
        ),
    }


def integrated_logical_payload(report: dict) -> dict:
    logical = dict(report)
    logical.pop("operational", None)
    logical.pop("payload_sha256", None)
    logical["fresh_replays"] = [
        {
            key: row[key]
            for key in (
                "name", "exit_code", "sentinel", "sentinel_seen", "status",
                "fresh_output_payload_sha256", "fresh_mutation_payload_sha256",
            )
            if key in row
        }
        for row in report.get("fresh_replays", [])
    ]
    return logical


def bind_fresh_replay_report(*, workspace: Path, phase_root: Path,
                             package_root: Path) -> dict[str, object]:
    relative = "release/work/referee_integrated_fresh_report.json"
    path = workspace / relative
    require(path.is_file(), ("missing detailed fresh-replay report", relative))
    value = json.loads(path.read_text(encoding="utf-8"))
    rows = value.get("fresh_replays")
    require(value.get("mathematical_classification_status") == "CERTIFIED" and
            isinstance(rows, list) and len(rows) == 20 and
            all(isinstance(row, dict) and row.get("status") == "PASS" and
                row.get("exit_code") == 0 and row.get("sentinel_seen") is True
                for row in rows),
            "detailed fresh-replay report does not certify twenty passing child checks")
    observed_payload = sha256_bytes(json.dumps(
        integrated_logical_payload(value), sort_keys=True, separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8"))
    require(value.get("payload_sha256") == observed_payload,
            "detailed fresh-replay report payload mismatch")
    evidence = phase_root / "integrated_fresh_report.json"
    shutil.copy2(path, evidence)
    return {
        "path": evidence.relative_to(package_root).as_posix(),
        "bytes": evidence.stat().st_size,
        "sha256": sha256_file(evidence),
        "fresh_replay_count": len(rows),
        "payload_sha256": observed_payload,
    }


def run_phase(*, phase: str, package_root: Path, python: Path,
              session_root: Path, plan: dict,
              runtime: dict[str, object]) -> dict[str, object]:
    proof = package_root / "proof_package"
    phase_root = session_root / phase
    workspace = phase_root / "workspace"
    phase_root.mkdir(parents=True, exist_ok=False)
    shutil.copytree(proof, workspace)
    (workspace / ".venv").symlink_to(python.parent.parent, target_is_directory=True)
    environment = deterministic_environment(workspace)
    before = snapshot(workspace)
    primary_path = workspace / "reproducibility/primary_gate_report.json"
    require(primary_path.is_file(), "canonical primary report missing")
    canonical_primary_bytes = primary_path.read_bytes()
    transcript_path = phase_root / "transcript.log"
    records: list[dict[str, object]] = []
    supplemental_outputs: list[dict[str, object]] = []
    started = time.monotonic()
    with transcript_path.open("w+", encoding="utf-8", newline="\n") as transcript:
        transcript.write(json.dumps({
            "schema": "k3p-independent-referee-transcript-v1",
            "phase": phase,
            "proof_source_commit": json.loads(
                (workspace / "ARCHIVE_MANIFEST.json").read_text()
            )["source_commit"],
            "python": str(python),
            "environment": {key: environment[key] for key in (
                "PYTHONDONTWRITEBYTECODE", "PYTHONHASHSEED", "LC_ALL", "LANG",
                "TZ", "SOURCE_DATE_EPOCH",
            )},
            "runtime": runtime,
        }, sort_keys=True) + "\n")
        if phase == "verify":
            commands = verify_commands(plan, python)
        else:
            commands = regeneration_commands(plan, python, workspace)
        for command in commands:
            records.append(run_command(
                command, workspace=workspace, environment=environment,
                transcript=transcript,
            ))
            if command["name"] in {
                "primary_rebind", "integrated_fresh_independent_replay"
            }:
                supplemental_outputs.append(preserve_and_restore_primary_report(
                    workspace=workspace, phase_root=phase_root,
                    package_root=package_root,
                    canonical_bytes=canonical_primary_bytes,
                    label=f"{command['name']}_location_dependent_primary_report",
                ))
    supplemental_outputs.append(bind_fresh_replay_report(
        workspace=workspace, phase_root=phase_root, package_root=package_root,
    ))
    after = snapshot(workspace)
    workspace_drift = drift(before, after)
    require(workspace_drift == {"added": [], "removed": [], "changed": []},
            ("unexpected workspace drift", workspace_drift))
    report = {
        "schema": "k3p-independent-referee-run-v1",
        "status": "PASS",
        "phase": phase,
        "command_count": len(records),
        "commands": records,
        "supplemental_outputs": supplemental_outputs,
        "runtime": runtime,
        "elapsed_seconds": time.monotonic() - started,
        "workspace_drift": workspace_drift,
        "transcript": {
            "path": transcript_path.relative_to(package_root).as_posix(),
            "bytes": transcript_path.stat().st_size,
            "sha256": sha256_file(transcript_path),
        },
    }
    report_path = phase_root / "report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
    return report


def run_integrity(package_root: Path, python: Path) -> None:
    command = [
        str(python), str(package_root / "referee_tools/verify_package_integrity.py"),
        "--package-root", str(package_root),
    ]
    result = subprocess.run(
        command, cwd=package_root, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True, check=False, timeout=600,
    )
    require(result.returncode == 0 and
            "K3P_REFEREE_PACKAGE_INTEGRITY_PASS" in result.stdout,
            ("package integrity preflight failed", result.stdout[-4000:]))
    print(result.stdout, end="")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path,
                        default=Path(__file__).resolve().parents[1])
    parser.add_argument("--python", type=Path)
    parser.add_argument("--mode", choices=("plan", "verify", "regenerate", "all"),
                        default="verify")
    args = parser.parse_args(argv)
    package_root = args.package_root.resolve()
    # Preserve a virtual-environment interpreter path rather than resolving its
    # symlink to the base interpreter, which would discard the venv context.
    python = (Path(os.path.abspath(args.python)) if args.python else
              package_root / ".venv/bin/python")
    try:
        run_integrity(package_root, Path(sys.executable))
        check_python(python)
        runtime = runtime_metadata(python, package_root)
        plan = load_plan(package_root)
        if args.mode == "plan":
            commands = regeneration_commands(
                plan, python, package_root / "proof_package"
            )
            print(json.dumps({
                "status": "PASS",
                "mathematical_regeneration_commands": len(commands),
                "ordered_names": [command["name"] for command in commands],
            }, sort_keys=True))
            print("K3P_REFEREE_REGENERATION_PLAN_PASS")
            return 0
        if args.mode in {"regenerate", "all"}:
            require(os.environ.get("K3P_REFEREE_CONFIRM_REGENERATION") == "YES",
                    "set K3P_REFEREE_CONFIRM_REGENERATION=YES for the long run")
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        session_root = package_root / "review_runs" / stamp
        session_root.mkdir(parents=True, exist_ok=False)
        phases = ["verify", "regenerate"] if args.mode == "all" else [args.mode]
        reports = [run_phase(
            phase=phase, package_root=package_root, python=python,
            session_root=session_root, plan=plan, runtime=runtime,
        ) for phase in phases]
        summary = {
            "status": "PASS",
            "mode": args.mode,
            "session_root": session_root.relative_to(package_root).as_posix(),
            "phases": [
                {"phase": report["phase"],
                 "commands": report["command_count"],
                 "elapsed_seconds": report["elapsed_seconds"]}
                for report in reports
            ],
        }
        (session_root / "summary.json").write_text(
            json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(json.dumps(summary, sort_keys=True))
        print("K3P_REFEREE_ACTIVE_VERIFIERS_PASS")
        return 0
    except (ReviewFailure, OSError, UnicodeError, json.JSONDecodeError,
            subprocess.SubprocessError, TypeError, ValueError) as error:
        print(f"K3P_REFEREE_ACTIVE_VERIFIERS_FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
