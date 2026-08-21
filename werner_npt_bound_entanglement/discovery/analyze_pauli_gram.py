"""Discovery-only Pauli-Gram diagnostics for a four-qutrit code frame.

The input format is the one written by search_n4_complex_sector_target:

    index  Re(u) Im(u) Re(v) Im(v)

Only the Python standard library is used.  Floating-point output is not a
certificate.
"""

from __future__ import annotations

import sys


def words() -> list[tuple[int, ...]]:
    out = []
    for index in range(81):
        value = index
        digits = []
        for _ in range(4):
            digits.append(value % 3)
            value //= 3
        out.append(tuple(digits))
    return out


WORDS = words()


def read_frame(path: str) -> tuple[list[complex], list[complex]]:
    u = [0j] * 81
    v = [0j] * 81
    with open(path, encoding="utf-8") as source:
        for line in source:
            fields = line.split()
            index = int(fields[0])
            u[index] = complex(float(fields[1]), float(fields[2]))
            v[index] = complex(float(fields[3]), float(fields[4]))
    return u, v


def encoded_paulis(
    u: list[complex], v: list[complex]
) -> list[list[complex]]:
    out = [[] for _ in range(4)]
    for i in range(81):
        for j in range(81):
            uu = u[i] * u[j].conjugate()
            vv = v[i] * v[j].conjugate()
            uv = u[i] * v[j].conjugate()
            vu = v[i] * u[j].conjugate()
            out[0].append(uu + vv)
            out[1].append(uv + vu)
            out[2].append(-1j * uv + 1j * vu)
            out[3].append(uu - vv)
    return out


def partial_trace(matrix: list[complex], retained: int) -> list[complex]:
    keep = [site for site in range(4) if retained >> site & 1]
    dimension = 3 ** len(keep)
    out = [0j] * (dimension * dimension)

    def retained_index(word: tuple[int, ...]) -> int:
        value = 0
        place = 1
        for site in keep:
            value += word[site] * place
            place *= 3
        return value

    indices = [retained_index(word) for word in WORDS]
    for i, left in enumerate(WORDS):
        row = indices[i]
        for j, right in enumerate(WORDS):
            if any(
                left[site] != right[site]
                for site in range(4)
                if not (retained >> site & 1)
            ):
                continue
            out[row * dimension + indices[j]] += matrix[81 * i + j]
    return out


def real_inner(left: list[complex], right: list[complex]) -> float:
    return sum(
        x.conjugate() * y for x, y in zip(left, right)
    ).real


def grams(paulis: list[list[complex]]) -> list[list[list[float]]]:
    out = []
    for subset in range(16):
        reduced = [
            partial_trace(pauli, subset) for pauli in paulis
        ]
        out.append(
            [
                [real_inner(reduced[a], reduced[b]) for b in range(4)]
                for a in range(4)
            ]
        )
    return out


def main() -> None:
    u, v = read_frame(sys.argv[1])
    gamma = grams(encoded_paulis(u, v))
    eta = (1.0, -1.0, -1.0, -1.0)
    alternating = [[0.0] * 4 for _ in range(4)]
    for subset in range(16):
        coefficient = -1.0 if bin(subset).count("1") & 1 else 1.0
        for a in range(4):
            for b in range(4):
                alternating[a][b] += coefficient * gamma[subset][a][b]

    d_matrix = [
        [alternating[a + 1][b + 1] - (2.0 if a == b else 0.0)
         for b in range(3)]
        for a in range(3)
    ]
    h_vector = alternating[0][1:]

    def c_value(left: int, right: int) -> float:
        return sum(
            eta[a] * eta[b]
            * gamma[left][a][b] * gamma[right][a][b]
            for a in range(4)
            for b in range(4)
        ) / 16.0

    rows = [
        sum(
            (-1.0 if bin(subset).count("1") & 1 else 1.0)
            * c_value(left, subset)
            for subset in range(16)
        )
        for left in range(16)
    ]
    raw_norm = sum(
        (-1.0 if bin(subset).count("1") & 1 else 1.0) * rows[subset]
        for subset in range(16)
    )

    print("moments", *(gamma[subset][0][0] for subset in range(16)))
    for subset in range(1, 15):
        print("b", subset, *gamma[subset][0][1:])
    print("h", *h_vector)
    for row in d_matrix:
        print("D", *row)
    print("lorentz_rows", *rows)
    print("raw_norm", raw_norm)


if __name__ == "__main__":
    main()
