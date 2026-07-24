#!/usr/bin/env python3
"""Verify the bounded cyclotomic cascade around Eliahou's distance-41 shell.

The C++ engine performs the full Phi4 and Phi4*Phi12 signature censuses.
This wrapper compiles it outside the repository, checks the frozen census,
replays every emitted support in the original 42-coordinate anti-fold,
independently recomputes the complete Phi4 counts in Python, and certifies
the refined joint Phi12/Phi28 Gaussian-frontier bounds.

No support emitted here satisfies the full anti-fold equation, and no
BS(84,83) or Hadamard matrix is claimed.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Sequence


HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
sys.path.insert(0, str(PARENT))

import verify_eliahou_adjacent42_repair as adjacent  # noqa: E402
import verify_eliahou_antifold42 as antifold  # noqa: E402


EXPECTED_PATH = HERE / "EXPECTED_CENSUS.json"
SOURCE_PATH = HERE / "audit_cyclotomic_cascade.cpp"

Case = tuple[str, int]
Polynomial = tuple[int, ...]


def canonical_cases() -> tuple[Case, ...]:
    long_catalog, short_catalog = adjacent.q_pair_signature_catalogs()
    cases = [
        ("L", index)
        for signature in ((-2, 0), (0, 2))
        for index in long_catalog[signature]
    ]
    seen: set[frozenset[int]] = set()
    for index in short_catalog[(0, 0)]:
        cells = frozenset(antifold.q_pair_cells("S", index))
        if cells in seen:
            continue
        seen.add(cells)
        cases.append(("S", index))
    if len(cases) != 30:
        raise AssertionError("the canonical 30-case list changed")
    return tuple(cases)


def normalized_pair_rows(
    rows: Sequence[Sequence[int]],
) -> tuple[Polynomial, Polynomial, Polynomial, Polynomial]:
    return (
        tuple((a + b) // 2 for a, b in zip(rows[0], rows[1])),
        tuple((a + b) // 2 for a, b in zip(rows[2], rows[3])),
        tuple((a - b) // 2 for a, b in zip(rows[0], rows[1])),
        tuple((a - b) // 2 for a, b in zip(rows[2], rows[3])),
    )


def q_adjusted_rows(block: str, index: int) -> list[list[int]]:
    rows = [
        list(row)
        for row in antifold.antifold_quadruple(adjacent.eliahou_base())
    ]
    active_row = 1 if block == "L" else 3
    for cell in antifold.q_pair_cells(block, index):
        rows[active_row][cell] = 0
    return rows


def evaluate_at_i(row: Sequence[int]) -> tuple[int, int]:
    real = 0
    imaginary = 0
    for index, value in enumerate(row):
        residue = index % 4
        if residue == 0:
            real += value
        elif residue == 1:
            imaginary += value
        elif residue == 2:
            real -= value
        else:
            imaginary -= value
    return real, imaginary


def phi4_block_histogram(
    row: Sequence[int], cells: Sequence[int]
) -> Counter[tuple[int, int]]:
    """Return (selected weight, Gaussian norm) -> support multiplicity."""

    base_real, base_imaginary = evaluate_at_i(row)
    states: Counter[tuple[int, int, int]] = Counter(
        {(0, base_real, base_imaginary): 1}
    )
    for cell in cells:
        value = row[cell]
        residue = cell % 4
        delta_real = -value if residue == 0 else value if residue == 2 else 0
        delta_imaginary = (
            -value if residue == 1 else value if residue == 3 else 0
        )
        following = states.copy()
        for (weight, real, imaginary), multiplicity in states.items():
            following[
                (
                    weight + 1,
                    real + delta_real,
                    imaginary + delta_imaginary,
                )
            ] += multiplicity
        states = following
    result: Counter[tuple[int, int]] = Counter()
    for (weight, real, imaginary), multiplicity in states.items():
        result[(weight, real * real + imaginary * imaginary)] += multiplicity
    return result


def independent_phi4_census() -> tuple[list[str], list[int]]:
    support_counts: list[str] = []
    joined_counts: list[int] = []
    for block, index in canonical_cases():
        pair_rows = normalized_pair_rows(q_adjusted_rows(block, index))
        long_cells, short_cells = antifold.available_s_support_cells(
            block, index
        )
        p_histogram = phi4_block_histogram(pair_rows[0], long_cells)
        q_histogram = phi4_block_histogram(pair_rows[1], short_cells)
        r_real, r_imaginary = evaluate_at_i(pair_rows[2])
        s_real, s_imaginary = evaluate_at_i(pair_rows[3])
        target = (
            167
            - r_real * r_real
            - r_imaginary * r_imaginary
            - s_real * s_real
            - s_imaginary * s_imaginary
        )
        count = 0
        joins = 0
        for (weight, energy), multiplicity in p_histogram.items():
            partner = q_histogram.get((39 - weight, target - energy), 0)
            if partner:
                count += multiplicity * partner
                joins += 1
        support_counts.append(str(count))
        joined_counts.append(joins)
    return support_counts, joined_counts


def reduce_negacyclic(
    coefficients: Sequence[int], modulus: int
) -> Polynomial:
    result = [0] * modulus
    for exponent, coefficient in enumerate(coefficients):
        quotient, residue = divmod(exponent, modulus)
        result[residue] += (-1 if quotient % 2 else 1) * coefficient
    return tuple(result)


def support_removal_state(
    row: Sequence[int], support: Sequence[int]
) -> tuple[int, ...]:
    """Encode one support choice simultaneously modulo 14 and modulo 6."""

    removal14 = sum(
        (-1 if (cell // 14) % 2 else 1) * row[cell]
        for cell in support
    )
    removal6 = [0] * 6
    for cell in support:
        removal6[cell % 6] += (
            (-1 if (cell // 6) % 2 else 1) * row[cell]
        )
    return (len(support), removal14, *removal6)


def refined_residue_states(
    row: Sequence[int], cells: Sequence[int], residue: int
) -> set[tuple[int, ...]]:
    """Return all joint (weight, mod-14, mod-6) states at one residue."""

    local_cells = tuple(cell for cell in cells if cell % 14 == residue)
    states: set[tuple[int, ...]] = set()
    for mask in range(1 << len(local_cells)):
        support = tuple(
            cell
            for bit, cell in enumerate(local_cells)
            if mask & (1 << bit)
        )
        states.add(support_removal_state(row, support))
    return states


def paired_refined_states(
    left: set[tuple[int, ...]], right: set[tuple[int, ...]]
) -> set[tuple[int, ...]]:
    """Combine residues j,j+7 into one Gaussian-coordinate state."""

    return {
        (
            left_state[0] + right_state[0],
            left_state[1],
            right_state[1],
            *(
                left_state[index] + right_state[index]
                for index in range(2, 8)
            ),
        )
        for left_state in left
        for right_state in right
    }


def refined_gaussian_frontier_census() -> dict[str, object]:
    """Certify the sharp ordered 3+4 joint Phi12/Phi28 frontier bounds."""

    maximum_residue_states = 0
    maximum_paired_states = 0
    maximum_ordered_three_half = 0
    maximum_ordered_four_half = 0

    for block, index in canonical_cases():
        pair_rows = normalized_pair_rows(q_adjusted_rows(block, index))
        long_cells, short_cells = antifold.available_s_support_cells(
            block, index
        )
        for row, cells in (
            (pair_rows[0], long_cells),
            (pair_rows[1], short_cells),
        ):
            residue_states = [
                refined_residue_states(row, cells, residue)
                for residue in range(14)
            ]
            maximum_residue_states = max(
                maximum_residue_states,
                *(len(states) for states in residue_states),
            )
            paired_sizes = []
            for residue in range(7):
                paired = paired_refined_states(
                    residue_states[residue],
                    residue_states[residue + 7],
                )
                paired_sizes.append(len(paired))
                maximum_paired_states = max(
                    maximum_paired_states, len(paired)
                )
            first_half = 1
            for size in paired_sizes[:3]:
                first_half *= size
            second_half = 1
            for size in paired_sizes[3:]:
                second_half *= size
            maximum_ordered_three_half = max(
                maximum_ordered_three_half, first_half
            )
            maximum_ordered_four_half = max(
                maximum_ordered_four_half, second_half
            )

    block, index = canonical_cases()[0]
    if (block, index) != ("L", 0):
        raise AssertionError("the pinned refinement collision case changed")
    pair_rows = normalized_pair_rows(q_adjusted_rows(block, index))
    long_cells, _ = antifold.available_s_support_cells(block, index)
    collision_cells = tuple(cell for cell in long_cells if cell % 14 == 1)
    support_a = (1,)
    support_b = (15,)
    state_a = support_removal_state(pair_rows[0], support_a)
    state_b = support_removal_state(pair_rows[0], support_b)
    if collision_cells != (1, 15, 29):
        raise AssertionError("the pinned refinement collision cells changed")
    if state_a[:2] != state_b[:2] or state_a[2:] == state_b[2:]:
        raise AssertionError("the pinned mod-14/mod-6 collision disappeared")

    return {
        "case_side_specifications": 2 * len(canonical_cases()),
        "maximum_residue_states": maximum_residue_states,
        "maximum_paired_coordinate_states": maximum_paired_states,
        "maximum_ordered_three_half_assignments": (
            maximum_ordered_three_half
        ),
        "maximum_ordered_four_half_assignments": maximum_ordered_four_half,
        "collision": {
            "case": "L0",
            "side": "P",
            "mod14_residue": 1,
            "cells": list(collision_cells),
            "support_a": list(support_a),
            "support_b": list(support_b),
            "common_coarse_state": list(state_a[:2]),
            "support_a_mod6_removal": list(state_a[2:]),
            "support_b_mod6_removal": list(state_b[2:]),
        },
    }


def replay_factor_witnesses(payload: dict[str, object]) -> None:
    modulus = int(payload["modulus"])
    cases = canonical_cases()
    records = payload["cases"]
    if not isinstance(records, list) or len(records) != len(cases):
        raise AssertionError("engine returned the wrong case count")
    for case_number, (record, expected_case) in enumerate(
        zip(records, cases)
    ):
        if not isinstance(record, dict):
            raise AssertionError("engine case is not an object")
        block, index = expected_case
        if (
            record["case"] != case_number
            or record["block"] != block
            or record["q_index"] != index
        ):
            raise AssertionError("engine case ordering changed")
        long_support = tuple(record["representative_long_support"])
        short_support = tuple(record["representative_short_support"])
        if len(long_support) + len(short_support) != 39:
            raise AssertionError("representative has the wrong weight")
        available_long, available_short = (
            antifold.available_s_support_cells(block, index)
        )
        if not set(long_support) <= set(available_long):
            raise AssertionError("representative used an unavailable long cell")
        if not set(short_support) <= set(available_short):
            raise AssertionError(
                "representative used an unavailable short cell"
            )
        rows = antifold.boundary_antifold_rows(
            block, index, long_support, short_support
        )
        full = antifold.negacyclic_norm_coefficients(rows)
        reduced = reduce_negacyclic(full, modulus)
        if reduced != (334,) + (0,) * (modulus - 1):
            raise AssertionError("factor witness failed direct integer replay")
        if full == (334,) + (0,) * 41:
            raise AssertionError(
                "unexpected exact anti-fold support requires full investigation"
            )


def compile_engine(destination: Path) -> None:
    subprocess.run(
        [
            "clang++",
            "-O3",
            "-std=c++20",
            "-Wall",
            "-Wextra",
            "-pedantic",
            str(SOURCE_PATH),
            "-o",
            str(destination),
        ],
        check=True,
    )


def run_json(binary: Path, *arguments: str) -> dict[str, object]:
    completed = subprocess.run(
        [str(binary), *arguments],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    value = json.loads(completed.stdout)
    if not isinstance(value, dict):
        raise AssertionError("engine output is not a JSON object")
    return value


def stable_fields(payload: dict[str, object]) -> tuple[list[str], list[int]]:
    records = payload["cases"]
    if not isinstance(records, list):
        raise AssertionError("engine cases are not a list")
    return (
        [str(record["support_count"]) for record in records],
        [int(record["joined_signature_count"]) for record in records],
    )


def verify() -> dict[str, object]:
    expected = json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))
    labels = [f"{block}{index}" for block, index in canonical_cases()]
    if labels != expected["case_labels"]:
        raise AssertionError("frozen case labels changed")

    python_counts, python_joins = independent_phi4_census()
    if python_counts != expected["phi4_support_counts"]:
        raise AssertionError("independent Python Phi4 counts changed")
    if python_joins != expected["phi4_joined_signature_counts"]:
        raise AssertionError("independent Python Phi4 joins changed")
    refined_frontier = refined_gaussian_frontier_census()
    if refined_frontier != expected["refined_gaussian_frontier"]:
        raise AssertionError("refined Gaussian frontier census changed")

    with tempfile.TemporaryDirectory(prefix="h668-cyclotomic-") as temporary:
        binary = Path(temporary) / "audit_cyclotomic_cascade"
        compile_engine(binary)
        subprocess.run([str(binary), "--self-test"], check=True)
        phi4 = run_json(binary, "--modulus", "2")
        phi12 = run_json(binary, "--modulus", "6")
        growth = run_json(binary, "--growth", "14")

    if stable_fields(phi4) != (
        expected["phi4_support_counts"],
        expected["phi4_joined_signature_counts"],
    ):
        raise AssertionError("C++ Phi4 census changed")
    if stable_fields(phi12) != (
        expected["phi12_support_counts"],
        expected["phi12_joined_signature_counts"],
    ):
        raise AssertionError("C++ Phi12 census changed")
    targets = [
        record["target_signature"]
        for record in phi12["cases"]
    ]
    if targets != expected["phi12_target_signatures"]:
        raise AssertionError("Phi12 target signatures changed")
    expected_growth = expected["phi28_growth"]
    for field, wanted in expected_growth.items():
        if growth[field] != wanted:
            raise AssertionError(f"Phi28 growth field {field!r} changed")

    replay_factor_witnesses(phi4)
    replay_factor_witnesses(phi12)

    phi12_counts = [int(value) for value in expected["phi12_support_counts"]]
    return {
        "status": (
            "verified exact Phi4 and Phi4*Phi12 support censuses; "
            "no anti-fold solution or H(668) claimed"
        ),
        "cases": len(labels),
        "phi4_surviving_cases": sum(value != "0" for value in python_counts),
        "phi12_surviving_cases": sum(value != 0 for value in phi12_counts),
        "phi12_support_count_range": [
            min(phi12_counts),
            max(phi12_counts),
        ],
        "certified_q0_phi12_supports": phi12_counts[0],
        "observed_q1_phi12_supports": phi12_counts[1],
        "phi28_raw_state_growth": expected_growth,
        "refined_gaussian_frontier": refined_frontier,
        "scope": (
            "Phi4*Phi12 is necessary only; every representative fails the "
            "full 42-coordinate anti-fold replay"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
