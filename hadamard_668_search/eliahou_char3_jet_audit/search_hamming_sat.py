#!/usr/bin/env python3
"""Exact SAT search inside a Hamming ball around a replayed support."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
JET = SEARCH / "eliahou_char3_jet"
sys.path[:0] = [str(JET), str(SEARCH)]

from pysat.card import CardEnc, EncType as CardEncType  # noqa: E402
from pysat.solvers import Solver  # noqa: E402

import search_char3_antifold as char3  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, choices=(0, 26), required=True)
    parser.add_argument("--center", type=Path, required=True)
    parser.add_argument("--radius", type=int, required=True)
    parser.add_argument("--moduli", default="2,3")
    args = parser.parse_args()
    payload = json.loads(args.center.read_text())
    if "best_selected" in payload:
        selected_payload = payload["best_selected"]
    elif "selected" in payload:
        selected_payload = payload["selected"]
    else:
        selected_payload = payload["model"]["selected"]
    center = {
        (str(block), int(cell))
        for block, cell in selected_payload
    }
    moduli = tuple(int(value) for value in args.moduli.split(","))
    case = char3.canonical_cases()[args.case]
    started = time.monotonic()
    cnf, pool, variables, equations = char3.build(case, moduli)

    differences = [
        -variable if key in center else variable
        for key, variable in variables.items()
    ]
    cnf.extend(
        CardEnc.atmost(
            differences,
            bound=args.radius,
            vpool=pool,
            encoding=CardEncType.totalizer,
        ).clauses
    )
    with Solver(
        name="cadical195", bootstrap_with=cnf.clauses
    ) as solver:
        satisfiable = solver.solve()
        if satisfiable:
            model = set(solver.get_model())
            selected = char3.selected_support(model, variables)
            replay = char3.replay(
                case, selected, equations, model, moduli
            )
            distance = len(center.symmetric_difference(set(selected)))
            assert distance <= args.radius
        else:
            replay = None
            distance = None
    print(
        json.dumps(
            {
                "status": "SAT" if satisfiable else "UNSAT",
                "case": args.case,
                "moduli": moduli,
                "radius": args.radius,
                "center_size": len(center),
                "variables": pool.top,
                "clauses": len(cnf.clauses),
                "seconds": time.monotonic() - started,
                "distance": distance,
                "model": replay,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
