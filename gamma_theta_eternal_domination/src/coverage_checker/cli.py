"""Command-line interface for the independent post-run extension audit."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys

from .audit import AuditError, AuditPaths, run_postrun_audit


def _campaign_root() -> Path:
    return Path(__file__).resolve().parents[2]


def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    campaign = _campaign_root()
    parser = argparse.ArgumentParser(
        description=(
            "Independently reconstruct and audit a completed 55-host "
            "one-vertex-extension ledger. This never launches the search."
        )
    )
    parser.add_argument(
        "--campaign-root", type=Path, default=campaign
    )
    parser.add_argument(
        "--catalog",
        type=Path,
        default=campaign / "instances" / "mmv2022_table9.csv",
    )
    parser.add_argument(
        "--parameters",
        type=Path,
        default=campaign / "results" / "mmv2022_parameters.csv",
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=campaign / "results" / "checkpoints" / "extensions.sqlite3",
    )
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=campaign / "results" / "checkpoints" / "extensions.json",
    )
    parser.add_argument(
        "--provenance",
        type=Path,
        default=campaign / "results" / "extensions_provenance.csv",
    )
    parser.add_argument(
        "--unique",
        type=Path,
        default=campaign / "results" / "extensions_unique.csv",
    )
    parser.add_argument(
        "--state",
        type=Path,
        default=(
            campaign
            / "results"
            / "checkpoints"
            / "extensions_coverage_audit.sqlite3"
        ),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=campaign / "results" / "extension_coverage_audit.json",
    )
    parser.add_argument("--checkpoint-interval", type=int, default=256)
    parser.add_argument(
        "--max-new-origins",
        type=int,
        help="cleanly stop after this many newly checked origins",
    )
    parser.add_argument("--wall-limit-seconds", type=float, default=2700.0)
    parser.add_argument("--memory-limit-mib", type=float, default=1024.0)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    arguments = parse_arguments(argv)
    paths = AuditPaths(
        campaign_root=arguments.campaign_root,
        catalog=arguments.catalog,
        parameters=arguments.parameters,
        database=arguments.database,
        checkpoint=arguments.checkpoint,
        provenance_csv=arguments.provenance,
        unique_csv=arguments.unique,
        state_database=arguments.state,
        report=arguments.report,
    )
    try:
        outcome = run_postrun_audit(
            paths=paths,
            checkpoint_interval=arguments.checkpoint_interval,
            max_new_origins=arguments.max_new_origins,
            wall_limit_seconds=arguments.wall_limit_seconds,
            memory_limit_mib=arguments.memory_limit_mib,
        )
    except (AuditError, ValueError) as error:
        print(f"coverage audit failed closed: {error}", file=sys.stderr)
        return 2
    print(json.dumps(asdict(outcome), indent=2, sort_keys=True))
    return 0 if outcome.status == "complete" else 3


if __name__ == "__main__":
    raise SystemExit(main())
