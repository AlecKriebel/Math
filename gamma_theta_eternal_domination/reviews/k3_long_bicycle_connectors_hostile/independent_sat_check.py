#!/usr/bin/env python3
"""Independent finite audit of the odd fan-path hypotheses.

This checker does not import any campaign search or transition code.  For a
specified connector length it creates Boolean variables for every graph edge
and every triple-family membership bit, then directly encodes:

* the required independent state and complement edges;
* the response-list membership/nonmembership assumptions;
* domination of every retained triple; and
* every unoccupied-attack, exactly-one-guard-move closure obligation.

The finite checks are sanity checks for the hand proof, not a replacement for
its induction over all odd connector lengths.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NOTE = (
    ROOT
    / "math"
    / "working"
    / "k3_long_bicycle_connectors"
    / "NOTE.md"
)
CADICAL = ROOT / "tools" / "cadical_3_0_1" / "build" / "cadical"


class CNF:
    def __init__(self) -> None:
        self._next_variable = 1
        self.variables: dict[tuple[object, ...], int] = {}
        self.clauses: list[tuple[int, ...]] = []

    def variable(self, *key: object) -> int:
        compound_key = tuple(key)
        if compound_key not in self.variables:
            self.variables[compound_key] = self._next_variable
            self._next_variable += 1
        return self.variables[compound_key]

    def add(self, *literals: int) -> None:
        assert literals
        self.clauses.append(tuple(literals))

    @property
    def variable_count(self) -> int:
        return self._next_variable - 1

    def dimacs(self) -> bytes:
        lines = [f"p cnf {self.variable_count} {len(self.clauses)}"]
        lines.extend(" ".join(map(str, clause)) + " 0" for clause in self.clauses)
        return ("\n".join(lines) + "\n").encode("ascii")


def normalized_pair(left: int, right: int) -> tuple[int, int]:
    assert left != right
    return (left, right) if left < right else (right, left)


def normalized_triple(vertices: itertools.chain[int] | tuple[int, ...]) -> tuple[int, int, int]:
    result = tuple(sorted(vertices))
    assert len(result) == 3 and len(set(result)) == 3
    return result


def build_instance(connector_length: int) -> CNF:
    assert connector_length >= 1

    # a,b,c,p,q,v_0,...,v_m
    a, b, c, p, q = range(5)
    path = tuple(range(5, 5 + connector_length + 1))
    vertex_count = connector_length + 6
    vertices = tuple(range(vertex_count))

    cnf = CNF()
    edge = {
        pair: cnf.variable("edge", *pair)
        for pair in itertools.combinations(vertices, 2)
    }
    states = tuple(itertools.combinations(vertices, 3))
    family = {state: cnf.variable("family", *state) for state in states}

    def edge_variable(left: int, right: int) -> int:
        return edge[normalized_pair(left, right)]

    def family_variable(state: tuple[int, ...]) -> int:
        return family[normalized_triple(state)]

    # Every retained triple dominates.
    for state in states:
        state_set = set(state)
        for attacked in vertices:
            if attacked in state_set:
                continue
            cnf.add(
                -family[state],
                *(edge_variable(guard, attacked) for guard in state),
            )

    # Every retained triple has a legal retained one-guard successor for each
    # unoccupied attacked vertex.
    for state in states:
        state_set = set(state)
        for attacked in vertices:
            if attacked in state_set:
                continue
            responses: list[int] = []
            for guard in state:
                move = cnf.variable("move", *state, attacked, guard)
                successor = tuple((state_set - {guard}) | {attacked})
                cnf.add(-move, edge_variable(guard, attacked))
                cnf.add(-move, family_variable(successor))
                responses.append(move)
            cnf.add(-family[state], *responses)

    reference = normalized_triple((a, b, c))
    positive_swap = normalized_triple((b, c, p))
    cnf.add(family[reference])
    cnf.add(family[positive_swap])
    cnf.add(edge_variable(a, p))

    # S is independent.
    for pair in itertools.combinations(reference, 2):
        cnf.add(-edge_variable(*pair))

    # a is absent from every path-vertex response list.  Under domination and
    # independence of S, direct-swap family membership is equivalent to list
    # membership, so forcing the swap absent is exact.
    for path_vertex in path:
        cnf.add(-family_variable((b, c, path_vertex)))

    # Required complement edges.
    required_complement_edges = {
        normalized_pair(p, q),
        normalized_pair(q, path[0]),
        normalized_pair(q, path[-1]),
    }
    required_complement_edges.update(
        normalized_pair(path[index], path[index + 1])
        for index in range(len(path) - 1)
    )
    for pair in sorted(required_complement_edges):
        cnf.add(-edge[pair])

    return cnf


def solve(
    connector_length: int, *, relax_terminal_fan_edge: bool = False
) -> dict[str, object]:
    cnf = build_instance(connector_length)
    if relax_terminal_fan_edge:
        q = 4
        terminal = 5 + connector_length
        terminal_edge = cnf.variables[
            ("edge", *normalized_pair(q, terminal))
        ]
        target_clause = (-terminal_edge,)
        matches = [
            index
            for index, clause in enumerate(cnf.clauses)
            if clause == target_clause
        ]
        assert len(matches) == 1
        del cnf.clauses[matches[0]]
    payload = cnf.dimacs()
    with tempfile.TemporaryDirectory(prefix="odd-fan-path-audit-") as directory:
        instance = Path(directory) / f"m{connector_length}.cnf"
        instance.write_bytes(payload)
        completed = subprocess.run(
            [str(CADICAL), "--quiet", str(instance)],
            check=False,
            capture_output=True,
            text=True,
        )
    combined_output = completed.stdout + completed.stderr
    if "s UNSATISFIABLE" in combined_output:
        status = "UNSATISFIABLE"
    elif "s SATISFIABLE" in combined_output:
        status = "SATISFIABLE"
    else:
        status = "UNKNOWN"
    return {
        "connector_length": connector_length,
        "relaxed_terminal_fan_edge": relax_terminal_fan_edge,
        "vertices": connector_length + 6,
        "variables": cnf.variable_count,
        "clauses": len(cnf.clauses),
        "cnf_sha256": hashlib.sha256(payload).hexdigest(),
        "solver_exit_code": completed.returncode,
        "status": status,
    }


def main() -> None:
    assert CADICAL.is_file()
    exact_instances = [solve(length) for length in (1, 3, 5)]
    relaxed_controls = [
        solve(length, relax_terminal_fan_edge=True)
        for length in (1, 3, 5)
    ]
    results = {
        "checker": "independent direct graph/family SAT encoding",
        "note_sha256": hashlib.sha256(NOTE.read_bytes()).hexdigest(),
        "cadical_version": subprocess.run(
            [str(CADICAL), "--version"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip(),
        "exact_instances": exact_instances,
        "relaxed_controls": relaxed_controls,
    }
    assert all(
        item["status"] == "UNSATISFIABLE" for item in exact_instances
    )
    assert all(
        item["status"] == "SATISFIABLE" for item in relaxed_controls
    )
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
