#!/usr/bin/env python3
"""Adversarial mutation suite for the direct-closure release verifier.

Every content mutation is made in an isolated hard-link clone, followed by a
fresh lock rebuild.  Atomic replacement breaks the mutated file's hard link,
so no byte in the source release can be modified by this test.
"""

from __future__ import annotations

if not __debug__:
    raise SystemExit("DIRECT_CLOSURE_MUTATION_OPTIMIZED_MODE_FORBIDDEN")

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[2]
AUTHORITATIVE_OUTPUT = ROOT / "direct_closure_mutation_report.json"
SCHEMA = "k2p-four-port-direct-closure-mutations-v2"
SUCCESS_TERMINAL = "K2P_FOUR_PORT_DIRECT_CLOSURE_RELEASE_PASS"
FORBIDDEN_FAILURE_TEXT = (
    "Traceback (most recent call last)",
    "AssertionError",
    "ModuleNotFoundError",
    "ImportError",
)
DIAGNOSTIC_TOKEN = re.compile(r"(?<![A-Z0-9_])(?:DIRECT|RELEASE)_[A-Z0-9_]+(?![A-Z0-9_])")


def fail(code: str, detail: object = None) -> "None":
    raise SystemExit(code if detail is None else f"{code}: {detail}")


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_object(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def validate_output_path(output: Path, allow_authoritative: bool = False) -> Path:
    """Allow routine reports only outside the source tree.

    An explicit maintainer override licenses exactly the canonical report path.
    Resolving both lexical and target paths rejects aliases into project files.
    """

    lexical = Path(os.path.abspath(os.fspath(output)))
    normalized = lexical.parent.resolve() / lexical.name
    resolved = lexical.resolve()
    canonical = AUTHORITATIVE_OUTPUT.parent.resolve() / AUTHORITATIVE_OUTPUT.name
    if allow_authoritative:
        if normalized != canonical or resolved != canonical:
            fail(
                "DIRECT_CLOSURE_MUTATION_OUTPUT_POLICY_FAIL",
                "authoritative override requires the exact nonsymbolic canonical report",
            )
        return canonical
    try:
        resolved.relative_to(PROJECT.resolve())
    except ValueError:
        return normalized
    fail(
        "DIRECT_CLOSURE_MUTATION_OUTPUT_POLICY_FAIL",
        "routine report output must be outside the project source tree",
    )


def prepare_output(output: Path) -> None:
    """Remove stale caller-owned PASS bytes before every fallible preflight."""

    output.unlink(missing_ok=True)


def atomic_write_bytes(path: Path, content: bytes) -> None:
    """Replace atomically without following hard links or late symlink swaps."""

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o644)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        temporary.unlink(missing_ok=True)


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


def check_lock(root: Path, timeout_seconds: float) -> None:
    result = run(
        [sys.executable, "-B", str(root / "build_direct_closure_lock.py"), "--check"],
        root,
        timeout_seconds,
    )
    output = result.stdout + result.stderr
    if (
        result.returncode != 0
        or b"DIRECT_CLOSURE_LOCK_PASS" not in output.splitlines()
        or any(token.encode() in output for token in FORBIDDEN_FAILURE_TEXT)
    ):
        fail("MUTATION_SOURCE_LOCK_BASELINE_FAIL", output.decode(errors="replace")[-5000:])


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


def require_pass(result: subprocess.CompletedProcess[bytes], label: str) -> dict[str, object]:
    output = result.stdout + result.stderr
    lines = output.decode("utf-8", errors="replace").splitlines()
    if (
        result.returncode != 0
        or SUCCESS_TERMINAL not in lines
        or any(token in "\n".join(lines) for token in FORBIDDEN_FAILURE_TEXT)
    ):
        fail(f"{label}_BASELINE_FAIL", output.decode(errors="replace")[-5000:])
    return {
        "returncode": 0,
        "terminal": SUCCESS_TERMINAL,
        "stderr_empty": result.stderr == b"",
    }


def completed_observation(result: subprocess.CompletedProcess[bytes]) -> dict[str, object]:
    output = (result.stdout + result.stderr).decode("utf-8", errors="replace")
    return {
        "returncode": result.returncode,
        "output": output,
        "timeout": False,
        "signal": result.returncode < 0,
        "success_artifact_present": SUCCESS_TERMINAL in output.splitlines(),
    }


def rejection_codes(output: str) -> set[str]:
    return {
        token
        for token in DIAGNOSTIC_TOKEN.findall(output)
        if not token.endswith(("_PASS", "_WRITTEN"))
    }


def normalized_diagnostic(name: str, output: str) -> str | None:
    """Normalize only licensed extraction-dependent absolute path details."""

    expected = MUTATION_DIAGNOSTICS[name]
    stripped = output.strip()
    if stripped == expected:
        return expected
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    if name == "optimized_mode":
        return expected if expected in lines else None
    path_cases = {
        "merged_root": "FOUR_PORT_SWEEP_MERGED_STATUS.json",
        "manifest_status": "source_1/residual_manifest.json",
        "manifest_unresolved": "source_1/residual_manifest.json",
        "swapped_candidate_records": "source_1/records/class_000025.json",
        "port_record": "source_1/records/class_000025.json",
        "semantic_record": "source_1/records/class_000025.json",
    }
    if name in path_cases:
        prefix = MUTATION_PRIMARY_CODES[name] + ": "
        candidates = [line[len(prefix) :] for line in lines if line.startswith(prefix)]
        if len(candidates) != 1:
            return None
        detail = candidates[0]
        suffix = path_cases[name]
        if not Path(detail).is_absolute() or not detail.replace("\\", "/").endswith(suffix):
            return None
        return expected
    if name == "missing_candidate":
        return expected if expected in lines else None
    coefficient_lines = {
        "quintic_coefficient": (
            "DIRECT_OVERLAY_REPLAY_FAIL: DIRECT_QUINTIC_ARTIFACT_HASH_FAIL"
        ),
        "quartic_coefficient": (
            "DIRECT_OVERLAY_REPLAY_FAIL: DIRECT_QUARTIC_EXPECTED_HASH_FAIL: F112"
        ),
        "cubic_coefficient": (
            "DIRECT_OVERLAY_REPLAY_FAIL: DIRECT_CUBIC_ARTIFACT_TERMS_FAIL"
        ),
    }
    if name in coefficient_lines:
        return expected if coefficient_lines[name] in lines else None
    return None


def qualify_mutation_failure(
    name: str, observation: dict[str, object]
) -> dict[str, object]:
    expected = MUTATION_DIAGNOSTICS[name]
    output = str(observation.get("output", ""))
    returncode = observation.get("returncode")
    if observation.get("timeout") is not False:
        fail("DIRECT_CLOSURE_MUTATION_TIMEOUT", name)
    if observation.get("signal") is not False or (
        isinstance(returncode, int) and returncode < 0
    ):
        fail("DIRECT_CLOSURE_MUTATION_SIGNAL_EXIT", name)
    if returncode != 1:
        fail(
            "DIRECT_CLOSURE_MUTATION_EXIT_CODE_FAIL",
            {"case": name, "returncode": returncode},
        )
    forbidden = [token for token in FORBIDDEN_FAILURE_TEXT if token in output]
    if forbidden:
        fail(
            "DIRECT_CLOSURE_MUTATION_UNRELATED_CRASH",
            {"case": name, "forbidden": forbidden},
        )
    if observation.get("success_artifact_present") is not False:
        fail("DIRECT_CLOSURE_MUTATION_SUCCESS_ARTIFACT", name)
    codes = rejection_codes(output)
    expected_codes = MUTATION_ALLOWED_CODES[name]
    observed_diagnostic = normalized_diagnostic(name, output)
    if codes != expected_codes or observed_diagnostic != expected:
        fail(
            "DIRECT_CLOSURE_MUTATION_DIAGNOSTIC_FAIL",
            {
                "case": name,
                "expected": expected,
                "observed": observed_diagnostic,
                "expected_codes": sorted(expected_codes),
                "observed_codes": sorted(codes),
            },
        )
    return {
        "case": name,
        "returncode": 1,
        "expected_diagnostic": expected,
        "observed_diagnostic": observed_diagnostic,
        "observed_diagnostic_codes": sorted(codes),
        "timeout": False,
        "signal": False,
        "success_artifact_present": False,
        "forbidden_crash_text_present": False,
    }


def require_rejection(
    result: subprocess.CompletedProcess[bytes],
    label: str,
    _legacy_marker: bytes | None = None,
) -> dict[str, object]:
    return qualify_mutation_failure(label, completed_observation(result))


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

MUTATION_PRIMARY_CODES = {
    "optimized_mode": "DIRECT_CLOSURE_OPTIMIZED_MODE_FORBIDDEN",
    "merged_root": "RELEASE_MERGED_MISMATCH",
    "manifest_status": "RELEASE_MANIFEST_STATUS_CENSUS_MISMATCH",
    "manifest_unresolved": "RELEASE_MANIFEST_UNRESOLVED_MISMATCH",
    "missing_candidate": "RELEASE_RECORD_SET_MISMATCH",
    "swapped_candidate_records": "RELEASE_RECORD_IDENTITY_MISMATCH",
    "port_record": "RELEASE_RECORD_SEMANTIC_HASH_MISMATCH",
    "semantic_record": "RELEASE_RECORD_SEMANTIC_HASH_MISMATCH",
    "quintic_coefficient": "DIRECT_QUINTIC_ARTIFACT_HASH_FAIL",
    "quartic_coefficient": "DIRECT_QUARTIC_EXPECTED_HASH_FAIL",
    "cubic_coefficient": "DIRECT_CUBIC_ARTIFACT_TERMS_FAIL",
}
MUTATION_DIAGNOSTICS = {
    "optimized_mode": (
        "DIRECT_CLOSURE_OPTIMIZED_MODE_FORBIDDEN: invoke Python without -O"
    ),
    "merged_root": (
        "RELEASE_MERGED_MISMATCH:<FOUR_PORT_SWEEP_MERGED_STATUS.json>"
    ),
    "manifest_status": (
        "RELEASE_MANIFEST_STATUS_CENSUS_MISMATCH:<source_1/residual_manifest.json>"
    ),
    "manifest_unresolved": (
        "RELEASE_MANIFEST_UNRESOLVED_MISMATCH:<source_1/residual_manifest.json>"
    ),
    "missing_candidate": (
        "RELEASE_RECORD_SET_MISMATCH: {'missing': "
        "['source_1/records/class_000025.json'], 'extra': []}"
    ),
    "swapped_candidate_records": (
        "RELEASE_RECORD_IDENTITY_MISMATCH:"
        "<source_1/records/class_000025.json>"
    ),
    "port_record": (
        "RELEASE_RECORD_SEMANTIC_HASH_MISMATCH:"
        "<source_1/records/class_000025.json>"
    ),
    "semantic_record": (
        "RELEASE_RECORD_SEMANTIC_HASH_MISMATCH:"
        "<source_1/records/class_000025.json>"
    ),
    "quintic_coefficient": (
        "DIRECT_OVERLAY_REPLAY_FAIL:DIRECT_QUINTIC_ARTIFACT_HASH_FAIL"
    ),
    "quartic_coefficient": (
        "DIRECT_OVERLAY_REPLAY_FAIL:DIRECT_QUARTIC_EXPECTED_HASH_FAIL:F112"
    ),
    "cubic_coefficient": (
        "DIRECT_OVERLAY_REPLAY_FAIL:DIRECT_CUBIC_ARTIFACT_TERMS_FAIL"
    ),
}
MUTATION_ALLOWED_CODES = {
    name: {code} for name, code in MUTATION_PRIMARY_CODES.items()
}
for _coefficient_case in (
    "quintic_coefficient",
    "quartic_coefficient",
    "cubic_coefficient",
):
    MUTATION_ALLOWED_CODES[_coefficient_case].add("DIRECT_OVERLAY_REPLAY_FAIL")


def qualification_negative_controls() -> dict[str, bool]:
    """Prove that only the exact production-verifier failure can qualify."""

    name = "merged_root"
    expected = MUTATION_DIAGNOSTICS[name]
    valid = {
        "returncode": 1,
        "output": expected,
        "timeout": False,
        "signal": False,
        "success_artifact_present": False,
    }
    controls = {
        "wrong_diagnostic_rejected": {**valid, "output": "RELEASE_LOCK_MISMATCH"},
        "traceback_rejected": {
            **valid,
            "output": f"Traceback (most recent call last):\nRuntimeError: {expected}",
        },
        "import_error_rejected": {
            **valid,
            "output": f"ModuleNotFoundError: dependency\n{expected}",
        },
        "timeout_rejected": {**valid, "returncode": None, "timeout": True},
        "signal_rejected": {**valid, "returncode": -9, "signal": True},
        "non_one_exit_rejected": {**valid, "returncode": 2},
        "success_artifact_rejected": {
            **valid,
            "output": f"{expected}\n{SUCCESS_TERMINAL}",
            "success_artifact_present": True,
        },
    }
    results: dict[str, bool] = {}
    for label, observation in controls.items():
        try:
            qualify_mutation_failure(name, observation)
        except SystemExit:
            results[label] = True
        else:
            fail("DIRECT_CLOSURE_MUTATION_NEGATIVE_CONTROL_SURVIVED", label)
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, default=ROOT)
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    parser.add_argument("--case", action="append", choices=[name for name, _mutation, _marker in MUTATIONS])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-authoritative-output", action="store_true")
    args = parser.parse_args()
    output_path = validate_output_path(args.output, args.allow_authoritative_output)
    prepare_output(output_path)
    if args.timeout_seconds <= 0:
        fail("MUTATION_TIMEOUT_INVALID")
    source = args.package_root.resolve()
    selected = set(args.case) if args.case else {name for name, _mutation, _marker in MUTATIONS}
    source_fingerprints = {
        "direct_closure_lock_sha256": sha_file(source / "DIRECT_CLOSURE_LOCK.json"),
        "production_verifier_sha256": sha_file(source / "verify_direct_closure_release.py"),
        "overlay_verifier_sha256": sha_file(
            source / "proofs/verify_four_port_direct_residual_closure.py"
        ),
        "mutation_runner_sha256": sha_file(Path(__file__).resolve()),
        "direct_overlay_certificate_sha256": sha_file(
            source / "proofs/four_port_direct_residual_closure_certificate.json"
        ),
    }
    check_lock(source, args.timeout_seconds)
    baseline = require_pass(
        invoke_verifier(source, args.timeout_seconds), "MUTATION_SUITE"
    )
    baseline.update(
        {
            "source_lock_checked_in_place": True,
            "production_verifier_sha256": source_fingerprints[
                "production_verifier_sha256"
            ],
        }
    )
    negative_controls = qualification_negative_controls()
    results: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="k2p_direct_closure_mutations_") as temporary:
        temporary_root = Path(temporary)
        optimized = invoke_verifier(source, args.timeout_seconds, optimized=True)
        results.append(require_rejection(
            optimized, "optimized_mode", b"DIRECT_CLOSURE_OPTIMIZED_MODE_FORBIDDEN"
        ))
        for name, mutation, marker in MUTATIONS:
            if name not in selected:
                continue
            case_root = temporary_root / name
            clone_release(source, case_root)
            mutation(case_root)
            rebuild_lock(case_root, args.timeout_seconds)
            result = invoke_verifier(case_root, args.timeout_seconds)
            results.append(require_rejection(result, name, marker))
            print(f"DIRECT_CLOSURE_MUTATION_REJECTED case={name}")
    after_fingerprints = {
        "direct_closure_lock_sha256": sha_file(source / "DIRECT_CLOSURE_LOCK.json"),
        "production_verifier_sha256": sha_file(source / "verify_direct_closure_release.py"),
        "overlay_verifier_sha256": sha_file(
            source / "proofs/verify_four_port_direct_residual_closure.py"
        ),
        "mutation_runner_sha256": sha_file(Path(__file__).resolve()),
        "direct_overlay_certificate_sha256": sha_file(
            source / "proofs/four_port_direct_residual_closure_certificate.json"
        ),
    }
    if after_fingerprints != source_fingerprints:
        fail("DIRECT_CLOSURE_MUTATION_SOURCE_TREE_DRIFT")
    expected_order = ["optimized_mode"] + [
        name for name, _mutation, _marker in MUTATIONS if name in selected
    ]
    if [row["case"] for row in results] != expected_order:
        fail("DIRECT_CLOSURE_MUTATION_CASE_ORDER_FAIL")
    payload = {
        "schema": SCHEMA,
        "status": "PASS",
        **source_fingerprints,
        "clean_baseline": baseline,
        "execution_contract": {
            "temporary_copies_only": True,
            "production_verifier_reached_by_every_content_mutation": True,
            "required_returncode": 1,
            "exact_named_diagnostics": True,
            "traceback_import_timeout_signal_non_one_forbidden": True,
            "success_terminal_forbidden": True,
            "source_tree_unchanged": True,
        },
        "diagnostic_contract": {
            name: sorted(MUTATION_ALLOWED_CODES[name]) for name in expected_order
        },
        "qualification_negative_controls": negative_controls,
        "case_count": len(results),
        "mutations_rejected": len(results),
        "mutations_survived": 0,
        "cases": results,
    }
    report = dict(payload)
    report["payload_sha256"] = sha_object(payload)
    atomic_write_bytes(
        output_path, (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()
    )
    print("DIRECT_CLOSURE_RELEASE_MUTATIONS_PASS")
    print(
        json.dumps(
            {
                "case_count": len(results),
                "payload_sha256": report["payload_sha256"],
                "status": "PASS",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
