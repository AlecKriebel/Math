#!/usr/bin/env python3
"""Verify the rational Lovasz-theta certificate using exact arithmetic only."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
DEFAULT_CERTIFICATE = HERE / "certificates" / "lovasz_theta_primal.json"


def decode_graph6(record: str) -> tuple[int, tuple[int, ...]]:
    """Decode a small graph6 record into bitset neighborhoods.

    This verifier deliberately implements its own decoder and accepts only the
    one-byte order format needed by the ten-vertex certificate.
    """

    text = record.strip()
    if text.startswith(">>graph6<<"):
        text = text[len(">>graph6<<") :]
    if not text:
        raise ValueError("empty graph6 record")
    values = [ord(character) - 63 for character in text]
    if any(value < 0 or value > 63 for value in values):
        raise ValueError("graph6 contains a non-ASCII payload character")
    order = values[0]
    if order == 63:
        raise ValueError("only the small graph6 order format is accepted")

    slot_count = order * (order - 1) // 2
    expected_payload = (slot_count + 5) // 6
    if len(values) != 1 + expected_payload:
        raise ValueError("graph6 payload has the wrong length")

    bits: list[int] = []
    for value in values[1:]:
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    if any(bits[slot_count:]):
        raise ValueError("graph6 padding bits are nonzero")

    adjacency = [0] * order
    position = 0
    for upper in range(1, order):
        for lower in range(upper):
            if bits[position]:
                adjacency[lower] |= 1 << upper
                adjacency[upper] |= 1 << lower
            position += 1
    return order, tuple(adjacency)


def exact_ldl_pivots(matrix: list[list[int]]) -> tuple[Fraction, ...]:
    """Return the exact diagonal pivots in an unpivoted LDL^T factorization."""

    order = len(matrix)
    lower = [
        [Fraction(int(row == column)) for column in range(order)]
        for row in range(order)
    ]
    diagonal = [Fraction(0) for _ in range(order)]
    for row in range(order):
        diagonal[row] = Fraction(matrix[row][row]) - sum(
            lower[row][k] * lower[row][k] * diagonal[k]
            for k in range(row)
        )
        if diagonal[row] == 0:
            raise ValueError(f"zero LDL pivot at index {row}")
        for later in range(row + 1, order):
            lower[later][row] = (
                Fraction(matrix[later][row])
                - sum(
                    lower[later][k] * lower[row][k] * diagonal[k]
                    for k in range(row)
                )
            ) / diagonal[row]
    return tuple(diagonal)


def verify_certificate(data: dict[str, Any]) -> dict[str, Any]:
    if data.get("format") != "lovasz-theta-primal-rational-v1":
        raise ValueError("unknown theta-certificate format")
    graph6 = data.get("graph6")
    if not isinstance(graph6, str):
        raise ValueError("graph6 must be a string")
    order, adjacency = decode_graph6(graph6)
    size = sum(mask.bit_count() for mask in adjacency) // 2

    denominator = data.get("denominator")
    matrix = data.get("matrix")
    expected = data.get("expected")
    if not isinstance(denominator, int) or denominator <= 0:
        raise ValueError("denominator must be a positive integer")
    if not isinstance(matrix, list) or len(matrix) != order:
        raise ValueError("matrix order does not match the graph")
    if not isinstance(expected, dict):
        raise ValueError("missing expected-value block")
    if expected.get("order") != order or expected.get("size") != size:
        raise ValueError("graph order or size does not match the certificate")

    for row in matrix:
        if (
            not isinstance(row, list)
            or len(row) != order
            or any(not isinstance(entry, int) for entry in row)
        ):
            raise ValueError("matrix must be a square integer matrix")
    for row in range(order):
        for column in range(order):
            if matrix[row][column] != matrix[column][row]:
                raise ValueError("matrix is not symmetric")

    trace_numerator = sum(matrix[index][index] for index in range(order))
    if trace_numerator != denominator:
        raise ValueError("scaled matrix does not have trace one")
    if trace_numerator != expected.get("trace_numerator"):
        raise ValueError("trace numerator does not match the manifest")

    edge_count = 0
    for first in range(order):
        for second in range(first + 1, order):
            if adjacency[first] & (1 << second):
                edge_count += 1
                if matrix[first][second] != 0:
                    raise ValueError(
                        f"matrix entry on edge {first}-{second} is nonzero"
                    )
    if edge_count != size:
        raise AssertionError("internal edge count disagrees with graph size")

    pivots = exact_ldl_pivots(matrix)
    if any(pivot <= 0 for pivot in pivots):
        raise ValueError("matrix is not positive definite")

    objective_numerator = sum(sum(row) for row in matrix)
    if objective_numerator != expected.get("objective_numerator"):
        raise ValueError("objective numerator does not match the manifest")
    objective = Fraction(objective_numerator, denominator)
    if str(objective) != expected.get("objective_reduced"):
        raise ValueError("reduced objective does not match the manifest")
    if objective <= 3:
        raise ValueError("certificate does not separate theta from three")

    return {
        "graph6": graph6,
        "order": order,
        "size": size,
        "trace": "1",
        "edge_zero_count": edge_count,
        "positive_definite": True,
        "ldl_pivots": [str(pivot) for pivot in pivots],
        "objective": str(objective),
        "objective_decimal": f"{float(objective):.4f}",
        "theta_strictly_greater_than_3": True,
    }


def load_and_verify(path: Path = DEFAULT_CERTIFICATE) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        data = json.load(stream)
    if not isinstance(data, dict):
        raise ValueError("certificate root must be an object")
    return verify_certificate(data)


def main() -> None:
    print(json.dumps(load_and_verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
