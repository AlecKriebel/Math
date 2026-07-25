#!/usr/bin/env python3
"""Independent direct-loop audit of the four-feature flag moment block."""

from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    ROOT
    / "experiments"
    / "global_flag_reoptimization"
    / "psd4_repair_certificate.json"
)
EXPECTED_SHA256 = (
    "cbc41e280054de15da735ffc0644e4aa696fe2dad884dd6d77c0a6ef8894cad4"
)
PAIRS = tuple(itertools.combinations(range(6), 2))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}


class VerificationError(Exception):
    """Raised when the independent exact audit fails."""


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def edge(edges, first, second):
    return edges[PAIR_INDEX[tuple(sorted((first, second)))]]


def features(edges, root, extension):
    i, j = root
    p, q = extension
    base = edge(edges, i, j) - 4
    ip = edge(edges, i, p) - 4
    jp = edge(edges, j, p) - 4
    iq = edge(edges, i, q) - 4
    jq = edge(edges, j, q) - 4
    pq = edge(edges, p, q) - 4
    return (
        pq,
        pq * (ip + iq),
        base * pq,
        ip * jq + iq * jp,
    )


def direct_atomic_matrix(edges):
    matrix = [[0] * 4 for _ in range(4)]
    for root in itertools.permutations(range(6), 2):
        residual = [vertex for vertex in range(6) if vertex not in root]
        extensions = tuple(itertools.combinations(residual, 2))
        values = [features(edges, root, extension) for extension in extensions]
        for left, first in enumerate(extensions):
            for right, second in enumerate(extensions):
                union_size = len(set(first) | set(second))
                coefficient = {2: 494, 3: 9139, 4: 329004}[union_size]
                for row in range(4):
                    for column in range(4):
                        matrix[row][column] += (
                            coefficient
                            * values[left][row]
                            * values[right][column]
                        )
    return tuple(tuple(row) for row in matrix)


def ldl_pivots(matrix):
    size = len(matrix)
    lower = [[Q(0)] * size for _ in range(size)]
    diagonal = [Q(0)] * size
    for row in range(size):
        lower[row][row] = 1
        for column in range(row):
            residual = Q(matrix[row][column]) - sum(
                lower[row][index]
                * lower[column][index]
                * diagonal[index]
                for index in range(column)
            )
            require(
                diagonal[column] != 0,
                "zero pivot in independent LDL factorization",
            )
            lower[row][column] = residual / diagonal[column]
        diagonal[row] = Q(matrix[row][row]) - sum(
            lower[row][index] ** 2 * diagonal[index]
            for index in range(row)
        )
    return tuple(diagonal)


def verify(certificate_path=CERTIFICATE):
    require(
        hashlib.sha256(certificate_path.read_bytes()).hexdigest()
        == EXPECTED_SHA256,
        "certificate hash mismatch",
    )
    data = json.loads(certificate_path.read_text())
    weights = tuple(Q(atom["weight"]) for atom in data["atoms"])
    atomic = []
    for atom in data["atoms"]:
        edges = tuple(
            atom[
                "edge_color_indices_01_02_03_04_05_12_13_14_15_23_24_25_34_35_45"
            ]
        )
        atomic.append(direct_atomic_matrix(edges))
    moment = tuple(
        tuple(
            sum(
                weight * matrix[row][column]
                for weight, matrix in zip(weights, atomic)
            )
            for column in range(4)
        )
        for row in range(4)
    )
    require(
        moment
        == tuple(
            tuple(Q(value) for value in row)
            for row in data["moment_matrix"]
        ),
        "independently recomputed moment mismatch",
    )
    pivots = ldl_pivots(moment)
    require(all(pivot > 0 for pivot in pivots), "nonpositive LDL pivot")

    # The previously separating continuous polynomial is the direction
    # 8 F0 - 3 F1 in this scaled basis.
    direction = (8, -3, 0, 0)
    repaired_row = sum(
        direction[row]
        * moment[row][column]
        * direction[column]
        for row in range(4)
        for column in range(4)
    )
    require(repaired_row > 0, "old separator direction is not repaired")
    return {
        "status": "PASS",
        "direct_atomic_recomputation": "PASS",
        "LDL_pivots": "all positive",
        "pivot_values": [str(value) for value in pivots],
        "repaired_old_separator": str(repaired_row),
    }


def main():
    require(
        len(sys.argv) <= 2,
        "usage: independent_psd4_audit.py [certificate]",
    )
    certificate_path = Path(sys.argv[1]) if len(sys.argv) == 2 else CERTIFICATE
    print(json.dumps(verify(certificate_path), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
