#!/usr/bin/env python3
"""Build the semantically reduced structured residual instance.

The removed clauses are not hypotheses.  They are consequences of literal
one-guard closure, the retained anchor state, and the signature ordering:

* selected-state domination and ``alpha <= 3``;
* family nonemptiness;
* the four graph edges already forced by the four positive port responses;
* the two negative port responses already forced by their H-signatures; and
* no-full clauses for vertices known to be nonneutral.

Only vertices 7, 8, and 9 can still have zero anchor signature, so only their
three no-full clauses remain.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
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


def no_full_target(clause: tuple[int, ...]) -> int:
    triples = tuple(itertools.combinations(range(13), 3))
    family_start = 78 + 78 * 11 + 1
    family_by_variable = {
        family_start + index: triple for index, triple in enumerate(triples)
    }
    states = [family_by_variable[abs(literal)] for literal in clause]
    outside = set(states[0]) - {0, 1, 2}
    if len(outside) != 1:
        raise AssertionError((clause, states))
    target = outside.pop()
    if any((set(state) - {0, 1, 2}) != {target} for state in states):
        raise AssertionError((clause, states))
    return target


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--instance", type=Path, default=HERE / "semantic.cnf")
    parser.add_argument("--proof", type=Path, default=HERE / "semantic-proof.drat")
    parser.add_argument("--summary", type=Path, default=HERE / "semantic.json")
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()

    variables, clauses = read_cnf(SOURCE)
    labels = semantic_labels()
    if len(labels) != len(clauses):
        raise AssertionError((len(labels), len(clauses)))
    always_remove = {
        "alpha_no_H_K4",
        "family_state_dominates_G",
        "family_nonempty",
        "port_signature_G_edge_implied_by_positive_list",
        "port_negative_list_membership",
    }
    kept: list[tuple[int, ...]] = []
    removed = {category: 0 for category in sorted(always_remove)}
    removed["nonneutral_no_full_clauses"] = 0
    for clause, label in zip(clauses, labels, strict=True):
        if label in always_remove:
            removed[label] += 1
            continue
        if label == "anchor_no_full_response" and no_full_target(clause) not in {
            7,
            8,
            9,
        }:
            removed["nonneutral_no_full_clauses"] += 1
            continue
        kept.append(clause)

    raw = dimacs(variables, kept)
    args.instance.write_text(raw, encoding="ascii")
    started = time.monotonic()
    try:
        completed = subprocess.run(
            [
                str(args.solver),
                "--quiet",
                "--binary=false",
                str(args.instance),
                str(args.proof),
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
    payload = {
        "status": status,
        "variables": variables,
        "clauses": len(kept),
        "removed": removed,
        "sha256": hashlib.sha256(raw.encode("ascii")).hexdigest(),
        "elapsed_seconds": time.monotonic() - started,
        "solver_return_code": return_code,
        "solver_output": output,
    }
    args.summary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    raise SystemExit(10 if status == "SAT" else 20 if status == "UNSAT" else 124)


if __name__ == "__main__":
    main()
