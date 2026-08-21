#!/usr/bin/env python3
"""SAT synthesis of the sharp static inactive-set boundary control.

The sought graph H' is explicitly tripartite, every pair of vertices has a
common neighbor, R induces a fixed C5, and A contains a fixed triangle.
Potential triangles that would violate componentwise responder-color
covariance are forbidden.  A satisfying instance therefore models every
static conclusion used in the active-set bridge, but R cannot use two colors.
"""

from __future__ import annotations

import argparse
import itertools
import subprocess
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[2]
CADICAL = CAMPAIGN / "tools" / "cadical_3_0_1" / "build" / "cadical"


class Cnf:
    def __init__(self) -> None:
        self.variables = 0
        self.clauses: list[tuple[int, ...]] = []

    def variable(self) -> int:
        self.variables += 1
        return self.variables

    def add(self, *literals: int) -> None:
        self.clauses.append(tuple(literals))


def synthesize(extra_counts: tuple[int, int, int]) -> dict[str, object] | None:
    # Fixed C5 colors: 0,1,0,1,2.  Vertices 5,6,7 form the active root
    # triangle in colors 0,1,2.  Remaining vertices are active auxiliaries.
    colors = [0, 1, 0, 1, 2, 0, 1, 2]
    for color, count in enumerate(extra_counts):
        colors.extend([color] * count)
    n = len(colors)
    inactive = frozenset(range(5))
    active = frozenset(range(5, n))
    cnf = Cnf()
    edge_var: dict[tuple[int, int], int] = {}
    for u, v in itertools.combinations(range(n), 2):
        if colors[u] != colors[v]:
            edge_var[u, v] = cnf.variable()

    def edge(u: int, v: int) -> int | None:
        if u > v:
            u, v = v, u
        return edge_var.get((u, v))

    cycle_edges = {
        tuple(sorted((vertex, (vertex + 1) % 5))) for vertex in range(5)
    }
    for u, v in itertools.combinations(range(5), 2):
        variable = edge(u, v)
        if variable is not None:
            cnf.add(variable if (u, v) in cycle_edges else -variable)

    for u, v in ((5, 6), (5, 7), (6, 7)):
        cnf.add(edge(u, v))

    # Every pair has an outside common neighbor.
    for u, v in itertools.combinations(range(n), 2):
        witnesses = []
        for w in range(n):
            if w in (u, v):
                continue
            left = edge(u, w)
            right = edge(v, w)
            if left is None or right is None:
                continue
            witness = cnf.variable()
            witnesses.append(witness)
            cnf.add(-witness, left)
            cnf.add(-witness, right)
            cnf.add(witness, -left, -right)
        if not witnesses:
            return None
        cnf.add(*witnesses)

    triples = []
    for triple in itertools.combinations(range(n), 3):
        if {colors[v] for v in triple} != {0, 1, 2}:
            continue
        edges = tuple(edge(u, v) for u, v in itertools.combinations(triple, 2))
        if any(variable is None for variable in edges):
            continue
        active_colors = frozenset(colors[v] for v in triple if v in active)
        triples.append((triple, edges, active_colors))
        if not active_colors:
            cnf.add(*(-variable for variable in edges))

    # Ridge-adjacent triangles must have identical active-color sets.
    for (left, left_edges, left_colors), (
        right,
        right_edges,
        right_colors,
    ) in itertools.combinations(triples, 2):
        if len(set(left) & set(right)) != 2 or left_colors == right_colors:
            continue
        union_edges = tuple(dict.fromkeys(left_edges + right_edges))
        cnf.add(*(-variable for variable in union_edges))

    with tempfile.TemporaryDirectory(prefix="inactive-static-control-") as tmp:
        dimacs = Path(tmp) / "instance.cnf"
        model_path = Path(tmp) / "model.txt"
        with dimacs.open("w", encoding="ascii") as stream:
            stream.write(f"p cnf {cnf.variables} {len(cnf.clauses)}\n")
            for clause in cnf.clauses:
                stream.write(" ".join(map(str, clause)) + " 0\n")
        completed = subprocess.run(
            [str(CADICAL), str(dimacs)],
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode == 20:
            return None
        if completed.returncode != 10:
            raise RuntimeError(completed.stdout + completed.stderr)
        model_path.write_text(completed.stdout, encoding="utf-8")
        positive = {
            int(token)
            for line in completed.stdout.splitlines()
            if line.startswith("v ")
            for token in line.split()[1:]
            if token != "0" and int(token) > 0
        }
    h_edges = [
        [u, v] for (u, v), variable in edge_var.items() if variable in positive
    ]
    return {
        "order": n,
        "colors": colors,
        "active_set": sorted(active),
        "inactive_set_R": sorted(inactive),
        "h_edges": h_edges,
        "variables": cnf.variables,
        "clauses": len(cnf.clauses),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-extra", type=int, default=6)
    args = parser.parse_args()
    for total in range(args.max_extra + 1):
        for first in range(total + 1):
            for second in range(total - first + 1):
                counts = (first, second, total - first - second)
                result = synthesize(counts)
                print("tested", counts, "SAT" if result else "UNSAT")
                if result:
                    print(result)
                    return
    print("no control in bounded search")


if __name__ == "__main__":
    main()
