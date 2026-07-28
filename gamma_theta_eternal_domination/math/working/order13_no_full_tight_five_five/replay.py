#!/usr/bin/env python3
"""Independent reconstruction and strict replay for the micro certificate."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys


N = 13
ANCHORS = (0, 1, 2)
EXPECTED = {
    "instance_sha256": "3d1a1379eb2a90ffd399e5a830b1a81881ed527c6e9db06574a390085cb5c1e0",
    "proof_sha256": "c4f1989ac80474a86b75ba939e494bde5928b2727fd61297eb695f3937222eee",
    "variables": 1222,
    "clauses": 24694,
    "proof_additions": 78697,
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def reconstruct() -> tuple[bytes, dict[str, int]]:
    """Reconstruct the DIMACS without importing the discovery generator."""

    next_variable = 1

    def allocate(keys):
        nonlocal next_variable
        result = {}
        for key in keys:
            result[key] = next_variable
            next_variable += 1
        return result

    vertices = tuple(range(N))
    pairs = tuple(itertools.combinations(vertices, 2))
    triples = tuple(itertools.combinations(vertices, 3))
    edge = allocate(pairs)
    family = allocate(triples)
    witness_keys = tuple(
        (u, v, w)
        for u, v in pairs
        for w in vertices
        if w not in (u, v)
    )
    witness = allocate(witness_keys)

    clauses: list[tuple[int, ...]] = []

    def add(*literals: int) -> None:
        if not literals or any(literal == 0 for literal in literals):
            raise AssertionError("bad reconstructed clause")
        clauses.append(tuple(literals))

    def e(u: int, v: int) -> int:
        return edge[(u, v) if u < v else (v, u)]

    # Each vertex pair has a named common open H-neighbor.
    for u, v in pairs:
        outside = tuple(w for w in vertices if w not in (u, v))
        add(*(witness[(u, v, w)] for w in outside))
        for w in outside:
            selector = witness[(u, v, w)]
            add(-selector, e(u, w))
            add(-selector, e(v, w))

    # Exact one-guard closure.  For each guard, one conjunct is its G move
    # edge and the other is membership of the one-swap successor.
    for state in triples:
        selected = family[state]
        for attacked in vertices:
            if attacked in state:
                continue
            options = []
            for guard in state:
                successor = tuple(
                    sorted((set(state) - {guard}) | {attacked})
                )
                options.append((-e(guard, attacked), family[successor]))
            for literals in itertools.product(*options):
                add(-selected, *literals)

    # Independent retained reference state.
    for u, v in itertools.combinations(ANCHORS, 2):
        add(e(u, v))
    add(family[ANCHORS])

    # Four vertices G-complete to the anchors.
    for q in range(8, 12):
        for anchor in ANCHORS:
            add(-e(anchor, q))

    # Positive memberships {0,2} subset L(3), {0,1} subset L(5).
    for vertex, response in ((3, (0, 2)), (5, (0, 1))):
        for anchor in response:
            successor = tuple(
                sorted((set(ANCHORS) - {anchor}) | {vertex})
            )
            add(family[successor])

    variable_count = next_variable - 1
    header = f"p cnf {variable_count} {len(clauses)}\n"
    body = "".join(
        " ".join(map(str, clause)) + " 0\n" for clause in clauses
    )
    census = {
        "edge_variables": len(edge),
        "family_variables": len(family),
        "witness_variables": len(witness),
        "variables": variable_count,
        "clauses": len(clauses),
        "unique_clauses": len(set(clauses)),
        "tautologies": sum(
            1 for clause in clauses if any(-literal in clause for literal in clause)
        ),
    }
    return (header + body).encode("ascii"), census


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path)
    args = parser.parse_args()

    here = Path(__file__).resolve().parent
    campaign = here.parents[2]
    instance_path = here / "micro-instance.cnf"
    proof_path = here / "micro-proof.additions.drat"
    checker = campaign / "tools" / "drat_trim_2023_05_22" / "drat-trim"

    reconstructed, census = reconstruct()
    actual_instance = instance_path.read_bytes()
    actual_proof = proof_path.read_bytes()
    proof_lines = actual_proof.decode("ascii").splitlines()

    checks = {
        "formula_byte_identity": reconstructed == actual_instance,
        "instance_hash": digest(actual_instance) == EXPECTED["instance_sha256"],
        "proof_hash": digest(actual_proof) == EXPECTED["proof_sha256"],
        "variable_count": census["variables"] == EXPECTED["variables"],
        "clause_count": census["clauses"] == EXPECTED["clauses"],
        "no_duplicate_clauses": census["unique_clauses"] == census["clauses"],
        "no_tautologies": census["tautologies"] == 0,
        "addition_count": len(proof_lines) == EXPECTED["proof_additions"],
        "addition_only": all(not line.startswith("d ") for line in proof_lines),
        "final_empty_clause": bool(proof_lines) and proof_lines[-1] == "0",
    }
    if not all(checks.values()):
        result = {
            "verdict": "FAIL_PRECHECK",
            "checks": checks,
            "census": census,
        }
        output = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.result:
            args.result.write_text(output, encoding="utf-8")
        print(output, end="")
        sys.exit(1)

    command = [
        str(checker),
        str(instance_path),
        str(proof_path),
        "-I",
        "-f",
        "-W",
        "-U",
        "-t",
        "60",
    ]
    completed = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    checks["drat_exit_zero"] = completed.returncode == 0
    checks["drat_verified"] = completed.stdout.count("s VERIFIED") == 1
    checks["rup_only"] = "0 RAT lemmas in core" in completed.stdout
    verdict = "PASS" if all(checks.values()) else "FAIL_REPLAY"
    result = {
        "verdict": verdict,
        "scope": (
            "order 13, gamma at least three, one independent retained "
            "triple, four additional neutral vertices, and two distinct "
            "ports carrying overlapping positive response pairs"
        ),
        "expected": EXPECTED,
        "actual": {
            "instance_sha256": digest(actual_instance),
            "proof_sha256": digest(actual_proof),
        },
        "census": census,
        "checks": checks,
        "drat_command": command,
    }
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.result:
        args.result.write_text(output, encoding="utf-8")
    print(output, end="")
    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
