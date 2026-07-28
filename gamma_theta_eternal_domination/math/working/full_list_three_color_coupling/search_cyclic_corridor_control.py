#!/usr/bin/env python3
"""Bounded falsifier for a proposed cyclic-corridor contradiction.

This is discovery code, not a certificate generator.  It asks for a graph
with gamma=alpha=gamma_infinity=3 and an explicit eternal triple-family
containing the complete named rank-zero cyclic corridor/witness ladder.
No clique-cover condition and no assertion that the three restricted
kernels are empty is imposed.
"""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
import tempfile
from pathlib import Path


ROOT = (0, 1, 2)
TARGET = 3
MOVERS = (4, 5, 6)
TERMINALS = (7, 8, 9)


class CNF:
    def __init__(self) -> None:
        self.next_variable = 1
        self.clauses: list[tuple[int, ...]] = []

    def variable(self) -> int:
        result = self.next_variable
        self.next_variable += 1
        return result

    def add(self, *literals: int) -> None:
        self.clauses.append(tuple(literals))


def pairs(order: int) -> tuple[tuple[int, int], ...]:
    return tuple(itertools.combinations(range(order), 2))


def triples(order: int) -> tuple[tuple[int, int, int], ...]:
    return tuple(itertools.combinations(range(order), 3))


def build(
    order: int,
    *,
    enforce_gamma_three: bool = True,
    gamma_pairs: frozenset[tuple[int, int]] | None = None,
) -> tuple[CNF, dict[tuple[int, int], int], dict[tuple[int, ...], int]]:
    if order < 10:
        raise ValueError("the named core uses vertices 0 through 9")
    cnf = CNF()
    edge = {pair: cnf.variable() for pair in pairs(order)}
    family = {triple: cnf.variable() for triple in triples(order)}

    def e(first: int, second: int) -> int:
        if first == second:
            raise ValueError("loop requested")
        return edge[tuple(sorted((first, second)))]

    def f(state: set[int] | tuple[int, ...]) -> int:
        return family[tuple(sorted(state))]

    # Root and full target.
    for first, second in itertools.combinations(ROOT, 2):
        cnf.add(-e(first, second))
    for anchor in ROOT:
        cnf.add(e(TARGET, anchor))
    cnf.add(f(ROOT))
    for color in ROOT:
        cnf.add(f((set(ROOT) - {color}) | {TARGET}))

    # Three cyclic rank-zero corridors.  Row u has secondary v=u+1,
    # remaining anchor t=u+2, mover q_u, terminal r_u, and private witness
    # w=q_v.  The exact nonedges make the secondary alternate miss w.
    for u in ROOT:
        v = (u + 1) % 3
        t = (u + 2) % 3
        q = MOVERS[u]
        w = MOVERS[v]
        r = TERMINALS[u]

        for first, second in (
            (TARGET, q),
            (u, q),
            (t, q),
            (u, r),
            (v, r),
            (q, r),
            (v, w),
        ):
            cnf.add(e(first, second))
        for first, second in (
            (TARGET, r),
            (v, q),
            (t, r),
            (w, t),
            (w, q),
            (w, r),
        ):
            cnf.add(-e(first, second))

        predecessor = (set(ROOT) - {u}) | {q}
        terminal = (set(ROOT) - {u}) | {r}
        secondary_root = (set(ROOT) - {v}) | {r}
        witness_q = {w, t, q}
        witness_r = {w, t, r}
        transferred_root = (set(ROOT) - {v}) | {w}
        for state in (
            predecessor,
            terminal,
            secondary_root,
            witness_q,
            witness_r,
            transferred_root,
        ):
            cnf.add(f(state))

    # alpha <= 3.
    for four in itertools.combinations(range(order), 4):
        cnf.add(*(e(first, second) for first, second in itertools.combinations(four, 2)))

    # gamma >= 3: every pair has a common closed-neighborhood miss.
    if enforce_gamma_three:
        selected_pairs = (
            tuple(sorted(gamma_pairs))
            if gamma_pairs is not None
            else tuple(itertools.combinations(range(order), 2))
        )
        for first, second in selected_pairs:
            witnesses = []
            for witness in range(order):
                if witness in (first, second):
                    continue
                z = cnf.variable()
                # z iff both pair-to-witness edges are absent.
                cnf.add(-z, -e(first, witness))
                cnf.add(-z, -e(second, witness))
                cnf.add(e(first, witness), e(second, witness), z)
                witnesses.append(z)
            cnf.add(*witnesses)

    # Every selected family state dominates and answers every unoccupied
    # attack by exactly one guard moving along one edge to another family
    # state.  Family membership is optional for all unnamed triples.
    for state in triples(order):
        state_set = set(state)
        fv = f(state)
        for attacked in range(order):
            if attacked in state_set:
                continue
            cnf.add(-fv, *(e(guard, attacked) for guard in state))
            moves = []
            for guard in state:
                successor = (state_set - {guard}) | {attacked}
                move = cnf.variable()
                cnf.add(-move, e(guard, attacked))
                cnf.add(-move, f(successor))
                cnf.add(-e(guard, attacked), -f(successor), move)
                moves.append(move)
            cnf.add(-fv, *moves)

    return cnf, edge, family


def solve(
    order: int,
    solver: Path,
    *,
    enforce_gamma_three: bool = True,
    gamma_pairs: frozenset[tuple[int, int]] | None = None,
) -> dict[str, object]:
    cnf, edge, family = build(
        order,
        enforce_gamma_three=enforce_gamma_three,
        gamma_pairs=gamma_pairs,
    )
    with tempfile.TemporaryDirectory(prefix="three-color-coupling-") as temp:
        directory = Path(temp)
        formula = directory / "instance.cnf"
        model_path = directory / "model.txt"
        with formula.open("w", encoding="ascii") as stream:
            stream.write(f"p cnf {cnf.next_variable - 1} {len(cnf.clauses)}\n")
            for clause in cnf.clauses:
                stream.write(" ".join(map(str, clause)) + " 0\n")
        completed = subprocess.run(
            [str(solver), str(formula)],
            check=False,
            capture_output=True,
            text=True,
        )
        model_path.write_text(completed.stdout, encoding="utf-8")
        status = "UNKNOWN"
        if completed.returncode == 10:
            status = "SAT"
        elif completed.returncode == 20:
            status = "UNSAT"
        positive: set[int] = set()
        if status == "SAT":
            for line in completed.stdout.splitlines():
                if line.startswith("v "):
                    positive.update(
                        literal
                        for literal in map(int, line[2:].split())
                        if literal > 0
                    )
        selected_edges = [
            list(pair) for pair, variable in sorted(edge.items())
            if variable in positive
        ]
        selected_family = [
            list(state) for state, variable in sorted(family.items())
            if variable in positive
        ]
    return {
        "order": order,
        "status": status,
        "solver_returncode": completed.returncode,
        "variables": cnf.next_variable - 1,
        "clauses": len(cnf.clauses),
        "edges": selected_edges,
        "family": selected_family,
        "scope": (
            "discovery falsifier only; no proof log, no restricted-kernel "
            "emptiness, and no clique-cover constraint"
        ),
        "enforce_gamma_three": enforce_gamma_three,
        "gamma_pairs": (
            [list(pair) for pair in sorted(gamma_pairs)]
            if gamma_pairs is not None
            else "all"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--allow-dominating-pairs", action="store_true")
    parser.add_argument(
        "--gamma-pair",
        nargs=2,
        action="append",
        type=int,
        metavar=("FIRST", "SECOND"),
    )
    args = parser.parse_args()
    result = solve(
        args.order,
        args.solver.resolve(),
        enforce_gamma_three=not args.allow_dominating_pairs,
        gamma_pairs=(
            frozenset(tuple(sorted(pair)) for pair in args.gamma_pair)
            if args.gamma_pair
            else None
        ),
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
