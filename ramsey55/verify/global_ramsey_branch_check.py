#!/usr/bin/env python3
"""Independently check a materialized global degree branch.

This checker deliberately does not import the branch generator.  It compares
the base and branch DIMACS clause streams, reconstructs the vertex-0 unit
clauses from the documented lexicographic edge-variable order, and checks the
recorded metadata and SHA-256 digests.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Generator


CHECKER_ID = "ramsey55_global_vertex0_degree_branch_checker_v1"
EXPECTED_GENERATOR_ID = "ramsey55_global_vertex0_degree_branch_v1"
ORDER = 43
ALLOWED_DEGREES = (18, 19, 20, 21)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def independent_edge_variable(
    order: int, left: int, right: int
) -> int:
    if not 0 <= left < right < order:
        raise ValueError("edge endpoints are outside the ordered graph")
    preceding = left * (2 * order - left - 1) // 2
    return preceding + (right - left)


def independent_units(order: int, degree: int) -> tuple[int, ...]:
    return tuple(
        (
            independent_edge_variable(order, 0, vertex)
            if vertex <= degree
            else -independent_edge_variable(order, 0, vertex)
        )
        for vertex in range(1, order)
    )


def dimacs_clause_stream(
    path: Path,
) -> Generator[tuple[int, ...], None, dict[str, object]]:
    declared_variables: int | None = None
    declared_clauses: int | None = None
    actual_clauses = 0
    current: list[int] = []
    comments: list[str] = []
    with path.open("rb") as source:
        for line_number, raw in enumerate(source, start=1):
            try:
                fields = raw.decode("ascii").split()
            except UnicodeDecodeError as error:
                raise ValueError(
                    f"{path}: non-ASCII input at line {line_number}"
                ) from error
            if not fields:
                continue
            if fields[0] == "c":
                comments.append(" ".join(fields[1:]))
                continue
            if fields[0] == "p":
                if (
                    declared_variables is not None
                    or len(fields) != 4
                    or fields[1] != "cnf"
                ):
                    raise ValueError(
                        f"{path}: invalid or duplicate header at line "
                        f"{line_number}"
                    )
                declared_variables = int(fields[2])
                declared_clauses = int(fields[3])
                continue
            if declared_variables is None:
                raise ValueError(
                    f"{path}: clause before header at line {line_number}"
                )
            for field in fields:
                literal = int(field)
                if literal:
                    if abs(literal) > declared_variables:
                        raise ValueError(
                            f"{path}: literal outside declared range at line "
                            f"{line_number}"
                        )
                    current.append(literal)
                else:
                    actual_clauses += 1
                    yield tuple(current)
                    current = []
    if current:
        raise ValueError(f"{path}: unterminated final clause")
    if declared_variables is None or declared_clauses is None:
        raise ValueError(f"{path}: missing DIMACS header")
    return {
        "declared_variable_count": declared_variables,
        "declared_clause_count": declared_clauses,
        "actual_clause_count": actual_clauses,
        "comments": comments,
    }


def next_or_summary(
    stream: Generator[tuple[int, ...], None, dict[str, object]],
) -> tuple[tuple[int, ...] | None, dict[str, object] | None]:
    try:
        return next(stream), None
    except StopIteration as stopped:
        return None, stopped.value


def check_branch(
    base_cnf: Path,
    branch_cnf: Path,
    metadata_path: Path,
    degree: int,
) -> dict[str, object]:
    if degree not in ALLOWED_DEGREES:
        raise ValueError(f"degree must be one of {ALLOWED_DEGREES}")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    base_sha256 = sha256_file(base_cnf)
    branch_sha256 = sha256_file(branch_cnf)
    expected_units = independent_units(ORDER, degree)

    base_stream = dimacs_clause_stream(base_cnf)
    branch_stream = dimacs_clause_stream(branch_cnf)
    first_mismatch: dict[str, object] | None = None
    copied_clause_count = 0
    base_summary: dict[str, object] | None = None
    branch_summary: dict[str, object] | None = None

    while base_summary is None:
        expected_clause, base_summary = next_or_summary(base_stream)
        if base_summary is not None:
            break
        actual_clause, early_summary = next_or_summary(branch_stream)
        if early_summary is not None:
            branch_summary = early_summary
            if first_mismatch is None:
                first_mismatch = {
                    "kind": "branch_ended_before_base",
                    "clause_index": copied_clause_count + 1,
                }
            break
        copied_clause_count += 1
        if first_mismatch is None and actual_clause != expected_clause:
            first_mismatch = {
                "kind": "copied_clause",
                "clause_index": copied_clause_count,
                "expected": list(expected_clause or ()),
                "actual": list(actual_clause or ()),
            }

    observed_units: list[tuple[int, ...]] = []
    if branch_summary is None:
        while True:
            clause, branch_summary = next_or_summary(branch_stream)
            if branch_summary is not None:
                break
            assert clause is not None
            observed_units.append(clause)

    assert base_summary is not None
    assert branch_summary is not None
    expected_unit_clauses = [(literal,) for literal in expected_units]
    branch_comments = branch_summary["comments"]
    assert isinstance(branch_comments, list)

    checks = {
        "base_declared_equals_actual": (
            base_summary["declared_clause_count"]
            == base_summary["actual_clause_count"]
        ),
        "branch_declared_equals_actual": (
            branch_summary["declared_clause_count"]
            == branch_summary["actual_clause_count"]
        ),
        "variable_count_unchanged": (
            branch_summary["declared_variable_count"]
            == base_summary["declared_variable_count"]
        ),
        "all_base_clauses_copied_in_order": (
            first_mismatch is None
            and copied_clause_count == base_summary["actual_clause_count"]
        ),
        "remaining_clauses_are_expected_units": (
            observed_units == expected_unit_clauses
        ),
        "branch_clause_increment_is_42": (
            branch_summary["actual_clause_count"]
            == base_summary["actual_clause_count"] + ORDER - 1
        ),
        "generator_comment_present": (
            f"branch_generator {EXPECTED_GENERATOR_ID}" in branch_comments
        ),
        "degree_comment_present": (
            f"vertex0_degree {degree}" in branch_comments
        ),
        "metadata_degree": metadata.get("degree") == degree,
        "metadata_order": metadata.get("order") == ORDER,
        "metadata_generator": (
            metadata.get("generator") == EXPECTED_GENERATOR_ID
        ),
        "metadata_base_sha256": (
            metadata.get("base_cnf_sha256") == base_sha256
        ),
        "metadata_branch_sha256": (
            metadata.get("cnf_sha256") == branch_sha256
        ),
        "metadata_unit_literals": (
            metadata.get("unit_literals") == list(expected_units)
        ),
        "metadata_variable_count": (
            metadata.get("variable_count")
            == branch_summary["declared_variable_count"]
        ),
        "metadata_clause_count": (
            metadata.get("clause_count")
            == branch_summary["declared_clause_count"]
        ),
        "metadata_byte_count": (
            metadata.get("cnf_bytes") == branch_cnf.stat().st_size
        ),
    }
    result: dict[str, object] = {
        "checker": CHECKER_ID,
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "valid": all(checks.values()),
        "degree": degree,
        "base_cnf_sha256": base_sha256,
        "branch_cnf_sha256": branch_sha256,
        "metadata_sha256": sha256_file(metadata_path),
        "copied_clause_count": copied_clause_count,
        "observed_unit_clause_count": len(observed_units),
        "expected_unit_literals": list(expected_units),
        "base_summary": base_summary,
        "branch_summary": branch_summary,
        "checks": checks,
    }
    if first_mismatch is not None:
        result["first_mismatch"] = first_mismatch
    if observed_units != expected_unit_clauses:
        result["observed_trailing_clauses"] = [
            list(clause) for clause in observed_units[:100]
        ]
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--branch-cnf", type=Path, required=True)
    parser.add_argument("--branch-metadata", type=Path, required=True)
    parser.add_argument("--degree", type=int, choices=ALLOWED_DEGREES, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    try:
        result = check_branch(
            args.base_cnf,
            args.branch_cnf,
            args.branch_metadata,
            args.degree,
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        result = {
            "checker": CHECKER_ID,
            "valid": False,
            "error": str(error),
        }
    result["runtime_seconds"] = time.monotonic() - started
    result["checker_source_sha256"] = hashlib.sha256(
        Path(__file__).read_bytes()
    ).hexdigest()
    rendered = json.dumps(result, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    print(rendered)
    return 0 if result.get("valid") else 1


if __name__ == "__main__":
    raise SystemExit(main())
