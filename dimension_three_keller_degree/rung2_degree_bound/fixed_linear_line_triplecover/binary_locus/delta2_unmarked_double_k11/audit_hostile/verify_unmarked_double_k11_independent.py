#!/usr/bin/env python3
"""Dependency-free hostile reconstruction of the unmarked-double {1,1} row.

This deliberately does not import SymPy, PARI, or any project verifier.
Sparse multivariate polynomials over Fraction are enough for the raw
q^2 jets, divided-gradient columns, resultants, contact curvature, and
the two projective contact eliminations.
"""

from __future__ import annotations

from fractions import Fraction
import itertools
import os
import sys


MUTATION = os.environ.get("AUDIT_MUTATION", "strict")
NAMES = (
    "p", "q", "r",
    "b", "c", "d", "e",
    "x", "y", "lam", "mu",
    "aa0", "aa1", "aa2", "aa3",
    "bb0", "bb1", "bb2", "bb3",
    "rr0", "rr1", "rr2", "rr3",
)
INDEX = {name: index for index, name in enumerate(NAMES)}
NVAR = len(NAMES)
ZERO_MONOMIAL = (0,) * NVAR
Poly = dict[tuple[int, ...], Fraction]


def fail(message: str) -> None:
    print(f"FAIL [{MUTATION}]: {message}", file=sys.stderr)
    raise SystemExit(1)


def check(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def clean(poly: Poly) -> Poly:
    return {monomial: coefficient for monomial, coefficient in poly.items()
            if coefficient}


def const(value: int | Fraction) -> Poly:
    value = Fraction(value)
    return {} if not value else {ZERO_MONOMIAL: value}


def var(name: str) -> Poly:
    monomial = [0] * NVAR
    monomial[INDEX[name]] = 1
    return {tuple(monomial): Fraction(1)}


def add(*polys: Poly) -> Poly:
    result: Poly = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
    return clean(result)


def neg(poly: Poly) -> Poly:
    return {monomial: -coefficient for monomial, coefficient in poly.items()}


def sub(left: Poly, right: Poly) -> Poly:
    return add(left, neg(right))


def scale(poly: Poly, scalar: int | Fraction) -> Poly:
    scalar = Fraction(scalar)
    return clean({monomial: scalar * coefficient
                  for monomial, coefficient in poly.items()})


def mul(left: Poly, right: Poly) -> Poly:
    result: Poly = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(
                left_exponent + right_exponent
                for left_exponent, right_exponent
                in zip(left_monomial, right_monomial)
            )
            result[monomial] = (
                result.get(monomial, Fraction(0))
                + left_coefficient * right_coefficient
            )
    return clean(result)


def power(poly: Poly, exponent: int) -> Poly:
    check(exponent >= 0, "negative polynomial exponent")
    result = const(1)
    base = poly
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = mul(result, base)
        base = mul(base, base)
        remaining //= 2
    return result


def prod(*polys: Poly) -> Poly:
    result = const(1)
    for poly in polys:
        result = mul(result, poly)
    return result


def derivative(poly: Poly, name: str) -> Poly:
    variable_index = INDEX[name]
    result: Poly = {}
    for monomial, coefficient in poly.items():
        exponent = monomial[variable_index]
        if exponent:
            derived = list(monomial)
            derived[variable_index] -= 1
            result[tuple(derived)] = coefficient * exponent
    return clean(result)


def divide_monomial(poly: Poly, **powers: int) -> Poly:
    decrements = {INDEX[name]: exponent for name, exponent in powers.items()}
    result: Poly = {}
    for monomial, coefficient in poly.items():
        reduced = list(monomial)
        for variable_index, exponent in decrements.items():
            check(
                reduced[variable_index] >= exponent,
                f"nonpolynomial division by {NAMES[variable_index]}^{exponent}",
            )
            reduced[variable_index] -= exponent
        result[tuple(reduced)] = coefficient
    return clean(result)


def substitute(poly: Poly, replacements: dict[str, Poly | int | Fraction]) -> Poly:
    images: dict[int, Poly] = {}
    for name, image in replacements.items():
        images[INDEX[name]] = image if isinstance(image, dict) else const(image)
    result: Poly = {}
    for monomial, coefficient in poly.items():
        term = const(coefficient)
        for variable_index, exponent in enumerate(monomial):
            if not exponent:
                continue
            image = images.get(variable_index)
            if image is None:
                image = var(NAMES[variable_index])
            term = mul(term, power(image, exponent))
        result = add(result, term)
    return result


def coefficient(poly: Poly, **fixed_powers: int) -> Poly:
    fixed = {INDEX[name]: exponent for name, exponent in fixed_powers.items()}
    result: Poly = {}
    for monomial, value in poly.items():
        if any(monomial[index] != exponent for index, exponent in fixed.items()):
            continue
        reduced = list(monomial)
        for index in fixed:
            reduced[index] = 0
        result[tuple(reduced)] = result.get(tuple(reduced), Fraction(0)) + value
    return clean(result)


def degree_in(poly: Poly, name: str) -> int:
    if not poly:
        return -1
    variable_index = INDEX[name]
    return max(monomial[variable_index] for monomial in poly)


def divisible_by(poly: Poly, name: str, exponent: int = 1) -> bool:
    variable_index = INDEX[name]
    return all(monomial[variable_index] >= exponent for monomial in poly)


def determinant(matrix: list[list[Poly]]) -> Poly:
    size = len(matrix)
    check(all(len(row) == size for row in matrix), "nonsquare determinant")
    result: Poly = {}
    for permutation in itertools.permutations(range(size)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(size) for j in range(i + 1, size)
        )
        term = const(-1 if inversions % 2 else 1)
        for row, column in enumerate(permutation):
            term = mul(term, matrix[row][column])
        result = add(result, term)
    return result


def jac2(first: Poly, second: Poly) -> Poly:
    return sub(
        mul(derivative(first, "p"), derivative(second, "q")),
        mul(derivative(first, "q"), derivative(second, "p")),
    )


def jac3(first: Poly, second: Poly, third: Poly) -> Poly:
    return determinant([
        [derivative(form, name) for name in ("p", "q", "r")]
        for form in (first, second, third)
    ])


def cross(left: tuple[Poly, Poly, Poly],
          right: tuple[Poly, Poly, Poly]) -> tuple[Poly, Poly, Poly]:
    return (
        sub(mul(left[1], right[2]), mul(left[2], right[1])),
        sub(mul(left[2], right[0]), mul(left[0], right[2])),
        sub(mul(left[0], right[1]), mul(left[1], right[0])),
    )


def resultant(first: Poly, second: Poly, name: str) -> Poly:
    first_degree = degree_in(first, name)
    second_degree = degree_in(second, name)
    check(first_degree >= 0 and second_degree >= 0, "zero resultant input")
    first_coefficients = [
        coefficient(first, **{name: exponent})
        for exponent in range(first_degree, -1, -1)
    ]
    second_coefficients = [
        coefficient(second, **{name: exponent})
        for exponent in range(second_degree, -1, -1)
    ]
    size = first_degree + second_degree
    matrix = [[{} for _ in range(size)] for _ in range(size)]
    for row in range(second_degree):
        for offset, entry in enumerate(first_coefficients):
            matrix[row][row + offset] = entry
    for row in range(first_degree):
        for offset, entry in enumerate(second_coefficients):
            matrix[second_degree + row][row + offset] = entry
    return determinant(matrix)


def remainder_in(dividend: Poly, divisor: Poly, name: str) -> Poly:
    divisor_degree = degree_in(divisor, name)
    check(divisor_degree >= 0, "zero remainder divisor")
    leading = coefficient(divisor, **{name: divisor_degree})
    check(
        set(leading).issubset({ZERO_MONOMIAL})
        and leading.get(ZERO_MONOMIAL, 0),
        "remainder divisor must have constant leading coefficient",
    )
    leading_scalar = leading[ZERO_MONOMIAL]
    variable = var(name)
    result = dividend
    while degree_in(result, name) >= divisor_degree:
        result_degree = degree_in(result, name)
        lead = coefficient(result, **{name: result_degree})
        correction = scale(
            mul(
                lead,
                mul(power(variable, result_degree - divisor_degree), divisor),
            ),
            Fraction(1, 1) / leading_scalar,
        )
        result = sub(result, correction)
    return result


PVAR, QVAR, RVAR = var("p"), var("q"), var("r")
BPAR, CPAR, DPAR, EPAR = (var(name) for name in ("b", "c", "d", "e"))
XPAR, YPAR, LAM, MU = (var(name) for name in ("x", "y", "lam", "mu"))


def homogeneous_cubic(coefficients: tuple[Poly, Poly, Poly, Poly]) -> Poly:
    return add(*[
        prod(coefficient_value, power(PVAR, 3 - index), power(QVAR, index))
        for index, coefficient_value in enumerate(coefficients)
    ])


def normal_forms(
    b_value: Poly,
    c_value: Poly,
    d_value: Poly,
    e_value: Poly,
) -> tuple[Poly, Poly, Poly]:
    first = prod(PVAR, power(QVAR, 3))
    second = prod(
        PVAR,
        add(
            power(PVAR, 3),
            prod(b_value, power(PVAR, 2), QVAR),
            prod(c_value, PVAR, power(QVAR, 2)),
        ),
    )
    third = add(
        mul(
            d_value,
            add(
                power(PVAR, 3),
                scale(prod(b_value, power(PVAR, 2), QVAR), Fraction(3, 4)),
                prod(
                    add(
                        scale(c_value, Fraction(3, 4)),
                        scale(power(b_value, 2), Fraction(-3, 32)),
                    ),
                    PVAR,
                    power(QVAR, 2),
                ),
            ),
        ),
        prod(e_value, power(QVAR, 3)),
    )
    return first, second, third


def tangents(
    first: Poly,
    second: Poly,
    third: Poly,
    b_value: Poly,
    c_value: Poly,
) -> tuple[tuple[Poly, Poly, Poly], tuple[Poly, Poly, Poly]]:
    gradient_p = tuple(derivative(form, "p") for form in (first, second, third))
    gradient_q = tuple(derivative(form, "q") for form in (first, second, third))
    first_column = tuple(
        divide_monomial(
            sub(q_derivative, scale(mul(b_value, p_derivative), Fraction(1, 4))),
            q=1,
        )
        for p_derivative, q_derivative in zip(gradient_p, gradient_q)
    )
    discriminant = sub(scale(power(b_value, 2), 3), scale(c_value, 8))
    second_column = tuple(
        divide_monomial(
            add(
                mul(PVAR, first_entry),
                scale(mul(discriminant, p_derivative), Fraction(1, 16)),
            ),
            q=1,
        )
        for first_entry, p_derivative in zip(first_column, gradient_p)
    )
    return first_column, second_column


def contact_coefficients(
    first: Poly,
    second: Poly,
    third: Poly,
    first_column: tuple[Poly, Poly, Poly],
    second_column: tuple[Poly, Poly, Poly],
) -> list[Poly]:
    tangent = tuple(
        add(mul(XPAR, first_entry), mul(YPAR, second_entry))
        for first_entry, second_entry in zip(first_column, second_column)
    )
    r_tangent = tuple(mul(RVAR, entry) for entry in tangent)
    curvature = coefficient(
        add(
            jac3(first, r_tangent[1], r_tangent[2]),
            jac3(r_tangent[0], second, r_tangent[2]),
            jac3(r_tangent[0], r_tangent[1], third),
        ),
        r=1,
    )
    alpha = jac2(second, third)
    beta = neg(jac2(first, third))
    residual = sub(sub(curvature, mul(LAM, alpha)), mul(MU, beta))
    return [
        coefficient(residual, p=5 - index, q=index)
        for index in range(6)
    ]


# ---------------------------------------------------------------------------
# 1. Re-derive the complete q^2 jet normal form.
# ---------------------------------------------------------------------------

aa = tuple(var(f"aa{index}") for index in range(4))
bb = tuple(var(f"bb{index}") for index in range(4))
rr = tuple(var(f"rr{index}") for index in range(4))
raw_a = homogeneous_cubic(aa)
raw_b = homogeneous_cubic(bb)
raw_r = homogeneous_cubic(rr)
raw_p = mul(PVAR, raw_a)
raw_q = mul(PVAR, raw_b)
raw_minors = (
    jac2(raw_q, raw_r),
    neg(jac2(raw_p, raw_r)),
    jac2(raw_p, raw_q),
)
normalized = {"aa0": 0, "bb0": 1}
normalized_minors = tuple(substitute(value, normalized) for value in raw_minors)

alpha_q0 = coefficient(normalized_minors[0], p=5, q=0)
alpha_q1 = coefficient(normalized_minors[0], p=4, q=1)
beta_q0 = coefficient(normalized_minors[1], p=5, q=0)
beta_q1 = coefficient(normalized_minors[1], p=4, q=1)
gamma_q0 = coefficient(normalized_minors[2], p=6, q=0)
gamma_q1 = coefficient(normalized_minors[2], p=5, q=1)

check(
    alpha_q0 == add(scale(mul(bb[1], rr[0]), -3), scale(rr[1], 4)),
    "q^0 alpha jet",
)
check(beta_q0 == scale(mul(aa[1], rr[0]), 3), "q^0 beta jet")
check(gamma_q0 == scale(aa[1], -4), "q^0 gamma jet")
check(
    alpha_q1
    == add(
        mul(bb[1], rr[1]),
        scale(mul(bb[2], rr[0]), -6),
        scale(rr[2], 8),
    ),
    "q^1 alpha jet",
)
check(
    beta_q1
    == add(neg(mul(aa[1], rr[1])), scale(mul(aa[2], rr[0]), 6)),
    "q^1 beta jet",
)
check(gamma_q1 == scale(aa[2], -8), "q^1 gamma jet")

jet_solution = {
    "aa1": 0,
    "aa2": 0,
    "rr1": scale(mul(bb[1], rr[0]), Fraction(3, 4)),
    "rr2": mul(
        add(
            scale(bb[2], Fraction(3, 4)),
            scale(power(bb[1], 2), Fraction(-3, 32)),
        ),
        rr[0],
    ),
}
check(
    all(
        substitute(jet, jet_solution) == {}
        for jet in (
            alpha_q0, alpha_q1, beta_q0, beta_q1, gamma_q0, gamma_q1
        )
    ),
    "q^2 jet solution is sufficient",
)

# The four sequential pivots -4, -8, 4, 8 are units.  Thus the displayed
# solution is also necessary.  aa3 != 0 follows from J(P,Q) != 0; scaling
# aa3 and the target shear Q -> Q-(bb3/aa3)P give aa3=1, bb3=0.
if MUTATION == "q2_jet":
    wrong_rr2 = mul(
        add(
            scale(bb[2], Fraction(3, 4)),
            scale(power(bb[1], 2), Fraction(-1, 32)),
        ),
        rr[0],
    )
    check(
        substitute(alpha_q1, {**jet_solution, "rr2": wrong_rr2}) == {},
        "fault injection must corrupt the q^2 jet",
    )

print("PASS independent q^2 jet normal form")


# ---------------------------------------------------------------------------
# 2. Polynomial divided-gradient columns and the {1,1} basis.
# ---------------------------------------------------------------------------

P0, Q0, R0 = normal_forms(BPAR, CPAR, DPAR, EPAR)
N0, M0 = tangents(P0, Q0, R0, BPAR, CPAR)
K0 = sub(scale(power(BPAR, 2), 3), scale(CPAR, 8))
Fp = tuple(derivative(form, "p") for form in (P0, Q0, R0))
Fq = tuple(derivative(form, "q") for form in (P0, Q0, R0))

for row in range(3):
    check(
        mul(K0, Fp[row])
        == add(scale(mul(PVAR, N0[row]), -16), scale(mul(QVAR, M0[row]), 16)),
        f"first gradient reconstruction row {row}",
    )
    check(
        mul(K0, Fq[row])
        == add(
            mul(
                add(
                    scale(prod(power(BPAR, 2), QVAR), 3),
                    scale(prod(BPAR, PVAR), -4),
                    scale(prod(CPAR, QVAR), -8),
                ),
                N0[row],
            ),
            scale(prod(BPAR, QVAR, M0[row]), 4),
        ),
        f"second gradient reconstruction row {row}",
    )

numerator_determinant = sub(
    mul(scale(PVAR, -16), scale(prod(BPAR, QVAR), 4)),
    mul(
        add(
            scale(prod(power(BPAR, 2), QVAR), 3),
            scale(prod(BPAR, PVAR), -4),
            scale(prod(CPAR, QVAR), -8),
        ),
        scale(QVAR, 16),
    ),
)
check(
    numerator_determinant == scale(prod(K0, power(QVAR, 2)), -16),
    "change-of-basis determinant numerator",
)

top_minors = cross(Fp, Fq)
reduced_minors = tuple(divide_monomial(value, q=2) for value in top_minors)
column_wedge = cross(N0, M0)
for row in range(3):
    check(
        scale(column_wedge[row], 16)
        == neg(mul(K0, reduced_minors[row])),
        f"primitive wedge row {row}",
    )
check(
    all(divisible_by(substitute(value, {"e": 0}), "p")
        for value in reduced_minors),
    "exact q^2 globally forces e nonzero",
)

print("PASS independent polynomial {1,1} columns and wedge")


# ---------------------------------------------------------------------------
# 3. Generic-chart exact-gcd boundary, including projective endpoints.
# ---------------------------------------------------------------------------

Pg, Qg, Rg = normal_forms(const(1), CPAR, const(1), EPAR)
generic_minors = (
    jac2(Qg, Rg),
    neg(jac2(Pg, Rg)),
    jac2(Pg, Qg),
)
generic_reduced = tuple(divide_monomial(value, q=2) for value in generic_minors)
Hg = add(
    scale(power(PVAR, 2), 3),
    scale(prod(PVAR, QVAR), 2),
    mul(CPAR, power(QVAR, 2)),
)
check(
    generic_reduced[2] == scale(prod(power(PVAR, 2), Hg), -4),
    "generic reduced gamma factorization",
)
check(
    substitute(generic_reduced[1], {"p": 0})
    == scale(prod(EPAR, power(QVAR, 3)), -3),
    "generic reduced beta at p=0",
)

beta_affine = substitute(generic_reduced[1], {"q": 1})
h_affine = substitute(Hg, {"q": 1})
computed_resultant = resultant(beta_affine, h_affine, "p")
j_linear_coefficient = 321 if MUTATION == "gcd_J" else 320
Jg = add(
    scale(power(CPAR, 3), 192),
    scale(power(CPAR, 2), -48),
    scale(mul(CPAR, EPAR), -1024),
    scale(CPAR, -5),
    scale(power(EPAR, 2), 1024),
    scale(EPAR, j_linear_coefficient),
)
check(
    computed_resultant == scale(Jg, Fraction(243, 1024)),
    "generic exact-gcd resultant J",
)

# If e=0, p divides all three reduced minors.  If e!=0, p cannot be a
# common factor.  Every other common factor divides H; H(p,0)=3p^2, so
# it has no q=0 projective root.  The affine resultant then detects all
# remaining roots.  At a root of beta and H, the gradient syzygy and
# P_p=q^3 force alpha to vanish as well.
check(
    all(divisible_by(substitute(value, {"e": 0}), "p")
        for value in generic_reduced),
    "e=0 is a larger-gcd boundary",
)
gradient_syzygy = add(
    mul(derivative(Pg, "p"), generic_reduced[0]),
    mul(derivative(Qg, "p"), generic_reduced[1]),
    mul(derivative(Rg, "p"), generic_reduced[2]),
)
check(gradient_syzygy == {}, "reduced-minor gradient syzygy")
check(
    substitute(Hg, {"q": 0}) == scale(power(PVAR, 2), 3),
    "q=0 projective endpoint is not on H",
)

print("PASS independent exact-gcd boundary e*J and projective endpoints")


# ---------------------------------------------------------------------------
# 4. Raw contact curvature and both generic projective charts.
# ---------------------------------------------------------------------------

Ng, Mg = tangents(Pg, Qg, Rg, const(1), CPAR)
generic_contact = contact_coefficients(Pg, Qg, Rg, Ng, Mg)
Kg = add(const(3), scale(CPAR, -8))

# y=0, x=1.
y0 = [
    substitute(value, {"y": 0, "x": 1})
    for value in generic_contact
]
check(y0[0] == {} and y0[1] == {}, "generic y=0 leading zeros")
check(
    y0[5] == scale(mul(EPAR, add(CPAR, scale(MU, 8))), Fraction(3, 8)),
    "generic y=0 mu pivot",
)
mu_value = scale(CPAR, Fraction(-1, 8))
y0_mu = [substitute(value, {"mu": mu_value}) for value in y0]
check(
    y0_mu[4]
    == scale(
        mul(
            EPAR,
            add(scale(prod(LAM, CPAR), 16), scale(CPAR, -8), const(-3)),
        ),
        Fraction(-3, 8),
    ),
    "generic y=0 lambda pivot",
)

# Cross-multiply the candidate lambda to avoid dividing by c.
lambda_numerator = add(scale(CPAR, 8), const(3))
lambda_denominator = scale(CPAR, 16)
for index, expected in (
    (
        2,
        scale(
            prod(
                add(scale(CPAR, 8), const(-3)),
                add(
                    scale(power(CPAR, 2), 96),
                    scale(CPAR, -36),
                    scale(EPAR, -128),
                    const(5),
                ),
            ),
            Fraction(-3, 32),
        ),
    ),
    (
        3,
        scale(
            prod(
                add(scale(CPAR, 8), const(-3)),
                add(
                    scale(mul(CPAR, EPAR), 32),
                    CPAR,
                    scale(EPAR, -24),
                ),
            ),
            Fraction(-3, 8),
        ),
    ),
):
    # Multiply f((8c+3)/(16c)) by 16c without introducing a rational
    # function into the sparse polynomial ring.
    lam_coefficient = coefficient(y0_mu[index], lam=1)
    lam_constant = coefficient(y0_mu[index], lam=0)
    cross_multiplied = add(
        mul(lam_coefficient, lambda_numerator),
        mul(lam_constant, lambda_denominator),
    )
    check(
        cross_multiplied == expected,
        f"generic y=0 residual {index}",
    )

e_value = scale(
    add(scale(power(CPAR, 2), 96), scale(CPAR, -36), const(5)),
    Fraction(1, 128),
)
second_y0_factor = add(
    scale(mul(CPAR, EPAR), 32),
    CPAR,
    scale(EPAR, -24),
)
check(
    substitute(second_y0_factor, {"e": e_value})
    == scale(
        prod(power(add(scale(CPAR, 4), const(-1)), 2),
             add(scale(CPAR, 8), const(-5))),
        Fraction(3, 16),
    ),
    "generic y=0 contact alternatives",
)
check(
    substitute(Jg, {"e": e_value})
    == scale(
        prod(
            power(add(scale(CPAR, 4), const(-1)), 2),
            power(add(scale(CPAR, 8), const(-5)), 2),
        ),
        Fraction(9, 16),
    ),
    "generic y=0 alternatives lie on J=0",
)

# y=1.
y1 = [substitute(value, {"y": 1}) for value in generic_contact]
e0 = scale(
    neg(add(const(25), scale(CPAR, -144), scale(power(CPAR, 2), 192))),
    Fraction(1, 512),
)
h = add(scale(power(CPAR, 2), 64), scale(CPAR, -16), const(-1))
check(
    y1[0]
    == scale(
        add(
            scale(power(CPAR, 2), 192),
            scale(CPAR, -144),
            scale(EPAR, 512),
            const(25),
        ),
        Fraction(3, 128),
    ),
    "generic y=1 e pivot",
)
check(
    substitute(y1[1], {"e": e0})
    == scale(prod(add(scale(CPAR, 8), const(-3)), h), Fraction(-45, 2048)),
    "generic y=1 h pivot",
)

remainders = [
    remainder_in(substitute(value, {"e": e0}), h, "c")
    for value in y1[2:]
]
R2 = add(
    scale(prod(LAM, CPAR), -1024),
    scale(LAM, 256),
    scale(MU, -2048),
    scale(prod(CPAR, power(XPAR, 2)), 1024),
    scale(prod(CPAR, XPAR), -512),
    scale(CPAR, -104),
    scale(power(XPAR, 2), -320),
    scale(XPAR, 160),
    const(31),
)
r3_constant = 122 if MUTATION == "contact_R3" else 121
R3 = add(
    scale(prod(LAM, CPAR), -5120),
    scale(LAM, 1280),
    scale(MU, -10240),
    scale(prod(CPAR, power(XPAR, 2)), 5120),
    scale(prod(CPAR, XPAR), -3904),
    scale(CPAR, -408),
    scale(power(XPAR, 2), -1600),
    scale(XPAR, 1208),
    const(r3_constant),
)
check(
    remainders[0] == scale(R2, Fraction(9, 2048)),
    "generic y=1 first reduced contact",
)
check(
    remainders[1] == scale(R3, Fraction(3, 8192)),
    "generic y=1 second reduced contact",
)
check(
    sub(R3, scale(R2, 5))
    == scale(
        prod(add(scale(CPAR, 56), const(-17)),
             add(scale(XPAR, 12), const(-1))),
        -2,
    ),
    "generic y=1 x compatibility",
)
check(
    resultant(h, add(scale(CPAR, 56), const(-17)), "c") == const(128),
    "generic y=1 first nonzero resultant",
)

x_value = const(Fraction(1, 12))
E0 = add(
    scale(prod(LAM, CPAR), 9216),
    scale(LAM, -2304),
    scale(MU, 18432),
    scale(CPAR, 1256),
    const(-379),
)
e1_constant = -3864 if MUTATION == "contact_E1" else -3865
E1 = add(
    scale(prod(LAM, CPAR), 4608),
    scale(LAM, -1728),
    scale(prod(MU, CPAR), -73728),
    scale(MU, 9216),
    scale(CPAR, 12792),
    const(e1_constant),
)
E2 = add(
    scale(prod(MU, CPAR), 221184),
    scale(MU, -64512),
    scale(CPAR, -824),
    const(249),
)
check(
    substitute(remainders[0], {"x": x_value}) == scale(E0, Fraction(-1, 2048)),
    "generic y=1 E0",
)
check(
    substitute(remainders[2], {"x": x_value}) == scale(E1, Fraction(1, 98304)),
    "generic y=1 E1",
)
check(
    substitute(remainders[3], {"x": x_value}) == scale(E2, Fraction(1, 393216)),
    "generic y=1 E2",
)

def linear_row(equation: Poly) -> list[Poly]:
    lam_coefficient = coefficient(equation, lam=1, mu=0)
    mu_coefficient = coefficient(equation, lam=0, mu=1)
    constant_part = coefficient(equation, lam=0, mu=0)
    return [lam_coefficient, mu_coefficient, constant_part]


augmented = [linear_row(equation) for equation in (E0, E1, E2)]
augmented_remainder = remainder_in(determinant(augmented), h, "c")
check(
    augmented_remainder
    == scale(add(scale(CPAR, 79048), const(-23855)), -31850496),
    "generic y=1 augmented determinant",
)
check(
    resultant(h, add(scale(CPAR, 79048), const(-23855)), "c")
    == const(278656),
    "generic y=1 final nonzero resultant",
)

print("PASS independent generic y=0 and y!=0 contact eliminations")


# ---------------------------------------------------------------------------
# 5. The three remaining scaling charts from raw curvature.
# ---------------------------------------------------------------------------

# b!=0,d=0: b=e=1.
P10, Q10, R10 = normal_forms(const(1), CPAR, const(0), const(1))
N10, M10 = tangents(P10, Q10, R10, const(1), CPAR)
contact10 = contact_coefficients(P10, Q10, R10, N10, M10)
check(contact10[0] == scale(power(YPAR, 2), 12), "b!=0,d=0 y pivot")
contact10_y0 = [
    substitute(value, {"y": 0, "x": 1}) for value in contact10
]
check(
    contact10_y0[2] == scale(add(LAM, const(-1)), -12),
    "b!=0,d=0 lambda pivot",
)
check(
    contact10_y0[3]
    == scale(add(scale(CPAR, 8), scale(LAM, 12), const(-15)), Fraction(-3, 4)),
    "b!=0,d=0 K boundary",
)

# b=0,c!=0,d!=0: c=d=1.
P01, Q01, R01 = normal_forms(const(0), const(1), const(1), EPAR)
N01, M01 = tangents(P01, Q01, R01, const(0), const(1))
contact01 = contact_coefficients(P01, Q01, R01, N01, M01)
check(contact01[0] == scale(power(YPAR, 2), Fraction(9, 2)),
      "b=0,c!=0,d!=0 y pivot")
contact01_y0 = [
    substitute(value, {"y": 0, "x": 1}) for value in contact01
]
check(contact01_y0[5] == scale(mul(EPAR, MU), 3),
      "b=0,c!=0,d!=0 mu pivot")
check(
    contact01_y0[4] == scale(add(MU, scale(mul(EPAR, LAM), 8)), Fraction(-3, 4)),
    "b=0,c!=0,d!=0 lambda pivot",
)
check(
    contact01_y0[3] == scale(add(LAM, scale(EPAR, 4)), Fraction(-3, 2)),
    "b=0,c!=0,d!=0 contradiction",
)

# b=d=0,c!=0: c=e=1.
P00, Q00, R00 = normal_forms(const(0), const(1), const(0), const(1))
N00, M00 = tangents(P00, Q00, R00, const(0), const(1))
contact00 = contact_coefficients(P00, Q00, R00, N00, M00)
check(contact00[1] == scale(power(YPAR, 2), 30),
      "b=d=0,c!=0 y pivot")
check(
    substitute(contact00[3], {"y": 0, "x": 1}) == const(-6),
    "b=d=0,c!=0 contradiction",
)

print("PASS independent three boundary contact charts")
print("ALL INDEPENDENT UNMARKED-DOUBLE {1,1} AUDIT CHECKS PASSED")
