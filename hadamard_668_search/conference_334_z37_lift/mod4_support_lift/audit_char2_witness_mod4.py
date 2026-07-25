#!/usr/bin/env python3
"""Audit the next 2-adic digit of the two exact characteristic-two supports.

The input witnesses satisfy A^2+A=83(I+J) modulo two, exact integral
block margins, and the 6/3 diagonal trace law.  This script independently
computes their residual modulo four.  A zero residual would be a
conference-core solution modulo 16.  A nonzero residual only rejects the
particular witness, not its parity type or quotient.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


P = 37
N = 9


def semantic_hash(payload: dict[str, object]) -> str:
    stripped = dict(payload)
    stripped.pop("semantic_sha256", None)
    encoded = json.dumps(
        stripped, sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def reverse_word(word: int) -> int:
    result = word & 1
    for lag in range(1, P):
        result |= ((word >> lag) & 1) << (P - lag)
    return result


def load(path: Path) -> tuple[dict[str, object], list[list[int]]]:
    payload = json.loads(path.read_text())
    assert payload["schema"] == "h668-c37-char2-support-witness-v1"
    assert payload["semantic_sha256"] == semantic_hash(payload)
    encoded = payload["word_hex"]
    assert isinstance(encoded, list) and len(encoded) == N
    words = [[int(value, 16) for value in row] for row in encoded]
    assert all(len(row) == N for row in words)
    return payload, words


def audit(path: Path) -> dict[str, object]:
    payload, words = load(path)
    quotient = payload["quotient"]
    assert isinstance(quotient, list)
    residues = {value * value % P for value in range(1, P)}

    for i in range(N):
        for j in range(N):
            assert words[i][j] == reverse_word(words[j][i])
            assert words[i][j].bit_count() == quotient[i][j]
        assert words[i][i] & 1 == 0
    for lag in range(1, P):
        incidence = sum((words[i][i] >> lag) & 1 for i in range(N))
        assert incidence == (6 if lag in residues else 3)

    full_histogram = [0] * 4
    independent_histogram = [0] * 4
    for i in range(N):
        for j in range(N):
            for lag in range(P):
                value = (words[i][j] >> lag) & 1
                for middle in range(N):
                    for source in range(P):
                        value += (
                            ((words[i][middle] >> source) & 1)
                            * (
                                (
                                    words[middle][j]
                                    >> ((lag - source) % P)
                                )
                                & 1
                            )
                        )
                target = 83 * (
                    1 + (1 if i == j and lag == 0 else 0)
                )
                residue = (value - target) % 4
                full_histogram[residue] += 1
                if i < j or (i == j and lag <= P // 2):
                    independent_histogram[residue] += 1

    assert full_histogram[1] == full_histogram[3] == 0
    assert independent_histogram[1] == independent_histogram[3] == 0
    assert sum(full_histogram) == N * N * P
    assert sum(independent_histogram) == 1503
    return {
        "path": str(path),
        "quotient_type": payload["quotient_type"],
        "semantic_sha256": payload["semantic_sha256"],
        "full_mod4_residue_histogram": full_histogram,
        "independent_mod4_residue_histogram": independent_histogram,
        "independent_carry_defects": independent_histogram[2],
        "independent_coefficients": 1503,
        "passes_adjacency_mod2": full_histogram[1] + full_histogram[3] == 0,
        "passes_adjacency_mod4": full_histogram[2] == 0,
        "scope": (
            "A nonzero carry rejects only this characteristic-two "
            "support witness, not the quotient or parity type."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("witness", type=Path, nargs="+")
    args = parser.parse_args()
    reports = [audit(path) for path in args.witness]
    print(json.dumps(reports, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
