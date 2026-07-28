#!/usr/bin/env python3
"""Discovery-only SAT probes for the remaining rank-one collision rows.

The fixed labels are u=0, x=1, p=2, q=3, r=4, followed by one private
witness y_g for every legal mover g from B={u,p,q} at the deleting attack
r.  The cases are the six rows of accepted C-150.

The encoding is intentionally direct:

* T={x,p,q} is independent and retained;
* B={u,p,q} dominates but is omitted;
* every legal r-successor of B has its displayed private witness and is
  therefore non-dominating, so B has literal greatest-kernel rank one;
* an existential independent completion of {u,y_p} and its u->x successor
  witness the active orientation u▷x;
* an arbitrary nonempty eternal family of dominating triples is encoded
  literally;
* alpha<=3 and gamma>=3 are exact subset constraints.

Thus a SAT model is a genuine equality-compatible rank-one realization of
the selected row.  UNSAT is only discovery evidence unless accompanied by
an independently audited proof certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
from pathlib import Path


BASE = {"u": 0, "x": 1, "p": 2, "q": 3, "r": 4}
CASES = {
    "XQ0": ({"x", "p"}, False),
    "XQ1": ({"x", "p"}, True),
    "QQ0": ({"p", "q"}, False),
    "QQ1": ({"p", "q"}, True),
    "AQ0": ({"x", "p", "q"}, False),
    "AQ1": ({"x", "p", "q"}, True),
}


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
            handle.write(f"p cnf {self.next_variable - 1} {len(self.clauses)}\n")
            for clause in self.clauses:
                handle.write(" ".join(map(str, clause)) + " 0\n")


def build(
    order: int,
    case_name: str,
    *,
    require_alpha: bool = True,
    require_gamma: bool = True,
    require_i: bool = False,
    required_pairs: tuple[tuple[int, int], ...] = (),
) -> tuple[CNF, dict[str, object]]:
    root_neighbors, ur_present = CASES[case_name]
    b_names = ("u", "p", "q")
    movers = [
        name
        for name in b_names
        if (name == "u" and ur_present) or name in root_neighbors
    ]
    labels = dict(BASE)
    for mover in movers:
        labels[f"y_{mover}"] = len(labels)
    if order < len(labels):
        raise ValueError(f"{case_name} needs order at least {len(labels)}")

    vertices = tuple(range(order))
    triples = tuple(itertools.combinations(vertices, 3))
    triple_index = {triple: index for index, triple in enumerate(triples)}
    cnf = CNF()

    def edge(left: int, right: int) -> int:
        if left == right:
            raise ValueError("loop requested")
        left, right = sorted((left, right))
        return cnf.variable(f"e:{left}:{right}")

    def family(state: tuple[int, ...] | set[int]) -> int:
        triple = tuple(sorted(state))
        if len(triple) != 3:
            raise ValueError(f"not a triple: {triple}")
        return cnf.variable(f"f:{triple_index[triple]}")

    def force_edge(left: int, right: int, present: bool) -> None:
        literal = edge(left, right)
        cnf.add(literal if present else -literal)

    # T is independent and u--x is the active move edge.
    for left, right in itertools.combinations(
        (labels["x"], labels["p"], labels["q"]), 2
    ):
        force_edge(left, right, False)
    force_edge(labels["u"], labels["x"], True)

    # Exact row incidence at r.
    for name in ("x", "p", "q"):
        force_edge(labels["r"], labels[name], name in root_neighbors)
    force_edge(labels["r"], labels["u"], ur_present)

    # A distinct private witness for every legal successor C_g=B-g+r.
    for mover in movers:
        witness = labels[f"y_{mover}"]
        force_edge(witness, labels[mover], True)
        force_edge(witness, labels["r"], False)
        for other in b_names:
            if other != mover:
                force_edge(witness, labels[other], False)

    # Witness u▷x using an arbitrary independent completion of {u,y_p}.
    # The completion may collide with any named vertex not explicitly
    # excluded, so all labels other than u,x,y_p remain candidates.
    y_p = labels["y_p"]
    completion_candidates = [
        vertex
        for vertex in vertices
        if vertex not in (labels["u"], labels["x"], y_p)
    ]
    completion_selectors: list[int] = []
    for candidate in completion_candidates:
        selector = cnf.variable(f"completion:{candidate}")
        completion_selectors.append(selector)
        cnf.add(-selector, -edge(labels["u"], candidate))
        cnf.add(-selector, -edge(y_p, candidate))
        cnf.add(-selector, family({labels["u"], y_p, candidate}))
        cnf.add(-selector, family({labels["x"], y_p, candidate}))
    cnf.add(*completion_selectors)

    t_state = {labels["x"], labels["p"], labels["q"]}
    b_state = {labels["u"], labels["p"], labels["q"]}
    cnf.add(family(t_state))
    cnf.add(-family(b_state))

    # Every retained state dominates.
    for state in triples:
        occupied = set(state)
        f_state = family(state)
        for target in vertices:
            if target not in occupied:
                cnf.add(-f_state, *(edge(guard, target) for guard in state))

    # Literal one-guard, one-edge closure at every unoccupied attack.
    for state in triples:
        occupied = set(state)
        f_state = family(state)
        for target in vertices:
            if target in occupied:
                continue
            responses: list[int] = []
            for guard in state:
                successor = (occupied - {guard}) | {target}
                response = cnf.variable(
                    f"move:{triple_index[state]}:{target}:{guard}"
                )
                responses.append(response)
                cnf.add(-response, edge(guard, target))
                cnf.add(-response, family(successor))
            cnf.add(-f_state, *responses)

    # alpha <= 3.
    if require_alpha:
        for four in itertools.combinations(vertices, 4):
            cnf.add(*(edge(*pair) for pair in itertools.combinations(four, 2)))

    # gamma >= 3: each vertex pair has an external common nonneighbor.
    pairs_for_nondomination = (
        tuple(itertools.combinations(vertices, 2))
        if require_gamma
        else tuple(tuple(sorted(pair)) for pair in required_pairs)
    )
    for left, right in pairs_for_nondomination:
        if left == right or left not in vertices or right not in vertices:
            raise ValueError(f"invalid required pair {(left, right)}")
        witnesses: list[int] = []
        for missed in vertices:
            if missed in (left, right):
                continue
            witness = cnf.variable(f"miss:{left}:{right}:{missed}")
            witnesses.append(witness)
            cnf.add(-witness, -edge(left, missed))
            cnf.add(-witness, -edge(right, missed))
        cnf.add(*witnesses)

    # i >= 3: every independent pair extends to an independent triple.
    # This differs from gamma >= 3 only on adjacent pairs.
    if require_i:
        for left, right in itertools.combinations(vertices, 2):
            witnesses: list[int] = []
            for extension in vertices:
                if extension in (left, right):
                    continue
                witness = cnf.variable(f"extend:{left}:{right}:{extension}")
                witnesses.append(witness)
                cnf.add(-witness, -edge(left, extension))
                cnf.add(-witness, -edge(right, extension))
            cnf.add(edge(left, right), *witnesses)

    # B dominates.  The displayed private witnesses make every legal
    # successor at r non-dominating, so B is deleted in the first round.
    for target in vertices:
        if target not in b_state:
            cnf.add(*(edge(guard, target) for guard in b_state))

    metadata: dict[str, object] = {
        "schema": "rank-one-remaining-collision-probe-v1",
        "classification": "OBSERVED_DISCOVERY_ONLY",
        "case": case_name,
        "order": order,
        "labels": labels,
        "root_neighbors": sorted(root_neighbors),
        "ur_present": ur_present,
        "movers": movers,
        "require_alpha": require_alpha,
        "require_gamma": require_gamma,
        "require_i": require_i,
        "required_pairs": [list(pair) for pair in required_pairs],
        "completion_candidates": completion_candidates,
        "variables": cnf.next_variable - 1,
        "clauses": len(cnf.clauses),
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
    parser.add_argument("--case", choices=sorted(CASES), required=True)
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--drop-alpha", action="store_true")
    parser.add_argument("--drop-gamma", action="store_true")
    parser.add_argument("--require-i", action="store_true")
    parser.add_argument(
        "--require-pair",
        action="append",
        default=[],
        metavar="U,V",
        help="when --drop-gamma is set, require only this pair not to dominate",
    )
    arguments = parser.parse_args()
    required_pairs = tuple(
        tuple(map(int, item.split(","))) for item in arguments.require_pair
    )

    cnf, result = build(
        arguments.order,
        arguments.case,
        require_alpha=not arguments.drop_alpha,
        require_gamma=not arguments.drop_gamma,
        require_i=arguments.require_i,
        required_pairs=required_pairs,
    )
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
        all_triples = tuple(itertools.combinations(range(arguments.order), 3))
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
