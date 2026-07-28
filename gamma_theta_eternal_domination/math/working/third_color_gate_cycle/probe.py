#!/usr/bin/env python3
"""Exact SAT probe for the shortest odd virtual-rainbow gate cycle.

The edge variables encode H = complement(G).  The fixed labels are

    S = (a,b,c) = (0,1,2)
    x = 3
    (q0,t0,y0,z1) = (4,5,6,7)
    (q1,t1,y1,z0) = (8,9,10,11).

The two original clauses are x-q0 and x-q1.  The even frozen-component
paths q0-t0-y0 and q1-t1-y1 identify the two endpoint events with y0 and
y1.  The failed incidences x-y0 and x-y1 have tight caps z1 and z0.
Finally y0-z0 is an odd connector between two type-0 ports.  Thus the two
gates identify their chirality through x, while the last connector reverses
it.

The formula imposes only:

* an independent retained state S;
* an eternal family of triples in the standard one-guard model;
* gamma(G) >= 3, via a common H-neighbor for every pair;
* the displayed exact response lists and literal H/G incidences.

It does not impose connectedness or theta(G) > 3.
"""

from __future__ import annotations

import argparse
from itertools import combinations, product
from pathlib import Path
import subprocess
import sys


S = (0, 1, 2)
X, Q0, T0, Y0, Z1, Q1, T1, Y1, Z0 = range(3, 12)


def pair(u: int, v: int) -> tuple[int, int]:
    if u == v:
        raise ValueError("loop")
    return (u, v) if u < v else (v, u)


class CNF:
    def __init__(self) -> None:
        self.names = [""]
        self.clauses: list[tuple[int, ...]] = []

    def var(self, name: str) -> int:
        self.names.append(name)
        return len(self.names) - 1

    def add(self, *literals: int) -> None:
        clause = tuple(int(literal) for literal in literals)
        if not clause or 0 in clause:
            raise ValueError("malformed clause")
        if any(-literal in clause for literal in clause):
            raise ValueError("tautology")
        self.clauses.append(clause)

    def dimacs(self) -> str:
        body = "".join(
            " ".join(map(str, clause)) + " 0\n"
            for clause in self.clauses
        )
        return f"p cnf {len(self.names) - 1} {len(self.clauses)}\n{body}"


def build(
    order: int,
    *,
    enforce_gamma: bool = True,
    connector_length: int = 1,
    include_second_gate: bool = True,
) -> tuple[
    CNF,
    dict[tuple[int, int], int],
    dict[tuple[int, int, int], int],
]:
    if connector_length < 0:
        raise ValueError("connector length must be nonnegative")
    connector_interior = tuple(
        range(12, 12 + max(0, connector_length - 1))
    )
    required_order = 12 + max(0, connector_length - 1)
    if order < required_order:
        raise ValueError("the named pattern needs at least twelve vertices")
    vertices = tuple(range(order))
    triples = tuple(combinations(vertices, 3))
    cnf = CNF()
    edge = {
        uv: cnf.var(f"edgeH({uv[0]},{uv[1]})")
        for uv in combinations(vertices, 2)
    }
    family = {
        state: cnf.var("family" + "_".join(map(str, state)))
        for state in triples
    }
    witness = {
        (u, v, w): cnf.var(f"commonH({u},{v};{w})")
        for u, v in combinations(vertices, 2)
        for w in vertices
        if w not in (u, v)
    }

    def e(u: int, v: int) -> int:
        return edge[pair(u, v)]

    # gamma(G) >= 3: every pair has a common open H-neighbor.
    if enforce_gamma:
        for u, v in combinations(vertices, 2):
            choices = tuple(w for w in vertices if w not in (u, v))
            cnf.add(*(witness[(u, v, w)] for w in choices))
            for w in choices:
                marker = witness[(u, v, w)]
                cnf.add(-marker, e(u, w))
                cnf.add(-marker, e(v, w))

    # Exact one-guard closure.  A possible response by guard g is the
    # conjunction (-edgeH(g,r) AND family(successor)).  Distribute the
    # disjunction of the three response conjunctions into eight clauses.
    # The all-move-edge row simultaneously enforces domination.
    for state in triples:
        selected = family[state]
        for attacked in vertices:
            if attacked in state:
                continue
            response_pairs: list[tuple[int, int]] = []
            for guard in state:
                successor = tuple(
                    sorted((set(state) - {guard}) | {attacked})
                )
                response_pairs.append(
                    (-e(guard, attacked), family[successor])
                )
            for chosen in product(*response_pairs):
                cnf.add(-selected, *chosen)

    # Independent retained reference state.
    for u, v in combinations(S, 2):
        cnf.add(e(u, v))
    cnf.add(family[S])

    def direct_state(vertex: int, omitted: int) -> tuple[int, int, int]:
        return tuple(sorted((set(S) - {omitted}) | {vertex}))

    def exact_list(vertex: int, response: frozenset[int]) -> None:
        for omitted in S:
            literal = family[direct_state(vertex, omitted)]
            cnf.add(literal if omitted in response else -literal)

    exact_list(X, frozenset((0, 1)))
    for vertex in (Q0, Y0, Z0):
        exact_list(vertex, frozenset((1, 2)))
    exact_list(Z1, frozenset((0, 2)))
    if include_second_gate:
        exact_list(Q1, frozenset((0, 2)))
        exact_list(Y1, frozenset((0, 2)))

    # The two connector interiors merely omit the corresponding anchor.
    cnf.add(-family[direct_state(T0, 0)])
    if include_second_gate:
        cnf.add(-family[direct_state(T1, 1)])
    for vertex in connector_interior:
        # The holonomy connector lies in W_a.
        cnf.add(-family[direct_state(vertex, 0)])

    h_edges = [
        # physical omitted-anchor incidences
        (2, X), (0, Y0), (1, Z1), (1, Y1), (0, Z0),
        # original clauses
        (X, Q0),
        # even same-variable physicalization paths
        (Q0, T0), (T0, Y0),
        # the two tight cap arms
        (X, Z1), (Y0, Z1),
    ]
    if include_second_gate:
        h_edges.extend(
            (
                (X, Q1),
                (Q1, T1), (T1, Y1),
                (X, Z0), (Y1, Z0),
            )
        )
        if connector_length:
            connector = (Y0, *connector_interior, Z0)
            h_edges.extend(zip(connector[:-1], connector[1:], strict=True))
    g_edges = [
        # positive list incidences are implied semantically, but fixing them
        # keeps the pattern readable and catches sign mistakes.
        (0, X), (1, X),
        (1, Y0), (2, Y0),
        (0, Z1), (2, Z1),
        # failed joint incidences
        (X, Y0),
    ]
    if include_second_gate:
        g_edges.extend(
            (
                (0, Y1), (2, Y1),
                (1, Z0), (2, Z0),
                (X, Y1),
            )
        )
    for u, v in h_edges:
        cnf.add(e(u, v))
    for u, v in g_edges:
        cnf.add(-e(u, v))
    return cnf, edge, family


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, default=12)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--instance", type=Path, required=True)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--model", type=Path)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--no-gamma", action="store_true")
    parser.add_argument("--no-odd-connector", action="store_true")
    parser.add_argument("--connector-length", type=int)
    parser.add_argument("--one-gate", action="store_true")
    args = parser.parse_args()

    connector_length = (
        args.connector_length
        if args.connector_length is not None
        else 0 if args.no_odd_connector else 1
    )
    cnf, _, _ = build(
        args.order,
        enforce_gamma=not args.no_gamma,
        connector_length=connector_length,
        include_second_gate=not args.one_gate,
    )
    args.instance.write_text(cnf.dimacs(), encoding="ascii")
    command = [str(args.solver), "--quiet", "--binary=false"]
    if args.model is not None:
        command.extend(("-w", str(args.model)))
    command.append(str(args.instance))
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
        output = run.stdout
        status = (
            "SAT" if run.returncode == 10
            else "UNSAT" if run.returncode == 20
            else f"EXIT_{run.returncode}"
        )
    except subprocess.TimeoutExpired as error:
        output = (error.stdout or "") + (error.stderr or "")
        status = "TIMEOUT"
    args.log.write_text(output, encoding="utf-8")
    print(
        f"order={args.order} variables={len(cnf.names)-1} "
        f"clauses={len(cnf.clauses)} status={status}"
    )
    if status == "SAT":
        raise SystemExit(10)
    if status == "UNSAT":
        raise SystemExit(20)
    if status == "TIMEOUT":
        raise SystemExit(124)
    raise SystemExit(1)


if __name__ == "__main__":
    main()
