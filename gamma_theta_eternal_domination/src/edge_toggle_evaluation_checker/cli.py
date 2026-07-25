"""Command-line entry point for the third edge-toggle mathematical audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .audit import AuditPaths, ThirdAuditError, run_audit


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    root = _root()
    parser = argparse.ArgumentParser(
        description=(
            "Independently prove gamma < one-guard eternal domination for "
            "every canonical row in the completed edge-toggle ledger."
        )
    )
    parser.add_argument("--campaign-root", type=Path, default=root)
    parser.add_argument(
        "--database",
        type=Path,
        default=root / "results/checkpoints/edge_toggles.sqlite3",
    )
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=root / "results/checkpoints/edge_toggles.json",
    )
    parser.add_argument(
        "--provenance",
        type=Path,
        default=root / "results/edge_toggles_provenance.csv",
    )
    parser.add_argument(
        "--unique",
        type=Path,
        default=root / "results/edge_toggles_unique.csv",
    )
    parser.add_argument(
        "--coverage-report",
        type=Path,
        default=root / "results/edge_toggle_coverage_audit.json",
    )
    parser.add_argument(
        "--certificate",
        type=Path,
        default=(
            root
            / "results"
            / "edge_toggle_third_evaluation_certificates.ndjson"
        ),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=root / "results/edge_toggle_third_evaluation_audit.json",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="replay the installed certificate and require the existing report",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    arguments = parse_arguments(argv)
    paths = AuditPaths(
        campaign_root=arguments.campaign_root,
        database=arguments.database,
        checkpoint=arguments.checkpoint,
        provenance_csv=arguments.provenance,
        unique_csv=arguments.unique,
        coverage_report=arguments.coverage_report,
        certificate=arguments.certificate,
        report=arguments.report,
    )
    try:
        outcome = run_audit(paths, verify_only=arguments.verify_only)
    except (ThirdAuditError, ValueError) as error:
        print(f"third edge-toggle audit failed closed: {error}", file=sys.stderr)
        return 2
    print(json.dumps(outcome, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
