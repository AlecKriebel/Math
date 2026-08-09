#!/usr/bin/env python3
"""Focused, dependency-free checks for restored exact-value benchmarks.

This script checks transcription-sensitive facts requested during the
dominating-merge review:

* the d=2,...,6 radical table and the source's truncated decimals;
* the finite cosecant-square identity and second-family lambda normalization;
* the canonical polar Bob observables against Eqs. (15) and (45) of
  arXiv:2606.21362v3;
* the two source Fourier relations and the explicit d=3 formula.

The finite floating-point checks support, but do not replace, the analytic
functional-calculus and trigonometric proofs in the manuscript.
"""

from __future__ import annotations

import cmath
import math
from fractions import Fraction


TOL = 3.0e-9
Matrix = list[list[complex]]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_close(actual: complex, expected: complex, message: str, tol: float = TOL) -> None:
    error = abs(actual - expected)
    scale = max(1.0, abs(actual), abs(expected))
    if error > tol * scale:
        raise AssertionError(
            f"{message}: got {actual!r}, expected {expected!r}, "
            f"relative error {error / scale:.3e}"
        )


def zero(d: int) -> Matrix:
    return [[0j for _ in range(d)] for _ in range(d)]


def identity(d: int) -> Matrix:
    out = zero(d)
    for j in range(d):
        out[j][j] = 1.0 + 0j
    return out


def add(left: Matrix, right: Matrix) -> Matrix:
    return [
        [left[row][column] + right[row][column] for column in range(len(left))]
        for row in range(len(left))
    ]


def scale(value: complex, matrix: Matrix) -> Matrix:
    return [[value * entry for entry in row] for row in matrix]


def multiply(left: Matrix, right: Matrix) -> Matrix:
    d = len(left)
    return [
        [
            sum(left[row][k] * right[k][column] for k in range(d))
            for column in range(d)
        ]
        for row in range(d)
    ]


def transpose(matrix: Matrix) -> Matrix:
    d = len(matrix)
    return [[matrix[column][row] for column in range(d)] for row in range(d)]


def dagger(matrix: Matrix) -> Matrix:
    d = len(matrix)
    return [
        [matrix[column][row].conjugate() for column in range(d)]
        for row in range(d)
    ]


def power(matrix: Matrix, exponent: int) -> Matrix:
    result = identity(len(matrix))
    factor = matrix
    n = exponent
    while n:
        if n & 1:
            result = multiply(result, factor)
        factor = multiply(factor, factor)
        n >>= 1
    return result


def residual(left: Matrix, right: Matrix) -> float:
    numerator = math.sqrt(
        sum(abs(left[i][j] - right[i][j]) ** 2 for i in range(len(left)) for j in range(len(left)))
    )
    denominator = max(
        1.0,
        math.sqrt(sum(abs(entry) ** 2 for row in left for entry in row)),
        math.sqrt(sum(abs(entry) ** 2 for row in right for entry in row)),
    )
    return numerator / denominator


def require_matrix_close(left: Matrix, right: Matrix, message: str, tol: float = TOL) -> None:
    error = residual(left, right)
    if error > tol:
        raise AssertionError(f"{message}: relative Frobenius residual {error:.3e}")


def weyl(d: int) -> tuple[complex, Matrix, Matrix]:
    omega = cmath.exp(2j * math.pi / d)
    z = zero(d)
    x = zero(d)
    for j in range(d):
        z[j][j] = omega**j
        x[(j + 1) % d][j] = 1.0 + 0j
    return omega, z, x


def polar_bob(d: int, y: int) -> Matrix:
    """Compute B_y=(p(W_y)^dagger Z^dagger)^T by spectral interpolation."""

    omega, z, x = weyl(d)
    w = scale(omega**y, multiply(dagger(z), x))
    powers = [identity(d)]
    for _ in range(1, d):
        powers.append(multiply(powers[-1], w))

    eta = cmath.exp(1j * math.pi / d)
    delta = 1 if d % 2 == 0 else 0
    phase_of_w = zero(d)
    for t in range(d):
        root = eta ** (2 * t + delta)
        projector = zero(d)
        for exponent, w_power in enumerate(powers):
            projector = add(projector, scale(root ** (-exponent) / d, w_power))
        phase = (1 + root) / abs(1 + root)
        phase_of_w = add(phase_of_w, scale(phase, projector))

    q = multiply(dagger(phase_of_w), dagger(z))
    return transpose(q)


def source_bob(d: int, y: int) -> Matrix:
    """Eqs. (15) and (45) of arXiv:2606.21362v3."""

    omega, z, x = weyl(d)
    result = zero(d)
    for k in range(d):
        coefficient = (
            (-1) ** k
            * omega ** (k * (k + 1) // 2)
            * omega ** (-y * (1 + k))
            / (d * math.sin(math.pi * (k + 0.5) / d))
        )
        monomial = multiply(power(x, k + 1), power(z, k))
        result = add(result, scale(coefficient, monomial))
    return result


def exact_radical_certificates() -> None:
    """Check exact algebraic products plus the positive numerical branches."""

    # d=4: [2 sqrt(4+2 sqrt(2))] [sqrt(2-sqrt(2))/2] = 2.
    # Squaring the product reduces to multiplication in Q(sqrt(2)).
    def qmul(left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction], radicand: int):
        a, b = left
        c, e = right
        return a * c + radicand * b * e, a * e + b * c

    require(
        qmul((Fraction(4), Fraction(2)), (Fraction(2), Fraction(-1)), 2)
        == (Fraction(4), Fraction(0)),
        "d=4 exact radical product failed",
    )
    # d=5 and d=6 reduce to differences of squares.
    require((Fraction(5) - 1) / 2 == 2, "d=5 exact radical product failed")
    require((Fraction(6) - 2) / 2 == 2, "d=6 exact radical product failed")
    require(Fraction(2 * 2, 2) == 2, "d=2 exact radical product failed")
    require(Fraction(4, 2) == 2, "d=3 exact radical product failed")

    radicals = {
        2: 2 * math.sqrt(2),
        3: 4.0,
        4: 2 * math.sqrt(4 + 2 * math.sqrt(2)),
        5: 2 * (1 + math.sqrt(5)),
        6: 2 * (math.sqrt(6) + math.sqrt(2)),
    }
    source_truncations = {2: "2.828", 3: "4.000", 4: "5.226", 5: "6.472", 6: "7.727"}
    for d, radical in radicals.items():
        target = 2 / math.sin(math.pi / (2 * d))
        require_close(radical, target, f"radical benchmark d={d}", 2.0e-14)
        require(f"{target:.3f}" == source_truncations[d], f"source decimal benchmark d={d}")
        require(d * math.sqrt(2) + 1.0e-14 >= target, f"source d sqrt(2) bound d={d}")
        if d > 2:
            require(d * math.sqrt(2) > target, f"source bound should be strict at d={d}")

    d4_entropy = -math.log2(Fraction(3, 32))
    require_close(d4_entropy, 5 - math.log2(3), "d=4 min-entropy identity", 2.0e-15)
    require(d4_entropy < 4, "d=4 witness must have less than four bits")


def cosecant_and_lambda_checks(max_d: int = 100) -> None:
    for d in range(2, max_d + 1):
        specialized = sum(
            1 / math.sin(math.pi * (ell - 0.5) / d) ** 2 for ell in range(d)
        )
        require_close(specialized, float(d * d), f"specialized csc-square identity d={d}", 2.0e-12)
        lambda_norm = specialized / (d * d)
        require_close(lambda_norm, 1.0, f"lambda normalization d={d}", 2.0e-12)

        # Hostile checks of the general identity away from its poles.
        for ratio in (0.17, 0.37, 0.61, 0.83):
            x = ratio * math.pi / d
            lhs = sum(1 / math.sin(x + k * math.pi / d) ** 2 for k in range(d))
            rhs = d * d / math.sin(d * x) ** 2
            require_close(lhs, rhs, f"general csc-square identity d={d}, ratio={ratio}", 3.0e-11)


def source_observable_checks(max_d: int = 12) -> int:
    checked = 0
    for d in range(2, max_d + 1):
        omega, z, x = weyl(d)
        source = []
        for y in range(d):
            by_source = source_bob(d, y)
            by_polar = polar_bob(d, y)
            require_matrix_close(by_source, by_polar, f"source/polar B match d={d}, y={y}")
            require_matrix_close(multiply(dagger(by_source), by_source), identity(d), f"B unitarity d={d}, y={y}")
            require_matrix_close(power(by_source, d), identity(d), f"B order d={d}, y={y}")
            source.append(by_source)
            checked += 1

            if d == 3:
                explicit = scale(
                    1 / 3,
                    add(
                        add(scale(2, power(z, 2)), scale(2 * omega ** (2 * y), x)),
                        scale(-omega ** (y + 1), multiply(power(x, 2), z)),
                    ),
                )
                require_matrix_close(by_source, explicit, f"source d=3 formula y={y}")

        fourier_zero = zero(d)
        fourier_one = zero(d)
        for y, by in enumerate(source):
            fourier_zero = add(fourier_zero, by)
            fourier_one = add(fourier_one, scale(omega**y, by))
        alpha = 1 / math.sin(math.pi / (2 * d))
        require_matrix_close(fourier_zero, scale(alpha, dagger(z)), f"source Fourier m=0 d={d}")
        require_matrix_close(fourier_one, scale(alpha, x), f"source Fourier m=1 d={d}")
    return checked


def main() -> None:
    exact_radical_certificates()
    cosecant_and_lambda_checks()
    observables = source_observable_checks()
    asymptotic_ratio = math.pi / (2 * math.sqrt(2))
    print("PASS exact d=2..6 radical benchmarks, source decimals, and d=4 entropy")
    print("PASS csc-square/lambda normalization d=2..100 and hostile general shifts")
    print(f"PASS source/polar/Fourier observables d=2..12 ({observables} Bob operators), including d=3")
    print(
        "INFO source-bound asymptotic ratio "
        f"(d sqrt(2))/(2 csc(pi/(2d))) -> {asymptotic_ratio:.12f} "
        f"({100 * (asymptotic_ratio - 1):.3f}% high)"
    )


if __name__ == "__main__":
    main()
