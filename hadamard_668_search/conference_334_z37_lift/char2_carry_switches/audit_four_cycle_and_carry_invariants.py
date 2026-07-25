#!/usr/bin/env python3
"""Exact small-switch and carry invariants for the two C37 witnesses.

This script has three independent purposes.

1. Expand each 9 by 9 cyclic-block witness to its 333 by 333 binary
   adjacency matrix and exhaust every unordered vertex pair.  A graph
   four-cycle switch has toggle matrix

       B = u v^T + v u^T,

   where u and v are disjoint weight-two vectors.  If A satisfies
   A^2+A=I+J over F_2, then A+B does too exactly when span(u,v) is
   A-invariant.  In particular A u must have weight two or four.

2. Verify the margin-forced carry invariant: every 37-coefficient carry
   block has even parity.  On a diagonal star-symmetric block this forces
   its lag-zero carry to vanish.

3. Replay the exact signed carry transformation between the two frozen
   witnesses.  For Delta=D'-D over the integers,

       R(D')-R(D)
       = (D Delta + Delta D + Delta^2 + Delta)/2  (mod 2).

No solver or probabilistic search is used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Iterable


P = 37
N = 9
V = P * N
WORD_MASK = (1 << P) - 1


def semantic_hash(payload: dict[str, object]) -> str:
    stripped = dict(payload)
    stripped.pop("semantic_sha256", None)
    encoded = json.dumps(
        stripped, sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def load(path: Path) -> tuple[dict[str, object], list[list[int]]]:
    payload = json.loads(path.read_text())
    assert payload["schema"] == "h668-c37-char2-support-witness-v1"
    assert payload["semantic_sha256"] == semantic_hash(payload)
    encoded = payload["word_hex"]
    assert isinstance(encoded, list) and len(encoded) == N
    words = [[int(value, 16) for value in row] for row in encoded]
    assert all(len(row) == N for row in words)
    return payload, words


def rotate37(word: int, amount: int) -> int:
    amount %= P
    if amount == 0:
        return word & WORD_MASK
    return ((word << amount) | (word >> (P - amount))) & WORD_MASK


def expand_rows(words: list[list[int]]) -> list[int]:
    rows: list[int] = []
    for fiber in range(N):
        for position in range(P):
            row = 0
            for target_fiber in range(N):
                block = rotate37(words[fiber][target_fiber], position)
                row |= block << (P * target_fiber)
            rows.append(row)
    assert len(rows) == V
    for vertex, row in enumerate(rows):
        assert ((row >> vertex) & 1) == 0
        for other in range(V):
            assert ((row >> other) & 1) == (
                (rows[other] >> vertex) & 1
            )
    full = (1 << V) - 1
    for vertex, row in enumerate(rows):
        square_row = 0
        neighbors = row
        while neighbors:
            other_bit = neighbors & -neighbors
            other = other_bit.bit_length() - 1
            square_row ^= rows[other]
            neighbors ^= other_bit
        assert (square_row ^ row) == (full ^ (1 << vertex))
    return rows


def invariant_pair_planes(rows: list[int]) -> dict[str, object]:
    distance_histogram: Counter[int] = Counter()
    minimum = V + 1
    minimum_pairs = 0
    invariant_planes: set[tuple[int, int]] = set()
    degree_preserving_switches: set[tuple[int, int]] = set()

    for first in range(V):
        u = (1 << first)
        for second in range(first + 1, V):
            u_pair = u | (1 << second)
            image = rows[first] ^ rows[second]
            weight = image.bit_count()
            distance_histogram[weight] += 1
            if weight < minimum:
                minimum = weight
                minimum_pairs = 1
            elif weight == minimum:
                minimum_pairs += 1

            possible_v: Iterable[int]
            if weight == 2:
                possible_v = (image,)
            elif weight == 4:
                possible_v = (image ^ u_pair,)
            else:
                continue

            for v_pair in possible_v:
                if v_pair.bit_count() != 2 or (u_pair & v_pair):
                    continue
                support_u = tuple(
                    index
                    for index in range(V)
                    if (u_pair >> index) & 1
                )
                support_v = tuple(
                    index
                    for index in range(V)
                    if (v_pair >> index) & 1
                )
                image_v = rows[support_v[0]] ^ rows[support_v[1]]
                if image_v not in (u_pair, u_pair ^ v_pair):
                    continue
                canonical = tuple(sorted((u_pair, v_pair)))
                invariant_planes.add(canonical)

                cross_edges = [
                    (rows[left] >> right) & 1
                    for left in support_u
                    for right in support_v
                ]
                if sum(cross_edges) == 2:
                    row_sums = (
                        cross_edges[0] + cross_edges[1],
                        cross_edges[2] + cross_edges[3],
                    )
                    column_sums = (
                        cross_edges[0] + cross_edges[2],
                        cross_edges[1] + cross_edges[3],
                    )
                    if row_sums == (1, 1) and column_sums == (1, 1):
                        degree_preserving_switches.add(canonical)

    return {
        "unordered_vertex_pairs": V * (V - 1) // 2,
        "minimum_column_difference_weight": minimum,
        "minimum_pair_count": minimum_pairs,
        "distance_histogram": dict(sorted(distance_histogram.items())),
        "invariant_weight_two_planes": len(invariant_planes),
        "degree_preserving_four_cycle_switches": len(
            degree_preserving_switches
        ),
    }


def cyclic_convolution_coefficient(
    left: list[int], right: list[int], lag: int
) -> int:
    return sum(
        left[source] * right[(lag - source) % P]
        for source in range(P)
    )


def coefficient_blocks(words: list[list[int]]) -> list[list[list[int]]]:
    return [
        [
            [(words[i][j] >> lag) & 1 for lag in range(P)]
            for j in range(N)
        ]
        for i in range(N)
    ]


def integer_residual(
    coefficients: list[list[list[int]]],
) -> list[list[list[int]]]:
    residual = [[[0] * P for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            for lag in range(P):
                value = coefficients[i][j][lag]
                for middle in range(N):
                    value += cyclic_convolution_coefficient(
                        coefficients[i][middle],
                        coefficients[middle][j],
                        lag,
                    )
                target = 83 * (
                    1 + int(i == j and lag == 0)
                )
                residual[i][j][lag] = value - target
                assert residual[i][j][lag] % 2 == 0
    return residual


def carry_words(
    words: list[list[int]],
) -> tuple[list[list[int]], dict[str, object]]:
    coefficients = coefficient_blocks(words)
    residual = integer_residual(coefficients)
    carry = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            word = 0
            for lag in range(P):
                word |= ((residual[i][j][lag] // 2) & 1) << lag
            carry[i][j] = word

    block_weights = [
        carry[i][j].bit_count()
        for i in range(N)
        for j in range(i, N)
    ]
    off_diagonal_even_parity = True
    diagonal_lag_zero_vanishes = True
    independent_defects = 0
    for i in range(N):
        for j in range(N):
            assert carry[i][j].bit_count() % 2 == 0
            reverse = carry[j][i] & 1
            for lag in range(1, P):
                reverse |= ((carry[j][i] >> lag) & 1) << (P - lag)
            assert carry[i][j] == reverse
            if i < j:
                off_diagonal_even_parity &= (
                    carry[i][j].bit_count() % 2 == 0
                )
                independent_defects += carry[i][j].bit_count()
            elif i == j:
                diagonal_lag_zero_vanishes &= (
                    (carry[i][i] & 1) == 0
                )
                independent_defects += (
                    (carry[i][i] & ((1 << 19) - 1)).bit_count()
                )

    trace_carry = 0
    for i in range(N):
        trace_carry ^= carry[i][i]
    report = {
        "independent_carry_defects": independent_defects,
        "carry_block_weight_minimum": min(block_weights),
        "carry_block_weight_maximum": max(block_weights),
        "all_45_carry_blocks_even": all(
            weight % 2 == 0 for weight in block_weights
        ),
        "all_36_off_diagonal_block_parities_zero": (
            off_diagonal_even_parity
        ),
        "all_9_diagonal_lag_zero_carries_zero": (
            diagonal_lag_zero_vanishes
        ),
        "trace_carry_hex": f"{trace_carry:010x}",
        "trace_carry_weight": trace_carry.bit_count(),
    }
    return carry, report


def signed_carry_change(
    first_words: list[list[int]],
    second_words: list[list[int]],
) -> dict[str, object]:
    first = coefficient_blocks(first_words)
    second = coefficient_blocks(second_words)
    delta = [
        [
            [
                second[i][j][lag] - first[i][j][lag]
                for lag in range(P)
            ]
            for j in range(N)
        ]
        for i in range(N)
    ]
    first_residual = integer_residual(first)
    second_residual = integer_residual(second)
    changed = 0
    nonzero_delta = 0
    for i in range(N):
        for j in range(N):
            nonzero_delta += sum(
                value != 0 for value in delta[i][j]
            )
            for lag in range(P):
                numerator = delta[i][j][lag]
                for middle in range(N):
                    numerator += cyclic_convolution_coefficient(
                        first[i][middle], delta[middle][j], lag
                    )
                    numerator += cyclic_convolution_coefficient(
                        delta[i][middle], first[middle][j], lag
                    )
                    numerator += cyclic_convolution_coefficient(
                        delta[i][middle], delta[middle][j], lag
                    )
                assert numerator % 2 == 0
                predicted = (numerator // 2) & 1
                observed = (
                    (second_residual[i][j][lag] // 2)
                    - (first_residual[i][j][lag] // 2)
                ) & 1
                assert predicted == observed
                changed += observed
    return {
        "ordered_support_coefficients_changed": nonzero_delta,
        "ordered_carry_coefficients_changed": changed,
        "signed_carry_transformation_coefficients_verified": N * N * P,
    }


def audit_one(path: Path) -> tuple[dict[str, object], list[list[int]]]:
    payload, words = load(path)
    rows = expand_rows(words)
    _, carry_report = carry_words(words)
    return (
        {
            "witness_file": path.name,
            "quotient_type": payload["quotient_type"],
            "semantic_sha256": payload["semantic_sha256"],
            "four_cycle_audit": invariant_pair_planes(rows),
            "carry_invariants": carry_report,
        },
        words,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("first", type=Path)
    parser.add_argument("second", type=Path)
    args = parser.parse_args()
    first_report, first_words = audit_one(args.first)
    second_report, second_words = audit_one(args.second)
    report = {
        "witnesses": [first_report, second_report],
        "cross_witness_carry_transformation": signed_carry_change(
            first_words, second_words
        ),
    }
    encoded = json.dumps(report, sort_keys=True, separators=(",", ":"))
    report["semantic_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
