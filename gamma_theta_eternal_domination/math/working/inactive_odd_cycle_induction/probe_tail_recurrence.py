#!/usr/bin/env python3
"""Discovery probe for a three-edge tail parity recurrence."""

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


def build(start_value: bool, partition: tuple[int, ...]) -> CNF:
    # anchor a; induced tail u_0...u_t; witnesses indexed by partition; target x
    a = 0
    tail = tuple(range(1, len(partition) + 2))
    witness_start = len(tail) + 1
    x = witness_start + max(partition) + 1
    vertices = tuple(range(x + 1))
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

    tail_edges = set(zip(tail, tail[1:]))
    for pair in itertools.combinations(tail, 2):
        cnf.add(edge(*pair) if pair in tail_edges else -edge(*pair))
    for tail_vertex in tail:
        cnf.add(-edge(a, tail_vertex))

    for (first, second), label in zip(zip(tail, tail[1:]), partition):
        witness = witness_start + label
        cnf.add(edge(first, witness))
        cnf.add(edge(second, witness))
        cnf.add(family[tuple(sorted((first, second, witness)))])
        cnf.add(-family[tuple(sorted((first, witness, x)))])
        cnf.add(-family[tuple(sorted((second, witness, x)))])

    values = [
        start_value if index % 2 == 0 else not start_value
        for index in range(len(tail))
    ]
    # Force the final value to repeat its predecessor instead of alternating.
    values[-1] = values[-2]
    for tail_vertex, value in zip(tail, values):
        state = family[tuple(sorted((a, tail_vertex, x)))]
        cnf.add(state if value else -state)
    return cnf


def solve(cnf: CNF, solver: Path) -> bool:
    with tempfile.TemporaryDirectory(prefix="inactive-tail-") as temporary:
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
    parser.add_argument("--tail-edges", type=int, default=3)
    arguments = parser.parse_args()
    partitions: list[tuple[int, ...]] = []

    def visit(prefix: tuple[int, ...], maximum: int) -> None:
        if len(prefix) == arguments.tail_edges:
            partitions.append(prefix)
            return
        for value in range(maximum + 2):
            visit(prefix + (value,), max(maximum, value))

    visit((0,), 0)
    rows = []
    for partition, start_value in itertools.product(partitions, (False, True)):
        cnf = build(start_value, partition)
        rows.append(
            {
                "partition": partition,
                "tail_edges": arguments.tail_edges,
                "start_value": start_value,
                "wrong_tail_pattern_satisfiable": solve(
                    cnf, arguments.solver.resolve()
                ),
                "variables": len(cnf.names) - 1,
                "clauses": len(cnf.clauses),
            }
        )
    print(
        json.dumps(
            {
                "classification": "OBSERVED",
                "rows": rows,
                "schema": "inactive-three-edge-tail-recurrence-probe-v1",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
