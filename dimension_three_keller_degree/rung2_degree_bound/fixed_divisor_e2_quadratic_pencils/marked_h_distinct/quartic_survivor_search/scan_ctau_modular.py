#!/usr/bin/env python3
"""Dependency-free finite-field reconnaissance for the CTAU E6/E5 system.

This is not the characteristic-zero proof.  It independently checks every
nonzero k over several prime fields before the exact symbolic lift.
"""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: assertions are required; do not run with -O", file=sys.stderr)
    raise SystemExit(2)

# Variable order:
# a0..a5, b0..b5, l0..l8.
NVARIABLES = 21
A1, A2, A3, A5 = 1, 2, 3, 5
B1, B2, B3, B5 = 7, 8, 9, 11
L1, L2, L4, L5, L7, L8 = 13, 14, 16, 17, 19, 20
FORCED = {A1, A2, A3, A5, B1, B2, B3, B5, L1, L2, L4, L5, L7, L8}


def row(entries: dict[int, int], prime: int) -> list[int]:
    result = [0] * NVARIABLES
    for index, value in entries.items():
        result[index] = value % prime
    return result


def systems(k: int, prime: int) -> tuple[list[list[int]], list[list[int]]]:
    e6 = [
        row({A1: 3 * k - 1, B1: -6 * k - 2, L7: 4}, prime),
        row({A2: -3 * k + 1, B2: 6 * k + 2, L8: -4}, prime),
        row({A3: 2 * (3 * k - 1), B3: -2 * (6 * k + 2)}, prime),
        row({A5: -2 * (3 * k - 1), B5: 2 * (6 * k + 2)}, prime),
        row({A1: -1, B1: -6 * k - 4, L7: 8}, prime),
        row({A2: 1, B2: 6 * k + 4, L8: -8}, prime),
        row({A3: -2, B3: -2 * (6 * k + 4)}, prime),
        row({A5: 2, B5: 2 * (6 * k + 4)}, prime),
        row({B1: -2, L7: 4}, prime),
        row({B2: 2, L8: -4}, prime),
        row({B3: -4}, prime),
        row({B5: 4}, prime),
    ]
    e5_after_e6 = [
        row({L1: 3 * k - 1, L4: -6 * k - 2}, prime),
        row({L2: -3 * k + 1, L5: 6 * k + 2}, prime),
        row({L1: -1, L4: -6 * k - 4}, prime),
        row({L2: 1, L5: 6 * k + 4}, prime),
        row({L4: -2}, prime),
        row({L5: 2}, prime),
    ]
    return e6, e5_after_e6


def rref(matrix: list[list[int]], prime: int) -> tuple[list[list[int]], list[int]]:
    data = [current[:] for current in matrix if any(value % prime for value in current)]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(NVARIABLES):
        chosen = next(
            (
                candidate
                for candidate in range(pivot_row, len(data))
                if data[candidate][column] % prime
            ),
            None,
        )
        if chosen is None:
            continue
        data[pivot_row], data[chosen] = data[chosen], data[pivot_row]
        inverse = pow(data[pivot_row][column] % prime, -1, prime)
        data[pivot_row] = [(value * inverse) % prime for value in data[pivot_row]]
        for other in range(len(data)):
            if other == pivot_row:
                continue
            multiplier = data[other][column] % prime
            if multiplier:
                data[other] = [
                    (left - multiplier * right) % prime
                    for left, right in zip(data[other], data[pivot_row])
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(data):
            break
    return data, pivot_columns


total_parameters = 0
for prime in (5, 7, 11, 13, 17, 19, 23, 29, 31):
    for k_value in range(1, prime):
        e6_rows, e5_rows = systems(k_value, prime)
        _, pivots6 = rref(e6_rows, prime)
        _, pivots65 = rref(e6_rows + e5_rows, prime)
        assert len(pivots6) == 10
        assert len(pivots65) == 14
        assert set(pivots65) == FORCED
        total_parameters += 1

assert total_parameters == sum(prime - 1 for prime in (5, 7, 11, 13, 17, 19, 23, 29, 31))
print(f"CTAU_MODULAR_SCAN_PASS_44DA09 parameters={total_parameters}")
print("all nonzero k: E6/E5 force the six off-axis entries of L to vanish")
