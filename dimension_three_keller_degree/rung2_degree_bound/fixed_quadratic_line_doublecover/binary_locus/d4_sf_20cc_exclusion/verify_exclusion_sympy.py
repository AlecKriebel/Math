#!/usr/bin/env python3
"""Exact full-lower exclusion certificate for canonical D4-SF-20CC."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

BASE = (
    Path(__file__).resolve().parent.parent
    / "d4_sf_21c_exclusion"
    / "verify_exclusion_sympy.py"
)
spec = importlib.util.spec_from_file_location("d4_sf_base", BASE)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(base)

p, q, r, w = base.p, base.q, base.r, base.w
unit = sp.I

# Starting from z=(3+4i)/5 and rescaling q and the target components gives
# this Q(i)-rational representative of the frozen orbit.
X = p - q
Y = 5 * p - (3 - 4 * unit) * q
base.root = unit
base.h = sp.expand(X * Y)
base.P = sp.expand(base.h * p**2)
base.Q = sp.expand(base.h * q**2)
base.R = sp.expand(X**2 * ((4 - 3 * unit) * p + 5 * q))
base.alpha = base.jac2(base.Q, base.R)
base.beta = -base.jac2(base.P, base.R)
base.gamma = base.jac2(base.P, base.Q)


def main():
    gcd = sp.gcd(
        sp.gcd(
            sp.Poly(base.alpha, p, q, extension=unit),
            sp.Poly(base.beta, p, q, extension=unit),
        ),
        sp.Poly(base.gamma, p, q, extension=unit),
    )
    expected_gcd = sp.Poly(
        sp.expand(p * q * X**2), p, q, extension=unit
    )
    assert gcd.total_degree() == 4
    assert gcd.exquo(expected_gcd).as_expr().free_symbols == set()
    assert len(base.syzygy_basis(base.alpha, base.beta, base.gamma, 1)) == 2
    assert len(base.syzygy_basis(base.alpha, base.beta, base.gamma, 2)) == 4
    print("D4_SF_20CC_INCIDENCE_PASS")

    data = base.build_full_determinant()
    determinant = data["determinant"]
    x0, x1 = data["x"]
    y0, y1, y2, y3 = data["y"]
    variables = data["variables"]

    e6_general = base.coefficients(determinant.coeff_monomial(w**6), 6)
    high_x = tuple(
        value
        for exponent, value in e6_general.items()
        if exponent[2] == 3 and value != 0
    )
    x_basis = sp.groebner(
        high_x, x0, x1, extension=unit, order="lex"
    )
    expected_x = (x0**2, x0 * x1, x1**2)
    expected_x_basis = sp.groebner(
        expected_x, x0, x1, extension=unit, order="lex"
    )
    assert all(x_basis.reduce(value)[1] == 0 for value in expected_x)
    assert all(expected_x_basis.reduce(value)[1] == 0 for value in high_x)

    x_zero = {x0: 0, x1: 0}
    e6_xzero = tuple(value.subs(x_zero) for value in e6_general.values())
    matrix_y, rhs_y = sp.linear_eq_to_matrix(e6_xzero, variables)
    nonzero_rows = tuple(
        index
        for index in range(matrix_y.rows)
        if any(matrix_y[index, column] != 0 for column in range(matrix_y.cols))
        or rhs_y[index] != 0
    )
    reduced_matrix = matrix_y.extract(nonzero_rows, range(matrix_y.cols))
    reduced_rhs = rhs_y.extract(nonzero_rows, (0,))
    compatibility = []
    for left in reduced_matrix.T.nullspace():
        numerator = sp.factor(
            sp.together((left.T * reduced_rhs)[0]).as_numer_denom()[0],
            extension=unit,
        )
        if numerator != 0:
            compatibility.append(numerator)
    assert reduced_matrix.shape == (13, 18)
    assert reduced_matrix.rank() == 9
    assert len(compatibility) == 4

    y_basis = sp.groebner(
        compatibility, y0, y1, y2, y3, extension=unit, order="grevlex"
    )
    force_y0 = (
        y0
        + (sp.Rational(4, 13) + 7 * unit / 13) * y1
        - unit * y2 / 3
        + (sp.Rational(7, 39) - 4 * unit / 39) * y3
    ) ** 2
    force_y1 = (
        y1 + (-sp.Rational(4, 5) + 16 * unit / 15) * y3
    ) ** 2
    force_y2 = (y2 + y3) ** 2
    assert y_basis.reduce(force_y0)[1] == 0
    assert y_basis.reduce(force_y1)[1] == 0
    assert y_basis.reduce(force_y2)[1] == 0

    n = sp.symbols("n")
    contact = {
        x0: 0,
        x1: 0,
        y0: -(3 + unit) * n / 3,
        y1: 4 * (3 - 4 * unit) * n / 15,
        y2: -n,
        y3: n,
    }
    contact_residuals = tuple(
        sp.cancel(sp.expand(value.subs(contact)))
        for value in compatibility
    )
    assert all(value == 0 for value in contact_residuals)
    print("D4_SF_20CC_CONTACT_LINE_PASS")

    contact_determinant = sp.Poly(
        sp.expand(determinant.as_expr().subs(contact)), w
    )
    e6 = base.coefficients(contact_determinant.coeff_monomial(w**6), 6)
    e6_equations = tuple(e6.values())
    matrix6, rhs6 = sp.linear_eq_to_matrix(e6_equations, variables)
    sample = matrix6.subs({n: 1})
    rank_generic = sample.rank()
    pivot_columns = tuple(sample.rref()[1])
    pivot_rows = tuple(sample.T.rref()[1])
    assert rank_generic == 6
    assert len(pivot_rows) == len(pivot_columns) == rank_generic
    pivot_minor = sp.factor(
        matrix6.extract(pivot_rows, pivot_columns).det(), extension=unit
    )
    assert sp.cancel(pivot_minor / n).free_symbols == set()

    (
        _,
        _,
        generic_substitution,
        _,
        _,
    ) = base.solve_linear_by_pivots(
        e6_equations,
        variables,
        expected_rank=rank_generic,
        rank_probe={n: 1},
    )
    raw_e5 = base.coefficients(contact_determinant.coeff_monomial(w**5), 5)
    first_e5 = sp.cancel(raw_e5[(2, 1, 2)].subs(generic_substitution))
    second_e5 = sp.cancel(raw_e5[(1, 2, 2)].subs(generic_substitution))
    obstruction_constant = sp.Rational(128, 25) - 112 * unit / 75
    assert sp.expand(first_e5 - obstruction_constant * n**3) == 0
    assert sp.expand(second_e5 + obstruction_constant * n**3) == 0
    assert obstruction_constant != 0
    print("D4_SF_20CC_GENERIC_E5_PASS")

    zero_equations = tuple(value.subs({n: 0}) for value in e6_equations)
    zero_matrix, zero_rhs = sp.linear_eq_to_matrix(zero_equations, variables)
    zero_rank = zero_matrix.rank()
    (
        _,
        zero_solution,
        zero_substitution,
        _,
        _,
    ) = base.solve_linear_by_pivots(
        zero_equations, variables, expected_rank=zero_rank
    )
    assert zero_rank == 5

    raw_e4 = base.coefficients(contact_determinant.coeff_monomial(w**4), 4)
    first_e4 = sp.factor(
        raw_e4[(3, 0, 1)].subs({n: 0}).subs(zero_substitution),
        extension=unit,
    )
    second_e4 = sp.factor(
        raw_e4[(0, 3, 1)].subs({n: 0}).subs(zero_substitution),
        extension=unit,
    )
    b4 = data["b"][4]
    l33 = data["ell"][8]
    first_constant = sp.Rational(600, 169) + 1440 * unit / 169
    second_constant = -sp.Rational(384, 169) + 1512 * unit / 169
    assert sp.expand(first_e4 - first_constant * (b4 - unit * l33 / 3) ** 2) == 0
    assert sp.expand(
        second_e4
        - second_constant
        * (b4 + (-sp.Rational(4, 5) + 16 * unit / 15) * l33) ** 2
    ) == 0
    assert first_constant != 0 and second_constant != 0
    assert -sp.Rational(4, 5) + 7 * unit / 5 != 0

    descended = dict(zip(variables, zero_solution))
    forced = {b4: 0, l33: 0}
    nonbinary_quadratic = (
        data["a"][2],
        data["a"][4],
        data["a"][5],
        data["b"][2],
        data["b"][4],
        data["b"][5],
    )
    assert all(
        sp.factor(descended[variable].subs(forced), extension=unit) == 0
        for variable in nonbinary_quadratic
    )
    print("D4_SF_20CC_ZERO_E4_PASS")
    print("D4_SF_20CC_SYMPY_STRICT_PASS")


if __name__ == "__main__":
    main()
