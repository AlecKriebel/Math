#!/usr/bin/env python3
"""Independent checks for the restored private-MUB and binary benchmark.

The proofs are analytic.  This dependency-free verifier checks four places
where a normalization or convention error would be particularly easy:

* the noncommutative two-square identity for the binary Bell operator;
* the exact Q(sqrt(3)) attaining strategy and target Fourier coefficients;
* the 1/d and 1/d^2 normalizations in the private-MUB construction; and
* three hostile controls obtained by deleting one composition hypothesis.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import cmath
import math


@dataclass(frozen=True)
class Q3:
    """The exact number a+b*sqrt(3), with rational a,b."""

    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __add__(self, other: object) -> "Q3":
        value = coerce(other)
        return Q3(self.a + value.a, self.b + value.b)

    __radd__ = __add__

    def __neg__(self) -> "Q3":
        return Q3(-self.a, -self.b)

    def __sub__(self, other: object) -> "Q3":
        return self + (-coerce(other))

    def __rsub__(self, other: object) -> "Q3":
        return coerce(other) - self

    def __mul__(self, other: object) -> "Q3":
        value = coerce(other)
        return Q3(
            self.a * value.a + 3 * self.b * value.b,
            self.a * value.b + self.b * value.a,
        )

    __rmul__ = __mul__

    def __truediv__(self, denominator: int) -> "Q3":
        return Q3(self.a / denominator, self.b / denominator)


def coerce(value: object) -> Q3:
    if isinstance(value, Q3):
        return value
    if isinstance(value, (int, Fraction)):
        return Q3(Fraction(value), Fraction(0))
    raise TypeError(f"cannot coerce {value!r} to Q3")


ZERO = Q3()
ONE = Q3(Fraction(1))
SQRT3 = Q3(Fraction(0), Fraction(1))


def add_word(target: dict[str, Q3], word: str, coefficient: Q3) -> None:
    target[word] = target.get(word, ZERO) + coefficient


def reduced_word(left: str, right: str) -> str:
    if left == right:
        return "I"
    # Only cross-party commutation is used.
    if left.startswith("B") and right.startswith("A"):
        return right + left
    return left + right


def square(terms: list[tuple[str, Q3]], prefactor: Q3) -> dict[str, Q3]:
    result: dict[str, Q3] = {}
    for left_word, left_coefficient in terms:
        for right_word, right_coefficient in terms:
            add_word(
                result,
                reduced_word(left_word, right_word),
                prefactor * left_coefficient * right_coefficient,
            )
    return result


def check_binary_sos() -> None:
    first = square(
        [("A0", SQRT3), ("B0", -ONE), ("B1", 2 * ONE)],
        SQRT3 / 6,  # 1/(2 sqrt(3))
    )
    second = square(
        [("A1", SQRT3), ("B0", -ONE), ("B1", -ONE)],
        SQRT3 / 3,  # 1/sqrt(3)
    )
    total = dict(first)
    for word, coefficient in second.items():
        add_word(total, word, coefficient)
    expected = {
        "I": 3 * SQRT3,
        "A0B0": -ONE,
        "A0B1": 2 * ONE,
        "A1B0": -2 * ONE,
        "A1B1": -2 * ONE,
        "B0B1": ZERO,
        "B1B0": ZERO,
    }
    assert total == expected, (total, expected)


MatrixQ3 = tuple[tuple[Q3, ...], ...]


def qmatrix(*rows: tuple[object, ...]) -> MatrixQ3:
    return tuple(tuple(coerce(value) for value in row) for row in rows)


def madd(*matrices: MatrixQ3) -> MatrixQ3:
    return tuple(
        tuple(sum((matrix[j][k] for matrix in matrices), ZERO) for k in range(len(matrices[0][0])))
        for j in range(len(matrices[0]))
    )


def mscale(value: object, matrix: MatrixQ3) -> MatrixQ3:
    scalar = coerce(value)
    return tuple(tuple(scalar * entry for entry in row) for row in matrix)


def mmul(left: MatrixQ3, right: MatrixQ3) -> MatrixQ3:
    return tuple(
        tuple(
            sum((left[j][r] * right[r][k] for r in range(len(right))), ZERO)
            for k in range(len(right[0]))
        )
        for j in range(len(left))
    )


def transpose(matrix: MatrixQ3) -> MatrixQ3:
    return tuple(tuple(matrix[k][j] for k in range(len(matrix))) for j in range(len(matrix[0])))


def trace(matrix: MatrixQ3) -> Q3:
    return sum((matrix[j][j] for j in range(len(matrix))), ZERO)


def phi_expect(left: MatrixQ3, right: MatrixQ3) -> Q3:
    """<Phi_2|left tensor right|Phi_2> = Tr(left^T right)/2."""

    return trace(mmul(transpose(left), right)) / 2


def check_binary_strategy() -> None:
    identity = qmatrix((1, 0), (0, 1))
    x = qmatrix((0, 1), (1, 0))
    z = qmatrix((1, 0), (0, -1))
    a0 = z
    a1 = madd(mscale(Fraction(-1, 2), z), mscale(SQRT3 / 2, x))
    b0 = x
    b1 = madd(mscale(-SQRT3 / 2, z), mscale(Fraction(1, 2), x))

    for observable in (a0, a1, b0, b1):
        assert mmul(observable, observable) == identity

    score = (
        phi_expect(a0, b0)
        - 2 * phi_expect(a0, b1)
        + 2 * phi_expect(a1, b0)
        + 2 * phi_expect(a1, b1)
    )
    assert score == 3 * SQRT3

    # (C_A tensor I + I tensor D_B)|Phi> = 0 iff C_A^T + D_B = 0.
    first_factor = madd(
        mscale(SQRT3, transpose(a0)), mscale(-1, b0), mscale(2, b1)
    )
    second_factor = madd(
        mscale(SQRT3, transpose(a1)), mscale(-1, b0), mscale(-1, b1)
    )
    zero_matrix = qmatrix((0, 0), (0, 0))
    assert first_factor == zero_matrix
    assert second_factor == zero_matrix

    projectors_a = [madd(identity, mscale((-1) ** a, a0)) for a in range(2)]
    projectors_b = [madd(identity, mscale((-1) ** b, b0)) for b in range(2)]
    projectors_a = [mscale(Fraction(1, 2), p) for p in projectors_a]
    projectors_b = [mscale(Fraction(1, 2), p) for p in projectors_b]
    probabilities = [
        phi_expect(projectors_a[a], projectors_b[b])
        for a in range(2)
        for b in range(2)
    ]
    assert probabilities == [Q3(Fraction(1, 4))] * 4

    moments = {
        (1, 0): phi_expect(a0, identity),
        (0, 1): phi_expect(identity, b0),
        (1, 1): phi_expect(a0, b0),
    }
    assert all(value == ZERO for value in moments.values())

    # Binary operator-valued Fourier inversion, tested on a non-scalar rho_E.
    rho = qmatrix((Fraction(2, 3), Fraction(1, 6)), (Fraction(1, 6), Fraction(1, 3)))
    sigma = {(a, b): mscale(Fraction(1, 4), rho) for a in range(2) for b in range(2)}
    hats: dict[tuple[int, int], MatrixQ3] = {}
    for k in range(2):
        for ell in range(2):
            hats[k, ell] = tuple(
                tuple(
                    sum(
                        (
                            ((-1) ** (k * a + ell * b)) * sigma[a, b][j][r]
                            for a in range(2)
                            for b in range(2)
                        ),
                        ZERO,
                    )
                    for r in range(2)
                )
                for j in range(2)
            )
    assert hats[0, 0] == rho
    assert hats[1, 0] == hats[0, 1] == hats[1, 1] == zero_matrix
    for a in range(2):
        for b in range(2):
            reconstructed = tuple(
                tuple(
                    sum(
                        (
                            ((-1) ** (k * a + ell * b)) * hats[k, ell][j][r]
                            for k in range(2)
                            for ell in range(2)
                        ),
                        ZERO,
                    )
                    / 4
                    for r in range(2)
                )
                for j in range(2)
            )
            assert reconstructed == sigma[a, b]


MatrixC = list[list[complex]]


def cidentity(d: int) -> MatrixC:
    return [[complex(j == k) for k in range(d)] for j in range(d)]


def cprojector(vector: list[complex]) -> MatrixC:
    return [[vector[j] * vector[k].conjugate() for k in range(len(vector))] for j in range(len(vector))]


def cmul(left: MatrixC, right: MatrixC) -> MatrixC:
    return [
        [sum(left[j][r] * right[r][k] for r in range(len(right))) for k in range(len(right[0]))]
        for j in range(len(left))
    ]


def cscale(value: complex, matrix: MatrixC) -> MatrixC:
    return [[value * entry for entry in row] for row in matrix]


def cadd(*matrices: MatrixC) -> MatrixC:
    return [
        [sum(matrix[j][k] for matrix in matrices) for k in range(len(matrices[0][0]))]
        for j in range(len(matrices[0]))
    ]


def cerror(left: MatrixC, right: MatrixC) -> float:
    return max(abs(left[j][k] - right[j][k]) for j in range(len(left)) for k in range(len(left[0])))


def ctrace(matrix: MatrixC) -> complex:
    return sum(matrix[j][j] for j in range(len(matrix)))


def phi_probability(left: MatrixC, right: MatrixC) -> float:
    # For |Phi_d>, <left tensor right> = Tr(left^T right)/d.
    d = len(left)
    left_transpose = [[left[k][j] for k in range(d)] for j in range(d)]
    return (ctrace(cmul(left_transpose, right)) / d).real


def check_private_mub_dimensions() -> int:
    checks = 0
    tolerance = 2e-11
    for d in range(2, 13):
        omega = cmath.exp(2j * math.pi / d)
        computational = [
            cprojector([complex(j == b) for j in range(d)]) for b in range(d)
        ]
        fourier = [
            cprojector([omega ** (a * j) / math.sqrt(d) for j in range(d)])
            for a in range(d)
        ]
        permutation = list(reversed(range(d)))
        q_labeled: list[MatrixC | None] = [None] * d
        for b, label in enumerate(permutation):
            q_labeled[label] = computational[b]
        assert all(projector is not None for projector in q_labeled)
        q = [projector for projector in q_labeled if projector is not None]

        # State-supported MUB sandwich; here it holds as a global identity.
        for a in range(d):
            for b in range(d):
                sandwich = cmul(computational[b], cmul(fourier[a], computational[b]))
                assert cerror(sandwich, cscale(1 / d, computational[b])) < tolerance
                checks += 1

        table = [[0.0 for _ in range(d)] for _ in range(d)]
        for a in range(d):
            for label in range(d):
                table[a][label] = phi_probability(fourier[a], q[label])
                assert abs(table[a][label] - 1 / d**2) < tolerance
                checks += 1
        for k in range(d):
            for ell in range(d):
                coefficient = sum(
                    omega ** (k * a + ell * label) * table[a][label]
                    for a in range(d)
                    for label in range(d)
                )
                expected = 1.0 if (k, ell) == (0, 0) else 0.0
                assert abs(coefficient - expected) < tolerance
                checks += 1

        # Hostile control 1: drop private-reference condition (i).  A GHZ
        # flag held by Eve keeps the observed target table uniform but gives
        # Eve the computational/Q outcome exactly.
        rho_e = cscale(1 / d, cidentity(d))
        max_flagged_gap = 0.0
        for b in range(d):
            flagged_sigma = cscale(1 / d**2, computational[b])
            ideal_sigma = cscale(1 / d**2, rho_e)
            max_flagged_gap = max(max_flagged_gap, cerror(flagged_sigma, ideal_sigma))
        assert max_flagged_gap > 1e-4

        # Hostile control 2: drop matching condition (ii).  Taking Bob's
        # target basis conjugate to R makes the target perfectly correlated.
        conjugate_fourier = [
            [[entry.conjugate() for entry in row] for row in projector]
            for projector in fourier
        ]
        correlated = [
            phi_probability(fourier[a], conjugate_fourier[b])
            for a in range(d)
            for b in range(d)
        ]
        assert max(correlated) > 1 / d**2 + 1e-4

        # Hostile control 3: drop the MUB sandwich (iii), taking R=P.
        diagonal = [
            phi_probability(computational[a], computational[b])
            for a in range(d)
            for b in range(d)
        ]
        assert max(diagonal) > 1 / d**2 + 1e-4
        checks += 3
    return checks


def main() -> None:
    check_binary_sos()
    check_binary_strategy()
    checks = check_private_mub_dimensions()
    print("PASS: binary SOS coefficients cancel exactly over Q(sqrt(3)).")
    print("PASS: exact binary strategy attains 3*sqrt(3) and has flat target Fourier data.")
    print(f"PASS: private-MUB normalization checked in d=2,...,12 ({checks} checks).")
    print("PASS: deleting each composition hypothesis triggered a hostile control.")


if __name__ == "__main__":
    main()
