#!/usr/bin/env python3
"""Independently check a fixed-core, two-new-vertex DPLL tree.

Given a 42-vertex graph and a deleted original vertex, this checker rebuilds
the 41-vertex labeled core and all clauses for adding vertices A and B:

* variables 0..40: A--core edges;
* variables 41..81: B--core edges;
* variable 82: A--B;
* homogeneous core 4-sets give width-4 clauses for A and separately B;
* homogeneous core triples give width-7 clauses involving A, B, and A--B.

The version-2 binary proof format is:

* bytes 0..7: ASCII ``CORE2DP2``;
* byte 8: original graph order (42);
* bytes 9..12: one-based catalog data-line number;
* byte 13: deleted original vertex;
* byte 14: variable count (83);
* bytes 15..18: little-endian original-clause count;
* remaining bytes: a preorder full binary tree, where 0..82 branches false
  then true and 255 marks an original-clause unit-propagation conflict.

The checker remains backward compatible with the original 15-byte
``CORE2DP1`` header, which implicitly refers to catalog line 1.

No solver code, clause file, learned clause, or claimed branch heuristic is
trusted.  The checker decodes graph6, reconstructs the core and formula,
checks the core itself, replays unit closure, and checks exhaustive coverage.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from dataclasses import dataclass
from pathlib import Path


MAGIC = b"CORE2DP1"
MAGIC_V2 = b"CORE2DP2"
LEAF = 255
INPUT_ORDER = 42
CORE_ORDER = 41
VARIABLE_COUNT = 83


def select_data_line(raw: bytes, line_number: int = 1) -> bytes:
    """Select a one-based nonempty, noncomment data line independently."""
    if line_number < 1:
        raise ValueError("catalog line number must be positive")
    lines = [
        line.strip()
        for line in raw.splitlines()
        if line.strip() and not line.lstrip().startswith(b"#")
    ]
    if line_number > len(lines):
        raise ValueError(
            f"catalog line {line_number} outside 1..{len(lines)}"
        )
    return lines[line_number - 1]


def decode_short_graph6(raw: bytes, line_number: int = 1) -> list[int]:
    """Decode one selected short-graph6 line without project imports."""
    line = select_data_line(raw, line_number)
    if line.startswith(b">>graph6<<"):
        line = line[len(b">>graph6<<") :]
    if not line:
        raise ValueError("empty graph6 input")
    n = line[0] - 63
    if not 0 <= n <= 62:
        raise ValueError("checker supports only short graph6 (n <= 62)")
    needed = n * (n - 1) // 2
    if 6 * (len(line) - 1) < needed:
        raise ValueError("truncated graph6 input")
    adjacency = [0] * n
    bit_index = 0
    for right in range(1, n):
        for left in range(right):
            value = line[1 + bit_index // 6] - 63
            if not 0 <= value < 64:
                raise ValueError("invalid graph6 payload byte")
            if (value >> (5 - bit_index % 6)) & 1:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            bit_index += 1
    return adjacency


def delete_vertex(adjacency: list[int], deleted: int) -> list[int]:
    if len(adjacency) != INPUT_ORDER:
        raise ValueError("this certificate requires a 42-vertex input")
    if not 0 <= deleted < len(adjacency):
        raise ValueError("deleted vertex is out of range")
    old_vertices = [v for v in range(len(adjacency)) if v != deleted]
    core = [0] * len(old_vertices)
    for left, old_left in enumerate(old_vertices):
        for right in range(left + 1, len(old_vertices)):
            old_right = old_vertices[right]
            if (adjacency[old_left] >> old_right) & 1:
                core[left] |= 1 << right
                core[right] |= 1 << left
    return core


def homogeneous_count(adjacency: list[int], vertices: tuple[int, ...]) -> int:
    return sum(
        (adjacency[left] >> right) & 1
        for left, right in itertools.combinations(vertices, 2)
    )


def check_core(adjacency: list[int]) -> tuple[int, int]:
    k5_count = 0
    i5_count = 0
    for vertices in itertools.combinations(range(len(adjacency)), 5):
        edges = homogeneous_count(adjacency, vertices)
        i5_count += edges == 0
        k5_count += edges == 10
    if k5_count or i5_count:
        raise ValueError(
            "fixed core already violates (5,5): "
            f"K5={k5_count} independent5={i5_count}"
        )
    return k5_count, i5_count


@dataclass(frozen=True)
class Formula:
    clauses: tuple[tuple[int, bool], ...]
    core_k4: int
    core_i4: int
    core_k3: int
    core_i3: int

    @property
    def negative_count(self) -> int:
        return 2 * self.core_k4 + self.core_k3

    @property
    def positive_count(self) -> int:
        return 2 * self.core_i4 + self.core_i3


def build_formula(core: list[int]) -> Formula:
    if len(core) != CORE_ORDER:
        raise ValueError("internal core order is not 41")
    clauses: list[tuple[int, bool]] = []
    core_k4 = core_i4 = core_k3 = core_i3 = 0
    for vertices in itertools.combinations(range(CORE_ORDER), 4):
        edges = homogeneous_count(core, vertices)
        if edges not in (0, 6):
            continue
        a_mask = sum(1 << vertex for vertex in vertices)
        positive = edges == 0
        clauses.append((a_mask, positive))
        clauses.append((a_mask << CORE_ORDER, positive))
        if positive:
            core_i4 += 1
        else:
            core_k4 += 1
    ab_bit = 1 << (2 * CORE_ORDER)
    for vertices in itertools.combinations(range(CORE_ORDER), 3):
        edges = homogeneous_count(core, vertices)
        if edges not in (0, 3):
            continue
        a_mask = sum(1 << vertex for vertex in vertices)
        both_mask = a_mask | (a_mask << CORE_ORDER) | ab_bit
        positive = edges == 0
        clauses.append((both_mask, positive))
        if positive:
            core_i3 += 1
        else:
            core_k3 += 1
    formula = Formula(
        tuple(clauses), core_k4, core_i4, core_k3, core_i3
    )
    if formula.negative_count + formula.positive_count != len(clauses):
        raise AssertionError("formula clause-count accounting failed")
    return formula


def canonical_dimacs(formula: Formula) -> bytes:
    """Render a stable, sorted DIMACS representation for formula hashing."""
    signed_clauses = []
    for mask, positive in formula.clauses:
        signed_clauses.append(
            tuple(
                variable + 1 if positive else -(variable + 1)
                for variable in range(VARIABLE_COUNT)
                if (mask >> variable) & 1
            )
        )
    signed_clauses.sort()
    lines = [
        "c canonical core_completion_proof formula v1",
        f"p cnf {VARIABLE_COUNT} {len(signed_clauses)}",
    ]
    lines.extend(
        " ".join(str(literal) for literal in clause) + " 0"
        for clause in signed_clauses
    )
    return ("\n".join(lines) + "\n").encode("ascii")


def unit_closure(
    clauses: tuple[tuple[int, bool], ...],
    true_mask: int,
    false_mask: int,
) -> tuple[bool, int, int, int]:
    """Return (conflict, true, false, number of newly assigned units)."""
    if true_mask & false_mask:
        raise ValueError("internally inconsistent assignment")
    units = 0
    while True:
        changed = False
        assigned = true_mask | false_mask
        for clause_mask, positive in clauses:
            satisfying = clause_mask & (true_mask if positive else false_mask)
            if satisfying:
                continue
            remaining = clause_mask & ~assigned
            if remaining == 0:
                return True, true_mask, false_mask, units
            if remaining.bit_count() == 1:
                if positive:
                    true_mask |= remaining
                else:
                    false_mask |= remaining
                units += 1
                changed = True
                break
        if not changed:
            return False, true_mask, false_mask, units


@dataclass
class CheckStats:
    nodes: int = 0
    branches: int = 0
    leaves: int = 0
    unit_assignments: int = 0
    max_depth: int = 0


class TreeChecker:
    def __init__(self, payload: bytes, clauses: tuple[tuple[int, bool], ...]):
        self.payload = payload
        self.clauses = clauses
        self.cursor = 0
        self.stats = CheckStats()

    def check_node(
        self, true_mask: int, false_mask: int, depth: int = 0
    ) -> None:
        self.stats.nodes += 1
        self.stats.max_depth = max(self.stats.max_depth, depth)
        conflict, true_mask, false_mask, units = unit_closure(
            self.clauses, true_mask, false_mask
        )
        self.stats.unit_assignments += units
        if self.cursor >= len(self.payload):
            raise ValueError(f"truncated tree at node {self.stats.nodes}")
        code = self.payload[self.cursor]
        self.cursor += 1
        if code == LEAF:
            self.stats.leaves += 1
            if not conflict:
                raise ValueError(
                    f"leaf {self.stats.leaves} has no original-clause conflict"
                )
            return
        self.stats.branches += 1
        if conflict:
            raise ValueError("branch occurs after unit propagation conflicts")
        if code >= VARIABLE_COUNT:
            raise ValueError(f"invalid branch-variable byte {code}")
        bit = 1 << code
        if (true_mask | false_mask) & bit:
            raise ValueError(f"branch variable {code} is already assigned")
        self.check_node(true_mask, false_mask | bit, depth + 1)
        self.check_node(true_mask | bit, false_mask, depth + 1)

    def run(self) -> CheckStats:
        self.check_node(0, 0)
        if self.cursor != len(self.payload):
            raise ValueError(
                f"{len(self.payload) - self.cursor} trailing proof byte(s)"
            )
        if self.stats.leaves != self.stats.branches + 1:
            raise ValueError("tree is not full binary")
        return self.stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", required=True, type=Path)
    parser.add_argument("--proof", required=True, type=Path)
    parser.add_argument("--line", type=int, default=1)
    parser.add_argument("--delete", required=True, type=int)
    args = parser.parse_args()
    started = time.perf_counter()

    graph_raw = args.graph.read_bytes()
    selected_graph6 = select_data_line(graph_raw, args.line)
    input_graph = decode_short_graph6(graph_raw, args.line)
    core = delete_vertex(input_graph, args.delete)
    core_k5, core_i5 = check_core(core)
    formula = build_formula(core)
    formula_raw = canonical_dimacs(formula)
    proof_raw = args.proof.read_bytes()
    if len(proof_raw) < 15:
        raise ValueError("proof is shorter than its header")
    if proof_raw[:8] == MAGIC:
        header_bytes = 15
        recorded_catalog_line = 1
        recorded_deleted = proof_raw[9]
        recorded_variables = proof_raw[10]
        recorded_clause_count = int.from_bytes(proof_raw[11:15], "little")
    elif proof_raw[:8] == MAGIC_V2:
        if len(proof_raw) < 19:
            raise ValueError("version-2 proof is shorter than its header")
        header_bytes = 19
        recorded_catalog_line = int.from_bytes(proof_raw[9:13], "little")
        recorded_deleted = proof_raw[13]
        recorded_variables = proof_raw[14]
        recorded_clause_count = int.from_bytes(proof_raw[15:19], "little")
    else:
        raise ValueError("wrong proof magic/version")
    if proof_raw[8] != len(input_graph):
        raise ValueError("proof input order does not match graph")
    if recorded_catalog_line != args.line:
        raise ValueError("proof catalog line does not match --line")
    if recorded_deleted != args.delete:
        raise ValueError("proof deleted vertex does not match --delete")
    if recorded_variables != VARIABLE_COUNT:
        raise ValueError("proof variable count is not 83")
    if recorded_clause_count != len(formula.clauses):
        raise ValueError("proof clause count does not match reconstructed formula")

    stats = TreeChecker(proof_raw[header_bytes:], formula.clauses).run()
    result = {
        "status": "VERIFIED_UNSAT_FIXED_41_CORE_TWO_VERTEX_COMPLETION",
        "graph": str(args.graph),
        "graph_sha256": hashlib.sha256(graph_raw).hexdigest(),
        "selected_graph6_sha256": hashlib.sha256(
            selected_graph6 + b"\n"
        ).hexdigest(),
        "catalog_line": args.line,
        "proof_format": proof_raw[:8].decode("ascii"),
        "deleted_original_vertex": args.delete,
        "core_order": len(core),
        "core_k5": core_k5,
        "core_independent5": core_i5,
        "variables": VARIABLE_COUNT,
        "core_k4": formula.core_k4,
        "core_independent4": formula.core_i4,
        "core_k3": formula.core_k3,
        "core_independent3": formula.core_i3,
        "negative_clauses": formula.negative_count,
        "positive_clauses": formula.positive_count,
        "clauses": len(formula.clauses),
        "canonical_cnf_sha256": hashlib.sha256(formula_raw).hexdigest(),
        "proof": str(args.proof),
        "proof_sha256": hashlib.sha256(proof_raw).hexdigest(),
        "proof_bytes": len(proof_raw),
        "tree_nodes": stats.nodes,
        "tree_branches": stats.branches,
        "tree_leaves": stats.leaves,
        "unit_assignments_replayed": stats.unit_assignments,
        "max_branch_depth": stats.max_depth,
        "checker_elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
