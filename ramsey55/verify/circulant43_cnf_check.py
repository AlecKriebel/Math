#!/usr/bin/env python3
"""Independently reconstruct and check the reduced circulant-order-43 CNF."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import time
from collections import Counter
from pathlib import Path


CHECKER_ID = "ramsey55_circulant43_independent_structural_checker_v1"
N = 43
K = 5
VARIABLES = 21


def file_digest(path: Path) -> str:
    accumulator = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            data = handle.read(1_048_576)
            if not data:
                break
            accumulator.update(data)
    return accumulator.hexdigest()


def independently_expected_clauses() -> tuple[tuple[int, ...], ...]:
    patterns: set[tuple[int, ...]] = set()
    for chosen in itertools.combinations(range(N), K):
        distances: set[int] = set()
        for first_index in range(K):
            for second_index in range(first_index + 1, K):
                difference = abs(chosen[second_index] - chosen[first_index])
                distances.add(min(difference, N - difference))
        patterns.add(tuple(sorted(distances)))

    clauses: list[tuple[int, ...]] = []
    for pattern in sorted(patterns):
        clauses.append(pattern)
        clauses.append(tuple(-entry for entry in pattern))
    return tuple(clauses)


def parse_dimacs(path: Path) -> tuple[int, int, tuple[tuple[int, ...], ...]]:
    declared_variables: int | None = None
    declared_clauses: int | None = None
    clauses: list[tuple[int, ...]] = []
    pending: list[int] = []
    with path.open("r", encoding="ascii") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            fields = raw_line.split()
            if not fields or fields[0] == "c":
                continue
            if fields[0] == "p":
                if (
                    declared_variables is not None
                    or len(fields) != 4
                    or fields[1] != "cnf"
                ):
                    raise ValueError(f"invalid DIMACS header on line {line_number}")
                declared_variables = int(fields[2])
                declared_clauses = int(fields[3])
                continue
            if declared_variables is None:
                raise ValueError("clause precedes DIMACS header")
            for field in fields:
                literal = int(field)
                if literal == 0:
                    if not pending:
                        raise ValueError("empty clause is not expected")
                    clauses.append(tuple(pending))
                    pending = []
                else:
                    if abs(literal) > declared_variables:
                        raise ValueError("literal exceeds declared variable count")
                    pending.append(literal)
    if declared_variables is None or declared_clauses is None or pending:
        raise ValueError("incomplete DIMACS file")
    return declared_variables, declared_clauses, tuple(clauses)


def check(cnf: Path, metadata_path: Path) -> dict[str, object]:
    started = time.monotonic()
    expected = independently_expected_clauses()
    actual_variables, actual_declared_clauses, actual = parse_dimacs(cnf)
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    patterns = expected[0::2]
    size_histogram = Counter(len(pattern) for pattern in patterns)
    cnf_sha256 = file_digest(cnf)
    expected_histogram = {
        str(size): size_histogram[size] for size in sorted(size_histogram)
    }
    metadata_valid = (
        metadata.get("order") == N
        and metadata.get("clique_size") == K
        and metadata.get("variable_count") == VARIABLES
        and metadata.get("five_set_count") == math.comb(N, K)
        and metadata.get("unreduced_ramsey_clause_count") == 2 * math.comb(N, K)
        and metadata.get("unique_distance_signature_count") == len(patterns)
        and metadata.get("clause_count") == len(expected)
        and metadata.get("signature_size_histogram") == expected_histogram
        and metadata.get("cnf_sha256") == cnf_sha256
        and metadata.get("cnf_bytes") == cnf.stat().st_size
    )
    first_mismatch: dict[str, object] | None = None
    for index, (wanted, observed) in enumerate(
        itertools.zip_longest(expected, actual), start=1
    ):
        if wanted != observed:
            first_mismatch = {
                "clause_index": index,
                "expected": list(wanted) if wanted is not None else None,
                "actual": list(observed) if observed is not None else None,
            }
            break
    valid = (
        actual_variables == VARIABLES
        and actual_declared_clauses == len(expected)
        and len(actual) == len(expected)
        and first_mismatch is None
        and metadata_valid
    )
    return {
        "checker": CHECKER_ID,
        "valid": valid,
        "cnf_path": str(cnf.resolve()),
        "cnf_sha256": cnf_sha256,
        "cnf_bytes": cnf.stat().st_size,
        "declared_variable_count": actual_variables,
        "declared_clause_count": actual_declared_clauses,
        "actual_clause_count": len(actual),
        "expected_clause_count": len(expected),
        "unique_distance_signature_count": len(patterns),
        "signature_size_histogram": expected_histogram,
        "metadata_valid": metadata_valid,
        "first_mismatch": first_mismatch,
        "runtime_seconds": time.monotonic() - started,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    result = check(args.cnf, args.metadata)
    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
