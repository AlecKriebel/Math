#!/usr/bin/env python3
"""Iterate exact seven-bin row facets against one numerical SDP cell.

Every generated facet is exhaustively integer-verified by
``separate_refined_rows.py``.  The SDP sources remain finite-grid,
floating-point discovery objects and are never certificates.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
SEARCH = Path(__file__).with_name("search.py")
SEPARATE = Path(__file__).with_name("separate_refined_rows.py")


def run(command: list[str]) -> None:
    subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        stdout=subprocess.DEVNULL,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", required=True)
    parser.add_argument("--start-result", type=Path, required=True)
    parser.add_argument("--initial-facet", type=Path, action="append", default=[])
    parser.add_argument("--iterations", type=int, default=5)
    parser.add_argument("--h1-lower", default="2")
    parser.add_argument("--h1-upper", default="5/2")
    args = parser.parse_args()

    directory = Path(__file__).resolve().parent
    source = args.start_result.resolve()
    facets = [path.resolve() for path in args.initial_facet]
    summaries = []
    for offset in range(args.iterations):
        index = len(facets)
        facet = directory / f"{args.prefix}_facet_{index}.json"
        result = directory / f"{args.prefix}_result_{index + 1}.json"
        run(
            [
                sys.executable,
                str(SEPARATE),
                str(source),
                "--output",
                str(facet),
            ]
        )
        facets.append(facet)
        command = [
            sys.executable,
            str(SEARCH),
            "--grid",
            "quarter",
            "--harmonic-degree",
            "16",
            "--pair-degree",
            "120",
            "--coarse-lift",
            "--rank-bands",
            "--h1-variance-lower",
            args.h1_lower,
            "--h1-variance-upper",
            args.h1_upper,
            "--output",
            str(result),
        ]
        for path in facets:
            command.extend(("--refined-facet", str(path)))
        run(command)
        payload = json.loads(result.read_text())
        summaries.append(
            {
                "iteration": offset,
                "facet_count": len(facets),
                "status": payload["status"],
                "objective": payload["objective_average_row_energy"],
                "minimum_bv_eigenvalue": min(
                    payload.get("minimum_bv_eigenvalues", [float("nan")])
                ),
            }
        )
        source = result
    print(json.dumps(summaries, indent=2))


if __name__ == "__main__":
    main()
