#!/usr/bin/env python3
"""Verify the exact SOS certificate for the qutrit boundary quartic.

The certificate contains one rational range basis and one positive
definite reduced Gram matrix for every character block.  This verifier
rebuilds the quartic exactly, reconstructs the character blocks, checks
all positive LDL pivots, and compares every polynomial coefficient.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT
    / "verification"
    / "certificates"
    / "n3_boundary_flat_quartic_sos.json"
)


def span_basis(rows):
    basis = {}
    for row in rows:
        value = row
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                for other, entry in tuple(basis.items()):
                    if other != pivot and ((entry >> pivot) & 1):
                        basis[other] = entry ^ value
                break
    return basis


def quotient(value, basis):
    for pivot in sorted(basis, reverse=True):
        if (value >> pivot) & 1:
            value ^= basis[pivot]
    return value


def decode_matrix(data):
    return [
        [Fraction(numerator, denominator) for numerator, denominator in row]
        for row in data
    ]


def positive_ldl(matrix):
    size = len(matrix)
    lower = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    pivots = []
    for i in range(size):
        lower[i][i] = 1
        pivot = matrix[i][i] - sum(
            lower[i][k] ** 2 * pivots[k] for k in range(i)
        )
        assert pivot > 0
        pivots.append(pivot)
        for j in range(i + 1, size):
            lower[j][i] = (
                matrix[j][i]
                - sum(
                    lower[j][k] * lower[i][k] * pivots[k]
                    for k in range(i)
                )
            ) / pivot


def verify_certificate(path: Path, expected_format: str) -> None:
    certificate = json.loads(path.read_text())
    assert certificate["format"] == expected_format
    dimension = certificate["dimension"]
    terms = {}
    for indices, encoded in certificate["quartic_terms"]:
        assert len(indices) == 4
        assert indices == sorted(indices)
        exponent = tuple(indices.count(index) for index in range(dimension))
        assert exponent not in terms
        terms[exponent] = Fraction(*encoded)
        assert terms[exponent]

    parity_basis = span_basis(
        [
            sum(
                1 << index
                for index, power in enumerate(exponent)
                if power & 1
            )
            for exponent in terms
        ]
    )
    active = {
        index
        for index in range(dimension)
        if terms.get(
            tuple(4 if other == index else 0 for other in range(dimension)),
            0,
        )
    }
    monomials = [(index, index) for index in active]
    for first, second in itertools.combinations(range(dimension), 2):
        exponent = tuple(
            2 if index in (first, second) else 0
            for index in range(dimension)
        )
        if terms.get(exponent, 0) or first in active and second in active:
            monomials.append((first, second))
    monomials.sort()

    by_character = defaultdict(list)
    for number, (first, second) in enumerate(monomials):
        parity = 0 if first == second else (1 << first) ^ (1 << second)
        by_character[quotient(parity, parity_basis)].append(number)
    blocks = list(by_character.values())

    bases = [decode_matrix(matrix) for matrix in certificate["bases"]]
    reduced = [
        decode_matrix(matrix) for matrix in certificate["reduced_grams"]
    ]
    assert len(bases) == len(reduced) == len(blocks)

    reconstructed = defaultdict(Fraction)
    for block, basis, small_gram in zip(blocks, bases, reduced):
        assert len(basis) == len(block)
        rank = len(basis[0])
        assert all(len(row) == rank for row in basis)
        assert len(small_gram) == rank
        assert all(len(row) == rank for row in small_gram)
        assert small_gram == [list(row) for row in zip(*small_gram)]
        positive_ldl(small_gram)

        full = [
            [
                sum(
                    basis[i][a]
                    * small_gram[a][b]
                    * basis[j][b]
                    for a in range(rank)
                    for b in range(rank)
                )
                for j in range(len(block))
            ]
            for i in range(len(block))
        ]
        for i, global_i in enumerate(block):
            for j in range(i, len(block)):
                global_j = block[j]
                exponent = [0] * dimension
                for index in monomials[global_i]:
                    exponent[index] += 1
                for index in monomials[global_j]:
                    exponent[index] += 1
                reconstructed[tuple(exponent)] += (
                    1 if i == j else 2
                ) * full[i][j]

    all_exponents = set(terms) | set(reconstructed)
    assert all(
        reconstructed[exponent] == terms.get(exponent, Fraction(0))
        for exponent in all_exponents
    )
    print(
        "verified exact SOS",
        expected_format,
        ":",
        len(blocks),
        "positive character blocks and",
        len(all_exponents),
        "exact coefficients",
    )


def main() -> None:
    verify_certificate(
        CERTIFICATE,
        "n3-flat-kernel-rational-face-v2",
    )


if __name__ == "__main__":
    main()
