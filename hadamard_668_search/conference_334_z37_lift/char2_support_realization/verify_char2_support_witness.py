#!/usr/bin/env python3
"""Independent bit-level replay of the C37 characteristic-two witness.

This verifier deliberately does not use the finite-field or unitary
machinery in ``search_char2_support.cpp``.  It reads the 45 upper-triangular
37-bit supports, reconstructs lower blocks by cyclic reversal, and checks
the complete 333-vertex adjacency equation in F_2[C_37]:

    A^2 + A = delta I + (1+x+...+x^36) J.

It also checks the exact integral orbit margins and the 6/3 diagonal
quadratic-character trace law.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


P = 37
N = 9
MASK = (1 << P) - 1

TYPE1_QUOTIENT = [
    [16, 18, 18, 18, 22, 22, 22, 13, 17],
    [18, 16, 18, 18, 22, 22, 13, 22, 17],
    [18, 18, 16, 18, 22, 13, 22, 22, 17],
    [18, 18, 18, 16, 13, 22, 22, 22, 17],
    [22, 22, 22, 13, 18, 17, 17, 17, 18],
    [22, 22, 13, 22, 17, 18, 17, 17, 18],
    [22, 13, 22, 22, 17, 17, 18, 17, 18],
    [13, 22, 22, 22, 17, 17, 17, 18, 18],
    [17, 17, 17, 17, 18, 18, 18, 18, 26],
]

TYPE2_QUOTIENT = [
    [24, 20, 20, 20, 18, 18, 16, 15, 15],
    [20, 22, 14, 14, 19, 19, 17, 22, 19],
    [20, 14, 18, 17, 24, 15, 19, 18, 21],
    [20, 14, 17, 18, 15, 24, 19, 18, 21],
    [18, 19, 24, 15, 14, 16, 21, 20, 19],
    [18, 19, 15, 24, 16, 14, 21, 20, 19],
    [16, 17, 19, 19, 21, 21, 20, 21, 12],
    [15, 22, 18, 18, 20, 20, 21, 12, 20],
    [15, 19, 21, 21, 19, 19, 12, 20, 20],
]


def reverse_cyclic(word: int) -> int:
    result = word & 1
    for lag in range(1, P):
        if word >> lag & 1:
            result |= 1 << (P - lag)
    return result


def convolution_coefficient(left: int, right: int, lag: int) -> int:
    result = 0
    for source in range(P):
        result ^= (
            (left >> source & 1)
            & (right >> ((lag - source) % P) & 1)
        )
    return result


def integer_convolution_coefficient(
    left: int, right: int, lag: int
) -> int:
    return sum(
        (left >> source & 1)
        * (right >> ((lag - source) % P) & 1)
        for source in range(P)
    )


def quadratic_residues() -> set[int]:
    return {value * value % P for value in range(1, P)}


def parse_witness(path: Path) -> tuple[int, list[list[int]], str]:
    if path.suffix == ".json":
        payload = json.loads(path.read_text())
        assert payload["schema"] == "h668-c37-char2-support-witness-v1"
        quotient_type = int(payload["quotient_type"])
        assert quotient_type in (1, 2)
        expected_quotient = (
            TYPE1_QUOTIENT if quotient_type == 1 else TYPE2_QUOTIENT
        )
        assert payload["quotient"] == expected_quotient
        assert payload["trace_orientation"] == "QR=6,NR=3"
        assert payload["adjacency_modulus"] == 2
        asserted_semantic = payload.pop("semantic_sha256")
        semantic = json.dumps(
            payload, sort_keys=True, separators=(",", ":")
        ).encode()
        digest = hashlib.sha256(semantic).hexdigest()
        assert digest == asserted_semantic
        encoded = payload["word_hex"]
        assert len(encoded) == N and all(len(row) == N for row in encoded)
        blocks = [
            [int(value, 16) for value in row] for row in encoded
        ]
        return quotient_type, blocks, digest

    text = path.read_text()
    assert "status PASS" in text
    quotient_type: int | None = None
    blocks: list[list[int | None]] = [
        [None for _ in range(N)] for _ in range(N)
    ]
    block_lines = 0
    for line in text.splitlines():
        fields = line.split()
        if not fields:
            continue
        if fields[0] == "quotient_type":
            quotient_type = int(fields[1])
        elif fields[0] == "block":
            i, j = map(int, fields[1:3])
            word = int(fields[3], 16)
            reported_weight = int(fields[4])
            reported_target = int(fields[5])
            assert 0 <= i <= j < N
            assert word & ~MASK == 0
            assert word.bit_count() == reported_weight == reported_target
            assert blocks[i][j] is None
            blocks[i][j] = word
            block_lines += 1
    assert quotient_type in (1, 2)
    assert block_lines == N * (N + 1) // 2
    for i in range(N):
        for j in range(i, N):
            assert blocks[i][j] is not None
            word = int(blocks[i][j])
            blocks[i][j] = word
            blocks[j][i] = reverse_cyclic(word)
    return (
        quotient_type,
        [[int(entry) for entry in row] for row in blocks],
        hashlib.sha256(text.encode()).hexdigest(),
    )


def verify(path: Path) -> None:
    quotient_type, blocks, digest = parse_witness(path)
    quotient = TYPE1_QUOTIENT if quotient_type == 1 else TYPE2_QUOTIENT

    assert quotient == [list(row) for row in zip(*quotient)]
    assert all(sum(row) == 166 for row in quotient)
    for i in range(N):
        for j in range(N):
            assert blocks[j][i] == reverse_cyclic(blocks[i][j])
            assert blocks[i][j].bit_count() == quotient[i][j]
            assert blocks[i][j].bit_count() % 2 == quotient[i][j] % 2
        assert blocks[i][i] & 1 == 0
        assert blocks[i][i] == reverse_cyclic(blocks[i][i])

    residues = quadratic_residues()
    incidence = {
        lag: sum(blocks[i][i] >> lag & 1 for i in range(N))
        for lag in range(1, P)
    }
    assert all(
        incidence[lag] == (6 if lag in residues else 3)
        for lag in range(1, P)
    )

    checked_coefficients = 0
    for i in range(N):
        for j in range(N):
            for lag in range(P):
                value = blocks[i][j] >> lag & 1
                for k in range(N):
                    value ^= convolution_coefficient(
                        blocks[i][k], blocks[k][j], lag
                    )
                expected = 1 ^ int(i == j and lag == 0)
                assert value == expected, (i, j, lag, value, expected)
                checked_coefficients += 1

    mod4_defects = 0
    diagonal_mod4_defects = 0
    mod4_constraints = 0
    for i in range(N):
        for j in range(i, N):
            lag_range = range(19) if i == j else range(P)
            for lag in lag_range:
                value = blocks[i][j] >> lag & 1
                for k in range(N):
                    value += integer_convolution_coefficient(
                        blocks[i][k], blocks[k][j], lag
                    )
                target = 83 * (1 + int(i == j and lag == 0))
                residue = (value - target) % 4
                assert residue % 2 == 0
                if residue:
                    mod4_defects += 1
                    diagonal_mod4_defects += i == j
                mod4_constraints += 1
    assert mod4_constraints == 1503
    if path.suffix == ".json":
        payload = json.loads(path.read_text())
        if "mod4_carry_defects" in payload:
            assert payload["mod4_independent_constraints"] == 1503
            assert payload["mod4_carry_defects"] == mod4_defects
    else:
        for line in path.read_text().splitlines():
            if line.startswith("carry_best_defects "):
                assert int(line.split()[1]) == mod4_defects

    # For any binary word f of size k, the fixed-field norm f*f^*
    # has absolute trace C(k,2) mod 2.  Directly recover that trace as the
    # parity of the 18 nonzero inverse-pair autocorrelation coefficients.
    norm_trace_edges = 0
    for i in range(N):
        degree_parity = 0
        for j in range(N):
            if i == j:
                continue
            word = blocks[i][j]
            norm_trace = 0
            for representative in range(1, 19):
                norm_trace ^= convolution_coefficient(
                    word, reverse_cyclic(word), representative
                )
            expected = quotient[i][j] * (quotient[i][j] - 1) // 2 & 1
            assert norm_trace == expected
            degree_parity ^= norm_trace
            if i < j:
                norm_trace_edges += norm_trace
        # The projection diagonal equation forces an Eulerian norm-trace
        # graph; this is also an exact quotient-level check.
        assert degree_parity == 0

    print(f"status PASS")
    print(f"quotient_type {quotient_type}")
    print(f"witness_sha256 {digest}")
    print(f"upper_blocks {N * (N + 1) // 2}")
    print(f"equation_coefficients {checked_coefficients}")
    print(
        f"mod4_carry_defects {mod4_defects}/1503 "
        f"diagonal={diagonal_mod4_defects} "
        f"offdiagonal={mod4_defects - diagonal_mod4_defects}"
    )
    print(f"norm_trace_edges {norm_trace_edges}")
    print("diagonal_trace QR=6 NR=3")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "witness",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("TYPE1_SUPPORT_WITNESS.txt"),
    )
    args = parser.parse_args()
    verify(args.witness)


if __name__ == "__main__":
    main()
