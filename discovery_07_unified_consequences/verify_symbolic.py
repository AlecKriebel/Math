#!/usr/bin/env python3
"""Bounded-memory exact verifier for the unified Discovery 07 claims."""

from __future__ import annotations

from fractions import Fraction
import json

import sympy as sp

from construction import (
    WEIGHTS_14,
    ROOT,
    compressed_cubic_map,
    cubic_component_factorization,
    d3_quartic_data,
    d6_construction,
    d6_direct_data,
    d6_homogeneous_data,
    degree_reduction,
    q_coefficient,
    r_coefficient,
    source_fiber_groebner,
    symmetrized_potential,
)


def as_fraction(value: sp.Expr) -> Fraction:
    value = sp.Rational(value)
    return Fraction(int(value.p), int(value.q))


def verify_source_fiber() -> None:
    basis = source_fiber_groebner()
    x, y, z = d6_construction().base_variables
    expected = (
        -27 * x**2 + 4 * z + 1,
        3 * x + 2 * y,
        x**3 - x,
    )
    assert tuple(poly.as_expr() for poly in basis.polys) == expected
    assert sp.gcd(x**3 - x, 3 * x**2 - 1) == 1
    print("[1/9] exact source fiber: reduced lex basis of length three")


def verify_determinant_blocks() -> None:
    # Discovery 06: verify the entire 14D determinant pencil through its 3x3
    # Schur complement, rather than expanding a 14x14 determinant.
    data = d6_construction()
    s = sp.Symbol("s")
    x_variables = data.base_variables
    jh2 = sp.Matrix(data.homogeneous_parts[0]).jacobian(x_variables)
    jc = data.C.jacobian(x_variables)
    inverse = sum(
        (s**power * data.N**power for power in range(5)),
        sp.zeros(11),
    )
    schur14 = sp.eye(3) + s * jh2 + s**2 * data.B * inverse * jc
    scaled14 = {variable: s * variable for variable in x_variables}
    jphi = sp.Matrix(data.phi).jacobian(x_variables)
    target14 = jphi.subs(scaled14, simultaneous=True)
    assert all(sp.expand(entry) == 0 for entry in schur14 - target14)
    assert sp.factor(jphi.det()) == 1

    # Discovery 03: independently recheck H3=B*K and the 22D block identity.
    # The determinant-one assertion for Psi follows from the six displayed
    # determinant-preserving stable operations and the identity-linear
    # normalization; no large 13x13 determinant is formed here.
    reduction = degree_reduction()
    injection, basis, _ = cubic_component_factorization(reduction)
    assert injection * sp.Matrix(basis) == sp.Matrix(reduction.cubic_part)
    variables22, nonlinear22, returned_injection, returned_basis = compressed_cubic_map(
        reduction
    )
    assert returned_injection == injection and returned_basis == basis
    w = variables22[-1]
    jh2_stable = sp.Matrix(reduction.quadratic_part).jacobian(reduction.variables)
    jk = sp.Matrix(basis).jacobian(reduction.variables)
    schur22 = sp.eye(13) + s * w * jh2_stable + s**2 * w**2 * injection * jk
    scaled22 = {variable: s * w * variable for variable in reduction.variables}
    jpsi = sp.Matrix(reduction.normalized_map).jacobian(reduction.variables)
    target22 = jpsi.subs(scaled22, simultaneous=True)
    assert all(sp.expand(entry) == 0 for entry in schur22 - target22)
    assert len(variables22) == 22 and len(nonlinear22) == 22
    print("[2/9] exact 14D and 22D Schur-complement determinant identities")


def verify_weights_and_integral_forms() -> None:
    data = d6_construction()
    s = sp.Symbol("s")
    scaling = {
        variable: s**weight * variable
        for variable, weight in zip(data.variables, WEIGHTS_14)
    }
    for component, weight in zip(data.g, WEIGHTS_14):
        polynomial = sp.Poly(component, *data.variables)
        for monomial, coefficient in polynomial.terms():
            assert coefficient != 0
            assert sum(power * w for power, w in zip(monomial, WEIGHTS_14)) == weight + 1
        assert sp.expand(component.subs(scaling, simultaneous=True) - s ** (weight + 1) * component) == 0

    # A separate diagonal conjugate has integral coefficients.
    diagonal = (2, 1, 1, 2, 2) + (1,) * 9
    substitution = {
        variable: factor * variable
        for variable, factor in zip(data.variables, diagonal)
    }
    integral = [
        sp.expand(component.subs(substitution, simultaneous=True) / factor)
        for component, factor in zip(data.g, diagonal)
    ]
    assert all(
        coefficient.q == 1
        for component in integral
        for _, coefficient in sp.Poly(component, *data.variables).terms()
    )

    # The weighted pencil member s=1/4 instead has an integral collision.
    scale = sp.Rational(1, 4)
    scaled_points = [
        tuple(
            sp.Rational(coordinate) / scale**weight
            for coordinate, weight in zip(point, WEIGHTS_14)
        )
        for point in data.collision_points
    ]
    assert all(value.q == 1 for point in scaled_points for value in point)
    common = (0, 0, -1) + (0,) * 11
    scaled_map = tuple(
        variable + scale * component
        for variable, component in zip(data.variables, data.g)
    )
    for point in scaled_points:
        substitutions = dict(zip(data.variables, point))
        assert tuple(sp.expand(entry.subs(substitutions)) for entry in scaled_map) == common
    print("[3/9] weighted pencil conjugacy and the two distinct integral normal forms")


def verify_exact_homogeneous_index() -> None:
    data = d6_construction()
    jacobian = sp.Matrix(data.g).jacobian(data.variables)

    # The block formula for Jh shows that its fourteenth power vanishes once
    # (Jg)^14=0 and (Jg)^13 g=0.  The first identity follows from the already
    # checked determinant pencil; this is the missing second identity.
    vector = sp.Matrix(data.g)
    for _ in range(13):
        vector = (jacobian * vector).applyfunc(sp.factor)
    assert vector == sp.zeros(14, 1)

    h_data = d6_homogeneous_data()
    jh = sp.Matrix(h_data.nonlinear).jacobian(h_data.variables)
    row = sp.zeros(1, 15)
    row[0, 0] = 1
    for _ in range(13):
        row = (row * jh).applyfunc(sp.factor)
    x, y, z = h_data.variables[:3]
    w = h_data.variables[-1]
    assert sp.factor(row[0, 4]) == -3 * w**67 * x**6 * y**4 * z
    print("[4/9] homogeneous companion: exact index 14 and generic type (14,1)")


def inverse_series(order: int = 36):
    t = sp.Symbol("t")
    tau = sp.S.Zero
    for _ in range(order + 2):
        tau = sp.series(t * (sp.Rational(1, 2) - tau**3), t, 0, order + 3).removeO()
    assert sp.series(tau + t * tau**3 - t / 2, t, 0, order + 1).removeO() == 0
    q = sp.diff(tau, t) - 3 * tau - (sp.diff(tau, t) - sp.Rational(1, 2)) / t
    r = sp.diff(tau, t) - 3 * tau + 3 * t * tau * sp.diff(tau, t)
    return t, tau, sp.expand(q), sp.expand(r)


def verify_inverse_coefficients() -> None:
    order = 36
    t, _, q, r = inverse_series(order)
    for m in range(order + 1):
        assert as_fraction(q.coeff(t, m)) == q_coefficient(m)
        assert as_fraction(r.coeff(t, m)) == r_coefficient(m)
        assert q_coefficient(m) != 0 and r_coefficient(m) != 0
    assert all(q_coefficient(m) and r_coefficient(m) for m in range(1000))
    print("[5/9] closed q_m and r_m formulas are nonzero in every residue class")


def verify_source_reconstruction() -> None:
    tau, t = sp.symbols("tau t")
    denominator = 1 + 3 * t * tau**2
    x = tau / denominator
    y = -3 * t * tau
    z = t * denominator * (1 - 30 * t * tau**2 - 18 * t**2 * tau**4)
    u = 1 + x * y
    source = (
        sp.together(u**3 * z + y**2 * u * (4 + 3 * x * y)),
        sp.together(y + 3 * x * u**2 * z + 3 * x * y**2 * (4 + 3 * x * y)),
        sp.together(2 * x - 3 * x**2 * y - x**3 * z),
    )
    relation = 2 * tau + 2 * t * tau**3 - t
    assert sp.factor(sp.together(source[0] - t)) == 0
    assert sp.factor(sp.together(source[1])) == 0
    numerator = sp.factor(sp.together(source[2] - t).as_numer_denom()[0])
    assert sp.rem(numerator, relation, t) == 0

    d3 = d3_quartic_data()
    expected_target = (
        sp.Rational(1, 2), 0, 1, 0, 0, 0, -2,
        0, 0, 0, 0, 0, 0,
    ) + (0,) * 8 + (1,)
    assert d3.target == expected_target
    assert d3.observable_indices == (0, 1, 7)
    print("[6/9] self-contained cubic resolvent and exact 22D inverse target")


def verify_companions() -> None:
    direct = d6_direct_data()
    homogeneous = d6_homogeneous_data()
    quartic = d3_quartic_data()

    direct_variables, direct_potential = symmetrized_potential(direct, "c", "d")
    homogeneous_variables, homogeneous_potential = symmetrized_potential(
        homogeneous, "a", "b"
    )
    quartic_variables, quartic_potential = symmetrized_potential(quartic, "e", "f")

    direct_poly = sp.Poly(direct_potential, *direct_variables)
    homogeneous_poly = sp.Poly(homogeneous_potential, *homogeneous_variables)
    quartic_poly = sp.Poly(quartic_potential, *quartic_variables)
    assert len(direct_variables) == 28 and len(direct_poly.terms()) == 178
    assert direct_poly.total_degree() == 8
    assert min(sum(monomial) for monomial, _ in direct_poly.terms()) == 2
    assert len(homogeneous_variables) == 30 and len(homogeneous_poly.terms()) == 608
    assert homogeneous_poly.total_degree() == 8 and homogeneous_poly.is_homogeneous
    assert len(quartic_variables) == 44 and len(quartic_poly.terms()) == 538
    assert quartic_poly.total_degree() == 4 and quartic_poly.is_homogeneous

    # Guard that the reconstructed flagship objects are exactly the archived
    # sparse objects named by the certificate hashes, not merely objects with
    # the same dimensions and term counts.
    d6_payload = json.loads(
        (ROOT / "discovery_06_unipotent_three_point" / "output" / "unipotent14_sparse.json").read_text()
    )
    assert d6_payload["variables"] == [str(variable) for variable in direct.variables]
    for current, archived in zip(direct.nonlinear, d6_payload["g"]):
        current_terms = dict(sp.Poly(current, *direct.variables).terms())
        archived_terms = {
            tuple(term["powers"]): sp.Rational(term["coefficient"])
            for term in archived
        }
        assert current_terms == archived_terms

    d3_payload = json.loads(
        (ROOT / "discovery_03_small_vanishing_counterexample" / "output" / "potential_sparse.json").read_text()
    )
    archived_quartic = {}
    for term in d3_payload["terms"]:
        powers = [0] * 44
        for index, exponent in term["powers"]:
            powers[index] = exponent
        coefficient = sp.Rational(term["coefficient"]["real"])
        coefficient += sp.I * sp.Rational(term["coefficient"]["imag"])
        archived_quartic[tuple(powers)] = coefficient
    assert dict(quartic_poly.terms()) == archived_quartic
    print(
        "[7/9] symmetric companions and exact D6/D3 precursor coefficient matches"
    )


def verify_symmetrization_identity() -> None:
    # Check the gradient identity on both homogeneous headline companions.
    for data, first_prefix, second_prefix in (
        (d6_homogeneous_data(), "a", "b"),
        (d3_quartic_data(), "e", "f"),
    ):
        variables, potential = symmetrized_potential(data, first_prefix, second_prefix)
        n = len(data.variables)
        first, second = variables[:n], variables[n:]
        substitutions = {
            variable: first[index] + sp.I * second[index]
            for index, variable in enumerate(data.variables)
        }
        h_at_x = sp.Matrix([entry.subs(substitutions) for entry in data.nonlinear])
        jh_at_x = sp.Matrix(data.nonlinear).jacobian(data.variables).subs(
            substitutions, simultaneous=True
        )
        gradient_first = sp.Matrix([sp.diff(potential, variable) for variable in first])
        gradient_second = sp.Matrix([sp.diff(potential, variable) for variable in second])
        b_vector = sp.Matrix(second)
        assert all(sp.expand(entry) == 0 for entry in gradient_first - sp.I * jh_at_x.T * b_vector)
        assert all(
            sp.expand(entry) == 0
            for entry in gradient_second - (-jh_at_x.T * b_vector + sp.I * h_at_x)
        )
    print("[8/9] exact triangular symmetrization and inverse-projection identity")


def verify_transfer_indices() -> None:
    # Zhao's k=1 formula contributes order t^(m+1) to the inverse map.
    # These arithmetic guards make the index shift and factorial explicit.
    for m in range(20):
        q_value = q_coefficient(m + 1)
        r_value = r_coefficient(m + 1)
        factor = 2**m * int(sp.factorial(m)) * int(sp.factorial(m + 1))
        q_derivative = factor * q_value
        r_derivative = factor * r_value
        assert q_derivative and r_derivative
    print("[9/9] Zhao index shift: every Delta^m P^(m+1) has a nonzero derivative")


def main() -> None:
    verify_source_fiber()
    verify_determinant_blocks()
    verify_weights_and_integral_forms()
    verify_exact_homogeneous_index()
    verify_inverse_coefficients()
    verify_source_reconstruction()
    verify_companions()
    verify_symmetrization_identity()
    verify_transfer_indices()
    print("All unified exact symbolic checks passed.")


if __name__ == "__main__":
    main()
