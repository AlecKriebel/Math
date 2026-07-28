#!/usr/bin/env python3
"""Discovery-only probe for simultaneous QQ1 pair witnesses.

The canonical QQ1 labels are

    u,x,p,q,r,b,c,d,w,z = 0,...,9.

Here d completes the independent pair {x,r}, w misses {u,d}, and z
misses {u,x}.  The probe keeps only selected global pair-nondomination
constraints.  SAT models are controls; UNSAT outputs have no certificate
and are not mathematical claims.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
from pathlib import Path


def load_collision():
    path = (
        Path(__file__).parents[1]
        / "rank_one_ur1_pair_core"
        / "probe_collision.py"
    )
    spec = importlib.util.spec_from_file_location("collision_probe", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_pair(text: str, labels: dict[str, int]) -> tuple[int, int]:
    left, right = text.split("-")
    def decode(token: str) -> int:
        return labels[token] if token in labels else int(token)

    return tuple(sorted((decode(left), decode(right))))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--ud", choices=("edge", "nonedge"), required=True)
    parser.add_argument(
        "--zw",
        choices=("any", "edge", "nonedge"),
        default="any",
    )
    parser.add_argument(
        "--pairs",
        default="u-x",
        help="comma-separated named pair-nondomination constraints",
    )
    parser.add_argument("--full-gamma", action="store_true")
    parser.add_argument("--drop-i", action="store_true")
    arguments = parser.parse_args()
    if arguments.order < 10:
        raise ValueError("ten named labels require order at least ten")

    collision = load_collision()
    labels = dict(collision.LABELS)
    labels.update({"d": 7, "w": 8, "z": 9})
    required_pairs = tuple(
        parse_pair(text, labels)
        for text in arguments.pairs.split(",")
        if text
    )
    cnf, metadata, base = collision.build(
        arguments.order,
        require_alpha=True,
        require_gamma=arguments.full_gamma,
        require_i=not arguments.drop_i,
        required_pairs=required_pairs,
    )

    def edge(left: int, right: int) -> int:
        left, right = sorted((left, right))
        return cnf.variable(f"e:{left}:{right}")

    def family(state) -> int:
        triple = tuple(sorted(state))
        index = metadata["triples"].index(triple)
        return cnf.variable(f"f:{index}")

    def force_edge(left: int, right: int, present: bool) -> None:
        literal = edge(left, right)
        cnf.add(literal if present else -literal)

    u, x, p, q, r, b, c, d, w, z = range(10)

    # The accepted completion and hot-layer incidence.
    for left, right, present in (
        (d, x, False),
        (d, r, False),
        (d, p, True),
        (d, q, True),
        (d, b, True),
        (d, c, True),
        (u, d, arguments.ud == "edge"),
        (w, u, False),
        (w, d, False),
        (w, x, True),
        (w, r, True),
        (z, u, False),
        (z, x, False),
        (z, d, True),
    ):
        force_edge(left, right, present)
    if arguments.zw != "any":
        force_edge(z, w, arguments.zw == "edge")
    cnf.add(edge(w, b), edge(w, c))
    cnf.add(edge(z, p), edge(z, q))
    cnf.add(edge(z, b), edge(z, c))

    # Named states proved before the outer-completion theorem.  U and R
    # are accepted C-158 states; A,K,E,F are the new candidate states.
    retained = (
        {u, b, c},
        {r, b, c},
        {x, r, d},
        {u, x, d},
        {u, d, w},
        {x, d, w},
        {r, d, w},
    )
    for state in retained:
        cnf.add(family(state))
    cnf.add(-family({u, r, d}))

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
        "schema": "QQ1-simultaneous-witness-discovery-v1",
        "classification": "OBSERVED_DISCOVERY_ONLY",
        "order": arguments.order,
        "ud": arguments.ud,
        "zw": arguments.zw,
        "pair_constraints": [
            [left, right] for left, right in required_pairs
        ],
        "full_gamma": arguments.full_gamma,
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
    print(json.dumps({key: result[key] for key in result if key != "edges"}))


if __name__ == "__main__":
    main()
