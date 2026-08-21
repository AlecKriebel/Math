#!/usr/bin/env python3
"""Discovery synthesis for an exact family-list mixed P4 at gamma=3.

This is deliberately a direct encoding of the one-guard definition.  The
edge variables encode H = complement(G), and the family variables encode an
arbitrary eternal family of triples.  Vertices 0,1,2 are the independent
reference state.  Vertices 3,4,5,6 induce the complement path

    3 -- 4 -- 5 -- 6

with exact family-response lists

    {0}, {0,2}, {1,2}, {1}.

Every vertex pair has a common H-neighbor, which is exactly gamma(G) >= 3.
Since the retained independent triple dominates, gamma(G) is then exactly
three.

The script is a discovery tool, not a certificate generator.
"""

from __future__ import annotations

import argparse
from itertools import combinations, product
from pathlib import Path
import subprocess


S = (0, 1, 2)
PATH = (3, 4, 5, 6)
LISTS = {
    3: frozenset((0,)),
    4: frozenset((0, 2)),
    5: frozenset((1, 2)),
    6: frozenset((1,)),
}


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
            raise ValueError("tautological clause")
        self.clauses.append(clause)

    def dimacs(self) -> str:
        body = "".join(
            " ".join(map(str, clause)) + " 0\n" for clause in self.clauses
        )
        return f"p cnf {len(self.names) - 1} {len(self.clauses)}\n{body}"


def build(
    order: int,
    *,
    enforce_gamma: bool = True,
    gamma_pairs: set[tuple[int, int]] | None = None,
) -> tuple[CNF, dict[tuple[int, int], int], dict[tuple[int, int, int], int]]:
    if order < 7:
        raise ValueError("order must be at least seven")
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

    # gamma(G) >= 3: no singleton or pair dominates, equivalently every
    # unordered vertex pair has an outside common complement neighbor.
    if enforce_gamma:
        selected_pairs = (
            set(combinations(vertices, 2))
            if gamma_pairs is None
            else {pair(u, v) for u, v in gamma_pairs}
        )
        for u, v in sorted(selected_pairs):
            choices = tuple(w for w in vertices if w not in (u, v))
            cnf.add(*(witness[(u, v, w)] for w in choices))
            for w in choices:
                marker = witness[(u, v, w)]
                cnf.add(-marker, e(u, w))
                cnf.add(-marker, e(v, w))

    # Exact one-guard closure.  With an attack at an undominated vertex all
    # move-edge literals are false, so this also excludes nondominating
    # retained triples.
    for state in triples:
        selected = family[state]
        for attacked in vertices:
            if attacked in state:
                continue
            response_terms: list[tuple[int, int]] = []
            for guard in state:
                successor = tuple(
                    sorted((set(state) - {guard}) | {attacked})
                )
                response_terms.append(
                    (-e(guard, attacked), family[successor])
                )
            for chosen in product(*response_terms):
                cnf.add(-selected, *chosen)

    # Independent retained reference state.
    for u, v in combinations(S, 2):
        cnf.add(e(u, v))
    cnf.add(family[S])

    def direct_state(vertex: int, omitted: int) -> tuple[int, int, int]:
        return tuple(sorted((set(S) - {omitted}) | {vertex}))

    for vertex, response in LISTS.items():
        for omitted in S:
            marker = family[direct_state(vertex, omitted)]
            cnf.add(marker if omitted in response else -marker)

    # Literal induced complement P4.  Inducedness is stronger than needed
    # for the list obstruction but makes the physical template unambiguous.
    for u, v in ((3, 4), (4, 5), (5, 6)):
        cnf.add(e(u, v))
    for u, v in ((3, 5), (3, 6), (4, 6)):
        cnf.add(-e(u, v))

    return cnf, edge_h, family


def parse_model(path: Path, variable_count: int) -> set[int]:
    values: set[int] = set()
    for token in path.read_text(encoding="ascii").split():
        if token in {"v", "s", "SATISFIABLE", "UNSATISFIABLE"}:
            continue
        try:
            literal = int(token)
        except ValueError:
            continue
        if literal > 0:
            values.add(literal)
    if any(value > variable_count for value in values):
        raise ValueError("model contains out-of-range variable")
    return values


def graph6(order: int, h_edges: set[tuple[int, int]]) -> str:
    # graph6 stores G, so complement the H bits.
    bits = []
    for high in range(1, order):
        for low in range(high):
            bits.append(0 if (low, high) in h_edges else 1)
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for index in range(0, len(bits), 6):
        value = 0
        for bit in bits[index:index + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return chr(order + 63) + "".join(payload)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--instance", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--no-gamma", action="store_true")
    parser.add_argument(
        "--gamma-anchors",
        help="comma-separated vertices; constrain only pairs incident to one",
    )
    args = parser.parse_args()

    selected_pairs = None
    if args.gamma_anchors:
        gamma_anchors = {
            int(value) for value in args.gamma_anchors.split(",") if value
        }
        selected_pairs = {
            pair(u, v)
            for u, v in combinations(range(args.order), 2)
            if u in gamma_anchors or v in gamma_anchors
        }
    cnf, edge_h, family = build(
        args.order,
        enforce_gamma=not args.no_gamma,
        gamma_pairs=selected_pairs,
    )
    args.instance.write_text(cnf.dimacs(), encoding="ascii")
    command = [
        str(args.solver),
        "--quiet",
        "--binary=false",
        "-w",
        str(args.model),
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

    detail = ""
    if status == "SAT":
        true_variables = parse_model(args.model, len(cnf.names) - 1)
        h_set = {uv for uv, marker in edge_h.items() if marker in true_variables}
        retained = [
            state for state, marker in family.items() if marker in true_variables
        ]
        detail = (
            f" graph6={graph6(args.order, h_set)}"
            f" family_states={len(retained)}"
        )
    print(
        f"order={args.order} variables={len(cnf.names)-1}"
        f" clauses={len(cnf.clauses)} status={status}{detail}"
    )
    raise SystemExit(
        10 if status == "SAT"
        else 20 if status == "UNSAT"
        else 124 if status == "TIMEOUT"
        else 1
    )


if __name__ == "__main__":
    main()
