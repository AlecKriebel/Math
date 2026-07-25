#!/usr/bin/env python3
"""Iterate exact row facets and numerical noncentered BV repairs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SEARCH = ROOT / "experiments" / "continuous_rank_bv_search" / "search.py"
VERIFY_BV = ROOT / "verifiers" / "verify_fixed41_bv_degree5.py"


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.DEVNULL,
        check=False,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warm", type=Path, required=True)
    parser.add_argument("--cut", type=Path, action="append", default=[])
    parser.add_argument("--start-index", type=int, required=True)
    parser.add_argument("--iterations", type=int, default=6)
    args = parser.parse_args()
    warm = args.warm.resolve()
    cuts = [path.resolve() for path in args.cut]
    summary = []
    for index in range(
        args.start_index, args.start_index + args.iterations
    ):
        numerical = HERE / f"noncentered_{index}_cuts_d12.json"
        candidate = HERE / f"candidate_exact_{index}.json"
        next_cut = HERE / f"integer_degree_obstruction_{index + 1}.json"
        command = [
            sys.executable,
            str(SEARCH),
            "--grid",
            "quarter",
            "--harmonic-degree",
            "12",
            "--pair-degree",
            "100",
            "--kernel-profile",
            "rich",
            "--pair-mode",
            "local-warm",
            "--warm-from",
            str(warm),
            "--robust-vertex-marginals",
            "--integer-degree-cut",
            "--solver",
            "CLARABEL",
            "--output",
            str(numerical),
        ]
        for cut in cuts:
            command.extend(("--extra-integer-degree-cut", str(cut)))
        if run(command).returncode:
            raise RuntimeError(f"numerical repair failed at cut {index}")
        if run(
            [
                sys.executable,
                str(HERE / "rationalize.py"),
                "--source",
                str(numerical),
                "--output",
                str(candidate),
            ]
        ).returncode:
            raise RuntimeError(f"rationalization failed at cut {index}")
        if run([sys.executable, str(VERIFY_BV), str(candidate)]).returncode:
            raise RuntimeError(f"exact BV check failed at cut {index}")
        separation = run(
            [
                sys.executable,
                str(HERE / "separate_integer_rows.py"),
                "--source",
                str(candidate),
                "--output",
                str(next_cut),
            ]
        )
        payload = json.loads(numerical.read_text())
        entry = {
            "cut_count": index,
            "objective_margin": payload["objective_margin"],
            "minimum_bv_margin_eigenvalue": min(
                payload["minimum_margin_bv_eigenvalues"]
            ),
            "integer_cut_values": payload["integer_degree_cut_values"],
            "separated_again": separation.returncode == 0,
        }
        summary.append(entry)
        if separation.returncode:
            mixture = run(
                [
                    sys.executable,
                    str(HERE / "solve_integer_row_mixture.py"),
                    "--source",
                    str(candidate),
                    "--output",
                    str(HERE / f"integer_row_mixture_{index}.json"),
                ]
            )
            entry["exact_mixture_reconstruction_returncode"] = (
                mixture.returncode
            )
            break
        cuts.append(next_cut)
        warm = numerical
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
