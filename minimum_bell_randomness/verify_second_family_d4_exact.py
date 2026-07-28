#!/usr/bin/env python3
"""Independent exact verifier for the d=4 second-family counterexample.

The calculation is performed in

    Q(zeta_16) = Q[x] / (x^8 + 1),  x = exp(pi i / 8),

using only ``fractions.Fraction`` arithmetic.  In particular, no numerical
tolerance is used anywhere in this file.

The verifier reconstructs the coefficients printed in Eq. (45) of the
originating paper, forms the Fourier-compressed Bob operators C_l, and checks

    C_l = 4 lambda_l D_l.

It then verifies all order-four constraints, the complete SOS identity and its
annihilation on |Phi_4>, the Bell values 4 and 5, and the nonuniform target
probability table (1/32 versus 3/32).
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Sequence


@dataclass(frozen=True)
class K:
    """An element of Q[x]/(x^8+1), represented in the power basis."""

    coeffs: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        if len(self.coeffs) != 8:
            raise ValueError("K requires exactly eight coefficients")

    @classmethod
    def rational(cls, value: int | Fraction) -> "K":
        value = Fraction(value)
        return cls((value,) + (Fraction(0),) * 7)

    def __add__(self, other: object) -> "K":
        if not isinstance(other, K):
            other = K.rational(other)  # type: ignore[arg-type]
        return K(tuple(a + b for a, b in zip(self.coeffs, other.coeffs)))

    def __radd__(self, other: object) -> "K":
        return self + other

    def __neg__(self) -> "K":
        return K(tuple(-a for a in self.coeffs))

    def __sub__(self, other: object) -> "K":
        return self + (-K._coerce(other))

    def __rsub__(self, other: object) -> "K":
        return K._coerce(other) - self

    def __mul__(self, other: object) -> "K":
        if not isinstance(other, K):
            return self.scale(other)  # type: ignore[arg-type]
        raw = [Fraction(0)] * 15
        for i, a in enumerate(self.coeffs):
            for j, b in enumerate(other.coeffs):
                raw[i + j] += a * b
        # x^8=-1, and degrees never exceed 14 in one multiplication.
        for degree in range(14, 7, -1):
            raw[degree - 8] -= raw[degree]
        return K(tuple(raw[:8]))

    def __rmul__(self, other: object) -> "K":
        return self * other

    def __truediv__(self, other: object) -> "K":
        if isinstance(other, K):
            return self * other.inverse()
        return self.scale(Fraction(1, 1) / Fraction(other))  # type: ignore[arg-type]

    def __pow__(self, exponent: int) -> "K":
        if exponent < 0:
            return (self.inverse()) ** (-exponent)
        result = ONE
        base = self
        power = exponent
        while power:
            if power & 1:
                result = result * base
            base = base * base
            power >>= 1
        return result

    def scale(self, value: int | Fraction) -> "K":
        value = Fraction(value)
        return K(tuple(value * a for a in self.coeffs))

    def conjugate(self) -> "K":
        # conj(x^j)=x^{-j}; x^{-j}=-x^(8-j) for 1<=j<=7.
        result = [Fraction(0)] * 8
        result[0] = self.coeffs[0]
        for j in range(1, 8):
            result[8 - j] -= self.coeffs[j]
        return K(tuple(result))

    def inverse(self) -> "K":
        """Invert a nonzero field element by exact Gaussian elimination."""

        if self == ZERO:
            raise ZeroDivisionError("division by zero in Q(zeta_16)")

        columns = []
        for j in range(8):
            columns.append((self * basis(j)).coeffs)
        aug = [
            [columns[col][row] for col in range(8)]
            + [Fraction(1 if row == 0 else 0)]
            for row in range(8)
        ]

        for col in range(8):
            pivot = next((row for row in range(col, 8) if aug[row][col]), None)
            if pivot is None:
                raise ZeroDivisionError("singular multiplication map")
            aug[col], aug[pivot] = aug[pivot], aug[col]
            pivot_value = aug[col][col]
            aug[col] = [entry / pivot_value for entry in aug[col]]
            for row in range(8):
                if row == col:
                    continue
                factor = aug[row][col]
                if factor:
                    aug[row] = [
                        entry - factor * pivot_entry
                        for entry, pivot_entry in zip(aug[row], aug[col])
                    ]
        return K(tuple(aug[row][8] for row in range(8)))

    def norm_squared(self) -> "K":
        return self.conjugate() * self

    def as_fraction(self) -> Fraction:
        if any(self.coeffs[1:]):
            raise AssertionError(f"expected a rational field element, got {self}")
        return self.coeffs[0]

    @staticmethod
    def _coerce(value: object) -> "K":
        return value if isinstance(value, K) else K.rational(value)  # type: ignore[arg-type]


ZERO = K.rational(0)
ONE = K.rational(1)


def basis(degree: int) -> K:
    coeffs = [Fraction(0)] * 8
    coeffs[degree] = Fraction(1)
    return K(tuple(coeffs))


def root(exponent: int) -> K:
    """Return zeta_16**exponent exactly."""

    exponent %= 16
    sign = 1
    if exponent >= 8:
        exponent -= 8
        sign = -1
    return basis(exponent).scale(sign)


ZETA = root(1)
I = root(4)
OMEGA = I
ETA = root(2)


def omega_power(exponent: int) -> K:
    return root(4 * exponent)


Matrix = list[list[K]]
Vector = list[K]


def zero_matrix(rows: int, cols: int) -> Matrix:
    return [[ZERO for _ in range(cols)] for _ in range(rows)]


def identity(size: int) -> Matrix:
    result = zero_matrix(size, size)
    for j in range(size):
        result[j][j] = ONE
    return result


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    return [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def matrix_sub(left: Matrix, right: Matrix) -> Matrix:
    return [
        [left[i][j] - right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def matrix_scale(scalar: K | int | Fraction, matrix: Matrix) -> Matrix:
    scalar = K._coerce(scalar)
    return [[scalar * entry for entry in row] for row in matrix]


def matrix_multiply(left: Matrix, right: Matrix) -> Matrix:
    rows = len(left)
    middle = len(right)
    cols = len(right[0])
    if len(left[0]) != middle:
        raise ValueError("incompatible matrix dimensions")
    result = zero_matrix(rows, cols)
    for i in range(rows):
        for k in range(middle):
            if left[i][k] == ZERO:
                continue
            for j in range(cols):
                result[i][j] = result[i][j] + left[i][k] * right[k][j]
    return result


def transpose(matrix: Matrix) -> Matrix:
    return [list(row) for row in zip(*matrix)]


def entrywise_conjugate(matrix: Matrix) -> Matrix:
    return [[entry.conjugate() for entry in row] for row in matrix]


def dagger(matrix: Matrix) -> Matrix:
    return transpose(entrywise_conjugate(matrix))


def matrix_power(matrix: Matrix, exponent: int) -> Matrix:
    result = identity(len(matrix))
    base = matrix
    power = exponent
    while power:
        if power & 1:
            result = matrix_multiply(result, base)
        base = matrix_multiply(base, base)
        power >>= 1
    return result


def kronecker(left: Matrix, right: Matrix) -> Matrix:
    lr, lc = len(left), len(left[0])
    rr, rc = len(right), len(right[0])
    result = zero_matrix(lr * rr, lc * rc)
    for i in range(lr):
        for j in range(lc):
            for k in range(rr):
                for ell in range(rc):
                    result[i * rr + k][j * rc + ell] = left[i][j] * right[k][ell]
    return result


def matrix_vector(matrix: Matrix, vector: Vector) -> Vector:
    return [
        sum((matrix[i][j] * vector[j] for j in range(len(vector))), ZERO)
        for i in range(len(matrix))
    ]


def inner(left: Vector, right: Vector) -> K:
    return sum(
        (a.conjugate() * b for a, b in zip(left, right)),
        ZERO,
    )


def trace(matrix: Matrix) -> K:
    return sum((matrix[j][j] for j in range(len(matrix))), ZERO)


def assert_matrix_equal(left: Matrix, right: Matrix, label: str) -> None:
    if left != right:
        for i, (left_row, right_row) in enumerate(zip(left, right)):
            for j, (a, b) in enumerate(zip(left_row, right_row)):
                if a != b:
                    raise AssertionError(f"{label}: first mismatch at ({i},{j}): {a} != {b}")
        raise AssertionError(f"{label}: incompatible matrix shapes")


def assert_vector_zero(vector: Vector, label: str) -> None:
    for j, value in enumerate(vector):
        if value != ZERO:
            raise AssertionError(f"{label}: component {j} is {value}, not zero")


def weighted_shift(weights: Sequence[K]) -> Matrix:
    """X diag(weights), where X|j>=|j+1 mod 4>."""

    if len(weights) != 4:
        raise ValueError("this verifier only handles d=4")
    result = zero_matrix(4, 4)
    for j, weight in enumerate(weights):
        result[(j + 1) % 4][j] = weight
    return result


def sine_half_grid(k: int) -> K:
    """sin(pi(k+1/2)/4), expressed in Q(zeta_16)."""

    exponent = 2 * k + 1
    return (root(exponent) - root(-exponent)) / I.scale(2)


def published_lambda(y: int, k: int) -> K:
    """The d=4 specialization of the published coefficient lambda_{y,k}."""

    numerator = omega_power(k * (k + 1) // 2).scale((-1) ** k)
    numerator = numerator * omega_power(-y * (1 + k))
    return numerator / sine_half_grid(k).scale(4)


def spectral_projector(observable: Matrix, outcome: int) -> Matrix:
    """Projector for the eigenvalue omega**outcome of an order-four unitary."""

    result = zero_matrix(4, 4)
    for power in range(4):
        coefficient = omega_power(-outcome * power)
        result = matrix_add(
            result,
            matrix_scale(coefficient, matrix_power(observable, power)),
        )
    return matrix_scale(Fraction(1, 4), result)


def main() -> None:
    d = 4
    identity4 = identity(4)
    identity16 = identity(16)
    x_shift = weighted_shift([ONE] * 4)

    # 1. Reconstruct all published coefficients and their Fourier selection.
    lambda_yk = [[published_lambda(y, k) for k in range(d)] for y in range(d)]
    lambdas = [published_lambda(0, (ell - 1) % d) for ell in range(d)]

    sin_pi_8 = sine_half_grid(0)
    sin_3pi_8 = sine_half_grid(1)
    assert lambdas[0] == ONE / sin_pi_8.scale(4)
    assert lambdas[1] == ONE / sin_pi_8.scale(4)
    assert lambdas[2] == (-I) / sin_3pi_8.scale(4)
    assert lambdas[3] == (-I) / sin_3pi_8.scale(4)
    assert sum((lam.norm_squared() for lam in lambdas), ZERO) == ONE

    # Eq. (16): Fourier summation over y selects k=ell-1 modulo four.
    for ell in range(d):
        for k in range(d):
            transformed = sum(
                (omega_power(ell * y) * lambda_yk[y][k] for y in range(d)),
                ZERO,
            )
            expected = (
                lambda_yk[0][k].scale(4)
                if k == (ell - 1) % d
                else ZERO
            )
            assert transformed == expected

    # 2. Construct the noncanonical kappa=(0,1,3,2) strategy exactly.
    kappa = (0, 1, 3, 2)
    equality_root_exponents = (2, 6, 10, 14)
    s0_exponents = (1, 3, 13, 15)

    polar_units: list[Matrix] = []
    bob: list[Matrix] = []
    for y in range(d):
        phase_weights = [
            root(s0_exponents[(kappa[j] + y) % d])
            for j in range(d)
        ]
        polar = weighted_shift(phase_weights)
        polar_units.append(polar)
        bob.append(entrywise_conjugate(polar))

    # The Fourier-compressed Bob operators C_ell.
    compressed: list[Matrix] = []
    for ell in range(d):
        c_ell = zero_matrix(4, 4)
        for y in range(d):
            c_ell = matrix_add(
                c_ell,
                matrix_scale(omega_power(ell * y), bob[y]),
            )
        compressed.append(c_ell)

    # Derive the scalar Fourier coefficients T_ell independently and verify
    # T_ell=4 lambda_ell q_ell, q_ell=eta^{-ell^2}.
    t_scalars: list[K] = []
    d_operators: list[Matrix] = []
    for ell in range(d):
        t_ell = sum(
            (
                omega_power(ell * r) * root(-s0_exponents[r])
                for r in range(d)
            ),
            ZERO,
        )
        t_scalars.append(t_ell)
        q_ell = root(-2 * ell * ell)
        assert t_ell == lambdas[ell].scale(4) * q_ell

        fourier_shift = weighted_shift(
            [omega_power(-ell * kappa[j]) for j in range(d)]
        )
        d_formula = matrix_scale(q_ell, fourier_shift)
        d_from_c = matrix_scale((lambdas[ell].scale(4)).inverse(), compressed[ell])
        assert_matrix_equal(d_from_c, d_formula, f"D_{ell} closed form")
        assert_matrix_equal(
            compressed[ell],
            matrix_scale(lambdas[ell].scale(4), d_formula),
            f"C_{ell}=4 lambda_{ell} D_{ell}",
        )
        d_operators.append(d_formula)

    alice = [entrywise_conjugate(operator) for operator in d_operators]
    bob_extra = x_shift

    # Sanity checks against the advertised A_0 and A_1 formulas.
    assert_matrix_equal(alice[0], x_shift, "A_0=X")
    advertised_a1 = weighted_shift(
        [root(equality_root_exponents[kappa[j]]) for j in range(d)]
    )
    assert_matrix_equal(alice[1], advertised_a1, "A_1=X diag(z_kappa)")
    assert_matrix_equal(bob_extra, entrywise_conjugate(alice[0]), "B_4=bar(A_0)")

    # 3. Check unitarity and every order-four relation.
    named_operators: list[tuple[str, Matrix]] = []
    named_operators.extend((f"A_{ell}", alice[ell]) for ell in range(d))
    named_operators.extend((f"D_{ell}", d_operators[ell]) for ell in range(d))
    named_operators.extend((f"B_{y}", bob[y]) for y in range(d))
    named_operators.append(("B_4", bob_extra))
    for name, operator in named_operators:
        assert_matrix_equal(
            matrix_multiply(dagger(operator), operator),
            identity4,
            f"{name} unitarity",
        )
        assert_matrix_equal(matrix_power(operator, 4), identity4, f"{name}^4=I")

    # 4. Verify the complete SOS certificate, including annihilation of Phi_4.
    phi = [ZERO] * 16
    for j in range(d):
        phi[d * j + j] = K.rational(Fraction(1, 2))
    assert inner(phi, phi) == ONE

    bell_operator = zero_matrix(16, 16)
    sos_rhs = zero_matrix(16, 16)
    for ell in range(d):
        tensor_term = kronecker(alice[ell], compressed[ell])
        weighted_term = matrix_scale(lambdas[ell].conjugate(), tensor_term)
        bell_operator = matrix_add(
            bell_operator,
            matrix_scale(Fraction(1, 2), matrix_add(weighted_term, dagger(weighted_term))),
        )

        p_ell = matrix_sub(
            matrix_scale(lambdas[ell].scale(4), identity16),
            tensor_term,
        )
        assert_vector_zero(
            matrix_vector(p_ell, phi),
            f"P_{ell}|Phi_4>",
        )
        sos_rhs = matrix_add(sos_rhs, matrix_multiply(dagger(p_ell), p_ell))

    sos_rhs = matrix_scale(Fraction(1, 8), sos_rhs)
    sos_lhs = matrix_sub(matrix_scale(4, identity16), bell_operator)
    assert_matrix_equal(sos_lhs, sos_rhs, "4I-F_4 exact SOS identity")

    bell_value = inner(phi, matrix_vector(bell_operator, phi))
    assert bell_value == K.rational(4)
    perfect_term = kronecker(alice[0], bob_extra)
    perfect_value = inner(phi, matrix_vector(perfect_term, phi))
    assert perfect_value == ONE
    augmented_value = bell_value + (
        perfect_value + perfect_value.conjugate()
    ).scale(Fraction(1, 2))
    assert augmented_value == K.rational(5)

    # 5. Check the target behavior for settings (A_1,B_4) exactly.
    alice_projectors = [spectral_projector(alice[1], a) for a in range(d)]
    bob_projectors = [spectral_projector(bob_extra, b) for b in range(d)]
    probabilities: list[list[Fraction]] = []
    for a in range(d):
        row: list[Fraction] = []
        for b in range(d):
            probability = (
                trace(
                    matrix_multiply(
                        alice_projectors[a],
                        transpose(bob_projectors[b]),
                    )
                )
                .scale(Fraction(1, 4))
                .as_fraction()
            )
            expected = Fraction(1, 32) if (a + b) % 2 == 0 else Fraction(3, 32)
            assert probability == expected
            row.append(probability)
        probabilities.append(row)

    for a in range(d):
        assert sum(probabilities[a]) == Fraction(1, 4)
    for b in range(d):
        assert sum(probabilities[a][b] for a in range(d)) == Fraction(1, 4)
    assert sum(sum(row) for row in probabilities) == Fraction(1)
    guessing_probability = max(max(row) for row in probabilities)
    assert guessing_probability == Fraction(3, 32)
    assert guessing_probability > Fraction(1, 16)

    # Independent Fourier check of the same table:
    # q=(1,zeta^2,-1,zeta^6), |qhat|^2=(2,6,2,6).
    q_exponents = (0, 2, 8, 6)
    q = [root(exponent) for exponent in q_exponents]
    qhat_norms: list[Fraction] = []
    for m in range(d):
        qhat = sum(
            (q[j] * omega_power(m * j) for j in range(d)),
            ZERO,
        )
        qhat_norms.append(qhat.norm_squared().as_fraction())
    assert qhat_norms == [Fraction(2), Fraction(6), Fraction(2), Fraction(6)]
    for a in range(d):
        for b in range(d):
            assert probabilities[a][b] == qhat_norms[-(a + b) % d] / 64

    print("PASS: exact d=4 second-family certificate verified in Q(zeta_16).")
    print("  Published lambda coefficients and Fourier selection: exact")
    print("  C_l = 4 lambda_l D_l for l=0,1,2,3: exact")
    print("  All unitarity and order-four relations: exact")
    print("  SOS annihilation and operator identity; <F_4>=4: exact")
    print("  Augmented value: 5")
    print("  Target probabilities: 1/32 (even), 3/32 (odd)")
    print("  Guessing probability: 3/32 > 1/16")


if __name__ == "__main__":
    main()
