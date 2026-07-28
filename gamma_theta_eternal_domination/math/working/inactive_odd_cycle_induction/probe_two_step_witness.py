#!/usr/bin/env python3
"""Probe the two-step common-neighbor cascade behind scalar transport."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import subprocess
import tempfile
from pathlib import Path


EXACT_PATH = Path(__file__).with_name("probe_exact_recurrence_order.py")
SPEC = importlib.util.spec_from_file_location("exact_recurrence", EXACT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot import exact recurrence probe")
EXACT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXACT)


def add_forced_edge(cnf, first: int, second: int) -> None:
    cnf.add(cnf.name_to_variable[f"h_{min(first, second)}_{max(first, second)}"])


def solve(cnf, solver: Path) -> bool:
    with tempfile.TemporaryDirectory(prefix="two-step-witness-") as temporary:
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
    arguments = parser.parse_args()
    # Base: a,b,c,d,p,q,x = 0,...,6.  z=7 witnesses {d,x};
    # y=8 witnesses either {d,z} or {x,z}.
    d, x, z, y = 3, 6, 7, 8
    rows = []
    for start_value, second_pair in itertools.product(
        (False, True), ((d, z), (x, z))
    ):
        cnf = EXACT.build(9, start_value, frozenset({(0, 1)}))
        # Remove the irrelevant restricted gamma-pair clauses by rebuilding
        # is deliberately avoided here; instead satisfy them explicitly with
        # the named witness p=4.
        add_forced_edge(cnf, 0, 4)
        add_forced_edge(cnf, 1, 4)
        add_forced_edge(cnf, d, z)
        add_forced_edge(cnf, x, z)
        add_forced_edge(cnf, second_pair[0], y)
        add_forced_edge(cnf, second_pair[1], y)
        rows.append(
            {
                "start_value": start_value,
                "second_pair": second_pair,
                "satisfiable": solve(cnf, arguments.solver.resolve()),
                "variables": len(cnf.names) - 1,
                "clauses": len(cnf.clauses),
            }
        )
    print(
        json.dumps(
            {
                "classification": "OBSERVED",
                "rows": rows,
                "schema": "inactive-two-step-common-neighbor-probe-v1",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
