#!/usr/bin/env python3
"""Greedy discovery minimization of pairwise gamma constraints."""

from __future__ import annotations

import argparse
import importlib.util
from itertools import combinations
from pathlib import Path
import subprocess
import tempfile


def load_synthesis(path: Path):
    spec = importlib.util.spec_from_file_location("mixed_synth", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load synthesis module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    args = parser.parse_args()
    synthesis = load_synthesis(Path(__file__).with_name("synth_mixed_path.py"))
    selected = set(combinations(range(args.order), 2))

    with tempfile.TemporaryDirectory(prefix="unit-chain-minimize-") as temp:
        instance = Path(temp) / "instance.cnf"

        def solve(pairs: set[tuple[int, int]]) -> int:
            cnf, _edges, _family = synthesis.build(
                args.order,
                enforce_gamma=True,
                gamma_pairs=pairs,
            )
            instance.write_text(cnf.dimacs(), encoding="ascii")
            run = subprocess.run(
                [
                    str(args.solver),
                    "--quiet",
                    "--binary=false",
                    str(instance),
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            return run.returncode

        if solve(selected) != 20:
            raise AssertionError("full instance was expected UNSAT")
        for candidate in sorted(tuple(selected), reverse=True):
            trial = selected - {candidate}
            status = solve(trial)
            if status == 20:
                selected = trial
                action = "drop"
            elif status == 10:
                action = "keep"
            else:
                raise RuntimeError(f"solver status {status}")
            print(
                f"pair={candidate} action={action} remaining={len(selected)}"
            )
        print(f"minimal_count={len(selected)} pairs={sorted(selected)}")


if __name__ == "__main__":
    main()
