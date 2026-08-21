#!/usr/bin/env python3
"""Discovery CEGAR for the gamma constraints in the mixed-P4 synthesis.

At each iteration the current SAT model is inspected for dominating pairs
of G, equivalently pairs with no common H-neighbor.  The missing gamma
constraints for all such pairs are added.  This is only a proof-discovery
aid: labels of spare vertices are not canonical and an UNSAT endpoint is
not a universal graph theorem.
"""

from __future__ import annotations

import argparse
import importlib.util
from itertools import combinations
from pathlib import Path
import subprocess


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
    parser.add_argument("--iterations", type=int, default=100)
    parser.add_argument("--work-prefix", type=Path, required=True)
    parser.add_argument("--initial-anchors", default="")
    args = parser.parse_args()

    synthesis = load_synthesis(Path(__file__).with_name("synth_mixed_path.py"))
    initial_anchors = {
        int(value) for value in args.initial_anchors.split(",") if value
    }
    selected: set[tuple[int, int]] = {
        (u, v)
        for u, v in combinations(range(args.order), 2)
        if u in initial_anchors or v in initial_anchors
    }
    for iteration in range(args.iterations):
        cnf, edge_h, _family = synthesis.build(
            args.order,
            enforce_gamma=True,
            gamma_pairs=selected,
        )
        instance = args.work_prefix.with_name(
            args.work_prefix.name + f".{iteration:03d}.cnf"
        )
        model = args.work_prefix.with_name(
            args.work_prefix.name + f".{iteration:03d}.model"
        )
        instance.write_text(cnf.dimacs(), encoding="ascii")
        run = subprocess.run(
            [
                str(args.solver),
                "--quiet",
                "--binary=false",
                "-w",
                str(model),
                str(instance),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        if run.returncode == 20:
            print(
                f"iteration={iteration} status=UNSAT"
                f" constrained_pairs={len(selected)}"
                f" pairs={sorted(selected)}"
            )
            return
        if run.returncode != 10:
            raise RuntimeError(
                f"solver exit {run.returncode}: {run.stdout[-1000:]}"
            )
        true_variables = synthesis.parse_model(model, len(cnf.names) - 1)
        h_edges = {
            uv for uv, marker in edge_h.items() if marker in true_variables
        }
        bad = set()
        for u, v in combinations(range(args.order), 2):
            if not any(
                synthesis.pair(u, w) in h_edges
                and synthesis.pair(v, w) in h_edges
                for w in range(args.order)
                if w not in (u, v)
            ):
                bad.add((u, v))
        new = bad - selected
        print(
            f"iteration={iteration} status=SAT"
            f" constrained_pairs={len(selected)}"
            f" dominating_pairs={len(bad)} new={sorted(new)}"
        )
        if not new:
            raise AssertionError("SAT gamma=3 model should have terminated")
        selected.update(new)
    raise RuntimeError("iteration budget exhausted")


if __name__ == "__main__":
    main()
