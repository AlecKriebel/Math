#!/usr/bin/env python3
"""Bounded conflict-budget comparison of modular and exact SAT encodings."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

from pysat.solvers import Solver


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
JET = SEARCH / "eliahou_char3_jet"
sys.path[:0] = [str(JET), str(SEARCH)]

import search_char3_antifold as char3  # noqa: E402
import search_eliahou_antifold_sat as exact  # noqa: E402


CERTIFICATE = HERE / "EXACT_CRT_SAT_BENCHMARK.json"
DEFAULT_CASES = (1, 2, 6, 14)
ENCODINGS = (
    ("mod6", (2, 3)),
    ("mod12", (2, 3, 4)),
    ("exact_crt84", (2, 3, 4, 7)),
    ("exact_pb", None),
)


def cnf_hash(clauses: list[list[int]]) -> str:
    hasher = hashlib.sha256()
    for clause in clauses:
        hasher.update(len(clause).to_bytes(2, "little"))
        for literal in clause:
            hasher.update(
                int(literal).to_bytes(4, "little", signed=True)
            )
    return hasher.hexdigest()


def benchmark(
    case_number: int,
    name: str,
    moduli: tuple[int, ...] | None,
    conflict_budget: int,
) -> dict[str, object]:
    case = char3.canonical_cases()[case_number]
    build_started = time.monotonic()
    if moduli is None:
        cnf, _, variables = exact.build(
            case, None, modulus=42, add_mod4=False
        )
        equations = None
    else:
        cnf, _, variables, equations = char3.build(case, moduli)
    build_seconds = time.monotonic() - build_started

    solve_started = time.monotonic()
    with Solver(name="cadical195", bootstrap_with=cnf) as solver:
        solver.conf_budget(conflict_budget)
        status = solver.solve_limited()
        solve_seconds = time.monotonic() - solve_started
        stats = {
            key: int(value)
            for key, value in solver.accum_stats().items()
        }
        model = set(solver.get_model() or ())

    replay = None
    if status is True:
        selected = tuple(
            key for key, variable in variables.items() if variable in model
        )
        if moduli is None:
            rows = exact.direct_rows(case, set(selected))
            correlations = exact.negacyclic_correlations(rows)
            if (
                len(selected) != 39
                or correlations[0] != 334
                or any(correlations[1:])
            ):
                raise AssertionError("exact-PB SAT model failed replay")
            replay = {
                "selected": [list(key) for key in selected],
                "full_exact": True,
            }
        else:
            replay = char3.replay(
                case, selected, equations, model, moduli
            )
            if name == "exact_crt84" and not replay["full_exact"]:
                raise AssertionError(
                    "a CRT-84 SAT model was not an exact support"
                )

    return {
        "case": case_number,
        "q_index": case.index,
        "encoding": name,
        "moduli": list(moduli) if moduli is not None else None,
        "variables": cnf.nv,
        "clauses": len(cnf.clauses),
        "cnf_sha256": cnf_hash(cnf.clauses),
        "conflict_budget": conflict_budget,
        "status": (
            "SAT" if status is True else ("UNSAT" if status is False else "UNKNOWN")
        ),
        "build_seconds": build_seconds,
        "solve_seconds": solve_seconds,
        "solver_stats": stats,
        "replay": replay,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cases",
        default=",".join(map(str, DEFAULT_CASES)),
        help="comma-separated canonical cases",
    )
    parser.add_argument("--conflicts", type=int, default=10_000)
    parser.add_argument("--write-certificate", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cases = tuple(int(value) for value in args.cases.split(",") if value)
    if (
        not cases
        or any(case not in range(1, 21) for case in cases)
        or args.conflicts < 1
    ):
        raise ValueError("invalid cases or conflict budget")
    results = [
        benchmark(case_number, name, moduli, args.conflicts)
        for case_number in cases
        for name, moduli in ENCODINGS
    ]
    payload: dict[str, object] = {
        "schema": "h668-exact-crt-sat-benchmark-v1",
        "cases": list(cases),
        "solver": "cadical195",
        "conflict_budget_per_run": args.conflicts,
        "production_search": False,
        "exactness": (
            "moduli 3,4,7 have lcm 84; every normalized residual has "
            "absolute value at most 83, so exact_crt84 is equivalent to "
            "the exact integer equations"
        ),
        "results": results,
    }
    semantic = json.loads(json.dumps(payload))
    for result in semantic["results"]:
        result.pop("build_seconds", None)
        result.pop("solve_seconds", None)
    payload["semantic_sha256"] = hashlib.sha256(
        json.dumps(
            semantic, sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()
    if args.write_certificate:
        CERTIFICATE.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n"
        )
        print(f"WROTE {CERTIFICATE}")
    else:
        print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
