#!/usr/bin/env python3
"""Greedily shrink the non-dominating-pair obligations in the SAT probe."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import subprocess
import tempfile
from pathlib import Path

SOURCE = Path(__file__).with_name("synthesize.py")
SPEC = importlib.util.spec_from_file_location("family_mixed_p4_synthesize", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load synthesize.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
make_formula = MODULE.make_formula


def unsat(
    order: int,
    pairs: set[tuple[int, int]],
    solver: Path,
    enforce_alpha: bool,
) -> bool:
    formula, _ = make_formula(order, pairs, enforce_alpha=enforce_alpha)
    with tempfile.NamedTemporaryFile(suffix=".cnf") as handle:
        formula.write(Path(handle.name))
        run = subprocess.run(
            [str(solver), "-q", handle.name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
    if run.returncode not in (10, 20):
        raise RuntimeError(
            f"solver failed with {run.returncode}: {run.stderr}\n{run.stdout}"
        )
    return run.returncode == 20


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, default=12)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--pair", action="append", default=[], metavar="U,V")
    parser.add_argument("--reverse", action="store_true")
    parser.add_argument("--no-alpha-bound", action="store_true")
    args = parser.parse_args()

    if args.pair:
        active = {
            tuple(sorted(int(value) for value in raw.split(",")))
            for raw in args.pair
        }
    else:
        active = set(itertools.combinations(range(args.order), 2))
    if not unsat(
        args.order, active, args.solver, not args.no_alpha_bound
    ):
        raise RuntimeError("full instance unexpectedly SAT")

    changed = True
    passes = 0
    while changed:
        changed = False
        passes += 1
        for pair in sorted(active, reverse=args.reverse):
            trial = active - {pair}
            if unsat(
                args.order, trial, args.solver, not args.no_alpha_bound
            ):
                active = trial
                changed = True
                print(
                    json.dumps(
                        {
                            "pass": passes,
                            "removed": pair,
                            "remaining": len(active),
                        }
                    ),
                    flush=True,
                )

    print(
        json.dumps(
            {
                "schema": "family-mixed-p4-gamma-pair-mus-discovery-v1",
                "classification": "OBSERVED_DISCOVERY_ONLY",
                "order": args.order,
                "greedy_irredundant_gamma_pairs": sorted(active),
                "count": len(active),
                "passes": passes,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
