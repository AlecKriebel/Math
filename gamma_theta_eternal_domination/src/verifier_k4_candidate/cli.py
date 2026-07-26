"""Command-line interface for the independent k=4 candidate checker."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .checker import (
    CandidateFormatError,
    VERIFIER,
    load_candidate,
    verify_candidate,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Independently verify a decoded connected order-12, "
            "parameter-4 gamma-theta counterexample candidate."
        )
    )
    parser.add_argument("candidate", type=Path)
    parser.add_argument(
        "--color-trace",
        type=Path,
        help=(
            "exclusively create a complete 65,536-row anchored "
            "four-coloring trace"
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version=VERIFIER,
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        candidate_path = arguments.candidate.resolve(strict=True)
        trace_path = (
            arguments.color_trace.resolve(strict=False)
            if arguments.color_trace is not None
            else None
        )
        if trace_path is not None:
            if trace_path == candidate_path:
                raise CandidateFormatError(
                    "candidate and trace paths must differ"
                )
            if trace_path.exists():
                raise CandidateFormatError(
                    "color trace output already exists"
                )
        candidate, source_hash = load_candidate(candidate_path)
        report = verify_candidate(
            candidate,
            source_sha256=source_hash,
            color_trace_path=trace_path,
        )
    except (CandidateFormatError, OSError, ValueError) as error:
        report = {
            "verifier": VERIFIER,
            "status": "MALFORMED_OR_IO_ERROR",
            "accepted": False,
            "error": str(error),
        }
        print(json.dumps(report, sort_keys=True, indent=2))
        return 2
    print(json.dumps(report, sort_keys=True, indent=2))
    return 0 if report["accepted"] else 1


if __name__ == "__main__":
    sys.exit(main())
