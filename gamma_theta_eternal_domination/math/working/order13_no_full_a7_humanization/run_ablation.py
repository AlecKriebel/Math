#!/usr/bin/env python3
"""Run semantic clause-family ablations of the structured residual formula.

Each ablation deletes complete clause families from the exact production
instance.  SAT witnesses are retained so that an apparently necessary
hypothesis always comes with a concrete countermodel.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time

from analyze_core import read_cnf, semantic_labels


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "order13_no_full_a7_structured" / "instance-proof.cnf"


def dimacs(variables: int, clauses: list[tuple[int, ...]]) -> str:
    body = "\n".join(
        " ".join(map(str, clause)) + " 0" for clause in clauses
    )
    return f"p cnf {variables} {len(clauses)}\n{body}\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument(
        "--omit",
        default="",
        help="comma-separated semantic categories from analyze_core.py",
    )
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()

    variables, clauses = read_cnf(SOURCE)
    labels = semantic_labels()
    if len(labels) != len(clauses):
        raise AssertionError((len(labels), len(clauses)))
    omitted = frozenset(filter(None, args.omit.split(",")))
    unknown = omitted - frozenset(labels)
    if unknown:
        raise ValueError(f"unknown categories: {sorted(unknown)}")

    kept = [
        clause
        for clause, label in zip(clauses, labels, strict=True)
        if label not in omitted
    ]
    raw = dimacs(variables, kept)
    instance = HERE / f"ablation-{args.name}.cnf"
    witness = HERE / f"ablation-{args.name}.model"
    log = HERE / f"ablation-{args.name}.solver.log"
    summary = HERE / f"ablation-{args.name}.json"
    instance.write_text(raw, encoding="ascii")

    command = [
        str(args.solver),
        "--quiet",
        "--binary=false",
        "-w",
        str(witness),
        str(instance),
    ]
    started = time.monotonic()
    try:
        completed = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=args.timeout,
            check=False,
        )
        elapsed = time.monotonic() - started
        status = (
            "SAT"
            if completed.returncode == 10
            else "UNSAT"
            if completed.returncode == 20
            else f"EXIT_{completed.returncode}"
        )
        output = completed.stdout
    except subprocess.TimeoutExpired as error:
        elapsed = time.monotonic() - started
        status = "TIMEOUT"
        output = (error.stdout or "") + (error.stderr or "")
    log.write_text(output, encoding="utf-8")
    if status != "SAT" and witness.exists():
        witness.unlink()

    payload = {
        "name": args.name,
        "status": status,
        "omitted_categories": sorted(omitted),
        "variables": variables,
        "clauses": len(kept),
        "sha256": hashlib.sha256(raw.encode("ascii")).hexdigest(),
        "elapsed_seconds": elapsed,
        "solver": str(args.solver),
        "solver_return_code": (
            completed.returncode if "completed" in locals() else None
        ),
    }
    summary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    raise SystemExit(10 if status == "SAT" else 20 if status == "UNSAT" else 124)


if __name__ == "__main__":
    main()
