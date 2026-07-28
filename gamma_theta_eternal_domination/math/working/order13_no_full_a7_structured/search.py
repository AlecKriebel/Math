#!/usr/bin/env python3
"""Structured discovery formula for the residual order-13 no-full branch.

Assuming the independently reviewed no-full decomposition and the
provisional four-neutral micro-exclusion, any surviving counterexample has
at least two exact two-list types and at most three neutral vertices.
Relabel the anchors so that two occurring types omit anchors 0 and 2.
The physical-representative theorem then permits the following labels:

* 3 is a pure-signature exact type-0 representative and 4 is its pure
  complement-adjacent mate;
* 5 is a pure-signature exact type-2 representative and 6 is its pure
  complement-adjacent mate.

Vertices 7,...,12 remain interchangeable, so their three-bit complement
signatures are sorted.  Since the four named vertices are nonneutral,
``|Q_S| <= 3`` is exactly the assertion that residual label 10 is
nonneutral.

This is an exploratory formula until the provisional cut, the relabeling
coverage, an independent generator, and any UNSAT proof are all audited.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys


N = 13
S = (0, 1, 2)
OUTSIDE = tuple(range(3, N))
RESIDUAL = tuple(range(7, N))


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(
        "order13_full_target_base_for_structured_no_full", path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def remove_once(clauses: list[tuple[int, ...]], clause: tuple[int, ...]) -> None:
    matches = [index for index, old in enumerate(clauses) if old == clause]
    if len(matches) != 1:
        raise AssertionError(
            f"expected exactly one removable clause {clause}, found {len(matches)}"
        )
    clauses.pop(matches[0])


def build(campaign: Path):
    source = (
        campaign
        / "math"
        / "working"
        / "order13_single_full_squeeze"
        / "search.py"
    )
    module = load_module(source)
    cnf, edge, family = module.build(
        sort_signatures=False,
        require_theta_gap=True,
        require_unique_full=False,
        require_closure=True,
        use_witness_bound=False,
        require_connected=False,
        force_all_independent_states=False,
    )

    def e(u: int, v: int) -> int:
        return edge[(u, v) if u < v else (v, u)]

    def direct_state(target: int, omitted_anchor: int) -> int:
        state = tuple(sorted((set(S) - {omitted_anchor}) | {target}))
        return family[state]

    # Remove the reusable builder's distinguished full target.
    for anchor in S:
        remove_once(cnf.clauses, (-e(anchor, 3),))
        remove_once(cnf.clauses, (direct_state(3, anchor),))

    # Exact no-full branch at the retained independent state S.
    for target in OUTSIDE:
        cnf.add(*(-direct_state(target, anchor) for anchor in S))

    def fix_signature(vertex: int, signature: frozenset[int]) -> None:
        for anchor in S:
            cnf.add(e(anchor, vertex) if anchor in signature else -e(anchor, vertex))

    def fix_list(vertex: int, response: frozenset[int]) -> None:
        for anchor in S:
            state = direct_state(vertex, anchor)
            cnf.add(state if anchor in response else -state)

    # Two occurring types, chosen up to the S_3 action on anchors.
    fix_signature(3, frozenset((0,)))
    fix_signature(4, frozenset((0,)))
    fix_list(3, frozenset((1, 2)))
    cnf.add(e(3, 4))

    fix_signature(5, frozenset((2,)))
    fix_signature(6, frozenset((2,)))
    fix_list(5, frozenset((0, 1)))
    cnf.add(e(5, 6))

    # The six unnamed residual vertices are freely interchangeable.  Sort
    # their anchor signatures numerically in complement-bit order.
    for left, right in zip(RESIDUAL[:-1], RESIDUAL[1:], strict=True):
        for p in range(8):
            for q in range(p):
                mismatch: list[int] = []
                for bit, anchor in enumerate(S):
                    lp = (p >> bit) & 1
                    rq = (q >> bit) & 1
                    mismatch.append(-e(left, anchor) if lp else e(left, anchor))
                    mismatch.append(-e(right, anchor) if rq else e(right, anchor))
                cnf.add(*mismatch)

    # At most three residual signatures are zero.
    cnf.add(*(e(anchor, 10) for anchor in S))
    return cnf


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--instance", type=Path, required=True)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--solver-log", type=Path, required=True)
    args = parser.parse_args()

    campaign = Path(__file__).resolve().parents[3]
    cnf = build(campaign)
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
    if status == "SAT":
        sys.exit(10)
    if status == "UNSAT":
        sys.exit(20)
    if status == "TIMEOUT":
        sys.exit(124)
    sys.exit(1)


if __name__ == "__main__":
    main()
