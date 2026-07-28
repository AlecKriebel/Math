#!/usr/bin/env python3
"""SAT discovery search for a two-dynamic-type equality control.

This is search code, not the independent verifier.  Vertices 0,1,2 form
the reference independent state.  Vertices 3 and 4 are forced dynamic
ports omitting 0 and 1 respectively; vertex 5 is a physical port omitting
2.  Every outside response list has exact size two, and every type-2 port
is forced physical.  The formula encodes gamma >= 3 and literal one-guard
closure of a selected triple family.
"""

from __future__ import annotations

import argparse
from itertools import combinations, product
from pathlib import Path
import subprocess


S = (0, 1, 2)


def pair(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


class CNF:
    def __init__(self) -> None:
        self.names = [""]
        self.clauses: list[tuple[int, ...]] = []

    def var(self, name: str) -> int:
        self.names.append(name)
        return len(self.names) - 1

    def add(self, *literals: int) -> None:
        self.clauses.append(tuple(literals))

    def dimacs(self) -> str:
        body = "".join(
            " ".join(map(str, clause)) + " 0\n"
            for clause in self.clauses
        )
        return f"p cnf {len(self.names)-1} {len(self.clauses)}\n{body}"


def build(
    order: int,
    dynamic_types: frozenset[int] = frozenset((0, 1)),
    gamma_mode: str = "three",
) -> tuple[CNF, dict[str, object]]:
    if order < 6:
        raise ValueError("order must be at least six")
    vertices = tuple(range(order))
    triples = tuple(combinations(vertices, 3))
    cnf = CNF()
    edge_h = {
        uv: cnf.var(f"H({uv[0]},{uv[1]})")
        for uv in combinations(vertices, 2)
    }
    family = {
        state: cnf.var("F(" + ",".join(map(str, state)) + ")")
        for state in triples
    }
    common = {
        (u, v, w): cnf.var(f"W({u},{v};{w})")
        for u, v in combinations(vertices, 2)
        for w in vertices
        if w not in (u, v)
    }

    def h(u: int, v: int) -> int:
        return edge_h[pair(u, v)]

    if gamma_mode == "three":
        # gamma(G) >= 3: every pair has a common H-neighbor.
        for u, v in combinations(vertices, 2):
            candidates = tuple(w for w in vertices if w not in (u, v))
            cnf.add(*(common[(u, v, w)] for w in candidates))
            for w in candidates:
                marker = common[(u, v, w)]
                cnf.add(-marker, h(u, w))
                cnf.add(-marker, h(v, w))
    elif gamma_mode == "two":
        # No dominating singleton.
        for u in vertices:
            cnf.add(*(h(u, w) for w in vertices if w != u))
        # The fixed pair {0,3} dominates G.
        for w in vertices:
            if w not in (0, 3):
                cnf.add(-h(0, w), -h(3, w))
    else:
        raise ValueError(gamma_mode)

    # Literal one-guard closure.  As in the accepted boundary probes,
    # closure against every unoccupied attack also forces domination.
    for state in triples:
        selected = family[state]
        for attacked in vertices:
            if attacked in state:
                continue
            response_pairs = []
            for guard in state:
                successor = tuple(
                    sorted((set(state) - {guard}) | {attacked})
                )
                response_pairs.append((-h(guard, attacked), family[successor]))
            for chosen in product(*response_pairs):
                cnf.add(-selected, *chosen)

    for u, v in combinations(S, 2):
        cnf.add(h(u, v))
    cnf.add(family[S])

    anchor = set(S)

    def direct(vertex: int, omitted: int) -> int:
        state = tuple(sorted((anchor - {omitted}) | {vertex}))
        return family[state]

    # Every outside list has exactly two responses.
    for vertex in range(3, order):
        responses = tuple(direct(vertex, omitted) for omitted in S)
        for first, second in combinations(responses, 2):
            cnf.add(first, second)
        cnf.add(*(-literal for literal in responses))

    # Exact types 0,1,2 for vertices 3,4,5.
    for vertex, omitted_type in ((3, 0), (4, 1), (5, 2)):
        for omitted in S:
            literal = direct(vertex, omitted)
            cnf.add(-literal if omitted == omitted_type else literal)

    # Each displayed type is dynamic or physical as requested.
    for omitted_type, vertex in enumerate((3, 4, 5)):
        cnf.add(
            -h(omitted_type, vertex)
            if omitted_type in dynamic_types
            else h(omitted_type, vertex)
        )

    # Every type outside the requested dynamic set is entirely physical.
    for omitted_type in set(S) - set(dynamic_types):
        for vertex in range(3, order):
            cnf.add(
                direct(vertex, omitted_type),
                h(omitted_type, vertex),
            )

    return cnf, {
        "order": order,
        "edge_h": edge_h,
        "family": family,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--instance", type=Path, required=True)
    parser.add_argument("--model", type=Path)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument(
        "--one-dynamic-type",
        action="store_true",
        help="force only type 0 dynamic; make types 1 and 2 entirely physical",
    )
    parser.add_argument(
        "--gamma-two-control",
        action="store_true",
        help="seek a gamma=2 sharpness control instead of imposing gamma>=3",
    )
    args = parser.parse_args()

    dynamic_types = (
        frozenset((0,))
        if args.one_dynamic_type
        else frozenset((0, 1))
    )
    cnf, _ = build(
        args.order,
        dynamic_types,
        "two" if args.gamma_two_control else "three",
    )
    args.instance.write_text(cnf.dimacs(), encoding="ascii")
    command = [str(args.solver), "--quiet", "--binary=false"]
    if args.model is not None:
        command.extend(("-w", str(args.model)))
    command.append(str(args.instance))
    try:
        run = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=args.timeout,
            check=False,
        )
        status = (
            "SAT"
            if run.returncode == 10
            else "UNSAT"
            if run.returncode == 20
            else f"EXIT_{run.returncode}"
        )
        output = run.stdout
    except subprocess.TimeoutExpired as error:
        status = "TIMEOUT"
        output = (error.stdout or "") + (error.stderr or "")
    args.log.write_text(output, encoding="utf-8")
    print(
        f"order={args.order} variables={len(cnf.names)-1} "
        f"clauses={len(cnf.clauses)} status={status}"
    )
    raise SystemExit(
        10 if status == "SAT"
        else 20 if status == "UNSAT"
        else 124 if status == "TIMEOUT"
        else 1
    )


if __name__ == "__main__":
    main()
