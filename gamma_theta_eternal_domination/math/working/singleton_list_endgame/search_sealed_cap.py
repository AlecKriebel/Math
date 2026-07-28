#!/usr/bin/env python3
"""Discovery SAT search for a sealed exact-two response cap.

This is deliberately a small, self-contained formula builder.  It asks
whether an eternal family of triples can coexist with:

* an independent retained reference state S={0,1,2};
* gamma(G) >= 3;
* nonempty, non-full response lists at S; and
* a vertex z=3 with L(z)={0,1} that is G-adjacent to every other
  outside vertex whose response list contains 0.

The last condition says that z is a sealed 0-positive exact-two vertex.
The program is a discovery tool, not a proof certificate.
"""

from __future__ import annotations

import argparse
from itertools import combinations, product
from pathlib import Path
import subprocess


S = (0, 1, 2)
Z = 3


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
        return (
            f"p cnf {len(self.names) - 1} {len(self.clauses)}\n"
            + body
        )


def build(order: int) -> tuple[CNF, dict[str, object]]:
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

    anchor = set(S)

    def direct(vertex: int, responder: int) -> int:
        state = tuple(sorted((anchor - {responder}) | {vertex}))
        return family[state]

    # gamma(G) >= 3: every pair has a common complement neighbor.
    for u, v in combinations(vertices, 2):
        candidates = tuple(w for w in vertices if w not in (u, v))
        cnf.add(*(common[(u, v, w)] for w in candidates))
        for w in candidates:
            marker = common[(u, v, w)]
            cnf.add(-marker, h(u, w))
            cnf.add(-marker, h(v, w))

    # Literal one-guard closure.  Closure against every unoccupied attack
    # also forces every selected state to dominate.
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
                response_pairs.append(
                    (-h(guard, attacked), family[successor])
                )
            for chosen in product(*response_pairs):
                cnf.add(-selected, *chosen)

    # S is independent and retained.
    for u, v in combinations(S, 2):
        cnf.add(h(u, v))
    cnf.add(family[S])

    # Every outside response list is nonempty and proper.
    for vertex in range(3, order):
        responses = tuple(direct(vertex, responder) for responder in S)
        cnf.add(*responses)
        cnf.add(*(-literal for literal in responses))

    # z has exact list {0,1}.
    cnf.add(direct(Z, 0))
    cnf.add(direct(Z, 1))
    cnf.add(-direct(Z, 2))

    # z is sealed against every other outside 0-positive vertex:
    # direct(v,0) => zv in E(G), equivalently not H(z,v).
    for vertex in range(3, order):
        if vertex == Z:
            continue
        cnf.add(-direct(vertex, 0), -h(Z, vertex))

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
    args = parser.parse_args()

    cnf, _ = build(args.order)
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
        f"order={args.order} variables={len(cnf.names) - 1} "
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
