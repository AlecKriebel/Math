#!/usr/bin/env python3
"""Small exact probes for two separated tight third-color gates.

This is discovery code, not a certificate generator.  The edge variables
encode H = complement(G).  The retained-state variables encode an arbitrary
eternal family of triples directly from the one-guard definition.

Vertices 0,1,2 are the independent anchors a,b,c.  Each gate has physical
ports

    X : list {a,b},  Y : list {b,c},  Z : list {a,c},

with H-edges cX, aY, bZ, XZ, YZ and a G-edge XY.  Two vertex-disjoint
projection paths connect X0 to X1 inside W_c and Y0 to Y1 inside W_a.
Their independently selectable parities let us test the first genuinely
distributed odd-holonomy bigon.
"""

from __future__ import annotations

import argparse
from itertools import combinations, product
from pathlib import Path
import subprocess


S = (0, 1, 2)
A, B, C = S
X0, Y0, Z0, X1, Y1, Z1 = range(3, 9)


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
    x_length: int,
    y_length: int,
    *,
    spare_vertices: int = 0,
    enforce_gamma: bool = True,
    rectangle_only: bool = False,
    list_only: bool = False,
    boundary_only: bool = False,
) -> tuple[CNF, int]:
    if x_length < 1 or y_length < 1:
        raise ValueError("this separated-port probe requires positive paths")

    next_vertex = 9
    x_interior = tuple(range(next_vertex, next_vertex + x_length - 1))
    next_vertex += x_length - 1
    y_interior = tuple(range(next_vertex, next_vertex + y_length - 1))
    next_vertex += y_length - 1
    order = next_vertex + spare_vertices
    vertices = tuple(range(order))
    triples = tuple(combinations(vertices, 3))

    cnf = CNF()
    edge = {
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
        return edge[pair(u, v)]

    if enforce_gamma:
        for u, v in combinations(vertices, 2):
            choices = tuple(w for w in vertices if w not in (u, v))
            cnf.add(*(witness[(u, v, w)] for w in choices))
            for w in choices:
                marker = witness[(u, v, w)]
                cnf.add(-marker, e(u, w))
                cnf.add(-marker, e(v, w))

    # Exact one-guard closure plus domination of every retained state.
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

    for u, v in combinations(S, 2):
        cnf.add(e(u, v))
    cnf.add(family[S])

    def direct_state(vertex: int, omitted: int) -> tuple[int, int, int]:
        return tuple(sorted((set(S) - {omitted}) | {vertex}))

    def exact_list(vertex: int, response: frozenset[int]) -> None:
        for omitted in S:
            literal = family[direct_state(vertex, omitted)]
            cnf.add(literal if omitted in response else -literal)

    if rectangle_only:
        for vertex in (X0, X1):
            cnf.add(-family[direct_state(vertex, C)])
        for vertex in (Y0, Y1):
            cnf.add(-family[direct_state(vertex, A)])
        for x, y in ((X0, Y0), (X1, Y1)):
            cnf.add(family[tuple(sorted((A, x, y)))])
            cnf.add(family[tuple(sorted((C, x, y)))])
    else:
        for vertex in (X0, X1):
            exact_list(vertex, frozenset((A, B)))
        for vertex in (Y0, Y1):
            exact_list(vertex, frozenset((B, C)))
        if not list_only and not boundary_only:
            for vertex in (Z0, Z1):
                exact_list(vertex, frozenset((A, C)))
        if boundary_only:
            cnf.add(-family[tuple(sorted((B, X0, Y0)))])
            cnf.add(-family[tuple(sorted((B, X1, Y1)))])

    # Connector interiors only need the relevant dynamic omission.
    for vertex in x_interior:
        cnf.add(-family[direct_state(vertex, C)])
    for vertex in y_interior:
        cnf.add(-family[direct_state(vertex, A)])

    h_edges: list[tuple[int, int]] = list(combinations(S, 2))
    if not rectangle_only and not list_only and not boundary_only:
        for x, y, z in ((X0, Y0, Z0), (X1, Y1, Z1)):
            h_edges.extend(((C, x), (A, y), (B, z), (x, z), (y, z)))
    x_path = (X0, *x_interior, X1)
    y_path = (Y0, *y_interior, Y1)
    h_edges.extend(zip(x_path[:-1], x_path[1:], strict=True))
    h_edges.extend(zip(y_path[:-1], y_path[1:], strict=True))

    g_edges: list[tuple[int, int]] = []
    if not rectangle_only and not list_only and not boundary_only:
        for x, y, z in ((X0, Y0, Z0), (X1, Y1, Z1)):
            g_edges.extend(
                (
                    (A, x), (B, x),
                    (B, y), (C, y),
                    (A, z), (C, z),
                    (x, y),
                )
            )

    for u, v in h_edges:
        cnf.add(e(u, v))
    for u, v in g_edges:
        cnf.add(-e(u, v))
    return cnf, order


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--x-length", type=int, required=True)
    parser.add_argument("--y-length", type=int, required=True)
    parser.add_argument("--spare-vertices", type=int, default=0)
    parser.add_argument("--no-gamma", action="store_true")
    parser.add_argument("--rectangle-only", action="store_true")
    parser.add_argument("--list-only", action="store_true")
    parser.add_argument("--boundary-only", action="store_true")
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--instance", type=Path, required=True)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--model", type=Path)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()

    cnf, order = build(
        args.x_length,
        args.y_length,
        spare_vertices=args.spare_vertices,
        enforce_gamma=not args.no_gamma,
        rectangle_only=args.rectangle_only,
        list_only=args.list_only,
        boundary_only=args.boundary_only,
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
        f"order={order} variables={len(cnf.names)-1} "
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
