#!/usr/bin/env python3
"""Dependency-free exact checker for the cycle-phase obstruction."""

from dataclasses import dataclass
from fractions import Fraction as F


@dataclass(frozen=True)
class Gaussian:
    real: F = F(0)
    imag: F = F(0)

    def __add__(self, other):
        other = gaussian(other)
        return Gaussian(self.real + other.real, self.imag + other.imag)

    __radd__ = __add__

    def __neg__(self):
        return Gaussian(-self.real, -self.imag)

    def __sub__(self, other):
        return self + (-gaussian(other))

    def __rsub__(self, other):
        return gaussian(other) - self

    def __mul__(self, other):
        other = gaussian(other)
        return Gaussian(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real,
        )

    __rmul__ = __mul__

    def __truediv__(self, value):
        return Gaussian(self.real / value, self.imag / value)

    def conjugate(self):
        return Gaussian(self.real, -self.imag)

    def norm_squared(self):
        return self.real * self.real + self.imag * self.imag


def gaussian(value):
    return value if isinstance(value, Gaussian) else Gaussian(F(value), F(0))


ZERO = Gaussian()
ONE = Gaussian(F(1))
I = Gaussian(F(0), F(1))


def pair_matrix(diagonal, off_diagonal):
    matrix = [[ZERO for _ in range(9)] for _ in range(9)]
    for i, value in enumerate(diagonal):
        matrix[i][i] = gaussian(value)
    for row, column, value in off_diagonal:
        matrix[row][column] = gaussian(value)
    return matrix


def pair_index(first, second):
    return 3 * first + second


def word_index(word):
    return 9 * word[0] + 3 * word[1] + word[2]


def partial_traces(matrix):
    first = [[ZERO for _ in range(3)] for _ in range(3)]
    second = [[ZERO for _ in range(3)] for _ in range(3)]
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for d in range(3):
                    value = matrix[pair_index(a, b)][pair_index(c, d)]
                    if a == c:
                        first[b][d] = first[b][d] + value
                    if b == d:
                        second[a][c] = second[a][c] + value
    return first, second


def hs_norm_squared(matrix):
    return sum(
        (entry.norm_squared() for row in matrix for entry in row),
        F(0),
    )


def apply_embedded(pair, spectator, vector):
    output = [ZERO for _ in range(27)]
    for out_word in (
        (a, b, c) for a in range(3) for b in range(3) for c in range(3)
    ):
        out_index = word_index(out_word)
        for in_word in (
            (a, b, c) for a in range(3) for b in range(3) for c in range(3)
        ):
            if out_word[spectator] != in_word[spectator]:
                continue
            active = [i for i in range(3) if i != spectator]
            row = pair_index(out_word[active[0]], out_word[active[1]])
            column = pair_index(in_word[active[0]], in_word[active[1]])
            output[out_index] = (
                output[out_index]
                + pair[row][column] * vector[word_index(in_word)]
            )
    return output


def inner(left, right):
    return sum(
        (x.conjugate() * y for x, y in zip(left, right)),
        ZERO,
    )


def main():
    b1 = pair_matrix(
        [57, -60, 3, -60, 57, 3, 3, 3, -6],
        [(0, 4, 360), (4, 0, 360)],
    )
    b2 = pair_matrix(
        [
            -183 * I,
            -9 + 186 * I,
            9 - 3 * I,
            -9 + 186 * I,
            -183 * I,
            9 - 3 * I,
            9 - 3 * I,
            9 - 3 * I,
            -18 + 6 * I,
        ],
        [(1, 3, 117 - 225 * I), (3, 1, 117 - 225 * I)],
    )
    b3 = pair_matrix(
        [
            -135 - 125 * I,
            126 + 127 * I,
            9 - 2 * I,
            126 + 127 * I,
            -135 - 125 * I,
            9 - 2 * I,
            9 - 2 * I,
            9 - 2 * I,
            -18 + 4 * I,
        ],
        [(0, 4, -243 - 81 * I), (4, 0, -243 - 81 * I)],
    )
    pairs = (b1, b2, b3)
    for pair in pairs:
        first, second = partial_traces(pair)
        assert first == [[ZERO for _ in range(3)] for _ in range(3)]
        assert second == [[ZERO for _ in range(3)] for _ in range(3)]

    norms = tuple(hs_norm_squared(pair) for pair in pairs)
    assert norms == (F(272970), F(265680), F(263610))

    # Work with the unnormalized numerators sqrt(5)u and sqrt(5)v.
    # Their output Gram is divided by 5 below.
    u = [ZERO for _ in range(27)]
    v = [ZERO for _ in range(27)]
    u[word_index((0, 0, 0))] = 1 + I
    u[word_index((1, 1, 0))] = I
    u[word_index((0, 1, 1))] = 1 - I
    v[word_index((1, 1, 1))] = 1 + I
    v[word_index((0, 0, 1))] = I
    v[word_index((1, 0, 0))] = 1 - I
    assert inner(u, u) == Gaussian(F(5))
    assert inner(v, v) == Gaussian(F(5))
    assert inner(u, v) == ZERO

    outputs = [
        (
            apply_embedded(pairs[i], i, u),
            apply_embedded(pairs[i], i, v),
        )
        for i in range(3)
    ]
    h = [[ZERO for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            h[i][j] = (
                inner(outputs[i][0], outputs[j][0])
                + inner(outputs[i][1], outputs[j][1])
            ) / 5

    expected = [
        [
            Gaussian(F(1069992, 5)),
            Gaussian(F(165996), F(-60408, 5)),
            Gaussian(F(126144), F(-106680)),
        ],
        [
            Gaussian(F(165996), F(60408, 5)),
            Gaussian(F(1071126, 5)),
            Gaussian(F(758094, 5), F(-71262, 5)),
        ],
        [
            Gaussian(F(126144), F(106680)),
            Gaussian(F(758094, 5), F(71262, 5)),
            Gaussian(F(213644)),
        ],
    ]
    assert h == expected

    denominator = 2 * sum(norms)
    assert denominator == F(1604520)

    trace_h = sum((h[i][i].real for i in range(3)), F(0))
    ordinary_cross = 2 * sum(
        (h[0][1].real, h[1][2].real, h[0][2].real),
        F(0),
    )
    physical_deficit = denominator - trace_h - ordinary_cross
    assert physical_deficit == F(375674, 5) > 0

    # Re(e^{i pi/4}(a+ib)) = (a-b)/sqrt(2)
    # = ((a-b)/2) sqrt(2).
    rational_excess = (
        trace_h
        + 2 * (h[0][1].real + h[1][2].real)
        - denominator
    )
    sqrt2_coefficient = h[0][2].real - h[0][2].imag
    assert rational_excess == F(-1637114, 5)
    assert sqrt2_coefficient == F(232824)

    # Exact positivity of rational_excess + sqrt2_coefficient*sqrt(2).
    left = 5 * sqrt2_coefficient
    right = F(1637114)
    square_gap = 2 * left * left - right * right
    assert square_gap == F(30208499804) > 0

    print("cycle phase-erasure obstruction: exact checks passed")


if __name__ == "__main__":
    main()
