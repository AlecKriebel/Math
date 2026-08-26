#!/usr/bin/env python3
"""Unified quick/full replay for the final principal-D+ K2P theorem package."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

from release_common import (
    HERE,
    PROJECT,
    PROMOTION_GUARD_STDOUT_SHA256,
    ReleaseFailure,
    child_environment,
    load_json,
    require,
    sha_file,
    validate_lock,
    validate_runtime_environment,
)


DEFAULT_LOCK = HERE / "RELEASE_LOCK.json"
AUTHORITATIVE_REPORT = (
    PROJECT / "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json"
)


def validate_report_output_path(
    output: Path | None, allow_authoritative: bool = False
) -> Path | None:
    """Resolve a caller-owned report and forbid aliases into release sources."""

    if output is None:
        require(
            not allow_authoritative,
            "FINAL_REPLAY_OUTPUT_POLICY_FAIL",
            "authoritative override requires --output",
        )
        return None
    lexical = Path(os.path.abspath(os.fspath(output)))
    normalized = lexical.parent.resolve() / lexical.name
    resolved = lexical.resolve()
    canonical = AUTHORITATIVE_REPORT.parent.resolve() / AUTHORITATIVE_REPORT.name
    if allow_authoritative:
        require(
            normalized == canonical and resolved == canonical,
            "FINAL_REPLAY_OUTPUT_POLICY_FAIL",
            "authoritative override requires the exact nonsymbolic canonical report",
        )
        return canonical
    try:
        resolved.relative_to(PROJECT.resolve())
    except ValueError:
        return normalized
    raise ReleaseFailure(
        "FINAL_REPLAY_OUTPUT_POLICY_FAIL:routine report output must be outside "
        "the project source tree"
    )


def prepare_report_output(output: Path | None) -> None:
    """Remove stale caller-owned PASS bytes before every fallible preflight."""

    if output is not None:
        output.unlink(missing_ok=True)


def atomic_write_text(path: Path, text: str) -> None:
    """Fsync and replace without following hard links or late symlink swaps."""

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o644)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text)
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


def qualified_python() -> Path:
    local = PROJECT / ".venv/bin/python"
    return local if local.is_file() else Path(sys.executable)


def locked_source_fingerprint(lock: dict[str, Any]) -> dict[str, str]:
    """Hash every locked input before and after orchestration."""

    files = lock.get("files")
    require(isinstance(files, dict), "SOURCE_FINGERPRINT_LOCK_FILES_FAIL")
    result: dict[str, str] = {}
    for relative in sorted(files):
        path = PROJECT / relative
        require(path.is_file(), "SOURCE_FINGERPRINT_FILE_MISSING", relative)
        result[relative] = sha_file(path)
    return result


def run_child(
    name: str,
    command: list[str],
    *,
    timeout: float,
    terminal_markers: tuple[bytes, ...] = (),
    cwd: Path = PROJECT,
    environment_overrides: dict[str, str] | None = None,
    semantic_command: tuple[str, ...] | None = None,
    source_paths: tuple[Path, ...] = (),
) -> dict[str, Any]:
    started = time.perf_counter()
    environment = child_environment()
    if environment_overrides is not None:
        environment.update(environment_overrides)
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise ReleaseFailure(f"REPLAY_TIMEOUT:{name}:{timeout}") from error
    elapsed = time.perf_counter() - started
    output = result.stdout + result.stderr
    require(result.returncode == 0, "REPLAY_NONZERO", f"{name}:{output[-4000:]!r}")
    for marker in terminal_markers:
        require(marker in output, "REPLAY_MARKER_MISSING", f"{name}:{marker!r}")
    row = {
        "name": name,
        "status": "PASS",
        "elapsed_seconds": round(elapsed, 6),
        "stdout_sha256": hashlib.sha256(result.stdout).hexdigest(),
        "stderr_sha256": hashlib.sha256(result.stderr).hexdigest(),
        "returncode": result.returncode,
    }
    if semantic_command is not None:
        require(bool(source_paths), "REPLAY_BOUND_SOURCE_PATHS_EMPTY", name)
        row["command_sha256"] = hashlib.sha256(
            json.dumps(
                semantic_command, sort_keys=True, separators=(",", ":")
            ).encode()
        ).hexdigest()
        row["source_sha256"] = {
            path.resolve().relative_to(PROJECT.resolve()).as_posix(): sha_file(path)
            for path in source_paths
        }
    print(
        f"K2P_FINAL_LAYER_PASS name={name} elapsed_seconds={elapsed:.3f}",
        flush=True,
    )
    return row


def run_expected_failure(
    name: str,
    command: list[str],
    *,
    timeout: float,
    required_markers: tuple[bytes, ...],
    cwd: Path = PROJECT,
    environment_overrides: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Certify that an isolated dependency-omission mutation is rejected."""

    started = time.perf_counter()
    environment = child_environment()
    if environment_overrides is not None:
        environment.update(environment_overrides)
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise ReleaseFailure(f"EXPECTED_FAILURE_TIMEOUT:{name}:{timeout}") from error
    elapsed = time.perf_counter() - started
    output = result.stdout + result.stderr
    require(result.returncode != 0, "EXPECTED_FAILURE_ACCEPTED", name)
    for marker in required_markers:
        require(marker in output, "EXPECTED_FAILURE_MARKER_MISSING", f"{name}:{marker!r}")
    row = {
        "name": name,
        "status": "PASS",
        "elapsed_seconds": round(elapsed, 6),
        "stdout_sha256": hashlib.sha256(result.stdout).hexdigest(),
        "stderr_sha256": hashlib.sha256(result.stderr).hexdigest(),
        "observed_nonzero_returncode": result.returncode,
    }
    print(
        f"K2P_FINAL_LAYER_PASS name={name} elapsed_seconds={elapsed:.3f}",
        flush=True,
    )
    return row


def compare_bytes(observed: Path, expected: Path, name: str) -> None:
    require(observed.is_file(), "REPLAY_OUTPUT_MISSING", name)
    require(
        observed.read_bytes() == expected.read_bytes(),
        "REPLAY_OUTPUT_BYTE_DRIFT",
        {
            "name": name,
            "observed": sha_file(observed),
            "expected": sha_file(expected),
        },
    )


def compare_logical_json(observed: Path, expected: Path, name: str) -> None:
    """Compare producer mathematics while excluding runtime telemetry."""

    observed_payload = load_json(observed)
    expected_payload = load_json(expected)
    for field in (
        "payload_sha256",
        "operational",
        "runtime_seconds",
        "elapsed_seconds",
    ):
        observed_payload.pop(field, None)
        expected_payload.pop(field, None)
    require(
        observed_payload == expected_payload,
        "REPLAY_LOGICAL_JSON_DRIFT",
        name,
    )


def replay_analytic_adversarial(
    rows: list[dict[str, Any]], timeout: float
) -> None:
    """Replay the analytic audit against the superseding proof draft.

    The frozen audit certificate predates the final proof-text repairs.  All
    mathematical fields must remain identical; only its bound GLOBAL_PROOF
    byte hash and the resulting payload hash may update.
    """

    with tempfile.TemporaryDirectory(prefix="k2p-final-analytic-audit-") as directory:
        observed = Path(directory) / "audit_certificate.json"
        rows.append(
            run_child(
                "analytic_adversarial_audit",
                [
                    str(qualified_python()),
                    "-B",
                    str(PROJECT / "work/adversarial_proof_review/verify_adversarial.py"),
                    "--require-pass",
                    "--output",
                    str(observed),
                ],
                timeout=timeout,
            )
        )
        current = load_json(observed)
        frozen = load_json(PROJECT / "work/adversarial_proof_review/audit_certificate.json")
        current_payload = current.pop("payload_sha256", None)
        frozen.pop("payload_sha256", None)
        current_global = current["upstream_hashes"].pop("global_proof", None)
        frozen["upstream_hashes"].pop("global_proof", None)
        require(current == frozen, "ANALYTIC_ADVERSARIAL_SEMANTIC_DRIFT")
        require(
            current_global
            == sha_file(PROJECT / "work/global_theorem_closure/GLOBAL_PROOF.md"),
            "ANALYTIC_ADVERSARIAL_CURRENT_PROOF_BINDING_FAIL",
        )
        require(
            isinstance(current_payload, str) and len(current_payload) == 64,
            "ANALYTIC_ADVERSARIAL_CURRENT_PAYLOAD_FAIL",
        )


def replay_promotion_guard(rows: list[dict[str, Any]], timeout: float) -> None:
    guard = (
        PROJECT
        / "work/global_theorem_closure/promotion_manuscript/verify_promotion_gate.py"
    )
    row = run_child(
        "promotion_manuscript_guard",
        [str(qualified_python()), "-B", str(guard)],
        timeout=timeout,
        terminal_markers=(b'"status":"PASS"',),
    )
    require(
        row["stdout_sha256"] == PROMOTION_GUARD_STDOUT_SHA256,
        "PROMOTION_GUARD_STDOUT_DRIFT",
    )
    require(
        row["stderr_sha256"]
        == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "PROMOTION_GUARD_STDERR_NOT_EMPTY",
    )
    rows.append(row)


def replay_corrected_probe_independent(
    rows: list[dict[str, Any]], timeout: float
) -> None:
    package = PROJECT / "work/probe_coherence_corrected"
    with tempfile.TemporaryDirectory(prefix="k2p-final-probe-independent-") as directory:
        observed = Path(directory) / "probe_coherence_independent_verification.json"
        rows.append(
            run_child(
                "corrected_probe_independent_streaming_replay",
                [
                    str(qualified_python()),
                    "-B",
                    str(package / "verify_probe_coherence_corrected.py"),
                    "--package-dir",
                    str(package),
                    "--output",
                    str(observed),
                ],
                timeout=timeout,
                terminal_markers=(b'"status": "PASS"',),
            )
        )
        compare_logical_json(
            observed,
            package / "probe_coherence_independent_verification.json",
            "corrected_probe_independent_streaming_replay",
        )


def replay_corrected_restoration_independent(
    rows: list[dict[str, Any]], timeout: float
) -> None:
    package = PROJECT / "work/restoration_sign_reclassification"
    verifier = package / "verify_corrected_restoration_forest.py"
    certificate = package / "corrected_restoration_forest.json"
    crosswalk = package / "corrected_restoration_historical_crosswalk.json"
    expected = package / "corrected_restoration_replay_certificate.json"
    semantic_command = (
        "<qualified-python>",
        "-B",
        "work/restoration_sign_reclassification/verify_corrected_restoration_forest.py",
        "--certificate",
        "work/restoration_sign_reclassification/corrected_restoration_forest.json",
        "--crosswalk",
        "work/restoration_sign_reclassification/corrected_restoration_historical_crosswalk.json",
        "--report",
        "<external-report-path>",
    )
    with tempfile.TemporaryDirectory(
        prefix="k2p-final-restoration-independent-"
    ) as directory:
        observed = Path(directory) / "corrected_restoration_replay_certificate.json"
        rows.append(
            run_child(
                "corrected_restoration_independent_full_replay",
                [
                    str(qualified_python()),
                    "-B",
                    str(verifier),
                    "--certificate",
                    str(certificate),
                    "--crosswalk",
                    str(crosswalk),
                    "--report",
                    str(observed),
                ],
                timeout=max(timeout, 900.0),
                terminal_markers=(b'"status": "PASS"',),
                semantic_command=semantic_command,
                source_paths=(verifier, certificate, crosswalk),
            )
        )
        replay = load_json(observed)
        unsigned = dict(replay)
        claimed_payload = unsigned.pop("payload_sha256", None)
        observed_payload = hashlib.sha256(
            json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        require(
            claimed_payload == observed_payload,
            "RESTORATION_INDEPENDENT_REPLAY_PAYLOAD_FAIL",
        )
        require(
            replay.get("schema")
            == "k2p-corrected-restoration-independent-replay-v3"
            and replay.get("status") == "PASS"
            and replay.get("source_certificate_sha256") == sha_file(certificate)
            and replay.get("source_crosswalk_sha256") == sha_file(crosswalk),
            "RESTORATION_INDEPENDENT_REPLAY_SOURCE_FAIL",
        )
        require(
            replay.get("canonical_parents") == 997
            and replay.get("member_roots") == 2_540
            and replay.get("first_parent_transport_edges_replayed") == 36_568
            and replay.get("second_parent_transport_edges_replayed") == 256
            and replay.get("final_leaves") == 36_792
            and replay.get("unresolved") == 0
            and replay.get("missing_children") == 0
            and replay.get("cycles") == 0,
            "RESTORATION_INDEPENDENT_REPLAY_CENSUS_FAIL",
        )
        compare_logical_json(
            observed,
            expected,
            "corrected_restoration_independent_full_replay",
        )


def replay_corrected_probe_site_partition(
    rows: list[dict[str, Any]], timeout: float
) -> None:
    source = PROJECT / "work/probe_coherence_corrected"
    with tempfile.TemporaryDirectory(prefix="k2p-final-probe-site-partition-") as directory:
        root = Path(directory)
        package = root / "work/probe_coherence_corrected"
        package.mkdir(parents=True)
        shutil.copy2(
            source / "verify_site_transport_partition.py",
            package / "verify_site_transport_partition.py",
        )
        for name in (
            "one_port_ledger.jsonl.gz",
            "two_port_ledger.jsonl.gz",
            "exact_transport_ledger.jsonl.gz",
        ):
            (package / name).symlink_to(source / name)
        adversarial = root / "work/adversarial_proof_review"
        adversarial.parent.mkdir(parents=True, exist_ok=True)
        adversarial.symlink_to(
            PROJECT / "work/adversarial_proof_review", target_is_directory=True
        )
        rows.append(
            run_child(
                "corrected_probe_site_transport_partition",
                [
                    str(qualified_python()),
                    "-B",
                    str(package / "verify_site_transport_partition.py"),
                ],
                cwd=root,
                timeout=timeout,
                terminal_markers=(b'"status": "PASS"',),
            )
        )
        compare_logical_json(
            package / "site_transport_partition_verification.json",
            source / "site_transport_partition_verification.json",
            "corrected_probe_site_transport_partition",
        )


def replay_output_program(
    rows: list[dict[str, Any]],
    *,
    name: str,
    script: Path,
    expected: Path,
    output_flag: str = "--output",
    extra: tuple[str, ...] = (),
    markers: tuple[bytes, ...] = (),
    timeout: float = 300.0,
    logical_compare: bool = False,
) -> None:
    with tempfile.TemporaryDirectory(prefix=f"k2p-final-{name}-") as directory:
        observed = Path(directory) / expected.name
        command = [
            str(qualified_python()),
            "-B",
            str(script),
            *extra,
            output_flag,
            str(observed),
        ]
        rows.append(
            run_child(
                name,
                command,
                timeout=timeout,
                terminal_markers=markers,
            )
        )
        if logical_compare:
            compare_logical_json(observed, expected, name)
        else:
            compare_bytes(observed, expected, name)


def replay_isolated_writer(
    rows: list[dict[str, Any]],
    *,
    name: str,
    script: Path,
    generated_name: str,
    expected: Path,
    marker: bytes,
    timeout: float = 120.0,
) -> None:
    with tempfile.TemporaryDirectory(prefix=f"k2p-final-{name}-") as directory:
        root = Path(directory)
        copied = root / script.name
        shutil.copy2(script, copied)
        rows.append(
            run_child(
                name,
                [str(qualified_python()), "-B", str(copied)],
                cwd=root,
                timeout=timeout,
                terminal_markers=(marker,),
            )
        )
        compare_bytes(root / generated_name, expected, name)


def replay_weak_sharpness(rows: list[dict[str, Any]]) -> None:
    with tempfile.TemporaryDirectory(prefix="k2p-final-weak-primary-") as directory:
        root = Path(directory)
        weak = root / "work/weak_sharpness_closure"
        weak.mkdir(parents=True)
        source = PROJECT / "work/weak_sharpness_closure/verify_weak_sharpness.py"
        shutil.copy2(source, weak / source.name)
        atlas_target = root / "package/referee/k2p_offline_sweep_portable/atlas"
        atlas_target.parent.mkdir(parents=True)
        atlas_target.symlink_to(
            PROJECT / "package/referee/k2p_offline_sweep_portable/atlas",
            target_is_directory=True,
        )
        rows.append(
            run_child(
                "weak_sharpness_primary",
                [str(qualified_python()), "-B", str(weak / source.name)],
                cwd=root,
                timeout=300,
                terminal_markers=(b"K2P_WEAK_SHARPNESS_PASS",),
            )
        )
        compare_bytes(
            weak / "weak_sharpness_certificate.json",
            PROJECT / "work/weak_sharpness_closure/weak_sharpness_certificate.json",
            "weak_sharpness_primary",
        )

    with tempfile.TemporaryDirectory(prefix="k2p-final-weak-independent-") as directory:
        root = Path(directory)
        primary_dir = root / "work/weak_sharpness_closure"
        audit_dir = root / "work/weak_sharpness_audit"
        primary_dir.mkdir(parents=True)
        audit_dir.mkdir(parents=True)
        shutil.copy2(
            PROJECT / "work/weak_sharpness_closure/weak_sharpness_certificate.json",
            primary_dir / "weak_sharpness_certificate.json",
        )
        source = PROJECT / "work/weak_sharpness_audit/audit_weak_sharpness.py"
        shutil.copy2(source, audit_dir / source.name)
        rows.append(
            run_child(
                "weak_sharpness_independent",
                [str(qualified_python()), "-B", str(audit_dir / source.name)],
                cwd=root,
                timeout=300,
                terminal_markers=(b"K2P_WEAK_SHARPNESS_INDEPENDENT_AUDIT_PASS",),
            )
        )
        compare_bytes(
            audit_dir / "audit_certificate.json",
            PROJECT / "work/weak_sharpness_audit/audit_certificate.json",
            "weak_sharpness_independent",
        )


def replay_full_map_truth(rows: list[dict[str, Any]], timeout: float) -> None:
    """Replay revoked-row replacements without writing into source packages."""

    with tempfile.TemporaryDirectory(prefix="k2p-final-full-map-truth-") as directory:
        root = Path(directory)
        audit = root / "work/adversarial_proof_review"
        audit.mkdir(parents=True)
        for name in (
            "audit_raw4_tree_sunlet_full_map.py",
            "audit_theta2_tree_sunlet_full_map.py",
        ):
            shutil.copy2(PROJECT / "work/adversarial_proof_review" / name, audit / name)

        raw_root = root / "work/raw_ledger_audit"
        raw_root.mkdir(parents=True)
        (raw_root / "artifacts").symlink_to(
            PROJECT / "work/raw_ledger_audit/artifacts", target_is_directory=True
        )
        theta_root = root / "work/theta2_five_port_closure"
        theta_root.mkdir(parents=True)
        (theta_root / "artifacts").symlink_to(
            PROJECT / "work/theta2_five_port_closure/artifacts",
            target_is_directory=True,
        )
        atlas = root / "package/referee/k2p_offline_sweep_portable/atlas"
        atlas.parent.mkdir(parents=True)
        atlas.symlink_to(
            PROJECT / "package/referee/k2p_offline_sweep_portable/atlas",
            target_is_directory=True,
        )

        rows.append(
            run_child(
                "raw4_full_map_Ti_truth",
                [
                    str(qualified_python()),
                    "-B",
                    str(audit / "audit_raw4_tree_sunlet_full_map.py"),
                ],
                cwd=root,
                timeout=timeout,
                terminal_markers=(b'"status": "PASS"',),
            )
        )
        compare_bytes(
            audit / "raw4_tree_sunlet_full_map_certificate.json",
            PROJECT
            / "work/adversarial_proof_review/raw4_tree_sunlet_full_map_certificate.json",
            "raw4_full_map_Ti_truth",
        )
        rows.append(
            run_child(
                "theta2_full_map_Ti_truth",
                [
                    str(qualified_python()),
                    "-B",
                    str(audit / "audit_theta2_tree_sunlet_full_map.py"),
                ],
                cwd=root,
                timeout=timeout,
                terminal_markers=(b'"status": "PASS"',),
            )
        )
        compare_bytes(
            audit / "theta2_tree_sunlet_full_map_certificate.json",
            PROJECT
            / "work/adversarial_proof_review/theta2_tree_sunlet_full_map_certificate.json",
            "theta2_full_map_Ti_truth",
        )


def quick_replays(rows: list[dict[str, Any]], timeout: float) -> None:
    python = str(qualified_python())
    replay_promotion_guard(rows, timeout)
    replay_output_program(
        rows,
        name="full_map_domain_reseal",
        script=HERE / "verify_full_map_reseal.py",
        expected=HERE / "full_map_reseal_audit.json",
        markers=(b'"status": "PASS"',),
        timeout=timeout,
    )
    replay_output_program(
        rows,
        name="corrected_universe_independent_replay",
        script=HERE / "verify_corrected_universe_independent.py",
        expected=HERE / "corrected_universe_independent_replay.json",
        markers=(b'"status": "PASS"',),
        timeout=timeout,
    )
    replay_output_program(
        rows,
        name="three_port_no_assert",
        script=HERE / "no_assert_triangle_sunlet.py",
        expected=HERE / "triangle_sunlet_certificate.json",
        markers=(b"K2P_THREE_PORT_NO_ASSERT_REPLAY_PASS",),
    )
    replay_isolated_writer(
        rows,
        name="domain_rooting",
        script=PROJECT / "work/domain_rooting_closure/verify_domain_rooting.py",
        generated_name="domain_rooting_certificate.json",
        expected=PROJECT / "work/domain_rooting_closure/domain_rooting_certificate.json",
        marker=b"K2P_DOMAIN_ROOTING_PASS",
    )
    replay_output_program(
        rows,
        name="quartet_sign_logic",
        script=PROJECT / "work/quartet_separation_closure/verify_quartet_logic.py",
        expected=PROJECT / "work/quartet_separation_closure/quartet_logic_certificate.json",
        extra=(
            "--project",
            str(PROJECT),
            "--spec",
            str(
                PROJECT
                / "work/quartet_separation_closure/QUARTET_SEMANTICS_SPEC.json"
            ),
        ),
        markers=(b"K2P_QUARTET_SIGN_LOGIC_PASS",),
        timeout=timeout,
    )
    replay_output_program(
        rows,
        name="quartet_terminal_bindings",
        script=PROJECT
        / "work/quartet_separation_closure/verify_quartet_terminal_bindings.py",
        expected=PROJECT
        / "work/quartet_separation_closure/quartet_terminal_binding_certificate.json",
        extra=(
            "--project",
            str(PROJECT),
            "--semantics-certificate",
            str(
                PROJECT
                / "work/quartet_separation_closure/quartet_logic_certificate.json"
            ),
        ),
        markers=(b"K2P_QUARTET_TERMINAL_BINDING_PASS",),
        timeout=timeout,
    )
    replay_output_program(
        rows,
        name="raw_displayed_quartet_direction",
        script=PROJECT / "work/adversarial_proof_review/verify_topology_direction.py",
        expected=PROJECT / "work/adversarial_proof_review/topology_direction_certificate.json",
        timeout=timeout,
    )
    rows.append(
        run_child(
            "canonicalizer_completeness_structural",
            [
                python,
                "-B",
                str(
                    PROJECT
                    / "work/canonicalizer_completeness/verify_canonicalizer_completeness.py"
                ),
            ],
            timeout=timeout,
            terminal_markers=(b"K2P_CANONICALIZER_COMPLETENESS_PASS",),
        )
    )
    rows.append(
        run_child(
            "graph_derived_parameter_transports_structural",
            [
                python,
                "-B",
                str(
                    PROJECT
                    / "work/canonicalizer_completeness/inheritance_transport/verify_parameter_transport_certificate.py"
                ),
                "--structural-only",
            ],
            timeout=max(timeout, 600.0),
            terminal_markers=(b"PARAMETER_TRANSPORT_REPLAY_PASS",),
        )
    )
    replay_output_program(
        rows,
        name="bridge_marginal_gluing",
        script=PROJECT / "work/bridge_marginal_closure/verify_bridge_marginal.py",
        expected=PROJECT / "work/bridge_marginal_closure/certificate.json",
    )
    replay_analytic_adversarial(rows, timeout)
    replay_output_program(
        rows,
        name="global_component_scale_audit",
        script=PROJECT / "work/global_proof_adversary/verify_component_scales.py",
        expected=PROJECT
        / "work/global_proof_adversary/component_scale_certificate.json",
        markers=(b"K2P_GLOBAL_COMPONENT_SCALE_AUDIT_PASS",),
        timeout=timeout,
    )
    replay_output_program(
        rows,
        name="raw4_corrected_overlay_independent",
        script=PROJECT
        / "work/raw4_sign_reclassification/verify_raw4_corrected_terminal_ledger.py",
        expected=PROJECT
        / "work/raw4_sign_reclassification/raw4_corrected_replay_certificate.json",
        output_flag="--report",
        extra=(
            "--certificate",
            str(
                PROJECT
                / "work/raw4_sign_reclassification/raw4_corrected_terminal_ledger.json"
            ),
        ),
        timeout=timeout,
        logical_compare=True,
    )
    replay_output_program(
        rows,
        name="theta2_full_map_independent",
        script=PROJECT
        / "work/theta2_sign_reclassification/verify_theta2_full_map_independent.py",
        expected=PROJECT
        / "work/theta2_sign_reclassification/theta2_independent_replay_certificate.json",
        output_flag="--report",
        extra=(
            "--certificate",
            str(
                PROJECT
                / "work/adversarial_proof_review/theta2_tree_sunlet_full_map_certificate.json"
            ),
        ),
        timeout=timeout,
        logical_compare=True,
    )

    rows.append(
        run_child(
            "four_port_raw_structural_provenance",
            [
                python,
                "-B",
                str(PROJECT / "work/raw_ledger_audit/verify_raw_ledger.py"),
                "--quick",
                "--timeout-seconds",
                str(timeout),
            ],
            timeout=timeout + 30,
            terminal_markers=(b"RAW_LEDGER_EXACT_RANK_UPPER_PASS",),
        )
    )
    rows.append(
        run_child(
            "four_port_direct36",
            [
                python,
                "-B",
                str(
                    PROJECT
                    / "package/referee/k2p_offline_sweep_portable/verify_direct_closure_release.py"
                ),
                "--package-root",
                str(PROJECT / "package/referee/k2p_offline_sweep_portable"),
                "--quick",
                "--timeout-seconds",
                str(timeout),
            ],
            timeout=timeout + 30,
            terminal_markers=(b"K2P_FOUR_PORT_DIRECT_CLOSURE_RELEASE_PASS",),
        )
    )
    rows.append(
        run_child(
            "theta2_structural_provenance",
            [
                python,
                "-B",
                str(PROJECT / "work/theta2_five_port_closure/verify_theta2_ledger.py"),
                "--quick",
                "--timeout-seconds",
                str(timeout),
            ],
            timeout=timeout + 30,
            terminal_markers=(b"THETA2_STRUCTURAL_REPLAY_PASS",),
        )
    )
    replay_output_program(
        rows,
        name="cycle_three_port_authoritative_promotion",
        script=PROJECT
        / "work/adversarial_proof_review/verify_corrected_cycle_promotion.py",
        expected=PROJECT
        / "work/adversarial_proof_review/cycle_promotion_independent_verification.json",
        output_flag="--report",
        markers=(b'"status": "PASS"',),
        timeout=timeout,
    )
    replay_corrected_probe_independent(rows, timeout)
    replay_corrected_probe_site_partition(rows, timeout)
    replay_weak_sharpness(rows)


def replay_rank_full(rows: list[dict[str, Any]], timeout: float) -> None:
    with tempfile.TemporaryDirectory(prefix="k2p-final-rank-full-") as directory:
        root = Path(directory)
        destination = root / "work/rank_upper_certificates"
        destination.parent.mkdir(parents=True)
        shutil.copytree(
            PROJECT / "work/rank_upper_certificates",
            destination,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
        )
        atlas = root / "package/referee/k2p_offline_sweep_portable/atlas"
        atlas.parent.mkdir(parents=True)
        atlas.symlink_to(
            PROJECT / "package/referee/k2p_offline_sweep_portable/atlas",
            target_is_directory=True,
        )
        rank_environment = {
            "PYTHONPATH": "",
            "PYTHONNOUSERSITE": "1",
        }
        rows.append(
            run_expected_failure(
                "four_port_exact_rank_staged_atlas_omission_mutation",
                [
                    str(qualified_python()),
                    "-B",
                    str(destination / "verify_rank_upper_certificates.py"),
                    "--help",
                ],
                cwd=root,
                timeout=min(timeout, 60.0),
                required_markers=(b"ModuleNotFoundError", b"k2p_atlas_core"),
                environment_overrides=rank_environment,
            )
        )
        staged_atlas_module = destination / "k2p_atlas_core.py"
        source_atlas_module = atlas / "k2p_atlas_core.py"
        shutil.copy2(source_atlas_module, staged_atlas_module)
        require(
            sha_file(staged_atlas_module) == sha_file(source_atlas_module),
            "RANK_STAGED_ATLAS_MODULE_HASH_DRIFT",
        )
        rows.append(
            run_child(
                "four_port_exact_rank_import_preflight",
                [
                    str(qualified_python()),
                    "-B",
                    str(destination / "verify_rank_upper_certificates.py"),
                    "--help",
                ],
                cwd=root,
                timeout=min(timeout, 60.0),
                terminal_markers=(b"usage:",),
                environment_overrides=rank_environment,
            )
        )
        rows.append(
            run_child(
                "four_port_exact_rank_full",
                [
                    str(qualified_python()),
                    "-B",
                    str(destination / "verify_rank_upper_certificates.py"),
                    "--atlas",
                    str(atlas),
                ],
                cwd=root,
                timeout=timeout,
                terminal_markers=(b'"zero_unresolved": true',),
                environment_overrides=rank_environment,
            )
        )
        compare_bytes(
            destination / "rank_upper_replay.json",
            PROJECT / "work/rank_upper_certificates/rank_upper_replay.json",
            "four_port_exact_rank_full",
        )


def replay_raw4_corrected_overlay_full(
    rows: list[dict[str, Any]], timeout: float
) -> None:
    with tempfile.TemporaryDirectory(prefix="k2p-final-raw4-overlay-full-") as directory:
        root = Path(directory)
        overlay_root = root / "work/raw4_sign_reclassification"
        overlay_root.mkdir(parents=True)
        for name in (
            "build_raw4_corrected_terminal_ledger.py",
            "raw4_sign_reclassification.json",
        ):
            shutil.copy2(
                PROJECT / "work/raw4_sign_reclassification" / name,
                overlay_root / name,
            )
        adversarial = root / "work/adversarial_proof_review"
        adversarial.mkdir(parents=True)
        shutil.copy2(
            PROJECT
            / "work/adversarial_proof_review/raw4_tree_sunlet_full_map_certificate.json",
            adversarial / "raw4_tree_sunlet_full_map_certificate.json",
        )
        raw = root / "work/raw_ledger_audit"
        raw.mkdir(parents=True)
        (raw / "artifacts").symlink_to(
            PROJECT / "work/raw_ledger_audit/artifacts", target_is_directory=True
        )
        atlas = root / "package/referee/k2p_offline_sweep_portable/atlas"
        atlas.parent.mkdir(parents=True)
        atlas.symlink_to(
            PROJECT / "package/referee/k2p_offline_sweep_portable/atlas",
            target_is_directory=True,
        )
        rows.append(
            run_child(
                "raw4_corrected_overlay_full_regeneration",
                [
                    str(qualified_python()),
                    "-B",
                    str(overlay_root / "build_raw4_corrected_terminal_ledger.py"),
                ],
                cwd=root,
                timeout=timeout,
                terminal_markers=(b'"status": "PASS"',),
            )
        )
        compare_bytes(
            overlay_root / "raw4_corrected_terminal_ledger.json",
            PROJECT
            / "work/raw4_sign_reclassification/raw4_corrected_terminal_ledger.json",
            "raw4_corrected_overlay_full_regeneration",
        )


def replay_corrected_probe_full(
    rows: list[dict[str, Any]], timeout: float
) -> None:
    """Regenerate the 574,535-row corrected probe package in isolation."""

    source = PROJECT / "work/probe_coherence_corrected"
    with tempfile.TemporaryDirectory(prefix="k2p-final-probe-full-") as directory:
        root = Path(directory)
        package = root / "work/probe_coherence_corrected"
        package.mkdir(parents=True)
        for name in (
            "build_probe_coherence_corrected.py",
            "verify_probe_coherence_corrected.py",
            "verify_site_transport_partition.py",
        ):
            shutil.copy2(source / name, package / name)
        for relative in (
            "package/referee/k2p_offline_sweep_portable/atlas",
            "work/adversarial_proof_review",
            "work/restoration_sign_reclassification",
            "work/raw_ledger_audit",
            "work/theta2_five_port_closure",
            "work/cycle_three_port_closure",
        ):
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.symlink_to(PROJECT / relative, target_is_directory=True)
        rows.append(
            run_child(
                "corrected_probe_full_primitive_regeneration",
                [
                    str(qualified_python()),
                    "-B",
                    str(package / "build_probe_coherence_corrected.py"),
                    "--stop-after",
                    "two",
                ],
                cwd=root,
                timeout=timeout,
                terminal_markers=(b'"status": "PASS"',),
            )
        )
        for name in (
            "one_port_ledger.jsonl.gz",
            "two_port_parent_inventory.jsonl.gz",
            "two_port_ledger.jsonl.gz",
            "exact_transport_ledger.jsonl.gz",
            "parent_restriction_ledger.jsonl.gz",
            "separation_proof_registry.json.gz",
        ):
            compare_bytes(package / name, source / name, f"corrected_probe_full:{name}")
        compare_logical_json(
            package / "probe_coherence_certificate.json",
            source / "probe_coherence_certificate.json",
            "corrected_probe_full:certificate",
        )
        replay_output = package / "independent_replay.json"
        rows.append(
            run_child(
                "corrected_probe_full_independent_replay",
                [
                    str(qualified_python()),
                    "-B",
                    str(package / "verify_probe_coherence_corrected.py"),
                    "--package-dir",
                    str(package),
                    "--output",
                    str(replay_output),
                ],
                cwd=root,
                timeout=timeout,
                terminal_markers=(b'"status": "PASS"',),
            )
        )
        compare_logical_json(
            replay_output,
            source / "probe_coherence_independent_verification.json",
            "corrected_probe_full:independent_replay",
        )
        rows.append(
            run_child(
                "corrected_probe_full_site_transport_partition",
                [
                    str(qualified_python()),
                    "-B",
                    str(package / "verify_site_transport_partition.py"),
                ],
                cwd=root,
                timeout=timeout,
                terminal_markers=(b'"status": "PASS"',),
            )
        )
        compare_logical_json(
            package / "site_transport_partition_verification.json",
            source / "site_transport_partition_verification.json",
            "corrected_probe_full:site_transport_partition",
        )


def replay_probe_adversarial_full(
    rows: list[dict[str, Any]], timeout: float
) -> None:
    audit = PROJECT / "work/global_proof_adversary/probe_full_audit"
    with tempfile.TemporaryDirectory(prefix="k2p-final-probe-adversarial-") as directory:
        root = Path(directory)
        certificate = root / "independent_probe_graph_audit_certificate.json"
        mutations = root / "independent_probe_mutation_report.json"
        rows.append(
            run_child(
                "corrected_probe_independent_primitive_graph_full",
                [
                    str(qualified_python()),
                    "-B",
                    str(audit / "independent_probe_graph_audit.py"),
                    "--package-dir",
                    str(PROJECT / "work/probe_coherence_corrected"),
                    "--output",
                    str(certificate),
                    "--mutations-output",
                    str(mutations),
                ],
                timeout=timeout,
                terminal_markers=(b'"status": "PASS"',),
            )
        )
        compare_bytes(
            certificate,
            audit / "independent_probe_graph_audit_certificate.json",
            "corrected_probe_independent_primitive_graph_full:certificate",
        )
        compare_bytes(
            mutations,
            audit / "independent_probe_mutation_report.json",
            "corrected_probe_independent_primitive_graph_full:mutations",
        )


def full_replays(rows: list[dict[str, Any]], timeout: float) -> None:
    python = str(qualified_python())
    rows.append(
        run_child(
            "canonicalizer_completeness_full",
            [
                python,
                "-B",
                str(
                    PROJECT
                    / "work/canonicalizer_completeness/verify_canonicalizer_completeness.py"
                ),
                "--full",
            ],
            timeout=max(timeout, 1_800.0),
            terminal_markers=(b"K2P_CANONICALIZER_COMPLETENESS_PASS",),
        )
    )
    rows.append(
        run_child(
            "graph_derived_parameter_transports_full",
            [
                python,
                "-B",
                str(
                    PROJECT
                    / "work/canonicalizer_completeness/inheritance_transport/verify_parameter_transport_certificate.py"
                ),
            ],
            timeout=max(timeout, 7_200.0),
            terminal_markers=(b"PARAMETER_TRANSPORT_REPLAY_PASS",),
        )
    )
    replay_corrected_restoration_independent(rows, timeout)
    replay_output_program(
        rows,
        name="corrected_universe_cross_layer_mutations",
        script=HERE / "run_corrected_universe_mutations.py",
        expected=HERE / "corrected_universe_mutation_report.json",
        extra=("--timeout-seconds", str(max(timeout, 180.0))),
        markers=(b'"status": "PASS"',),
        timeout=max(timeout, 4_000.0),
    )
    replay_full_map_truth(rows, timeout)
    replay_output_program(
        rows,
        name="composite_domain_reseal_diff",
        script=HERE / "verify_composite_reseal_diff.py",
        expected=HERE / "composite_reseal_diff_audit.json",
        markers=(b'"status": "PASS"',),
        timeout=max(timeout, 1_200.0),
    )
    replay_rank_full(rows, timeout)
    replay_raw4_corrected_overlay_full(rows, timeout)
    rows.append(
        run_child(
            "four_port_raw_full_regeneration_provenance",
            [
                python,
                "-B",
                str(PROJECT / "work/raw_ledger_audit/verify_raw_ledger.py"),
                "--timeout-seconds",
                str(timeout),
            ],
            timeout=timeout + 30,
            terminal_markers=(b"RAW_LEDGER_FULL_PRIMITIVE_REPLAY_PASS",),
        )
    )
    rows.append(
        run_child(
            "four_port_direct36_full",
            [
                python,
                "-B",
                str(
                    PROJECT
                    / "package/referee/k2p_offline_sweep_portable/verify_direct_closure_release.py"
                ),
                "--package-root",
                str(PROJECT / "package/referee/k2p_offline_sweep_portable"),
                "--timeout-seconds",
                str(timeout),
            ],
            timeout=timeout + 30,
            terminal_markers=(b"K2P_FOUR_PORT_DIRECT_CLOSURE_RELEASE_PASS",),
        )
    )
    rows.append(
        run_child(
            "theta2_full_regeneration_provenance",
            [
                python,
                "-B",
                str(PROJECT / "work/theta2_five_port_closure/verify_theta2_ledger.py"),
                "--timeout-seconds",
                str(timeout),
            ],
            timeout=timeout + 30,
            terminal_markers=(b"THETA2_FULL_PRIMITIVE_REPLAY_PASS",),
        )
    )
    replay_corrected_probe_full(rows, max(timeout, 7_200.0))
    replay_probe_adversarial_full(rows, max(timeout, 7_200.0))


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--quick", action="store_true")
    mode.add_argument("--full", action="store_true")
    parser.add_argument("--lock", type=Path, default=DEFAULT_LOCK)
    parser.add_argument("--timeout-seconds", type=float, default=1200.0)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--allow-authoritative-output", action="store_true")
    parser.add_argument(
        "--audit-blocked",
        action="store_true",
        help="run diagnostic replays for a blocked candidate, but still exit blocked",
    )
    args = parser.parse_args()
    report_output = validate_report_output_path(
        args.output, args.allow_authoritative_output
    )
    prepare_report_output(report_output)
    if not __debug__:
        raise SystemExit("FINAL_THEOREM_RELEASE_OPTIMIZED_MODE_FORBIDDEN")
    require(args.timeout_seconds > 0, "INVALID_TIMEOUT")
    runtime = validate_runtime_environment()
    lock = load_json(args.lock.resolve())
    started = time.perf_counter()
    lock_result = validate_lock(lock)
    source_before = locked_source_fingerprint(lock)
    blockers = lock_result["blockers"]
    if blockers and not args.audit_blocked:
        raise ReleaseFailure("FINAL_THEOREM_PROMOTION_BLOCKED:" + json.dumps(blockers))
    rows: list[dict[str, Any]] = []
    try:
        quick_replays(rows, args.timeout_seconds)
        if args.full:
            full_replays(rows, args.timeout_seconds)
    finally:
        require(
            locked_source_fingerprint(lock) == source_before,
            "SOURCE_TREE_FINGERPRINT_DRIFT",
        )
    elapsed = time.perf_counter() - started
    report = {
        "schema": "k2p-principal-d-plus-final-theorem-replay-report-v1",
        "mode": "full" if args.full else "quick",
        "status": "PASS" if not blockers else "BLOCKED",
        "promotion_ready": not blockers,
        "blockers": blockers,
        "lock_payload_sha256": lock_result["lock_payload_sha256"],
        "layer_replays": rows,
        "elapsed_seconds": round(elapsed, 6),
        "optimized_mode": False,
        "runtime": runtime,
    }
    if report_output is not None:
        atomic_write_text(
            report_output, json.dumps(report, indent=2, sort_keys=True) + "\n"
        )
    if blockers:
        print("K2P_FINAL_THEOREM_RELEASE_BLOCKED")
        print(json.dumps(report, sort_keys=True))
        return 2
    print("K2P_FINAL_THEOREM_RELEASE_PASS")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ReleaseFailure as error:
        raise SystemExit(f"FINAL_THEOREM_RELEASE_FAIL:{error}") from error
