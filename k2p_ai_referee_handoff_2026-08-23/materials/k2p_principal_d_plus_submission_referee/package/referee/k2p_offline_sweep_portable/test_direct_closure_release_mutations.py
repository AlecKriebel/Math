#!/usr/bin/env python3
"""Adversarial mutation suite for the direct-closure release verifier.

Every content mutation is made in an isolated hard-link clone, followed by a
fresh lock rebuild.  Atomic replacement breaks the mutated file's hard link,
so no byte in the source release can be modified by this test.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parent


def fail(code: str, detail: object = None) -> "None":
    raise SystemExit(code if detail is None else f"{code}: {detail}")


def hardlink_or_copy(source: str, destination: str) -> str:
    try:
        os.link(source, destination)
    except OSError:
        shutil.copy2(source, destination)
    return destination


def clone_release(source: Path, destination: Path) -> None:
    ignored = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", ".DS_Store")
    shutil.copytree(
        source,
        destination,
        symlinks=False,
        copy_function=hardlink_or_copy,
        ignore=ignored,
    )


def atomic_bytes(path: Path, content: bytes) -> None:
    temporary = path.with_name(f"{path.name}.mutation.{os.getpid()}")
    with temporary.open("wb") as handle:
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        fail("MUTATION_INPUT_JSON_FAIL", f"{path}: {exc}")
    if not isinstance(value, dict):
        fail("MUTATION_INPUT_JSON_OBJECT_FAIL", path)
    return value


def write_json(path: Path, value: dict) -> None:
    atomic_bytes(path, (json.dumps(value, indent=2, sort_keys=True) + "\n").encode())


def child_environment() -> dict[str, str]:
    environment = dict(os.environ)
    environment.pop("PYTHONOPTIMIZE", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment.setdefault("PYTHONHASHSEED", "0")
    return environment


def run(command: list[str], cwd: Path, timeout_seconds: float) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            env=child_environment(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        fail("MUTATION_SUBPROCESS_TIMEOUT", command)


def rebuild_lock(root: Path, timeout_seconds: float) -> None:
    result = run(
        [sys.executable, "-B", str(root / "build_direct_closure_lock.py")],
        root, timeout_seconds,
    )
    if result.returncode != 0 or b"DIRECT_CLOSURE_LOCK_WRITTEN" not in result.stdout:
        fail("MUTATION_LOCK_REBUILD_FAIL", (result.stdout + result.stderr).decode(errors="replace"))


def invoke_verifier(root: Path, timeout_seconds: float, optimized: bool = False) -> subprocess.CompletedProcess[bytes]:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend((
        "-B", str(root / "verify_direct_closure_release.py"),
        "--package-root", str(root), "--quick",
        "--timeout-seconds", str(timeout_seconds),
    ))
    return run(command, root, timeout_seconds + 15)


def require_pass(result: subprocess.CompletedProcess[bytes], label: str) -> None:
    output = result.stdout + result.stderr
    if result.returncode != 0 or b"K2P_FOUR_PORT_DIRECT_CLOSURE_RELEASE_PASS" not in output.splitlines():
        fail(f"{label}_BASELINE_FAIL", output.decode(errors="replace")[-5000:])


def require_rejection(
    result: subprocess.CompletedProcess[bytes],
    label: str,
    marker: bytes,
) -> dict[str, object]:
    output = result.stdout + result.stderr
    if result.returncode == 0:
        fail(f"{label}_FALSE_ACCEPT", output.decode(errors="replace")[-5000:])
    if result.returncode < 0:
        fail(f"{label}_SIGNAL_EXIT", result.returncode)
    if marker not in output:
        fail(
            f"{label}_WRONG_REJECTION",
            {"wanted": marker.decode(), "output": output.decode(errors="replace")[-5000:]},
        )
    return {
        "case": label,
        "returncode": result.returncode,
        "required_marker": marker.decode(),
        "output_sha256": hashlib.sha256(output).hexdigest(),
    }


def mutate_merged_root(root: Path) -> None:
    path = root / "results/four_port_release_v4/FOUR_PORT_SWEEP_MERGED_STATUS.json"
    value = load_json(path)
    value["semantic_sweep_sha256"] = "0" * 64
    write_json(path, value)


def mutate_manifest_status(root: Path) -> None:
    path = root / "results/four_port_release_v4/source_1/residual_manifest.json"
    value = load_json(path)
    value["records"][25]["status"] = "separated"
    write_json(path, value)


def mutate_manifest_unresolved(root: Path) -> None:
    path = root / "results/four_port_release_v4/source_1/residual_manifest.json"
    value = load_json(path)
    value["unresolved"] = value["unresolved"][1:]
    write_json(path, value)


def mutate_missing_candidate(root: Path) -> None:
    (root / "results/four_port_release_v4/source_1/records/class_000025.json").unlink()


def mutate_swapped_candidates(root: Path) -> None:
    first = root / "results/four_port_release_v4/source_1/records/class_000025.json"
    second = root / "results/four_port_release_v4/source_1/records/class_000026.json"
    first_bytes, second_bytes = first.read_bytes(), second.read_bytes()
    atomic_bytes(first, second_bytes)
    atomic_bytes(second, first_bytes)


def mutate_record_port(root: Path) -> None:
    path = root / "results/four_port_release_v4/source_1/records/class_000025.json"
    value = load_json(path)
    replacement = [0, 2, 3, 1]
    value["port_match"] = replacement
    value["port_matches"] = [replacement]
    value["members"][0]["port_match"] = replacement
    write_json(path, value)


def mutate_record_semantic_hash(root: Path) -> None:
    path = root / "results/four_port_release_v4/source_1/records/class_000025.json"
    value = load_json(path)
    value["semantic_record_sha256"] = "0" * 64
    write_json(path, value)


def mutate_quintic_coefficient(root: Path) -> None:
    path = root / "proofs/theta0_quintic_orbit_certificate.json"
    value = load_json(path)
    value["invariant"][0][1] += 1
    write_json(path, value)


def mutate_quartic_coefficient(root: Path) -> None:
    path = root / "proofs/theta_quartic_obstruction_certificates.json"
    value = load_json(path)
    value["certificates"][0]["terms"][0][0] += 1
    write_json(path, value)


def mutate_cubic_coefficient(root: Path) -> None:
    path = root / "proofs/theta3_cubic_obstruction_certificate.json"
    value = load_json(path)
    value["normalized_terms"][0][0] += 1
    write_json(path, value)


Mutation = tuple[str, Callable[[Path], None], bytes]
MUTATIONS: tuple[Mutation, ...] = (
    ("merged_root", mutate_merged_root, b"RELEASE_MERGED_MISMATCH"),
    ("manifest_status", mutate_manifest_status, b"RELEASE_MANIFEST_STATUS_CENSUS_MISMATCH"),
    ("manifest_unresolved", mutate_manifest_unresolved, b"RELEASE_MANIFEST_UNRESOLVED_MISMATCH"),
    ("missing_candidate", mutate_missing_candidate, b"RELEASE_RECORD_SET_MISMATCH"),
    ("swapped_candidate_records", mutate_swapped_candidates, b"RELEASE_RECORD_IDENTITY_MISMATCH"),
    ("port_record", mutate_record_port, b"RELEASE_RECORD_SEMANTIC_HASH_MISMATCH"),
    ("semantic_record", mutate_record_semantic_hash, b"RELEASE_RECORD_SEMANTIC_HASH_MISMATCH"),
    ("quintic_coefficient", mutate_quintic_coefficient, b"DIRECT_OVERLAY_REPLAY_FAIL"),
    ("quartic_coefficient", mutate_quartic_coefficient, b"DIRECT_OVERLAY_REPLAY_FAIL"),
    ("cubic_coefficient", mutate_cubic_coefficient, b"DIRECT_OVERLAY_REPLAY_FAIL"),
)


def main() -> None:
    if not __debug__:
        fail("DIRECT_CLOSURE_MUTATION_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, default=ROOT)
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    parser.add_argument("--case", action="append", choices=[name for name, _mutation, _marker in MUTATIONS])
    args = parser.parse_args()
    if args.timeout_seconds <= 0:
        fail("MUTATION_TIMEOUT_INVALID")
    source = args.package_root.resolve()
    selected = set(args.case) if args.case else {name for name, _mutation, _marker in MUTATIONS}
    results: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="k2p_direct_closure_mutations_") as temporary:
        temporary_root = Path(temporary)
        baseline = temporary_root / "baseline"
        clone_release(source, baseline)
        rebuild_lock(baseline, args.timeout_seconds)
        require_pass(invoke_verifier(baseline, args.timeout_seconds), "MUTATION_SUITE")
        optimized = invoke_verifier(baseline, args.timeout_seconds, optimized=True)
        results.append(require_rejection(
            optimized, "optimized_mode", b"DIRECT_CLOSURE_OPTIMIZED_MODE_FORBIDDEN"
        ))
        for name, mutation, marker in MUTATIONS:
            if name not in selected:
                continue
            case_root = temporary_root / name
            clone_release(baseline, case_root)
            mutation(case_root)
            rebuild_lock(case_root, args.timeout_seconds)
            result = invoke_verifier(case_root, args.timeout_seconds)
            results.append(require_rejection(result, name, marker))
            print(f"DIRECT_CLOSURE_MUTATION_REJECTED case={name}")
    print("DIRECT_CLOSURE_RELEASE_MUTATIONS_PASS")
    print(json.dumps({"rejections": results}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
