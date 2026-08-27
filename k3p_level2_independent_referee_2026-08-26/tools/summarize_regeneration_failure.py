#!/usr/bin/env python3
"""Validate and summarize a 44-command transcript whose outer drift gate failed."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--transcript", required=True, type=Path)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--before-report", required=True, type=Path)
    parser.add_argument("--after-report", required=True, type=Path)
    parser.add_argument("--primary-output", required=True, type=Path)
    parser.add_argument("--integrated-output", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    records = []
    for line in args.transcript.read_text(encoding="utf-8").splitlines():
        if line.startswith("RESULT "):
            records.append(json.loads(line[len("RESULT "):]))
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    expected = plan["regeneration"]["ordered_names"]
    names = [record["name"] for record in records]
    if names != expected:
        raise RuntimeError(("ordered command mismatch", names, expected))
    if not all(
        row.get("status") == "PASS"
        and row.get("exit_code") == 0
        and row.get("sentinel_seen") is True
        for row in records
    ):
        raise RuntimeError("one or more transcript commands did not pass")

    transcript_stat = args.transcript.stat()
    report = {
        "schema": "k3p-referee-once-only-regeneration-failure-summary-v1",
        "overall_status": "FAIL_OUTER_DRIFT_AFTER_ALL_COMMANDS_PASS",
        "command_count": len(records),
        "ordered_names_match_declared_plan": True,
        "all_command_exit_codes_zero": True,
        "all_command_sentinels_seen": True,
        "command_elapsed_seconds_sum": sum(
            float(row["elapsed_seconds"]) for row in records
        ),
        "transcript_filesystem_wall_seconds": (
            transcript_stat.st_mtime - transcript_stat.st_birthtime
        ),
        "commands": records,
        "slowest_commands": sorted(
            (
                {"name": row["name"], "elapsed_seconds": row["elapsed_seconds"]}
                for row in records
            ),
            key=lambda row: float(row["elapsed_seconds"]),
            reverse=True,
        )[:8],
        "transcript": {
            "path": str(args.transcript.resolve()),
            "bytes": transcript_stat.st_size,
            "sha256": digest(args.transcript),
        },
        "outer_failure": {
            "reason": "unexpected workspace drift",
            "changed_path": "restoration/K3P_RESTORATION_THEOREM_REPORT.md",
            "before": {
                "bytes": args.before_report.stat().st_size,
                "sha256": digest(args.before_report),
            },
            "after": {
                "bytes": args.after_report.stat().st_size,
                "sha256": digest(args.after_report),
            },
            "semantic_difference": (
                "one reproduction-command cwd line changed from the source-project "
                "absolute path to the isolated regeneration-workspace absolute path"
            ),
            "runner_report_created": False,
            "runner_summary_created": False,
        },
        "preserved_supplemental_outputs": [
            {
                "role": "primary location-dependent report",
                "path": str(args.primary_output.resolve()),
                "bytes": args.primary_output.stat().st_size,
                "sha256": digest(args.primary_output),
            },
            {
                "role": "integrated ten-child fresh report",
                "path": str(args.integrated_output.resolve()),
                "bytes": args.integrated_output.stat().st_size,
                "sha256": digest(args.integrated_output),
            },
        ],
        "rerun_policy": "not rerun: the referee prompt permits exactly one complete regeneration",
    }
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "overall_status": report["overall_status"],
        "command_count": report["command_count"],
        "command_elapsed_seconds_sum": report["command_elapsed_seconds_sum"],
        "transcript_filesystem_wall_seconds": report["transcript_filesystem_wall_seconds"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
