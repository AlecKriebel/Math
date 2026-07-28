#!/usr/bin/env python3
"""Discovery probe for the witness-free inactive-path parity statement.

The finite template consists only of an induced complement path
``r_0 ... r_m`` and a target ``x``.  It encodes an arbitrary family of
dominating triples, literal one-guard closure at template attacks, all
retained edge states ``{r_i,r_{i+1},x}``, and all absent distance-two
states ``{r_i,r_{i+2},x}``.  It then tests the endpoint state.

This is exploration code.  Solver output alone is not a theorem.
"""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
import tempfile
from pathlib import Path


class CNF:
    def __init__(self) -> None:
        self.names = [""]
        self.name_to_variable: dict[str, int] = {}
        self.clauses: list[tuple[int, ...]] = []

    def variable(self, name: str) -> int:
        if name not in self.name_to_variable:
            self.name_to_variable[name] = len(self.names)
            self.names.append(name)
        return self.name_to_variable[name]

    def add(self, *literals: int) -> None:
        if not literals or any(literal == 0 for literal in literals):
            raise ValueError("bad clause")
        self.clauses.append(tuple(literals))

    def dimacs(self) -> str:
        rows = [f"p cnf {len(self.names) - 1} {len(self.clauses)}"]
        rows.extend(" ".join(map(str, row)) + " 0" for row in self.clauses)
        return "\n".join(rows) + "\n"


def build(
    path_edges: int,
    wrong_endpoint_value: bool,
    witness_partition: tuple[int, ...] | None,
    rim_attacks_only: bool = False,
) -> CNF:
    if path_edges < 2:
        raise ValueError("need at least two path edges")
    rim_order = path_edges + 1
    witness_order = (
        max(witness_partition) + 1 if witness_partition is not None else 0
    )
    target = rim_order + witness_order
    vertices = tuple(range(target + 1))
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
            if rim_attacks_only and attacked >= rim_order and attacked != target:
                continue
            choices = []
            for guard in state:
                move = moves[(state, attacked, guard)]
                successor = tuple(sorted((set(state) - {guard}) | {attacked}))
                choices.append(move)
                cnf.add(-move, -edge(guard, attacked))
                cnf.add(-move, family[successor])
            cnf.add(-family[state], *choices)

    rim = tuple(range(path_edges + 1))
    path_pairs = {(index, index + 1) for index in range(path_edges)}
    for pair in itertools.combinations(rim, 2):
        cnf.add(edge(*pair) if pair in path_pairs else -edge(*pair))

    for index in range(path_edges):
        cnf.add(family[tuple(sorted((index, index + 1, target)))])
    for index in range(path_edges - 1):
        cnf.add(-family[tuple(sorted((index, index + 2, target)))])

    if witness_partition is not None:
        for index, witness_label in enumerate(witness_partition):
            witness = rim_order + witness_label
            cnf.add(edge(index, witness))
            cnf.add(edge(index + 1, witness))
            cnf.add(family[tuple(sorted((index, index + 1, witness)))])
            cnf.add(-family[tuple(sorted((index, witness, target)))])
            cnf.add(-family[tuple(sorted((index + 1, witness, target)))])

    endpoint = family[tuple(sorted((0, path_edges, target)))]
    cnf.add(endpoint if wrong_endpoint_value else -endpoint)
    return cnf


def solve(cnf: CNF, solver: Path) -> bool:
    with tempfile.TemporaryDirectory(prefix="inactive-path-") as temporary:
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
    parser.add_argument("--max-edges", type=int, default=10)
    parser.add_argument("--with-distinct-witnesses", action="store_true")
    parser.add_argument("--all-witness-partitions", action="store_true")
    parser.add_argument("--rim-attacks-only", action="store_true")
    arguments = parser.parse_args()
    rows = []
    for path_edges in range(2, arguments.max_edges + 1):
        expected = path_edges % 2 == 1
        partitions: list[tuple[int, ...] | None]
        if arguments.all_witness_partitions:
            partitions = []

            def visit(prefix: tuple[int, ...], maximum: int) -> None:
                if len(prefix) == path_edges:
                    partitions.append(prefix)
                    return
                for value in range(maximum + 2):
                    visit(prefix + (value,), max(maximum, value))

            visit((0,), 0)
        elif arguments.with_distinct_witnesses:
            partitions = [tuple(range(path_edges))]
        else:
            partitions = [None]
        for partition in partitions:
            cnf = build(
                path_edges,
                not expected,
                partition,
                arguments.rim_attacks_only,
            )
            row = {
                "path_edges": path_edges,
                "expected_endpoint_membership": expected,
                "wrong_endpoint_is_satisfiable": solve(
                    cnf, arguments.solver.resolve()
                ),
                "witness_partition": partition,
                "rim_attacks_only": arguments.rim_attacks_only,
                "variables": len(cnf.names) - 1,
                "clauses": len(cnf.clauses),
            }
            rows.append(row)
            print(json.dumps(row, sort_keys=True), flush=True)
            if row["wrong_endpoint_is_satisfiable"]:
                break
    print(
        json.dumps(
            {
                "classification": "OBSERVED",
                "rows": rows,
                "schema": "inactive-witness-free-path-parity-probe-v1",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
