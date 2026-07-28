#!/usr/bin/env python3
"""Discovery SAT search for an equality-compatible rank-one XQ1 control.

This is deliberately a small existential-family encoding, not a proof
certificate.  Labels are

    0=u, 1=x, 2=p, 3=q, 4=r, 5=y_p, 6=y_u.

Here T={x,p,q}, B={u,p,q}, r is the XQ1 deleting attack, y_p and y_u
are fixed private witnesses for the two rank-zero successors.  An
existential selector chooses a third vertex s completing {u,y_p} to an
independent triple and forces both that source and its u -> x successor
into the family.  This includes the collision s=q and every external
completion.

A SAT model has alpha=gamma=gamma_infinity=3: alpha<=3 and gamma>=3 are
encoded, while the explicit eternal triple-family gives gamma_infinity<=3;
the independent retained triples give equality in the other directions.
The state B is dominating but is deleted in round one because the attack r
has exactly two legal successors and both have displayed missed vertices.
Thus a SAT model is a genuine greatest-family one-sided active edge with a
rank-one XQ1 collision, even though the encoded family need not be greatest.

UNSAT output is discovery evidence only unless the encoding and a solver
certificate are independently audited.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
from pathlib import Path


NAMES = ("u", "x", "p", "q", "r", "y_p", "y_u")


class CNF:
    def __init__(self) -> None:
        self.next_variable = 1
        self.by_name: dict[str, int] = {}
        self.clauses: list[tuple[int, ...]] = []

    def variable(self, name: str) -> int:
        result = self.by_name.get(name)
        if result is None:
            result = self.next_variable
            self.next_variable += 1
            self.by_name[name] = result
        return result

    def add(self, *literals: int) -> None:
        if not literals:
            raise ValueError("empty clause")
        self.clauses.append(tuple(literals))

    def write(self, path: Path) -> None:
        with path.open("w", encoding="ascii") as handle:
            handle.write(
                f"p cnf {self.next_variable - 1} {len(self.clauses)}\n"
            )
            for clause in self.clauses:
                handle.write(" ".join(map(str, clause)) + " 0\n")


def build(order: int) -> tuple[CNF, dict[str, object]]:
    if order < len(NAMES):
        raise ValueError(f"order must be at least {len(NAMES)}")
    vertices = tuple(range(order))
    triples = tuple(itertools.combinations(vertices, 3))
    triple_index = {triple: index for index, triple in enumerate(triples)}
    cnf = CNF()

    def edge(left: int, right: int) -> int:
        if left == right:
            raise ValueError("no loop variable")
        u, v = sorted((left, right))
        return cnf.variable(f"e:{u}:{v}")

    def family(state: tuple[int, int, int] | set[int]) -> int:
        triple = tuple(sorted(state))
        return cnf.variable(f"f:{triple_index[triple]}")

    def force_edge(left: int, right: int, present: bool) -> None:
        literal = edge(left, right)
        cnf.add(literal if present else -literal)

    # T={x,p,q} is independent.  The XQ1 attack hits x,p,u and misses q.
    for left, right in itertools.combinations((1, 2, 3), 2):
        force_edge(left, right, False)
    for endpoint in (0, 1, 2):
        force_edge(4, endpoint, True)
    force_edge(4, 3, False)
    force_edge(0, 1, True)

    # Exact displayed private-witness incidence.
    # y_p misses C_p={u,r,q}, and y_u misses C_u={r,p,q}.
    for endpoint in (0, 4, 3):
        force_edge(5, endpoint, False)
    force_edge(5, 2, True)
    for endpoint in (4, 2, 3):
        force_edge(6, endpoint, False)
    force_edge(6, 0, True)

    # Consequences already proved in C-150.
    for left, right in ((1, 5), (1, 6), (5, 6)):
        force_edge(left, right, True)

    # Choose some independent completion {u,y_p,s}; activity u -> x is
    # witnessed by the retained successor {x,y_p,s}.  The named incidence
    # already rules out x,p,r,y_u, but keeping every possible third vertex
    # in the selector makes the collision coverage literal.
    completion_selectors: list[int] = []
    # The fixed incidence excludes x (adjacent to u and y_p), p (adjacent
    # to y_p), r (adjacent to u), and y_u (adjacent to u and y_p).
    # Hence the completion is q or a vertex outside the seven named ones.
    completion_candidates = [3, *range(len(NAMES), order)]
    for candidate in completion_candidates:
        selector = cnf.variable(f"completion:{candidate}")
        completion_selectors.append(selector)
        cnf.add(-selector, -edge(0, candidate))
        cnf.add(-selector, -edge(5, candidate))
        cnf.add(-selector, family({0, 5, candidate}))
        cnf.add(-selector, family({1, 5, candidate}))
    cnf.add(*completion_selectors)

    required_family = ((1, 2, 3),)
    cnf.add(family(required_family[0]))

    reverse = (0, 2, 3)
    cnf.add(-family(reverse))

    # Every retained state dominates.
    for state in triples:
        occupied = set(state)
        f_state = family(state)
        for target in vertices:
            if target not in occupied:
                cnf.add(
                    -f_state,
                    *(edge(guard, target) for guard in state),
                )

    # Literal one-edge, one-guard closure for every unoccupied attack.
    for state in triples:
        occupied = set(state)
        f_state = family(state)
        for target in vertices:
            if target in occupied:
                continue
            witnesses: list[int] = []
            for guard in state:
                successor = tuple(sorted((occupied - {guard}) | {target}))
                witness = cnf.variable(
                    f"move:{triple_index[state]}:{target}:{guard}"
                )
                witnesses.append(witness)
                cnf.add(-witness, edge(guard, target))
                cnf.add(-witness, family(successor))
            cnf.add(-f_state, *witnesses)

    # alpha <= 3.
    for four in itertools.combinations(vertices, 4):
        cnf.add(*(edge(*pair) for pair in itertools.combinations(four, 2)))

    # gamma >= 3: every pair has an external common nonneighbor.
    for left, right in itertools.combinations(vertices, 2):
        witnesses: list[int] = []
        for missed in vertices:
            if missed in (left, right):
                continue
            witness = cnf.variable(f"miss:{left}:{right}:{missed}")
            witnesses.append(witness)
            cnf.add(-witness, -edge(left, missed))
            cnf.add(-witness, -edge(right, missed))
        cnf.add(*witnesses)

    # B dominates.  Its only r-successors are C_u and C_p, already forced
    # non-dominating by y_u and y_p respectively, so rho(B)=1.
    reverse_set = set(reverse)
    for target in vertices:
        if target not in reverse_set:
            cnf.add(*(edge(guard, target) for guard in reverse))

    metadata: dict[str, object] = {
        "schema": "rank-one-XQ1-control-synthesis-v1",
        "classification": "OBSERVED_DISCOVERY_ONLY",
        "order": order,
        "labels": {name: position for position, name in enumerate(NAMES)},
        "variables": cnf.next_variable - 1,
        "clauses": len(cnf.clauses),
        "required_family": [list(state) for state in required_family],
        "completion_candidates": completion_candidates,
        "reverse_state": list(reverse),
        "edge_variables": {
            name: number
            for name, number in cnf.by_name.items()
            if name.startswith("e:")
        },
        "family_variables": {
            name: number
            for name, number in cnf.by_name.items()
            if name.startswith("f:")
        },
    }
    return cnf, metadata


def parse_model(stdout: str) -> tuple[str, set[int]]:
    status = ""
    positive: set[int] = set()
    for line in stdout.splitlines():
        if line.startswith("s "):
            status = line
        elif line.startswith("v "):
            for literal in map(int, line.split()[1:]):
                if literal > 0:
                    positive.add(literal)
    if "UNSATISFIABLE" in status:
        return "UNSAT", positive
    if "SATISFIABLE" in status:
        return "SAT", positive
    raise RuntimeError(f"unexpected solver status {status!r}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    arguments = parser.parse_args()

    cnf, result = build(arguments.order)
    cnf.write(arguments.cnf)
    completed = subprocess.run(
        [str(arguments.solver), str(arguments.cnf)],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    status, positive = parse_model(completed.stdout)
    result["status"] = status
    result["solver_returncode"] = completed.returncode
    result["solver_stdout_tail"] = completed.stdout.splitlines()[-20:]
    result["solver_stderr"] = completed.stderr

    if status == "SAT":
        edges: list[list[int]] = []
        for name, number in result["edge_variables"].items():
            if number in positive:
                _, left, right = name.split(":")
                edges.append([int(left), int(right)])
        family_states: list[list[int]] = []
        all_triples = tuple(
            itertools.combinations(range(arguments.order), 3)
        )
        for name, number in result["family_variables"].items():
            if number in positive:
                family_states.append(
                    list(all_triples[int(name.split(":")[1])])
                )
        result["edges"] = edges
        result["family"] = family_states

    result.pop("edge_variables")
    result.pop("family_variables")
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    result["payload_sha256_before_hash_field"] = hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()
    arguments.result.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
