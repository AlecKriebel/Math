#!/usr/bin/env python3
"""Test a two-edge endpoint-state recurrence in the inactive path gadget."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import subprocess
import tempfile
from pathlib import Path


PROBE_PATH = Path(__file__).with_name("probe.py")
SPEC = importlib.util.spec_from_file_location("inactive_rim_probe", PROBE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load probe.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
CNF = MODULE.CNF


def build(
    start_value: bool,
    end_value: bool,
) -> CNF:
    # a,b,c,d,p,q,x
    a, b, c, d, p, q, x = range(7)
    vertices = tuple(range(7))
    triples = tuple(itertools.combinations(vertices, 3))
    cnf = CNF()
    edge = {
        pair: cnf.variable(f"h_{pair[0]}_{pair[1]}")
        for pair in itertools.combinations(vertices, 2)
    }
    family = {
        state: cnf.variable("f_" + "_".join(map(str, state)))
        for state in triples
    }
    move = {
        (state, attacked, guard): cnf.variable(
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
        return edge[tuple(sorted((first, second)))]

    for state in triples:
        for attacked in vertices:
            if attacked in state:
                continue
            cnf.add(
                -family[state],
                -h(attacked, state[0]),
                -h(attacked, state[1]),
                -h(attacked, state[2]),
            )
    for state in triples:
        for attacked in vertices:
            if attacked in state:
                continue
            choices: list[int] = []
            for guard in state:
                response = move[(state, attacked, guard)]
                successor = tuple(sorted((set(state) - {guard}) | {attacked}))
                choices.append(response)
                cnf.add(-response, -h(guard, attacked))
                cnf.add(-response, family[successor])
            cnf.add(-family[state], *choices)

    for first, second in ((b, c), (c, d), (b, p), (c, p), (c, q), (d, q)):
        cnf.add(h(first, second))
    for first, second, witness in ((b, c, p), (c, d, q)):
        cnf.add(family[tuple(sorted((first, second, witness)))])
        cnf.add(-family[tuple(sorted((second, witness, x)))])
        cnf.add(-family[tuple(sorted((first, witness, x)))])

    start = family[tuple(sorted((a, b, x)))]
    end = family[tuple(sorted((a, d, x)))]
    cnf.add(start if start_value else -start)
    cnf.add(end if end_value else -end)
    return cnf


def solve(cnf: CNF, solver: Path) -> bool:
    with tempfile.TemporaryDirectory(prefix="inactive-recurrence-") as temporary:
        instance = Path(temporary) / "instance.cnf"
        instance.write_text(cnf.dimacs(), encoding="ascii")
        completed = subprocess.run(
            [str(solver), "-q", str(instance)],
            check=False,
            capture_output=True,
            text=True,
        )
    if completed.returncode not in (10, 20):
        raise RuntimeError(completed.stdout + completed.stderr)
    return completed.returncode == 10


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    arguments = parser.parse_args()
    rows = []
    for start, end in itertools.product((False, True), repeat=2):
        cnf = build(start, end)
        rows.append(
            {
                "start": start,
                "end": end,
                "satisfiable": solve(cnf, arguments.solver.resolve()),
                "variables": len(cnf.names) - 1,
                "clauses": len(cnf.clauses),
            }
        )
    result = {
        "schema": "inactive-two-edge-recurrence-probe-v1",
        "classification": "OBSERVED",
        "rows": rows,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
