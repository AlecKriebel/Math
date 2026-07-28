#!/usr/bin/env python3
"""Discovery probe for a two-edge inactive-path transport recurrence."""

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
    start_value: bool,
    anchor_misses_segment: bool,
    force_opposite_middle: bool,
    exact_equality: bool,
    omit_alpha: bool = False,
    omit_gamma: bool = False,
    omit_deletion_gamma: bool = False,
    omit_anchor_physical: bool = False,
    restricted_gamma_pairs: frozenset[tuple[int, int]] = frozenset(),
) -> CNF:
    # anchor a; path b-c-d; witnesses p,q; target x
    a, b, c, d, p, q, x = range(7)
    vertices = tuple(range(7))
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

    cnf.add(edge(b, c))
    cnf.add(edge(c, d))
    cnf.add(-edge(b, d))
    if anchor_misses_segment:
        cnf.add(-edge(a, b))
        cnf.add(-edge(a, c))
        cnf.add(-edge(a, d))

    for first, second, witness in ((b, c, p), (c, d, q)):
        cnf.add(edge(first, witness))
        cnf.add(edge(second, witness))
        cnf.add(family[tuple(sorted((first, second, witness)))])
        cnf.add(-family[tuple(sorted((first, witness, x)))])
        cnf.add(-family[tuple(sorted((second, witness, x)))])

    if exact_equality:
        if not omit_alpha:
            # alpha(G) <= 3: every four-set has an H-nonedge.
            for group in itertools.combinations(vertices, 4):
                cnf.add(
                    *(
                        -edge(first, second)
                        for first, second in itertools.combinations(group, 2)
                    )
                )
        if not omit_gamma:
            # gamma(G) >= 3: every pair has a common outside H-neighbor.
            for first, second in itertools.combinations(vertices, 2):
                if (
                    restricted_gamma_pairs
                    and (first, second) not in restricted_gamma_pairs
                ):
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
        if not omit_deletion_gamma:
            # The same domination lower bound after deleting x.
            deletion = tuple(vertex for vertex in vertices if vertex != x)
            for first, second in itertools.combinations(deletion, 2):
                choices = []
                for witness in deletion:
                    if witness in (first, second):
                        continue
                    indicator = cnf.variable(f"cx_{first}_{second}__{witness}")
                    choices.append(indicator)
                    cnf.add(-indicator, edge(first, witness))
                    cnf.add(-indicator, edge(second, witness))
                cnf.add(*choices)
        if not omit_anchor_physical:
            # Physical inactivity of the anchor.
            cnf.add(edge(a, x))

    start = family[tuple(sorted((a, b, x)))]
    middle = family[tuple(sorted((a, c, x)))]
    end = family[tuple(sorted((a, d, x)))]
    cnf.add(start if start_value else -start)
    if force_opposite_middle:
        cnf.add(middle if not start_value else -middle)
    cnf.add(-end if start_value else end)
    return cnf


def solve(cnf: CNF, solver: Path) -> bool:
    with tempfile.TemporaryDirectory(prefix="inactive-recurrence-") as temporary:
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
    parser.add_argument("--exact-equality", action="store_true")
    parser.add_argument("--omit-alpha", action="store_true")
    parser.add_argument("--omit-gamma", action="store_true")
    parser.add_argument("--omit-deletion-gamma", action="store_true")
    parser.add_argument("--omit-anchor-physical", action="store_true")
    parser.add_argument(
        "--gamma-pair",
        action="append",
        default=[],
        help="restrict gamma constraints to a comma-separated pair",
    )
    arguments = parser.parse_args()
    rows = []
    for anchor_misses_segment, force_opposite_middle, start_value in itertools.product(
        (False, True), repeat=3
    ):
        cnf = build(
            start_value,
            anchor_misses_segment,
            force_opposite_middle,
            arguments.exact_equality,
            arguments.omit_alpha,
            arguments.omit_gamma,
            arguments.omit_deletion_gamma,
            arguments.omit_anchor_physical,
            frozenset(
                tuple(sorted(map(int, pair.split(","))))
                for pair in arguments.gamma_pair
            ),
        )
        rows.append(
            {
                "anchor_misses_segment_in_H": anchor_misses_segment,
                "force_opposite_middle": force_opposite_middle,
                "exact_equality": arguments.exact_equality,
                "omissions": {
                    "alpha": arguments.omit_alpha,
                    "gamma": arguments.omit_gamma,
                    "deletion_gamma": arguments.omit_deletion_gamma,
                    "anchor_physical": arguments.omit_anchor_physical,
                },
                "restricted_gamma_pairs": arguments.gamma_pair,
                "start_value": start_value,
                "opposite_end_value_satisfiable": solve(
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
                "schema": "inactive-two-edge-transport-probe-v1",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
