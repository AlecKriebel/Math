#!/usr/bin/env python3
"""Export the exact shell-two primitive alphabets in a degree-12 field basis.

The promoted primitive-unit audit represents E=F_(167^12) inside the
36-dimensional ambient prime field used by the repository.  For fast,
bounded multiplicative-character experiments, this exporter constructs a
power basis 1,theta,...,theta^11 of E over F_167, derives theta's exact
degree-12 reduction polynomial, and writes all 15 seed/channel physical
alphabets in that basis.

The output is a small deterministic binary input for joint_character_audit.cpp.
It contains no searched data and can be regenerated from promoted sources.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import struct
import sys
from typing import Sequence


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
PROMOTED = SEARCH_ROOT / "lp333_shell_two_primitive_units"
for path in (SEARCH_ROOT, PROMOTED):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import audit_primitive_degenerate as audit  # noqa: E402
import verify_lp333_order3_phase_prime167 as phase167  # noqa: E402
import verify_lp333_order3_prime167_split as split  # noqa: E402


P = 167
DEGREE = 12
AMBIENT = 36
MAGIC = b"H668CHAR1"


def vector(value: split.L) -> tuple[int, ...]:
    result = tuple(coordinate for pair in value for coordinate in pair)
    if len(result) != AMBIENT:
        raise AssertionError("ambient coordinate dimension changed")
    return result


def inverse_mod(matrix: Sequence[Sequence[int]]) -> list[list[int]]:
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError("matrix must be square")
    work = [
        [int(value) % P for value in row]
        + [int(index == row_index) for index in range(n)]
        for row_index, row in enumerate(matrix)
    ]
    for column in range(n):
        pivot = next(
            (row for row in range(column, n) if work[row][column] % P),
            None,
        )
        if pivot is None:
            raise ValueError("matrix is singular")
        work[column], work[pivot] = work[pivot], work[column]
        scale = pow(work[column][column], -1, P)
        work[column] = [(value * scale) % P for value in work[column]]
        for row in range(n):
            if row == column:
                continue
            scale = work[row][column] % P
            if scale:
                work[row] = [
                    (left - scale * right) % P
                    for left, right in zip(work[row], work[column])
                ]
    return [row[n:] for row in work]


def matrix_vector(
    matrix: Sequence[Sequence[int]], value: Sequence[int]
) -> tuple[int, ...]:
    return tuple(
        sum(left * right for left, right in zip(row, value)) % P
        for row in matrix
    )


def field_basis() -> tuple[
    split.L,
    tuple[split.L, ...],
    tuple[int, ...],
    tuple[tuple[int, ...], ...],
]:
    """Return theta, powers, selected ambient rows, and their inverse."""

    theta = split.field_fixture(401)
    if split.l_power(theta, P**6) == theta:
        raise AssertionError("theta unexpectedly lies in F_(167^6)")
    powers = [split.L_ONE]
    for _ in range(DEGREE):
        powers.append(split.l_multiply(powers[-1], theta))

    # This deterministic theta has the following lexicographically first
    # independent row set.  Derive it rather than pinning it blindly.
    selected: list[int] = []
    for row in range(AMBIENT):
        candidate = selected + [row]
        rectangular = [
            [vector(powers[column])[index] for column in range(DEGREE)]
            for index in candidate
        ]
        # Rank by elimination on the small candidate matrix.
        rank_work = [values[:] for values in rectangular]
        rank = 0
        for column in range(DEGREE):
            pivot = next(
                (
                    index
                    for index in range(rank, len(rank_work))
                    if rank_work[index][column] % P
                ),
                None,
            )
            if pivot is None:
                continue
            rank_work[rank], rank_work[pivot] = (
                rank_work[pivot],
                rank_work[rank],
            )
            scale = pow(rank_work[rank][column], -1, P)
            rank_work[rank] = [
                value * scale % P for value in rank_work[rank]
            ]
            for index in range(len(rank_work)):
                if index == rank:
                    continue
                scale = rank_work[index][column] % P
                if scale:
                    rank_work[index] = [
                        (left - scale * right) % P
                        for left, right in zip(
                            rank_work[index], rank_work[rank]
                        )
                    ]
            rank += 1
            if rank == len(rank_work):
                break
        if rank == len(candidate):
            selected.append(row)
        if len(selected) == DEGREE:
            break
    if len(selected) != DEGREE:
        raise AssertionError("theta powers do not span E")

    square = [
        [vector(powers[column])[row] for column in range(DEGREE)]
        for row in selected
    ]
    inverse = inverse_mod(square)
    return (
        theta,
        tuple(powers),
        tuple(selected),
        tuple(tuple(row) for row in inverse),
    )


def coordinate_map(
    powers: Sequence[split.L],
    selected: Sequence[int],
    inverse: Sequence[Sequence[int]],
):
    def coordinates(value: split.L) -> tuple[int, ...]:
        selected_value = tuple(vector(value)[row] for row in selected)
        result = matrix_vector(inverse, selected_value)
        reconstructed = split.L_ZERO
        for coefficient, power in zip(result, powers):
            if coefficient:
                reconstructed = split.l_add(
                    reconstructed,
                    split.l_multiply(split.l_embed((coefficient, 0)), power),
                )
        if reconstructed != value:
            raise AssertionError("an exported value lies outside E")
        return result

    return coordinates


def load_cases() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    seen: set[tuple[object, ...]] = set()
    for filename in (
        "h2_factors_0_2_certificate.json",
        "h2_astar_a_all_factors_certificate.json",
    ):
        payload = json.loads((PROMOTED / filename).read_text())
        for item in payload["audits"]:
            if item["primitive_factor"] != 0:
                continue
            key = (
                item["label"],
                item["channel"],
                tuple(item["profile_ids"]),
            )
            if key in seen:
                continue
            seen.add(key)
            rows.append(
                {
                    "label": item["label"],
                    "channel": item["channel"],
                    "profile_ids": tuple(item["profile_ids"]),
                }
            )
    if len(rows) != 15:
        raise AssertionError(f"expected 15 seed/channel cases, found {len(rows)}")
    return rows


def write_u32(handle, value: int) -> None:
    handle.write(struct.pack("<I", value))


def export(output: Path, metadata_output: Path) -> dict[str, object]:
    theta, powers, selected, inverse = field_basis()
    coordinates = coordinate_map(powers, selected, inverse)
    theta_relation = coordinates(powers[DEGREE])
    alpha = phase167.ninth_root_of_unity()
    cases = load_cases()

    metadata_cases = []
    with output.open("wb") as handle:
        handle.write(MAGIC)
        handle.write(bytes(theta_relation))
        write_u32(handle, len(cases))
        for case in cases:
            label = f"{case['label']}:{case['channel']}".encode("ascii")
            write_u32(handle, len(label))
            handle.write(label)
            channel = 0 if case["channel"] == "A" else 1
            handle.write(bytes((channel,)))
            profile_ids = tuple(int(value) for value in case["profile_ids"])
            handle.write(bytes(profile_ids))

            per_factor_option_counts = []
            for factor in range(6):
                constant = coordinates(
                    audit.zero_column_value(channel, alpha)
                )
                handle.write(bytes(constant))
                options = audit.class_options(
                    profile_ids, alpha, factor, channel
                )
                factor_counts = []
                for _, alphabet in options:
                    write_u32(handle, len(alphabet))
                    factor_counts.append(len(alphabet))
                    for ambient_value in alphabet:
                        value = tuple(
                            (int(ambient_value[2 * index]),
                             int(ambient_value[2 * index + 1]))
                            for index in range(18)
                        )
                        handle.write(bytes(coordinates(value)))
                per_factor_option_counts.append(factor_counts)
            if any(
                counts != per_factor_option_counts[0]
                for counts in per_factor_option_counts[1:]
            ):
                raise AssertionError("factor alphabets changed option counts")
            metadata_cases.append(
                {
                    "label": label.decode("ascii"),
                    "profile_ids": list(profile_ids),
                    "class_option_counts": per_factor_option_counts[0],
                }
            )

    metadata = {
        "schema": "h668-ratio-torus-character-input-v1",
        "prime": P,
        "degree": DEGREE,
        "theta_source": "field_fixture(401)",
        "selected_ambient_rows": list(selected),
        "theta_power_relation": list(theta_relation),
        "cases": metadata_cases,
        "binary_bytes": output.stat().st_size,
    }
    metadata_output.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n"
    )
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=HERE / "character_instances.bin",
    )
    parser.add_argument(
        "--metadata-output",
        type=Path,
        default=HERE / "character_instances.json",
    )
    args = parser.parse_args()
    metadata = export(args.output, args.metadata_output)
    print(f"cases={len(metadata['cases'])}")
    print(f"binary_bytes={metadata['binary_bytes']}")
    print(
        "theta_power_relation="
        + ",".join(str(value) for value in metadata["theta_power_relation"])
    )


if __name__ == "__main__":
    main()
