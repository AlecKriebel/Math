#!/usr/bin/env python3
"""Exact top-identity tests for the all-vertical (e,a)=(2,2) frontier."""

if not __debug__:
    raise RuntimeError("verification must not run with Python optimization")

import sympy as sp


x, y, z, t = sp.symbols("x y z t")
variables = (x, y, z)


def require_zero(value, message):
    if sp.expand(value) != 0:
        raise AssertionError(message)


def monomials(degree):
    return tuple(
        x**i * y**j * z ** (degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def jac(a, b, c):
    return sp.expand(sp.Matrix([a, b, c]).jacobian(variables).det())


def cubic_kernel(h, p, q):
    coefficients = sp.symbols("kernel0:10")
    cubic = sum(
        coefficient * monomial
        for coefficient, monomial in zip(coefficients, monomials(3))
    )
    expression = jac(h * p, h * q, cubic)
    equations = [
        sp.Poly(expression, *variables).coeff_monomial(monomial)
        for monomial in monomials(8)
    ]
    matrix, constant = sp.linear_eq_to_matrix(equations, coefficients)
    if constant != sp.zeros(len(equations), 1):
        raise AssertionError("cubic kernel system is not homogeneous")
    kernel = tuple(
        sp.factor(
            sum(vector[index] * monomials(3)[index] for index in range(10))
        )
        for vector in matrix.nullspace()
    )
    return matrix.rank(), kernel


def conic_matrix(form):
    polynomial = sp.Poly(sp.expand(form), *variables)
    return sp.Matrix(
        [
            [
                polynomial.coeff_monomial(x**2),
                polynomial.coeff_monomial(x * y) / 2,
                polynomial.coeff_monomial(x * z) / 2,
            ],
            [
                polynomial.coeff_monomial(x * y) / 2,
                polynomial.coeff_monomial(y**2),
                polynomial.coeff_monomial(y * z) / 2,
            ],
            [
                polynomial.coeff_monomial(x * z) / 2,
                polynomial.coeff_monomial(y * z) / 2,
                polynomial.coeff_monomial(z**2),
            ],
        ]
    )


def require_minimal_sample(p, q, expected_determinant, message):
    actual = sp.factor(conic_matrix(p - t * q).det())
    require_zero(actual - expected_determinant, message)
    if actual == 0:
        raise AssertionError(f"{message}: generic conic is singular")


# The p=h reduction is an exact polynomial identity.
h0 = sp.symbols("h0")
h = x**2 + 2 * x * y + 3 * y * z + 5 * z**2
q = 2 * x**2 + x * z + y**2 + 7 * z**2
gcoeff = sp.symbols("g0:10")
G = sum(c * m for c, m in zip(gcoeff, monomials(3)))
require_zero(
    jac(h**2, h * q, G) - 2 * h**2 * jac(h, q, G),
    "p=h determinant reduction",
)


# Exhaustive canonical double-line kernels.
rank_two_rank, rank_two_kernel = cubic_kernel(x**2, x**2, y * z)
if rank_two_rank != 8 or set(rank_two_kernel) != {x**3, x * y * z}:
    raise AssertionError(
        f"rank-two restriction kernel: {rank_two_rank}, {rank_two_kernel}"
    )

rank_one_rank, rank_one_kernel = cubic_kernel(
    x**2, x**2, y**2 + x * z
)
if rank_one_rank != 8 or set(rank_one_kernel) != {
    x**3,
    x * (x * z + y**2),
}:
    raise AssertionError(
        f"rank-one restriction kernel: {rank_one_rank}, {rank_one_kernel}"
    )


# A p=h pencil with a double member has exactly the predicted two witnesses.
hd = x**2 + y**2 + z**2
double_rank, double_kernel = cubic_kernel(hd, hd, z**2)
if double_rank != 8 or set(double_kernel) != {z**3, z * (x**2 + y**2)}:
    raise AssertionError(
        f"double-member p=h kernel: {double_rank}, {double_kernel}"
    )
require_zero(
    jac(hd, z**2, z * hd),
    "coordinate-free double-member witness",
)
require_minimal_sample(
    hd,
    z**2,
    1 - t,
    "double-member p=h minimality",
)


# Genuine square-shape samples: even an additional double member does not
# evade the same-fibre obstruction.
square_samples = (
    (z**2, z * x, x**2 + y**2, t / 4, "square generic"),
    (z**2, z * x, y**2, t / 4, "square with other double member"),
)
for sample_h, sample_p, sample_q, determinant, label in square_samples:
    rank, kernel = cubic_kernel(sample_h, sample_p, sample_q)
    if rank != 10 or kernel:
        raise AssertionError(f"{label} cubic kernel: {rank}, {kernel}")
    require_minimal_sample(sample_p, sample_q, determinant, label)


# Distinct split vertical members.
split_h, split_p, split_q = y * z, x * y, z**2
split_rank, split_kernel = cubic_kernel(split_h, split_p, split_q)
if split_rank != 10 or split_kernel:
    raise AssertionError(
        f"distinct split cubic kernel: {split_rank}, {split_kernel}"
    )
require_minimal_sample(
    split_p,
    split_q,
    t / 4,
    "distinct split minimality",
)


# p=h with no double-line member.  The diagonal pencil has no rank-one
# member because no two of its three diagonal coefficients vanish together.
hn = x**2 + y**2 + z**2
qn = x**2 + 2 * y**2 + 3 * z**2
no_double_rank, no_double_kernel = cubic_kernel(hn, hn, qn)
if no_double_rank != 10 or no_double_kernel:
    raise AssertionError(
        f"no-double p=h cubic kernel: {no_double_rank}, {no_double_kernel}"
    )
require_minimal_sample(
    hn,
    qn,
    -(t - 1) * (2 * t - 1) * (3 * t - 1),
    "no-double p=h minimality",
)
u = sp.symbols("u")
diagonal_coefficients = (1 - u, 1 - 2 * u, 1 - 3 * u)
for first in range(3):
    for second in range(first + 1, 3):
        if sp.solve(
            [
                diagonal_coefficients[first],
                diagonal_coefficients[second],
            ],
            [u],
        ):
            raise AssertionError("diagonal pencil unexpectedly has rank one")


# Minimality is essential in the one remaining split specialization.
nonminimal_rank, nonminimal_kernel = cubic_kernel(y * z, y**2, z**2)
if nonminimal_rank != 6 or set(nonminimal_kernel) != {
    y**3,
    y**2 * z,
    y * z**2,
    z**3,
}:
    raise AssertionError(
        f"nonminimal split counterexample: "
        f"{nonminimal_rank}, {nonminimal_kernel}"
    )


# The two impossible same-fibre congruences have no integral solution.
for left in (6, 3):
    if left % 4 == 0:
        raise AssertionError("same-fibre valuation obstruction vanished")


print("all-vertical (2,2) top-obstruction SymPy checks passed")
