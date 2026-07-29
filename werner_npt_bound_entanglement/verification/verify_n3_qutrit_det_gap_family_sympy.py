"""Symbolic audit of the one-parameter qutrit determinant-gap family."""

import sympy as sp


t = sp.symbols("t", positive=True)
eigenvalue = sp.symbols("eigenvalue")
denominator = 1 + t**2

# In the coordinate order recorded in
# notes/agent_n3_four_channel_ppt_schur.md, this is the exact invariant
# block of M_Q for
# u0=(|111>+t|222>)/sqrt(1+t^2),
# u1=(|100>+t|200>)/sqrt(1+t^2).
block = sp.Matrix(
    [
        [
            (8 * t**2 + 1) / denominator,
            -t / denominator,
            0,
            1 / denominator,
            0,
            -t / denominator,
        ],
        [
            -t / denominator,
            (t**2 + 2) / denominator,
            2 / denominator,
            -t / denominator,
            0,
            t**2 / denominator,
        ],
        [
            0,
            2 / denominator,
            2 * (2 * t**2 + 1) / denominator,
            0,
            0,
            0,
        ],
        [
            1 / denominator,
            -t / denominator,
            0,
            (2 * t**2 + 1) / denominator,
            2 * t**2 / denominator,
            -t / denominator,
        ],
        [
            0,
            0,
            0,
            2 * t**2 / denominator,
            2 * (t**2 + 2) / denominator,
            0,
        ],
        [
            -t / denominator,
            t**2 / denominator,
            0,
            -t / denominator,
            0,
            (t**2 + 8) / denominator,
        ],
    ]
)

characteristic = sp.cancel(block.charpoly(eigenvalue).as_expr())
quadratic_factor = (
    denominator**2 * eigenvalue**2
    - 4 * denominator**2 * eigenvalue
    + 8 * t**2
)
coefficient_field = sp.QQ.frac_field(t)
characteristic_poly = sp.Poly(
    characteristic, eigenvalue, domain=coefficient_field
)
quadratic_poly = sp.Poly(
    quadratic_factor, eigenvalue, domain=coefficient_field
)
quotient_poly, remainder_poly = characteristic_poly.div(quadratic_poly)
assert remainder_poly.is_zero
assert quotient_poly.degree() == 4

lambda_minus = 2 - 2 * sp.sqrt(1 + t**4) / denominator
assert sp.simplify(quadratic_factor.subs(eigenvalue, lambda_minus)) == 0

determinant_sum = 2 * t**2 / denominator**2
ratio = sp.simplify(lambda_minus / determinant_sum)
expected_ratio = (
    2 * denominator / (denominator + sp.sqrt(1 + t**4))
)
assert sp.simplify(ratio - expected_ratio) == 0
assert sp.limit(ratio, t, 0, dir="+") == 1

print(
    "verified: symbolic invariant block; quadratic spectral factor; "
    "exact determinant ratio; limiting coefficient one"
)
