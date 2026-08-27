#!/usr/bin/env python3
"""Validate and seal the completed one-shot portable-regeneration evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
from pathlib import PurePosixPath
import re


class SealFailure(RuntimeError):
    pass


EXPECTED_REPLAYS = (
    "primary_28_of_28",
    "clean_room_h21_fourteen_orbits",
    "sharpness_adversarial",
    "cut_transfer_ordinary_optimized_adversarial",
    "cut_transfer_claim_boundary_mutations",
    "cut_topology_graph_regeneration",
    "global_infrastructure",
    "global_infrastructure_mutations",
    "full_four_port_independent_replay",
    "full_four_port_coherent_mutations",
    "full_probe_independent_replay",
    "full_probe_semantic_replay",
    "restoration_independent_replay",
    "restoration_20_mutations",
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise SealFailure(message)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), ("JSON root is not an object", str(path)))
    return value


def regular_file(path: Path) -> bool:
    return path.is_file() and not path.is_symlink()


def real_directory(path: Path) -> bool:
    return path.is_dir() and not path.is_symlink()


def require_no_symlink_components(path: Path) -> None:
    absolute = Path(os.path.abspath(path))
    cursor = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        cursor /= part
        require(not cursor.is_symlink(), ("symlinked path component", str(cursor)))


def finite_nonnegative(value: object) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
        and float(value) >= 0.0
    )


def safe_relative(value: object) -> str:
    require(
        isinstance(value, str)
        and value
        and "\\" not in value
        and "\x00" not in value,
        ("unsafe relative path characters", value),
    )
    path = PurePosixPath(value)
    require(
        not path.is_absolute()
        and ".." not in path.parts
        and value not in {".", ""}
        and path.as_posix() == value,
        ("unsafe or noncanonical relative path", value),
    )
    return value


def integrated_logical_payload(report: dict) -> dict:
    logical = dict(report)
    logical.pop("operational", None)
    logical.pop("payload_sha256", None)
    logical["fresh_replays"] = [
        {
            key: row[key]
            for key in (
                "name",
                "exit_code",
                "sentinel",
                "sentinel_seen",
                "status",
                "fresh_output_payload_sha256",
                "fresh_mutation_payload_sha256",
            )
            if key in row
        }
        for row in report.get("fresh_replays", [])
    ]
    return logical


def parse_transcript(
    transcript: str, expected_names: list[str], report_rows: list[dict]
) -> dict:
    header_end = transcript.find("\n")
    require(header_end > 0, "transcript header line")
    header = json.loads(transcript[:header_end])
    require(isinstance(header, dict), "transcript header object")
    cursor = header_end + 1
    for index, (expected_name, report_row) in enumerate(
        zip(expected_names, report_rows, strict=True)
    ):
        prefix = f"\nCOMMAND {expected_name}\nARGV "
        require(transcript.startswith(prefix, cursor), ("command marker", index, expected_name))
        argv_start = cursor + len(prefix)
        argv_end = transcript.find("\n", argv_start)
        require(argv_end >= argv_start, ("ARGV line", expected_name))
        argv = json.loads(transcript[argv_start:argv_end])
        require(argv == report_row.get("argv"), ("ARGV/report mismatch", expected_name))
        output_start = argv_end + 1
        result_match = re.search(r"(?m)^RESULT (\{[^\n]*\})\n", transcript[output_start:])
        require(result_match is not None, ("RESULT line", expected_name))
        result_start = output_start + result_match.start()
        result_end = output_start + result_match.end()
        output = transcript[output_start:result_start]
        result = json.loads(result_match.group(1))
        require(result == report_row, ("RESULT/report mismatch", expected_name))
        require(result.get("name") == expected_name, ("RESULT name", expected_name))
        require(
            result.get("stdout_sha256") == sha256_bytes(output.encode("utf-8")),
            ("stdout hash", expected_name),
        )
        cursor = result_end
    require(cursor == len(transcript), "unexpected trailing transcript data")
    return header


def atomic_publish_file(path: Path, data: bytes) -> None:
    require(not os.path.lexists(path), ("seal already exists", str(path)))
    temporary = path.with_name(f".{path.name}.tmp.{os.getpid()}")
    require(not os.path.lexists(temporary), ("temporary seal exists", str(temporary)))
    created = False
    linked = False
    success = False
    descriptor = None
    identity = None
    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        descriptor = os.open(temporary, flags, 0o600)
        created = True
        identity = os.fstat(descriptor).st_dev, os.fstat(descriptor).st_ino
        with os.fdopen(descriptor, "wb", closefd=False) as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        observed = temporary.lstat()
        require(
            not temporary.is_symlink()
            and (observed.st_dev, observed.st_ino) == identity,
            "temporary seal identity changed",
        )
        os.link(temporary, path, follow_symlinks=False)
        linked = True
        published = path.lstat()
        require(
            not path.is_symlink()
            and (published.st_dev, published.st_ino) == identity,
            "published seal identity changed",
        )
        success = True
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if linked and not success and os.path.lexists(path):
            observed = path.lstat()
            if not path.is_symlink() and (observed.st_dev, observed.st_ino) == identity:
                path.unlink()
        if created and os.path.lexists(temporary):
            observed = temporary.lstat()
            if not temporary.is_symlink() and (observed.st_dev, observed.st_ino) == identity:
                temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, required=True)
    parser.add_argument("--session-root", type=Path, required=True)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--outer-console", type=Path, required=True)
    parser.add_argument("--diff-tool", type=Path, required=True)
    parser.add_argument("--runner", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    args = parser.parse_args()

    audit_root = Path(__file__).resolve().parents[1]
    package_root = Path(os.path.abspath(args.package_root))
    session_root = Path(os.path.abspath(args.session_root))
    phase_root = session_root / "regenerate"
    expected_profile = audit_root / "logs/offline_credential_free.sb"
    expected_diff_tool = audit_root / "tools/full_workspace_diff.py"
    expected_runner = package_root / "referee_tools/run_active_verifiers.py"
    expected_plan = package_root / "referee_tools/ACTIVE_VERIFIER_PLAN.json"
    expected_console = package_root / "review_runs/regenerate_console.log"

    require(real_directory(package_root), "package root must be a real directory")
    require(
        real_directory(package_root / "review_runs")
        and session_root.parent == package_root / "review_runs"
        and real_directory(session_root)
        and real_directory(phase_root),
        "session path must be one real review_runs child",
    )
    require(Path(os.path.abspath(args.profile)) == expected_profile, "unexpected sandbox profile")
    require(Path(os.path.abspath(args.diff_tool)) == expected_diff_tool, "unexpected diff tool")
    require(Path(os.path.abspath(args.runner)) == expected_runner, "unexpected runner")
    require(Path(os.path.abspath(args.plan)) == expected_plan, "unexpected plan")
    require(Path(os.path.abspath(args.outer_console)) == expected_console, "unexpected outer console")

    report_path = phase_root / "report.json"
    summary_path = session_root / "summary.json"
    transcript_path = phase_root / "transcript.log"
    diff_path = phase_root / "full_workspace_diff.json"
    integrated_path = phase_root / "integrated_fresh_report.json"
    location_paths = (
        phase_root / "primary_rebind_location_dependent_primary_report.json",
        phase_root / "integrated_fresh_independent_replay_location_dependent_primary_report.json",
    )
    seal_path = phase_root / "REGENERATION_SEAL.json"

    evidence_inputs = (
        report_path,
        summary_path,
        transcript_path,
        diff_path,
        integrated_path,
        *location_paths,
        expected_profile,
        expected_console,
        expected_diff_tool,
        expected_runner,
        expected_plan,
        Path(__file__).resolve(),
    )
    for path in (
        package_root,
        session_root,
        phase_root,
        *evidence_inputs,
        seal_path,
    ):
        require_no_symlink_components(path)
    for path in evidence_inputs:
        require(regular_file(path), ("missing or symlinked evidence file", str(path)))
    require(
        not os.path.lexists(seal_path),
        "seal file must not pre-exist",
    )
    require(
        set(phase_root.glob("*_location_dependent_primary_report.json"))
        == set(location_paths),
        "unexpected location-dependent primary report",
    )

    package_manifest_path = package_root / "PACKAGE_MANIFEST.json"
    require(regular_file(package_manifest_path), "package manifest")
    package_manifest = load_json(package_manifest_path)
    require(
        package_manifest.get("schema") == "k3p-independent-referee-package-v1",
        "package manifest schema",
    )
    payload_rows = package_manifest.get("payload")
    require(isinstance(payload_rows, list), "package payload list")
    payload_index = {
        row.get("path"): row for row in payload_rows if isinstance(row, dict)
    }
    require(len(payload_index) == len(payload_rows), "package payload path uniqueness")
    for relative, path in (
        ("referee_tools/run_active_verifiers.py", expected_runner),
        ("referee_tools/ACTIVE_VERIFIER_PLAN.json", expected_plan),
    ):
        row = payload_index.get(relative)
        require(
            isinstance(row, dict)
            and row.get("bytes") == path.stat().st_size
            and row.get("sha256") == sha256_file(path),
            ("runner/plan not bound by package manifest", relative),
        )

    report = load_json(report_path)
    summary = load_json(summary_path)
    plan = load_json(expected_plan)
    diff = load_json(diff_path)
    integrated = load_json(integrated_path)
    commands = report.get("commands")
    regeneration = plan.get("regeneration")
    require(isinstance(regeneration, dict), "active plan regeneration object")
    expected_names = regeneration.get("ordered_names")
    require(
        plan.get("schema") == "k3p-independent-referee-plan-v1"
        and regeneration.get("original_command_count") == 54
        and regeneration.get("mathematical_command_count") == 53
        and isinstance(expected_names, list)
        and len(expected_names) == 53
        and len(set(expected_names)) == 53,
        "active plan schema/count/order",
    )
    require(
        report.get("schema") == "k3p-independent-referee-run-v1"
        and report.get("status") == "PASS"
        and report.get("phase") == "regenerate"
        and report.get("command_count") == 53
        and isinstance(commands, list)
        and len(commands) == 53,
        "regeneration report status/count",
    )
    observed_names = [row.get("name") for row in commands]
    require(observed_names == expected_names, "regeneration command order drift")
    require(observed_names.count("probe_hour_scale_producer") == 1, "probe producer count")
    for row in commands:
        require(
            isinstance(row, dict)
            and row.get("status") == "PASS"
            and row.get("exit_code") == 0
            and row.get("sentinel_seen") is True
            and finite_nonnegative(row.get("elapsed_seconds"))
            and re.fullmatch(r"[0-9a-f]{64}", str(row.get("stdout_sha256"))) is not None,
            ("invalid command record", row.get("name") if isinstance(row, dict) else row),
        )
    require(
        finite_nonnegative(report.get("elapsed_seconds"))
        and report.get("workspace_drift") == {"added": [], "removed": [], "changed": []},
        "report elapsed time or runner workspace drift",
    )
    require(
        report.get("transcript", {}).get("path")
        == transcript_path.relative_to(package_root).as_posix()
        and report.get("transcript", {}).get("bytes") == transcript_path.stat().st_size
        and report.get("transcript", {}).get("sha256") == sha256_file(transcript_path),
        "report/transcript binding",
    )

    transcript = transcript_path.read_text(encoding="utf-8")
    header = parse_transcript(transcript, expected_names, commands)
    require(
        header.get("schema") == "k3p-independent-referee-transcript-v1"
        and header.get("phase") == "regenerate"
        and header.get("proof_source_commit") == package_manifest.get("proof_source_commit")
        and header.get("runtime") == report.get("runtime"),
        "transcript header binding",
    )
    require(
        header.get("python") == str(package_root / ".venv/bin/python"),
        "transcript interpreter path",
    )

    relative_session = session_root.relative_to(package_root).as_posix()
    phases = summary.get("phases")
    require(
        summary.get("status") == "PASS"
        and summary.get("mode") == "regenerate"
        and summary.get("session_root") == relative_session
        and isinstance(phases, list)
        and len(phases) == 1
        and phases[0] == {
            "phase": "regenerate",
            "commands": 53,
            "elapsed_seconds": report.get("elapsed_seconds"),
        },
        "session summary binding",
    )

    expected_supplemental = {
        path.relative_to(package_root).as_posix(): path
        for path in (*location_paths, integrated_path)
    }
    supplemental = report.get("supplemental_outputs")
    require(isinstance(supplemental, list) and len(supplemental) == 3, "supplemental outputs")
    supplemental_index = {
        row.get("path"): row for row in supplemental if isinstance(row, dict)
    }
    require(set(supplemental_index) == set(expected_supplemental), "supplemental path set")
    for relative, path in expected_supplemental.items():
        row = supplemental_index[relative]
        require(
            row.get("bytes") == path.stat().st_size
            and row.get("sha256") == sha256_file(path),
            ("supplemental binding", relative),
        )

    fresh_rows = integrated.get("fresh_replays")
    require(
        integrated.get("schema") == "k3p-same-integrated-classification-gate-v2"
        and integrated.get("status") == "CERTIFIED_K3P_SAME"
        and integrated.get("mathematical_classification_status") == "CERTIFIED"
        and isinstance(fresh_rows, list)
        and tuple(row.get("name") for row in fresh_rows) == EXPECTED_REPLAYS,
        "integrated fresh replay schema/order",
    )
    require(
        all(
            row.get("status") == "PASS"
            and row.get("exit_code") == 0
            and row.get("sentinel_seen") is True
            for row in fresh_rows
        ),
        "integrated child status",
    )
    observed_payload = sha256_bytes(
        json.dumps(
            integrated_logical_payload(integrated),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("utf-8")
    )
    require(integrated.get("payload_sha256") == observed_payload, "integrated payload hash")

    baseline_directory = package_root / "proof_package"
    target_directory = phase_root / "workspace"
    require(
        real_directory(baseline_directory) and real_directory(target_directory),
        "diff trees must be real directories",
    )
    require_no_symlink_components(baseline_directory)
    require_no_symlink_components(target_directory)
    differences = diff.get("difference_counts")
    added = diff.get("added")
    removed = diff.get("removed")
    changed = diff.get("changed")
    require(
        diff.get("schema") == "k3p-revision-referee-full-workspace-byte-diff-v1"
        and diff.get("baseline") == str(baseline_directory.resolve())
        and diff.get("target") == str(target_directory.resolve())
        and isinstance(differences, dict)
        and isinstance(added, list)
        and isinstance(removed, list)
        and isinstance(changed, list)
        and differences == {
            "added": len(added),
            "removed": len(removed),
            "changed": len(changed),
        }
        and removed == []
        and changed == [],
        "full workspace diff binding",
    )
    require(
        all(isinstance(row, dict) and set(row) == {"path", "after"} for row in added),
        "malformed added-path record",
    )
    added_paths = [safe_relative(row["path"]) for row in added]
    require(
        len(added_paths) == len(added)
        and len(set(added_paths)) == len(added_paths)
        and all(path == ".venv" or path.startswith("release/work/") for path in added_paths),
        "undeclared full-workspace addition",
    )
    unchanged = diff.get("unchanged_entries")
    baseline_entries = diff.get("baseline_entries")
    target_entries = diff.get("target_entries")
    unchanged_bytes = diff.get("unchanged_regular_file_bytes")
    require(
        all(isinstance(value, int) and value >= 0 for value in (unchanged, baseline_entries, target_entries))
        and isinstance(unchanged_bytes, int)
        and unchanged_bytes >= 0
        and baseline_entries == unchanged
        and target_entries == unchanged + len(added),
        "full workspace count arithmetic",
    )

    console = expected_console.read_text(encoding="utf-8")
    console_lines = console.splitlines()
    require(len(console_lines) >= 57, "outer console line count")
    console_summary = json.loads(console_lines[-2])
    progress_rows = []
    for line in console_lines:
        if line.startswith('{"command": '):
            value = json.loads(line)
            require(isinstance(value, dict), "outer progress object")
            progress_rows.append(value)
    require(
        console.count("K3P_REFEREE_PACKAGE_INTEGRITY_PASS") == 1
        and console.count("K3P_REFEREE_ACTIVE_VERIFIERS_PASS") == 1
        and "K3P_REFEREE_PACKAGE_INTEGRITY_FAIL" not in console
        and "K3P_REFEREE_ACTIVE_VERIFIERS_FAIL" not in console
        and console.rstrip().endswith("K3P_REFEREE_ACTIVE_VERIFIERS_PASS")
        and console_summary == summary
        and len(progress_rows) == 53
        and [row.get("command") for row in progress_rows] == expected_names
        and all(
            row
            == {
                "command": report_row["name"],
                "elapsed_seconds": report_row["elapsed_seconds"],
                "status": report_row["status"],
            }
            for row, report_row in zip(progress_rows, commands, strict=True)
        ),
        "outer console status/command inventory",
    )

    elapsed_by_name = {row["name"]: float(row["elapsed_seconds"]) for row in commands}
    sum_command_seconds = sum(elapsed_by_name.values())
    require(float(report["elapsed_seconds"]) >= sum_command_seconds, "phase elapsed below command sum")
    slowest = sorted(
        (
            {"name": name, "elapsed_seconds": elapsed}
            for name, elapsed in elapsed_by_name.items()
        ),
        key=lambda row: (-row["elapsed_seconds"], row["name"]),
    )[:10]
    evidence_summary = {
        "schema": "k3p-revision-referee-regeneration-seal-v1",
        "status": "PASS",
        "proof_source_commit": package_manifest.get("proof_source_commit"),
        "command_count": 53,
        "command_order": observed_names,
        "elapsed_seconds": float(report["elapsed_seconds"]),
        "sum_command_seconds": sum_command_seconds,
        "slowest_commands": slowest,
        "probe_hour_scale_producer_count": 1,
        "integrated_fresh_replay_count": len(fresh_rows),
        "runner_workspace_drift": report["workspace_drift"],
        "full_workspace_difference_counts": differences,
        "full_workspace_added": added,
        "baseline_entries": baseline_entries,
        "target_entries": target_entries,
        "unchanged_entries": unchanged,
        "unchanged_regular_file_bytes": unchanged_bytes,
        "retained_sandbox_profile": {
            "path": os.path.relpath(expected_profile, phase_root),
            "path_base": "directory containing REGENERATION_SEAL.json",
            "sha256": sha256_file(expected_profile),
            "evidentiary_role": (
                "This binds the retained policy file, not its historical use; "
                "sandbox use is established procedurally by the recorded invocation "
                "and live denial probes outside this seal."
            ),
        },
    }
    ledger_records: dict[str, str] = {}
    for path in (*evidence_inputs, package_manifest_path):
        relative = os.path.relpath(path, phase_root)
        require(relative not in ledger_records, ("duplicate ledger path", relative))
        ledger_records[relative] = sha256_file(path)
    seal_value = {
        "schema": "k3p-revision-referee-regeneration-seal-bundle-v1",
        "status": "PASS",
        "summary": evidence_summary,
        "sha256_ledger": [
            {"path": relative, "sha256": digest}
            for relative, digest in sorted(ledger_records.items())
        ],
    }
    seal_bytes = (json.dumps(seal_value, indent=2, sort_keys=True) + "\n").encode("utf-8")
    atomic_publish_file(seal_path, seal_bytes)
    print(json.dumps(evidence_summary, sort_keys=True))
    print("K3P_REVISION_REFEREE_REGENERATION_SEAL_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
