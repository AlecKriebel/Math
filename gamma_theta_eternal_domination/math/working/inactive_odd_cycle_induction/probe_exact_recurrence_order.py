#!/usr/bin/env python3
"""Direct exact-equality synthesis for a scalar recurrence countercontrol."""

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
    order: int,
    start_value: bool,
    gamma_pairs: frozenset[tuple[int, int]] = frozenset(),
) -> CNF:
    if order < 7:
        raise ValueError("order must be at least seven")
    a, b, c, d, p, q, x = range(7)
    vertices = tuple(range(order))
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

    # Exact equality collapse: omega(H)=3, no dominating pair in G, and
    # every maximum independent triple is retained.
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
    for first, second in itertools.combinations(vertices, 2):
        if gamma_pairs and (first, second) not in gamma_pairs:
            continue
        choices = []
        for witness in vertices:
            if witness in (first, second):
                continue
            indicator = cnf.variable(f"c_{first}_{second}__{witness}")
            choices.append(indicator)
            cnf.add(-indicator, edge(first, witness))
            cnf.add(-indicator, edge(second, witness))
        cnf.add(*choices)

    cnf.add(edge(b, c))
    cnf.add(edge(c, d))
    cnf.add(-edge(b, d))
    cnf.add(edge(a, x))
    for first, second, witness in ((b, c, p), (c, d, q)):
        cnf.add(edge(first, witness))
        cnf.add(edge(second, witness))
        cnf.add(family[tuple(sorted((first, second, witness)))])
        cnf.add(-family[tuple(sorted((first, witness, x)))])
        cnf.add(-family[tuple(sorted((second, witness, x)))])

    start = family[tuple(sorted((a, b, x)))]
    end = family[tuple(sorted((a, d, x)))]
    cnf.add(start if start_value else -start)
    cnf.add(-end if start_value else end)
    return cnf


def solve(cnf: CNF, solver: Path) -> bool:
    with tempfile.TemporaryDirectory(prefix="exact-recurrence-") as temporary:
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
    parser.add_argument("--max-order", type=int, default=10)
    parser.add_argument(
        "--only-gamma-pair",
        action="append",
        default=[],
        help="comma-separated pair; omit for all pairs",
    )
    arguments = parser.parse_args()
    rows = []
    for order in range(7, arguments.max_order + 1):
        for start_value in (False, True):
            cnf = build(
                order,
                start_value,
                frozenset(
                    tuple(sorted(map(int, pair.split(","))))
                    for pair in arguments.only_gamma_pair
                ),
            )
            row = {
                "order": order,
                "start_value": start_value,
                "countercontrol_satisfiable": solve(
                    cnf, arguments.solver.resolve()
                ),
                "variables": len(cnf.names) - 1,
                "clauses": len(cnf.clauses),
                "gamma_pairs": arguments.only_gamma_pair or "all",
            }
            rows.append(row)
            print(json.dumps(row, sort_keys=True), flush=True)
    print(
        json.dumps(
            {
                "classification": "OBSERVED",
                "rows": rows,
                "schema": "exact-equality-scalar-recurrence-order-probe-v1",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
