#!/usr/bin/env python3
"""Exact discovery probe for a one-clause chain from one singleton marker.

Anchors are d,u,e = 0,1,2.  The singleton s has list {d}.  An even
complement path P in W_u joins s to a type-u port x with list {d,e}; an
even complement path Q in W_e joins s to a type-e port y with list {d,u}.
The cross edge xy then falsifies the shared-d clause under both units.

The edge variables encode H and family variables encode an arbitrary
one-guard eternal family directly.  No gamma condition is imposed unless
requested.  This is proof-discovery code, not a certificate generator.
"""

from __future__ import annotations

import argparse
from itertools import combinations, product
from pathlib import Path
import subprocess


S = (0, 1, 2)
D, U, E = S
SINGLETON = 3
X = 4
Y = 5


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
        clause = tuple(int(value) for value in literals)
        if not clause or 0 in clause:
            raise ValueError("malformed clause")
        if any(-value in clause for value in clause):
            raise ValueError("tautology")
        self.clauses.append(clause)

    def dimacs(self) -> str:
        body = "".join(
            " ".join(map(str, clause)) + " 0\n" for clause in self.clauses
        )
        return f"p cnf {len(self.names)-1} {len(self.clauses)}\n{body}"


def build(
    p_length: int,
    q_length: int,
    *,
    spare_vertices: int = 0,
    enforce_gamma: bool = False,
) -> tuple[CNF, int]:
    if p_length < 1 or q_length < 1:
        raise ValueError("path lengths must be positive")
    next_vertex = 6
    p_interior = tuple(range(next_vertex, next_vertex + p_length - 1))
    next_vertex += p_length - 1
    q_interior = tuple(range(next_vertex, next_vertex + q_length - 1))
    next_vertex += q_length - 1
    order = next_vertex + spare_vertices
    vertices = tuple(range(order))
    triples = tuple(combinations(vertices, 3))
    cnf = CNF()
    edge_h = {
        uv: cnf.var(f"edgeH({uv[0]},{uv[1]})")
        for uv in combinations(vertices, 2)
    }
    family = {
        state: cnf.var("family(" + ",".join(map(str, state)) + ")")
        for state in triples
    }
    witness = {
        (u, v, w): cnf.var(f"commonH({u},{v};{w})")
        for u, v in combinations(vertices, 2)
        for w in vertices
        if w not in (u, v)
    }

    def e(u: int, v: int) -> int:
        return edge_h[pair(u, v)]

    if enforce_gamma:
        for u, v in combinations(vertices, 2):
            choices = tuple(w for w in vertices if w not in (u, v))
            cnf.add(*(witness[(u, v, w)] for w in choices))
            for w in choices:
                marker = witness[(u, v, w)]
                cnf.add(-marker, e(u, w))
                cnf.add(-marker, e(v, w))

    for state in triples:
        selected = family[state]
        for attacked in vertices:
            if attacked in state:
                continue
            response_terms = []
            for guard in state:
                successor = tuple(
                    sorted((set(state) - {guard}) | {attacked})
                )
                response_terms.append(
                    (-e(guard, attacked), family[successor])
                )
            for chosen in product(*response_terms):
                cnf.add(-selected, *chosen)

    for u, v in combinations(S, 2):
        cnf.add(e(u, v))
    cnf.add(family[S])

    def direct_state(vertex: int, omitted: int) -> tuple[int, int, int]:
        return tuple(sorted((set(S) - {omitted}) | {vertex}))

    def exact_list(vertex: int, response: frozenset[int]) -> None:
        for omitted in S:
            marker = family[direct_state(vertex, omitted)]
            cnf.add(marker if omitted in response else -marker)

    exact_list(SINGLETON, frozenset((D,)))
    exact_list(X, frozenset((D, E)))
    exact_list(Y, frozenset((D, U)))
    for vertex in p_interior:
        cnf.add(-family[direct_state(vertex, U)])
    for vertex in q_interior:
        cnf.add(-family[direct_state(vertex, E)])

    p_path = (SINGLETON, *p_interior, X)
    q_path = (SINGLETON, *q_interior, Y)
    for left, right in zip(p_path[:-1], p_path[1:], strict=True):
        cnf.add(e(left, right))
    for left, right in zip(q_path[:-1], q_path[1:], strict=True):
        cnf.add(e(left, right))
    cnf.add(e(X, Y))
    return cnf, order


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-length", type=int, required=True)
    parser.add_argument("--q-length", type=int, required=True)
    parser.add_argument("--spare-vertices", type=int, default=0)
    parser.add_argument("--gamma", action="store_true")
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--instance", type=Path, required=True)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()
    cnf, order = build(
        args.p_length,
        args.q_length,
        spare_vertices=args.spare_vertices,
        enforce_gamma=args.gamma,
    )
    args.instance.write_text(cnf.dimacs(), encoding="ascii")
    command = [
        str(args.solver),
        "--quiet",
        "--binary=false",
        str(args.instance),
    ]
    if args.proof is not None:
        command.append(str(args.proof))
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
            "SAT" if run.returncode == 10
            else "UNSAT" if run.returncode == 20
            else f"EXIT_{run.returncode}"
        )
    except subprocess.TimeoutExpired:
        status = "TIMEOUT"
    print(
        f"order={order} variables={len(cnf.names)-1}"
        f" clauses={len(cnf.clauses)} status={status}"
    )
    raise SystemExit(
        10 if status == "SAT"
        else 20 if status == "UNSAT"
        else 124 if status == "TIMEOUT"
        else 1
    )


if __name__ == "__main__":
    main()
