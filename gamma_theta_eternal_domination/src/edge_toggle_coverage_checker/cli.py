"""CLI for the independent edge-toggle coverage/isomorphism audit."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sqlite3
import sys

from .audit import AuditError, AuditPaths, run_audit


def _campaign_root() -> Path:
    return Path(__file__).resolve().parents[2]


def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    campaign = _campaign_root()
    parser = argparse.ArgumentParser(
        description=(
            "Independently reconstruct all 25,641 one-edge toggles and audit "
            "a completed production ledger. This never launches the search."
        )
    )
    parser.add_argument("--campaign-root", type=Path, default=campaign)
    parser.add_argument(
        "--seed-input",
        type=Path,
        default=campaign / "results" / "extensions_unique.csv",
    )
    parser.add_argument(
        "--extension-coverage-audit",
        type=Path,
        default=campaign / "results" / "extension_coverage_audit.json",
    )
    parser.add_argument(
        "--extension-evaluation-audit",
        type=Path,
        default=campaign / "results" / "extensions_evaluation_audit.json",
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=campaign / "results" / "checkpoints" / "edge_toggles.sqlite3",
    )
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=campaign / "results" / "checkpoints" / "edge_toggles.json",
    )
    parser.add_argument(
        "--provenance",
        type=Path,
        default=campaign / "results" / "edge_toggles_provenance.csv",
    )
    parser.add_argument(
        "--unique",
        type=Path,
        default=campaign / "results" / "edge_toggles_unique.csv",
    )
    parser.add_argument(
        "--candidate-directory",
        type=Path,
        default=campaign / "certificates" / "frozen_edge_toggle_candidates",
    )
    parser.add_argument(
        "--state",
        type=Path,
        default=(
            campaign
            / "results"
            / "checkpoints"
            / "edge_toggle_coverage_audit.sqlite3"
        ),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=campaign / "results" / "edge_toggle_coverage_audit.json",
    )
    parser.add_argument("--checkpoint-interval", type=int, default=256)
    parser.add_argument("--max-new-origins", type=int)
    parser.add_argument("--wall-limit-seconds", type=float, default=2700.0)
    parser.add_argument("--memory-limit-mib", type=float, default=1024.0)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    arguments = parse_arguments(argv)
    paths = AuditPaths(
        campaign_root=arguments.campaign_root,
        seed_input=arguments.seed_input,
        extension_coverage_audit=arguments.extension_coverage_audit,
        extension_evaluation_audit=arguments.extension_evaluation_audit,
        database=arguments.database,
        checkpoint=arguments.checkpoint,
        provenance_csv=arguments.provenance,
        unique_csv=arguments.unique,
        candidate_directory=arguments.candidate_directory,
        state_database=arguments.state,
        report=arguments.report,
    )
    try:
        outcome = run_audit(
            paths=paths,
            checkpoint_interval=arguments.checkpoint_interval,
            max_new_origins=arguments.max_new_origins,
            wall_limit_seconds=arguments.wall_limit_seconds,
            memory_limit_mib=arguments.memory_limit_mib,
        )
    except (AuditError, ValueError, sqlite3.Error) as error:
        print(f"edge-toggle coverage audit failed closed: {error}", file=sys.stderr)
        return 2
    print(json.dumps(asdict(outcome), indent=2, sort_keys=True))
    return 0 if outcome.status == "complete" else 3


if __name__ == "__main__":
    raise SystemExit(main())
