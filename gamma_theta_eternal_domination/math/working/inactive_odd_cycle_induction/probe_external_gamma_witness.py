#!/usr/bin/env python3
"""Sound local probe adding one external witness to a nondominating pair."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import subprocess
import tempfile
from pathlib import Path


PATH_PROBE = Path(__file__).with_name("probe_path.py")
SPEC = importlib.util.spec_from_file_location("path_probe", PATH_PROBE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot import probe_path.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
CNF = MODULE.CNF


def build(
    start_value: bool,
    witnessed_pair: tuple[int, int],
    equality_collapse: bool,
) -> CNF:
    a, b, c, d, p, q, x, z = range(8)
    vertices = tuple(range(8))
    triples = tuple(itertools.combinations(vertices, 3))
    cnf = CNF()
    h = {
        pair: cnf.variable(f"h_{pair[0]}_{pair[1]}")
        for pair in itertools.combinations(vertices, 2)
    }
    family = {
        state: cnf.variable("f_" + "_".join(map(str, state)))
        for state in triples
    }
    moves = {
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

    def edge(first: int, second: int) -> int:
        return h[tuple(sorted((first, second)))]

    for state in triples:
        for attacked in vertices:
            if attacked not in state:
                cnf.add(
                    -family[state],
                    -edge(attacked, state[0]),
                    -edge(attacked, state[1]),
                    -edge(attacked, state[2]),
                )
    for state in triples:
        for attacked in vertices:
            if attacked in state:
                continue
            choices = []
            for guard in state:
                move = moves[(state, attacked, guard)]
                successor = tuple(sorted((set(state) - {guard}) | {attacked}))
                choices.append(move)
                cnf.add(-move, -edge(guard, attacked))
                cnf.add(-move, family[successor])
            cnf.add(-family[state], *choices)

    cnf.add(edge(b, c))
    cnf.add(edge(c, d))
    for first, second, witness in ((b, c, p), (c, d, q)):
        cnf.add(edge(first, witness))
        cnf.add(edge(second, witness))
        cnf.add(family[tuple(sorted((first, second, witness)))])
        cnf.add(-family[tuple(sorted((first, witness, x)))])
        cnf.add(-family[tuple(sorted((second, witness, x)))])

    cnf.add(edge(z, witnessed_pair[0]))
    cnf.add(edge(z, witnessed_pair[1]))
    if equality_collapse:
        for group in itertools.combinations(vertices, 4):
            cnf.add(
                *(
                    -edge(first, second)
                    for first, second in itertools.combinations(group, 2)
                )
            )
        for state in triples:
            cnf.add(
                *(
                    -edge(first, second)
                    for first, second in itertools.combinations(state, 2)
                ),
                family[state],
            )
    start = family[tuple(sorted((a, b, x)))]
    end = family[tuple(sorted((a, d, x)))]
    cnf.add(start if start_value else -start)
    cnf.add(-end if start_value else end)
    return cnf


def solve(cnf: CNF, solver: Path) -> bool:
    with tempfile.TemporaryDirectory(prefix="external-gamma-witness-") as temporary:
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
    parser.add_argument("--solver", required=True, type=Path)
    parser.add_argument("--equality-collapse", action="store_true")
    arguments = parser.parse_args()
    rows = []
    for pair in itertools.combinations(range(7), 2):
        for start_value in (False, True):
            cnf = build(start_value, pair, arguments.equality_collapse)
            rows.append(
                {
                    "witnessed_pair": pair,
                    "start_value": start_value,
                    "equality_collapse": arguments.equality_collapse,
                    "opposite_end_value_satisfiable": solve(
                        cnf, arguments.solver.resolve()
                    ),
                }
            )
    print(
        json.dumps(
            {
                "classification": "OBSERVED",
                "rows": rows,
                "schema": "inactive-external-gamma-witness-probe-v1",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
