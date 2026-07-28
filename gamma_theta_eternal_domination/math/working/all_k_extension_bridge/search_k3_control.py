#!/usr/bin/env python3
"""Discovery SAT search for a critical-deletion full-target control.

The unknown edge variables encode H = complement(G).  The formula asks for
an equality graph with k=3, an equality deletion G-x, and an eternal family
having a full response at a fixed root triangle.  Two proper colorings of
H-x are planted:

* one extends over x and certifies theta(G)=3;
* the other uses all three colors on three physical H-neighbors of x.

Thus a model would show, inside the exact equality and critical-deletion
hypotheses, that a deletion coloring cannot be chosen arbitrarily in the
C-108 common-responder-color argument.

This is a discovery generator, not a certificate-producing program.
"""

from __future__ import annotations

import argparse
import itertools
import subprocess
import tempfile
from pathlib import Path


ROOT = (0, 1, 2)
BLOCKERS = (3, 4, 5)


def pair(first: int, second: int) -> tuple[int, int]:
    if first == second:
        raise ValueError("loop")
    return (first, second) if first < second else (second, first)


class CNF:
    def __init__(self) -> None:
        self.names = [""]
        self.clauses: list[tuple[int, ...]] = []

    def var(self, name: str) -> int:
        self.names.append(name)
        return len(self.names) - 1

    def add(self, *literals: int) -> None:
        clause = tuple(literals)
        if not clause:
            raise ValueError("empty clause")
        if any(literal == 0 for literal in clause):
            raise ValueError("zero literal")
        if any(-literal in clause for literal in clause):
            return
        self.clauses.append(tuple(dict.fromkeys(clause)))

    def dimacs(self) -> str:
        rows = [f"p cnf {len(self.names) - 1} {len(self.clauses)}"]
        rows.extend(" ".join(map(str, clause)) + " 0" for clause in self.clauses)
        return "\n".join(rows) + "\n"


def build(
    order: int,
    *,
    impose_blocked_coloring: bool = True,
) -> tuple[
    CNF,
    dict[tuple[int, int], int],
    dict[tuple[int, int, int], int],
]:
    if order < 8:
        raise ValueError("need a root, three blockers, one residual, and x")
    target = order - 1
    vertices = range(order)
    deletion = range(target)
    triples = tuple(itertools.combinations(vertices, 3))
    cnf = CNF()
    edge = {
        uv: cnf.var(f"h_{uv[0]}_{uv[1]}")
        for uv in itertools.combinations(vertices, 2)
    }
    family = {
        state: cnf.var("f_" + "_".join(map(str, state)))
        for state in triples
    }
    witness = {
        (u, v, w): cnf.var(f"w_{u}_{v}_{w}")
        for u, v in itertools.combinations(vertices, 2)
        for w in vertices
        if w not in (u, v)
    }
    deletion_witness = {
        (u, v, w): cnf.var(f"wd_{u}_{v}_{w}")
        for u, v in itertools.combinations(deletion, 2)
        for w in deletion
        if w not in (u, v)
    }
    move = {
        (state, attacked, guard): cnf.var(
            "m_"
            + "_".join(map(str, state))
            + f"__{attacked}_{guard}"
        )
        for state in triples
        for attacked in vertices
        if attacked not in state
        for guard in state
    }

    def h(first: int, second: int) -> int:
        return edge[pair(first, second)]

    # A selected full coloring makes H K4-free and certifies theta(G) <= 3.
    full_color = {
        (vertex, color): cnf.var(f"c_{vertex}_{color}")
        for vertex in vertices
        for color in range(3)
    }
    for vertex in vertices:
        cnf.add(*(full_color[(vertex, color)] for color in range(3)))
        for first, second in itertools.combinations(range(3), 2):
            cnf.add(
                -full_color[(vertex, first)],
                -full_color[(vertex, second)],
            )
    for u, v in itertools.combinations(vertices, 2):
        for color in range(3):
            cnf.add(
                -h(u, v),
                -full_color[(u, color)],
                -full_color[(v, color)],
            )
    for vertex, color in zip(ROOT, range(3), strict=True):
        cnf.add(full_color[(vertex, color)])
    cnf.add(full_color[(target, 0)])

    # A second selected proper coloring of H-x is deliberately blocked at x.
    if impose_blocked_coloring:
        blocked_color = {
            (vertex, color): cnf.var(f"b_{vertex}_{color}")
            for vertex in deletion
            for color in range(3)
        }
        for vertex in deletion:
            cnf.add(*(blocked_color[(vertex, color)] for color in range(3)))
            for first, second in itertools.combinations(range(3), 2):
                cnf.add(
                    -blocked_color[(vertex, first)],
                    -blocked_color[(vertex, second)],
                )
        for u, v in itertools.combinations(deletion, 2):
            for color in range(3):
                cnf.add(
                    -h(u, v),
                    -blocked_color[(u, color)],
                    -blocked_color[(v, color)],
                )
        for vertex, color in zip(ROOT, range(3), strict=True):
            cnf.add(blocked_color[(vertex, color)])
        for vertex, color in zip(BLOCKERS, range(3), strict=True):
            cnf.add(blocked_color[(vertex, color)])

    # gamma(G) >= 3: every pair has a common H-neighbor.
    for u, v in itertools.combinations(vertices, 2):
        choices = [w for w in vertices if w not in (u, v)]
        cnf.add(*(witness[(u, v, w)] for w in choices))
        for w in choices:
            z = witness[(u, v, w)]
            cnf.add(-z, h(u, w))
            cnf.add(-z, h(v, w))

    # The deletion also has gamma >= 3.
    for u, v in itertools.combinations(deletion, 2):
        choices = [w for w in deletion if w not in (u, v)]
        cnf.add(*(deletion_witness[(u, v, w)] for w in choices))
        for w in choices:
            z = deletion_witness[(u, v, w)]
            cnf.add(-z, h(u, w))
            cnf.add(-z, h(v, w))

    # Every selected family state dominates G.
    for state in triples:
        selected = family[state]
        for attacked in vertices:
            if attacked in state:
                continue
            cnf.add(
                -selected,
                -h(attacked, state[0]),
                -h(attacked, state[1]),
                -h(attacked, state[2]),
            )

    # Literal one-guard closure.
    cnf.add(*family.values())
    for state in triples:
        selected = family[state]
        for attacked in vertices:
            if attacked in state:
                continue
            responses: list[int] = []
            for guard in state:
                z = move[(state, attacked, guard)]
                successor = tuple(
                    sorted((set(state) - {guard}) | {attacked})
                )
                responses.append(z)
                cnf.add(-z, -h(guard, attacked))
                cnf.add(-z, family[successor])
            cnf.add(-selected, *responses)

    # Every H-triangle is a maximum independent set and must be retained.
    for state in triples:
        cnf.add(
            -h(state[0], state[1]),
            -h(state[0], state[2]),
            -h(state[1], state[2]),
            family[state],
        )

    # The root is an H-triangle and x has a full family response there.
    for u, v in itertools.combinations(ROOT, 2):
        cnf.add(h(u, v))
    root = tuple(ROOT)
    cnf.add(family[root])
    for guard in ROOT:
        cnf.add(-h(guard, target))
        successor = tuple(sorted((set(ROOT) - {guard}) | {target}))
        cnf.add(family[successor])

    # The blocked coloring uses all three colors on physical H-neighbors of x.
    if impose_blocked_coloring:
        for blocker in BLOCKERS:
            cnf.add(h(blocker, target))

    return cnf, edge, family


def solve(
    order: int,
    solver: Path,
    *,
    impose_blocked_coloring: bool,
) -> int:
    cnf, edge, family = build(
        order,
        impose_blocked_coloring=impose_blocked_coloring,
    )
    with tempfile.TemporaryDirectory(prefix="all-k-bridge-control-") as temp:
        instance = Path(temp) / "instance.cnf"
        instance.write_text(cnf.dimacs(), encoding="ascii")
        completed = subprocess.run(
            [str(solver), str(instance)],
            check=False,
            capture_output=True,
            text=True,
        )
    print(
        f"n={order} vars={len(cnf.names)-1} clauses={len(cnf.clauses)} "
        f"returncode={completed.returncode}"
    )
    if completed.returncode != 10:
        print(completed.stdout)
        return completed.returncode
    values: dict[int, bool] = {}
    for line in completed.stdout.splitlines():
        if not line.startswith("v "):
            continue
        for literal_text in line.split()[1:]:
            literal = int(literal_text)
            if literal:
                values[abs(literal)] = literal > 0
    h_edges = [uv for uv, variable in edge.items() if values.get(variable, False)]
    selected = [
        state
        for state, variable in family.items()
        if values.get(variable, False)
    ]
    print("H_EDGES", h_edges)
    print("FAMILY", selected)
    return 10


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--ablate-blocked-coloring", action="store_true")
    arguments = parser.parse_args()
    raise SystemExit(
        solve(
            arguments.order,
            arguments.solver.resolve(),
            impose_blocked_coloring=not arguments.ablate_blocked_coloring,
        )
    )


if __name__ == "__main__":
    main()
