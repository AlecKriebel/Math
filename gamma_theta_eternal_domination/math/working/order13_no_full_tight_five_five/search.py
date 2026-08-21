#!/usr/bin/env python3
"""Exact discovery formula for the order-13 no-full tight 5+5 normal form.

This file intentionally imports only the general equality/eternal-family
allocator from ``order13_single_full_squeeze/search.py``.  It removes the
six distinguished-full-target units and then fixes, by relabeling, the
human-proved normal form from C-093.

Edge variables encode H = complement(G).  The fixed anchor state is
S=(h,i,j)=(0,1,2).  Outside labels are

    3,4       pure i;
    5,6       pure j;
    7         exceptional r, sigma(r)={h,i}, L(r)={j};
    8,...,12  neutral Q.

The two occurring exact two-list types omit i and j.  A same-sign physical
representative of each type lies in its corresponding two-vertex pure
class.  The forbidden third type omitting h is excluded at every neutral
vertex.  The formula includes literal one-guard family closure.  It
deliberately omits theta(G)>3: UNSAT therefore proves the stronger statement
that the tight normal form is incompatible with equality itself.

This is a discovery generator until independently reconstructed and
proof-checked.  SAT or timeout is not a mathematical result.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys


N = 13
S = (0, 1, 2)
H, I, J = S
PURE_I = (3, 4)
PURE_J = (5, 6)
R = 7
Q = tuple(range(8, N))


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def remove_once(clauses: list[tuple[int, ...]], clause: tuple[int, ...]) -> None:
    matches = [idx for idx, old in enumerate(clauses) if old == clause]
    if len(matches) != 1:
        raise AssertionError(
            f"expected exactly one removable clause {clause}, got {len(matches)}"
        )
    clauses.pop(matches[0])


def direct_states(family, target: int) -> tuple[int, int, int]:
    return tuple(
        family[tuple(sorted((set(S) - {guard}) | {target}))]
        for guard in S
    )


def add_signature(cnf, edge, vertex: int, signature: frozenset[int]) -> None:
    for anchor in S:
        variable = edge[(anchor, vertex)]
        cnf.add(variable if anchor in signature else -variable)


def add_exact_list(cnf, family, vertex: int, response: frozenset[int]) -> None:
    for anchor, state in zip(S, direct_states(family, vertex), strict=True):
        cnf.add(state if anchor in response else -state)


def build(campaign: Path):
    source = (
        campaign
        / "math"
        / "working"
        / "order13_single_full_squeeze"
        / "search.py"
    )
    module = load_module(source, "tight_five_five_base")
    cnf, edge, family = module.build(
        sort_signatures=False,
        require_theta_gap=False,
        require_unique_full=False,
        require_closure=True,
        use_witness_bound=False,
        require_connected=False,
        force_all_independent_states=False,
    )

    def e(u: int, v: int) -> int:
        return edge[(u, v) if u < v else (v, u)]

    # Remove the reusable builder's distinguished full target x=3.
    for guard in S:
        remove_once(cnf.clauses, (-e(guard, 3),))
        successor = tuple(sorted((set(S) - {guard}) | {3}))
        remove_once(cnf.clauses, (family[successor],))

    # Exact C-093 anchor signatures.
    for vertex in PURE_I:
        add_signature(cnf, edge, vertex, frozenset((I,)))
    for vertex in PURE_J:
        add_signature(cnf, edge, vertex, frozenset((J,)))
    add_signature(cnf, edge, R, frozenset((H, I)))
    for vertex in Q:
        add_signature(cnf, edge, vertex, frozenset())

    # Exceptional singleton and universal complement adjacency to Q.
    add_exact_list(cnf, family, R, frozenset((J,)))
    for vertex in Q:
        cnf.add(e(R, vertex))

    # The physical representative and its doubled pure mate are the only
    # two vertices of their signatures.  Relabel within each pair so vertex
    # 3 (respectively 5) is the exact representative.
    add_exact_list(cnf, family, PURE_I[0], frozenset((H, J)))
    add_exact_list(cnf, family, PURE_J[0], frozenset((H, I)))
    cnf.add(e(*PURE_I))
    cnf.add(e(*PURE_J))

    # Closure at S supplies a nonempty direct response at every target.
    # Exclude a full list everywhere and exclude the absent type omitting h,
    # namely {i,j}, at every neutral vertex.  Nonneutral signatures already
    # exclude at least one anchor response by domination of the direct state.
    for vertex in range(3, N):
        f_h, f_i, f_j = direct_states(family, vertex)
        cnf.add(-f_h, -f_i, -f_j)
    for vertex in Q:
        _, f_i, f_j = direct_states(family, vertex)
        cnf.add(-f_i, -f_j)

    return cnf


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--instance", type=Path, required=True)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--solver-log", type=Path, required=True)
    parser.add_argument("--model", type=Path)
    args = parser.parse_args()

    campaign = Path(__file__).resolve().parents[3]
    cnf = build(campaign)
    args.instance.parent.mkdir(parents=True, exist_ok=True)
    args.instance.write_text(cnf.dimacs(), encoding="ascii")

    command = [str(args.solver), "--quiet", "--binary=false"]
    if args.model is not None:
        command.extend(("-w", str(args.model)))
    command.append(str(args.instance))
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
