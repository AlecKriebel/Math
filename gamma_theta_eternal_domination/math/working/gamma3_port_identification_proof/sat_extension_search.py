#!/usr/bin/env python3
"""SAT search for equality extensions of the separated-port control.

The search fixes the exact nine-vertex induced complement and its six
response lists from ``HFzvvn{``.  It asks whether arbitrary additional
vertices can make

    gamma(G) = alpha(G) = gamma^infinity(G) = 3

while retaining an eternal triple-family with those exact old lists.

The CNF directly encodes the one-guard definition.  It is intended for
discovery and bounded controls; a SAT model is independently rechecked by
``verify_sat_extension.py`` before it is used.
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
    *,
    unique_full: bool,
    require_gamma_three: bool,
    selected_gamma_pairs: frozenset[tuple[int, int]],
    force_v01_cap: bool,
    require_exact_old_lists: bool,
    require_closure: bool,
) -> CNF:
    assert n >= BASE_N
    cnf = CNF()
    vertices = range(n)
    triples = tuple(itertools.combinations(vertices, 3))

    def edge(u: int, v: int) -> int:
        a, b = pair(u, v)
        return cnf.var(f"e_{a}_{b}")

    def state(triple: tuple[int, int, int] | frozenset[int]) -> int:
        a, b, c = sorted(triple)
        return cnf.var(f"f_{a}_{b}_{c}")

    # The old nine vertices induce exactly the separated-port complement.
    for u, v in itertools.combinations(range(BASE_N), 2):
        cnf.add(edge(u, v) if (u, v) in BASE_H_EDGES else -edge(u, v))

    # alpha(G)=omega(H)=3: the anchor triangle exists and no H K4 exists.
    for u, v in itertools.combinations(S, 2):
        cnf.add(edge(u, v))
    for quad in itertools.combinations(vertices, 4):
        cnf.add(*(-edge(u, v) for u, v in itertools.combinations(quad, 2)))

    # gamma(G)>=3: every pair has a common H-neighbor.
    gamma_pairs = (
        tuple(itertools.combinations(vertices, 2))
        if require_gamma_three
        else tuple(sorted(selected_gamma_pairs))
    )
    if gamma_pairs:
        for u, v in gamma_pairs:
            witnesses = []
            for w in vertices:
                if w in (u, v):
                    continue
                witness = cnf.var(f"w_{u}_{v}_{w}")
                witnesses.append(witness)
                cnf.add(-witness, edge(u, w))
                cnf.add(-witness, edge(v, w))
            cnf.add(*witnesses)

    # The family is nonempty at S and has exactly the prescribed old direct
    # swaps.  The anchor K4 exclusion also makes S a dominating triple.
    cnf.add(state(S))
    old_list_requirements = (
        DESIRED_LISTS
        if require_exact_old_lists
        else {X: frozenset((0, 1, 2))}
    )
    for target, allowed in old_list_requirements.items():
        for guard in S:
            successor = tuple(sorted((set(S) - {guard}) | {target}))
            cnf.add(state(successor) if guard in allowed else -state(successor))

    if force_v01_cap:
        assert n > BASE_N
        cap = BASE_N
        cnf.add(edge(cap, V0))
        cnf.add(edge(cap, V1))
        successor = tuple(sorted((set(S) - {0}) | {cap}))
        cnf.add(state(successor))

    if unique_full:
        for target in range(BASE_N, n):
            direct = [
                state(tuple(sorted((set(S) - {guard}) | {target})))
                for guard in S
            ]
            cnf.add(*(-literal for literal in direct))

    # Every retained state dominates.  For an outside vertex r, domination
    # means at least one state vertex has a G-edge to r, i.e. a missing
    # complement edge.
    for triple in triples:
        f_triple = state(triple)
        for attack in vertices:
            if attack in triple:
                continue
            cnf.add(
                -f_triple,
                *(-edge(guard, attack) for guard in triple),
            )

    # Literal one-guard closure.  A selected move must use a G-edge and land
    # in a retained successor.  Every retained source has one selected move
    # for each unoccupied attack.
    if require_closure:
        for triple in triples:
            f_triple = state(triple)
            triple_set = set(triple)
            for attack in vertices:
                if attack in triple_set:
                    continue
                moves = []
                for guard in triple:
                    move = cnf.var(
                        "m_"
                        + "_".join(map(str, triple))
                        + f"_{attack}_{guard}"
                    )
                    moves.append(move)
                    successor = tuple(
                        sorted((triple_set - {guard}) | {attack})
                    )
                    cnf.add(-move, -edge(guard, attack))
                    cnf.add(-move, state(successor))
                cnf.add(-f_triple, *moves)

    return cnf


def write_dimacs(cnf: CNF, path: Path, names_path: Path) -> None:
    with path.open("w", encoding="ascii") as handle:
        handle.write(f"p cnf {len(cnf.names) - 1} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")
    with names_path.open("w", encoding="utf-8") as handle:
        for index, name in enumerate(cnf.names[1:], start=1):
            handle.write(f"{index}\\t{name}\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--names", type=Path, required=True)
    parser.add_argument("--unique-full", action="store_true")
    parser.add_argument("--allow-gamma-two", action="store_true")
    parser.add_argument("--force-v01-cap", action="store_true")
    parser.add_argument("--only-full-x", action="store_true")
    parser.add_argument("--omit-closure", action="store_true")
    parser.add_argument(
        "--gamma-pair",
        action="append",
        default=[],
        help="require a common H-neighbor for u,v even with --allow-gamma-two",
    )
    args = parser.parse_args()
    cnf = build(
        args.order,
        unique_full=args.unique_full,
        require_gamma_three=not args.allow_gamma_two,
        selected_gamma_pairs=frozenset(
            pair(*(int(item) for item in value.split(",")))
            for value in args.gamma_pair
        ),
        force_v01_cap=args.force_v01_cap,
        require_exact_old_lists=not args.only_full_x,
        require_closure=not args.omit_closure,
    )
    write_dimacs(cnf, args.cnf, args.names)
    print(
        f"order={args.order} vars={len(cnf.names)-1} "
        f"clauses={len(cnf.clauses)} unique_full={args.unique_full} "
        f"require_gamma_three={not args.allow_gamma_two} "
        f"force_v01_cap={args.force_v01_cap} "
        f"exact_old_lists={not args.only_full_x} "
        f"closure={not args.omit_closure} "
        f"selected_gamma_pairs={args.gamma_pair}"
    )


if __name__ == "__main__":
    main()
