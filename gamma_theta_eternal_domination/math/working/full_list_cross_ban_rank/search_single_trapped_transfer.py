#!/usr/bin/env python3
"""Bounded falsifier for "a transfer endpoint cannot lie in the ban".

The formula asks for a gamma=alpha=gamma-infinity=3 graph containing one
named rank-zero corridor whose forced witness transfer lies in the target's
complement neighborhood.  A SAT result is only a candidate control and is
rechecked from the graph itself before use.
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import subprocess
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = (
    HERE.parent
    / "full_list_three_color_coupling"
    / "search_cyclic_corridor_control.py"
)
SPEC = importlib.util.spec_from_file_location("cyclic_search", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise AssertionError("could not load discovery CNF helper")
SEARCH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SEARCH)


def encode_graph6(order: int, edges: set[tuple[int, int]]) -> str:
    bits = [
        int((low, high) in edges)
        for high in range(1, order)
        for low in range(high)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    payload = "".join(
        chr(63 + sum(bits[offset + bit] << (5 - bit) for bit in range(6)))
        for offset in range(0, len(bits), 6)
    )
    return chr(63 + order) + payload


def build(
    order: int,
    gamma_pairs: frozenset[tuple[int, int]] | None = None,
    enforce_gamma_three: bool = True,
    second_witness_in_B: bool = False,
    force_dynamic_transfer: bool = True,
    enforce_alpha_three: bool = True,
    enforce_family_closure: bool = True,
    second_witness_misses_primary: bool = False,
    omit_primary_second_transfer: bool = False,
    omit_named_states: frozenset[int] = frozenset(),
):
    if order < 8:
        raise ValueError("the named core uses vertices 0 through 7")
    cnf = SEARCH.CNF()
    edge = {pair: cnf.variable() for pair in SEARCH.pairs(order)}
    family = {triple: cnf.variable() for triple in SEARCH.triples(order)}

    def e(first: int, second: int) -> int:
        return edge[tuple(sorted((first, second)))]

    def f(state) -> int:
        return family[tuple(sorted(state))]

    root = (0, 1, 2)
    target, mover, terminal, witness = 3, 4, 5, 6
    for pair in itertools.combinations(root, 2):
        cnf.add(-e(*pair))
    for anchor in root:
        cnf.add(e(target, anchor))
    for first, second in (
        (target, mover),
        (0, mover),
        (0, terminal),
        (1, terminal),
        (mover, terminal),
        (0, witness),
        (1, witness),
    ):
        cnf.add(e(first, second))
    for first, second in (
        (target, terminal),
        (target, witness),
        (2, witness),
        (mover, witness),
        (terminal, witness),
    ):
        cnf.add(-e(first, second))
    # If the third root guard can move to the terminal, its unbanned
    # alternate {1,4,5} is still nondominating: vertex 7 misses it.
    for guard in (1, mover, terminal):
        cnf.add(-e(7, guard))
    if second_witness_in_B:
        cnf.add(-e(target, 7))
    if second_witness_misses_primary:
        cnf.add(-e(0, 7))

    named_states = (
        root,
        (1, 2, target),
        (0, 2, target),
        (0, 1, target),
        (1, 2, mover),
        (1, 2, terminal),
        (0, 2, terminal),
        (2, mover, witness),
        (2, terminal, witness),
        (0, 2, witness),
    )
    for index, state in enumerate(named_states):
        if index not in omit_named_states:
            cnf.add(f(state))
    # Dynamic palette absence, not a graph nonedge: 1 is absent from Q(4).
    if force_dynamic_transfer:
        cnf.add(-f((0, 2, mover)))
    if omit_primary_second_transfer:
        cnf.add(-f((1, 2, 7)))

    # alpha <= 3.
    if enforce_alpha_three:
        for four in itertools.combinations(range(order), 4):
            cnf.add(
                *(
                    e(first, second)
                    for first, second in itertools.combinations(four, 2)
                )
            )

    # gamma >= 3.
    selected_pairs = (
        ()
        if not enforce_gamma_three
        else (
            tuple(itertools.combinations(range(order), 2))
            if gamma_pairs is None
            else tuple(sorted(gamma_pairs))
        )
    )
    for first, second in selected_pairs:
        misses = []
        for missed in range(order):
            if missed in (first, second):
                continue
            variable = cnf.variable()
            cnf.add(-variable, -e(first, missed))
            cnf.add(-variable, -e(second, missed))
            cnf.add(e(first, missed), e(second, missed), variable)
            misses.append(variable)
        cnf.add(*misses)

    # Literal one-guard eternal-family closure and domination.
    for state in SEARCH.triples(order):
        state_set = set(state)
        fv = f(state)
        for attacked in range(order):
            if attacked in state_set:
                continue
            cnf.add(-fv, *(e(guard, attacked) for guard in state))
            if not enforce_family_closure:
                continue
            moves = []
            for guard in state:
                successor = (state_set - {guard}) | {attacked}
                move = cnf.variable()
                cnf.add(-move, e(guard, attacked))
                cnf.add(-move, f(successor))
                cnf.add(-e(guard, attacked), -f(successor), move)
                moves.append(move)
            cnf.add(-fv, *moves)
    return cnf, edge, family


def solve(
    order: int,
    solver: Path,
    gamma_pairs: frozenset[tuple[int, int]] | None = None,
    enforce_gamma_three: bool = True,
    second_witness_in_B: bool = False,
    force_dynamic_transfer: bool = True,
    enforce_alpha_three: bool = True,
    enforce_family_closure: bool = True,
    second_witness_misses_primary: bool = False,
    omit_primary_second_transfer: bool = False,
    omit_named_states: frozenset[int] = frozenset(),
) -> dict[str, object]:
    cnf, edge, family = build(
        order,
        gamma_pairs,
        enforce_gamma_three,
        second_witness_in_B,
        force_dynamic_transfer,
        enforce_alpha_three,
        enforce_family_closure,
        second_witness_misses_primary,
        omit_primary_second_transfer,
        omit_named_states,
    )
    with tempfile.TemporaryDirectory(prefix="trapped-transfer-") as temp:
        formula = Path(temp) / "instance.cnf"
        with formula.open("w", encoding="ascii") as stream:
            stream.write(
                f"p cnf {cnf.next_variable - 1} {len(cnf.clauses)}\n"
            )
            for clause in cnf.clauses:
                stream.write(" ".join(map(str, clause)) + " 0\n")
        completed = subprocess.run(
            (str(solver), str(formula)),
            check=False,
            capture_output=True,
            text=True,
        )
    status = {10: "SAT", 20: "UNSAT"}.get(completed.returncode, "UNKNOWN")
    positive = set()
    if status == "SAT":
        for line in completed.stdout.splitlines():
            if line.startswith("v "):
                positive.update(
                    literal
                    for literal in map(int, line[2:].split())
                    if literal > 0
                )
    selected_edges = {
        pair for pair, variable in edge.items() if variable in positive
    }
    selected_family = [
        list(state)
        for state, variable in family.items()
        if variable in positive
    ]
    return {
        "status": status,
        "order": order,
        "variables": cnf.next_variable - 1,
        "clauses": len(cnf.clauses),
        "graph6": (
            encode_graph6(order, selected_edges) if status == "SAT" else None
        ),
        "edges": [list(pair) for pair in sorted(selected_edges)],
        "family": selected_family,
        "scope": "OBSERVED bounded falsifier; no proof-log claim",
        "gamma_pairs": (
            "none"
            if not enforce_gamma_three
            else "all"
            if gamma_pairs is None
            else [list(pair) for pair in sorted(gamma_pairs)]
        ),
        "second_witness_in_B": second_witness_in_B,
        "force_dynamic_transfer": force_dynamic_transfer,
        "enforce_alpha_three": enforce_alpha_three,
        "enforce_family_closure": enforce_family_closure,
        "second_witness_misses_primary": second_witness_misses_primary,
        "omit_primary_second_transfer": omit_primary_second_transfer,
        "omit_named_states": sorted(omit_named_states),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument(
        "--gamma-pair",
        nargs=2,
        type=int,
        action="append",
        metavar=("FIRST", "SECOND"),
    )
    parser.add_argument("--allow-dominating-pairs", action="store_true")
    parser.add_argument("--second-witness-in-B", action="store_true")
    parser.add_argument("--allow-mover-transfer", action="store_true")
    parser.add_argument("--allow-independent-four", action="store_true")
    parser.add_argument("--domination-only-family", action="store_true")
    parser.add_argument(
        "--second-witness-misses-primary",
        action="store_true",
    )
    parser.add_argument(
        "--omit-primary-second-transfer",
        action="store_true",
    )
    parser.add_argument("--omit-named-state", action="append", type=int)
    args = parser.parse_args()
    gamma_pairs = (
        None
        if args.gamma_pair is None
        else frozenset(
            tuple(sorted(pair)) for pair in args.gamma_pair
        )
    )
    print(
        json.dumps(
            solve(
                args.order,
                args.solver.resolve(),
                gamma_pairs,
                enforce_gamma_three=not args.allow_dominating_pairs,
                second_witness_in_B=args.second_witness_in_B,
                force_dynamic_transfer=not args.allow_mover_transfer,
                enforce_alpha_three=not args.allow_independent_four,
                enforce_family_closure=not args.domination_only_family,
                second_witness_misses_primary=(
                    args.second_witness_misses_primary
                ),
                omit_primary_second_transfer=(
                    args.omit_primary_second_transfer
                ),
                omit_named_states=frozenset(args.omit_named_state or ()),
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
