#!/usr/bin/env python3
"""Compare all actual subgroup sets produced by the two standalone verifiers.

Element numbers differ between implementations. Convert both sides to sets
of actual matrices before comparing, rather than comparing indices or orders.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path


def decode_matrix(value: int, prime: int) -> tuple[int, int, int, int]:
    entries = []
    for _ in range(4):
        value, digit = divmod(value, prime)
        entries.append(digit)
    if value != 0:
        raise ValueError("Matrix encoding is outside the expected range")
    return tuple(reversed(entries))


def compare(python_path: Path, cpp_path: Path) -> None:
    certificate = json.loads(python_path.read_text())
    prime = certificate["prime"]
    matrices = [tuple(matrix) for matrix in certificate["matrices"]]
    python_subgroups = {
        frozenset(matrices[index] for index in subgroup["elements"])
        for subgroup in certificate["subgroups"]
    }
    lines = cpp_path.read_text().splitlines()
    claimed_count = int(lines[0])
    cpp_subgroups = {
        frozenset(decode_matrix(int(value), prime) for value in line.split())
        for line in lines[1:] if line.strip()
    }
    if len(lines) - 1 != claimed_count or len(cpp_subgroups) != claimed_count:
        raise AssertionError("C++ subgroup export contains omissions or duplicates")
    if len(python_subgroups) != len(certificate["subgroups"]):
        raise AssertionError("Python subgroup export contains duplicates")
    if python_subgroups != cpp_subgroups or claimed_count != 76:
        raise AssertionError("The actual subgroup sets do not agree")
    print("PASS: all 76 actual matrix subgroups agree between Python and C++,")
    print("despite different element orderings and independent generation.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("python_certificate", type=Path)
    parser.add_argument("cpp_export", type=Path)
    args = parser.parse_args()
    compare(args.python_certificate, args.cpp_export)
