#!/usr/bin/env python3
"""Dependency-free hostile audit of the triple-root gamma != 0 branch.

The candidate SymPy checker is neither imported nor executed here. The raw
determinant and a separate exterior E6 expansion are reconstructed with the
repository's dependency-free sparse polynomial arithmetic.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
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
check(
    hashlib.sha256(ARITHMETIC_PATH.read_bytes()).hexdigest()
    == "9ad87c003bc0ce00e86b8c863b53af356aeec900d487c93999981908e28528e9",
    "sparse arithmetic kernel hash mismatch",
)
spec = importlib.util.spec_from_file_location(
    "vertical_gamma_nonzero_sparse_arithmetic",
    ARITHMETIC_PATH,
)
check(spec is not None and spec.loader is not None, "cannot load arithmetic kernel")
sp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sp)


# The sparse kernel already reserves the unused parameter name k. It is
# deliberately repurposed locally as gamma; no candidate formula is imported.
GAMMA = sp.variable("k")
ALPHA = sp.variable("alpha")
U_PARAMETER = sp.variable("u")
V_PARAMETER = sp.variable("v")
W_PARAMETER = sp.variable("w")

W_GENERAL = sp.add(
    sp.mul(GAMMA, sp.power(sp.X, 2)),
    sp.mul(
        sp.Z,
        sp.add(
            sp.mul(U_PARAMETER, sp.X),
            sp.mul(V_PARAMETER, sp.Y),
            sp.mul(W_PARAMETER, sp.Z),
        ),
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


def contains_parameter(poly, name):
    position = sp.INDEX[name]
    return any(exponent[position] for exponent in poly)


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
    return sp.determinant_of_jets(sp.linear_matrix(), h2, h3, h4)


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


def linear_combination(coefficient_map, terms):
    return sp.add(
        *(
            sp.scale(coefficient_map.get(monomial, {}), scalar)
            for scalar, monomial in terms
        )
    )


def expected_product(coefficient):
    return sp.scale(sp.mul(GAMMA, sp.S), coefficient)


def extract_claims(label, e6):
    if label == "q_C":
        return {
            "single": e6.get((4, 1, 1), {}),
        }
    if label == "q_B":
        first = e6.get((5, 0, 1), {})
        second = linear_combination(
            e6,
            (
                (Fraction(-1, 6), (3, 1, 2)),
                (Fraction(1), (1, 2, 3)),
            ),
        )
        return {
            "first": first,
            "second": second,
            "elimination": sp.sub(first, sp.scale(second, 9)),
        }
    if label == "q_E":
        return {
            "combination": linear_combination(
                e6,
                (
                    (Fraction(2, 3), (4, 0, 2)),
                    (Fraction(1), (1, 1, 4)),
                ),
            ),
        }
    fail(f"unknown chart {label}")


CHARTS = {
    "q_C": Q_C,
    "q_B": Q_B,
    "q_E": Q_E,
}

EXPECTED = {
    "q_C": {
        "single": expected_product(4),
    },
    "q_B": {
        "first": sp.mul(
            sp.S,
            sp.sub(sp.scale(GAMMA, 2), sp.scale(V_PARAMETER, 3)),
        ),
        "second": sp.scale(
            sp.mul(sp.S, sp.add(GAMMA, V_PARAMETER)),
            Fraction(-1, 3),
        ),
        "elimination": expected_product(5),
    },
    "q_E": {
        "combination": expected_product(Fraction(10, 3)),
    },
}


def audit_retained_inputs():
    for name in ("a0", "a1", "a2", "a3", "a4", "a5"):
        check(contains_parameter(sp.A, name), f"A lost retained coefficient {name}")
    for name in ("b0", "b1", "b2", "b3", "b4", "b5"):
        check(
            contains_parameter(sp.B_GENERAL, name),
            f"B lost retained coefficient {name}",
        )
    for name in ("v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8"):
        check(
            contains_parameter(sp.V_GENERAL, name),
            f"V lost retained coefficient {name}",
        )
    linear = sp.linear_matrix()
    for index in range(9):
        check(
            any(contains_parameter(entry, f"l{index}") for row in linear for entry in row),
            f"linear part lost retained entry l{index}",
        )
    for name in ("k", "u", "v", "w"):
        check(contains_parameter(W_GENERAL, name), f"W lost parameter {name}")
    check(contains_parameter(Q_C, "alpha"), "q_C lost alpha modulus")


def audit_chart(label, q):
    raw = build_raw_determinant(q)
    check(sp.all_zero_in_degree(raw, 8), f"{label}: E8 survives the gauge")
    check(sp.all_zero_in_degree(raw, 7), f"{label}: E7 survives the gauge")
    raw_e6 = sp.coefficients_of_source_degree(raw, 6)

    # This exterior reconstruction is independent of the six-term expansion
    # inside determinant_of_jets and must agree coefficient by coefficient.
    exterior = exterior_e6(q)
    exterior_e6_map = sp.coefficients_of_source_degree(exterior, 6)
    check(
        raw_e6 == exterior_e6_map,
        f"{label}: raw determinant and exterior E6 disagree",
    )
    check(
        all(
            sum(exponent[position] for position in sp.SOURCE) == 6
            for exponent in exterior
        ),
        f"{label}: exterior expression is not homogeneous of degree six",
    )

    actual = extract_claims(label, raw_e6)
    check(set(actual) == set(EXPECTED[label]), f"{label}: claim ledger mismatch")
    for claim, expected in EXPECTED[label].items():
        check(actual[claim] == expected, f"{label}: {claim} identity mismatch")

    # Normalization negative control: doubling the normalized x^3 coefficient
    # of q must invalidate at least one claimed identity.
    doubled_x3 = sp.add(q, sp.power(sp.X, 3))
    doubled_e6 = sp.coefficients_of_source_degree(
        build_raw_determinant(doubled_x3),
        6,
    )
    doubled_claims = extract_claims(label, doubled_e6)
    check(
        any(
            doubled_claims[name] != EXPECTED[label][name]
            for name in EXPECTED[label]
        ),
        f"{label}: x^3 normalization mutation escaped detection",
    )

    # Scope negative control: an xy term in W0 leaves the classified
    # W0=gamma*x^2 branch. The full E6 coefficient map must detect it. Some
    # selected linear combinations can legitimately be blind to this
    # mutation, so the comparison is made before coefficient selection.
    mutated_w = sp.add(W_GENERAL, sp.mul(sp.X, sp.Y))
    mutated_e6 = sp.coefficients_of_source_degree(
        build_raw_determinant(q, w_form=mutated_w),
        6,
    )
    check(
        mutated_e6 != raw_e6,
        f"{label}: W0-scope mutation escaped detection",
    )

    # Sensitivity control for the selected obstruction itself: shifting the
    # x^2 coefficient of W0 changes gamma and must change an advertised
    # identity on every chart.
    shifted_gamma = sp.add(W_GENERAL, sp.power(sp.X, 2))
    shifted_e6 = sp.coefficients_of_source_degree(
        build_raw_determinant(q, w_form=shifted_gamma),
        6,
    )
    shifted_claims = extract_claims(label, shifted_e6)
    check(
        any(
            shifted_claims[name] != EXPECTED[label][name]
            for name in EXPECTED[label]
        ),
        f"{label}: gamma-coefficient mutation escaped detection",
    )

    print(f"PASS {label}: raw/exterior E6, claims, and mutations")


def main():
    audit_retained_inputs()
    for label, q in CHARTS.items():
        audit_chart(label, q)
    print("PASS: HOSTILE_VERTICAL_TRIPLE_GAMMA_NONZERO_SPARSE_8D41C6")


if __name__ == "__main__":
    main()
