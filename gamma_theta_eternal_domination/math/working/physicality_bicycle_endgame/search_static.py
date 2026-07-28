#!/usr/bin/env python3
"""Search for a static physical odd-holonomy control.

This is a proof-discovery helper, not a certificate checker.  The fixed
vertices 0,1,2 are the anchor triangle in H.  The nine outside vertices
form three transversal triangles, joined by three same-type edges of odd
total parity.  All anchor incidences are physical, every same-type graph
respects a prescribed bipartition, every outside neighborhood is
side-pure in each type, every cross edge extends to a transversal
triangle, H has no K4, and every vertex pair has a common H-neighbor.
"""

from __future__ import annotations

import argparse
from itertools import combinations
from pathlib import Path
import subprocess


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
        return f"p cnf {len(self.names) - 1} {len(self.clauses)}\n{body}"


def pair(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def build() -> tuple[CNF, dict[str, object]]:
    order = 12
    anchors = (0, 1, 2)
    outside = tuple(range(3, order))
    gates = (
        (3, 4, 5),
        (6, 7, 8),
        (9, 10, 11),
    )
    vertex_type = {
        vertex: gate_position
        for gate in gates
        for gate_position, vertex in enumerate(gate)
    }
    side = {
        3: 0,
        6: 1,
        9: 1,
        4: 1,
        7: 0,
        10: 1,
        5: 1,
        8: 1,
        11: 0,
    }

    cnf = CNF()
    edge = {
        uv: cnf.var(f"H({uv[0]},{uv[1]})")
        for uv in combinations(range(order), 2)
    }

    def h(u: int, v: int) -> int:
        return edge[pair(u, v)]

    # Exact anchor triangle and exact physical type incidence.
    for u, v in combinations(anchors, 2):
        cnf.add(h(u, v))
    for vertex in outside:
        for anchor in anchors:
            cnf.add(
                h(anchor, vertex)
                if anchor == vertex_type[vertex]
                else -h(anchor, vertex)
            )

    # Fixed transversal gates.
    for gate in gates:
        for u, v in combinations(gate, 2):
            cnf.add(h(u, v))

    # Odd three-gate ring plus a same-type mate for each unused port.
    for u, v in ((3, 6), (7, 10), (11, 5), (3, 9), (4, 7), (8, 11)):
        cnf.add(h(u, v))

    # Prescribed bipartitions for all same-type edges.
    for u, v in combinations(outside, 2):
        if vertex_type[u] == vertex_type[v] and side[u] == side[v]:
            cnf.add(-h(u, v))

    # Universal side-purity relative to each prescribed type bipartition.
    for q in outside:
        for omitted in anchors:
            left = [
                x
                for x in outside
                if vertex_type[x] == omitted and side[x] == 0 and x != q
            ]
            right = [
                x
                for x in outside
                if vertex_type[x] == omitted and side[x] == 1 and x != q
            ]
            for x in left:
                for y in right:
                    cnf.add(-h(q, x), -h(q, y))

    # Every cross edge extends to a triangle through the third type.
    for x, y in combinations(outside, 2):
        tx = vertex_type[x]
        ty = vertex_type[y]
        if tx == ty:
            continue
        third = ({0, 1, 2} - {tx, ty}).pop()
        witnesses = []
        for z in outside:
            if vertex_type[z] != third:
                continue
            marker = cnf.var(f"T({x},{y};{z})")
            witnesses.append(marker)
            cnf.add(-marker, h(x, z))
            cnf.add(-marker, h(y, z))
        cnf.add(-h(x, y), *witnesses)

    # Clique number at most three.
    for four in combinations(range(order), 4):
        cnf.add(*(-h(u, v) for u, v in combinations(four, 2)))

    # gamma(complement(H)) >= 3: every pair has a common H-neighbor.
    for u, v in combinations(range(order), 2):
        witnesses = []
        for z in range(order):
            if z in (u, v):
                continue
            marker = cnf.var(f"W({u},{v};{z})")
            witnesses.append(marker)
            cnf.add(-marker, h(u, z))
            cnf.add(-marker, h(v, z))
        cnf.add(*witnesses)

    return cnf, {
        "order": order,
        "edge": edge,
        "types": vertex_type,
        "sides": side,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--instance", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    args = parser.parse_args()
    cnf, _ = build()
    args.instance.write_text(cnf.dimacs(), encoding="ascii")
    run = subprocess.run(
        [
            str(args.solver),
            "--quiet",
            "--binary=false",
            "-w",
            str(args.model),
            str(args.instance),
        ],
        check=False,
    )
    print(
        f"variables={len(cnf.names)-1} clauses={len(cnf.clauses)} "
        f"exit={run.returncode}"
    )
    raise SystemExit(run.returncode)


if __name__ == "__main__":
    main()
