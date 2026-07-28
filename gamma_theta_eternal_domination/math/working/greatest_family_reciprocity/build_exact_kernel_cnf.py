#!/usr/bin/env python3
"""Build an exact bounded-fixed-point CNF for a reciprocity countermodel.

Labels fix disjoint independent triples S=012 and T=345 and the selected
exchange u=0, x=3.  The formula enforces alpha=gamma=3 and unfolds the
literal greatest triple-kernel for C(n,3) deletion rounds.  It requires
S-0+3 to survive and T-3+0 not to survive.  Because a descending chain on
C(n,3) states stabilizes within that many strict deletions, this is an exact
greatest-family condition rather than an arbitrary-family approximation.

This is a discovery/instance generator.  Any SAT model must be independently
decoded and checked from the graph.
"""

from __future__ import annotations

import argparse
import itertools
from pathlib import Path


class CNF:
    def __init__(self) -> None:
        self.names = [""]
        self.by_name: dict[str, int] = {}
        self.clauses: list[tuple[int, ...]] = []

    def var(self, name: str) -> int:
        found = self.by_name.get(name)
        if found is None:
            found = len(self.names)
            self.by_name[name] = found
            self.names.append(name)
        return found

    def add(self, *lits: int) -> None:
        if not lits:
            raise ValueError("empty clause")
        self.clauses.append(tuple(lits))

    def equiv_and(self, out: int, inputs: tuple[int, ...]) -> None:
        for value in inputs:
            self.add(-out, value)
        self.add(out, *(-value for value in inputs))

    def equiv_or(self, out: int, inputs: tuple[int, ...]) -> None:
        for value in inputs:
            self.add(-value, out)
        self.add(-out, *inputs)


def pair(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def build(n: int, rounds: int | None = None) -> CNF:
    if n < 6:
        raise ValueError("disjoint triples require n>=6")
    vertices = tuple(range(n))
    triples = tuple(itertools.combinations(vertices, 3))
    triple_index = {triple: index for index, triple in enumerate(triples)}
    if rounds is None:
        rounds = len(triples)
    cnf = CNF()

    def edge(u: int, v: int) -> int:
        a, b = pair(u, v)
        return cnf.var(f"e_{a}_{b}")

    def live(level: int, triple: tuple[int, int, int]) -> int:
        return cnf.var(f"k_{level}_{triple_index[triple]}")

    # S=012 and T=345 are independent in G.
    for triple in ((0, 1, 2), (3, 4, 5)):
        for u, v in itertools.combinations(triple, 2):
            cnf.add(-edge(u, v))

    # alpha(G)<=3.
    for quad in itertools.combinations(vertices, 4):
        cnf.add(*(edge(u, v) for u, v in itertools.combinations(quad, 2)))

    # gamma(G)>=3: every pair has a vertex outside it nonadjacent to both.
    for u, v in itertools.combinations(vertices, 2):
        witnesses: list[int] = []
        for w in vertices:
            if w in (u, v):
                continue
            witness = cnf.var(f"w_{u}_{v}_{w}")
            witnesses.append(witness)
            cnf.add(-witness, -edge(u, w))
            cnf.add(-witness, -edge(v, w))
            # Exactness is unnecessary: witnesses only certify existence.
        cnf.add(*witnesses)

    # K_0 is exactly the set of dominating triples.
    for triple in triples:
        domination_bits: list[int] = []
        occupied = set(triple)
        for target in vertices:
            if target in occupied:
                continue
            dom = cnf.var(f"d_{triple_index[triple]}_{target}")
            incident = tuple(edge(guard, target) for guard in triple)
            cnf.equiv_or(dom, incident)
            domination_bits.append(dom)
        cnf.equiv_and(live(0, triple), tuple(domination_bits))

    # Exact descending deletion operator.
    for level in range(rounds):
        for triple in triples:
            occupied = set(triple)
            obligations: list[int] = [live(level, triple)]
            for target in vertices:
                if target in occupied:
                    continue
                good_moves: list[int] = []
                for guard in triple:
                    successor = tuple(sorted((occupied - {guard}) | {target}))
                    move = cnf.var(
                        f"m_{level}_{triple_index[triple]}_{target}_{guard}"
                    )
                    cnf.equiv_and(
                        move,
                        (edge(guard, target), live(level, successor)),
                    )
                    good_moves.append(move)
                answer = cnf.var(
                    f"a_{level}_{triple_index[triple]}_{target}"
                )
                cnf.equiv_or(answer, tuple(good_moves))
                obligations.append(answer)
            cnf.equiv_and(live(level + 1, triple), tuple(obligations))

    S = (0, 1, 2)
    T = (3, 4, 5)
    forward = (1, 2, 3)
    reverse = (0, 4, 5)
    cnf.add(live(rounds, S))
    cnf.add(live(rounds, T))
    cnf.add(live(rounds, forward))
    cnf.add(-live(rounds, reverse))
    return cnf


def write(cnf: CNF, cnf_path: Path, names_path: Path) -> None:
    with cnf_path.open("w", encoding="ascii") as handle:
        handle.write(f"p cnf {len(cnf.names)-1} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")
    with names_path.open("w", encoding="utf-8") as handle:
        for number, name in enumerate(cnf.names[1:], start=1):
            handle.write(f"{number}\t{name}\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--rounds", type=int)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--names", type=Path, required=True)
    args = parser.parse_args()
    cnf = build(args.order, args.rounds)
    write(cnf, args.cnf, args.names)
    print(
        f"order={args.order} rounds={args.rounds or len(tuple(itertools.combinations(range(args.order),3)))} "
        f"variables={len(cnf.names)-1} clauses={len(cnf.clauses)}"
    )


if __name__ == "__main__":
    main()
