#!/usr/bin/env python3
"""Strict exact verification of the interior two-contact exclusion."""

from __future__ import annotations

import contextlib
import importlib
import io

import sympy as sp
from sympy.polys.rings import ring


with contextlib.redirect_stdout(io.StringIO()):
    generic = importlib.import_module(
        "derive_delta2_11_interior_two_contacts"
    )
    fields = importlib.import_module(
        "derive_delta2_11_interior_two_contacts_fields"
    )
    lower = importlib.import_module(
        "derive_delta2_11_interior_two_contacts_u_minus1_lower"
    )

w = generic.w_symbol
a = generic.a_symbol
u = w**2
p = generic.p_symbol
q = generic.q_symbol

# The normal form and its residual stabilizer.
assert sp.expand(generic.h_symbol.subs({p: q, q: p}, simultaneous=True)) == (
    generic.h_symbol
)
R_A_D = (
    lambda A, D: 4 * w * A * p**3
    - 3 * (1 + u) * A * p**2 * q
    - 3 * (1 + u) * D * p * q**2
    + 4 * w * D * q**3
)
assert sp.expand(
    R_A_D(a, 1).subs({p: q, q: p}, simultaneous=True)
    - R_A_D(1, a)
) == 0
h_for = lambda parameter: sp.expand(
    (p - parameter * q) * (parameter * p - q)
)
R_for = lambda parameter, ratio: (
    4 * parameter * ratio * p**3
    - 3 * (1 + parameter**2) * ratio * p**2 * q
    - 3 * (1 + parameter**2) * p * q**2
    + 4 * parameter * q**3
)
assert sp.cancel(h_for(1 / w) - h_for(w) / u) == 0
assert sp.cancel(u * R_for(1 / w, a) - R_for(w, a)) == 0
assert sp.expand(
    h_for(w).subs(p, -p) + h_for(-w)
) == 0
assert sp.expand(
    -R_for(w, a).subs(p, -p) - R_for(-w, -a)
) == 0
assert sp.factor(
    sp.gcd(
        sp.gcd(generic.alpha_symbol, generic.beta_symbol),
        generic.gamma_symbol,
    )
) == p * q

EL = a * w**3 - 3 * a * w - 3 * u + 1
EM = -3 * a * u + a + w**3 - 3 * w
kappa_minus = u - 4 * w + 1
kappa_plus = u + 4 * w + 1

# Generic-basis stratification.
b = -36 * w**5 - 8 * w**3 - 36 * w
c = 7 * w**6 - 27 * w**4 - 27 * w**2 + 7
assert sp.expand(generic.K1 - (a * b + c)) == 0
assert sp.expand(generic.K2 - (a * c + b)) == 0

Sminus = c + b
Splus = c - b
assert sp.expand(
    sp.resultant(generic.K1, generic.K2, a) + Sminus * Splus
) == 0
for polynomial in (Sminus, Splus):
    primitive_content, _primitive = sp.Poly(polynomial, w).primitive()
    assert primitive_content == 1
    assert sp.Poly(polynomial, w).is_irreducible

G = 7 * w**8 - 156 * w**6 + 66 * w**4 - 12 * w**2 + 15
H = 15 * w**8 - 12 * w**6 + 66 * w**4 - 156 * w**2 + 7
denominator = 4 * (3 * u - 4 * w + 3) * (3 * u + 4 * w + 3)
assert sp.cancel(EL.subs(a, -c / b) - G / denominator) == 0
assert sp.cancel(EM.subs(a, -c / b) - H / (w * denominator)) == 0
assert sp.gcd(sp.Poly(b / (-4 * w), w), sp.Poly(c, w)) == 1

W4 = 5 * w**4 - 6 * w**2 + 5
expected_q_gcd = (
    w**6
    * (w - 1) ** 8
    * (w + 1) ** 8
    * (u + 1) ** 5
    * kappa_minus**4
    * kappa_plus**4
    * W4**2
)
assert sp.expand(sp.gcd_list(generic.resultants) - expected_q_gcd) == 0


def algebraic_polynomial(expression, modulus):
    """Map Q[w,a] to (Q[w]/modulus)[a] exactly."""

    field = sp.QQ.alg_field_from_poly(sp.Poly(modulus, w), alias="w")
    generator = field.convert(field.ext)
    polynomial_ring, aa = ring("a", field)
    answer = polynomial_ring.zero
    polynomial = sp.Poly(sp.expand(expression), a, w, domain=sp.QQ)
    for (a_degree, w_degree), coefficient in polynomial.terms():
        answer += (
            field.convert(coefficient)
            * generator**w_degree
            * aa**a_degree
        )
    return answer


def common_gcd(expressions, modulus):
    images = [algebraic_polynomial(value, modulus) for value in expressions]
    answer = images[0]
    for value in images[1:]:
        answer = answer.gcd(value)
    return answer.monic()


u_minus_one_gcd = common_gcd(generic.residuals, u + 1)
assert u_minus_one_gcd == algebraic_polynomial(a**2 + 1, u + 1).monic()
assert sp.rem(
    sp.Poly(EL.subs(a, -w), w),
    sp.Poly(u + 1, w),
).is_zero
assert sp.rem(
    sp.Poly(EM.subs(a, w), w),
    sp.Poly(u + 1, w),
).is_zero

quartic_common = 10 * a**2 + (-5 * w**3 + 11 * w) * a + 10
quartic_gcd = common_gcd(generic.residuals, W4)
assert quartic_gcd == algebraic_polynomial(quartic_common, W4).monic()
a1 = (3 * u - 5) / (4 * w)
a2 = (3 - 5 * u) / (4 * w)
factor_residual = sp.cancel(
    quartic_common - 10 * (a - a1) * (a - a2)
)
factor_numerator, factor_denominator = factor_residual.as_numer_denom()
assert sp.rem(factor_numerator, W4, w) == 0
assert sp.gcd(sp.Poly(factor_denominator, w), sp.Poly(W4, w)) == 1
for expression in (EM.subs(a, a1), EL.subs(a, a2)):
    numerator, denominator_value = sp.cancel(expression).as_numer_denom()
    assert sp.rem(numerator, W4, w) == 0
    assert sp.gcd(
        sp.Poly(denominator_value, w), sp.Poly(W4, w)
    ) == 1

# The alternate E7 basis is regular away from w(u+1)=0.
alternate_determinant = sp.factor(generic.pivot_matrix.det())
assert sp.expand(
    alternate_determinant
    - 10368
    * w**3
    * (w - 1) ** 2
    * (w + 1) ** 2
    * (u + 1)
    * EL**2
    * EM**2
) == 0

P16 = fields.P16
expected_B_gcd = (
    59049
    * w
    * kappa_minus**2
    * kappa_plus**2
    * W4**2
    * P16
)
assert sp.expand(sp.gcd_list(generic.B_resultants) - expected_B_gcd) == 0
primitive_content, _primitive = sp.Poly(P16, w).primitive()
assert primitive_content == 1
assert sp.Poly(P16, w).is_irreducible
assert sp.cancel(generic.a_B_reduced - fields.a_P16) == 0

# Fresh exact-field pivots, with no specialization of a singular basis.
assert [result["contact_rank"] for result in fields.field_results] == [
    4,
    4,
    3,
    5,
]
assert all(result["constant_rank"] == 5 for result in fields.field_results)
assert [result["outcome"] for result in fields.field_results] == [
    "contact rank 4, non-Veronese",
    "contact rank 4, non-Veronese",
    "contact rank 3, unique Veronese GENUINE E5 SURVIVOR",
    "contact rank 5",
]

# The sole full-lower survivor has singular linear part.
assert lower.E3.is_zero
assert all(
    sp.Poly(lower.reduced(lower.E[degree]), lower.r).is_zero
    for degree in (2, 1)
)
assert sp.simplify(
    lower.Ldone[:, 0] - lower.uc[2] * lower.Ldone[:, 2]
) == sp.zeros(3, 1)
assert sp.expand(lower.Ldone.det()) == 0

print(
    "PASS exact two-contact generic/alternate charts, algebraic pivots, "
    "and full lower singularity"
)
