#!/usr/bin/env python3
"""Dependency-free hostile audit of the triple-root gamma=0 reduction.

The sparse Laurent-polynomial arithmetic kernel comes from the earlier
hostile yz^2 audit.  No equation or coefficient selection is imported
from the supplied SymPy verifier.
"""

from __future__ import annotations

from fractions import Fraction
import importlib.util
from pathlib import Path
import sys


if not __debug__:
    raise SystemExit("refusing optimized Python: fail-closed checks required")


def fail(message):
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def check(condition, message):
    if not condition:
        fail(message)


ARITHMETIC_PATH = (
    Path(__file__).resolve().parent.parent
    / "audit_vertical_triple_yz2_gamma0_ell0"
    / "verify_vertical_triple_yz2_sparse.py"
)
check(ARITHMETIC_PATH.is_file(), "sparse arithmetic kernel missing")
spec = importlib.util.spec_from_file_location(
    "vertical_gamma0_sparse_arithmetic",
    ARITHMETIC_PATH,
)
check(spec is not None and spec.loader is not None, "cannot load arithmetic kernel")
sp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sp)


ALPHA = sp.variable("alpha")
U_PARAMETER = sp.variable("u")
V_PARAMETER = sp.variable("v")
W_GENERAL = sp.mul(
    sp.Z,
    sp.add(
        sp.mul(U_PARAMETER, sp.X),
        sp.mul(V_PARAMETER, sp.Y),
        sp.mul(sp.variable("w"), sp.Z),
    ),
)

Q_C = sp.add(
    sp.power(sp.X, 3),
    sp.mul(sp.power(sp.Y, 2), sp.Z),
    sp.mul(ALPHA, sp.mul(sp.X, sp.power(sp.Z, 2))),
)
Q_B = sp.add(
    sp.power(sp.X, 3),
    sp.mul(sp.X, sp.mul(sp.Y, sp.Z)),
)
Q_E = sp.add(
    sp.power(sp.X, 3),
    sp.mul(sp.Y, sp.power(sp.Z, 2)),
)


def set_zero(poly, name):
    position = sp.INDEX[name]
    return sp.clean(
        {
            exponent: coefficient
            for exponent, coefficient in poly.items()
            if exponent[position] == 0
        }
    )


def jacobian_triple(first, second, third):
    return sp.det3(sp.jacobian((first, second, third)))


def build_forms(q, w_form=W_GENERAL):
    p = sp.power(sp.Z, 4)
    capital_q = sp.mul(sp.Z, q)
    r = sp.power(sp.Z, 3)
    first_cubic = sp.add(
        sp.scale(sp.mul(sp.Z, w_form), Fraction(4, 3)),
        sp.mul(sp.S, q),
    )
    h2 = (sp.A, sp.B_GENERAL, w_form)
    h3 = (first_cubic, sp.V_GENERAL, r)
    h4 = (p, capital_q, {})
    return p, capital_q, r, first_cubic, h2, h3, h4


def build_raw_determinant(q, w_form=W_GENERAL):
    _, _, _, _, h2, h3, h4 = build_forms(q, w_form)
    return sp.determinant_of_jets(
        sp.linear_matrix(),
        h2,
        h3,
        h4,
    )


def exterior_e6(q, w_form=W_GENERAL):
    p, capital_q, r, first_cubic, _, _, _ = build_forms(q, w_form)
    l3 = sp.add(
        sp.mul(sp.variable("l6"), sp.X),
        sp.mul(sp.variable("l7"), sp.Y),
        sp.mul(sp.variable("l8"), sp.Z),
    )
    return sp.add(
        jacobian_triple(p, capital_q, l3),
        jacobian_triple(first_cubic, capital_q, w_form),
        jacobian_triple(p, sp.V_GENERAL, w_form),
        jacobian_triple(sp.A, capital_q, r),
        jacobian_triple(first_cubic, sp.V_GENERAL, r),
        jacobian_triple(p, sp.B_GENERAL, r),
    )


CHARTS = {
    "quadratic-y": {
        "q": Q_C,
        "combination": (
            (Fraction(1, 3), (3, 1, 2)),
            (Fraction(1), (0, 3, 3)),
        ),
        "expected_u": Fraction(8, 3),
    },
    "mixed-xy": {
        "q": Q_B,
        "combination": (
            (Fraction(-1, 9), (4, 0, 2)),
            (Fraction(-1, 3), (2, 1, 3)),
            (Fraction(1), (0, 2, 4)),
        ),
        "expected_u": Fraction(-4, 9),
    },
    "linear-y": {
        "q": Q_E,
        "combination": (
            (Fraction(1, 3), (3, 0, 3)),
            (Fraction(1), (0, 1, 5)),
        ),
        "expected_u": Fraction(4, 3),
    },
}


def linear_combination(coefficient_map, terms):
    return sp.add(
        *(
            sp.scale(coefficient_map.get(monomial, {}), scalar)
            for scalar, monomial in terms
        )
    )


def audit_chart(label, data):
    q = data["q"]
    raw = build_raw_determinant(q)
    check(sp.all_zero_in_degree(raw, 8), f"{label}: E8 survives")
    check(sp.all_zero_in_degree(raw, 7), f"{label}: E7 survives")
    raw_e6 = sp.coefficients_of_source_degree(raw, 6)

    # Independently reconstruct the entire E6 homogeneous identity by
    # exterior multilinearity and compare every coefficient.
    exterior = exterior_e6(q)
    exterior_coefficients = sp.coefficients_of_source_degree(exterior, 6)
    check(
        exterior_coefficients == raw_e6,
        f"{label}: raw determinant and exterior E6 disagree",
    )
    check(
        all(
            sum(exponent[position] for position in sp.SOURCE) == 6
            for exponent in exterior
        ),
        f"{label}: exterior expression is not homogeneous of degree six",
    )

    expected_v = sp.scale(sp.mul(sp.S, V_PARAMETER), -3)
    actual_v = raw_e6.get((5, 0, 1), {})
    check(actual_v == expected_v, f"{label}: [x^5 z] obstruction mismatch")

    after_v = {
        monomial: set_zero(coefficient, "v")
        for monomial, coefficient in raw_e6.items()
    }
    actual_u = linear_combination(after_v, data["combination"])
    expected_u = sp.scale(
        sp.mul(sp.S, U_PARAMETER),
        data["expected_u"],
    )
    check(actual_u == expected_u, f"{label}: u obstruction mismatch")

    # Normal-form negative control: doubling the normalized x^3 coefficient
    # must invalidate both claimed coefficients.  This exercises the raw
    # determinant path rather than merely mutating an expected constant.
    mutated_q = sp.add(q, sp.power(sp.X, 3))
    mutated = build_raw_determinant(mutated_q)
    mutated_e6 = sp.coefficients_of_source_degree(mutated, 6)
    mutated_v = mutated_e6.get((5, 0, 1), {})
    mutated_after_v = {
        monomial: set_zero(coefficient, "v")
        for monomial, coefficient in mutated_e6.items()
    }
    mutated_u = linear_combination(mutated_after_v, data["combination"])
    check(
        mutated_v != expected_v,
        f"{label}: x^3-normalization negative control missed v identity",
    )
    check(
        mutated_u != expected_u,
        f"{label}: x^3-normalization negative control missed u identity",
    )

    # Scope guard: adding W0=x^2 exits gamma=0.  At least one decisive
    # identity must change, preventing accidental promotion of this checker
    # to the gamma != 0 branch.
    gamma_mutation = sp.add(W_GENERAL, sp.power(sp.X, 2))
    gamma_raw = build_raw_determinant(q, w_form=gamma_mutation)
    gamma_e6 = sp.coefficients_of_source_degree(gamma_raw, 6)
    gamma_v = gamma_e6.get((5, 0, 1), {})
    gamma_after_v = {
        monomial: set_zero(coefficient, "v")
        for monomial, coefficient in gamma_e6.items()
    }
    gamma_u = linear_combination(gamma_after_v, data["combination"])
    check(
        gamma_v != expected_v or gamma_u != expected_u,
        f"{label}: gamma-boundary mutation was not detected",
    )

    print(
        f"{label}: [x^5z]E6=-3*s*v; "
        f"u-combination={data['expected_u']}*s*u; "
        f"raw/exterior and negative controls passed"
    )


def main():
    for label, data in CHARTS.items():
        audit_chart(label, data)
    print("PASS: independent sparse audit of triple gamma=0 reduction")


if __name__ == "__main__":
    main()
