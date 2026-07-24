#!/usr/bin/env python3
"""Independent audit of a materialized residual-completion result.

The checker imports neither completion generator nor project graph utilities.
It reconstructs candidate values, checks the fixed boundary, compares the
completion CNF to the base clauses plus sorted units, and reruns both external
proof checkers for a claimed certified UNSAT result.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
import time
from pathlib import Path
from typing import Iterable


CHECKER_ID = "ramsey55_residual_completion_independent_checker_v1"
PINNED = {
    "drat_trim": "f58f63b0f76945d4c4c9ff6e87afaf870f579e67c0f7cca589492df8fc7ebd47",
    "lrat_check": "bd7eb8052623525814a0a37502b47f05375d9d9dfaf96ddc2fcd858958517cea",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_dimacs(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    variables: int | None = None
    expected: int | None = None
    clauses: list[tuple[int, ...]] = []
    pending: list[int] = []
    for line_number, raw in enumerate(
        path.read_text(encoding="ascii").splitlines(), start=1
    ):
        fields = raw.split()
        if not fields or fields[0] == "c":
            continue
        if fields[0] == "p":
            if variables is not None or len(fields) != 4 or fields[1] != "cnf":
                raise ValueError(f"bad DIMACS header at line {line_number}")
            variables, expected = int(fields[2]), int(fields[3])
            continue
        if variables is None:
            raise ValueError(f"clause before header at line {line_number}")
        for field in fields:
            literal = int(field)
            if literal:
                if not 1 <= abs(literal) <= variables:
                    raise ValueError("DIMACS literal outside declared range")
                pending.append(literal)
            else:
                clauses.append(tuple(pending))
                pending = []
    if variables is None or expected is None or pending or len(clauses) != expected:
        raise ValueError("malformed or incomplete DIMACS")
    return variables, clauses


def decode_graph6(text: str) -> list[int]:
    raw = text.strip()
    if raw.startswith(">>graph6<<"):
        raw = raw[len(">>graph6<<") :]
    if not raw:
        raise ValueError("empty graph6")
    order = ord(raw[0]) - 63
    if not 0 <= order <= 62:
        raise ValueError("only short graph6 is supported")
    adjacency = [0] * order
    bit = 0
    for right in range(1, order):
        for left in range(right):
            value = ord(raw[1 + bit // 6]) - 63
            if not 0 <= value < 64:
                raise ValueError("invalid graph6 payload")
            if (value >> (5 - bit % 6)) & 1:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            bit += 1
    return adjacency


def read_candidate_graph(path: Path) -> list[int]:
    if path.suffix.lower() == ".json":
        value = json.loads(path.read_text(encoding="utf-8"))
        if "graph6" not in value:
            raise ValueError("independent checker requires graph6 candidate JSON")
        return decode_graph6(str(value["graph6"]))
    lines = [
        line.strip()
        for line in path.read_text(encoding="ascii").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    if len(lines) != 1:
        raise ValueError("candidate graph file must have exactly one data line")
    return decode_graph6(lines[0])


def checker_says_verified(output: str) -> bool:
    return any(
        "VERIFIED" in line and "NOT VERIFIED" not in line
        for line in output.splitlines()
    )


def count_forbidden(adjacency: list[int]) -> tuple[int, int]:
    cliques = independent = 0
    for vertices in itertools.combinations(range(len(adjacency)), 5):
        values = [
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        ]
        cliques += int(all(values))
        independent += int(not any(values))
    return cliques, independent


def check(
    *,
    base_cnf: Path,
    base_metadata: Path,
    candidate_path: Path,
    completion_cnf: Path,
    result_path: Path,
    proof: Path,
    lrat: Path,
    drat_trim: Path,
    lrat_check: Path,
) -> dict[str, object]:
    started = time.monotonic()
    metadata = json.loads(base_metadata.read_text(encoding="utf-8"))
    result = json.loads(result_path.read_text(encoding="utf-8"))
    base_variables, base_clauses = read_dimacs(base_cnf)
    completion_variables, completion_clauses = read_dimacs(completion_cnf)
    candidate = read_candidate_graph(candidate_path)
    base_graph = decode_graph6(str(metadata["base_graph6"]))
    free_edges = tuple(
        (int(edge[0]), int(edge[1])) for edge in metadata["free_edges"]
    )
    free_set = set(free_edges)

    errors: list[str] = []
    if len(candidate) != len(base_graph):
        errors.append("candidate order differs from base order")
    boundary_mismatches = sum(
        ((candidate[left] >> right) & 1)
        != ((base_graph[left] >> right) & 1)
        for left, right in itertools.combinations(range(len(base_graph)), 2)
        if (left, right) not in free_set
    )
    if boundary_mismatches:
        errors.append("candidate changes a fixed-boundary edge")

    assignment = tuple(
        bool((candidate[left] >> right) & 1) for left, right in free_edges
    )
    fixed = tuple(int(value) for value in result["fixed_variables"])
    if fixed != tuple(sorted(set(fixed))):
        errors.append("fixed-variable list is not unique and sorted")
    units = tuple(
        (variable if assignment[variable - 1] else -variable,)
        for variable in fixed
    )
    if completion_variables != base_variables:
        errors.append("completion changes the variable count")
    if completion_clauses != base_clauses + list(units):
        errors.append("completion is not base clauses followed by candidate units")

    hashes = {
        "base_cnf_sha256": sha256_file(base_cnf),
        "candidate_sha256": sha256_file(candidate_path),
        "completion_cnf_sha256": sha256_file(completion_cnf),
        "result_sha256": sha256_file(result_path),
        "proof_sha256": sha256_file(proof) if proof.is_file() else None,
        "lrat_sha256": sha256_file(lrat) if lrat.is_file() else None,
    }
    for field in ("base_cnf_sha256", "candidate_sha256", "completion_cnf_sha256"):
        if result.get(field) != hashes[field]:
            errors.append(f"result {field} mismatch")

    status = result.get("status")
    drat_valid: bool | None = None
    lrat_valid: bool | None = None
    model_forbidden: tuple[int, int] | None = None
    if status == "CERTIFIED_UNSAT":
        if (
            not proof.is_file()
            or not lrat.is_file()
            or result.get("proof_sha256") != hashes["proof_sha256"]
            or result.get("lrat_sha256") != hashes["lrat_sha256"]
        ):
            errors.append("proof artifact or recorded hash is missing")
        if sha256_file(drat_trim) != PINNED["drat_trim"]:
            errors.append("drat-trim hash is not pinned")
        if sha256_file(lrat_check) != PINNED["lrat_check"]:
            errors.append("lrat-check hash is not pinned")
        if not errors:
            drat = subprocess.run(
                (
                    str(drat_trim),
                    str(completion_cnf),
                    str(proof),
                    "-I",
                ),
                text=True,
                capture_output=True,
                check=False,
            )
            drat_valid = drat.returncode == 0 and checker_says_verified(
                drat.stdout + drat.stderr
            )
            lrat_result = subprocess.run(
                (str(lrat_check), str(completion_cnf), str(lrat)),
                text=True,
                capture_output=True,
                check=False,
            )
            lrat_valid = (
                lrat_result.returncode == 0
                and checker_says_verified(
                    lrat_result.stdout + lrat_result.stderr
                )
            )
            if not drat_valid or not lrat_valid:
                errors.append("an independent proof checker rejected the result")
    elif status == "SAT":
        true_set = {int(value) for value in result["true_variables"]}
        if not all(
            any((literal > 0) == (abs(literal) in true_set) for literal in clause)
            for clause in completion_clauses
        ):
            errors.append("SAT model does not satisfy completion formula")
        completed_graph = base_graph.copy()
        for variable, (left, right) in enumerate(free_edges, start=1):
            if variable in true_set:
                completed_graph[left] |= 1 << right
                completed_graph[right] |= 1 << left
            else:
                completed_graph[left] &= ~(1 << right)
                completed_graph[right] &= ~(1 << left)
        model_forbidden = count_forbidden(completed_graph)
        if model_forbidden != (0, 0):
            errors.append("SAT model graph has a forbidden five-set")
    elif status == "TIMEOUT":
        if result.get("proof_written") or result.get("lrat_written"):
            errors.append("timeout result claims a proof artifact")
    else:
        errors.append(f"unsupported result status {status}")

    return {
        "checker": CHECKER_ID,
        "valid": not errors,
        "status": status,
        "errors": errors,
        "base_variable_count": base_variables,
        "base_clause_count": len(base_clauses),
        "completion_clause_count": len(completion_clauses),
        "fixed_variable_count": len(fixed),
        "free_variable_count": base_variables - len(fixed),
        "fixed_boundary_mismatch_count": boundary_mismatches,
        "exact_formula_match": completion_clauses == base_clauses + list(units),
        "drat_trim_valid": drat_valid,
        "lrat_check_valid": lrat_valid,
        "model_forbidden_counts": list(model_forbidden) if model_forbidden else None,
        "hashes": hashes,
        "runtime_seconds": time.monotonic() - started,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--base-metadata", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--completion-cnf", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--proof", type=Path, required=True)
    parser.add_argument("--lrat", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--lrat-check", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = check(
            base_cnf=args.base_cnf,
            base_metadata=args.base_metadata,
            candidate_path=args.candidate,
            completion_cnf=args.completion_cnf,
            result_path=args.result,
            proof=args.proof,
            lrat=args.lrat,
            drat_trim=args.drat_trim,
            lrat_check=args.lrat_check,
        )
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        result = {
            "checker": CHECKER_ID,
            "valid": False,
            "errors": [str(error)],
        }
    rendered = json.dumps(result, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    print(rendered)
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
