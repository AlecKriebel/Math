#!/usr/bin/env python3
"""Independently verify that the committed depth-5 cubes cover TU(41).

This checker is deliberately separate from the C++ enumerator.  It rebuilds
the first five autocorrelation polynomials in Python, exhausts all 2^19 sign
assignments to their variables, applies only the proved C/D swap symmetry and
row-sum feasibility condition, and compares the resulting feasible set with
the cube file.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path


Entry = tuple[int, str | None]
Polynomial = dict[int, int]


SEARCH_ORDER = [
    "a2",
    "c1",
    "d1",
    "a3",
    "b2",
    "c2",
    "d2",
    "a4",
    "b3",
    "c3",
    "d3",
    "a5",
    "b4",
    "c4",
    "d4",
    "a6",
    "b5",
    "c5",
    "d5",
]
INDEX = {name: index for index, name in enumerate(SEARCH_ORDER)}


def negate(entry: Entry) -> Entry:
    return -entry[0], entry[1]


def variable(name: str) -> Entry:
    return 1, name


def normalized_sequences() -> tuple[list[Entry], ...]:
    one: Entry = (1, None)
    minus_one: Entry = (-1, None)
    a = [variable(f"a{index}") for index in range(2, 21)]
    b = [variable(f"b{index}") for index in range(2, 21)]
    c = [variable(f"c{index}") for index in range(1, 21)]
    d = [variable(f"d{index}") for index in range(1, 21)]
    sequence_a = [one, one, *a, *(negate(x) for x in reversed(a)), minus_one, minus_one]
    sequence_b = [one, one, *b, *(negate(x) for x in reversed(b)), minus_one, one]
    sequence_c = [one, *c, *reversed(c[:-1]), one]
    sequence_d = [one, *d, *reversed(d[:-1]), one]
    lengths = tuple(map(len, (sequence_a, sequence_b, sequence_c, sequence_d)))
    if lengths != (42, 42, 41, 41):
        raise AssertionError(lengths)
    return sequence_a, sequence_b, sequence_c, sequence_d


def lag_polynomial(sequences: tuple[list[Entry], ...], lag: int) -> Polynomial:
    symbolic: defaultdict[tuple[str, ...], int] = defaultdict(int)
    for sequence in sequences:
        for index in range(len(sequence) - lag):
            left_coefficient, left_name = sequence[index]
            right_coefficient, right_name = sequence[index + lag]
            coefficient = left_coefficient * right_coefficient
            if left_name is None and right_name is None:
                monomial: tuple[str, ...] = ()
            elif left_name is None:
                monomial = (right_name,)  # type: ignore[arg-type]
            elif right_name is None:
                monomial = (left_name,)
            elif left_name == right_name:
                monomial = ()
            else:
                monomial = tuple(sorted((left_name, right_name)))
            symbolic[monomial] += coefficient

    result: defaultdict[int, int] = defaultdict(int)
    for monomial, coefficient in symbolic.items():
        if not coefficient:
            continue
        try:
            mask = sum(1 << INDEX[name] for name in monomial)
        except KeyError as error:
            raise AssertionError(
                f"lag {lag} unexpectedly depends on later variable {error.args[0]}"
            ) from error
        result[mask] += coefficient
    return dict(result)


def evaluate(polynomial: Polynomial, assignment_mask: int) -> int:
    return sum(
        coefficient
        * (-1 if (assignment_mask & monomial_mask).bit_count() & 1 else 1)
        for monomial_mask, coefficient in polynomial.items()
    )


def cd_canonical(assignment_mask: int) -> bool:
    for index in range(1, 6):
        c_negative = bool(assignment_mask & (1 << INDEX[f"c{index}"]))
        d_negative = bool(assignment_mask & (1 << INDEX[f"d{index}"]))
        if c_negative != d_negative:
            # +1 (bit zero) is lexicographically first.
            return not c_negative
    return True


def short_row_feasible(assignment_mask: int, letter: str) -> bool:
    assigned_negative = 2 * sum(
        bool(assignment_mask & (1 << INDEX[f"{letter}{index}"]))
        for index in range(1, 6)
    )
    # Unassigned c6..c19 (or d6..d19) have weight two in the row
    # sum, while the unassigned center c20/d20 has weight one.
    reachable = {2 * pairs + center for pairs in range(15) for center in (0, 1)}
    return any(target - assigned_negative in reachable for target in (16, 25))


def cube_from_mask(mask: int) -> str:
    return "".join("1" if mask & (1 << index) else "0" for index in range(19))


def read_cubes(path: Path) -> list[str]:
    cubes = [
        line.removeprefix("cube=").strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.removeprefix("cube=").strip()
    ]
    if any(len(cube) != 19 or set(cube) - {"0", "1"} for cube in cubes):
        raise AssertionError("cube file contains a malformed prefix")
    if len(cubes) != len(set(cubes)):
        raise AssertionError("cube file contains duplicates")
    return cubes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("cubes", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sequences = normalized_sequences()
    polynomials = [lag_polynomial(sequences, lag) for lag in range(39, 34, -1)]
    feasible: set[str] = set()
    for assignment_mask in range(1 << 19):
        if not all(evaluate(polynomial, assignment_mask) == 0 for polynomial in polynomials):
            continue
        if not cd_canonical(assignment_mask):
            continue
        if not short_row_feasible(assignment_mask, "c"):
            continue
        if not short_row_feasible(assignment_mask, "d"):
            continue
        feasible.add(cube_from_mask(assignment_mask))

    actual = set(read_cubes(args.cubes))
    missing = feasible - actual
    extra = actual - feasible
    if missing or extra:
        raise AssertionError(
            f"cube cover mismatch: missing={len(missing)} extra={len(extra)}"
        )
    print(f"PASS independent depth-5 cube cover: {len(actual)} prefixes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
