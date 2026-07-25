#!/usr/bin/env python3
"""Audit the universal 6/3 trace-law ambient count over all quotient classes."""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations, combinations_with_replacement
from math import comb, factorial, log2
from pathlib import Path
import sys


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def big_log2(value: int) -> float:
    exponent = value.bit_length() - 1
    return exponent + log2(value / (1 << exponent))


def read_canonical_matrices(path: Path) -> list[list[list[int]]]:
    matrices: list[list[list[int]]] = []
    for line in path.read_text().splitlines():
        fields = line.split()
        if not fields or fields[0] != "canonical_upper":
            continue
        require(len(fields) == 47, "canonical line does not have 45 entries")
        upper = list(map(int, fields[2:]))
        matrix = [[0] * 9 for _ in range(9)]
        index = 0
        for i in range(9):
            for j in range(i, 9):
                matrix[i][j] = matrix[j][i] = upper[index]
                index += 1
        matrices.append(matrix)
    require(len(matrices) == 625, "expected 625 canonical matrices")
    return matrices


@lru_cache(maxsize=None)
def three_per_column_count(state: tuple[int, ...]) -> int:
    """Count labeled 9-row, 9-column binary matrices of column sum three."""

    state = tuple(sorted(state))
    total = sum(state)
    if total == 0:
        return 1
    if total % 3:
        return 0
    columns = total // 3
    if columns > 9 or state[-1] > columns:
        return 0

    count = 0
    for indices in combinations(range(9), 3):
        if all(state[index] > 0 for index in indices):
            previous = list(state)
            for index in indices:
                previous[index] -= 1
            count += three_per_column_count(tuple(sorted(previous)))
    return count


@lru_cache(maxsize=None)
def trace_diagonal_count(diagonal: tuple[int, ...]) -> int:
    """Count diagonal supports satisfying QR/NR incidences 6 and 3."""

    # Complement the nine QR columns.  Both complemented QR and NR parts
    # then have nine columns of sum three.  If u_i is the complemented QR
    # row sum, the NR row sum is u_i - T_ii/4.
    offsets = tuple(sorted(-entry // 4 for entry in diagonal))
    groups = sorted(Counter(offsets).items())
    answer = 0

    for u_state in combinations_with_replacement(range(10), 9):
        if sum(u_state) != 27:
            continue
        first_count = three_per_column_count(u_state)
        if first_count == 0:
            continue

        remaining = [u_state.count(value) for value in range(10)]
        second_counts = [0] * 10

        def assign_group(group_index: int, multiplicity: int) -> None:
            nonlocal answer
            if group_index == len(groups):
                second_state = tuple(
                    value
                    for value, count in enumerate(second_counts)
                    for _ in range(count)
                )
                answer += (
                    first_count
                    * multiplicity
                    * three_per_column_count(second_state)
                )
                return

            offset, group_size = groups[group_index]
            allowed = [
                value
                for value in range(10)
                if remaining[value] and 0 <= value + offset <= 9
            ]
            choice = [0] * len(allowed)

            def choose_values(
                value_index: int, left: int, denominator: int
            ) -> None:
                if value_index == len(allowed):
                    if left:
                        return
                    for count, value in zip(choice, allowed):
                        remaining[value] -= count
                        second_counts[value + offset] += count
                    assign_group(
                        group_index + 1,
                        multiplicity * factorial(group_size) // denominator,
                    )
                    for count, value in zip(choice, allowed):
                        remaining[value] += count
                        second_counts[value + offset] -= count
                    return

                value = allowed[value_index]
                for count in range(min(remaining[value], left) + 1):
                    choice[value_index] = count
                    choose_values(
                        value_index + 1,
                        left - count,
                        denominator * factorial(count),
                    )

            choose_values(0, group_size, 1)

        assign_group(0, 1)

    return answer


def main() -> None:
    require(
        len(sys.argv) == 2,
        "usage: audit_z37_all_quotient_ambient.py CENSUS_OUTPUT",
    )
    matrices = read_canonical_matrices(Path(sys.argv[1]))
    totals: list[int] = []

    for matrix in matrices:
        diagonal = tuple(sorted(matrix[i][i] for i in range(9)))
        trace_count = trace_diagonal_count(diagonal)
        off_diagonal_count = 1
        for i in range(9):
            for j in range(i + 1, 9):
                off_diagonal_count *= comb(37, (37 - matrix[i][j]) // 2)
        totals.append(off_diagonal_count * trace_count)

    certified_diagonal = tuple(sorted([0, -4, 0, -4, 0, -4, 0, -4, 16]))
    require(
        trace_diagonal_count(certified_diagonal)
        == 21108675338240988108715384392,
        "certified trace-law control changed",
    )

    union = sum(totals)
    trace_logs = list(map(big_log2, totals))
    union_log = big_log2(union)
    moment_divisor = 37**16
    require(
        union % moment_divisor == 0,
        "625-class union is not uniform over first moments",
    )
    post_moment_union = union // moment_divisor
    require(
        abs(min(trace_logs) - 1297.60492221007667) < 1e-11,
        "minimum trace-law exponent changed",
    )
    require(
        abs(max(trace_logs) - 1297.90621474626255) < 1e-11,
        "maximum trace-law exponent changed",
    )
    require(
        abs(union_log - 1307.10873431446430) < 1e-11,
        "625-class union exponent changed",
    )
    require(
        union.bit_length() == 1308 and len(str(union)) == 394,
        "625-class union size changed",
    )
    require(
        abs(big_log2(post_moment_union) - 1223.75748046440094) < 1e-11,
        "post-first-moment union exponent changed",
    )
    print(f"quotient_classes={len(matrices)}")
    print(f"diagonal_multisets={trace_diagonal_count.cache_info().misses}")
    print(f"per_class_trace_log2_min={min(trace_logs):.14f}")
    print(f"per_class_trace_log2_max={max(trace_logs):.14f}")
    print(f"all_625_class_union_log2={union_log:.14f}")
    print(f"all_625_class_union_bit_length={union.bit_length()}")
    print(f"all_625_class_union_decimal_digits={len(str(union))}")
    print(
        "post_first_moment_union_log2="
        f"{big_log2(post_moment_union):.14f}"
    )


if __name__ == "__main__":
    main()
