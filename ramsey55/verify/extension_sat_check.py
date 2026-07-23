#!/usr/bin/env python3
"""Independent checker for extension_sat_solver.py exhaustive tree proofs."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path


CHECKER_ID = "extension_sat_tree_checker_v1"


class CheckError(ValueError):
    pass


def read_cnf(path: Path) -> tuple[int, list[list[int]]]:
    variables: int | None = None
    expected: int | None = None
    clauses: list[list[int]] = []
    current: list[int] = []
    for raw in path.read_text(encoding="ascii").splitlines():
        fields = raw.split()
        if not fields or fields[0] == "c":
            continue
        if fields[0] == "p":
            if len(fields) != 4 or fields[1] != "cnf" or variables is not None:
                raise CheckError("invalid CNF header")
            variables, expected = int(fields[2]), int(fields[3])
            continue
        if variables is None:
            raise CheckError("CNF clause appears before its header")
        for token in fields:
            literal = int(token)
            if literal:
                if not 1 <= abs(literal) <= variables:
                    raise CheckError("CNF literal outside declared range")
                current.append(literal)
            else:
                clauses.append(current)
                current = []
    if variables is None or expected is None or current or len(clauses) != expected:
        raise CheckError("malformed or incomplete CNF")
    return variables, clauses


def read_proof(
    path: Path, expected_variables: int, expected_cnf_sha256: str
) -> list[tuple[str, int, int | None]]:
    records: list[tuple[str, int, int | None]] = []
    header_seen = False
    declared_records: int | None = None
    stated_cnf_sha256: str | None = None
    for raw in path.read_text(encoding="ascii").splitlines():
        fields = raw.split()
        if not fields:
            continue
        if fields[0] == "c":
            if len(fields) == 3 and fields[1] == "cnf_sha256":
                stated_cnf_sha256 = fields[2]
            continue
        if fields[0] == "p":
            if (
                header_seen
                or len(fields) != 4
                or fields[1] != "tree"
                or int(fields[2]) != expected_variables
            ):
                raise CheckError("invalid tree proof header")
            declared_records = int(fields[3])
            header_seen = True
            continue
        if not header_seen:
            raise CheckError("proof record appears before its header")
        if fields[0] == "u" and len(fields) == 3:
            records.append(("u", int(fields[1]), int(fields[2])))
        elif fields[0] in {"b", "x"} and len(fields) == 2:
            records.append((fields[0], int(fields[1]), None))
        else:
            raise CheckError(f"invalid proof record: {raw}")
    if stated_cnf_sha256 != expected_cnf_sha256:
        raise CheckError("proof names a different CNF hash")
    if not header_seen or declared_records != len(records):
        raise CheckError("proof record count does not match header")
    return records


@dataclass
class CheckerStats:
    records_checked: int = 0
    branch_records: int = 0
    unit_records: int = 0
    conflict_records: int = 0
    maximum_depth: int = 0


class TreeChecker:
    def __init__(
        self,
        variable_count: int,
        clauses: list[list[int]],
        records: list[tuple[str, int, int | None]],
    ) -> None:
        self.variable_count = variable_count
        self.clauses = clauses
        self.records = records
        self.position = 0
        self.values: dict[int, bool] = {}
        self.stats = CheckerStats()

    def _clause_status(self, clause: list[int]) -> tuple[bool, list[int]]:
        undecided: list[int] = []
        for literal in clause:
            variable = abs(literal)
            if variable not in self.values:
                undecided.append(literal)
            elif self.values[variable] == (literal > 0):
                return True, []
        return False, undecided

    def _next(self) -> tuple[str, int, int | None]:
        if self.position >= len(self.records):
            raise CheckError("proof ended before the tree was complete")
        record = self.records[self.position]
        self.position += 1
        self.stats.records_checked += 1
        return record

    def _subtree(self, depth: int) -> None:
        self.stats.maximum_depth = max(self.stats.maximum_depth, depth)
        kind, first, second = self._next()
        if kind == "x":
            clause_index = first
            if not 1 <= clause_index <= len(self.clauses):
                raise CheckError("conflict clause index is out of range")
            satisfied, undecided = self._clause_status(
                self.clauses[clause_index - 1]
            )
            if satisfied or undecided:
                raise CheckError("claimed conflict clause is not falsified")
            self.stats.conflict_records += 1
            return

        if kind == "u":
            literal = first
            clause_index = second
            if (
                not 1 <= abs(literal) <= self.variable_count
                or abs(literal) in self.values
                or clause_index is None
                or not 1 <= clause_index <= len(self.clauses)
            ):
                raise CheckError("invalid unit record")
            satisfied, undecided = self._clause_status(
                self.clauses[clause_index - 1]
            )
            if satisfied or undecided != [literal]:
                raise CheckError("unit reason is not unit with the stated literal")
            variable = abs(literal)
            self.values[variable] = literal > 0
            self.stats.unit_records += 1
            self._subtree(depth + 1)
            del self.values[variable]
            return

        if kind == "b":
            variable = first
            if not 1 <= variable <= self.variable_count or variable in self.values:
                raise CheckError("invalid branch variable")
            self.stats.branch_records += 1
            self.values[variable] = False
            self._subtree(depth + 1)
            self.values[variable] = True
            self._subtree(depth + 1)
            del self.values[variable]
            return

        raise CheckError(f"unknown proof record kind {kind}")

    def check(self) -> CheckerStats:
        self._subtree(0)
        if self.position != len(self.records):
            raise CheckError("proof has trailing records after the root tree")
        if self.values:
            raise AssertionError("checker assignment stack did not unwind")
        return self.stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("proof", type=Path)
    args = parser.parse_args()

    start = time.monotonic()
    cnf_sha256 = hashlib.sha256(args.cnf.read_bytes()).hexdigest()
    proof_sha256 = hashlib.sha256(args.proof.read_bytes()).hexdigest()
    try:
        variable_count, clauses = read_cnf(args.cnf)
        records = read_proof(args.proof, variable_count, cnf_sha256)
        stats = TreeChecker(variable_count, clauses, records).check()
    except (CheckError, ValueError, UnicodeError) as error:
        print(
            json.dumps(
                {
                    "checker": CHECKER_ID,
                    "valid": False,
                    "error": str(error),
                    "cnf_sha256": cnf_sha256,
                    "proof_sha256": proof_sha256,
                    "runtime_seconds": time.monotonic() - start,
                },
                sort_keys=True,
            )
        )
        return 1

    print(
        json.dumps(
            {
                "checker": CHECKER_ID,
                "valid": True,
                "conclusion": "UNSAT",
                "variable_count": variable_count,
                "clause_count": len(clauses),
                "cnf_sha256": cnf_sha256,
                "proof_sha256": proof_sha256,
                "runtime_seconds": time.monotonic() - start,
                **vars(stats),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
