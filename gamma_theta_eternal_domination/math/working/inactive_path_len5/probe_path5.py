#!/usr/bin/env python3
"""Discovery probe for an inactive witnessed path.

The default formula uses length five.  It asks whether a one-guard eternal
triple-family can contain the named independent edge states, omit both
endpoint responses at a fixed target from each state, and also omit the
target state on the two endpoints of the path.  Witness vertices may
coincide according to a set partition.
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import subprocess
import tempfile
from pathlib import Path


RIM_PROBE = Path(__file__).parents[1] / "inactive_odd_cycle_generalization" / "probe.py"
SPEC = importlib.util.spec_from_file_location("inactive_rim_probe", RIM_PROBE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load the inactive-rim CNF helper")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
CNF = MODULE.CNF
restricted_growth_strings = MODULE.restricted_growth_strings


def build(partition: str) -> tuple[CNF, dict[str, object]]:
    path_length = len(partition)
    if path_length < 1:
        raise ValueError("path length must be positive")
    if partition not in set(restricted_growth_strings(path_length)):
        raise ValueError("partition must be a restricted-growth string")

    labels = tuple(map(int, partition))
    block_count = max(labels) + 1
    path_order = path_length + 1
    target = path_order + block_count
    vertices = tuple(range(target + 1))
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
            state_name = "_".join(map(str, state))
            cnf.group = f"domination_{state_name}__{attacked}"
            cnf.add(
                -family[state],
                -h(attacked, state[0]),
                -h(attacked, state[1]),
                -h(attacked, state[2]),
            )

            cnf.group = f"closure_{state_name}__{attacked}"
            choices: list[int] = []
            for guard in state:
                response = move[(state, attacked, guard)]
                successor = tuple(sorted((set(state) - {guard}) | {attacked}))
                choices.append(response)
                cnf.add(-response, -h(guard, attacked))
                cnf.add(-response, family[successor])
            cnf.add(-family[state], *choices)

    cnf.group = "induced_path"
    path_edges = {(index, index + 1) for index in range(path_length)}
    for pair in itertools.combinations(range(path_order), 2):
        cnf.add(h(*pair) if pair in path_edges else -h(*pair))

    witnesses: list[int] = []
    named_states: list[tuple[int, int, int]] = []
    forbidden_successors: list[tuple[int, int, int]] = []
    for index, label in enumerate(labels):
        witness = path_order + label
        witnesses.append(witness)
        named = tuple(sorted((index, index + 1, witness)))
        first = tuple(sorted((index + 1, witness, target)))
        second = tuple(sorted((index, witness, target)))
        named_states.append(named)
        forbidden_successors.extend((first, second))

        cnf.group = f"named_edge_{index}"
        cnf.add(h(index, witness))
        cnf.add(h(index + 1, witness))
        cnf.add(family[named])
        cnf.add(-family[first])
        cnf.add(-family[second])

    endpoint_state = tuple(sorted((0, path_length, target)))
    cnf.group = "forbidden_endpoint_state"
    cnf.add(-family[endpoint_state])

    return cnf, {
        "partition": partition,
        "path_length": path_length,
        "block_count": block_count,
        "order": len(vertices),
        "target": target,
        "witnesses": witnesses,
        "named_states": [list(state) for state in named_states],
        "forbidden_successors": [
            list(state) for state in forbidden_successors
        ],
        "forbidden_endpoint_state": list(endpoint_state),
        "variables": len(cnf.names) - 1,
        "clauses": len(cnf.clauses),
    }


def solve(cnf: CNF, solver: Path) -> bool:
    with tempfile.TemporaryDirectory(prefix="inactive-path5-") as temporary:
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
    parser.add_argument("--path-length", type=int, default=5)
    parser.add_argument("--partition")
    arguments = parser.parse_args()

    if arguments.partition is not None:
        partitions = (arguments.partition,)
    else:
        partitions = restricted_growth_strings(arguments.path_length)

    rows: list[dict[str, object]] = []
    for partition in partitions:
        cnf, metadata = build(partition)
        rows.append(
            {
                **metadata,
                "satisfiable": solve(cnf, arguments.solver.resolve()),
            }
        )

    result = {
        "schema": "inactive-witnessed-path5-probe-v1",
        "classification": "OBSERVED",
        "partition_count": len(rows),
        "satisfiable_count": sum(bool(row["satisfiable"]) for row in rows),
        "rows": rows,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
