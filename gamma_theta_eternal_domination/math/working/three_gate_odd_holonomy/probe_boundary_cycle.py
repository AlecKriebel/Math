#!/usr/bin/env python3
"""Exact discovery probe for cyclic tight-gate boundary geometries.

This is deliberately a boundary-state probe, not a certificate generator.
It encodes an arbitrary eternal family of triples directly from the
one-guard definition.  Vertices 0,1,2 are an independent retained anchor
state S.  A cyclic type word u_0,...,u_{r-1} gives one W_{u_i} connector
from gate i to gate i+1.  Gate i uses terminal types u_{i-1},u_i and a
physical cap of the third type.

Each gate has exact two-lists at its two terminals and cap, plus the three
literal complement incidences that make

    {third_type, left_terminal, right_terminal}

a dead boundary state.  This is weaker than a full virtual-rainbow gate:
it does not encode the original cross clause or its same-sign
physicalization paths.  Therefore UNSAT here would prove a stronger
attack theorem, while SAT is only a countercontrol to that stronger route.
"""

from __future__ import annotations

import argparse
from itertools import combinations, product
from pathlib import Path
import subprocess


S = (0, 1, 2)


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
    types: tuple[int, ...],
    lengths: tuple[int, ...],
    *,
    enforce_gamma: bool,
    spare_vertices: int,
    full_gates: bool = False,
    all_two_lists: bool = False,
) -> tuple[CNF, dict[str, object]]:
    r = len(types)
    if r < 3 or len(lengths) != r:
        raise ValueError("need equally many types/lengths and at least 3 gates")
    if any(u not in S for u in types):
        raise ValueError("types must be 0,1,2")
    if any(types[i - 1] == types[i] for i in range(r)):
        raise ValueError("successive connector types must differ")
    if any(length < 1 for length in lengths):
        raise ValueError("this probe uses distinct positive-length connectors")

    # For connector i, R_i is its start at gate i and L_{i+1} its end.
    next_vertex = 3
    right = tuple(range(next_vertex, next_vertex + r))
    next_vertex += r
    left = tuple(range(next_vertex, next_vertex + r))
    next_vertex += r
    cap = tuple(range(next_vertex, next_vertex + r))
    next_vertex += r
    if full_gates:
        original = tuple(range(next_vertex, next_vertex + r))
        next_vertex += r
        physicalization_middle = tuple(range(next_vertex, next_vertex + r))
        next_vertex += r
    else:
        original = ()
        physicalization_middle = ()
    interiors: list[tuple[int, ...]] = []
    for length in lengths:
        interior = tuple(range(next_vertex, next_vertex + length - 1))
        next_vertex += length - 1
        interiors.append(interior)
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
        # gamma(G) >= 3: every vertex pair has a common H-neighbor.
        for u, v in combinations(vertices, 2):
            choices = tuple(w for w in vertices if w not in (u, v))
            cnf.add(*(witness[(u, v, w)] for w in choices))
            for w in choices:
                marker = witness[(u, v, w)]
                cnf.add(-marker, e(u, w))
                cnf.add(-marker, e(v, w))

    # Exact one-guard closure, including domination of every retained state.
    for state in triples:
        selected = family[state]
        for attacked in vertices:
            if attacked in state:
                continue
            response_pairs: list[tuple[int, int]] = []
            for guard in state:
                successor = tuple(sorted((set(state) - {guard}) | {attacked}))
                response_pairs.append((-e(guard, attacked), family[successor]))
            for chosen in product(*response_pairs):
                cnf.add(-selected, *chosen)

    for u, v in combinations(S, 2):
        cnf.add(e(u, v))
    cnf.add(family[S])

    def direct_state(vertex: int, omitted: int) -> tuple[int, int, int]:
        return tuple(sorted((set(S) - {omitted}) | {vertex}))

    def exact_list(vertex: int, response: frozenset[int]) -> None:
        for omitted in S:
            selected = family[direct_state(vertex, omitted)]
            cnf.add(selected if omitted in response else -selected)

    # Each gate i has left terminal type types[i-1], right terminal type
    # types[i], and cap of the third type.
    thirds: list[int] = []
    h_edges: list[tuple[int, int]] = list(combinations(S, 2))
    g_edges: list[tuple[int, int]] = []
    boundaries: list[tuple[int, int, int]] = []
    for i in range(r):
        left_type = types[i - 1]
        right_type = types[i]
        third = ({0, 1, 2} - {left_type, right_type}).pop()
        thirds.append(third)
        exact_list(left[i], frozenset(set(S) - {left_type}))
        exact_list(right[i], frozenset(set(S) - {right_type}))
        exact_list(cap[i], frozenset(set(S) - {third}))
        h_edges.extend(
            (
                (left_type, left[i]),
                (right_type, right[i]),
                (third, cap[i]),
                (left[i], cap[i]),
                (right[i], cap[i]),
            )
        )
        for color in set(S) - {left_type}:
            g_edges.append((color, left[i]))
        for color in set(S) - {right_type}:
            g_edges.append((color, right[i]))
        for color in set(S) - {third}:
            g_edges.append((color, cap[i]))
        boundaries.append(tuple(sorted((third, left[i], right[i]))))
        if full_gates:
            # The left terminal is already physical.  The original clause
            # joins it to an original port of the right type.  A length-two
            # path in W_{right_type} identifies that original port with the
            # physical right terminal, while left-right is the failed
            # incidence repaired by the tight cap.
            exact_list(
                original[i],
                frozenset(set(S) - {right_type}),
            )
            cnf.add(
                -family[
                    direct_state(physicalization_middle[i], right_type)
                ]
            )
            h_edges.extend(
                (
                    (left[i], original[i]),
                    (original[i], physicalization_middle[i]),
                    (physicalization_middle[i], right[i]),
                )
            )
            g_edges.append((left[i], right[i]))

    paths: list[tuple[int, ...]] = []
    for i, (u, interior) in enumerate(zip(types, interiors, strict=True)):
        path = (right[i], *interior, left[(i + 1) % r])
        paths.append(path)
        for vertex in interior:
            cnf.add(-family[direct_state(vertex, u)])
        h_edges.extend(zip(path[:-1], path[1:], strict=True))

    if all_two_lists:
        for vertex in range(3, order):
            responses = tuple(
                family[direct_state(vertex, omitted)]
                for omitted in S
            )
            # Exactly two of the three direct response states.
            for omitted_pair in combinations(responses, 2):
                cnf.add(*omitted_pair)
            cnf.add(*(-literal for literal in responses))

    for u, v in h_edges:
        cnf.add(e(u, v))
    for u, v in g_edges:
        cnf.add(-e(u, v))

    metadata: dict[str, object] = {
        "order": order,
        "types": list(types),
        "lengths": list(lengths),
        "left": list(left),
        "right": list(right),
        "cap": list(cap),
        "original": list(original),
        "physicalization_middle": list(physicalization_middle),
        "thirds": thirds,
        "paths": [list(path) for path in paths],
        "boundaries": [list(state) for state in boundaries],
        "edge": edge,
        "family": family,
        "witness": witness,
    }
    return cnf, metadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--types", default="012")
    parser.add_argument("--lengths", default="1,1,1")
    parser.add_argument("--spare-vertices", type=int, default=0)
    parser.add_argument(
        "--full-gates",
        action="store_true",
        help="include an original clause and even physicalization path per gate",
    )
    parser.add_argument(
        "--all-two-lists",
        action="store_true",
        help="require every outside vertex to have an exact two-list",
    )
    parser.add_argument("--no-gamma", action="store_true")
    parser.add_argument(
        "--gamma-pair",
        action="append",
        help=(
            "when --no-gamma is used, require only this comma-separated "
            "pair to have a common H-neighbor; may be repeated"
        ),
    )
    parser.add_argument(
        "--force-common-h",
        action="append",
        help=(
            "comma-separated u,v,w: force w to be a common H-neighbor "
            "of u,v; may be repeated (discovery ablation)"
        ),
    )
    parser.add_argument(
        "--force-h",
        action="append",
        help="comma-separated H-edge; may be repeated (discovery ablation)",
    )
    parser.add_argument(
        "--force-g",
        action="append",
        help="comma-separated G-edge; may be repeated (discovery ablation)",
    )
    parser.add_argument(
        "--force-family",
        action="append",
        help="comma-separated triple forced into the family",
    )
    parser.add_argument(
        "--forbid-family",
        action="append",
        help="comma-separated triple forbidden from the family",
    )
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--instance", type=Path, required=True)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--model", type=Path)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()

    types = tuple(int(char) for char in args.types)
    lengths = tuple(int(piece) for piece in args.lengths.split(","))
    cnf, metadata = build(
        types,
        lengths,
        enforce_gamma=not args.no_gamma,
        spare_vertices=args.spare_vertices,
        full_gates=args.full_gates,
        all_two_lists=args.all_two_lists,
    )
    edge = metadata["edge"]
    witness = metadata["witness"]
    assert isinstance(edge, dict)
    assert isinstance(witness, dict)
    if args.no_gamma:
        order = int(metadata["order"])
        for selected_pair in args.gamma_pair or ():
            u, v = (int(piece) for piece in selected_pair.split(","))
            u, v = pair(u, v)
            choices = tuple(w for w in range(order) if w not in (u, v))
            cnf.add(*(witness[(u, v, w)] for w in choices))
            for w in choices:
                marker = witness[(u, v, w)]
                cnf.add(-marker, edge[pair(u, w)])
                cnf.add(-marker, edge[pair(v, w)])
    for forced in args.force_common_h or ():
        u, v, w = (int(piece) for piece in forced.split(","))
        cnf.add(edge[pair(u, w)])
        cnf.add(edge[pair(v, w)])
    for forced in args.force_h or ():
        u, v = (int(piece) for piece in forced.split(","))
        cnf.add(edge[pair(u, v)])
    for forced in args.force_g or ():
        u, v = (int(piece) for piece in forced.split(","))
        cnf.add(-edge[pair(u, v)])
    family = metadata["family"]
    assert isinstance(family, dict)
    for forced in args.force_family or ():
        state = tuple(sorted(int(piece) for piece in forced.split(",")))
        cnf.add(family[state])
    for forbidden in args.forbid_family or ():
        state = tuple(sorted(int(piece) for piece in forbidden.split(",")))
        cnf.add(-family[state])
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
        f"order={metadata['order']} variables={len(cnf.names)-1} "
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
