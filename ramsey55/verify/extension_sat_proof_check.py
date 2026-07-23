#!/usr/bin/env python3
"""Independently check a compact DPLL tree for fixed vertex-extension UNSAT.

The proof format is intentionally tiny and rigid:

* bytes 0..7: ASCII ``EXTDPLL1``
* byte 8: graph order n
* bytes 9..12: little-endian original-clause count
* remaining bytes: a preorder tree
  * 0..n-1 branches on that variable (false child, then true child)
  * 255 is a leaf at which original-clause unit propagation conflicts

No derived clauses or solver decisions are trusted.  The checker independently
decodes graph6, reconstructs all K4/independent-4 clauses, performs unit
propagation, checks that every branch covers both Boolean values, and rejects
trailing or truncated data.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from dataclasses import dataclass
from pathlib import Path


MAGIC = b"EXTDPLL1"
LEAF = 255


def decode_short_graph6(raw: bytes) -> list[int]:
    """Decode one noncomment short-graph6 line without project imports."""
    lines = [
        line.strip()
        for line in raw.splitlines()
        if line.strip() and not line.startswith(b"#")
    ]
    if not lines:
        raise ValueError("graph file has no data line")
    line = lines[0]
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


def extension_clauses(adjacency: list[int]) -> tuple[list[tuple[int, bool]], int, int]:
    """Return (mask, positive) clauses plus K4 and independent-4 counts."""
    clauses: list[tuple[int, bool]] = []
    k4_count = 0
    i4_count = 0
    for vertices in itertools.combinations(range(len(adjacency)), 4):
        edge_count = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
        mask = sum(1 << vertex for vertex in vertices)
        if edge_count == 0:
            clauses.append((mask, True))
            i4_count += 1
        elif edge_count == 6:
            clauses.append((mask, False))
            k4_count += 1
    return clauses, k4_count, i4_count


def unit_closure(
    clauses: list[tuple[int, bool]], true_mask: int, false_mask: int
) -> tuple[bool, int, int, int]:
    """Return (conflict, true, false, new-unit-count) at a fixed point."""
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
    leaves: int = 0
    branches: int = 0
    unit_assignments: int = 0
    max_depth: int = 0


class TreeChecker:
    def __init__(self, payload: bytes, n: int, clauses: list[tuple[int, bool]]):
        self.payload = payload
        self.n = n
        self.clauses = clauses
        self.cursor = 0
        self.stats = CheckStats()

    def check_node(self, true_mask: int, false_mask: int, depth: int = 0) -> None:
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
            raise ValueError("branch occurs after unit propagation already conflicts")
        if code >= self.n:
            raise ValueError(f"invalid branch-variable byte {code}")
        bit = 1 << code
        if (true_mask | false_mask) & bit:
            raise ValueError(f"branch variable {code} is already assigned")

        # Checking both children establishes exhaustive coverage of this split.
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
    args = parser.parse_args()
    started = time.perf_counter()

    graph_raw = args.graph.read_bytes()
    adjacency = decode_short_graph6(graph_raw)
    clauses, k4_count, i4_count = extension_clauses(adjacency)
    proof_raw = args.proof.read_bytes()
    if len(proof_raw) < 13:
        raise ValueError("proof is shorter than its header")
    if proof_raw[:8] != MAGIC:
        raise ValueError("wrong proof magic/version")
    if proof_raw[8] != len(adjacency):
        raise ValueError("proof graph order does not match input")
    recorded_clause_count = int.from_bytes(proof_raw[9:13], "little")
    if recorded_clause_count != len(clauses):
        raise ValueError("proof clause count does not match reconstructed CNF")

    stats = TreeChecker(proof_raw[13:], len(adjacency), clauses).run()
    result = {
        "status": "VERIFIED_UNSAT_FIXED_EXTENSION_CNF",
        "graph": str(args.graph),
        "graph_sha256": hashlib.sha256(graph_raw).hexdigest(),
        "proof": str(args.proof),
        "proof_sha256": hashlib.sha256(proof_raw).hexdigest(),
        "proof_bytes": len(proof_raw),
        "n": len(adjacency),
        "variables": len(adjacency),
        "clauses": len(clauses),
        "k4_negative_clauses": k4_count,
        "independent4_positive_clauses": i4_count,
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
