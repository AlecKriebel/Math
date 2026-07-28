#!/usr/bin/env python3
"""Discovery-only SAT probe for the two ud-edge bow-tie branches.

This deliberately drops the global gamma=3 condition except for the named
pair {u,d}.  SAT output is therefore only a sharp-boundary search and is
never a theorem or counterexample.
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument(
        "--bowtie",
        choices=("retained", "omitted"),
        required=True,
    )
    parser.add_argument("--drop-i", action="store_true")
    parser.add_argument(
        "--core-extensions",
        default="",
        help="comma-separated names ub,uc,pc,qb,rb,rc or all",
    )
    parser.add_argument(
        "--w-pattern",
        choices=("any", "b-only", "c-only", "both"),
        default="any",
    )
    parser.add_argument(
        "--core-states",
        default="",
        help="comma-separated Mp,Mq,U,R or all",
    )
    arguments = parser.parse_args()
    if arguments.order < 11:
        raise ValueError("labels u,x,p,q,r,b,c,d,w,s,t need order >= 11")

    collision = load_collision()
    cnf, metadata, base = collision.build(
        arguments.order,
        require_alpha=True,
        require_gamma=False,
        require_i=not arguments.drop_i,
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

    u, x, p, q, r, b, c, d, w, s, t = range(11)
    named_pairs = {
        "ub": (u, b),
        "uc": (u, c),
        "pc": (p, c),
        "qb": (q, b),
        "rb": (r, b),
        "rc": (r, c),
    }

    # d is an x,r completion and w is a fixed missed vertex for {u,d}.
    for left, right, present in (
        (d, x, False),
        (d, r, False),
        (d, p, True),
        (d, q, True),
        (d, b, True),
        (d, c, True),
        (u, d, True),
        (w, u, False),
        (w, d, False),
        (w, x, True),
        (w, r, True),
    ):
        force_edge(left, right, present)
    cnf.add(edge(w, b), edge(w, c))
    if arguments.w_pattern != "any":
        force_edge(w, b, arguments.w_pattern in ("b-only", "both"))
        force_edge(w, c, arguments.w_pattern in ("c-only", "both"))

    # s completes {u,w}; t completes {d,w}.
    for left, right, present in (
        (s, u, False),
        (s, w, False),
        (s, d, True),
        (t, d, False),
        (t, w, False),
        (t, u, True),
    ):
        force_edge(left, right, present)

    retained = (
        {x, r, d},
        {u, x, d},
        {u, d, w},
        {x, d, w},
        {r, d, w},
        {u, w, s},
        {d, w, t},
    )
    for state in retained:
        cnf.add(family(state))
    core_states = {
        "Mp": {x, b, q},
        "Mq": {x, p, c},
        "U": {u, b, c},
        "R": {r, b, c},
    }
    requested_states = {
        name
        for name in arguments.core_states.split(",")
        if name
    }
    if "all" in requested_states:
        requested_states = set(core_states)
    if not requested_states <= set(core_states):
        raise ValueError(f"unknown core states: {sorted(requested_states)}")
    for name in requested_states:
        cnf.add(family(core_states[name]))
    cnf.add(-family({u, r, d}))
    mixed = family({s, w, t})
    cnf.add(mixed if arguments.bowtie == "retained" else -mixed)

    requested = {
        name
        for name in arguments.core_extensions.split(",")
        if name
    }
    if "all" in requested:
        requested = set(named_pairs)
    if not requested <= set(named_pairs):
        raise ValueError(f"unknown extension names: {sorted(requested)}")
    for name in sorted(requested):
        left, right = named_pairs[name]
        selectors = []
        for third in range(arguments.order):
            if third in (left, right):
                continue
            selector = cnf.variable(f"named-extend:{name}:{third}")
            selectors.append(selector)
            cnf.add(-selector, -edge(left, third))
            cnf.add(-selector, -edge(right, third))
        cnf.add(*selectors)

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
        "schema": "QQ1-hot-bowtie-discovery-v1",
        "classification": "OBSERVED_DISCOVERY_ONLY",
        "order": arguments.order,
        "bowtie": arguments.bowtie,
        "core_extensions": sorted(requested),
        "core_states": sorted(requested_states),
        "w_pattern": arguments.w_pattern,
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
