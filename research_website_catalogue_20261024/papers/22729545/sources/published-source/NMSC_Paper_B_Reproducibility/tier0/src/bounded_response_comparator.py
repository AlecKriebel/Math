#!/usr/bin/env python3
"""Bounded exact comparison of diagonal two-state response realizations."""
from __future__ import annotations

import argparse
import itertools
from pathlib import Path

import sympy as sp

from record_schema import make_record, write_jsonl


def hankel(
    generator: sp.Matrix,
    initial: sp.Matrix,
    terminal: sp.Matrix,
) -> sp.Matrix:
    dimension = generator.rows
    return sp.Matrix(
        [
            [(initial * (generator ** (row + column)) * terminal)[0] for column in range(dimension)]
            for row in range(dimension)
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()
    if args.limit < 1:
        raise SystemExit("limit must be positive")
    systems = []
    for rates in itertools.product(range(1, args.limit + 1), repeat=2):
        generator = sp.diag(*[-rate for rate in rates])
        initial = sp.Matrix([[1, 1]])
        terminal = sp.Matrix([[1], [1]])
        systems.append((rates, generator, hankel(generator, initial, terminal)))

    records = []
    for index, (left_rates, left_generator, left_hankel) in enumerate(systems):
        for right_rates, right_generator, right_hankel in systems[index:]:
            if left_hankel != right_hankel:
                continue
            unordered_equal = tuple(sorted(left_rates)) == tuple(sorted(right_rates))
            records.append(
                make_record(
                    job="bounded_response_comparator",
                    case_input={
                        "left_rates": list(left_rates),
                        "right_rates": list(right_rates),
                        "limit": args.limit,
                    },
                    status="PASS" if unordered_equal else "BLOCKING",
                    system={
                        "left_generator": str(left_generator),
                        "right_generator": str(right_generator),
                        "initial": "Matrix([[1, 1]])",
                        "terminal": "Matrix([[1], [1]])",
                    },
                    exact_witness={
                        "equal_hankel_matrix": str(left_hankel),
                        "unordered_rate_multisets_equal": unordered_equal,
                    },
                    declared_quotient_orbit={
                        "unordered_rates": list(sorted(left_rates))
                        if unordered_equal
                        else None
                    },
                    notes="Every equal bounded Hankel response is checked against the intrinsic state permutation.",
                )
            )
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    write_jsonl(output, records)
    blocking = [record for record in records if record["status"] != "PASS"]
    if blocking:
        print(f"BOUNDED_RESPONSE_COMPARATOR_BLOCKING count={len(blocking)}")
        raise SystemExit(1)
    print(f"BOUNDED_RESPONSE_COMPARATOR_OK equal={len(records)}")


if __name__ == "__main__":
    main()
