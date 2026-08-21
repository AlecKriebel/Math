#!/usr/bin/env python3
"""Exact full-lower exclusion of both delta=1 E6 survivors.

The two families retain every binary H3/H2 coefficient and every entry
of the linear part until E6 and E5 solve them.  E4 then exhibits a
nonzero right-kernel vector of the linear part.  Literal rank mutations
guard every divisor used to define the two exact-delta=1 open strata.
"""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: assertions are required", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp

p, q, r, z = sp.symbols("p q r z")
variables = (p, q, r)


def zero(value):
    return sp.cancel(sp.expand(value)) == 0


def binary(coefficients, degree):
    return sum(
        coefficients[index] * p ** (degree - index) * q**index
        for index in range(degree + 1)
    )


def weighted_coefficients(H4, H3, H2, L):
    determinant = sp.Poly(
        sp.expand(
            (
                L
                + z * H2.jacobian(variables)
                + z**2 * H3.jacobian(variables)
                + z**3 * H4.jacobian(variables)
            ).det()
        ),
        z,
    )
    return {
        degree: sp.expand(determinant.coeff_monomial(z**degree))
        for degree in range(9)
    }


def coefficient(value, p_degree, q_degree, r_degree):
    return sp.Poly(sp.expand(value), p, q, r).coeff_monomial(
        p**p_degree * q**q_degree * r**r_degree
    )


def jac(f, g):
    return sp.expand(
        sp.diff(f, p) * sp.diff(g, q)
        - sp.diff(f, q) * sp.diff(g, p)
    )


def coefficient_vector(value, degree):
    poly = sp.Poly(sp.expand(value), p, q)
    return sp.Matrix(
        [
            poly.coeff_monomial(p**index * q ** (degree - index))
            for index in range(degree, -1, -1)
        ]
    )


def split_ranks(h, R):
    P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
    alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
    multiplier_blocks = (
        ((1,), (1,), ()),
        ((p, q), (p, q), (1,)),
        ((p**2, p * q, q**2), (p**2, p * q, q**2), (p, q)),
    )
    output = []
    for offset, blocks in enumerate(multiplier_blocks):
        columns = (
            tuple(alpha * item for item in blocks[0])
            + tuple(beta * item for item in blocks[1])
            + tuple(gamma * item for item in blocks[2])
        )
        output.append(
            sp.Matrix.hstack(
                *(coefficient_vector(column, 5 + offset) for column in columns)
            ).rank()
        )
    return tuple(output)


# ---------------------------------------------------------------------------
# Branch-square survivor
# ---------------------------------------------------------------------------

b, d, k = sp.symbols("b d k")
bu = sp.symbols("bu0:4")
bv = sp.symbols("bv0:4")
bt = sp.symbols("bt0:3")
bx = sp.symbols("bx0:6")
by = sp.symbols("by0:6")
bl = sp.symbols("bl0:9")

branch_H4 = sp.Matrix([p**4, p**2 * q**2, 0])
branch_H3 = sp.Matrix(
    [
        binary(bu, 3) + 2 * k * r * p**2,
        binary(bv, 3) + k * r * q**2,
        b * p**2 * q + d * q**3,
    ]
)
branch_H2 = sp.Matrix(
    [
        binary(bx[:3], 2)
        + r * (bx[3] * p + bx[4] * q) + bx[5] * r**2,
        binary(by[:3], 2)
        + r * (by[3] * p + by[4] * q) + by[5] * r**2,
        binary(bt, 2) + k * b * q * r,
    ]
)
branch_L = sp.Matrix(3, 3, bl)
branch_E = weighted_coefficients(
    branch_H4, branch_H3, branch_H2, branch_L
)
assert zero(branch_E[8])
assert zero(branch_E[7])

branch_e6 = {
    bx[5]: k**2,
    by[5]: 0,
    bu[2]: 0,
    bt[1]: b * bv[2],
    by[3]: sp.Rational(3, 2) * k * bv[0],
    by[4]: k * bv[1],
    bx[3]: k * (sp.Rational(3, 2) * bu[0] - bv[2]),
    bx[4]: k * bu[1],
    bl[8]: k * bt[0],
}
assert zero(branch_E[6].subs(branch_e6))

# Mutation guard for k: this is the full remaining r-coefficient of E5.
branch_E5_after_E6 = sp.Poly(
    sp.expand(branch_E[5].subs(branch_e6)), r
)
branch_E5_r = sp.factor(branch_E5_after_E6.coeff_monomial(r))
branch_E5_r_expected = sp.Rational(3, 2) * k**2 * (
    2 * b * p**4 * bv[0]
    + b * p**2 * q**2 * bu[0]
    - 2 * b * p**2 * q**2 * bv[2]
    + 6 * d * p**2 * q**2 * bv[0]
    - 3 * d * q**4 * bu[0]
    + 6 * d * q**4 * bv[2]
)
assert zero(branch_E5_r - branch_E5_r_expected)
assert zero(branch_E5_r.subs(k, 0))
assert not zero(branch_E5_r.subs({b: 1, d: 1, k: 1}))

branch_e5_high = {bv[0]: 0, bu[0]: 2 * bv[2]}
branch_e5_constant = {
    bx[1]: bu[1] * bv[2],
    by[1]: bv[1] * bv[2],
    bl[2]: k * (bx[0] - bv[2] ** 2),
    bl[5]: k * by[0],
    bl[6]: bt[0] * bv[2],
}
branch_E5_completed = (
    branch_E[5]
    .subs(branch_e6)
    .subs(branch_e5_high)
    .subs(branch_e5_constant)
)
assert zero(branch_E5_completed)

branch_E4_completed = sp.expand(
    branch_E[4]
    .subs(branch_e6)
    .subs(branch_e5_high)
    .subs(branch_e5_constant)
)
branch_M0 = (k * bl[0] - bv[2] * bl[2]).subs(
    branch_e5_constant
)
branch_M3 = (k * bl[3] - bv[2] * bl[5]).subs(
    branch_e5_constant
)
branch_E4_expected = (
    2 * b * branch_M3 * p**4
    + (b * branch_M0 + 6 * d * branch_M3) * p**2 * q**2
    - 3 * d * branch_M0 * q**4
)
assert zero(branch_E4_completed - branch_E4_expected)

branch_L_completed = branch_L.subs(branch_e6).subs(
    branch_e5_constant
)
branch_kernel = sp.Matrix([k, 0, -bv[2]])
branch_kernel_residual = (
    branch_L_completed * branch_kernel
    - sp.Matrix([branch_M0, branch_M3, 0])
)
assert all(zero(entry) for entry in branch_kernel_residual)
# Wrong-sign mutation must not pass the kernel assertion.
assert not zero((branch_L_completed * sp.Matrix([k, 0, bv[2]]))[2])
assert zero(
    coefficient(branch_E4_expected, 4, 0, 0) - 2 * b * branch_M3
)
assert zero(
    coefficient(branch_E4_expected, 0, 4, 0) + 3 * d * branch_M0
)
print("PASS full branch-square E6/E5 solve and E4 kernel")


# ---------------------------------------------------------------------------
# Interior eta=0 survivor
# ---------------------------------------------------------------------------

a, c = sp.symbols("a c")
iu = sp.symbols("iu0:4")
iv = sp.symbols("iv0:4")
it = sp.symbols("it0:3")
ix = sp.symbols("ix0:6")
iy = sp.symbols("iy0:6")
il = sp.symbols("il0:9")

interior_H4 = sp.Matrix(
    [(p**2 + q**2) * p**2, (p**2 + q**2) * q**2, 0]
)
interior_H3 = sp.Matrix(
    [
        binary(iu, 3) + k * r * p**2,
        binary(iv, 3) + k * r * (p**2 + 2 * q**2),
        a * p**3 + c * p * q**2,
    ]
)
interior_H2 = sp.Matrix(
    [
        binary(ix[:3], 2)
        + r * (ix[3] * p + ix[4] * q) + ix[5] * r**2,
        binary(iy[:3], 2)
        + r * (iy[3] * p + iy[4] * q) + iy[5] * r**2,
        binary(it, 2) + k * c * p * r,
    ]
)
interior_L = sp.Matrix(3, 3, il)
interior_E = weighted_coefficients(
    interior_H4, interior_H3, interior_H2, interior_L
)
assert zero(interior_E[8])
assert zero(interior_E[7])

interior_e6 = {
    ix[5]: 0,
    iy[5]: k**2,
    iv[1]: iu[1],
    it[1]: c * iu[1],
    ix[3]: k * iu[2],
    ix[4]: sp.Rational(3, 2) * k * iu[3],
    iy[3]: k * iv[2],
    iy[4]: k * (sp.Rational(3, 2) * iv[3] - iu[1]),
    il[8]: k * it[2],
}
assert zero(interior_E[6].subs(interior_e6))

interior_E5_after_E6 = sp.Poly(
    sp.expand(interior_E[5].subs(interior_e6)), r
)
interior_E5_r = sp.factor(
    interior_E5_after_E6.coeff_monomial(r)
)
interior_E5_r_expected = sp.Rational(3, 2) * k**2 * (
    6 * a * p**4 * iu[1]
    + 3 * a * p**4 * iu[3]
    - 3 * a * p**4 * iv[3]
    + 6 * a * p**2 * q**2 * iu[3]
    - 8 * c * p**4 * iu[1]
    + 4 * c * p**4 * iv[3]
    - 2 * c * p**2 * q**2 * iu[1]
    - c * p**2 * q**2 * iu[3]
    + c * p**2 * q**2 * iv[3]
    + 2 * c * q**4 * iu[3]
)
assert zero(interior_E5_r - interior_E5_r_expected)
assert zero(interior_E5_r.subs(k, 0))
assert not zero(interior_E5_r.subs({a: 2, c: 1, k: 1}))

interior_e5_high = {iu[3]: 0, iv[3]: 2 * iu[1]}
interior_e5_constant = {
    ix[1]: iu[1] * iu[2],
    iy[1]: iu[1] * iv[2],
    ix[2]: il[2] / k,
    iy[2]: iu[1] ** 2 + il[5] / k,
    il[7]: it[2] * iu[1],
}
interior_E5_completed = sp.cancel(
    interior_E[5]
    .subs(interior_e6)
    .subs(interior_e5_high)
    .subs(interior_e5_constant)
)
assert zero(interior_E5_completed)

interior_E4_completed = sp.cancel(
    interior_E[4]
    .subs(interior_e6)
    .subs(interior_e5_high)
    .subs(interior_e5_constant)
)
interior_M1 = k * il[1] - iu[1] * il[2]
interior_M4 = k * il[4] - iu[1] * il[5]
interior_E4_expected = (
    (3 * a * interior_M1 + (-3 * a + 4 * c) * interior_M4)
    * p**4
    + ((6 * a - c) * interior_M1 + c * interior_M4)
    * p**2 * q**2
    + 2 * c * interior_M1 * q**4
)
assert zero(interior_E4_completed - interior_E4_expected)

interior_L_completed = interior_L.subs(interior_e6).subs(
    interior_e5_constant
)
interior_kernel = sp.Matrix([0, k, -iu[1]])
interior_kernel_residual = (
    interior_L_completed * interior_kernel
    - sp.Matrix([interior_M1, interior_M4, 0])
)
assert all(zero(entry) for entry in interior_kernel_residual)
assert not zero(
    (interior_L_completed * sp.Matrix([0, k, iu[1]]))[2]
)
assert zero(
    coefficient(interior_E4_expected, 0, 4, 0)
    - 2 * c * interior_M1
)
print("PASS full interior E6/E5 solve and E4 kernel")


# ---------------------------------------------------------------------------
# Divisor mutation guards
# ---------------------------------------------------------------------------

# b and d are both essential to the exact branch-square delta=1 open.
assert split_ranks(p**2, p**2 * q + q**3) == (2, 5, 7)
assert split_ranks(p**2, q**3) == (2, 5, 6)       # b=0
assert split_ranks(p**2, p**2 * q) == (2, 4, 5)  # d=0

# c and a-c are both essential to the exact interior delta=1 open.
interior_h = p**2 + q**2
assert split_ranks(interior_h, 2 * p**3 + p * q**2) == (2, 5, 7)
assert split_ranks(interior_h, p**3) == (2, 5, 6)  # c=0
assert split_ranks(interior_h, p**3 + p * q**2) == (2, 4, 5)  # a-c=0

# On k=0 the contact terms disappear; it is a separate binary/plane exit,
# not a specialization to which either nonzero kernel vector proof applies.
assert branch_kernel.subs(k, 0)[0] == 0
assert interior_kernel.subs(k, 0)[1] == 0
print("PASS b,d,c,a-c,k divisor mutations and final kernel vectors")

print("ALL EXACT DELTA=1 LOWER EXCLUSION CHECKS PASSED")
