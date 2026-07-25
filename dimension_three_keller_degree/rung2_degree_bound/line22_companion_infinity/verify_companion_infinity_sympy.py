#!/usr/bin/env python3
"""Exact certificates for the line-(2,2) companion-at-infinity boundary."""

from __future__ import annotations

if not __debug__:
    raise RuntimeError("verification requires assertions; do not use -O")

from itertools import product

import sympy as sp


x, y, z = sp.symbols("x y z")
t, a = sp.symbols("t a")
p, q = x**2, y * z
variables = (x, y, z)


def monomials(degree: int) -> tuple[sp.Expr, ...]:
    return tuple(
        x**i * y**j * z ** (degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def form(prefix: str, degree: int) -> tuple[sp.Expr, tuple[sp.Symbol, ...]]:
    coefficients = sp.symbols(f"{prefix}0:{len(monomials(degree))}")
    return (
        sum(
            coefficient * monomial
            for coefficient, monomial in zip(
                coefficients, monomials(degree)
            )
        ),
        coefficients,
    )


def weighted_coefficient(
    linear: sp.Matrix,
    quadratic: sp.Matrix,
    cubic: sp.Matrix,
    quartic: sp.Matrix,
    weight: int,
) -> sp.Expr:
    matrices = tuple(
        vector.jacobian(variables)
        for vector in (linear, quadratic, cubic, quartic)
    )
    result = 0
    for choices in product(range(4), repeat=3):
        if sum(choices) != weight:
            continue
        result += sp.Matrix.vstack(
            *(matrices[choices[row]].row(row) for row in range(3))
        ).det()
    return sp.expand(result)


def coefficient_matrix(
    expression: sp.Expr,
    unknowns: tuple[sp.Symbol, ...],
    degree: int,
) -> sp.Matrix:
    polynomial = sp.Poly(sp.expand(expression), *variables)
    equations = [
        polynomial.coeff_monomial(monomial)
        for monomial in monomials(degree)
    ]
    matrix, right = sp.linear_eq_to_matrix(equations, unknowns)
    assert right == sp.zeros(len(equations), 1)
    return matrix


def triplet_vector(
    first: sp.Expr, second: sp.Expr, third: sp.Expr
) -> sp.Matrix:
    entries = []
    for expression, degree in ((first, 3), (second, 3), (third, 2)):
        polynomial = sp.Poly(sp.expand(expression), *variables)
        entries.extend(
            polynomial.coeff_monomial(monomial)
            for monomial in monomials(degree)
        )
    return sp.Matrix(entries)


raw_u, raw_uc = form("rawU", 3)
raw_v, raw_vc = form("rawV", 3)
raw_w, raw_wc = form("rawW", 2)
raw_unknowns = raw_uc + raw_vc + raw_wc
normal_companion = x * q


def raw_e7_matrix(first: sp.Expr, second: sp.Expr) -> sp.Matrix:
    quartic = sp.Matrix([first, second, 0])
    cubic = sp.Matrix([raw_u, raw_v, normal_companion])
    quadratic = sp.Matrix([0, 0, raw_w])
    e7 = weighted_coefficient(
        sp.zeros(3, 1), quadratic, cubic, quartic, 7
    )
    return coefficient_matrix(e7, raw_unknowns, 7)


base_kernel = (
    (x**3, 0, 0),
    (x * q, 0, 0),
    (0, x**3, 0),
    (0, x * q, 0),
    (0, 0, p),
    (0, 0, q),
)


def certify_kernel(
    matrix: sp.Matrix,
    directions: tuple[tuple[sp.Expr, sp.Expr, sp.Expr], ...],
) -> None:
    kernel = sp.Matrix.hstack(
        *(triplet_vector(*direction) for direction in directions)
    )
    assert matrix * kernel == sp.zeros(matrix.rows, kernel.cols)
    # A constant minor proves independence at every parameter value.
    rows = (0, 4, 10, 14, 17, 18, 20, 24)
    assert sp.expand(kernel.extract(rows, range(8)).det() - 4) == 0


# Both outer critical points finite.  Their unordered pair is normalized to
# {t,1}; t=1 is degenerate, and t=-2,-1/2 form one residual resonance orbit.
finite_first = (p - t * q) ** 2
finite_second = (p - q) ** 2
finite_raw = raw_e7_matrix(finite_first, finite_second)
finite_rows = (
    1, 2, 3, 5, 6, 7, 8, 9, 11, 13, 16, 17, 18, 19, 23, 25, 31, 32
)
finite_columns = (
    1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 15, 16, 17, 18, 19, 23, 25
)
finite_minor = sp.factor(
    finite_raw.extract(finite_rows, finite_columns).det()
)
assert sp.expand(
    finite_minor
    + 347892350976
    * (t - 1) ** 10
    * (t + 2) ** 4
    * (2 * t + 1) ** 4
) == 0
finite_directions = base_kernel + (
    (
        -2 * t * y * (p - t * q),
        -2 * y * (p - q),
        x * y,
    ),
    (
        -2 * t * z * (p - t * q),
        -2 * z * (p - q),
        x * z,
    ),
)
certify_kernel(finite_raw, finite_directions)
assert raw_e7_matrix(
    finite_first.subs(t, -2), finite_second
).rank() == 14
assert raw_e7_matrix(
    finite_first.subs(t, sp.Rational(-1, 2)), finite_second
).rank() == 14
assert raw_e7_matrix(
    finite_first.subs(t, 1), finite_second
).rank() == 8


# One outer critical point is at infinity.  The constant rank certificate
# works for every a, simultaneously covering the residual a=0 and a!=0
# orbits.
outer_first = (p - a * q) ** 2
outer_second = q**2
outer_raw = raw_e7_matrix(outer_first, outer_second)
outer_rows = (
    1, 2, 3, 5, 6, 7, 8, 9, 11, 13, 17, 18, 23, 25, 30, 31, 32, 33
)
outer_columns = finite_columns
assert (
    outer_raw.extract(outer_rows, outer_columns).det()
    == -5566277615616
)
outer_directions = base_kernel + (
    (
        -2 * a * y * (p - a * q),
        2 * y * q,
        x * y,
    ),
    (
        -2 * a * z * (p - a * q),
        2 * z * q,
        x * z,
    ),
)
certify_kernel(outer_raw, outer_directions)


# After affine source translations and target shears, the complete
# nonresonant kernel has this normal form.
C, w0, w1 = sp.symbols("C w0 w1")
normal_cubic = sp.Matrix([0, C * x**3, normal_companion])
normal_w = w0 * p + w1 * q
assert weighted_coefficient(
    sp.zeros(3, 1),
    sp.Matrix([0, 0, normal_w]),
    normal_cubic,
    sp.Matrix([finite_first, finite_second, 0]),
    7,
) == 0
assert weighted_coefficient(
    sp.zeros(3, 1),
    sp.Matrix([0, 0, normal_w]),
    normal_cubic,
    sp.Matrix([outer_first, outer_second, 0]),
    7,
) == 0


# Complete E6 reconstruction.
quadratic_first, quadratic_first_coefficients = form("quadA", 2)
quadratic_second, quadratic_second_coefficients = form("quadB", 2)
linear_coefficients = sp.symbols("ell0:9")
linear_matrix = sp.Matrix(3, 3, linear_coefficients)
linear = linear_matrix * sp.Matrix([x, y, z])
quadratic = sp.Matrix(
    [quadratic_first, quadratic_second, normal_w]
)
lower_unknowns = (
    quadratic_first_coefficients
    + quadratic_second_coefficients
    + linear_coefficients
)
forced_columns = (1, 2, 3, 5, 7, 8, 9, 11, 19, 20)
unforced_columns = tuple(
    index for index in range(21) if index not in forced_columns
)
forced_variables = tuple(lower_unknowns[index] for index in forced_columns)
e6_zero_substitution = {variable: 0 for variable in forced_variables}


def e6_matrix(first: sp.Expr, second: sp.Expr) -> tuple[sp.Expr, sp.Matrix]:
    quartic = sp.Matrix([first, second, 0])
    e6 = weighted_coefficient(
        linear, quadratic, normal_cubic, quartic, 6
    )
    return e6, coefficient_matrix(e6, lower_unknowns, 6)


finite_e6, finite_e6_matrix = e6_matrix(finite_first, finite_second)
assert finite_e6_matrix[:, unforced_columns] == sp.zeros(28, 11)
finite_e6_rows = (1, 2, 3, 5, 7, 8, 11, 13, 17, 18)
assert sp.expand(
    finite_e6_matrix.extract(finite_e6_rows, forced_columns).det()
    + 1048576
    * (t - 1) ** 6
    * (t + 2) ** 2
    * (2 * t + 1) ** 2
) == 0
assert sp.expand(finite_e6.subs(e6_zero_substitution)) == 0

outer_e6, outer_e6_matrix = e6_matrix(outer_first, outer_second)
assert outer_e6_matrix[:, unforced_columns] == sp.zeros(28, 11)
outer_e6_rows = (1, 2, 3, 5, 7, 8, 17, 18, 23, 25)
assert (
    outer_e6_matrix.extract(outer_e6_rows, forced_columns).det()
    == -4194304
)
assert sp.expand(outer_e6.subs(e6_zero_substitution)) == 0


# E5 then kills the remaining entries in columns two and three of L.
remaining_linear = (
    linear_coefficients[1],
    linear_coefficients[2],
    linear_coefficients[4],
    linear_coefficients[5],
)


def reduced_e5(first: sp.Expr, second: sp.Expr) -> sp.Expr:
    return sp.expand(
        weighted_coefficient(
            linear,
            quadratic,
            normal_cubic,
            sp.Matrix([first, second, 0]),
            5,
        ).subs(e6_zero_substitution)
    )


finite_e5 = reduced_e5(finite_first, finite_second)
finite_e5_expected = -2 * (
    2 * linear_coefficients[1] * x**4 * y
    - linear_coefficients[1] * x**2 * y**2 * z
    - linear_coefficients[1] * y**3 * z**2
    - 2 * linear_coefficients[2] * x**4 * z
    + linear_coefficients[2] * x**2 * y * z**2
    + linear_coefficients[2] * y**2 * z**3
    + t**2 * linear_coefficients[4] * y**3 * z**2
    + t * linear_coefficients[4] * x**2 * y**2 * z
    - 2 * linear_coefficients[4] * x**4 * y
    - t**2 * linear_coefficients[5] * y**2 * z**3
    - t * linear_coefficients[5] * x**2 * y * z**2
    + 2 * linear_coefficients[5] * x**4 * z
)
assert sp.expand(finite_e5 - finite_e5_expected) == 0
finite_e5_matrix = coefficient_matrix(finite_e5, remaining_linear, 5)
finite_e5_rows = (1, 2, 7, 8)
assert sp.expand(
    finite_e5_matrix.extract(finite_e5_rows, range(4)).det()
    - 64 * (t - 1) ** 2
) == 0

outer_e5 = reduced_e5(outer_first, outer_second)
outer_e5_expected = 2 * (
    -a**2 * linear_coefficients[4] * y**3 * z**2
    + a**2 * linear_coefficients[5] * y**2 * z**3
    - a * linear_coefficients[4] * x**2 * y**2 * z
    + a * linear_coefficients[5] * x**2 * y * z**2
    + linear_coefficients[1] * y**3 * z**2
    - linear_coefficients[2] * y**2 * z**3
    + 2 * linear_coefficients[4] * x**4 * y
    - 2 * linear_coefficients[5] * x**4 * z
)
assert sp.expand(outer_e5 - outer_e5_expected) == 0
outer_e5_matrix = coefficient_matrix(outer_e5, remaining_linear, 5)
outer_e5_rows = (1, 2, 17, 18)
assert outer_e5_matrix.extract(outer_e5_rows, range(4)).det() == 64

singular_substitution = dict(e6_zero_substitution)
singular_substitution.update(
    {variable: 0 for variable in remaining_linear}
)
assert sp.expand(linear_matrix.det().subs(singular_substitution)) == 0


# ---------------------------------------------------------------------------
# The unique finite-pair resonance t=-2 (equivalently t=-1/2 after swapping
# the unordered outer critical points).
# ---------------------------------------------------------------------------
resonance_first = (p + 2 * q) ** 2
resonance_second = (p - q) ** 2
resonance_raw = raw_e7_matrix(resonance_first, resonance_second)
assert resonance_raw.rank() == 14

resonance_C = sp.symbols("resonanceC")
resonance_w = sp.symbols("resonanceW0:6")
rw0, rw1, rw2, rw3, rw4, rw5 = resonance_w
resonance_normal_directions = (
    (0, resonance_C * x**3, 0),
    (0, 0, rw0 * p),
    (0, -6 * rw1 * x**2 * y, rw1 * x * y),
    (0, -6 * rw2 * x**2 * z, rw2 * x * z),
    (0, -6 * rw3 * x * y**2, rw3 * y**2),
    (0, 0, rw4 * q),
    (0, -6 * rw5 * x * z**2, rw5 * z**2),
)
resonance_cubic = sp.Matrix(
    [
        0,
        resonance_C * x**3
        - 6 * rw1 * x**2 * y
        - 6 * rw2 * x**2 * z
        - 6 * rw3 * x * y**2
        - 6 * rw5 * x * z**2,
        normal_companion,
    ]
)
resonance_w_form = (
    rw0 * p
    + rw1 * x * y
    + rw2 * x * z
    + rw3 * y**2
    + rw4 * q
    + rw5 * z**2
)
assert weighted_coefficient(
    sp.zeros(3, 1),
    sp.Matrix([0, 0, resonance_w_form]),
    resonance_cubic,
    sp.Matrix([resonance_first, resonance_second, 0]),
    7,
) == 0

# Five legal gauge directions (two target shears and three affine source
# translations) plus the seven displayed normal directions span the full
# twelve-dimensional raw kernel.
resonance_directions = (
    (x * q, 0, 0),
    (0, x * q, 0),
    (4 * x * (p + 2 * q), 4 * x * (p - q), q),
    (4 * z * (p + 2 * q), -2 * z * (p - q), x * z),
    (4 * y * (p + 2 * q), -2 * y * (p - q), x * y),
    (0, x**3, 0),
    (0, 0, p),
    (0, -6 * x**2 * y, x * y),
    (0, -6 * x**2 * z, x * z),
    (0, -6 * x * y**2, y**2),
    (0, 0, q),
    (0, -6 * x * z**2, z**2),
)
resonance_kernel = sp.Matrix.hstack(
    *(triplet_vector(*direction) for direction in resonance_directions)
)
assert resonance_raw * resonance_kernel == sp.zeros(36, 12)
resonance_kernel_rows = (0, 1, 2, 4, 10, 11, 12, 13, 14, 15, 20, 24)
assert (
    resonance_kernel.extract(resonance_kernel_rows, range(12)).det()
    == 82944
)

resonance_quadratic = sp.Matrix(
    [quadratic_first, quadratic_second, resonance_w_form]
)
resonance_quartic = sp.Matrix(
    [resonance_first, resonance_second, 0]
)
resonance_e6 = weighted_coefficient(
    linear,
    resonance_quadratic,
    resonance_cubic,
    resonance_quartic,
    6,
)
resonance_e6_polynomial = sp.Poly(resonance_e6, *variables)
resonance_e6_equations = [
    resonance_e6_polynomial.coeff_monomial(monomial)
    for monomial in monomials(6)
]
resonance_e6_matrix, resonance_e6_right = sp.linear_eq_to_matrix(
    resonance_e6_equations, lower_unknowns
)
assert resonance_e6_matrix.rank() == 8

# Exact left-kernel compatibility includes the decisive square chain.
resonance_e6_compatibility = [
    sp.factor((vector.T * resonance_e6_right)[0])
    for vector in resonance_e6_matrix.T.nullspace()
]


def has_associate(
    expressions: list[sp.Expr], target: sp.Expr
) -> bool:
    for expression in expressions:
        if expression == 0:
            continue
        quotient = sp.cancel(expression / target)
        if quotient.is_Rational and quotient != 0:
            return True
    return False


resonance_K = resonance_C + 4 * rw0 - 2 * rw4
for required in (
    rw3**2,
    rw5**2,
    resonance_K * rw3 - rw1**2,
    resonance_K * rw5 - rw2**2,
):
    assert has_associate(resonance_e6_compatibility, required)

# Over C, the compatibility equations force rw3=rw5=rw1=rw2=0.
resonance_top_substitution = {
    rw1: 0,
    rw2: 0,
    rw3: 0,
    rw5: 0,
}
resonance_reduced_e6 = sp.expand(
    resonance_e6.subs(resonance_top_substitution)
)
resonance_reduced_matrix = coefficient_matrix(
    resonance_reduced_e6, lower_unknowns, 6
)
resonance_forced_columns = (1, 2, 3, 5, 7, 8, 9, 11)
resonance_forced_rows = (1, 2, 3, 5, 7, 8, 11, 13)
assert (
    resonance_reduced_matrix.extract(
        resonance_forced_rows, resonance_forced_columns
    ).det()
    == 5308416
)
resonance_e6_solution = {
    quadratic_first_coefficients[1]: 0,
    quadratic_first_coefficients[2]: 0,
    quadratic_first_coefficients[3]: 0,
    quadratic_first_coefficients[5]: 0,
    quadratic_second_coefficients[1]: -6 * linear_coefficients[7],
    quadratic_second_coefficients[2]: -6 * linear_coefficients[8],
    quadratic_second_coefficients[3]: 0,
    quadratic_second_coefficients[5]: 0,
}
assert sp.expand(
    resonance_reduced_e6.subs(resonance_e6_solution)
) == 0

resonance_e5 = sp.expand(
    weighted_coefficient(
        linear,
        resonance_quadratic,
        resonance_cubic,
        resonance_quartic,
        5,
    )
    .subs(resonance_top_substitution)
    .subs(resonance_e6_solution)
)
resonance_e5_matrix, resonance_e5_right = sp.linear_eq_to_matrix(
    [
        sp.Poly(resonance_e5, *variables).coeff_monomial(monomial)
        for monomial in monomials(5)
    ],
    remaining_linear,
)
assert resonance_e5_matrix.rank() == 4
resonance_e5_rows = (1, 2, 7, 8)
assert (
    resonance_e5_matrix.extract(resonance_e5_rows, range(4)).det()
    == 576
)
resonance_e5_pivot_solution = {
    linear_coefficients[1]:
        -2 * resonance_K * linear_coefficients[7],
    linear_coefficients[2]:
        -2 * resonance_K * linear_coefficients[8],
    linear_coefficients[4]:
        -5 * resonance_K * linear_coefficients[7],
    linear_coefficients[5]:
        -5 * resonance_K * linear_coefficients[8],
}
resonance_e5_residual = sp.expand(
    resonance_e5.subs(resonance_e5_pivot_solution)
)
assert sp.expand(
    resonance_e5_residual
    - 36
    * resonance_K
    * (
        linear_coefficients[7] * y**3 * z**2
        - linear_coefficients[8] * y**2 * z**3
    )
) == 0

# If K!=0, the residual kills ell32,ell33; if K=0 they may remain.
# In both branches, the last two columns of the linear part are dependent.
resonance_k_nonzero = dict(resonance_e5_pivot_solution)
resonance_k_nonzero.update(
    {linear_coefficients[7]: 0, linear_coefficients[8]: 0}
)
assert sp.expand(
    linear_matrix.det().subs(resonance_k_nonzero)
) == 0
resonance_k_zero = {
    resonance_C: -4 * rw0 + 2 * rw4,
    linear_coefficients[1]: 0,
    linear_coefficients[2]: 0,
    linear_coefficients[4]: 0,
    linear_coefficients[5]: 0,
}
assert sp.expand(linear_matrix.det().subs(resonance_k_zero)) == 0

print("line-(2,2) companion-at-infinity SymPy certificates passed")
