#!/usr/bin/env python3
"""Bounded discovery probe for the order-13 no-full-list k=3 branch.

This deliberately reuses only the already frozen variable allocator and
general equality/closure clause builder from the full-target discovery
formula.  It removes the six units that distinguish vertex 3 as a full
target, then forbids a full response at every vertex outside the fixed
independent state S={0,1,2}.

The output is discovery evidence until a separate generator reconstructs
the formula and a hostile audit proves coverage.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys


S = (0, 1, 2)
N = 13


def load_frozen_builder(campaign: Path):
    source = (
        campaign
        / "math"
        / "working"
        / "order13_single_full_squeeze"
        / "search.py"
    )
    spec = importlib.util.spec_from_file_location(
        "order13_full_target_frozen_builder", source
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load frozen builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def remove_once(clauses: list[tuple[int, ...]], clause: tuple[int, ...]) -> None:
    matches = [index for index, existing in enumerate(clauses) if existing == clause]
    if len(matches) != 1:
        raise AssertionError(
            f"expected one removable distinguished-target clause {clause}, "
            f"found {len(matches)}"
        )
    clauses.pop(matches[0])


def build_no_full(campaign: Path):
    module = load_frozen_builder(campaign)
    cnf, edge, family = module.build(
        sort_signatures=True,
        require_theta_gap=True,
        require_unique_full=False,
        require_closure=True,
        use_witness_bound=False,
        require_connected=False,
        force_all_independent_states=False,
    )

    def e(u: int, v: int) -> int:
        return edge[(u, v) if u < v else (v, u)]

    # Remove exactly the three G-edge units and three retained-successor
    # units that made vertex 3 a distinguished full target.  The anchor
    # H-triangle and retained anchor state remain fixed.
    distinguished = 3
    for guard in S:
        remove_once(cnf.clauses, (-e(guard, distinguished),))
        successor = tuple(sorted((set(S) - {guard}) | {distinguished}))
        remove_once(cnf.clauses, (family[successor],))

    # A retained successor S-{guard}+{target} already implies the target is
    # G-adjacent to the omitted guard: otherwise that state misses the guard.
    # Thus this clause is exactly |L_S(target)| <= 2.
    for target in range(3, N):
        successors = [
            family[tuple(sorted((set(S) - {guard}) | {target}))]
            for guard in S
        ]
        cnf.add(*(-state for state in successors))

    return cnf


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--instance", type=Path, required=True)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--solver-log", type=Path, required=True)
    args = parser.parse_args()

    campaign = Path(__file__).resolve().parents[3]
    cnf = build_no_full(campaign)
    args.instance.parent.mkdir(parents=True, exist_ok=True)
    args.instance.write_text(cnf.dimacs(), encoding="ascii")

    command = [str(args.solver), "--quiet", "--binary=false", str(args.instance)]
    if args.proof is not None:
        command.append(str(args.proof))
    try:
        completed = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=args.timeout,
            check=False,
        )
        status = (
            "SAT"
            if completed.returncode == 10
            else "UNSAT"
            if completed.returncode == 20
            else f"EXIT_{completed.returncode}"
        )
        output = completed.stdout
    except subprocess.TimeoutExpired as error:
        status = "TIMEOUT"
        output = (error.stdout or "") + (error.stderr or "")

    args.solver_log.write_text(output, encoding="utf-8")
    print(
        f"variables={len(cnf.names)-1} clauses={len(cnf.clauses)} "
        f"status={status}"
    )
    if status == "TIMEOUT":
        sys.exit(124)
    if status == "UNSAT":
        sys.exit(20)
    if status == "SAT":
        sys.exit(10)
    sys.exit(1)


if __name__ == "__main__":
    main()
