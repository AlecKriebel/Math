#!/usr/bin/env python3
"""Exhaustive clean-room probe of the order-12 k=4 anchor-signature action."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CNF_PATH = ROOT / "instances/order12_k4_connected_parent/instance.cnf"
NOTE_PATH = ROOT / "math/lemmas/order12_k4_anchor_signature_symmetry.md"
EXPECTED_CNF_SHA256 = (
    "adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac"
)
BANK_START = 49_101
BANK_SIZE = 4**8
SORTER_START = 114_637
CANONICAL_MINIMA = (0b0000, 0b0001, 0b0011, 0b0111)
NONCANONICAL_ZERO_FIRST = (0b0010, 0b0100, 0b0101, 0b0110)


def parse_dimacs(payload: bytes) -> list[tuple[int, ...]]:
    lines = payload.decode("ascii").splitlines()
    header = lines[0].split()
    if header != ["p", "cnf", "18381", "114742"]:
        raise AssertionError("frozen parent DIMACS header differs")
    clauses: list[tuple[int, ...]] = []
    for line in lines[1:]:
        tokens = tuple(map(int, line.split()))
        if not tokens or tokens[-1] != 0 or 0 in tokens[:-1]:
            raise AssertionError("malformed frozen DIMACS clause")
        clauses.append(tokens[:-1])
    if len(clauses) != 114_742:
        raise AssertionError("frozen parent clause count differs")
    return clauses


def edge_map() -> dict[tuple[int, int], int]:
    return {
        pair: index
        for index, pair in enumerate(combinations(range(12), 2), start=1)
    }


def pair(first: int, second: int) -> tuple[int, int]:
    return (first, second) if first < second else (second, first)


def coloring_clause(
    colors: tuple[int, ...], edge: dict[tuple[int, int], int]
) -> tuple[int, ...]:
    return tuple(
        edge[(first, second)]
        for first, second in combinations(range(12), 2)
        if colors[first] == colors[second]
    )


def signature_bits(code: int) -> tuple[int, int, int, int]:
    return tuple((code >> shift) & 1 for shift in (3, 2, 1, 0))


def signature_code(bits: tuple[int, int, int, int]) -> int:
    return sum(bit << shift for bit, shift in zip(bits, (3, 2, 1, 0)))


def coordinate_action(code: int, permutation: tuple[int, ...]) -> int:
    """Push anchors old i -> permutation[i], hence move old bit i likewise."""

    old = signature_bits(code)
    new = [0, 0, 0, 0]
    for old_coordinate, new_coordinate in enumerate(permutation):
        new[new_coordinate] = old[old_coordinate]
    return signature_code(tuple(new))


def swapped_coordinates(code: int, coordinate: int) -> int:
    bits = list(signature_bits(code))
    bits[coordinate], bits[coordinate + 1] = (
        bits[coordinate + 1],
        bits[coordinate],
    )
    return signature_code(tuple(bits))


def main() -> None:
    payload = CNF_PATH.read_bytes()
    if sha256(payload).hexdigest() != EXPECTED_CNF_SHA256:
        raise AssertionError("frozen parent hash differs")
    clauses = parse_dimacs(payload)
    edge = edge_map()

    bank = clauses[BANK_START : BANK_START + BANK_SIZE]
    if len(bank) != BANK_SIZE or SORTER_START != BANK_START + BANK_SIZE:
        raise AssertionError("complete normalized bank boundary differs")
    rows = tuple(product(range(4), repeat=8))
    for index, outer_colors in enumerate(rows):
        colors = (0, 1, 2, 3, *outer_colors)
        if bank[index] != coloring_clause(colors, edge):
            raise AssertionError("frozen complete coloring-bank row differs")

    anchor_action_rows = 0
    anchor_permutations = tuple(permutations(range(4)))
    for permutation in anchor_permutations:
        vertex_image = {
            vertex: permutation[vertex] if vertex < 4 else vertex
            for vertex in range(12)
        }
        for outer_colors in rows:
            colors = (0, 1, 2, 3, *outer_colors)
            new_colors = [-1] * 12
            for old_vertex, old_color in enumerate(colors):
                new_vertex = vertex_image[old_vertex]
                new_colors[new_vertex] = permutation[old_color]
            if tuple(new_colors[:4]) != (0, 1, 2, 3):
                raise AssertionError("anchor/color action lost normalization")
            transformed_clause = tuple(
                sorted(
                    edge[pair(vertex_image[first], vertex_image[second])]
                    for first, second in combinations(range(12), 2)
                    if colors[first] == colors[second]
                )
            )
            if transformed_clause != coloring_clause(tuple(new_colors), edge):
                raise AssertionError("anchor/color action does not preserve a bank row")
            anchor_action_rows += 1

    outer_adjacent_swap_rows = 0
    for left in range(4, 11):
        right = left + 1
        vertex_image = {
            vertex: (
                right if vertex == left else left if vertex == right else vertex
            )
            for vertex in range(12)
        }
        for outer_colors in rows:
            colors = (0, 1, 2, 3, *outer_colors)
            new_colors = [-1] * 12
            for old_vertex, color in enumerate(colors):
                new_colors[vertex_image[old_vertex]] = color
            transformed_clause = tuple(
                sorted(
                    edge[pair(vertex_image[first], vertex_image[second])]
                    for first, second in combinations(range(12), 2)
                    if colors[first] == colors[second]
                )
            )
            if transformed_clause != coloring_clause(tuple(new_colors), edge):
                raise AssertionError("outer adjacent swap does not preserve the bank")
            outer_adjacent_swap_rows += 1

    action_tables = tuple(
        tuple(coordinate_action(code, permutation) for code in range(16))
        for permutation in anchor_permutations
    )
    abstract_multisets = 0
    adjacent_inversion_checks = 0
    canonical_minimum_counts: Counter[str] = Counter()
    noncanonical_zero_first_multisets = 0
    abstract_first_one_multisets = 0
    for signatures in combinations_with_replacement(range(15), 8):
        abstract_multisets += 1
        first = signatures[0]
        if first in NONCANONICAL_ZERO_FIRST:
            noncanonical_zero_first_multisets += 1
        if first >= 8:
            abstract_first_one_multisets += 1

        first_bits = signature_bits(first)
        for coordinate in range(3):
            if first_bits[coordinate : coordinate + 2] == (1, 0):
                swapped = tuple(
                    sorted(
                        swapped_coordinates(code, coordinate)
                        for code in signatures
                    )
                )
                if not swapped[0] < first or not swapped < signatures:
                    raise AssertionError("adjacent-inversion descent argument failed")
                adjacent_inversion_checks += 1

        images = (
            tuple(sorted(table[code] for code in signatures))
            for table in action_tables
        )
        canonical = min(images)
        canonical_first = canonical[0]
        if canonical_first not in CANONICAL_MINIMA:
            raise AssertionError("abstract S4 orbit lacks a four-cube representative")
        canonical_minimum_counts[f"{canonical_first:04b}"] += 1

    expected_multisets = 319_770
    if abstract_multisets != expected_multisets:
        raise AssertionError("abstract multiset universe is incomplete")

    report = {
        "schema": (
            "gamma-theta-order12-k4-anchor-signature-hostile-probe-v1"
        ),
        "status": "PASS_EXACT_SYMMETRY_REDUCTION_ONLY",
        "claim_boundary": (
            "This verifies the four-cube orbit reduction only; it is not an "
            "aggregate UNSAT, order-12 slice, or universal-conjecture claim."
        ),
        "note_sha256": sha256(NOTE_PATH.read_bytes()).hexdigest(),
        "parent_cnf_sha256": EXPECTED_CNF_SHA256,
        "complete_coloring_bank_rows_checked": len(rows),
        "anchor_permutations_checked": len(anchor_permutations),
        "anchor_color_action_rows_checked": anchor_action_rows,
        "outer_adjacent_swap_action_rows_checked": outer_adjacent_swap_rows,
        "abstract_no_k5_signature_multisets_checked": abstract_multisets,
        "adjacent_inversion_descent_checks": adjacent_inversion_checks,
        "canonical_minimum_counts": dict(sorted(canonical_minimum_counts.items())),
        "noncanonical_zero_first_multisets_checked": (
            noncanonical_zero_first_multisets
        ),
        "abstract_first_one_multisets": abstract_first_one_multisets,
        "canonical_cube_ids": [f"{code:04b}" for code in CANONICAL_MINIMA],
        "logically_unsat_first_one_cube_ids": [
            f"{code:04b}" for code in range(8, 16)
        ],
        "orbit_redundant_zero_first_cube_ids": [
            f"{code:04b}" for code in NONCANONICAL_ZERO_FIRST
        ],
    }
    print(json.dumps(report, allow_nan=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
