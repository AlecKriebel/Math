#!/usr/bin/python3
"""Exact checks for the nonbinary fixed-quadratic line-cover theorem."""

from __future__ import annotations

import sympy as sp

if not __debug__:
    raise RuntimeError("verification requires Python assertions")

p, q, r, t, s, z = sp.symbols("p q r t s z")
variables = (p, q, r)
cubic_monomials = (
    p**3,
    p**2 * q,
    p * q**2,
    q**3,
    p**2 * r,
    p * q * r,
    q**2 * r,
    p * r**2,
    q * r**2,
    r**3,
)
quadratic_monomials = (p**2, p * q, q**2, p * r, q * r, r**2)


def jac(vector: sp.Matrix) -> sp.Matrix:
    return vector.jacobian(variables)


def is_zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.expand(entry) == 0 for entry in matrix)


def coefficients(expression: sp.Expr) -> list[sp.Expr]:
    return [
        coefficient
        for _, coefficient in sp.Poly(
            sp.expand(expression), p, q, r
        ).terms()
    ]


def coefficient(
    expression: sp.Expr, exponents: tuple[int, int, int]
) -> sp.Expr:
    return sp.Poly(sp.expand(expression), p, q, r).coeff_monomial(
        exponents
    )


def weighted(
    H4: sp.Matrix, H3: sp.Matrix, H2: sp.Matrix, L0: sp.Matrix
) -> sp.Poly:
    return sp.Poly(
        sp.expand(
            (
                L0
                + z * jac(H2)
                + z**2 * jac(H3)
                + z**3 * jac(H4)
            ).det()
        ),
        z,
    )


# General adjugate and logarithmic derivation.
hc = sp.symbols("hc0:6")
h = sum(hc[i] * quadratic_monomials[i] for i in range(6))
hr = sp.diff(h, r)
H4_general = sp.Matrix([h * p**2, h * q**2, 0])
C_general = jac(H4_general)
k = sp.Matrix([p * hr, q * hr, r * hr - 4 * h])
e3 = sp.Matrix([0, 0, 1])
assert is_zero_matrix(C_general * k)
assert is_zero_matrix(
    C_general.adjugate() + 2 * h * p * q * k * e3.T
)

for degree, monomials in (
    (3, cubic_monomials),
    (2, quadratic_monomials),
):
    gc = sp.symbols(f"g{degree}c0:{len(monomials)}")
    G = sum(gc[i] * monomials[i] for i in range(len(monomials)))
    DkG = sum(
        sp.diff(G, variables[i]) * k[i] for i in range(3)
    )
    Hts = sp.expand(h.subs({q: p * t, r: p * s}) / p**2)
    gts = sp.expand(G.subs({q: p * t, r: p * s}) / p**degree)
    expected = p ** (degree + 1) * (
        degree * sp.diff(Hts, s) * gts
        - 4 * Hts * sp.diff(gts, s)
    )
    assert (
        sp.expand(DkG.subs({q: p * t, r: p * s}) - expected)
        == 0
    )

# Exceptional square and its complete quadratic invariant space.
H4 = sp.Matrix([p**2 * r**2, q**2 * r**2, 0])
hr_square = 2 * r
k_square = sp.Matrix([2 * p * r, 2 * q * r, -2 * r**2])
gc2 = sp.symbols("g2c0:6")
G2 = sum(gc2[i] * quadratic_monomials[i] for i in range(6))
D_square_G2 = sum(
    sp.diff(G2, variables[i]) * k_square[i] for i in range(3)
)
kernel_matrix, _ = sp.linear_eq_to_matrix(
    coefficients(D_square_G2), gc2
)
kernel = kernel_matrix.nullspace()
assert kernel_matrix.rank() == 4
assert {
    sp.expand(
        sum(vector[i] * quadratic_monomials[i] for i in range(6))
    )
    for vector in kernel
} == {p * r, q * r}

# Raw E6 kernels for the two nonzero invariant orbits.
u = sp.symbols("u0:20")
H3_raw = sp.Matrix(
    [
        sum(u[10 * row + j] * cubic_monomials[j] for j in range(10))
        if row < 2
        else 0
        for row in range(3)
    ]
)
v = sp.symbols("v0:12")
L = sp.symbols("L0:9")
L0_raw = sp.Matrix(3, 3, L)


def raw_E6(normal_component: sp.Expr) -> tuple[sp.Matrix, sp.Expr]:
    H2_raw = sp.Matrix(
        [
            sum(
                v[6 * row + j] * quadratic_monomials[j]
                for j in range(6)
            )
            if row < 2
            else normal_component
            for row in range(3)
        ]
    )
    determinant = weighted(H4, H3_raw, H2_raw, L0_raw)
    assert sp.expand(determinant.coeff_monomial(z**8)) == 0
    assert sp.expand(determinant.coeff_monomial(z**7)) == 0
    E6 = sp.expand(determinant.coeff_monomial(z**6))
    unknowns = tuple(u) + (L[6], L[7], L[8])
    matrix, right = sp.linear_eq_to_matrix(coefficients(E6), unknowns)
    assert all(entry == 0 for entry in right)
    return matrix, E6


matrix_pr, _ = raw_E6(p * r)
matrix_sum, _ = raw_E6((p + q) * r)
assert matrix_pr.rank() == 10
assert len(matrix_pr.nullspace()) == 13
assert matrix_sum.rank() == 14
assert len(matrix_sum.nullspace()) == 9

a, b, c = sp.symbols("a b c")
Ucoeff = sp.symbols("U0:10")
U = sum(Ucoeff[i] * cubic_monomials[i] for i in range(10))
H3_pr = sp.Matrix([2 * p * r * (a * p + b * q + c * r), U, 0])

# The complete E5 solution in the pr orbit.
H2_pr_raw = sp.Matrix(
    [
        sum(v[6 * row + j] * quadratic_monomials[j] for j in range(6))
        if row < 2
        else p * r
        for row in range(3)
    ]
)
L0_pr = sp.Matrix(
    [[L[0], L[1], L[2]], [L[3], L[4], L[5]], [a, b, c]]
)
raw_pr_after_E6 = weighted(H4, H3_pr, H2_pr_raw, L0_pr)
raw_pr_E5 = raw_pr_after_E6.coeff_monomial(z**5)
raw_pr_lower_unknowns = tuple(v) + tuple(L[:6])
raw_pr_E5_matrix, _ = sp.linear_eq_to_matrix(
    coefficients(raw_pr_E5), raw_pr_lower_unknowns
)
assert raw_pr_E5_matrix.rank() == 4

Vrawcoeff = sp.symbols("Vraw0:6")
Vraw = sum(
    Vrawcoeff[i] * quadratic_monomials[i] for i in range(6)
)
d, e = sp.symbols("d e")
H2_pr = sp.Matrix(
    [
        (a * p + b * q) ** 2
        + d * p * r
        + e * q * r
        + c**2 * r**2,
        Vraw,
        p * r,
    ]
)
det_pr = weighted(H4, H3_pr, H2_pr, L0_pr)
for degree in (8, 7, 6, 5):
    assert sp.expand(det_pr.coeff_monomial(z**degree)) == 0

K = sp.symbols("K")
E4_pr = sp.expand(det_pr.coeff_monomial(z**4).subs({e: 2 * b * c - K}))
expected_E4_pr = (
    3 * K * Ucoeff[0] * p**3 * r
    + 3 * K * Ucoeff[1] * p**2 * q * r
    + K * Ucoeff[4] * p**2 * r**2
    + 3 * K * Ucoeff[2] * p * q**2 * r
    + (
        2 * L[0]
        + K * Ucoeff[5]
        + 4 * a**2 * c
        - 2 * a * d
    )
    * p
    * q
    * r**2
    - K * Ucoeff[7] * p * r**3
    + 3 * K * Ucoeff[3] * q**3 * r
    + (
        2 * L[1]
        + K * Ucoeff[6]
        + 4 * a * b * c
        - 2 * b * d
    )
    * q**2
    * r**2
    + (
        -2 * L[2]
        - K * Ucoeff[8]
        - 4 * a * c**2
        + 2 * c * d
    )
    * q
    * r**3
    - 3 * K * Ucoeff[9] * r**4
)
assert sp.expand(E4_pr - expected_E4_pr) == 0

# K=0 makes the first and third linear rows proportional.
L0_pr_K0 = sp.Matrix(
    [
        [
            a * (d - 2 * a * c),
            b * (d - 2 * a * c),
            c * (d - 2 * a * c),
        ],
        [L[3], L[4], L[5]],
        [a, b, c],
    ]
)
assert sp.expand(L0_pr_K0.det()) == 0

# K nonzero branch through E2.
A, B, Cc, g, j = sp.symbols("A B Cc g j")
m, n, o = sp.symbols("m n o")
H3_pr_final = sp.Matrix(
    [
        2 * p * r * (a * p + b * q + c * r),
        q * r * (A * p + B * q + Cc * r),
        0,
    ]
)
H2_pr_final = sp.Matrix(
    [
        (a * p + b * q) ** 2
        + d * p * r
        + (2 * b * c - K) * q * r
        + c**2 * r**2,
        (A * p + B * q) ** 2 / 4
        + g * p * r
        + j * q * r
        + Cc**2 * r**2 / 4,
        p * r,
    ]
)
L0_pr_final = sp.Matrix(
    [
        [
            -A * K / 2 - 2 * a**2 * c + a * d,
            -B * K / 2 - 2 * a * b * c + b * d,
            -Cc * K / 2 - 2 * a * c**2 + c * d,
        ],
        [m, n, o],
        [a, b, c],
    ]
)
det_pr_final = weighted(
    H4, H3_pr_final, H2_pr_final, L0_pr_final
)
for degree in (8, 7, 6, 5, 4, 3):
    assert sp.expand(det_pr_final.coeff_monomial(z**degree)) == 0
lower_pr = {
    m: (-A * B * Cc - 2 * A * Cc * a + 2 * A * j + 4 * a * g)
    / 4,
    n: (-2 * A * Cc * b - B**2 * Cc + 2 * B * j + 4 * b * g)
    / 4,
    o: (-2 * A * Cc * c - B * Cc**2 + 2 * Cc * j + 4 * c * g)
    / 4,
}
assert sp.expand(det_pr_final.coeff_monomial(z**2).subs(lower_pr)) == 0
assert sp.expand(det_pr_final.coeff_monomial(z).subs(lower_pr)) == 0
assert sp.expand(L0_pr_final.det().subs(lower_pr)) == 0

# Raw (p+q)r E5: the three binary coefficients of W vanish by squares.
w = sp.symbols("w0:6")
Wraw = sum(w[i] * quadratic_monomials[i] for i in range(6))
H3_sum_raw = sp.Matrix(
    [-p * Wraw + 2 * p * r * (a * p + b * q + c * r), q * Wraw, 0]
)
H2_sum_raw = sp.Matrix(
    [
        sum(v[j] * quadratic_monomials[j] for j in range(6)),
        sum(v[6 + j] * quadratic_monomials[j] for j in range(6)),
        (p + q) * r,
    ]
)
det_sum_raw = weighted(H4, H3_sum_raw, H2_sum_raw, L0_pr)
assert sp.expand(det_sum_raw.coeff_monomial(z**6)) == 0
E5_sum_raw = det_sum_raw.coeff_monomial(z**5)
E5_sum_coefficients = coefficients(E5_sum_raw)
assert any(sp.expand(value + 3 * w[0] ** 2) == 0 for value in E5_sum_coefficients)
assert any(sp.expand(value + 3 * w[2] ** 2) == 0 for value in E5_sum_coefficients)
after_outer_squares = [
    sp.expand(value.subs({w[0]: 0, w[2]: 0}))
    for value in E5_sum_coefficients
]
assert any(
    sp.expand(value + 3 * w[1] ** 2) == 0
    for value in after_outer_squares
)
sum_E5_matrix, _ = sp.linear_eq_to_matrix(
    [
        sp.expand(value.subs({w[0]: 0, w[1]: 0, w[2]: 0}))
        for value in E5_sum_coefficients
    ],
    raw_pr_lower_unknowns,
)
assert sum_E5_matrix.rank() == 6

# Complete post-E5 form for the sum orbit.
D, E, T = sp.symbols("D E T")
alpha, beta, gamma = sp.symbols("alpha beta gamma")
X, Y, P, Q, R, S = sp.symbols("X Y P Q R S")
H3_sum = sp.Matrix(
    [
        -p * r * (D * p + E * q + T * r)
        + 2 * p * r * (a * p + b * q + c * r),
        q * r * (D * p + E * q + T * r),
        0,
    ]
)
H2_sum = sp.Matrix(
    [
        (alpha**2 / 4 + X) * p**2
        + (alpha * beta / 2 + Y) * p * q
        + beta**2 * q**2 / 4
        + P * p * r
        + Q * q * r
        + gamma**2 * r**2 / 4,
        D**2 * p**2 / 4
        + (D * E / 2 - X) * p * q
        + (E**2 / 4 - Y) * q**2
        + R * p * r
        + S * q * r
        + T**2 * r**2 / 4,
        (p + q) * r,
    ]
).subs({alpha: D - 2 * a, beta: E - 2 * b, gamma: T - 2 * c})
det_sum = weighted(H4, H3_sum, H2_sum, L0_pr)
for degree in (8, 7, 6, 5):
    assert sp.expand(det_sum.coeff_monomial(z**degree)) == 0

E4_sum = sp.expand(det_sum.coeff_monomial(z**4))
shift = {D: 2 * a + alpha, E: 2 * b + beta, T: 2 * c + gamma}
E4_shift = sp.expand(E4_sum.subs(shift))
assert sp.expand(
    coefficient(E4_shift, (3, 0, 1)) - 3 * (2 * a + alpha) * X
) == 0
assert sp.expand(
    coefficient(E4_shift, (2, 1, 1))
    - 3 * ((alpha + 2 * b + beta) * X + (2 * a + alpha) * Y)
) == 0
assert sp.expand(
    coefficient(E4_shift, (1, 2, 1))
    - 3 * (beta * X + (alpha + 2 * b + beta) * Y)
) == 0
assert sp.expand(
    coefficient(E4_shift, (0, 3, 1)) - 3 * beta * Y
) == 0

# Standard branch X=Y=0.  Solve E4, then expose the common E3 factor.
standard_substitution = dict(shift)
standard_substitution.update({X: 0, Y: 0})
E4_standard = sp.Poly(
    sp.expand(E4_sum.subs(standard_substitution)), p, q, r
)
E4_solution_list = sp.solve(
    [value for _, value in E4_standard.terms()],
    [L[0], L[1], L[2], L[3], L[5]],
    dict=True,
    simplify=False,
)
assert len(E4_solution_list) == 1
E4_solution = E4_solution_list[0]
det_sum_standard = sp.Poly(
    sp.expand(
        weighted(H4, H3_sum, H2_sum, L0_pr)
        .as_expr()
        .subs(standard_substitution)
        .subs(E4_solution)
    ),
    z,
)
M = (
    -4 * L[4]
    + 4 * a * beta * c
    + 2 * a * beta * gamma
    + 2 * alpha * beta * c
    + alpha * beta * gamma
    - 8 * b**2 * c
    - 4 * b**2 * gamma
    - 8 * b * beta * c
    - 4 * b * beta * gamma
    + 4 * b * S
    - 2 * beta**2 * c
    - beta**2 * gamma
    - 2 * beta * R
    + 2 * beta * S
)
E3_standard = det_sum_standard.coeff_monomial(z**3)
assert sp.expand(
    coefficient(E3_standard, (2, 0, 1))
    - (2 * a + alpha) * M / 2
) == 0
assert sp.expand(
    coefficient(E3_standard, (1, 1, 1))
    - (alpha + 2 * b + beta) * M / 2
) == 0
assert sp.expand(
    coefficient(E3_standard, (0, 2, 1)) - beta * M / 2
) == 0
M_zero = {L[4]: sp.solve(M, L[4], dict=False)[0]}
L0_sum_standard = sp.Matrix(
    [
        [L[0], L[1], L[2]],
        [L[3], L[4], L[5]],
        [a, b, c],
    ]
).subs(standard_substitution).subs(E4_solution)
assert sp.expand(L0_sum_standard.det().subs(M_zero)) == 0

# Deep exceptional branch.  E3 kills X,Y; E2/E1 give M_*^2.
exceptional_substitution = {
    D: 0,
    E: 2 * a,
    T: 2 * c + gamma,
    b: a,
}
E4_exceptional = sp.Poly(
    sp.expand(E4_sum.subs(exceptional_substitution)), p, q, r
)
exceptional_solution_list = sp.solve(
    [value for _, value in E4_exceptional.terms()],
    [L[0], L[1], L[2], L[3], L[5]],
    dict=True,
    simplify=False,
)
assert len(exceptional_solution_list) == 1
exceptional_solution = exceptional_solution_list[0]
det_exceptional = sp.Poly(
    sp.expand(
        weighted(H4, H3_sum, H2_sum, L0_pr)
        .as_expr()
        .subs(exceptional_substitution)
        .subs(exceptional_solution)
    ),
    z,
)
E3_exceptional = det_exceptional.coeff_monomial(z**3)
assert sp.expand(
    coefficient(E3_exceptional, (3, 0, 0)) + 2 * X**2
) == 0
assert sp.expand(
    coefficient(E3_exceptional, (0, 3, 0)) + 2 * Y**2
) == 0

deep = {X: 0, Y: 0}
Mstar = L[4] + 2 * a**2 * c + a**2 * gamma - a * S
Astar = 4 * a * c + 2 * a * gamma + R - S
E2_exceptional = sp.expand(
    det_exceptional.coeff_monomial(z**2).subs(deep)
)
E1_exceptional = sp.expand(
    det_exceptional.coeff_monomial(z).subs(deep)
)
assert sp.expand(
    coefficient(E2_exceptional, (1, 0, 1)) - Mstar * Astar
) == 0
assert sp.expand(
    coefficient(E1_exceptional, (1, 0, 0))
    - Mstar * (a * Astar - Mstar)
) == 0
L0_sum_exceptional = sp.Matrix(
    [
        [L[0], L[1], L[2]],
        [L[3], L[4], L[5]],
        [a, a, c],
    ]
).subs(exceptional_solution).subs(deep)
Mstar_zero = {L[4]: -2 * a**2 * c - a**2 * gamma + a * S}
assert sp.expand(L0_sum_exceptional.det().subs(Mstar_zero)) == 0

print("nonbinary fixed-quadratic line-cover SymPy checks passed")
