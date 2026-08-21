#!/usr/bin/env python3
"""Bounded one-guard survival search for the exact separated-port core.

This is a discovery tool, not a certificate generator.  It fixes the exact
nine-vertex complement core and exact six response lists, imposes
``gamma(G) >= 3`` and ``alpha(G) <= 3``, and asks whether all required
direct states can survive a prescribed number of attack rounds while the
forbidden direct states remain absent.
"""

from __future__ import annotations

import argparse
import itertools
from pathlib import Path


S = (0, 1, 2)
X, R, T, Q, V0, V1 = 3, 4, 5, 6, 7, 8
BASE_N = 9
BASE_H_EDGES = {
    (0, 1),
    (0, 2),
    (1, 2),
    (X, R),
    (R, T),
    (T, Q),
    (Q, V1),
    (V0, V1),
    (R, V0),
}
DESIRED_LISTS = {
    X: frozenset((0, 1, 2)),
    R: frozenset((0, 1)),
    T: frozenset((0, 1)),
    Q: frozenset((0, 1)),
    V0: frozenset((1, 2)),
    V1: frozenset((1, 2)),
}


class CNF:
    def __init__(self) -> None:
        self.names: list[str] = [""]
        self.by_name: dict[str, int] = {}
        self.clauses: list[tuple[int, ...]] = []

    def var(self, name: str) -> int:
        value = self.by_name.get(name)
        if value is None:
            value = len(self.names)
            self.by_name[name] = value
            self.names.append(name)
        return value

    def add(self, *literals: int) -> None:
        self.clauses.append(tuple(literals))


def pair(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def build(
    n: int,
    horizon: int,
    required_root_names: frozenset[str] | None = None,
) -> CNF:
    assert n >= BASE_N
    assert horizon >= 0
    cnf = CNF()
    vertices = tuple(range(n))
    triples = tuple(itertools.combinations(vertices, 3))

    def edge(u: int, v: int) -> int:
        a, b = pair(u, v)
        return cnf.var(f"e_{a}_{b}")

    def alive(level: int, triple: tuple[int, int, int] | frozenset[int]) -> int:
        a, b, c = sorted(triple)
        return cnf.var(f"k_{level}_{a}_{b}_{c}")

    # Exact old induced complement.
    for u, v in itertools.combinations(range(BASE_N), 2):
        cnf.add(edge(u, v) if (u, v) in BASE_H_EDGES else -edge(u, v))

    # omega(H)=3.
    for quad in itertools.combinations(vertices, 4):
        cnf.add(*(-edge(u, v) for u, v in itertools.combinations(quad, 2)))

    # gamma(G)>=3: every pair has an H-common neighbor.
    for u, v in itertools.combinations(vertices, 2):
        witnesses = []
        for w in vertices:
            if w in (u, v):
                continue
            witness = cnf.var(f"w_{u}_{v}_{w}")
            witnesses.append(witness)
            cnf.add(-witness, edge(u, w))
            cnf.add(-witness, edge(v, w))
        cnf.add(*witnesses)

    # Level zero means that the state dominates and is not one of the exact
    # forbidden direct swaps.
    for triple in triples:
        k0 = alive(0, triple)
        for attack in vertices:
            if attack in triple:
                continue
            cnf.add(-k0, *(-edge(guard, attack) for guard in triple))

    required: dict[str, tuple[int, int, int]] = {"S": tuple(S)}
    forbidden: list[tuple[int, int, int]] = []
    for target, allowed in DESIRED_LISTS.items():
        for guard in S:
            successor = tuple(sorted((set(S) - {guard}) | {target}))
            if guard in allowed:
                required[f"{target}:{guard}"] = successor
            else:
                forbidden.append(successor)

    for triple in forbidden:
        cnf.add(-alive(0, triple))

    # One-guard survival recurrence.  A selected response uses a G-edge and
    # lands in a state that survives one fewer future attack round.
    for level in range(1, horizon + 1):
        for triple in triples:
            current = alive(level, triple)
            cnf.add(-current, alive(0, triple))
            triple_set = set(triple)
            for attack in vertices:
                if attack in triple_set:
                    continue
                responses = []
                for guard in triple:
                    response = cnf.var(
                        f"m_{level}_{'_'.join(map(str, triple))}_{attack}_{guard}"
                    )
                    responses.append(response)
                    successor = tuple(
                        sorted((triple_set - {guard}) | {attack})
                    )
                    cnf.add(-response, -edge(guard, attack))
                    cnf.add(-response, alive(level - 1, successor))
                cnf.add(-current, *responses)

    selected_required = (
        required
        if required_root_names is None
        else {
            name: triple
            for name, triple in required.items()
            if name in required_root_names
        }
    )
    unknown = (
        set()
        if required_root_names is None
        else set(required_root_names) - set(required)
    )
    if unknown:
        raise ValueError(f"unknown roots: {sorted(unknown)}")
    for triple in selected_required.values():
        cnf.add(alive(horizon, triple))

    return cnf


def write(cnf: CNF, cnf_path: Path, names_path: Path) -> None:
    with cnf_path.open("w", encoding="ascii") as handle:
        handle.write(f"p cnf {len(cnf.names) - 1} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")
    with names_path.open("w", encoding="utf-8") as handle:
        for index, name in enumerate(cnf.names[1:], 1):
            handle.write(f"{index}\t{name}\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, default=14)
    parser.add_argument("--horizon", type=int, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--names", type=Path, required=True)
    parser.add_argument(
        "--root",
        action="append",
        default=None,
        help="required root: S or TARGET:GUARD; omit for every exact root",
    )
    args = parser.parse_args()
    cnf = build(
        args.order,
        args.horizon,
        None if args.root is None else frozenset(args.root),
    )
    write(cnf, args.cnf, args.names)
    print(
        f"order={args.order} horizon={args.horizon} "
        f"vars={len(cnf.names) - 1} clauses={len(cnf.clauses)} "
        f"roots={'all' if args.root is None else sorted(args.root)}"
    )


if __name__ == "__main__":
    main()
