#!/usr/bin/env python3
"""Exact lower-identity closure of the six marked-distinct endpoints.

The neighboring ``verify_e7_e6_sympy.py`` certifies the complete E7 normal
forms and the E6 compatibility ideals.  This verifier reconstructs every
weighted determinant again and certifies the exhaustive E5/E4 branches.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

if not __debug__:
    print("FAIL: assertions are required; do not run with -O", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp

parent = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    "released_endpoints", parent / "verify_e7_e6_sympy.py"
)
released = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(released)

x, y, z, weight = released.x, released.y, released.z, released.tau
xyz = released.xyz
mon2 = released.mon2
A, B, C, D = released.A, released.B, released.C, released.D
T, E, F = released.T, released.E, released.F


def exact_zero(value):
    return sp.cancel(sp.expand(value)) == 0


def coefficients(value, degree):
    return released.homogeneous_coefficients(value, degree)


def polynomial_left_values(matrix, rhs):
    values = []
    for vector in matrix.T.nullspace():
        denominators = [
            sp.together(entry).as_numer_denom()[1]
            for entry in vector
            if not exact_zero(entry)
        ]
        denominator = sp.factor(sp.lcm(denominators)) if denominators else 1
        vector = vector.applyfunc(lambda entry: sp.cancel(denominator * entry))
        assert all(exact_zero(entry) for entry in matrix.T * vector)
        value = sp.factor((vector.T * rhs)[0])
        if not exact_zero(value):
            values.append(value)
    return values


def has_associate(values, target):
    for value in values:
        if exact_zero(value) or exact_zero(target):
            continue
        ratio = sp.cancel(value / target)
        if not ratio.free_symbols and ratio != 0:
            return True
    return False


def weighted_data(branch, substitutions, suffix):
    h = branch["h"]
    P, Q = sp.expand(h**2), sp.expand(h * x**2)
    R = sp.expand(branch["R"])
    U = sp.expand(branch["U"].subs(substitutions))
    V = sp.expand(branch["V"].subs(substitutions))
    W = sp.expand(branch["W"].subs(substitutions))
    prefix = (
        branch["label"].replace("-", "_").replace("/", "_")
        + "_"
        + suffix
    )
    aa = sp.symbols(f"{prefix}_a0:6")
    bb = sp.symbols(f"{prefix}_b0:6")
    ell = sp.symbols(f"{prefix}_l0:9")
    H2 = sp.Matrix(
        [
            sum(coefficient * monomial for coefficient, monomial in zip(aa, mon2)),
            sum(coefficient * monomial for coefficient, monomial in zip(bb, mon2)),
            W,
        ]
    )
    L = sp.Matrix(3, 3, ell)
    determinant = sp.Poly(
        sp.expand(
            (
                L
                + weight * H2.jacobian(xyz)
                + weight**2 * sp.Matrix([U, V, R]).jacobian(xyz)
                + weight**3 * sp.Matrix([P, Q, 0]).jacobian(xyz)
            ).det()
        ),
        weight,
    )
    return determinant, aa + bb + ell, L


def solve_identity(determinant, degree, unknowns, prior=None):
    prior = prior or {}
    identity = sp.expand(
        determinant.coeff_monomial(weight**degree).subs(prior)
    )
    remaining = tuple(
        unknown for unknown in unknowns if unknown in identity.free_symbols
    )
    matrix, rhs = sp.linear_eq_to_matrix(coefficients(identity, degree), remaining)
    solution = next(iter(sp.linsolve((matrix, rhs), remaining)))
    substitutions = dict(zip(remaining, solution))
    assert all(
        exact_zero(entry)
        for entry in (
            matrix * sp.Matrix(solution) - rhs
        )
    )
    return matrix, rhs, remaining, substitutions


branches = {entry["label"]: entry for entry in released.BRANCHES}


def verify_h_endpoint_compatibilities():
    """E6 plus global E5 syzygies force C=D=E=F=0."""

    for label in ("RT-reducible/H", "RT-smooth/H"):
        determinant, unknowns, _ = weighted_data(
            branches[label], {A: 0, E: 0, F: 0}, "Azero"
        )
        matrix6, rhs6, _, substitutions6 = solve_identity(
            determinant, 6, unknowns
        )
        assert matrix6.rank() == 8
        identity5 = sp.expand(
            determinant.coeff_monomial(weight**5).subs(substitutions6)
        )
        remaining5 = tuple(
            unknown for unknown in unknowns if unknown in identity5.free_symbols
        )
        matrix5, rhs5 = sp.linear_eq_to_matrix(
            coefficients(identity5, 5), remaining5
        )
        values = polynomial_left_values(matrix5, rhs5)
        assert has_associate(values, C**3)
        assert has_associate(values, D**3)

    label = "RO-smooth/H"
    determinant, unknowns, _ = weighted_data(
        branches[label], {A: 0, E: 0, F: 0}, "Azero"
    )
    _, _, _, substitutions6 = solve_identity(determinant, 6, unknowns)
    identity5 = sp.expand(
        determinant.coeff_monomial(weight**5).subs(substitutions6)
    )
    remaining5 = tuple(
        unknown for unknown in unknowns if unknown in identity5.free_symbols
    )
    matrix5, rhs5 = sp.linear_eq_to_matrix(
        coefficients(identity5, 5), remaining5
    )
    values = polynomial_left_values(matrix5, rhs5)
    assert has_associate(values, D**3)
    # Once D=0, the global value -12*C*(6*B*D-C^2) is 12*C^3.
    assert any(
        exact_zero(
            value.subs(D, 0) - 12 * C**3
        )
        or exact_zero(
            value.subs(D, 0) + 12 * C**3
        )
        for value in values
    )


def verify_rt_h_endpoints():
    for label in ("RT-reducible/H", "RT-smooth/H"):
        final = {C: 0, D: 0, E: 0, F: 0}
        # A != 0 open chart.
        determinant, unknowns, L = weighted_data(
            branches[label], final, "Aopen"
        )
        _, _, _, substitutions6 = solve_identity(determinant, 6, unknowns)
        matrix5, _, _, substitutions5 = solve_identity(
            determinant, 5, unknowns, substitutions6
        )
        assert matrix5.rank() == 6
        assert sp.factor(
            matrix5.extract((1, 2, 7, 8, 17, 18), range(6)).det()
        ) == -36 * A**2
        assert exact_zero(L.det().subs(substitutions6).subs(substitutions5))

        # Fresh A=0 boundary, with no division by A.
        determinant0, unknowns0, L0 = weighted_data(
            branches[label], final | {A: 0}, "Azero_final"
        )
        _, _, _, substitutions60 = solve_identity(
            determinant0, 6, unknowns0
        )
        matrix50, _, _, substitutions50 = solve_identity(
            determinant0, 5, unknowns0, substitutions60
        )
        assert matrix50.rank() == 4
        assert exact_zero(L0.det().subs(substitutions60).subs(substitutions50))


def verify_ro_h_endpoint():
    label = "RO-smooth/H"
    final = {C: 0, D: 0, E: 0, F: 0}

    # A*T != 0.
    determinant, unknowns, L = weighted_data(branches[label], final, "ATopen")
    _, _, _, substitutions6 = solve_identity(determinant, 6, unknowns)
    matrix5, _, _, substitutions5 = solve_identity(
        determinant, 5, unknowns, substitutions6
    )
    assert matrix5.rank() == 6
    assert sp.factor(
        matrix5.extract((0, 1, 2, 4, 5, 8), (0, 1, 2, 4, 6, 7)).det()
    ) == 288 * A**2 * T**2
    assert exact_zero(L.det().subs(substitutions6).subs(substitutions5))

    # T=0, A != 0.
    determinant_t0, unknowns_t0, L_t0 = weighted_data(
        branches[label], final | {T: 0}, "Tzero"
    )
    _, _, _, substitutions6_t0 = solve_identity(
        determinant_t0, 6, unknowns_t0
    )
    matrix5_t0, _, _, substitutions5_t0 = solve_identity(
        determinant_t0, 5, unknowns_t0, substitutions6_t0
    )
    assert matrix5_t0.rank() == 6
    assert exact_zero(
        L_t0.det().subs(substitutions6_t0).subs(substitutions5_t0)
    )

    # A=T=0.
    determinant_a0t0, unknowns_a0t0, L_a0t0 = weighted_data(
        branches[label], final | {A: 0, T: 0}, "ATzero"
    )
    _, _, _, substitutions6_a0t0 = solve_identity(
        determinant_a0t0, 6, unknowns_a0t0
    )
    matrix5_a0t0, _, _, substitutions5_a0t0 = solve_identity(
        determinant_a0t0, 5, unknowns_a0t0, substitutions6_a0t0
    )
    assert matrix5_a0t0.rank() == 4
    assert exact_zero(
        L_a0t0.det().subs(substitutions6_a0t0).subs(substitutions5_a0t0)
    )

    # A=0,T!=0: the unique sharp endpoint survivor through E5.
    determinant_a0, unknowns_a0, L_a0 = weighted_data(
        branches[label], final | {A: 0}, "Azero_Topen"
    )
    _, _, _, substitutions6_a0 = solve_identity(
        determinant_a0, 6, unknowns_a0
    )
    matrix5_a0, _, _, substitutions5_a0 = solve_identity(
        determinant_a0, 5, unknowns_a0, substitutions6_a0
    )
    assert matrix5_a0.rank() == 4
    through5 = substitutions6_a0 | substitutions5_a0
    E4 = sp.expand(
        determinant_a0.coeff_monomial(weight**4).subs(through5)
    )
    E4coeff = sp.Poly(E4, x, y, z)
    ell = tuple(L_a0)
    # Matrix iteration is row-major: ell[7]=l_32, ell[8]=l_33.
    assert E4coeff.coeff_monomial(x * y * z**2) == -8 * ell[8] ** 2
    second = sp.expand(
        E4coeff.coeff_monomial(x**2 * y * z).subs(ell[8], 0)
    )
    assert second == 4 * ell[7] ** 2
    assert exact_zero(L_a0.det().subs(through5).subs(ell[7], 0))


def verify_s_endpoints():
    for label in ("RT-reducible/S", "RT-smooth/S"):
        determinant, unknowns, L = weighted_data(
            branches[label], {C: 0, D: 0}, "CDzero"
        )
        _, _, _, substitutions6 = solve_identity(determinant, 6, unknowns)
        matrix5, _, _, substitutions5 = solve_identity(
            determinant, 5, unknowns, substitutions6
        )
        assert matrix5.rank() == 4
        assert exact_zero(L.det().subs(substitutions6).subs(substitutions5))

    label = "RO-smooth/S"
    # D=0 is forced at E6.  A global E5 syzygy then forces C=0.
    determinant_d0, unknowns_d0, _ = weighted_data(
        branches[label], {D: 0}, "Dzero"
    )
    _, _, _, substitutions6_d0 = solve_identity(
        determinant_d0, 6, unknowns_d0
    )
    identity5_d0 = sp.expand(
        determinant_d0.coeff_monomial(weight**5).subs(substitutions6_d0)
    )
    remaining5_d0 = tuple(
        unknown
        for unknown in unknowns_d0
        if unknown in identity5_d0.free_symbols
    )
    matrix5_d0, rhs5_d0 = sp.linear_eq_to_matrix(
        coefficients(identity5_d0, 5), remaining5_d0
    )
    values = polynomial_left_values(matrix5_d0, rhs5_d0)
    assert has_associate(values, C**3)

    for case_name, extra in (("Aopen", {}), ("Azero", {A: 0})):
        determinant, unknowns, L = weighted_data(
            branches[label], {C: 0, D: 0} | extra, case_name
        )
        _, _, _, substitutions6 = solve_identity(determinant, 6, unknowns)
        matrix5, _, _, substitutions5 = solve_identity(
            determinant, 5, unknowns, substitutions6
        )
        assert matrix5.rank() == 4
        assert exact_zero(L.det().subs(substitutions6).subs(substitutions5))


verify_h_endpoint_compatibilities()
verify_rt_h_endpoints()
verify_ro_h_endpoint()
verify_s_endpoints()

print("MARKED_DISTINCT_ENDPOINTS_SYMPY_PASS_0E5C42")
print("six CH/CS endpoints: exhaustive E5/E4 branches force det(L)=0")
