#!/usr/bin/env python3
"""Bounded case splitter for the order-13, k=3, no-full-list branch.

This is a discovery generator.  It starts from the relaxed equality/closure
formula used by ``order13_no_full_probe`` but replaces the old pivoted S_9
sorter by a full S_10 sort of the three-bit H-signatures to the fixed
independent state S={0,1,2}.

The theorem-grade branch retained in ``NOTE.md`` is ``residual``:
every order-13 no-full counterexample has at least five nonneutral outside
vertices.  The two ``a4-*`` modes are redundant, deliberately nonexhaustive
discovery controls below that proved floor:

* ``a4-singleton-q``: exactly four nonneutral outside vertices, and every
  neutral response list is a singleton;
* ``a4-one-q-type``: exactly four nonneutral outside vertices, and the
  neutral vertices use one (canonically chosen) two-list type;
* ``residual``: at least five nonneutral outside vertices (the complete
  theorem-supported remaining branch).

The two ``a4-*`` modes do not cover every formal four-nonneutral response
pattern and must not be combined into a coverage claim.  Any UNSAT result
remains discovery evidence until independently generated and proof-checked.
A timeout is a nonclaim.
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
from pathlib import Path
import subprocess
import sys


N = 13
S = (0, 1, 2)
OUTSIDE = tuple(range(3, N))


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def remove_once(clauses: list[tuple[int, ...]], clause: tuple[int, ...]) -> None:
    matches = [i for i, existing in enumerate(clauses) if existing == clause]
    if len(matches) != 1:
        raise AssertionError(
            f"expected exactly one removable clause {clause}, found {len(matches)}"
        )
    clauses.pop(matches[0])


def build_relaxed_base(campaign: Path):
    builder_path = (
        campaign
        / "math"
        / "working"
        / "order13_single_full_squeeze"
        / "search.py"
    )
    module = load_module(builder_path, "order13_full_target_base_for_split")
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

    # Remove the six distinguished-full-target units inherited from the
    # reusable builder.  Nothing else in this build distinguishes vertex 3.
    for guard in S:
        remove_once(cnf.clauses, (-e(guard, 3),))
        successor = tuple(sorted((set(S) - {guard}) | {3}))
        remove_once(cnf.clauses, (family[successor],))

    # Literal no-full-list condition at every outside target.  Closure at S
    # supplies nonemptiness.
    for target in OUTSIDE:
        direct = tuple(
            family[tuple(sorted((set(S) - {guard}) | {target}))]
            for guard in S
        )
        cnf.add(*(-state for state in direct))

    # Full S_10 symmetry breaker: vertices outside S are wholly
    # interchangeable.  Sort their three-bit H-adjacency signatures to S.
    for left, right in zip(OUTSIDE[:-1], OUTSIDE[1:], strict=True):
        for p in range(8):
            for q in range(p):
                mismatch: list[int] = []
                for bit, anchor in enumerate(S):
                    lp = (p >> bit) & 1
                    rq = (q >> bit) & 1
                    mismatch.append(-e(left, anchor) if lp else e(left, anchor))
                    mismatch.append(-e(right, anchor) if rq else e(right, anchor))
                cnf.add(*mismatch)

    return cnf, edge, family


def add_signature_units(cnf, edge, vertex: int, signature: int) -> None:
    for bit, anchor in enumerate(S):
        variable = edge[(anchor, vertex)]
        cnf.add(variable if (signature >> bit) & 1 else -variable)


def direct_states(family, target: int) -> tuple[int, int, int]:
    return tuple(
        family[tuple(sorted((set(S) - {guard}) | {target}))]
        for guard in S
    )


def add_exact_list(cnf, family, target: int, colors: frozenset[int]) -> None:
    for color, state in zip(S, direct_states(family, target), strict=True):
        cnf.add(state if color in colors else -state)


def add_residual_case(cnf, edge) -> None:
    """At least five outside vertices have a nonempty H-signature to S."""

    # With sorted signatures, |Q_S|<=5 is exactly: vertex 8 is nonneutral.
    cnf.add(edge[(0, 8)], edge[(1, 8)], edge[(2, 8)])


def add_a4_case(cnf, edge, family, *, neutral_two_lists: bool) -> None:
    """Canonical |A|=4 normal form.

    The two list types omit anchors 0 and 2.  Each type has exactly two
    pure-signature vertices, and the pair must be an H-edge.  The six
    neutral vertices either all have singleton lists, or use (after the
    residual 0<->2 anchor symmetry) only type {0,1}, with at least one such
    neutral two-list.
    """

    signatures = {
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0b001,
        10: 0b001,
        11: 0b100,
        12: 0b100,
    }
    for vertex, signature in signatures.items():
        add_signature_units(cnf, edge, vertex, signature)

    # Name one physical representative of each type.  The only possible
    # common-H-neighbor for its pair with the omitted anchor is the other
    # pure vertex, forcing the two displayed H-edges.
    add_exact_list(cnf, family, 9, frozenset((1, 2)))
    add_exact_list(cnf, family, 11, frozenset((0, 1)))
    cnf.add(edge[(9, 10)])
    cnf.add(edge[(11, 12)])

    neutral_ab: list[int] = []
    for vertex in range(3, 9):
        f0, f1, f2 = direct_states(family, vertex)
        # Type {0,2} is absent.  In the one-neutral-type branch, the
        # residual anchor swap chooses {0,1} rather than {1,2}.
        cnf.add(-f0, -f2)
        cnf.add(-f1, -f2)
        if neutral_two_lists:
            selector = cnf.var(f"neutral_ab_{vertex}")
            neutral_ab.append(selector)
            cnf.add(-selector, f0)
            cnf.add(-selector, f1)
            cnf.add(-f0, -f1, selector)
        else:
            cnf.add(-f0, -f1)
    if neutral_two_lists:
        cnf.add(*neutral_ab)


def build_case(campaign: Path, case: str):
    cnf, edge, family = build_relaxed_base(campaign)
    if case == "a4-singleton-q":
        add_a4_case(cnf, edge, family, neutral_two_lists=False)
    elif case == "a4-one-q-type":
        add_a4_case(cnf, edge, family, neutral_two_lists=True)
    elif case == "residual":
        add_residual_case(cnf, edge)
    else:
        raise ValueError(f"unknown case {case}")
    return cnf


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--case",
        choices=("a4-singleton-q", "a4-one-q-type", "residual"),
        required=True,
    )
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--instance", type=Path, required=True)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--solver-log", type=Path, required=True)
    args = parser.parse_args()

    campaign = Path(__file__).resolve().parents[3]
    cnf = build_case(campaign, args.case)
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
        f"case={args.case} variables={len(cnf.names)-1} "
        f"clauses={len(cnf.clauses)} status={status}"
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
