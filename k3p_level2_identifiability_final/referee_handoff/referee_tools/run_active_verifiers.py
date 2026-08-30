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
import stat
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


def mode_string(mode: int) -> str:
    return format(stat.S_IMODE(mode), "04o")


def open_private_directory_chain(root: Path,
                                 components: tuple[str, ...]) -> tuple[int, Path]:
    """Create and hold a directory chain without following package symlinks."""
    root_metadata = root.lstat()
    require(stat.S_ISDIR(root_metadata.st_mode) and
            not stat.S_ISLNK(root_metadata.st_mode),
            ("runtime package root must be a real directory", str(root)))
    require(hasattr(os, "O_DIRECTORY") and hasattr(os, "O_NOFOLLOW"),
            "runtime no-follow directory opens are unavailable")
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    descriptor = os.open(root, flags)
    current = root
    try:
        opened_root = os.fstat(descriptor)
        require((opened_root.st_dev, opened_root.st_ino) ==
                (root_metadata.st_dev, root_metadata.st_ino),
                ("runtime package root changed while opening", str(root)))
        for component in components:
            require(component not in {"", ".", ".."} and "/" not in component,
                    ("unsafe runtime path component", component))
            try:
                metadata = os.stat(
                    component, dir_fd=descriptor, follow_symlinks=False
                )
            except FileNotFoundError:
                os.mkdir(component, mode=0o700, dir_fd=descriptor)
                metadata = os.stat(
                    component, dir_fd=descriptor, follow_symlinks=False
                )
            require(stat.S_ISDIR(metadata.st_mode) and
                    not stat.S_ISLNK(metadata.st_mode),
                    ("runtime path component must be a real directory",
                     str(current / component)))
            child = os.open(component, flags, dir_fd=descriptor)
            try:
                opened = os.fstat(child)
                require((opened.st_dev, opened.st_ino) ==
                        (metadata.st_dev, metadata.st_ino),
                        ("runtime path component changed while opening",
                         str(current / component)))
                os.fchmod(child, 0o700)
            except BaseException:
                os.close(child)
                raise
            os.close(descriptor)
            descriptor = child
            current = current / component
        return descriptor, current
    except BaseException:
        os.close(descriptor)
        raise


def ensure_private_directory_chain(root: Path, components: tuple[str, ...]) -> Path:
    descriptor, path = open_private_directory_chain(root, components)
    os.close(descriptor)
    return path


def prepare_runtime_control(package_root: Path) -> dict[str, Path]:
    """Materialize the excluded runtime control paths with no-follow traversal."""
    review_runs = ensure_private_directory_chain(package_root, ("review_runs",))
    control = ensure_private_directory_chain(
        package_root, ("review_runs", "runner_control")
    )
    home = ensure_private_directory_chain(
        package_root, ("review_runs", "runner_control", "home")
    )
    temporary = ensure_private_directory_chain(
        package_root, ("review_runs", "runner_control", "tmp")
    )
    return {
        "review_runs": review_runs,
        "runner_control": control,
        "home": home,
        "tmp": temporary,
    }


def filesystem_inventory(root: Path) -> dict[str, dict[str, object]]:
    """Inventory every entry below root without following symlinks."""
    require(root.is_dir() and not root.is_symlink(),
            ("inventory root must be a real directory", str(root)))
    result: dict[str, dict[str, object]] = {
        ".": {"mode": mode_string(root.lstat().st_mode), "type": "directory"}
    }

    def visit(directory: Path) -> None:
        with os.scandir(directory) as entries:
            ordered = sorted(entries, key=lambda entry: entry.name)
        for entry in ordered:
            path = Path(entry.path)
            relative = path.relative_to(root).as_posix()
            metadata = entry.stat(follow_symlinks=False)
            common: dict[str, object] = {"mode": mode_string(metadata.st_mode)}
            if stat.S_ISLNK(metadata.st_mode):
                result[relative] = {
                    **common, "type": "symlink", "target": os.readlink(path),
                }
            elif stat.S_ISDIR(metadata.st_mode):
                result[relative] = {**common, "type": "directory"}
                visit(path)
            elif stat.S_ISREG(metadata.st_mode):
                result[relative] = {
                    **common,
                    "type": "file",
                    "bytes": metadata.st_size,
                    "sha256": sha256_file(path),
                }
            else:
                raise ReviewFailure(("unexpected filesystem object", relative))

    visit(root)
    return result


def drift(before: dict[str, dict[str, object]],
          after: dict[str, dict[str, object]]) -> dict[str, object]:
    before_keys, after_keys = set(before), set(after)
    changed = sorted(path for path in before_keys & after_keys
                     if before[path] != after[path])
    return {
        "added": sorted(after_keys - before_keys),
        "removed": sorted(before_keys - after_keys),
        "changed": [
            {"path": path, "before": before[path], "after": after[path]}
            for path in changed
        ],
    }


def drift_paths(value: dict[str, object]) -> set[str]:
    return (
        set(value["added"])
        | set(value["removed"])
        | {row["path"] for row in value["changed"]}
    )


def restrict_drift(value: dict[str, object], paths: set[str]) -> dict[str, object]:
    return {
        "added": [path for path in value["added"] if path in paths],
        "removed": [path for path in value["removed"] if path in paths],
        "changed": [row for row in value["changed"] if row["path"] in paths],
    }


def write_inventory(path: Path, root: Path,
                    value: dict[str, dict[str, object]]) -> dict[str, object]:
    payload = {
        "schema": "k3p-referee-filesystem-inventory-v1",
        "root": str(root),
        "entry_count": len(value),
        "entries": [
            {"path": relative, **record}
            for relative, record in sorted(value.items())
        ],
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")
    return {
        "path": path.as_posix(),
        "entry_count": len(value),
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def load_plan(package_root: Path) -> dict:
    path = package_root / "referee_tools/ACTIVE_VERIFIER_PLAN.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    require(value.get("schema") == "k3p-independent-referee-plan-v1",
            "active verifier plan schema")
    return value


def deterministic_environment(workspace: Path) -> dict[str, str]:
    manifest = json.loads((workspace / "ARCHIVE_MANIFEST.json").read_text())
    temporary = workspace / "release/work/referee_tmp"
    home = workspace / "release/work/referee_home"
    temporary.mkdir(parents=True, exist_ok=True)
    home.mkdir(parents=True, exist_ok=True)
    (workspace / "release/work/regeneration_ephemeral").mkdir(
        parents=True, exist_ok=True
    )
    return {
        "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
        "HOME": str(home.resolve()),
        "TMPDIR": str(temporary.resolve()),
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0",
        "PYTHONNOUSERSITE": "1",
        "LC_ALL": "C",
        "LANG": "C",
        "TZ": "UTC",
        "SOURCE_DATE_EPOCH": str(manifest["source_date_epoch"]),
    }


def control_environment(package_root: Path, source_date_epoch: str) -> dict[str, str]:
    runtime = prepare_runtime_control(package_root)
    return {
        "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
        "HOME": str(runtime["home"]),
        "TMPDIR": str(runtime["tmp"]),
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0",
        "PYTHONNOUSERSITE": "1",
        "LC_ALL": "C",
        "LANG": "C",
        "TZ": "UTC",
        "SOURCE_DATE_EPOCH": source_date_epoch,
    }


def bootstrap_environment() -> dict[str, str]:
    """Read-only environment used before any excluded runtime path exists."""
    return {
        "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
        "HOME": "/",
        "TMPDIR": "/tmp",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0",
        "PYTHONNOUSERSITE": "1",
        "LC_ALL": "C",
        "LANG": "C",
        "TZ": "UTC",
        "SOURCE_DATE_EPOCH": "0",
    }


def check_python(python: Path, environment: dict[str, str]) -> None:
    require(python.is_file() and os.access(python, os.X_OK),
            ("Python interpreter is not executable", str(python)))
    returncode, output = run_captured(
        [str(python), "-c",
         "import mpmath, networkx, numpy, sympy; print('DEPENDENCIES_OK')"],
        cwd=python.parent, environment=environment, timeout_seconds=60,
    )
    require(returncode == 0 and "DEPENDENCIES_OK" in output,
            ("required Python dependencies unavailable", output[-2000:]))


def runtime_metadata(python: Path, package_root: Path,
                     environment: dict[str, str]) -> dict[str, object]:
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
    returncode, output = run_captured(
        [str(python), "-c", script],
        cwd=package_root, environment=environment, timeout_seconds=60,
    )
    require(returncode == 0, ("runtime metadata failed", output))
    value = json.loads(output)
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


def process_group_exists(process_group: int) -> bool:
    try:
        os.killpg(process_group, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        # Some Unix kernels transiently report EPERM while a just-signalled
        # group contains only unreaped processes.  Treat it as present and
        # keep the cleanup path fail-closed.
        return True


def terminate_process_group(process: subprocess.Popen, *, grace: float = 5.0) -> None:
    process_group = process.pid
    try:
        os.killpg(process_group, signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        pass
    if process.poll() is None:
        try:
            process.wait(timeout=grace)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process_group, signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                pass
            try:
                process.wait(timeout=grace)
            except subprocess.TimeoutExpired as error:
                raise ReviewFailure(
                    ("cannot reap interrupted command", process_group)
                ) from error
    # The direct child may have exited while descendants remain in its group.
    try:
        os.killpg(process_group, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass
    deadline = time.monotonic() + grace
    while process_group_exists(process_group) and time.monotonic() < deadline:
        time.sleep(0.05)
    require(not process_group_exists(process_group),
            ("descendant process group survived termination", process_group))


def run_captured(argv: list[str], *, cwd: Path,
                 environment: dict[str, str],
                 timeout_seconds: float) -> tuple[int, str]:
    process = subprocess.Popen(
        argv, cwd=cwd, env=environment, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    try:
        output, _ = process.communicate(timeout=timeout_seconds)
    except subprocess.TimeoutExpired as error:
        terminate_process_group(process)
        raise ReviewFailure(("captured command timeout", argv[0])) from error
    except BaseException:
        terminate_process_group(process)
        raise
    if process_group_exists(process.pid):
        terminate_process_group(process)
        raise ReviewFailure(("captured command left descendants", argv[0]))
    return process.returncode, output


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
        terminate_process_group(process)
        raise ReviewFailure(("command timeout", name, timeout_seconds)) from error
    except BaseException:
        terminate_process_group(process)
        raise
    if process_group_exists(process.pid):
        terminate_process_group(process)
        raise ReviewFailure(("command left descendant processes", name))
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
                                        canonical_mode: int,
                                        label: str) -> dict[str, object]:
    relative = "reproducibility/primary_gate_report.json"
    path = workspace / relative
    require(path.is_file(), ("missing regenerated primary report", relative))
    current_bytes = path.read_bytes()
    current_mode = stat.S_IMODE(path.stat().st_mode)
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
    evidence.chmod(current_mode)
    path.write_bytes(canonical_bytes)
    path.chmod(canonical_mode)
    require(path.read_bytes() == canonical_bytes and
            stat.S_IMODE(path.stat().st_mode) == canonical_mode,
            "canonical primary report bytes and mode were not restored")
    return {
        "path": evidence.relative_to(package_root).as_posix(),
        "bytes": evidence.stat().st_size,
        "sha256": sha256_file(evidence),
        "mode": mode_string(evidence.stat().st_mode),
        "canonical_mode_restored": mode_string(path.stat().st_mode),
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
    virtual_environment = python.parent.parent.resolve()
    require((virtual_environment / "pyvenv.cfg").is_file(),
            ("runner Python is not in a virtual environment", str(python)))
    (workspace / ".venv").symlink_to(
        virtual_environment, target_is_directory=True
    )
    environment = deterministic_environment(workspace)
    before = filesystem_inventory(workspace)
    virtual_environment_before = filesystem_inventory(virtual_environment)
    before_record = write_inventory(
        phase_root / "workspace_inventory_before.json", workspace, before
    )
    virtual_environment_before_record = write_inventory(
        phase_root / "virtual_environment_inventory_before.json",
        virtual_environment, virtual_environment_before,
    )
    output_mode_control = run_output_mode_control(
        package_root, workspace, python, environment,
    )
    primary_path = workspace / "reproducibility/primary_gate_report.json"
    require(primary_path.is_file(), "canonical primary report missing")
    canonical_primary_bytes = primary_path.read_bytes()
    canonical_primary_mode = stat.S_IMODE(primary_path.stat().st_mode)
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
            "environment": environment,
            "umask": "0022",
            "external_sandbox_attested": True,
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
                    canonical_mode=canonical_primary_mode,
                    label=f"{command['name']}_location_dependent_primary_report",
                ))
    supplemental_outputs.append(bind_fresh_replay_report(
        workspace=workspace, phase_root=phase_root, package_root=package_root,
    ))
    after = filesystem_inventory(workspace)
    virtual_environment_after = filesystem_inventory(virtual_environment)
    after_record = write_inventory(
        phase_root / "workspace_inventory_after.json", workspace, after
    )
    virtual_environment_after_record = write_inventory(
        phase_root / "virtual_environment_inventory_after.json",
        virtual_environment, virtual_environment_after,
    )
    for record in (
        before_record, after_record,
        virtual_environment_before_record, virtual_environment_after_record,
    ):
        record["path"] = Path(record["path"]).relative_to(package_root).as_posix()
    complete_workspace_drift = drift(before, after)
    all_changed_paths = drift_paths(complete_workspace_drift)
    declared_runtime_paths = {
        path for path in all_changed_paths
        if path == "release/work" or path.startswith("release/work/")
    }
    undeclared_paths = all_changed_paths - declared_runtime_paths
    workspace_drift = restrict_drift(complete_workspace_drift, undeclared_paths)
    declared_runtime_drift = restrict_drift(
        complete_workspace_drift, declared_runtime_paths
    )
    require(workspace_drift == {"added": [], "removed": [], "changed": []},
            ("unexpected workspace drift", workspace_drift))
    virtual_environment_drift = drift(
        virtual_environment_before, virtual_environment_after
    )
    require(virtual_environment_drift == {
        "added": [], "removed": [], "changed": [],
    }, ("virtual-environment drift", virtual_environment_drift))
    report = {
        "schema": "k3p-independent-referee-run-v2",
        "status": "PASS",
        "phase": phase,
        "command_count": len(records),
        "commands": records,
        "supplemental_outputs": supplemental_outputs,
        "output_mode_control": output_mode_control,
        "runtime": runtime,
        "elapsed_seconds": time.monotonic() - started,
        "execution_boundary": {
            "child_environment_allowlist": sorted(environment),
            "external_sandbox_attested": True,
            "external_sandbox_enforced_by_runner": False,
            "umask": "0022",
            "workspace_copy_is_git_free": True,
        },
        "filesystem_inventories": {
            "workspace_before": before_record,
            "workspace_after": after_record,
            "virtual_environment_before": virtual_environment_before_record,
            "virtual_environment_after": virtual_environment_after_record,
        },
        "complete_workspace_drift": complete_workspace_drift,
        "declared_runtime_drift": declared_runtime_drift,
        "workspace_drift": workspace_drift,
        "virtual_environment_drift": virtual_environment_drift,
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


def run_integrity(package_root: Path, python: Path,
                  environment: dict[str, str]) -> None:
    command = [
        str(python), str(package_root / "referee_tools/verify_package_integrity.py"),
        "--package-root", str(package_root),
    ]
    returncode, output = run_captured(
        command, cwd=package_root, environment=environment, timeout_seconds=600,
    )
    require(returncode == 0 and
            "K3P_REFEREE_PACKAGE_INTEGRITY_PASS" in output,
            ("package integrity check failed", output[-4000:]))
    print(output, end="")


def run_output_mode_control(package_root: Path, project_root: Path,
                            python: Path,
                            environment: dict[str, str]) -> dict[str, object]:
    command = [
        str(python),
        str(package_root / "referee_tools/test_output_mode_preservation.py"),
        "--project-root", str(project_root),
    ]
    returncode, output = run_captured(
        command, cwd=package_root, environment=environment, timeout_seconds=120,
    )
    require(returncode == 0 and "K3P_OUTPUT_MODE_PRESERVATION_PASS" in output,
            ("output-mode preservation control failed", output[-4000:]))
    print(output, end="")
    return {
        "status": "PASS",
        "sentinel": "K3P_OUTPUT_MODE_PRESERVATION_PASS",
        "stdout_bytes": len(output.encode("utf-8")),
        "stdout_sha256": sha256_bytes(output.encode("utf-8")),
    }


def acquire_lock(package_root: Path, mode: str) -> tuple[int, int, Path, tuple[int, int]]:
    prepare_runtime_control(package_root)
    runtime_descriptor, runtime = open_private_directory_chain(
        package_root, ("review_runs",)
    )
    path = runtime / ".active_runner.lock"
    try:
        descriptor = os.open(
            path.name, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600,
            dir_fd=runtime_descriptor,
        )
    except FileExistsError as error:
        os.close(runtime_descriptor)
        raise ReviewFailure((
            "another runner owns the atomic lock; do not launch a duplicate; "
            "after confirming that no runner remains, remove",
            str(path),
        )) from error
    except BaseException:
        os.close(runtime_descriptor)
        raise
    try:
        record = json.dumps({
            "schema": "k3p-referee-run-lock-v1",
            "pid": os.getpid(),
            "mode": mode,
            "started_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        }, sort_keys=True).encode("utf-8") + b"\n"
        os.write(descriptor, record)
        os.fsync(descriptor)
        metadata = os.fstat(descriptor)
        return (descriptor, runtime_descriptor, path,
                (metadata.st_dev, metadata.st_ino))
    except BaseException:
        try:
            os.unlink(path.name, dir_fd=runtime_descriptor)
        except FileNotFoundError:
            pass
        os.close(descriptor)
        os.close(runtime_descriptor)
        raise


def release_lock(lock: tuple[int, int, Path, tuple[int, int]]) -> None:
    descriptor, runtime_descriptor, path, identity = lock
    try:
        metadata = os.stat(
            path.name, dir_fd=runtime_descriptor, follow_symlinks=False
        )
        require(not stat.S_ISLNK(metadata.st_mode) and
                stat.S_ISREG(metadata.st_mode) and
                (metadata.st_dev, metadata.st_ino) == identity,
                ("runner lock was replaced", str(path)))
        os.unlink(path.name, dir_fd=runtime_descriptor)
    finally:
        os.close(descriptor)
        os.close(runtime_descriptor)


def interrupted(signum: int, _frame) -> None:
    raise ReviewFailure(("runner interrupted by signal", signum))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path,
                        default=Path(__file__).resolve().parents[1])
    parser.add_argument("--python", type=Path)
    parser.add_argument("--mode", choices=("plan", "verify", "regenerate", "all"),
                        default="verify")
    parser.add_argument("--prepare-runtime-only", action="store_true",
                        help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    package_root = args.package_root.resolve()
    # Preserve a virtual-environment interpreter path rather than resolving its
    # symlink to the base interpreter, which would discard the venv context.
    python = (Path(os.path.abspath(args.python)) if args.python else
              package_root / ".venv/bin/python")
    sandbox_attested = os.environ.get("K3P_REFEREE_EXTERNAL_SANDBOX") == "YES"
    regeneration_confirmed = (
        os.environ.get("K3P_REFEREE_CONFIRM_REGENERATION") == "YES"
    )
    os.umask(0o022)
    lock = None
    previous_handlers: dict[int, object] = {}
    try:
        require(sandbox_attested,
                "set K3P_REFEREE_EXTERNAL_SANDBOX=YES only after supplying "
                "an external offline, credential-free sandbox")
        read_only_environment = bootstrap_environment()
        run_integrity(
            package_root, Path(sys.executable), read_only_environment
        )
        if args.prepare_runtime_only:
            runtime_paths = prepare_runtime_control(package_root)
            print(json.dumps({
                "status": "PASS",
                "runtime_paths": {
                    name: path.relative_to(package_root).as_posix()
                    for name, path in runtime_paths.items()
                },
                "modes": {
                    name: mode_string(path.lstat().st_mode)
                    for name, path in runtime_paths.items()
                },
            }, sort_keys=True))
            print("K3P_REFEREE_RUNTIME_SETUP_PASS")
            return 0
        lock = acquire_lock(package_root, args.mode)
        for signum in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
            previous_handlers[signum] = signal.getsignal(signum)
            signal.signal(signum, interrupted)
        manifest = json.loads(
            (package_root / "proof_package/ARCHIVE_MANIFEST.json").read_text()
        )
        environment = control_environment(
            package_root, str(manifest["source_date_epoch"])
        )
        os.environ.clear()
        os.environ.update(environment)
        check_python(python, environment)
        runtime = runtime_metadata(python, package_root, environment)
        plan = load_plan(package_root)
        if args.mode == "plan":
            commands = regeneration_commands(
                plan, python, package_root / "proof_package"
            )
            run_integrity(package_root, Path(sys.executable), environment)
            print(json.dumps({
                "status": "PASS",
                "atomic_lock": "HELD_DURING_PLAN",
                "child_environment_allowlist": sorted(environment),
                "external_sandbox_attested": True,
                "external_sandbox_enforced_by_runner": False,
                "umask": "0022",
                "mathematical_regeneration_commands": len(commands),
                "ordered_names": [command["name"] for command in commands],
            }, sort_keys=True))
            print("K3P_REFEREE_REGENERATION_PLAN_PASS")
            return 0
        if args.mode in {"regenerate", "all"}:
            require(regeneration_confirmed,
                    "set K3P_REFEREE_CONFIRM_REGENERATION=YES for the long run")
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
        session_root = package_root / "review_runs" / stamp
        session_root.mkdir(parents=True, exist_ok=False)
        phases = ["verify", "regenerate"] if args.mode == "all" else [args.mode]
        reports = [run_phase(
            phase=phase, package_root=package_root, python=python,
            session_root=session_root, plan=plan, runtime=runtime,
        ) for phase in phases]
        run_integrity(package_root, Path(sys.executable), environment)
        summary = {
            "status": "PASS",
            "mode": args.mode,
            "atomic_lock": "HELD_DURING_RUN",
            "external_sandbox_attested": True,
            "external_sandbox_enforced_by_runner": False,
            "umask": "0022",
            "package_integrity_postflight": "PASS",
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
    except (ReviewFailure, KeyboardInterrupt, OSError, UnicodeError,
            json.JSONDecodeError, subprocess.SubprocessError,
            TypeError, ValueError) as error:
        print(f"K3P_REFEREE_ACTIVE_VERIFIERS_FAIL: {error}", file=sys.stderr)
        return 1
    finally:
        for signum, handler in previous_handlers.items():
            signal.signal(signum, handler)
        if lock is not None:
            release_lock(lock)


if __name__ == "__main__":
    raise SystemExit(main())
