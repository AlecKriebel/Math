#!/usr/bin/env python3
"""Small independent CNF for the four-neutral/two-port obstruction.

Unlike ``search.py``, this generator does not import the campaign SAT
builder and does not allocate move variables.  It expands the exact
three-guard response disjunction directly into eight CNF clauses.

The production formula asks for a 13-vertex graph G, an eternal family F
of triples, and an independent family state S=(h,i,j)=(0,1,2), subject to:

* gamma(G) >= 3;
* vertices 8,...,11 are G-complete to S;
* {h,j} is contained in L(3), and {h,i} is contained in L(5).

No alpha block is needed: an eternal triple-family and the independent
state S themselves force alpha(G)=3.  There is also no theta gap,
connectivity, negative list literal, signature condition on 3 or 5,
no-full hypothesis, exceptional vertex, mate edge, or condition on
vertices 4,6,7,12.  Thus UNSAT is stronger than the tight 5+5 exclusion.

Edge variables encode H=complement(G).
"""

from __future__ import annotations

import argparse
import itertools
from pathlib import Path
import subprocess
import sys


N = 13
S = (0, 1, 2)
H, I, J = S
X = 3
Y = 5
Q_START = 8


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
        clause = tuple(literals)
        if not clause or any(lit == 0 for lit in clause):
            raise ValueError("malformed clause")
        self.clauses.append(clause)

    def dimacs(self) -> str:
        body = "".join(
            " ".join(map(str, clause)) + " 0\n" for clause in self.clauses
        )
        return f"p cnf {len(self.names)-1} {len(self.clauses)}\n{body}"


def build(
    *,
    neutral_count: int = 4,
) -> tuple[CNF, dict[tuple[int, int], int], dict[tuple[int, ...], int]]:
    if not 0 <= neutral_count <= 5:
        raise ValueError("neutral_count must lie in 0..5")
    neutral_vertices = tuple(range(Q_START, Q_START + neutral_count))
    cnf = CNF()
    vertices = tuple(range(N))
    triples = tuple(itertools.combinations(vertices, 3))
    edge = {
        uv: cnf.var(f"edgeH({uv[0]},{uv[1]})")
        for uv in itertools.combinations(vertices, 2)
    }
    family = {
        state: cnf.var(f"family{state}")
        for state in triples
    }
    witness = {
        (u, v, w): cnf.var(f"commonH({u},{v};{w})")
        for u, v in itertools.combinations(vertices, 2)
        for w in vertices
        if w not in (u, v)
    }

    def e(u: int, v: int) -> int:
        return edge[pair(u, v)]

    # gamma(G)>=3: every pair has a common open H-neighbor.
    for u, v in itertools.combinations(vertices, 2):
        choices = [w for w in vertices if w not in (u, v)]
        cnf.add(*(witness[(u, v, w)] for w in choices))
        for w in choices:
            z = witness[(u, v, w)]
            cnf.add(-z, e(u, w))
            cnf.add(-z, e(v, w))

    # Literal one-guard closure, without move auxiliaries.  For a guard g,
    # the response conjunction is (-edgeH(g,r) AND family(successor)).
    # The disjunction of the three conjunctions has the exact eight-clause
    # distributive CNF below.  The choice of all three move-edge literals is
    # exactly the domination clause for the attacked vertex, so closure also
    # enforces that every selected state dominates; a duplicate domination
    # block is deliberately not emitted.
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
                response_pairs.append((-e(guard, attacked), family[successor]))
            for selected_literals in itertools.product(*response_pairs):
                cnf.add(-selected, *selected_literals)

    # Independent retained reference state.
    for u, v in itertools.combinations(S, 2):
        cnf.add(e(u, v))
    cnf.add(family[S])

    # Named neutral vertices.
    for q in neutral_vertices:
        for anchor in S:
            cnf.add(-e(anchor, q))

    def add_positive_responses(vertex: int, response: frozenset[int]) -> None:
        for anchor in response:
            successor = tuple(sorted((set(S) - {anchor}) | {vertex}))
            cnf.add(family[successor])

    add_positive_responses(X, frozenset((H, J)))
    add_positive_responses(Y, frozenset((H, I)))
    return cnf, edge, family


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--instance", type=Path, required=True)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--solver-log", type=Path, required=True)
    parser.add_argument("--model", type=Path)
    parser.add_argument("--neutral-count", type=int, default=4)
    args = parser.parse_args()

    cnf, _, _ = build(neutral_count=args.neutral_count)
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
