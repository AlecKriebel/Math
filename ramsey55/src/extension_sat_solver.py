#!/usr/bin/env python3
"""Small deterministic exact DPLL solver with an explicit tree certificate.

This is intentionally a bounded, dependency-free solver for the 42-variable
one-vertex extension instance.  It is not intended to replace a modern
proof-producing SAT solver.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO


SOLVER_ID = "extension_sat_deterministic_dpll_v1"


class DimacsError(ValueError):
    pass


class SearchTimeout(RuntimeError):
    pass


def parse_dimacs(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    variable_count: int | None = None
    declared_clause_count: int | None = None
    clauses: list[tuple[int, ...]] = []
    pending: list[int] = []
    for line_number, raw_line in enumerate(
        path.read_text(encoding="ascii").splitlines(), 1
    ):
        line = raw_line.strip()
        if not line or line.startswith("c"):
            continue
        fields = line.split()
        if fields[0] == "p":
            if variable_count is not None or len(fields) != 4 or fields[1] != "cnf":
                raise DimacsError(f"bad problem line at {line_number}")
            variable_count = int(fields[2])
            declared_clause_count = int(fields[3])
            continue
        if variable_count is None:
            raise DimacsError(f"clause before problem line at {line_number}")
        for field in fields:
            literal = int(field)
            if literal == 0:
                clauses.append(tuple(pending))
                pending.clear()
            else:
                if abs(literal) > variable_count:
                    raise DimacsError(
                        f"literal out of range at line {line_number}: {literal}"
                    )
                pending.append(literal)
    if variable_count is None or declared_clause_count is None:
        raise DimacsError("missing problem line")
    if pending:
        raise DimacsError("unterminated final clause")
    if len(clauses) != declared_clause_count:
        raise DimacsError(
            f"declared {declared_clause_count} clauses but read {len(clauses)}"
        )
    return variable_count, clauses


@dataclass
class SearchStats:
    nodes: int = 0
    decisions: int = 0
    propagations: int = 0
    conflicts: int = 0
    maximum_depth: int = 0


class DpllSolver:
    def __init__(
        self,
        variable_count: int,
        clauses: list[tuple[int, ...]],
        deadline: float,
    ) -> None:
        self.variable_count = variable_count
        self.clauses = clauses
        self.deadline = deadline
        self.assignment = [-1] * (variable_count + 1)
        self.stats = SearchStats()
        self.proof_records: list[tuple[str, int, int | None]] = []

    def _check_deadline(self) -> None:
        if time.monotonic() > self.deadline:
            raise SearchTimeout

    def _clause_state(
        self, clause: tuple[int, ...]
    ) -> tuple[bool, list[int]]:
        unknown: list[int] = []
        for literal in clause:
            value = self.assignment[abs(literal)]
            if value < 0:
                unknown.append(literal)
            elif bool(value) == (literal > 0):
                return True, []
        return False, unknown

    def _rollback(self, trail: list[int], start: int) -> None:
        for variable in reversed(trail[start:]):
            self.assignment[variable] = -1
        del trail[start:]

    def _choose_variable(self) -> int:
        scores = [0] * (self.variable_count + 1)
        for clause in self.clauses:
            satisfied, unknown = self._clause_state(clause)
            if satisfied:
                continue
            # Short unresolved clauses get exponentially more weight.
            weight = 1 << max(0, 8 - len(unknown))
            for literal in unknown:
                scores[abs(literal)] += weight
        return max(
            (v for v in range(1, self.variable_count + 1) if self.assignment[v] < 0),
            key=lambda v: (scores[v], -v),
        )

    def _search(self, trail: list[int], depth: int) -> list[int] | None:
        self._check_deadline()
        self.stats.nodes += 1
        self.stats.maximum_depth = max(self.stats.maximum_depth, depth)
        node_trail_start = len(trail)

        while True:
            self._check_deadline()
            unit: tuple[int, int] | None = None
            all_satisfied = True
            for clause_index, clause in enumerate(self.clauses, 1):
                satisfied, unknown = self._clause_state(clause)
                if satisfied:
                    continue
                all_satisfied = False
                if not unknown:
                    self.stats.conflicts += 1
                    self.proof_records.append(("x", clause_index, None))
                    self._rollback(trail, node_trail_start)
                    return None
                if len(unknown) == 1:
                    unit = (unknown[0], clause_index)
                    break
            if unit is None:
                if all_satisfied:
                    model = self.assignment.copy()
                    for variable in range(1, self.variable_count + 1):
                        if model[variable] < 0:
                            model[variable] = 0
                    self._rollback(trail, node_trail_start)
                    return model
                break
            literal, reason_clause = unit
            variable = abs(literal)
            value = int(literal > 0)
            if self.assignment[variable] >= 0:
                raise AssertionError("unit propagation selected an assigned variable")
            self.assignment[variable] = value
            trail.append(variable)
            self.stats.propagations += 1
            self.proof_records.append(("u", literal, reason_clause))

        variable = self._choose_variable()
        self.stats.decisions += 1
        self.proof_records.append(("b", variable, None))
        branch_trail_start = len(trail)

        self.assignment[variable] = 0
        trail.append(variable)
        model = self._search(trail, depth + 1)
        self._rollback(trail, branch_trail_start)
        if model is not None:
            self._rollback(trail, node_trail_start)
            return model

        self.assignment[variable] = 1
        trail.append(variable)
        model = self._search(trail, depth + 1)
        self._rollback(trail, branch_trail_start)
        self._rollback(trail, node_trail_start)
        return model

    def solve(self) -> list[int] | None:
        return self._search([], 0)


def model_satisfies(
    model: list[int], clauses: list[tuple[int, ...]]
) -> bool:
    return all(
        any(bool(model[abs(literal)]) == (literal > 0) for literal in clause)
        for clause in clauses
    )


def write_proof(
    stream: TextIO,
    variable_count: int,
    cnf_sha256: str,
    records: list[tuple[str, int, int | None]],
) -> None:
    stream.write("c extension_sat_dpll_tree_v1\n")
    stream.write(f"c cnf_sha256 {cnf_sha256}\n")
    stream.write(f"p tree {variable_count} {len(records)}\n")
    for kind, first, second in records:
        if kind == "u":
            stream.write(f"u {first} {second}\n")
        else:
            stream.write(f"{kind} {first}\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--time-limit", type=float, default=60.0)
    parser.add_argument("--proof", type=Path)
    args = parser.parse_args()
    if args.time_limit <= 0:
        raise SystemExit("--time-limit must be positive")

    cnf_bytes = args.cnf.read_bytes()
    cnf_sha256 = hashlib.sha256(cnf_bytes).hexdigest()
    variable_count, clauses = parse_dimacs(args.cnf)
    start = time.monotonic()
    solver = DpllSolver(
        variable_count,
        clauses,
        deadline=start + args.time_limit,
    )
    try:
        model = solver.solve()
    except SearchTimeout:
        result = {
            "solver": SOLVER_ID,
            "status": "TIMEOUT",
            "cnf_sha256": cnf_sha256,
            "variable_count": variable_count,
            "clause_count": len(clauses),
            "runtime_seconds": time.monotonic() - start,
            **vars(solver.stats),
        }
        print(json.dumps(result, sort_keys=True))
        return 2

    runtime = time.monotonic() - start
    status = "SAT" if model is not None else "UNSAT"
    if model is not None and not model_satisfies(model, clauses):
        raise AssertionError("internal model check failed")

    proof_sha256: str | None = None
    if model is None and args.proof:
        args.proof.parent.mkdir(parents=True, exist_ok=True)
        with args.proof.open("w", encoding="ascii", newline="\n") as stream:
            write_proof(
                stream,
                variable_count,
                cnf_sha256,
                solver.proof_records,
            )
        proof_sha256 = hashlib.sha256(args.proof.read_bytes()).hexdigest()

    result: dict[str, object] = {
        "solver": SOLVER_ID,
        "status": status,
        "cnf_sha256": cnf_sha256,
        "variable_count": variable_count,
        "clause_count": len(clauses),
        "runtime_seconds": runtime,
        "proof_record_count": len(solver.proof_records),
        "proof_sha256": proof_sha256,
        **vars(solver.stats),
    }
    if model is not None:
        result["true_variables"] = [
            variable for variable in range(1, variable_count + 1) if model[variable]
        ]
    print(json.dumps(result, sort_keys=True))
    return 10 if model is not None else 20


if __name__ == "__main__":
    raise SystemExit(main())
