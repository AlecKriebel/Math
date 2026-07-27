#!/usr/bin/env python3
"""Independent exact verifier for the sparse d=4 counterexample certificate.

All arithmetic is performed in Q(zeta_16)=Q[x]/(x^8+1), with
x=exp(pi*i/8).  The verifier reads certificate.json, reconstructs every
observable from sparse weighted-shift data, and evaluates both the original
Bell expression and the target probabilities without floating point.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterable

DEGREE = 8
DIMENSION = 4
CERTIFICATE = Path(__file__).with_name("certificate.json")


@dataclass(frozen=True)
class K:
    """An element of Q[x]/(x^8+1) in the power basis."""

    coefficients: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        if len(self.coefficients) != DEGREE:
            raise ValueError("field elements require eight coefficients")

    @staticmethod
    def rational(value: int | Fraction) -> "K":
        coefficients = [Fraction(0)] * DEGREE
        coefficients[0] = Fraction(value)
        return K(tuple(coefficients))

    def __add__(self, other: "K") -> "K":
        return K(tuple(a + b for a, b in zip(self.coefficients, other.coefficients)))

    def __sub__(self, other: "K") -> "K":
        return K(tuple(a - b for a, b in zip(self.coefficients, other.coefficients)))

    def __neg__(self) -> "K":
        return K(tuple(-a for a in self.coefficients))

    def __mul__(self, other: "K") -> "K":
        result = [Fraction(0)] * DEGREE
        for i, a in enumerate(self.coefficients):
            for j, b in enumerate(other.coefficients):
                if not a or not b:
                    continue
                exponent = i + j
                sign = 1
                if exponent >= DEGREE:
                    exponent -= DEGREE
                    sign = -1
                result[exponent] += sign * a * b
        return K(tuple(result))

    def __pow__(self, power: int) -> "K":
        if power < 0:
            raise ValueError("negative powers are unnecessary")
        result = ONE
        base = self
        while power:
            if power & 1:
                result = result * base
            base = base * base
            power >>= 1
        return result

    def scale(self, value: int | Fraction) -> "K":
        value = Fraction(value)
        return K(tuple(value * a for a in self.coefficients))

    def conjugate(self) -> "K":
        result = ZERO
        for exponent, coefficient in enumerate(self.coefficients):
            if coefficient:
                result = result + root(-exponent).scale(coefficient)
        return result

    def as_fraction(self) -> Fraction:
        if any(self.coefficients[1:]):
            raise ValueError(f"field element is not rational: {self}")
        return self.coefficients[0]


def root(exponent: int) -> K:
    """Return zeta_16^exponent."""
    exponent %= 16
    sign = 1
    if exponent >= 8:
        exponent -= 8
        sign = -1
    coefficients = [Fraction(0)] * DEGREE
    coefficients[exponent] = Fraction(sign)
    return K(tuple(coefficients))


ZERO = K.rational(0)
ONE = K.rational(1)
I = root(4)
HALF = Fraction(1, 2)
QUARTER = Fraction(1, 4)

Matrix = list[list[K]]


def zeros(rows: int, columns: int | None = None) -> Matrix:
    if columns is None:
        columns = rows
    return [[ZERO for _ in range(columns)] for _ in range(rows)]


def eye(n: int) -> Matrix:
    result = zeros(n)
    for j in range(n):
        result[j][j] = ONE
    return result


def add(A: Matrix, B: Matrix) -> Matrix:
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def scale(value: K, A: Matrix) -> Matrix:
    return [[value * entry for entry in row] for row in A]


def multiply(A: Matrix, B: Matrix) -> Matrix:
    result = zeros(len(A), len(B[0]))
    for i in range(len(A)):
        for k in range(len(B)):
            if A[i][k] == ZERO:
                continue
            for j in range(len(B[0])):
                result[i][j] = result[i][j] + A[i][k] * B[k][j]
    return result


def power(A: Matrix, exponent: int) -> Matrix:
    result = eye(len(A))
    base = A
    while exponent:
        if exponent & 1:
            result = multiply(result, base)
        base = multiply(base, base)
        exponent >>= 1
    return result


def dagger(A: Matrix) -> Matrix:
    return [[A[j][i].conjugate() for j in range(len(A))] for i in range(len(A[0]))]


def transpose(A: Matrix) -> Matrix:
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]


def entrywise_conjugate(A: Matrix) -> Matrix:
    return [[entry.conjugate() for entry in row] for row in A]


def trace(A: Matrix) -> K:
    return sum((A[j][j] for j in range(len(A))), ZERO)


def diagonal(entries: Iterable[K]) -> Matrix:
    entries = list(entries)
    result = zeros(len(entries))
    for j, entry in enumerate(entries):
        result[j][j] = entry
    return result


def weighted_shift(exponents: list[int]) -> Matrix:
    """Return X diag(zeta^exponents[j])."""
    result = zeros(len(exponents))
    for j, exponent in enumerate(exponents):
        result[(j + 1) % len(exponents)][j] = root(exponent)
    return result


def projector(observable: Matrix, outcome: int) -> Matrix:
    """Project onto eigenvalue i^outcome for a fourth-order observable."""
    result = zeros(DIMENSION)
    for r in range(DIMENSION):
        result = add(result, scale(root(-4 * outcome * r), power(observable, r)))
    return scale(ONE.scale(QUARTER), result)


def assert_matrix_equal(A: Matrix, B: Matrix, label: str) -> None:
    if A == B:
        return
    for i in range(len(A)):
        for j in range(len(A[0])):
            if A[i][j] != B[i][j]:
                raise AssertionError(f"{label}: mismatch at ({i},{j})")
    raise AssertionError(label)


def parse_fraction(text: str) -> Fraction:
    return Fraction(text)


def load_certificate() -> dict:
    certificate = json.loads(CERTIFICATE.read_text())
    if certificate["schema"] != "cyclic-bell-randomness-counterexample/v2":
        raise AssertionError("unexpected certificate schema")
    claim = certificate["claim"]
    expected_claim = {
        "dimension": DIMENSION,
        "augmented_bell_value": "2*csc(pi/8)+1",
        "target_settings": {"alice": 1, "bob": 4},
        "guessing_probability": "3/32",
        "uniform_benchmark": "1/16",
        "strict_gap": "1/32",
    }
    if claim != expected_claim:
        raise AssertionError("unexpected claim metadata")
    field = certificate["field"]
    expected_field = {
        "name": "Q(zeta_16)",
        "generator": "zeta",
        "interpretation": "zeta=exp(pi*i/8)",
        "minimal_polynomial": "zeta^8+1",
    }
    if field != expected_field:
        raise AssertionError("unexpected field encoding")
    if certificate["spaces"] != {"H_A": 4, "H_B": 4, "H_E": 1}:
        raise AssertionError("unexpected Hilbert-space metadata")
    if certificate["state"] != {
        "name": "Phi_4",
        "formula": "(1/2)*sum_{j=0}^3 |j,j>",
    }:
        raise AssertionError("unexpected state metadata")
    return certificate


def main() -> None:
    certificate = load_certificate()
    encoded = certificate["weighted_shift_encoding"]
    expected_order = [0, 1, 3, 2]
    expected_roots = [2, 6, 14, 10]
    if encoded["phase_order_kappa"] != expected_order:
        raise AssertionError("unexpected phase order")
    if encoded["equality_phase_exponents_in_kappa_order"] != expected_roots:
        raise AssertionError("incorrect equality phases")

    A0 = weighted_shift(encoded["A0_weight_exponents"])
    A1 = weighted_shift(encoded["A1_weight_exponents"])
    V = [weighted_shift(row) for row in encoded["V_y_weight_exponents"]]
    B = [weighted_shift(row) for row in encoded["B_y_weight_exponents"]]
    B4 = weighted_shift(encoded["B4_weight_exponents"])
    identity = eye(DIMENSION)

    # Certificate consistency and all admissibility relations.
    for y in range(DIMENSION):
        assert_matrix_equal(B[y], entrywise_conjugate(V[y]), f"B_{y}=conj(V_{y})")
    assert_matrix_equal(B4, entrywise_conjugate(A0), "B4=conj(A0)")
    for label, observable in [
        ("A0", A0),
        ("A1", A1),
        *[(f"V{y}", V[y]) for y in range(DIMENSION)],
        *[(f"B{y}", B[y]) for y in range(DIMENSION)],
        ("B4", B4),
    ]:
        assert_matrix_equal(multiply(dagger(observable), observable), identity, f"{label} unitary")
        assert_matrix_equal(power(observable, DIMENSION), identity, f"{label}^4=I")

    # Exact polar factorizations.  Each diagonal coefficient of H_y is one
    # of 2*cos(pi/8) or 2*cos(3*pi/8), both strictly positive.
    positive_lengths = {root(1) + root(15), root(3) + root(13)}
    H: list[Matrix] = []
    for y in range(DIMENSION):
        C = add(A0, scale(I**y, A1))
        H_y = multiply(dagger(V[y]), C)
        assert_matrix_equal(H_y, dagger(H_y), f"H_{y} Hermitian")
        for row in range(DIMENSION):
            for column in range(DIMENSION):
                if row != column and H_y[row][column] != ZERO:
                    raise AssertionError(f"H_{y} is not diagonal")
            if H_y[row][row] not in positive_lengths:
                raise AssertionError(f"H_{y} has an unexpected diagonal length")
        assert_matrix_equal(multiply(V[y], H_y), C, f"polar factorization y={y}")
        H.append(H_y)

    # Evaluate the original Bell expression directly on |Phi_4>.
    bell = ZERO
    for y in range(DIMENSION):
        C = add(A0, scale(I**y, A1))
        correlator = trace(multiply(C, transpose(B[y]))).scale(QUARTER)
        bell = bell + (correlator + correlator.conjugate()).scale(HALF)
    length_short = root(1) + root(15)
    length_long = root(3) + root(13)
    M4 = (length_short + length_long).scale(2)
    if bell != M4:
        raise AssertionError("unaugmented Bell value mismatch")
    added_correlator = trace(multiply(A0, transpose(B4))).scale(QUARTER)
    added = (added_correlator + added_correlator.conjugate()).scale(HALF)
    if added != ONE:
        raise AssertionError("augmented correlator mismatch")

    # Reconstruct the complete target table from spectral projectors.
    probabilities: list[list[Fraction]] = []
    for a in range(DIMENSION):
        alice = projector(A1, a)
        row: list[Fraction] = []
        for b in range(DIMENSION):
            bob = projector(B4, b)
            probability = trace(multiply(alice, transpose(bob))).scale(QUARTER)
            row.append(probability.as_fraction())
        probabilities.append(row)
    expected_table = [
        [parse_fraction(entry) for entry in row]
        for row in certificate["target_probability_table"]
    ]
    if probabilities != expected_table:
        raise AssertionError("target probability table mismatch")
    if sum(sum(row) for row in probabilities) != 1:
        raise AssertionError("target probabilities do not sum to one")
    for a in range(DIMENSION):
        if sum(probabilities[a]) != QUARTER:
            raise AssertionError("Alice marginal is not uniform")
    for b in range(DIMENSION):
        if sum(probabilities[a][b] for a in range(DIMENSION)) != QUARTER:
            raise AssertionError("Bob marginal is not uniform")

    # Independently derive the same table from the q-sequence and its DFT.
    fourier = certificate["fourier_certificate"]
    q_exponents = fourier["q_exponents"]
    derived_q_exponents = [0]
    for exponent in expected_roots[:-1]:
        derived_q_exponents.append((derived_q_exponents[-1] + exponent) % 16)
    if q_exponents != derived_q_exponents:
        raise AssertionError("q recurrence mismatch")
    q = [root(exponent) for exponent in q_exponents]
    qhat: list[K] = []
    squared_magnitudes: list[Fraction] = []
    for m in range(DIMENSION):
        value = sum((q[j] * I ** (m * j) for j in range(DIMENSION)), ZERO)
        qhat.append(value)
        squared_magnitudes.append((value * value.conjugate()).as_fraction())
    if squared_magnitudes != [Fraction(x) for x in fourier["qhat_squared_magnitudes"]]:
        raise AssertionError("Fourier squared magnitudes mismatch")
    fourier_table = [
        [
            squared_magnitudes[-(a + b) % DIMENSION] / DIMENSION**3
            for b in range(DIMENSION)
        ]
        for a in range(DIMENSION)
    ]
    if fourier_table != probabilities:
        raise AssertionError("projector and Fourier probability calculations disagree")

    guessing = max(max(row) for row in probabilities)
    if guessing != Fraction(3, 32) or guessing <= Fraction(1, 16):
        raise AssertionError("strict guessing-probability gap failed")

    # Exact d=4 comparison with the cyclic root ordering.  The two strategies
    # have identical first harmonics in every Bell term but different full
    # target tables.
    canonical_A1 = weighted_shift([2, 6, 10, 14])
    canonical_V = [
        weighted_shift(row)
        for row in [
            [1, 3, 13, 15],
            [3, 13, 15, 1],
            [13, 15, 1, 3],
            [15, 1, 3, 13],
        ]
    ]
    canonical_B = [entrywise_conjugate(observable) for observable in canonical_V]
    for y in range(DIMENSION):
        for label, canonical_alice, swapped_alice in [
            ("A0", A0, A0),
            ("A1", canonical_A1, A1),
        ]:
            canonical_correlator = trace(
                multiply(canonical_alice, transpose(canonical_B[y]))
            ).scale(QUARTER)
            swapped_correlator = trace(
                multiply(swapped_alice, transpose(B[y]))
            ).scale(QUARTER)
            if canonical_correlator != swapped_correlator:
                raise AssertionError(
                    f"{label},B{y}: Bell-visible first harmonic changed"
                )
    for label, canonical_alice, swapped_alice in [
        ("A0", A0, A0),
        ("A1", canonical_A1, A1),
    ]:
        canonical_correlator = trace(
            multiply(canonical_alice, transpose(B4))
        ).scale(QUARTER)
        swapped_correlator = trace(
            multiply(swapped_alice, transpose(B4))
        ).scale(QUARTER)
        if canonical_correlator != swapped_correlator:
            raise AssertionError(f"{label},B4: first harmonic changed")

    canonical_probabilities: list[list[Fraction]] = []
    for a in range(DIMENSION):
        alice = projector(canonical_A1, a)
        row = []
        for b in range(DIMENSION):
            bob = projector(B4, b)
            probability = trace(multiply(alice, transpose(bob))).scale(QUARTER)
            row.append(probability.as_fraction())
        canonical_probabilities.append(row)
    if any(
        probability != Fraction(1, 16)
        for row in canonical_probabilities
        for probability in row
    ):
        raise AssertionError("cyclic-order canonical target table is not uniform")
    if canonical_probabilities == probabilities:
        raise AssertionError("canonical and root-swapped target tables coincide")

    print("PASS: sparse exact Q(zeta_16) certificate verified")
    print("  A0,A1,B0,...,B4 are unitary and fourth order")
    print("  all C_y=V_y H_y use the two analytically positive exact lengths")
    print("  <I_4>=2*csc(pi/8) and <overline(I)_4>=2*csc(pi/8)+1")
    print("  projector and Fourier calculations give 1/32,3/32 alternating")
    print("  both local marginals are uniform, while G=3/32>1/16")
    print("  cyclic and root-swapped maximizers have identical first harmonics")
    print("  their exact target tables differ: 1/16 versus 1/32,3/32")


if __name__ == "__main__":
    main()
