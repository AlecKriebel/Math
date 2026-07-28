#!/usr/bin/env python3
"""Probe the inactive-rim local template at arbitrary cycle length.

This is discovery code.  It generalizes the C5 certificate formula to an
induced cycle of user-selected length and can additionally impose
``gamma(G) >= 3`` by requiring every vertex pair to have a common
H-neighbor, where H is the complement of G.
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
        self.names: list[str] = [""]
        self.by_name: dict[str, int] = {}
        self.clauses: list[tuple[int, ...]] = []
        self.groups: list[str] = []
        self.group = "unclassified"

    def variable(self, name: str) -> int:
        if name in self.by_name:
            return self.by_name[name]
        result = len(self.names)
        self.names.append(name)
        self.by_name[name] = result
        return result

    def add(self, *literals: int) -> None:
        if not literals or any(literal == 0 for literal in literals):
            raise ValueError("invalid clause")
        self.clauses.append(tuple(literals))
        self.groups.append(self.group)

    def dimacs(self) -> str:
        rows = [f"p cnf {len(self.names) - 1} {len(self.clauses)}"]
        rows.extend(" ".join(map(str, clause)) + " 0" for clause in self.clauses)
        return "\n".join(rows) + "\n"


def restricted_growth_strings(length: int):
    def visit(prefix: tuple[int, ...], maximum: int):
        if len(prefix) == length:
            yield "".join(map(str, prefix))
            return
        for value in range(maximum + 2):
            yield from visit(prefix + (value,), max(maximum, value))

    yield from visit((0,), 0)


def build(
    cycle_length: int,
    partition: str,
    gamma_at_least_three: bool,
    allowed_forbidden_indices: frozenset[int] = frozenset(),
    forced_family_states: tuple[tuple[int, int, int], ...] = (),
    forbidden_family_states: tuple[tuple[int, int, int], ...] = (),
) -> tuple[CNF, dict[str, object]]:
    if cycle_length < 4:
        raise ValueError("cycle length must be at least four")
    if partition not in set(restricted_growth_strings(cycle_length)):
        raise ValueError("partition is not a restricted-growth string")

    labels = tuple(map(int, partition))
    block_count = max(labels) + 1
    n = cycle_length + block_count + 1
    rim = tuple(range(cycle_length))
    target = n - 1
    vertices = tuple(range(n))
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

    # Every retained state dominates the whole finite graph G.
    cnf.group = "domination"
    for state in triples:
        for attacked in vertices:
            if attacked not in state:
                cnf.group = (
                    "domination_"
                    + "_".join(map(str, state))
                    + f"__{attacked}"
                )
                cnf.add(
                    -family[state],
                    -h(attacked, state[0]),
                    -h(attacked, state[1]),
                    -h(attacked, state[2]),
                )

    # Literal one-guard closure at every unoccupied attack.
    cnf.group = "closure"
    for state in triples:
        for attacked in vertices:
            if attacked in state:
                continue
            cnf.group = (
                "closure_"
                + "_".join(map(str, state))
                + f"__{attacked}"
            )
            choices: list[int] = []
            for guard in state:
                response = move[(state, attacked, guard)]
                successor = tuple(sorted((set(state) - {guard}) | {attacked}))
                choices.append(response)
                cnf.add(-response, -h(guard, attacked))
                cnf.add(-response, family[successor])
            cnf.add(-family[state], *choices)

    # The rim induces exactly C_m in H.
    cnf.group = "induced_rim"
    rim_edges = {
        tuple(sorted((index, (index + 1) % cycle_length)))
        for index in rim
    }
    for pair in itertools.combinations(rim, 2):
        cnf.add(h(*pair) if pair in rim_edges else -h(*pair))

    witness_vertices: list[int] = []
    named_states: list[tuple[int, int, int]] = []
    forbidden_successors: list[tuple[int, int, int]] = []
    for index, label in enumerate(labels):
        cnf.group = f"named_edge_{index}"
        witness = cycle_length + label
        following = (index + 1) % cycle_length
        witness_vertices.append(witness)
        named = tuple(sorted((index, following, witness)))
        successor_first = tuple(sorted((following, witness, target)))
        successor_second = tuple(sorted((index, witness, target)))
        named_states.append(named)
        forbidden_successors.extend((successor_first, successor_second))
        cnf.add(h(index, witness))
        cnf.add(h(following, witness))
        cnf.add(family[named])
        first_constraint_index = 2 * index
        second_constraint_index = first_constraint_index + 1
        if first_constraint_index not in allowed_forbidden_indices:
            cnf.add(-family[successor_first])
        if second_constraint_index not in allowed_forbidden_indices:
            cnf.add(-family[successor_second])

    # gamma(G) >= 3 iff no pair dominates G.  In complement language every
    # pair has a common outside H-neighbor.
    common_neighbor = {}
    if gamma_at_least_three:
        cnf.group = "gamma_at_least_three"
        for first, second in itertools.combinations(vertices, 2):
            choices: list[int] = []
            for witness in vertices:
                if witness in (first, second):
                    continue
                indicator = cnf.variable(f"c_{first}_{second}__{witness}")
                common_neighbor[(first, second, witness)] = indicator
                choices.append(indicator)
                cnf.add(-indicator, h(first, witness))
                cnf.add(-indicator, h(second, witness))
            cnf.add(*choices)

    cnf.group = "forced_family_state"
    for state in forced_family_states:
        normalized = tuple(sorted(state))
        if normalized not in family:
            raise ValueError(f"invalid forced family state {state}")
        cnf.add(family[normalized])
    for state in forbidden_family_states:
        normalized = tuple(sorted(state))
        if normalized not in family:
            raise ValueError(f"invalid forbidden family state {state}")
        cnf.add(-family[normalized])

    metadata = {
        "cycle_length": cycle_length,
        "partition": partition,
        "block_count": block_count,
        "order": n,
        "target": target,
        "witness_vertices": witness_vertices,
        "named_states": named_states,
        "forbidden_successors": forbidden_successors,
        "gamma_at_least_three": gamma_at_least_three,
        "allowed_forbidden_indices": sorted(allowed_forbidden_indices),
        "forced_family_states": [list(state) for state in forced_family_states],
        "forbidden_family_states": [
            list(state) for state in forbidden_family_states
        ],
        "variables": len(cnf.names) - 1,
        "clauses": len(cnf.clauses),
    }
    return cnf, metadata


def solve(cnf: CNF, solver: Path) -> tuple[bool, set[int], str]:
    with tempfile.TemporaryDirectory(prefix="inactive-odd-rim-") as temporary:
        instance = Path(temporary) / "instance.cnf"
        instance.write_text(cnf.dimacs(), encoding="ascii")
        completed = subprocess.run(
            [str(solver), "-q", str(instance)],
            check=False,
            capture_output=True,
            text=True,
        )
    output = completed.stdout + completed.stderr
    if completed.returncode == 20:
        return False, set(), output
    if completed.returncode != 10:
        raise RuntimeError(
            f"solver returned {completed.returncode}\n{output}"
        )
    values: set[int] = set()
    for line in output.splitlines():
        if line.startswith("v "):
            values.update(
                literal
                for literal in map(int, line.split()[1:])
                if literal > 0
            )
    return True, values, output


def model_record(
    cnf: CNF,
    metadata: dict[str, object],
    values: set[int],
) -> dict[str, object]:
    true_names = {
        cnf.names[variable]
        for variable in values
        if 0 < variable < len(cnf.names)
    }
    h_edges = sorted(
        [
            [int(parts[1]), int(parts[2])]
            for name in true_names
            if name.startswith("h_")
            for parts in [name.split("_")]
        ]
    )
    family_states = sorted(
        [
            [int(value) for value in name.split("_")[1:]]
            for name in true_names
            if name.startswith("f_")
        ]
    )
    return {
        **metadata,
        "satisfiable": True,
        "h_edges": h_edges,
        "family_states": family_states,
        "family_size": len(family_states),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cycle-length", type=int, default=7)
    parser.add_argument("--partition")
    parser.add_argument("--gamma-at-least-three", action="store_true")
    parser.add_argument(
        "--allow-forbidden-index",
        type=int,
        action="append",
        default=[],
    )
    parser.add_argument(
        "--force-family",
        action="append",
        default=[],
        help="comma-separated triple",
    )
    parser.add_argument(
        "--forbid-family",
        action="append",
        default=[],
        help="comma-separated triple",
    )
    parser.add_argument("--all-partitions", action="store_true")
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    if arguments.all_partitions:
        partitions = restricted_growth_strings(arguments.cycle_length)
    elif arguments.partition is not None:
        partitions = iter((arguments.partition,))
    else:
        partitions = iter(
            ("".join(map(str, range(arguments.cycle_length))),)
        )

    summary: list[dict[str, object]] = []
    first_model: dict[str, object] | None = None
    for partition in partitions:
        cnf, metadata = build(
            arguments.cycle_length,
            partition,
            arguments.gamma_at_least_three,
            frozenset(arguments.allow_forbidden_index),
            tuple(
                tuple(map(int, value.split(",")))
                for value in arguments.force_family
            ),
            tuple(
                tuple(map(int, value.split(",")))
                for value in arguments.forbid_family
            ),
        )
        satisfiable, values, _ = solve(cnf, arguments.solver.resolve())
        row = {
            "partition": partition,
            "order": metadata["order"],
            "variables": metadata["variables"],
            "clauses": metadata["clauses"],
            "satisfiable": satisfiable,
        }
        summary.append(row)
        print(json.dumps(row, sort_keys=True), flush=True)
        if satisfiable:
            first_model = model_record(cnf, metadata, values)
            break

    result = {
        "schema": "inactive-odd-cycle-generalization-probe-v1",
        "classification": "OBSERVED",
        "summary": summary,
        "first_model": first_model,
    }
    if arguments.output:
        arguments.output.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
