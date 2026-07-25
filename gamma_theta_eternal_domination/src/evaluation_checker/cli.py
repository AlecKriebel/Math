"""Command-line entry point for the independent mathematical audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .audit import (
    EvaluationAuditError,
    EvaluationPaths,
    PRODUCTION_POLICY,
    collect_binding,
    run_evaluation_audit,
    verify_certificate,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Independently evaluate all 54,216 canonical extension rows and "
            "emit/replay compact mathematical certificates."
        )
    )
    parser.add_argument("--campaign-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--unique-csv",
        type=Path,
        default=Path("results/extensions_unique.csv"),
    )
    parser.add_argument(
        "--provenance-csv",
        type=Path,
        default=Path("results/extensions_provenance.csv"),
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=Path("results/checkpoints/extensions.sqlite3"),
    )
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=Path("results/checkpoints/extensions.json"),
    )
    parser.add_argument(
        "--coverage-report",
        type=Path,
        default=Path("results/extension_coverage_audit.json"),
    )
    parser.add_argument(
        "--coverage-state-database",
        type=Path,
        default=Path(
            "results/checkpoints/extensions_coverage_audit.sqlite3"
        ),
    )
    parser.add_argument(
        "--certificate",
        type=Path,
        default=Path("results/extensions_evaluation_certificates.ndjson"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("results/extensions_evaluation_audit.json"),
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="replay an existing certificate without replacing it",
    )
    return parser


def _under_root(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def main(argv: list[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    root = arguments.campaign_root.expanduser().resolve()
    paths = EvaluationPaths(
        campaign_root=root,
        unique_csv=_under_root(root, arguments.unique_csv),
        provenance_csv=_under_root(root, arguments.provenance_csv),
        database=_under_root(root, arguments.database),
        checkpoint=_under_root(root, arguments.checkpoint),
        coverage_report=_under_root(root, arguments.coverage_report),
        coverage_state_database=_under_root(
            root, arguments.coverage_state_database
        ),
        certificate=_under_root(root, arguments.certificate),
        report=_under_root(root, arguments.report),
    )
    try:
        if arguments.verify_only:
            binding, source_manifest = collect_binding(
                paths, PRODUCTION_POLICY
            )
            outcome = verify_certificate(
                paths.unique_csv,
                paths.certificate,
                binding=binding,
                source_manifest=source_manifest,
                policy=PRODUCTION_POLICY,
            )
            mode = "verify-only"
        else:
            outcome = run_evaluation_audit(paths, PRODUCTION_POLICY)
            mode = "generate-and-replay"
    except EvaluationAuditError as error:
        print(
            json.dumps(
                {"error": str(error), "passed": False},
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 2
    print(
        json.dumps(
            {
                "category_counts": dict(outcome.category_counts),
                "certificate_sha256": outcome.certificate_sha256,
                "mode": mode,
                "passed": True,
                "record_lines_sha256": outcome.record_lines_sha256,
                "row_count": outcome.row_count,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
