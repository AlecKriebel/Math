#!/usr/bin/env python3
"""Materialize deterministic leaf CNFs for the exact 5^8 1^3 cover."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import automorphism5_fixed_split_search as split  # noqa: E402


GENERATOR_ID = "ramsey55_order5_leaf_cnf_generator_v1"
HARD_COUNTS = (1,) * 8


def sha256_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def type_schedule() -> tuple[tuple[str, tuple[int, ...]], ...]:
    return tuple(
        (fixed_pattern, counts)
        for fixed_pattern in ("edgeless", "one_edge")
        for counts in split.fixed_split_types(fixed_pattern)
        if not (fixed_pattern == "one_edge" and counts == HARD_COUNTS)
    )


def orientation_schedule() -> tuple[tuple[bool, ...], ...]:
    return split.internal_orientation_types(HARD_COUNTS)


def leaf(
    kind: str, index: int
) -> tuple[str, tuple[int, ...], tuple[bool, ...] | None]:
    if kind == "type":
        schedule = type_schedule()
        if not 0 <= index < len(schedule):
            raise IndexError(index)
        fixed_pattern, counts = schedule[index]
        return fixed_pattern, counts, None
    if kind == "orientation":
        schedule = orientation_schedule()
        if not 0 <= index < len(schedule):
            raise IndexError(index)
        return "one_edge", HARD_COUNTS, schedule[index]
    raise ValueError(kind)


def assumption_literals(
    kind: str, index: int
) -> tuple[
    str, tuple[int, ...], tuple[bool, ...] | None, tuple[int, ...]
]:
    edge_variable, _ = split.edge_orbits()
    fixed_pattern, counts, orientation = leaf(kind, index)
    assumptions = list(
        split.assumptions_for_split(fixed_pattern, counts, edge_variable)
    )
    if orientation is not None:
        assumptions.extend(
            split.internal_orientation_assumptions(orientation, edge_variable)
        )
    if len(assumptions) != len(set(map(abs, assumptions))):
        raise AssertionError("overlapping assumptions")
    return fixed_pattern, counts, orientation, tuple(assumptions)


def read_header(path: Path) -> tuple[int, int]:
    with path.open("r", encoding="ascii") as stream:
        header = stream.readline().split()
    if len(header) != 4 or header[:2] != ["p", "cnf"]:
        raise ValueError("invalid base DIMACS header")
    return int(header[2]), int(header[3])


def write_leaf_cnf(
    base_cnf: Path,
    output_cnf: Path,
    assumptions: tuple[int, ...],
) -> None:
    variables, clauses = read_header(base_cnf)
    if variables != split.EXPECTED_VARIABLES or clauses != split.EXPECTED_CLAUSES:
        raise ValueError("unexpected order-5 base formula dimensions")
    if sha256_file(base_cnf) != split.EXPECTED_DIMACS_SHA256:
        raise ValueError("unexpected order-5 base formula hash")
    output_cnf.parent.mkdir(parents=True, exist_ok=True)
    with (
        base_cnf.open("r", encoding="ascii") as source,
        output_cnf.open("w", encoding="ascii", newline="\n") as target,
    ):
        next(source)
        target.write(f"p cnf {variables} {clauses + len(assumptions)}\n")
        for line in source:
            target.write(line)
        for literal in assumptions:
            target.write(f"{literal} 0\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--kind", choices=("type", "orientation"), required=True)
    parser.add_argument("--index", type=int, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()

    fixed_pattern, counts, orientation, assumptions = assumption_literals(
        args.kind, args.index
    )
    write_leaf_cnf(args.base_cnf, args.cnf, assumptions)
    assumption_bytes = "".join(f"{literal} 0\n" for literal in assumptions).encode(
        "ascii"
    )
    source = Path(__file__).resolve()
    metadata = {
        "generator": GENERATOR_ID,
        "cycle_type": "5^8 1^3",
        "kind": args.kind,
        "index": args.index,
        "type_leaf_count": len(type_schedule()),
        "orientation_leaf_count": len(orientation_schedule()),
        "fixed_pattern": fixed_pattern,
        "membership_counts": list(counts),
        "internal_orientation": (
            [int(value) for value in orientation]
            if orientation is not None
            else None
        ),
        "assumptions": list(assumptions),
        "assumption_count": len(assumptions),
        "assumption_stream_sha256": hashlib.sha256(assumption_bytes).hexdigest(),
        "base_cnf_path": str(args.base_cnf.resolve()),
        "base_cnf_sha256": sha256_file(args.base_cnf),
        "cnf_path": str(args.cnf.resolve()),
        "cnf_sha256": sha256_file(args.cnf),
        "cnf_bytes": args.cnf.stat().st_size,
        "variable_count": split.EXPECTED_VARIABLES,
        "base_clause_count": split.EXPECTED_CLAUSES,
        "clause_count": split.EXPECTED_CLAUSES + len(assumptions),
        "generator_path": str(source),
        "generator_sha256": sha256_file(source),
    }
    args.metadata.parent.mkdir(parents=True, exist_ok=True)
    args.metadata.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(metadata, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
