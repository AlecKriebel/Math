#!/usr/bin/env python3
"""Independent exact audit of the centered degree-two repair certificate.

This checker authenticates the frozen certificate, recomputes the flag moment
with a separate direct loop over actual vertex pairs, and certifies the
seven-dimensional quotient by an exact LDL^T factorization.
"""

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
    / "centered_degree2_repair_certificate.json"
)
EXPECTED_SHA256 = (
    "7b8dd73bfdaced21fe6a6f6acd74231a976b7359bce600cf45c0d1c44db895d6"
)
PAIRS = tuple(itertools.combinations(range(6), 2))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}
QUOTIENT_INDICES = (0, 1, 5, 7, 12, 13, 14)


class VerificationError(Exception):
    """Raised when the independent exact audit fails."""


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def edge(edges, first, second):
    return edges[PAIR_INDEX[tuple(sorted((first, second)))]]


def basis_values(edges, root, extension):
    i, j = root
    p, r = extension
    q = edge(edges, i, j) - 4
    ip = edge(edges, i, p) - 4
    jp = edge(edges, j, p) - 4
    ir = edge(edges, i, r) - 4
    jr = edge(edges, j, r) - 4
    pr = edge(edges, p, r) - 4
    return (
        1,
        q,
        pr,
        ip + ir,
        jp + jr,
        q**2,
        q * pr,
        pr**2,
        q * (ip + ir),
        q * (jp + jr),
        pr * (ip + ir),
        pr * (jp + jr),
        ip**2 + ir**2,
        jp**2 + jr**2,
        ip * jp + ir * jr,
        ip * ir,
        jp * jr,
        ip * jr + jp * ir,
    )


def direct_atomic_matrix(edges):
    matrix = [[0] * 18 for _ in range(18)]
    for root in itertools.permutations(range(6), 2):
        residual = tuple(vertex for vertex in range(6) if vertex not in root)
        extensions = tuple(itertools.combinations(residual, 2))
        values = [
            basis_values(edges, root, extension)
            for extension in extensions
        ]
        for left_index, left in enumerate(extensions):
            for right_index, right in enumerate(extensions):
                coefficient = {
                    2: 494,
                    3: 9139,
                    4: 329004,
                }[len(set(left) | set(right))]
                for row, left_value in enumerate(values[left_index]):
                    for column, right_value in enumerate(
                        values[right_index]
                    ):
                        matrix[row][column] += (
                            coefficient * left_value * right_value
                        )
    return tuple(tuple(row) for row in matrix)


def ldl_pivots(matrix):
    size = len(matrix)
    lower = [[Q(0)] * size for _ in range(size)]
    diagonal = [Q(0)] * size
    for row in range(size):
        lower[row][row] = Q(1)
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


def rank(matrix):
    work = [[Q(entry) for entry in row] for row in matrix]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(work))
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        for entry in range(column, len(work[0])):
            work[pivot_row][entry] /= pivot_value
        for row in range(pivot_row + 1, len(work)):
            scale = work[row][column]
            if scale == 0:
                continue
            for entry in range(column, len(work[0])):
                work[row][entry] -= scale * work[pivot_row][entry]
        pivot_row += 1
    return pivot_row


def make_kernel(entries):
    vector = [0] * 18
    for index, value in entries.items():
        vector[index] = value
    return tuple(vector)


def independent_centered_kernels():
    return (
        make_kernel({0: 152, 1: 38, 3: 741}),
        make_kernel({0: 152, 1: 38, 4: 741}),
        make_kernel({0: 74, 1: -1, 2: 741}),
        make_kernel({1: 152, 5: 38, 8: 741}),
        make_kernel({1: 152, 5: 38, 9: 741}),
        make_kernel({1: 74, 5: -1, 6: 741}),
        make_kernel({0: -608, 1: -304, 5: -38, 12: 741, 15: 56316}),
        make_kernel({0: -608, 1: -304, 5: -38, 13: 741, 16: 56316}),
        make_kernel({0: -608, 1: -304, 5: -38, 14: 741, 17: 28158}),
        make_kernel({3: 4, 10: 38, 12: 1, 14: 1}),
        make_kernel({4: 4, 11: 38, 13: 1, 14: 1}),
    )


def verify(certificate_path=CERTIFICATE):
    require(
        hashlib.sha256(certificate_path.read_bytes()).hexdigest()
        == EXPECTED_SHA256,
        "certificate hash mismatch",
    )
    data = json.loads(certificate_path.read_text())
    weights = tuple(Q(atom["weight"]) for atom in data["atoms"])
    require(all(weight > 0 for weight in weights), "weight is not positive")
    require(sum(weights) == 1, "weights do not sum to one")

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
            for column in range(18)
        )
        for row in range(18)
    )
    require(
        moment
        == tuple(
            tuple(Q(value) for value in row)
            for row in data["moment_matrix"]
        ),
        "independently recomputed moment mismatch",
    )

    kernels = independent_centered_kernels()
    for kernel in kernels:
        require(
            all(
                sum(
                    kernel[row] * moment[row][column]
                    for row in range(18)
                )
                == 0
                for column in range(18)
            ),
            "independent centered kernel does not annihilate moment",
        )
    coordinates = []
    for index in QUOTIENT_INDICES:
        coordinate = [0] * 18
        coordinate[index] = 1
        coordinates.append(tuple(coordinate))
    require(
        rank(kernels + tuple(coordinates)) == 18,
        "kernel and quotient vectors do not span feature space",
    )
    require(rank(moment) == 7, "full moment rank is not seven")

    quotient = tuple(
        tuple(moment[row][column] for column in QUOTIENT_INDICES)
        for row in QUOTIENT_INDICES
    )
    pivots = ldl_pivots(quotient)
    require(all(pivot > 0 for pivot in pivots), "nonpositive LDL pivot")

    return {
        "status": "PASS",
        "certificate_sha256": EXPECTED_SHA256,
        "direct_atomic_recomputation": "PASS",
        "centered_kernel_radical": "dimension 11",
        "full_moment_rank": 7,
        "quotient_LDL_pivots": "all positive",
        "pivot_values": [str(value) for value in pivots],
    }


def main():
    require(
        len(sys.argv) <= 2,
        "usage: independent_centered_degree2_audit.py [certificate]",
    )
    certificate_path = Path(sys.argv[1]) if len(sys.argv) == 2 else CERTIFICATE
    print(json.dumps(verify(certificate_path), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
