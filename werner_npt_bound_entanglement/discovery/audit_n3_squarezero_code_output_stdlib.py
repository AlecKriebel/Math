#!/usr/bin/env python3
"""Floating-point audit of the square-zero code-output compression.

This intentionally uses only Python's standard library so saved NumPy
archives can be inspected on machines without NumPy.  It is discovery
code, not a verifier.
"""

from __future__ import annotations

import argparse
import ast
import cmath
import math
import struct
import zipfile


def read_npy_member(path: str, member: str):
    with zipfile.ZipFile(path) as archive:
        data = archive.read(member + ".npy")
    major = data[6]
    if major == 1:
        offset = 10
        header_length = struct.unpack("<H", data[8:10])[0]
    else:
        offset = 12
        header_length = struct.unpack("<I", data[8:12])[0]
    header = ast.literal_eval(
        data[offset : offset + header_length].decode().strip()
    )
    raw = data[offset + header_length :]
    if header["descr"] == "<c16":
        values = [complex(*pair) for pair in struct.iter_unpack("<dd", raw)]
    elif header["descr"] == "<f8":
        values = [item[0] for item in struct.iter_unpack("<d", raw)]
    else:
        raise ValueError(header["descr"])
    return header, values


def decode(index: int) -> tuple[int, int, int]:
    return index // 9, (index // 3) % 3, index % 3


WORDS = [decode(index) for index in range(27)]


def inner(left, right):
    return sum(x.conjugate() * y for x, y in zip(left, right))


def reduced_transition(left, right, retained):
    retained = tuple(retained)
    traced = tuple(site for site in range(3) if site not in retained)
    size = 3 ** len(retained)
    out = [[0j] * size for _ in range(size)]
    for row, row_word in enumerate(WORDS):
        for column, column_word in enumerate(WORDS):
            if all(row_word[site] == column_word[site] for site in traced):
                reduced_row = 0
                reduced_column = 0
                for site in retained:
                    reduced_row = 3 * reduced_row + row_word[site]
                    reduced_column = (
                        3 * reduced_column + column_word[site]
                    )
                out[reduced_row][reduced_column] += (
                    left[row] * right[column].conjugate()
                )
    return out


def embedded_entry(left, right, reduced, retained):
    retained = tuple(retained)
    complement = tuple(site for site in range(3) if site not in retained)
    answer = 0j
    for row, row_word in enumerate(WORDS):
        for column, column_word in enumerate(WORDS):
            if all(
                row_word[site] == column_word[site]
                for site in complement
            ):
                reduced_row = 0
                reduced_column = 0
                for site in retained:
                    reduced_row = 3 * reduced_row + row_word[site]
                    reduced_column = (
                        3 * reduced_column + column_word[site]
                    )
                answer += (
                    left[row].conjugate()
                    * reduced[reduced_row][reduced_column]
                    * right[column]
                )
    return answer


def add(*matrices):
    size = len(matrices[0])
    return [
        [
            sum(matrix[row][column] for matrix in matrices)
            for column in range(size)
        ]
        for row in range(size)
    ]


def scale(matrix, scalar):
    return [[scalar * value for value in row] for row in matrix]


def multiply(left, right):
    return [
        [
            sum(
                left[row][middle] * right[middle][column]
                for middle in range(len(right))
            )
            for column in range(len(right))
        ]
        for row in range(len(left))
    ]


def frobenius_norm(matrix):
    return math.sqrt(sum(abs(value) ** 2 for row in matrix for value in row))


def identity(size):
    return [
        [complex(row == column) for column in range(size)]
        for row in range(size)
    ]


def compression(left, right, retained):
    out = [[0j] * 4 for _ in range(4)]
    reductions = [
        [
            reduced_transition(right[b], right[d], retained)
            for d in range(2)
        ]
        for b in range(2)
    ]
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    out[2 * a + b][2 * c + d] = embedded_entry(
                        left[a],
                        left[c],
                        reductions[b][d],
                        retained,
                    )
    return out


def determinant(matrix):
    work = [row[:] for row in matrix]
    answer = 1 + 0j
    for column in range(len(work)):
        pivot = max(
            range(column, len(work)),
            key=lambda row: abs(work[row][column]),
        )
        if abs(work[pivot][column]) < 1e-14:
            return 0j
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        p = work[column][column]
        answer *= p
        for row in range(column + 1, len(work)):
            factor = work[row][column] / p
            for j in range(column + 1, len(work)):
                work[row][j] -= factor * work[column][j]
    return answer


def hermitian_eigenvalues(matrix):
    """Cyclic complex Jacobi diagonalization for a small Hermitian matrix."""
    work = [row[:] for row in matrix]
    size = len(work)
    for _ in range(500):
        p, q = max(
            (
                (row, column)
                for row in range(size)
                for column in range(row + 1, size)
            ),
            key=lambda pair: abs(work[pair[0]][pair[1]]),
        )
        value = work[p][q]
        if abs(value) < 1e-13:
            break
        app = work[p][p].real
        aqq = work[q][q].real
        phase = cmath.phase(value)
        tau = (aqq - app) / (2 * abs(value))
        tangent = (
            (1 if tau >= 0 else -1)
            / (abs(tau) + math.sqrt(1 + tau * tau))
        )
        cosine = 1 / math.sqrt(1 + tangent * tangent)
        sine = cosine * tangent * cmath.exp(1j * phase)
        for row in range(size):
            if row in (p, q):
                continue
            old_p = work[row][p]
            old_q = work[row][q]
            work[row][p] = cosine * old_p - sine.conjugate() * old_q
            work[row][q] = sine * old_p + cosine * old_q
            work[p][row] = work[row][p].conjugate()
            work[q][row] = work[row][q].conjugate()
        shift = tangent * abs(value)
        work[p][p] = app - shift
        work[q][q] = aqq + shift
        work[p][q] = 0j
        work[q][p] = 0j
    return sorted(work[index][index].real for index in range(size))


def plane_marginal(frame, site):
    blocks = [
        reduced_transition(frame[column], frame[column], (site,))
        for column in range(2)
    ]
    return add(*blocks)


def code_local_output(frame, site):
    out = [[0j] * 6 for _ in range(6)]
    for a in range(2):
        for b in range(2):
            block = reduced_transition(frame[a], frame[b], (site,))
            for row in range(3):
                for column in range(3):
                    out[3 * a + row][3 * b + column] = block[row][column]
    return out


def audit_orientation(left, right):
    one_site = [compression(left, right, (site,)) for site in range(3)]
    pair = [
        compression(left, right, retained)
        for retained in ((0, 1), (0, 2), (1, 2))
    ]
    one_sum = add(*one_site)
    pair_sum = add(*pair)
    unit = identity(4)
    deviation = add(one_sum, scale(unit, -1))
    baseline = scale(add(unit, scale(deviation, -1)), 0.5)
    gram = add(baseline, scale(pair_sum, 0.25))
    return {
        "gram": gram,
        "one_sum": one_sum,
        "pair_sum": pair_sum,
        "deviation": deviation,
        "baseline": baseline,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archive")
    args = parser.parse_args()
    header, values = read_npy_member(args.archive, "z")
    if header["shape"] != (27, 4):
        raise ValueError(header["shape"])
    columns = [
        [values[4 * row + column] for row in range(27)]
        for column in range(4)
    ]
    print(
        "frame error",
        max(
            abs(inner(columns[a], columns[b]) - (a == b))
            for a in range(4)
            for b in range(4)
        ),
    )
    left, right = columns[:2], columns[2:]
    local_determinants = [
        determinant(plane_marginal(frame, site)).real
        for frame in (left, right)
        for site in range(3)
    ]
    normalized_product = math.prod(
        27 * value / 8 for value in local_determinants
    )
    print("local determinants", local_determinants)
    print("normalized determinant product", normalized_product)
    for label, first, second in (
        ("right anchor", left, right),
        ("left anchor", right, left),
    ):
        data = audit_orientation(first, second)
        print(label)
        for key in ("gram", "deviation", "baseline", "pair_sum"):
            print(
                " ",
                key,
                "eigenvalues",
                hermitian_eigenvalues(data[key]),
                "det",
                determinant(data[key]).real,
            )
        commutator = add(
            multiply(data["deviation"], data["pair_sum"]),
            scale(multiply(data["pair_sum"], data["deviation"]), -1),
        )
        print("  deviation/pair commutator norm", frobenius_norm(commutator))
    for label, frame in (("left", left), ("right", right)):
        print(label, "logical-local spectra")
        for site in range(3):
            print(
                " ",
                site,
                hermitian_eigenvalues(code_local_output(frame, site)),
            )


if __name__ == "__main__":
    main()
