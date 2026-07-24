#!/usr/bin/env python3
"""Build one selector-union CNF for the exact order-5 structural cover.

Fifty-eight ordinary normalized structural types are represented directly.
The remaining hard all-cell-counts-one type is replaced by its eighty exact
internal-orientation representatives.  A selector variable implies every
assumption of its leaf, and one final clause requires at least one selector.
Thus one UNSAT proof covers every normalized leaf at once.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import automorphism5_fixed_split_search as split  # noqa: E402
from automorphism5_leaf_cnf import (  # noqa: E402
    HARD_COUNTS,
    orientation_schedule,
    sha256_file,
    type_schedule,
)


GENERATOR_ID = "ramsey55_order5_selector_union_cnf_generator_v1"


def all_leaves() -> tuple[dict[str, object], ...]:
    edge_variable, _ = split.edge_orbits()
    records: list[dict[str, object]] = []
    for index, (fixed_pattern, counts) in enumerate(type_schedule()):
        assumptions = split.assumptions_for_split(
            fixed_pattern, counts, edge_variable
        )
        records.append(
            {
                "kind": "type",
                "index": index,
                "fixed_pattern": fixed_pattern,
                "membership_counts": list(counts),
                "internal_orientation": None,
                "assumptions": list(assumptions),
            }
        )
    hard_assumptions = split.assumptions_for_split(
        "one_edge", HARD_COUNTS, edge_variable
    )
    for index, orientation in enumerate(orientation_schedule()):
        assumptions = hard_assumptions + split.internal_orientation_assumptions(
            orientation, edge_variable
        )
        records.append(
            {
                "kind": "orientation",
                "index": index,
                "fixed_pattern": "one_edge",
                "membership_counts": list(HARD_COUNTS),
                "internal_orientation": [int(value) for value in orientation],
                "assumptions": list(assumptions),
            }
        )
    if len(records) != 138:
        raise AssertionError("unexpected selector leaf count")
    return tuple(records)


def select_leaves(
    portion: str, batch_start: int, batch_count: int | None
) -> tuple[dict[str, object], ...]:
    records = all_leaves()
    if portion == "ordinary":
        chosen = [record for record in records if record["kind"] == "type"]
    elif portion == "orientations":
        chosen = [
            record for record in records if record["kind"] == "orientation"
        ]
    elif portion == "all":
        chosen = list(records)
    else:
        raise ValueError(portion)
    if batch_start < 0 or batch_start > len(chosen):
        raise ValueError("batch start outside selected schedule")
    stop = (
        len(chosen)
        if batch_count is None
        else min(len(chosen), batch_start + batch_count)
    )
    chosen = chosen[batch_start:stop]
    if not chosen:
        raise ValueError("empty selector batch")
    return tuple(chosen)


def appended_clauses(
    records: tuple[dict[str, object], ...],
    selectors_first: bool,
) -> tuple[tuple[int, ...], ...]:
    clauses: list[tuple[int, ...]] = []
    offset = len(records) if selectors_first else 0
    for record in records:
        selector = int(record["selector_variable"])
        for literal in record["assumptions"]:  # type: ignore[union-attr]
            literal = int(literal)
            shifted = (
                (abs(literal) + offset) * (1 if literal > 0 else -1)
                if selectors_first
                else literal
            )
            clauses.append((-selector, shifted))
    selectors = tuple(int(record["selector_variable"]) for record in records)
    clauses.extend(
        (-first, -second)
        for first, second in itertools.combinations(selectors, 2)
    )
    clauses.append(selectors)
    return tuple(clauses)


def clause_stream_sha256(clauses: tuple[tuple[int, ...], ...]) -> str:
    payload = "".join(
        " ".join(map(str, clause)) + " 0\n" for clause in clauses
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def write_cnf(
    base_cnf: Path,
    output_cnf: Path,
    records: tuple[dict[str, object], ...],
    selectors_first: bool,
) -> tuple[tuple[int, ...], ...]:
    if sha256_file(base_cnf) != split.EXPECTED_DIMACS_SHA256:
        raise ValueError("unexpected order-5 base formula hash")
    with base_cnf.open("r", encoding="ascii") as source:
        fields = source.readline().split()
    if fields != [
        "p",
        "cnf",
        str(split.EXPECTED_VARIABLES),
        str(split.EXPECTED_CLAUSES),
    ]:
        raise ValueError("unexpected order-5 base formula header")
    extra = appended_clauses(records, selectors_first)
    output_cnf.parent.mkdir(parents=True, exist_ok=True)
    with (
        base_cnf.open("r", encoding="ascii") as source,
        output_cnf.open("w", encoding="ascii", newline="\n") as target,
    ):
        next(source)
        target.write(
            f"p cnf {split.EXPECTED_VARIABLES + len(records)} "
            f"{split.EXPECTED_CLAUSES + len(extra)}\n"
        )
        if selectors_first:
            offset = len(records)
            for line in source:
                fields = line.split()
                shifted = [
                    str(
                        (abs(int(field)) + offset)
                        * (1 if int(field) > 0 else -1)
                    )
                    for field in fields
                    if int(field) != 0
                ]
                target.write(" ".join(shifted) + " 0\n")
        else:
            for line in source:
                target.write(line)
        for clause in extra:
            target.write(" ".join(map(str, clause)) + " 0\n")
    return extra


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument(
        "--portion",
        choices=("all", "ordinary", "orientations"),
        default="all",
    )
    parser.add_argument("--batch-start", type=int, default=0)
    parser.add_argument("--batch-count", type=int)
    parser.add_argument("--selectors-first", action="store_true")
    args = parser.parse_args()
    if args.batch_count is not None and args.batch_count <= 0:
        parser.error("--batch-count must be positive")

    selected = select_leaves(args.portion, args.batch_start, args.batch_count)
    records_list: list[dict[str, object]] = []
    for selector_offset, selected_record in enumerate(selected, start=1):
        record = dict(selected_record)
        record["selector_variable"] = (
            selector_offset
            if args.selectors_first
            else split.EXPECTED_VARIABLES + selector_offset
        )
        records_list.append(record)
    records = tuple(records_list)
    extra = write_cnf(
        args.base_cnf, args.cnf, records, args.selectors_first
    )
    source = Path(__file__).resolve()
    metadata = {
        "generator": GENERATOR_ID,
        "cycle_type": "5^8 1^3",
        "base_variable_count": split.EXPECTED_VARIABLES,
        "selector_variable_count": len(records),
        "variable_count": split.EXPECTED_VARIABLES + len(records),
        "base_clause_count": split.EXPECTED_CLAUSES,
        "selector_implication_clause_count": sum(
            len(record["assumptions"]) for record in records
        ),
        "selector_at_most_one_clause_count": len(records)
        * (len(records) - 1)
        // 2,
        "selector_cover_clause_count": 1,
        "appended_clause_count": len(extra),
        "clause_count": split.EXPECTED_CLAUSES + len(extra),
        "ordinary_type_leaf_count": len(type_schedule()),
        "hard_orientation_leaf_count": len(orientation_schedule()),
        "total_leaf_count": len(records),
        "portion": args.portion,
        "batch_start": args.batch_start,
        "batch_count": len(records),
        "selectors_first": args.selectors_first,
        "base_variable_offset": len(records) if args.selectors_first else 0,
        "omitted_hard_type": {
            "fixed_pattern": "one_edge",
            "membership_counts": list(HARD_COUNTS),
        },
        "leaves": records,
        "appended_clause_stream_sha256": clause_stream_sha256(extra),
        "base_cnf_path": str(args.base_cnf.resolve()),
        "base_cnf_sha256": sha256_file(args.base_cnf),
        "cnf_path": str(args.cnf.resolve()),
        "cnf_sha256": sha256_file(args.cnf),
        "cnf_bytes": args.cnf.stat().st_size,
        "generator_path": str(source),
        "generator_sha256": sha256_file(source),
        "equivalence": (
            (
                "Each selector implies one exact normalized leaf, and the "
                "exactly-one selector clauses require one leaf. The 58 "
                "ordinary leaves plus 80 orientation leaves replace the "
                "complete 59-type cover, with the all-ones hard type "
                "partitioned by its exact orientation orbits."
            )
            if args.portion == "all"
            else (
                "Each selector implies one of the 58 ordinary normalized "
                "types, and the exactly-one selector clauses require one "
                "type. The omitted one-edge all-ones type is outside this "
                "formula and requires its separate orientation cover."
            )
            if args.portion == "ordinary"
            else (
                "Each selector implies one exact internal-orientation "
                "representative in the recorded batch, and the exactly-one "
                "selector clauses require one representative. This formula "
                "covers only the recorded orientation batch."
            )
        ),
    }
    args.metadata.parent.mkdir(parents=True, exist_ok=True)
    args.metadata.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {key: value for key, value in metadata.items() if key != "leaves"},
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
