#!/usr/bin/env python3
"""Deterministic quick, full-replay, and producer-regeneration orchestration."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import platform
import resource
import signal
import subprocess
import sys
import time

from release_common import (
    ReleaseFailure,
    atomic_write,
    canonical_json_bytes,
    head_commit,
    head_commit_epoch,
    load_json,
    read_head_blob,
    refuse_optimized_python,
    require,
    resolve_inside,
    safe_relative_path,
    scoped_status,
    sha256_bytes,
    sha256_file,
    tracked_worktree_fingerprint,
)


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
WORK = PROJECT / "release/work"


class Command:
    def __init__(self, name: str, argv: list[str], sentinel: str | None = None,
                 timeout_seconds: int = 14_400):
        self.name = name
        self.argv = argv
        self.sentinel = sentinel
        self.timeout_seconds = timeout_seconds


def normalized_command_plan(commands: list[Command]) -> list[dict]:
    result = []
    for command in commands:
        require(isinstance(command.argv, list) and command.argv,
                ("empty release command", command.name))
        argv = list(command.argv)
        argv[0] = "{python}"
        result.append({
            "name": command.name,
            "argv": argv,
            "sentinel": command.sentinel,
            "timeout_seconds": command.timeout_seconds,
        })
    return result


def suite_code_bindings(project: Path) -> dict[str, str]:
    return {
        "suite_sha256": sha256_bytes(read_head_blob(
            project, "reproducibility/run_release_suite.py"
        )),
        "release_common_sha256": sha256_bytes(read_head_blob(
            project, "reproducibility/release_common.py"
        )),
    }


def quick_commands(python: str, allow_uncommitted: bool) -> list[Command]:
    inputs = [python, "reproducibility/verify_release_inputs.py"]
    if allow_uncommitted:
        inputs.append("--allow-uncommitted-sources")
    return [
        Command("release_inputs", inputs, "K3P_RELEASE_INPUT_GATE_PASS", 600),
        Command(
            "integrated_artifact_binding",
            [python, "reproducibility/verify_k3p_same_classification.py",
             "--artifact-only", "--no-write-report"],
            "K3P_SAME_CLASSIFICATION_GATE_PASS", 1_800,
        ),
    ]


def full_commands(python: str, allow_uncommitted: bool) -> list[Command]:
    return [
        *quick_commands(python, allow_uncommitted)[:1],
        Command(
            "integrated_fresh_independent_replay",
            [python, "reproducibility/verify_k3p_same_classification.py",
             "--no-write-report"],
            "K3P_SAME_CLASSIFICATION_GATE_PASS", 14_400,
        ),
        Command(
            "integrated_classification_mutations",
            [python, "reproducibility/test_k3p_same_classification_mutations.py"],
            "K3P_SAME_CLASSIFICATION_MUTATIONS_PASS", 3_600,
        ),
        Command(
            "release_engineering_mutations",
            [python, "reproducibility/test_release_engineering_mutations.py",
             "--no-write-report"],
            "K3P_RELEASE_ENGINEERING_MUTATIONS_PASS", 600,
        ),
    ]


def regeneration_commands(python: str, allow_uncommitted: bool) -> list[Command]:
    # The probe producer is intentionally present only here.  It is an
    # hour-scale deterministic rebuild on the target M1 machine.
    commands = [
        Command("cut_single_minor_search", [python,
            "cut_recovery/strong_crossbridge/search_cut_minor_signs.py", "--fresh"],
            timeout_seconds=43_200),
        Command("cut_signed_pair_build", [python,
            "cut_recovery/strong_crossbridge/signed_pair_certificates/build_signed_pair_certificates.py"],
            timeout_seconds=14_400),
        Command("cut_signed_pair_verify", [python,
            "cut_recovery/strong_crossbridge/signed_pair_certificates/verify_signed_pair_certificates.py"],
            timeout_seconds=14_400),
        Command("cut_signed_pair_mutations", [python,
            "cut_recovery/strong_crossbridge/signed_pair_certificates/run_adversarial_mutations.py"],
            timeout_seconds=14_400),
        Command("cut_record39_audit", [python,
            "cut_recovery/strong_crossbridge/audit_simplex/verify_record39_cyclic_certificate.py"],
            timeout_seconds=14_400),
        Command("cut_cyclic_build", [python,
            "cut_recovery/strong_crossbridge/cyclic_certificates/generate_cyclic_certificates.py"],
            timeout_seconds=14_400),
        Command("cut_cyclic_verify", [python,
            "cut_recovery/strong_crossbridge/cyclic_certificates/verify_cyclic_certificates.py",
            "--mutations"],
            timeout_seconds=14_400),
        Command("cut_cyclic_verify_optimized", [python, "-O",
            "cut_recovery/strong_crossbridge/cyclic_certificates/verify_cyclic_certificates.py",
            "--mutations", "--report",
            "cut_recovery/strong_crossbridge/cyclic_certificates/OPTIMIZED_VERIFICATION_REPORT.json"],
            timeout_seconds=14_400),
        Command("cut_cyclic_manifest", [python,
            "cut_recovery/strong_crossbridge/cyclic_certificates/build_manifest.py"],
            timeout_seconds=3_600),
        Command("cut_record43_audit", [python,
            "cut_recovery/strong_crossbridge/audit_simplex/verify_record43_cyclic_transport.py"],
            timeout_seconds=14_400),
        Command("cut_record60_audit", [python,
            "cut_recovery/strong_crossbridge/audit_simplex/verify_record60_cyclic_certificate.py"],
            timeout_seconds=14_400),
        Command("cut_final_build", [python,
            "cut_recovery/strong_crossbridge/final_certificate/build_final_certificate.py"],
            timeout_seconds=14_400),
        Command("cut_final_verify", [python,
            "cut_recovery/strong_crossbridge/final_certificate/verify_final_certificate.py"],
            timeout_seconds=14_400),
        Command("cut_final_mutations", [python,
            "cut_recovery/strong_crossbridge/final_certificate/run_adversarial_mutations.py"],
            timeout_seconds=14_400),
        Command("cut_global_transfer_build", [python,
            "cut_recovery/strong_crossbridge/global_transfer/build_global_transfer.py"],
            timeout_seconds=14_400),
        Command("cut_global_transfer_verify", [python,
            "cut_recovery/strong_crossbridge/global_transfer/verify_global_transfer.py",
            "--mutations"],
            timeout_seconds=14_400),
        Command("cut_global_transfer_verify_optimized", [python, "-O",
            "cut_recovery/strong_crossbridge/global_transfer/verify_global_transfer.py",
            "--mutations", "--report",
            "cut_recovery/strong_crossbridge/global_transfer/OPTIMIZED_VERIFICATION_REPORT.json"],
            timeout_seconds=14_400),
        Command("cut_global_transfer_adversarial", [python,
            "cut_recovery/strong_crossbridge/global_transfer/adversarial/verify_global_transfer_adversarial.py"],
            timeout_seconds=14_400),
        Command("cut_global_transfer_adversarial_mutations", [python,
            "cut_recovery/strong_crossbridge/global_transfer/adversarial/test_global_transfer_adversarial_mutations.py"],
            timeout_seconds=14_400),
        Command("cut_global_transfer_adversarial_manifest_check", [python,
            "cut_recovery/strong_crossbridge/global_transfer/adversarial/verify_global_transfer_adversarial.py",
            "--check-manifest", "--no-write-report"],
            timeout_seconds=14_400),
        Command("cut_global_transfer_release", [python,
            "cut_recovery/strong_crossbridge/global_transfer/verify_release.py"],
            timeout_seconds=14_400),
        Command("cut_global_transfer_release_optimized", [python, "-O",
            "cut_recovery/strong_crossbridge/global_transfer/verify_release.py", "--report",
            "cut_recovery/strong_crossbridge/global_transfer/RELEASE_OPTIMIZED_VERIFICATION_REPORT.json"],
            timeout_seconds=14_400),
        Command("cut_global_transfer_manifest", [python,
            "cut_recovery/strong_crossbridge/global_transfer/build_manifest.py"],
            timeout_seconds=3_600),
        Command("restoration_full_producer", [python,
            "restoration/regenerate_k3p_restoration.py", "--fresh"], timeout_seconds=43_200),
        Command("restoration_independent_replay", [python,
            "restoration/verify_k3p_restoration.py"], timeout_seconds=14_400),
        Command("restoration_mutations", [python,
            "restoration/test_k3p_restoration_mutations.py"], timeout_seconds=14_400),
        Command("probe_hour_scale_producer", [python,
            "probes/regenerate_k3p_probes.py"], timeout_seconds=86_400),
        Command("probe_independent_replay", [python,
            "probes/verify_k3p_probes.py", "--output",
            "release/work/regeneration_ephemeral/K3P_PROBE_INDEPENDENT_VERIFICATION.json"],
            timeout_seconds=14_400),
        Command("probe_mutations", [python,
            "probes/test_k3p_probe_mutations.py", "--no-write-report"],
            timeout_seconds=14_400),
        Command("probe_manifest_seal", [python,
            "probes/seal_probe_manifests.py"], timeout_seconds=3_600),
        Command("sharpness_krawczyk_producer", [python,
            "sharpness/independent_krawczyk_replay.py"], timeout_seconds=14_400),
        Command("sharpness_topology_alln_producer", [python,
            "sharpness/independent_topology_alln_replay.py"], timeout_seconds=14_400),
        Command("sharpness_build", [python,
            "sharpness/build_sharpness_report.py"], timeout_seconds=14_400),
        Command("sharpness_adversarial", [python,
            "sharpness/adversarial/adversarial_audit.py"], timeout_seconds=14_400),
        Command("global_infrastructure_build", [python,
            "global_infrastructure/generate_global_infrastructure.py"], timeout_seconds=14_400),
        Command("global_infrastructure_verify", [python,
            "global_infrastructure/verify_global_infrastructure.py"], timeout_seconds=14_400),
        Command("global_infrastructure_mutations", [python,
            "global_infrastructure/test_global_infrastructure_mutations.py"], timeout_seconds=14_400),
        Command("primary_rebind", [python,
            "reproducibility/verify_primary.py"], "PRIMARY_GATE_STATUS PASS", 14_400),
        *full_commands(python, allow_uncommitted),
    ]
    return commands


def deterministic_environment(project: Path) -> dict[str, str]:
    environment = dict(os.environ)
    environment.update({
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0",
        "LC_ALL": "C",
        "LANG": "C",
        "TZ": "UTC",
        "SOURCE_DATE_EPOCH": str(head_commit_epoch(project)),
    })
    temporary = WORK / "tmp"
    temporary.mkdir(parents=True, exist_ok=True)
    environment["TMPDIR"] = str(temporary)
    return environment


def memory_record() -> dict:
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    raw = int(usage.ru_maxrss)
    unit = "bytes" if platform.system() == "Darwin" else "KiB"
    byte_estimate = raw if unit == "bytes" else raw * 1024
    return {"ru_maxrss_raw": raw, "ru_maxrss_unit": unit, "peak_bytes": byte_estimate}


def run_one(command: Command, environment: dict[str, str], transcript) -> dict:
    transcript.write(f"\nCOMMAND {command.name}\n")
    transcript.write("ARGV " + json.dumps(command.argv) + "\n")
    transcript.flush()
    started = time.monotonic()
    transcript.flush()
    output_start = transcript.tell()
    process = subprocess.Popen(
        command.argv, cwd=PROJECT, env=environment, text=True,
        stdout=transcript, stderr=subprocess.STDOUT, start_new_session=True,
    )
    try:
        returncode = process.wait(timeout=command.timeout_seconds)
    except subprocess.TimeoutExpired as error:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()
        raise ReleaseFailure(("command timeout", command.name, command.timeout_seconds)) from error
    elapsed = time.monotonic() - started
    transcript.flush()
    output_end = transcript.tell()
    transcript.seek(output_start)
    output = transcript.read(output_end - output_start)
    transcript.seek(output_end)
    require(returncode == 0,
            ("command failed", command.name, returncode, output[-4000:]))
    if command.sentinel is not None:
        require(command.sentinel in output,
                ("command sentinel missing", command.name, command.sentinel))
    record = {
        "name": command.name,
        "argv": command.argv,
        "exit_code": returncode,
        "sentinel": command.sentinel,
        "sentinel_seen": command.sentinel is None or command.sentinel in output,
        "timeout_seconds": command.timeout_seconds,
        "elapsed_seconds": elapsed,
        "transcript_sha256": sha256_bytes(output.encode("utf-8")),
        "status": "PASS",
    }
    transcript.write("RESULT " + json.dumps(record, sort_keys=True) + "\n")
    transcript.flush()
    print(json.dumps({"command": command.name, "status": "PASS",
                      "elapsed_seconds": elapsed}, sort_keys=True), flush=True)
    return record


def verify_suite_report(project: Path, report_path: Path,
                        transcript_assets: set[str]) -> dict:
    report = load_json(report_path)
    expected_fields = {
        "schema", "status", "mode", "source_commit", "command_count",
        "command_plan", "command_plan_sha256", "commands", "elapsed_seconds",
        "peak_memory", "tracked_fingerprint_before", "tracked_fingerprint_after",
        "tracked_worktree_unchanged", "clean_checkout_required", "initial_status",
        "final_status", "transcript", "suite_sha256", "release_common_sha256",
        "python_version", "payload_sha256",
    }
    require(set(report) == expected_fields, "release suite report field set")
    claimed = report.get("payload_sha256")
    body = dict(report)
    body.pop("payload_sha256", None)
    require(claimed == sha256_bytes(canonical_json_bytes(body)),
            "release suite report payload hash")
    mode = report.get("mode")
    require(report.get("schema") == "k3p-release-suite-report-v1" and
            report.get("status") == "PASS" and mode in {"quick", "full", "regenerate"},
            "release suite report schema/status/mode")
    require(report.get("source_commit") == head_commit(project),
            "release suite report source commit")
    require(report.get("clean_checkout_required") is True and
            report.get("initial_status") == report.get("final_status") == [] and
            report.get("tracked_worktree_unchanged") is True,
            "release suite clean-worktree claim")
    require(isinstance(report.get("elapsed_seconds"), (int, float)) and
            report["elapsed_seconds"] >= 0 and
            isinstance(report.get("python_version"), str) and report["python_version"],
            "release suite runtime metadata")
    memory = report.get("peak_memory")
    require(isinstance(memory, dict) and set(memory) == {
        "ru_maxrss_raw", "ru_maxrss_unit", "peak_bytes"
    } and isinstance(memory["ru_maxrss_raw"], int) and memory["ru_maxrss_raw"] >= 0 and
            memory["ru_maxrss_unit"] in {"bytes", "KiB"} and
            memory["peak_bytes"] == memory["ru_maxrss_raw"] * (
                1 if memory["ru_maxrss_unit"] == "bytes" else 1024
            ), "release suite peak-memory metadata")
    fingerprint = tracked_worktree_fingerprint(project)
    require(report.get("tracked_fingerprint_before") ==
            report.get("tracked_fingerprint_after") == fingerprint,
            "release suite tracked-worktree fingerprint")
    bindings = suite_code_bindings(project)
    require(all(report.get(key) == value for key, value in bindings.items()),
            "release suite code binding")
    expected_commands = {
        "quick": quick_commands,
        "full": full_commands,
        "regenerate": regeneration_commands,
    }[mode]("{python}", False)
    expected_plan = normalized_command_plan(expected_commands)
    require(report.get("command_plan") == expected_plan and
            report.get("command_plan_sha256") ==
            sha256_bytes(canonical_json_bytes(expected_plan)),
            "release suite exact command plan")
    records = report.get("commands")
    require(isinstance(records, list) and len(records) == len(expected_plan) and
            report.get("command_count") == len(expected_plan),
            "release suite command count")
    for record, plan in zip(records, expected_plan, strict=True):
        require(isinstance(record, dict) and set(record) == {
            "name", "argv", "exit_code", "sentinel", "sentinel_seen",
            "timeout_seconds", "elapsed_seconds", "transcript_sha256", "status",
        }, "release suite command record schema")
        normalized_argv = list(record.get("argv", []))
        require(bool(normalized_argv), "release suite command argv")
        normalized_argv[0] = "{python}"
        require(record.get("name") == plan["name"] and normalized_argv == plan["argv"] and
                record.get("sentinel") == plan["sentinel"] and
                record.get("timeout_seconds") == plan["timeout_seconds"] and
                record.get("exit_code") == 0 and record.get("sentinel_seen") is True and
                record.get("status") == "PASS" and
                isinstance(record.get("elapsed_seconds"), (int, float)) and
                record["elapsed_seconds"] >= 0 and
                isinstance(record.get("transcript_sha256"), str) and
                len(record["transcript_sha256"]) == 64 and
                all(character in "0123456789abcdef"
                    for character in record["transcript_sha256"]),
                ("release suite command record", plan["name"]))
    transcript = report.get("transcript")
    require(isinstance(transcript, dict) and set(transcript) == {"path", "sha256", "bytes"},
            "release suite transcript record")
    relative = transcript.get("path")
    safe_relative_path(relative)
    require(relative in transcript_assets, ("unbound release suite transcript", relative))
    transcript_path = resolve_inside(project, relative)
    require(transcript_path.is_file() and transcript_path.stat().st_size == transcript.get("bytes")
            and sha256_file(transcript_path) == transcript.get("sha256"),
            "release suite transcript bytes")
    lines = transcript_path.read_text(encoding="utf-8").splitlines()
    require(bool(lines), "empty release suite transcript")
    header = json.loads(lines[0])
    require(header == {
        "schema": "k3p-release-suite-transcript-v1",
        "mode": mode,
        "source_commit": head_commit(project),
        "command_count": len(expected_plan),
        "command_plan_sha256": report["command_plan_sha256"],
        "suite_sha256": bindings["suite_sha256"],
        "release_common_sha256": bindings["release_common_sha256"],
        "environment": {
            "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0",
            "LC_ALL": "C", "LANG": "C", "TZ": "UTC",
            "SOURCE_DATE_EPOCH": str(head_commit_epoch(project)),
        },
    }, "release suite transcript header")
    transcript_results = [
        json.loads(line.removeprefix("RESULT "))
        for line in lines if line.startswith("RESULT ")
    ]
    require(transcript_results == records, "release suite transcript/result binding")
    return {"mode": mode, "payload_sha256": claimed,
            "transcript_sha256": transcript["sha256"], "command_count": len(records)}


def main(argv: list[str] | None = None) -> int:
    try:
        refuse_optimized_python()
        parser = argparse.ArgumentParser()
        parser.add_argument("mode", choices=("quick", "full", "regenerate"))
        parser.add_argument("--allow-dirty", action="store_true",
                            help="development only; never valid for Gate J")
        parser.add_argument("--transcript-dir", type=Path,
                            help="project-local final transcript directory")
        args = parser.parse_args(argv)
        if args.mode == "regenerate":
            require(os.environ.get("K3P_CONFIRM_FULL_REGENERATION") == "YES",
                    "FULL_REGENERATION_REQUIRES_K3P_CONFIRM_FULL_REGENERATION=YES")
        initial_status = scoped_status(PROJECT)
        if not args.allow_dirty:
            require(initial_status == [], ("project is not clean at suite start", initial_status))
        initial_fingerprint = tracked_worktree_fingerprint(PROJECT)
        commit = head_commit(PROJECT)
        python = sys.executable
        commands = {
            "quick": quick_commands,
            "full": full_commands,
            "regenerate": regeneration_commands,
        }[args.mode](python, args.allow_dirty)
        command_plan = normalized_command_plan(commands)
        command_plan_sha256 = sha256_bytes(canonical_json_bytes(command_plan))
        bindings = suite_code_bindings(PROJECT)
        environment = deterministic_environment(PROJECT)
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        transcript_root = (args.transcript_dir.resolve() if args.transcript_dir else
                           (WORK / "transcripts").resolve())
        try:
            transcript_root.relative_to(PROJECT.resolve())
        except ValueError as error:
            raise ReleaseFailure(("transcript directory outside project", transcript_root)) from error
        transcript_path = transcript_root / f"{args.mode}_{commit[:12]}_{stamp}.log"
        report_path = transcript_root / f"{args.mode}_{commit[:12]}_{stamp}.json"
        transcript_path.parent.mkdir(parents=True, exist_ok=True)
        started = time.monotonic()
        records = []
        with transcript_path.open("w+", encoding="utf-8", newline="\n") as transcript:
            transcript.write(json.dumps({
                "schema": "k3p-release-suite-transcript-v1",
                "mode": args.mode,
                "source_commit": commit,
                "command_count": len(commands),
                "command_plan_sha256": command_plan_sha256,
                **bindings,
                "environment": {key: environment[key] for key in (
                    "PYTHONDONTWRITEBYTECODE", "PYTHONHASHSEED", "LC_ALL", "LANG", "TZ",
                    "SOURCE_DATE_EPOCH",
                )},
            }, sort_keys=True) + "\n")
            for command in commands:
                records.append(run_one(command, environment, transcript))
        elapsed = time.monotonic() - started
        final_fingerprint = tracked_worktree_fingerprint(PROJECT)
        require(final_fingerprint == initial_fingerprint,
                ("suite changed tracked project files", initial_fingerprint, final_fingerprint))
        final_status = scoped_status(PROJECT)
        if not args.allow_dirty:
            require(final_status == [], ("project is not clean at suite end", final_status))
        transcript_record = {
            "path": str(transcript_path.relative_to(PROJECT)),
            "sha256": sha256_file(transcript_path),
            "bytes": transcript_path.stat().st_size,
        }
        report = {
            "schema": "k3p-release-suite-report-v1",
            "status": "PASS",
            "mode": args.mode,
            "source_commit": commit,
            "command_count": len(records),
            "command_plan": command_plan,
            "command_plan_sha256": command_plan_sha256,
            "commands": records,
            "elapsed_seconds": elapsed,
            "peak_memory": memory_record(),
            "tracked_fingerprint_before": initial_fingerprint,
            "tracked_fingerprint_after": final_fingerprint,
            "tracked_worktree_unchanged": True,
            "clean_checkout_required": not args.allow_dirty,
            "initial_status": initial_status,
            "final_status": final_status,
            "transcript": transcript_record,
            **bindings,
            "python_version": platform.python_version(),
        }
        report["payload_sha256"] = sha256_bytes(canonical_json_bytes(report))
        atomic_write(report_path, (json.dumps(report, indent=2, sort_keys=True) + "\n").encode())
        print(json.dumps({
            "status": "PASS", "mode": args.mode, "elapsed_seconds": elapsed,
            "peak_memory": report["peak_memory"],
            "transcript": report["transcript"]["path"],
            "report": str(report_path.relative_to(PROJECT)),
            "payload_sha256": report["payload_sha256"],
        }, sort_keys=True))
        print(f"K3P_RELEASE_SUITE_{args.mode.upper()}_PASS")
        return 0
    except (ReleaseFailure, OSError, UnicodeError, subprocess.SubprocessError) as error:
        print(f"K3P_RELEASE_SUITE_FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
