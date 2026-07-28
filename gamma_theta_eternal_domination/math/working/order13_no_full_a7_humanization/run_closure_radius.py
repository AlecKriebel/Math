#!/usr/bin/env python3
"""Ablate closure obligations outside a Johnson-radius ball around S."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import time

from analyze_core import read_cnf


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "order13_no_full_a7_structured" / "instance-proof.cnf"
S = frozenset((0, 1, 2))


def dimacs(variables: int, clauses: list[tuple[int, ...]]) -> str:
    body = "\n".join(
        " ".join(map(str, clause)) + " 0" for clause in clauses
    )
    return f"p cnf {variables} {len(clauses)}\n{body}\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument(
        "--radius",
        type=int,
        choices=(0, 1, 2, 3),
        required=True,
        help="retain closure for states D with 3-|D intersect S| <= radius",
    )
    parser.add_argument(
        "--anchors",
        default="0,1,2",
        help=(
            "comma-separated retained original-anchor slices; a state inside "
            "the radius is constrained only if it contains one of these"
        ),
    )
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()

    retained_anchors = frozenset(
        int(text) for text in args.anchors.split(",") if text
    )
    if not retained_anchors or not retained_anchors <= S:
        raise ValueError("anchors must be a nonempty subset of 0,1,2")
    variables, clauses = read_cnf(SOURCE)
    closure_start = 715 + 1794 + 2860 + 1
    closure_stop = closure_start + 286 * 10 * 7
    triples = tuple(itertools.combinations(range(13), 3))
    retained_closure_indices: set[int] = set()
    retained_obligations = 0
    for state_index, state in enumerate(triples):
        state_set = frozenset(state)
        if (
            3 - len(state_set & S) > args.radius
            or not state_set & retained_anchors
        ):
            continue
        for attack_index in range(10):
            obligation = state_index * 10 + attack_index
            first = closure_start + 7 * obligation
            retained_closure_indices.update(range(first, first + 7))
            retained_obligations += 1

    kept = [
        clause
        for index, clause in enumerate(clauses)
        if not (
            closure_start <= index < closure_stop
            and index not in retained_closure_indices
        )
    ]
    raw = dimacs(variables, kept)
    anchor_tag = "".join(map(str, sorted(retained_anchors)))
    name = f"closure-radius-{args.radius}-anchors-{anchor_tag}"
    instance = HERE / f"{name}.cnf"
    model = HERE / f"{name}.model"
    summary = HERE / f"{name}.json"
    instance.write_text(raw, encoding="ascii")
    started = time.monotonic()
    try:
        completed = subprocess.run(
            [
                str(args.solver),
                "--quiet",
                "--binary=false",
                "-w",
                str(model),
                str(instance),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=args.timeout,
            check=False,
        )
        status = (
            "SAT"
            if completed.returncode == 10
            else "UNSAT"
            if completed.returncode == 20
            else f"EXIT_{completed.returncode}"
        )
        return_code = completed.returncode
        output = completed.stdout
    except subprocess.TimeoutExpired as error:
        status = "TIMEOUT"
        return_code = None
        output = (error.stdout or "") + (error.stderr or "")
    if status != "SAT" and model.exists():
        model.unlink()
    payload = {
        "radius": args.radius,
        "retained_anchor_slices": sorted(retained_anchors),
        "status": status,
        "variables": variables,
        "clauses": len(kept),
        "retained_closure_obligations": retained_obligations,
        "total_closure_obligations": 2860,
        "sha256": hashlib.sha256(raw.encode("ascii")).hexdigest(),
        "elapsed_seconds": time.monotonic() - started,
        "solver_return_code": return_code,
        "solver_output": output,
    }
    summary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    raise SystemExit(10 if status == "SAT" else 20 if status == "UNSAT" else 124)


if __name__ == "__main__":
    main()
