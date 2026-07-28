#!/usr/bin/env python3
"""Discovery SAT model for an equality graph with a proper-family mixed P4.

This is a proof-discovery tool only.  It writes a CNF encoding an unknown
simple graph G and an explicit one-guard eternal family of triples.  Labels:

    0=a, 1=b, 2=c, 3=x0, 4=x1, 5=x2, 6=x3.

The family contains S={a,b,c}, has exact direct response lists

    {a}, {a,c}, {b,c}, {b}

on the induced complement path x0-x1-x2-x3, and the graph satisfies
gamma(G)=alpha(G)=3.  Thus any SAT model is an equality-compatible control:
alpha <= gamma_infinity <= 3 and the explicit independent triple gives
alpha >= 3.

No conclusion from an UNSAT run is a campaign theorem without a separately
audited encoding and proof certificate.
"""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
from pathlib import Path


class CNF:
    def __init__(self) -> None:
        self.next_var = 1
        self.clauses: list[list[int]] = []
        self.names: dict[str, int] = {}

    def var(self, name: str) -> int:
        if name not in self.names:
            self.names[name] = self.next_var
            self.next_var += 1
        return self.names[name]

    def add(self, *literals: int) -> None:
        self.clauses.append(list(literals))

    def write(self, path: Path) -> None:
        with path.open("w", encoding="ascii") as handle:
            handle.write(f"p cnf {self.next_var - 1} {len(self.clauses)}\n")
            for clause in self.clauses:
                handle.write(" ".join(map(str, clause)) + " 0\n")


def make_formula(
    order: int,
    gamma_pairs: set[tuple[int, int]] | None = None,
    enforce_alpha: bool = True,
) -> tuple[CNF, dict]:
    if order < 7:
        raise ValueError("order must be at least seven")
    cnf = CNF()
    vertices = tuple(range(order))
    triples = tuple(itertools.combinations(vertices, 3))
    triple_index = {triple: index for index, triple in enumerate(triples)}

    def edge(left: int, right: int) -> int:
        if left == right:
            raise ValueError("loops have no edge variable")
        u, v = sorted((left, right))
        return cnf.var(f"e:{u}:{v}")

    def family(state) -> int:
        triple = tuple(sorted(state))
        return cnf.var(f"f:{triple_index[triple]}")

    # Anchor independence.
    for pair in itertools.combinations((0, 1, 2), 2):
        cnf.add(-edge(*pair))

    # x0..x3 induce a P4 in the complement: consecutive G-nonedges and
    # nonconsecutive G-edges.
    for pair in ((3, 4), (4, 5), (5, 6)):
        cnf.add(-edge(*pair))
    for pair in ((3, 5), (3, 6), (4, 6)):
        cnf.add(edge(*pair))

    reference = (0, 1, 2)
    positive_lists = {
        3: (0,),
        4: (0, 2),
        5: (1, 2),
        6: (1,),
    }
    negative_lists = {
        3: (1, 2),
        4: (1,),
        5: (0,),
        6: (0, 2),
    }
    cnf.add(family(reference))
    required_states: list[tuple[int, int, int]] = [reference]
    forbidden_states: list[tuple[int, int, int]] = []
    for attacked, guards in positive_lists.items():
        for guard in guards:
            state = tuple(sorted((set(reference) - {guard}) | {attacked}))
            required_states.append(state)
            cnf.add(family(state))
            cnf.add(edge(guard, attacked))
    for attacked, guards in negative_lists.items():
        for guard in guards:
            state = tuple(sorted((set(reference) - {guard}) | {attacked}))
            forbidden_states.append(state)
            cnf.add(-family(state))

    # Every family state dominates.  Occupied vertices need no clause.
    for state in triples:
        f_state = family(state)
        occupied = set(state)
        for target in vertices:
            if target in occupied:
                continue
            cnf.add(-f_state, *(edge(guard, target) for guard in state))

    # Literal one-guard closure.  Each auxiliary response witness implies
    # both the graph edge and membership of its one-guard successor.
    for state in triples:
        f_state = family(state)
        occupied = set(state)
        for attacked in vertices:
            if attacked in occupied:
                continue
            witnesses: list[int] = []
            for guard in state:
                successor = tuple(sorted((occupied - {guard}) | {attacked}))
                witness = cnf.var(
                    f"r:{triple_index[state]}:{attacked}:{guard}"
                )
                witnesses.append(witness)
                cnf.add(-witness, edge(guard, attacked))
                cnf.add(-witness, family(successor))
            cnf.add(-f_state, *witnesses)

    # alpha(G) <= 3: every four vertices span a G-edge.  S gives alpha >= 3.
    if enforce_alpha:
        for four in itertools.combinations(vertices, 4):
            cnf.add(*(edge(*pair) for pair in itertools.combinations(four, 2)))

    # gamma(G) >= 3: every pair misses an outside vertex.  The auxiliary
    # witness is allowed only when both incident graph edges are absent.
    # S is a family state and therefore dominates, giving gamma <= 3.
    enforced_gamma_pairs = (
        tuple(itertools.combinations(vertices, 2))
        if gamma_pairs is None
        else tuple(sorted(tuple(sorted(pair)) for pair in gamma_pairs))
    )
    for left, right in enforced_gamma_pairs:
        witnesses: list[int] = []
        for missed in vertices:
            if missed in (left, right):
                continue
            witness = cnf.var(f"m:{left}:{right}:{missed}")
            witnesses.append(witness)
            cnf.add(-witness, -edge(left, missed))
            cnf.add(-witness, -edge(right, missed))
        cnf.add(*witnesses)

    metadata = {
        "order": order,
        "edge_vars": {
            name: variable
            for name, variable in cnf.names.items()
            if name.startswith("e:")
        },
        "family_vars": {
            name: variable
            for name, variable in cnf.names.items()
            if name.startswith("f:")
        },
        "required_states": required_states,
        "forbidden_states": forbidden_states,
        "variables": cnf.next_var - 1,
        "clauses": len(cnf.clauses),
        "enforced_gamma_pairs": [list(pair) for pair in enforced_gamma_pairs],
        "enforce_alpha_at_most_three": enforce_alpha,
    }
    return cnf, metadata


def parse_model(stdout: str) -> set[int] | None:
    status = None
    model: set[int] = set()
    for line in stdout.splitlines():
        if line.startswith("s "):
            status = line
        elif line.startswith("v "):
            for literal in map(int, line.split()[1:]):
                if literal > 0:
                    model.add(literal)
    if status is None:
        raise RuntimeError("solver gave no status")
    if "UNSATISFIABLE" in status:
        return None
    if "SATISFIABLE" not in status:
        raise RuntimeError(f"unexpected status: {status}")
    return model


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, default=12)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument(
        "--gamma-pair",
        action="append",
        default=[],
        metavar="U,V",
        help=(
            "enforce non-domination only for this pair; repeat as needed. "
            "Omitting the option enforces all pairs."
        ),
    )
    parser.add_argument(
        "--no-gamma",
        action="store_true",
        help="omit every non-dominating-pair obligation (discovery only)",
    )
    parser.add_argument(
        "--no-alpha-bound",
        action="store_true",
        help="omit alpha <= 3 clauses (discovery boundary control)",
    )
    args = parser.parse_args()

    if args.no_gamma and args.gamma_pair:
        raise ValueError("--no-gamma and --gamma-pair are mutually exclusive")
    selected_pairs = set() if args.no_gamma else None
    if args.gamma_pair:
        selected_pairs = set()
        for raw in args.gamma_pair:
            left, right = (int(value) for value in raw.split(","))
            if left == right or not (
                0 <= left < args.order and 0 <= right < args.order
            ):
                raise ValueError(f"invalid gamma pair {raw!r}")
            selected_pairs.add(tuple(sorted((left, right))))
    cnf, metadata = make_formula(
        args.order,
        selected_pairs,
        enforce_alpha=not args.no_alpha_bound,
    )
    cnf.write(args.cnf)
    run = subprocess.run(
        [str(args.solver), str(args.cnf)],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    model = parse_model(run.stdout)
    result = {
        "schema": "family-mixed-p4-discovery-sat-v1",
        "classification": "OBSERVED_DISCOVERY_ONLY",
        "solver_returncode": run.returncode,
        "solver_stdout_tail": run.stdout.splitlines()[-20:],
        "solver_stderr": run.stderr,
        **metadata,
    }
    if model is None:
        result["status"] = "UNSAT"
    else:
        result["status"] = "SAT"
        edges = []
        for name, variable in metadata["edge_vars"].items():
            if variable in model:
                _, left, right = name.split(":")
                edges.append([int(left), int(right)])
        states = []
        triples = tuple(itertools.combinations(range(args.order), 3))
        for name, variable in metadata["family_vars"].items():
            if variable in model:
                states.append(list(triples[int(name.split(":")[1])]))
        result["edges"] = edges
        result["family"] = states
    args.result.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
