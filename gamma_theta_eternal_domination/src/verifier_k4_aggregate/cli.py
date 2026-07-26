"""Command-line entry point for the independent aggregate auditor."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time
from typing import Sequence

from .checker import (
    AGGREGATE_REPORT_SCHEMA,
    AGGREGATE_REPORT_SCHEMA_VERSION,
    AuditError,
    AuditPolicy,
    FAILURE_STATUS,
    ResourceGateError,
    SatLeafPresentError,
    VERIFIER,
    audit_run,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Independently audit and freshly replay a frozen order-12, "
            "parameter-four 16-leaf run."
        )
    )
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument(
        "--replay-dir",
        required=True,
        type=Path,
        help=(
            "Dedicated external directory for append-only per-leaf replay "
            "records; it must not be beneath the frozen production run."
        ),
    )
    parser.add_argument("--wall-seconds", type=int, default=1_800)
    parser.add_argument("--memory-mib", type=int, default=4_096)
    parser.add_argument("--file-limit-mib", type=int, default=16)
    parser.add_argument("--load-max", type=float, default=7.5)
    parser.add_argument("--memory-reserve-mib", type=int, default=2_048)
    parser.add_argument("--disk-reserve-mib", type=int, default=512)
    return parser


def _failure(status: str, error: BaseException) -> dict[str, object]:
    return {
        "schema": AGGREGATE_REPORT_SCHEMA,
        "schema_version": AGGREGATE_REPORT_SCHEMA_VERSION,
        "verifier": VERIFIER,
        "status": status,
        "claim_boundary": "NO_AGGREGATE_OR_MATHEMATICAL_CLAIM",
        "error_type": type(error).__name__,
        "error": str(error),
        "completed_unix_ns": time.time_ns(),
    }


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    policy = AuditPolicy(
        wall_seconds=arguments.wall_seconds,
        memory_mib=arguments.memory_mib,
        file_limit_mib=arguments.file_limit_mib,
        load_max=arguments.load_max,
        memory_reserve_mib=arguments.memory_reserve_mib,
        disk_reserve_mib=arguments.disk_reserve_mib,
    )
    try:
        report = audit_run(
            arguments.run_dir,
            policy=policy,
            replay_directory=arguments.replay_dir,
        )
    except SatLeafPresentError as error:
        report = _failure("SAT_CANDIDATE_HOLD_NONCLAIM", error)
        exit_code = 3
    except ResourceGateError as error:
        report = _failure("RESOURCE_GATE_BLOCKED_NONCLAIM", error)
        exit_code = 4
    except (AuditError, OSError) as error:
        report = _failure(FAILURE_STATUS, error)
        exit_code = 2
    else:
        exit_code = 0 if report["status"].startswith("CERTIFIED_") else 3
    json.dump(
        report,
        sys.stdout,
        allow_nan=False,
        ensure_ascii=True,
        indent=2,
        sort_keys=True,
    )
    sys.stdout.write("\n")
    return exit_code


__all__ = ["main"]
