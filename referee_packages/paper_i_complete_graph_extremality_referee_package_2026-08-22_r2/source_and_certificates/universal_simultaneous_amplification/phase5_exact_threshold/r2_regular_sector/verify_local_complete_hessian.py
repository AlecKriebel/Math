#!/usr/bin/env python3
"""Exact certificate for the complete-kernel regular-sector Hessian theorem.

This verifier is independent of ``derive_complete_hessian.py``.  It uses the
rank/cut reduction proved in ``LOCAL_COMPLETE_HESSIAN_THEOREM.md`` rather than
constructing the absorbing subset chain.  All finite calculations use
``fractions.Fraction``.  SymPy is used only to expand integer polynomials and
check that every coefficient in the displayed positivity certificates is
strictly positive.
"""

from __future__ import annotations

from fractions import Fraction as F

import sympy as sp


class CertificateFailure(RuntimeError):
    """Raised when an explicit certificate check fails."""


def require(condition, detail="certificate check failed"):
    """Raise a failure that remains active under optimized Python."""
    if not condition:
        raise CertificateFailure(str(detail))


def gaussian_solve(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    """Solve a nonsingular rational system by exact Gauss--Jordan elimination."""

    n = len(rhs)
    aug = [row[:] + [value] for row, value in zip(matrix, rhs, strict=True)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [value / scale for value in aug[col]]
        for row in range(n):
            if row == col or not aug[row][col]:
                continue
            scale = aug[row][col]
            aug[row] = [
                left - scale * right
                for left, right in zip(aug[row], aug[col], strict=True)
            ]
    return [aug[row][-1] for row in range(n)]


def rho_complete(n: int) -> F:
    return F((n - 1) * 2 ** (n - 2), n * (2 ** (n - 1) - 1))


def rank_quantities(n: int):
    rho = rho_complete(n)

    def up(k: int) -> F:
        return F(2 * k, n - 1 + k)

    def down(k: int) -> F:
        return F(n - k, n + k - 2)

    def source(k: int) -> F:
        return rho * F(
            2 * (n - 1) * (n + k),
            2**k * (n + k - 1) * (n + k - 2),
        )

    def occupation(k: int) -> F:
        return rho * (
            F(n + k, k * (n - k))
            - F(n * 2 ** (k + 1), 2**n * k * (n - k))
        )

    def q2(k: int) -> F:
        return F(
            4 * k * (k - 1) * (n - k) * (n - k - 1),
            n * (n - 1) * (n - 2) * (n - 3),
        )

    def out2(k: int) -> F:
        return F(
            2 * k * (n - k) * (n - k - 1), n * (n - 1) * (n - 2)
        )

    def in2(k: int) -> F:
        return F(2 * k * (k - 1) * (n - k), n * (n - 1) * (n - 2))

    def first_up(k: int) -> F:
        return F(2 * (n - 1) ** 2, (n - 1 + k) ** 2)

    def first_down(k: int) -> F:
        return F(2 * (n - 1) ** 2, (n + k - 2) ** 2)

    def increment(k: int) -> F:
        return rho * F(n + k - 1, (n - 1) * 2**k)

    return (
        rho,
        up,
        down,
        source,
        occupation,
        q2,
        out2,
        in2,
        first_up,
        first_down,
        increment,
    )


def solve_v(n: int) -> dict[int, F]:
    _, up, down, source, *_ = rank_quantities(n)
    ranks = list(range(2, n - 1))
    matrix = [[F(0) for _ in ranks] for _ in ranks]
    rhs = [source(k) for k in ranks]
    for row, k in enumerate(ranks):
        matrix[row][row] = up(k) * (n - k) + down(k) * k
        if k + 1 <= n - 2:
            matrix[row][row + 1] = -up(k) * (n - k - 2)
        if k - 1 >= 2:
            matrix[row][row - 1] = -down(k) * (k - 2)
    values = gaussian_solve(matrix, rhs)
    result = {1: F(0), n - 1: F(0)}
    result.update(zip(ranks, values, strict=True))
    require(all(result[k] > 0 for k in ranks))
    return result


def direct_magnitude(n: int) -> F:
    (
        _,
        _,
        _,
        _,
        occupation,
        _,
        out2,
        in2,
        _,
        _,
        increment,
    ) = rank_quantities(n)
    return sum(
        occupation(k)
        * (
            F(4 * (n - 1) ** 3, (n - 1 + k) ** 3)
            * increment(k)
            * out2(k)
            + F(4 * (n - 1) ** 3, (n + k - 2) ** 3)
            * increment(k - 1)
            * in2(k)
        )
        for k in range(1, n)
    )


def response_coefficients(n: int) -> dict[int, F]:
    (
        _,
        _,
        _,
        _,
        occupation,
        q2,
        out2,
        in2,
        first_up,
        first_down,
        _,
    ) = rank_quantities(n)
    result: dict[int, F] = {}
    for k in range(2, n - 1):
        result[k] = 2 * (
            occupation(k) * (first_up(k) + first_down(k)) * q2(k)
            + occupation(k - 1)
            * first_up(k - 1)
            * (-q2(k - 1) + 2 * out2(k - 1))
            + occupation(k + 1)
            * first_down(k + 1)
            * (-q2(k + 1) + 2 * in2(k + 1))
        )
    require(all(value > 0 for value in result.values()))
    return result


def bar_v(n: int, k: int) -> F:
    _, _, _, source, *_ = rank_quantities(n)
    return F(21, 20) * F(n + k, 4 * n - 2 * k) * source(k)


def exact_hessian_per_edge_norm(n: int) -> F:
    v = solve_v(n)
    response = sum(
        coefficient * v[k]
        for k, coefficient in response_coefficients(n).items()
    )
    return -direct_magnitude(n) + response


def verify_finite_ranks() -> None:
    # The four-cycle test direction has squared edge norm four.  These values
    # therefore agree with one quarter of the independent subset-chain output.
    expected = {
        4: F(-27, 637),
        5: F(-367616, 7498125),
    }
    for n, value in expected.items():
        actual = exact_hessian_per_edge_norm(n)
        require(actual == value, (n, actual, value))

    # For n=6,7,8 the comparison v <= bar_v and the following exact total
    # ratios close the proof.  For n>=9 a pointwise certificate is used below.
    expected_ratios = {
        6: F(265019, 275520),
        7: F(32970550983, 36455056000),
        8: F(383371803381, 446439422000),
    }
    for n, expected_ratio in expected_ratios.items():
        coefficients = response_coefficients(n)
        bound = sum(coefficients[k] * bar_v(n, k) for k in coefficients)
        direct = direct_magnitude(n)
        require(bound / direct == expected_ratio)
        require(bound < direct)


def positive_coefficients(expression: sp.Expr, *variables: sp.Symbol) -> None:
    polynomial = sp.Poly(sp.cancel(expression), *variables)
    require(polynomial.coeffs())
    require(all(coefficient > 0 for coefficient in polynomial.coeffs()))


def verify_supersolution_certificate() -> None:
    a, b = sp.symbols("a b", integer=True, nonnegative=True)
    n = a + b + 4
    k = a + 2

    def up(index):
        return 2 * index / (n - 1 + index)

    def down(index):
        return (n - index) / (n + index - 2)

    # The common positive factor rho_K is omitted.
    def source(index):
        return 2 * (n - 1) * (n + index) / (
            2**index * (n + index - 1) * (n + index - 2)
        )

    def barrier(index):
        return sp.Rational(21, 20) * (n + index) / (4 * n - 2 * index) * source(index)

    residual = sp.factor(
        (up(k) * (n - k) + down(k) * k) * barrier(k)
        - up(k) * (n - k - 2) * barrier(k + 1)
        - down(k) * (k - 2) * barrier(k - 1)
        - source(k)
    )
    numerator, denominator = sp.fraction(residual)
    positive_coefficients(numerator, a, b)
    quotient, remainder = sp.div(numerator, a + b + 3, a, b)
    require(remainder == 0)
    barrier_polynomial = sp.Poly(quotient, a, b)
    require(len(barrier_polynomial.terms()) == 45)
    require(min(barrier_polynomial.coeffs()) == 16)
    require(all(coefficient > 0 for coefficient in barrier_polynomial.coeffs()))
    # Every displayed factor of this denominator is positive on a,b>=0.
    expected_denominator = (
        80
        * 2**a
        * (a + 2 * b + 5)
        * (a + 2 * b + 6)
        * (a + 2 * b + 7)
        * (2 * a + b + 3)
        * (2 * a + b + 4) ** 2
        * (2 * a + b + 5) ** 2
        * (2 * a + b + 6)
    )
    require(sp.expand(denominator - expected_denominator) == 0)


def verify_pointwise_large_n_certificate() -> None:
    """Prove ell_k bar(v)_k < D_{k-1} for n>=9, 2<=k<=n-2."""

    a, b, c, q = sp.symbols("a b c q", integer=True, nonnegative=True)
    n = a + b + 4
    k = a + 2
    j = k - 1

    def cubic(index):
        return (
            index**3
            + 3 * index**2 * n
            - 3 * index**2
            + 3 * index * n**2
            - 10 * index * n
            + 6 * index
            + n**3
            - 7 * n**2
            + 12 * n
            - 6
        )

    a_zero = k * n - 3 * k + n**2 - 3 * n + 3
    b_zero = k**2 + 2 * k * n - 6 * k + n**2 - 4 * n + 5
    # After cancelling positive common factors, D_{k-1}-ell_k*bar(v)_k
    # has the sign of H(q), with q=2^(k-n)=2^(-b-2).
    h = sp.expand(
        20
        * (n + k - 1 - n * q)
        * cubic(j)
        * (2 * n - k)
        * (n - 3)
        * (n + k - 1) ** 2
        - 21
        * n
        * (n - 1)
        * (n + k) ** 2
        * (a_zero - q * b_zero)
        * (n + k - 3) ** 2
    )
    h_poly = sp.Poly(h, q)
    h_zero = h_poly.coeff_monomial(1)
    h_one = h_poly.coeff_monomial(q)
    require(sp.expand(h - h_zero - q * h_one) == 0)

    # If b=0,...,4, the condition a+b>=5 is parameterized by
    # a=c+5-b.  The five exact univariate certificates have only positive
    # coefficients.
    for b_value in range(5):
        specialized = sp.expand(
            h.subs(
                {
                    b: b_value,
                    a: c + 5 - b_value,
                    q: sp.Rational(1, 2 ** (b_value + 2)),
                }
            )
        )
        positive_coefficients(specialized, c)
        polynomial = sp.Poly(specialized, c)
        require(polynomial.degree() == 8)
        require(min(polynomial.coeffs()) == (784, 696, 652, 630, 619)[b_value])

    # If b>=5, write b=c+5.  H_0 and 128 H_0+H_1 have positive
    # coefficients.  Since q<=1/128, this proves H_0+q H_1>0 whether
    # H_1 is nonnegative or negative at the point under consideration.
    large_h_zero = sp.Poly(sp.expand(h_zero.subs(b, c + 5)), a, c)
    large_combination = sp.Poly(
        sp.expand((128 * h_zero + h_one).subs(b, c + 5)), a, c
    )
    positive_coefficients(large_h_zero.as_expr(), a, c)
    positive_coefficients(large_combination.as_expr(), a, c)
    require(len(large_h_zero.terms()) == len(large_combination.terms()) == 45)
    require(min(large_h_zero.coeffs()) == 19)
    require(min(large_combination.coeffs()) == 2413)


def main() -> None:
    verify_finite_ranks()
    verify_supersolution_certificate()
    verify_pointwise_large_n_certificate()
    print("PASS: exact local complete-kernel Hessian certificate for every n>=4")


if __name__ == "__main__":
    main()
