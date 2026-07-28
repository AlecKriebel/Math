#!/usr/bin/env python3
"""Discovery-only SAT probe for the rank-one QQ1 collision normal form.

The labels are

    u=0, x=1, p=2, q=3, r=4, b=5, c=6.

Here x itself is the private witness for the non-dominating successor
{r,p,q}; b and c are the private witnesses for {u,r,q} and {u,p,r}.
The encoding is literal but its UNSAT outputs are not certificates.
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import subprocess
from pathlib import Path


LABELS = {"u": 0, "x": 1, "p": 2, "q": 3, "r": 4, "b": 5, "c": 6}


def load_base(path: Path):
    spec = importlib.util.spec_from_file_location("rank_one_base", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build(
    order: int,
    *,
    require_alpha: bool,
    require_gamma: bool,
    require_i: bool,
    required_pairs: tuple[tuple[int, int], ...] = (),
):
    base_path = (
        Path(__file__).parents[1]
        / "rank_one_remaining_endgame"
        / "probe_cases.py"
    )
    base = load_base(base_path)
    if order < len(LABELS):
        raise ValueError("collision normal form needs at least seven vertices")

    vertices = tuple(range(order))
    triples = tuple(itertools.combinations(vertices, 3))
    triple_index = {triple: index for index, triple in enumerate(triples)}
    cnf = base.CNF()

    def edge(left: int, right: int) -> int:
        left, right = sorted((left, right))
        return cnf.variable(f"e:{left}:{right}")

    def family(state) -> int:
        triple = tuple(sorted(state))
        return cnf.variable(f"f:{triple_index[triple]}")

    def force_edge(left: int, right: int, present: bool) -> None:
        literal = edge(left, right)
        cnf.add(literal if present else -literal)

    u, x, p, q, r, b, c = (LABELS[name] for name in LABELS)

    # T={x,p,q} is independent; QQ1 root and private witnesses.
    for left, right in itertools.combinations((x, p, q), 2):
        force_edge(left, right, False)
    for left, right in ((u, x), (u, r), (p, r), (q, r), (p, b), (q, c)):
        force_edge(left, right, True)
    for left, right in (
        (x, r),
        (b, u),
        (b, r),
        (b, q),
        (c, u),
        (c, r),
        (c, p),
    ):
        force_edge(left, right, False)

    # Accepted saturation of the collision normal form.
    for left, right in ((x, b), (x, c), (b, c), (u, p), (u, q)):
        force_edge(left, right, True)

    t_state = {x, p, q}
    b_state = {u, p, q}
    cnf.add(family(t_state))
    cnf.add(-family(b_state))

    # A witness for u▷x: every independent completion of {u,b} has its
    # u->x successor retained.  This is stronger syntactically than one
    # selector but equivalent under C-108 and i>=3.
    for z in vertices:
        if z in (u, x, b):
            continue
        cnf.add(edge(u, z), edge(b, z), family({x, b, z}))

    # Literal one-guard family: retained states dominate and answer every
    # unoccupied attack by one guard along one edge.
    for state in triples:
        occupied = set(state)
        f_state = family(state)
        for target in vertices:
            if target in occupied:
                continue
            cnf.add(-f_state, *(edge(guard, target) for guard in state))
            responses = []
            for guard in state:
                successor = occupied - {guard} | {target}
                response = cnf.variable(
                    f"move:{triple_index[state]}:{target}:{guard}"
                )
                responses.append(response)
                cnf.add(-response, edge(guard, target))
                cnf.add(-response, family(successor))
            cnf.add(-f_state, *responses)

    if require_alpha:
        for four in itertools.combinations(vertices, 4):
            cnf.add(*(edge(*pair) for pair in itertools.combinations(four, 2)))

    pair_constraints = (
        tuple(itertools.combinations(vertices, 2))
        if require_gamma
        else required_pairs
    )
    for left, right in pair_constraints:
        selectors = []
        for missed in vertices:
            if missed in (left, right):
                continue
            selector = cnf.variable(f"miss:{left}:{right}:{missed}")
            selectors.append(selector)
            cnf.add(-selector, -edge(left, missed))
            cnf.add(-selector, -edge(right, missed))
        cnf.add(*selectors)

    if require_i:
        for left, right in itertools.combinations(vertices, 2):
            selectors = []
            for third in vertices:
                if third in (left, right):
                    continue
                selector = cnf.variable(f"extend:{left}:{right}:{third}")
                selectors.append(selector)
                cnf.add(-selector, -edge(left, third))
                cnf.add(-selector, -edge(right, third))
            cnf.add(edge(left, right), *selectors)

    # B dominates; its three r-successors are non-dominating via x,b,c.
    for target in vertices:
        if target not in b_state:
            cnf.add(*(edge(guard, target) for guard in b_state))

    metadata = {
        "labels": LABELS,
        "edge_variables": {
            name: number
            for name, number in cnf.by_name.items()
            if name.startswith("e:")
        },
        "family_variables": {
            name: number
            for name, number in cnf.by_name.items()
            if name.startswith("f:")
        },
        "triples": triples,
    }
    return cnf, metadata, base


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--drop-alpha", action="store_true")
    parser.add_argument("--drop-gamma", action="store_true")
    parser.add_argument("--require-i", action="store_true")
    arguments = parser.parse_args()

    cnf, metadata, base = build(
        arguments.order,
        require_alpha=not arguments.drop_alpha,
        require_gamma=not arguments.drop_gamma,
        require_i=arguments.require_i,
    )
    cnf.write(arguments.cnf)
    completed = subprocess.run(
        [str(arguments.solver), str(arguments.cnf)],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    status, positive = base.parse_model(completed.stdout)
    result = {
        "schema": "rank-one-QQ1-collision-probe-v1",
        "classification": "OBSERVED_DISCOVERY_ONLY",
        "order": arguments.order,
        "status": status,
        "variables": cnf.next_variable - 1,
        "clauses": len(cnf.clauses),
    }
    if status == "SAT":
        result["edges"] = [
            list(map(int, name.split(":")[1:]))
            for name, number in metadata["edge_variables"].items()
            if number in positive
        ]
    arguments.result.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
