#!/usr/bin/env python3
"""Verify the equilibrium-scaled half-plane certificates exactly.

The homogeneous certificate is tied directly to the characteristic factor
Q(lambda) F_0(lambda)-R(lambda).  The m=3 case is handled separately by an
exact cubic Routh--Hurwitz calculation.  A rational Rouche enclosure records
why the superseded all-dimensional lower endpoint cannot be restored.
"""
from __future__ import annotations

if not __debug__:
    raise SystemExit(
        "Exact verifier requires assertions; unset PYTHONOPTIMIZE and do not use python -O"
    )

import argparse
from fractions import Fraction
import json
from pathlib import Path
import sys

import sympy as sp


def coefficient_values(term, parameter, section):
    """Read the section's declared coefficient parameter unambiguously."""

    required = f"coefficient_in_{parameter}_ascending"
    recognized = {
        key
        for key in ("coefficient_in_U_ascending", "coefficient_in_A_ascending")
        if key in term
    }
    if required not in recognized:
        raise AssertionError(
            f"{section}: row {term.get('powers')!r} lacks required field {required!r}"
        )
    conflicting = recognized - {required}
    if conflicting:
        raise AssertionError(
            f"{section}: row {term.get('powers')!r} has conflicting recognized "
            f"coefficient field(s) {sorted(conflicting)!r}"
        )
    return [sp.Rational(value) for value in term[required]]


def even(expr, y, z):
    out = 0
    for (k,), coef in sp.Poly(sp.expand(expr), y).terms():
        assert k % 2 == 0
        out += coef * z ** (k // 2)
    return sp.expand(out)


def generate():
    x, y, z, s, A, U = sp.symbols("x y z s A U", real=True)
    lam = x + sp.I * y

    # At t=0 the normalized characteristic determinant is Q F0-R.  For
    # nu>=2, |Q|^2 >= 1+A*x+(5/4)*y^2.  Coefficient positivity is exposed
    # after the harmless shift U=A-1/4.
    F0 = lam**3 + 11 * lam**2 + 31 * lam + 16
    R = 5 * lam**2 + 33 * lam + 16
    Eh = sp.expand(
        (1 + (U + sp.Rational(1, 4)) * x + sp.Rational(5, 4) * z)
        * even(F0 * sp.conjugate(F0), y, z)
        - even(R * sp.conjugate(R), y, z)
    )

    # For t=1+s the higher-mode certificate is unchanged.  The repaired
    # interval is a subset of the interval on which this B=1/3 bound holds.
    q0 = sp.Rational(91, 90)
    t = 1 + s
    g1 = lam + 2 + t * sp.Rational(23, 63)
    gm = lam + 5 + t * sp.Rational(1, 7)
    gz = lam + 4 + t * sp.Rational(16, 45)
    F = sp.expand(g1 * gm * gz - 4 * g1 - 4 * gm + gz)
    G = sp.expand(gz * (4 * g1 + gm) - 36)
    Em = sp.expand(
        q0**2
        * (1 + A * x + sp.Rational(1, 3) * z)
        * even(F * sp.conjugate(F), y, z)
        - even(G * sp.conjugate(G), y, z)
    )
    return Eh, Em, (x, z, s, A, U)


def verify_characteristic_connection():
    """Check QF0-R against exact determinants in symbolic low dimensions."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import pareto_core as pc

    lam, L = sp.symbols("lambda L")
    F0 = lam**3 + 11 * lam**2 + 31 * lam + 16
    R = 5 * lam**2 + 33 * lam + 16
    for m in (3, 4, 5):
        H = sp.diag(*pc.Hlist(m, L))
        actual = sp.factor((lam * sp.eye(m + 1) - H * pc.A(m)).det() / H.det())
        Q = sp.prod(
            1 + L * sp.Rational(pc.K(m, i - 1), pc.K(m, i)) * lam
            for i in range(2, m)
        )
        assert sp.factor(actual - (Q * F0 - R)) == 0


def verify_exceptional_nu_one():
    """Exact Routh--Hurwitz check for the exceptional case m=3."""
    lam, c = sp.symbols("lambda c", positive=True)
    F0 = lam**3 + 11 * lam**2 + 31 * lam + 16
    R = 5 * lam**2 + 33 * lam + 16
    quotient = sp.div(sp.Poly((1 + c * lam) * F0 - R, lam), sp.Poly(lam, lam))
    expected = c * lam**3 + (1 + 11 * c) * lam**2 + (6 + 31 * c) * lam + 16 * c - 2
    assert quotient[1].as_expr() == 0
    assert sp.expand(quotient[0].as_expr() - expected) == 0
    rh_gap = sp.expand((1 + 11 * c) * (6 + 31 * c) - c * (16 * c - 2))
    assert rh_gap == 6 + 99 * c + 325 * c**2
    c0 = sp.Rational(91, 90) / sp.sqrt(3)
    assert c0 > sp.Rational(1, 8)
    assert all(v.subs(c, c0) > 0 for v in (c, 1 + 11 * c, 6 + 31 * c, 16 * c - 2, rh_gap))


def _gadd(a, b):
    return a[0] + b[0], a[1] + b[1]


def _gmul(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def _gscale(a, c):
    return a[0] * c, a[1] * c


def _l1(a):
    return abs(a[0]) + abs(a[1])


def legacy_endpoint_rouche_regression():
    """Exactly enclose an unstable root at the superseded m=149 endpoint.

    All arithmetic below is rational.  On the circle |w|=rho around z0 we
    compare p(z0+w) with p'(z0)w.  A product bound gives a rational upper
    bound M2 for |p''| on the disk.  The strict inequality

        |Re p'(z0)| rho > |p(z0)|_1 + M2 rho^2/2

    proves by Rouche's theorem that the disk contains one root.  The entire
    disk lies in the open right half-plane.
    """
    m = 149
    nu = m - 2
    legacy_L = Fraction(1, 21)  # 1/sqrt(3*147)
    assert legacy_L * legacy_L * nu == Fraction(1, 3)

    def K(i):
        return 91 * m - 181 - i

    cs = [legacy_L * Fraction(K(i - 1), K(i)) for i in range(2, m)]
    z0 = (
        Fraction(136549671610931, 10**18),
        Fraction(880678386744175, 10**15),
    )
    rho = Fraction(1, 10**12)

    Q = (Fraction(1), Fraction(0))
    Qp = (Fraction(0), Fraction(0))
    for c in cs:
        factor = _gadd((Fraction(1), Fraction(0)), _gscale(z0, c))
        Qp = _gadd(_gmul(Qp, factor), _gscale(Q, c))
        Q = _gmul(Q, factor)

    z2 = _gmul(z0, z0)
    z3 = _gmul(z2, z0)
    F0 = _gadd(
        _gadd(_gadd(z3, _gscale(z2, 11)), _gscale(z0, 31)),
        (Fraction(16), Fraction(0)),
    )
    F0p = _gadd(_gadd(_gscale(z2, 3), _gscale(z0, 22)), (Fraction(31), Fraction(0)))
    R = _gadd(_gadd(_gscale(z2, 5), _gscale(z0, 33)), (Fraction(16), Fraction(0)))
    Rp = _gadd(_gscale(z0, 10), (Fraction(33), Fraction(0)))
    p0 = _gadd(_gmul(Q, F0), _gscale(R, -1))
    p1 = _gadd(_gadd(_gmul(Qp, F0), _gmul(Q, F0p)), _gscale(Rp, -1))

    # On the disk, |lambda| <= Z by the rational l1 bound.  Therefore
    # |Q|, |Q'|, |Q''| are bounded respectively by Qbar,
    # Qbar*sum(c_i), and Qbar*sum(c_i)^2.
    Z = z0[0] + z0[1] + rho
    Qbar = Fraction(1)
    for c in cs:
        Qbar *= 1 + c * Z
    sum_c = sum(cs, Fraction(0))
    Fbar = Z**3 + 11 * Z**2 + 31 * Z + 16
    Fpbar = 3 * Z**2 + 22 * Z + 31
    Fppbar = 6 * Z + 22
    M2 = (
        Qbar * sum_c**2 * Fbar
        + 2 * Qbar * sum_c * Fpbar
        + Qbar * Fppbar
        + 10
    )
    linear_lower = abs(p1[0]) * rho
    remainder_upper = _l1(p0) + M2 * rho**2 / 2
    assert linear_lower > remainder_upper
    assert z0[0] - rho > 0


def verify(path: Path):
    data = json.loads(path.read_text())
    Eh, Em, (x, z, s, A, U) = generate()

    homogeneous = data["modulus"]["homogeneous"]
    assert homogeneous["variables"] == ["x", "z"]
    assert homogeneous["B"] == "5/4"
    assert homogeneous["coefficient_parameter"] == "U=A-1/4"
    assert homogeneous["term_count"] == 22
    homogeneous_rows = homogeneous["terms"]
    homogeneous_powers = [tuple(term["powers"]) for term in homogeneous_rows]
    expected_homogeneous = {
        monomial: list(reversed(sp.Poly(coefficient, U).all_coeffs()))
        for monomial, coefficient in sp.Poly(Eh, x, z).terms()
    }
    assert all(len(powers) == 2 for powers in homogeneous_powers)
    assert len(homogeneous_rows) == homogeneous["term_count"] == len(expected_homogeneous)
    assert len(set(homogeneous_powers)) == len(homogeneous_powers)
    table = {
        tuple(t["powers"]): coefficient_values(t, "U", "homogeneous modulus certificate")
        for t in homogeneous_rows
    }
    assert set(table) == set(expected_homogeneous)
    for mon, coeffs in expected_homogeneous.items():
        assert table[mon] == coeffs
        assert all(v >= 0 for v in coeffs) and any(v > 0 for v in coeffs)
    # Strict positivity away from x=z=0 follows already at U=0 from the
    # x^2 and z^2 coefficients; the x coefficient becomes positive for U>0.
    assert sp.Poly(Eh, x, z).coeff_monomial(x**2).subs(U, 0) > 0
    assert sp.Poly(Eh, x, z).coeff_monomial(z**2).subs(U, 0) > 0

    spatial = data["modulus"]["spatial"]
    assert spatial["variables"] == ["x", "z", "s"]
    assert spatial["B"] == "1/3"
    assert spatial["term_count"] == 84
    spatial_rows = spatial["terms"]
    spatial_powers = [tuple(term["powers"]) for term in spatial_rows]
    expected_spatial = {
        monomial: list(reversed(sp.Poly(coefficient, A).all_coeffs()))
        for monomial, coefficient in sp.Poly(Em, x, z, s).terms()
    }
    assert all(len(powers) == 3 for powers in spatial_powers)
    assert len(spatial_rows) == spatial["term_count"] == len(expected_spatial)
    assert len(set(spatial_powers)) == len(spatial_powers)
    table = {
        tuple(t["powers"]): coefficient_values(t, "A", "spatial modulus certificate")
        for t in spatial_rows
    }
    assert set(table) == set(expected_spatial)
    for mon, coeffs in expected_spatial.items():
        assert table[mon] == coeffs
        assert all(v >= 0 for v in coeffs) and any(v > 0 for v in coeffs)

    verify_characteristic_connection()
    verify_exceptional_nu_one()
    legacy_endpoint_rouche_regression()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "certificate",
        nargs="?",
        default=str(Path(__file__).resolve().parent / "pareto_all_m_certificate.json"),
    )
    args = parser.parse_args()
    verify(Path(args.certificate))
    print("VERIFY_MODE_CERTIFICATES_PASS")
