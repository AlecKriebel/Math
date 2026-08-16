#!/usr/bin/env python3
"""Exact determinant and right-half-plane certificates for the rational seed.

This discovery-side module derives the sparse product-minus-boundary
characteristic formula and emits coefficientwise-positive modulus
certificates.  It deliberately limits full symbolic determinant expansion to
small m; the all-m proof is the sparse recurrence, not interpolation.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp
from reconstruct_family import jacobian_factor

D1 = sp.Rational(257, 240)
DM = sp.Rational(43, 165)
DZ = sp.Integer(21)


def dlist(m: int) -> list[sp.Expr]:
    if m < 3:
        raise ValueError("m must be at least 3")
    return (
        [D1, sp.Rational(m + 1, 227 * m - 457)]
        + [sp.Rational(3, 227 * m - 451 - 3 * i) for i in range(3, m)]
        + [DM, DZ]
    )


def product_formula(m: int, lam: sp.Expr, t: sp.Expr) -> sp.Expr:
    ds = dlist(m)
    g1 = lam + 2 + t * ds[0]
    gm = lam + 5 + t * ds[m - 1]
    gz = lam + 4 + t * ds[m]
    Q = sp.prod(lam + 1 + t * ds[i - 1] for i in range(2, m))
    F = g1 * gm * gz - 4 * g1 - 4 * gm + gz
    G = gz * (4 * g1 + gm) - 36
    return sp.factor(Q * F - G)


def direct_characteristic(m: int, lam: sp.Expr, t: sp.Expr) -> sp.Expr:
    A = jacobian_factor(m, 1, 1)
    D = sp.diag(*dlist(m))
    return sp.factor((lam * sp.eye(m + 1) - A + t * D).det(method="domain-ge"))


def _modulus_squared(expr: sp.Expr, x: sp.Symbol, y: sp.Symbol) -> sp.Expr:
    return sp.expand(expr * sp.conjugate(expr)).subs(
        {sp.conjugate(x): x, sp.conjugate(y): y}
    ).expand()


def _even_y_terms(poly: sp.Poly) -> dict[tuple[int, ...], sp.Expr]:
    out: dict[tuple[int, ...], sp.Expr] = {}
    for powers, coeff in poly.terms():
        y_power = powers[1]
        if y_power % 2:
            raise AssertionError(f"unexpected odd y power: {powers}")
        out[(powers[0], y_power // 2, *powers[2:])] = sp.factor(coeff)
    return out


def modulus_polynomials() -> tuple[dict[tuple[int, ...], sp.Expr], dict[tuple[int, ...], sp.Expr]]:
    x, y, s = sp.symbols("x y s", nonnegative=True, real=True)
    lam = x + sp.I * y

    P = lam**4 + 12 * lam**3 + 42 * lam**2 + 47 * lam + 16
    R = 5 * lam**2 + 33 * lam + 16
    E_hom = sp.Poly(
        sp.expand(((x + 1) ** 2 + y**2) * _modulus_squared(P, x, y)
                  - _modulus_squared(R, x, y)),
        x,
        y,
    )
    hom_terms = _even_y_terms(E_hom)

    t = 1 + s
    g1 = lam + 2 + t * D1
    gm = lam + 5 + t * DM
    gz = lam + 4 + t * DZ
    F = sp.expand(g1 * gm * gz - 4 * g1 - 4 * gm + gz)
    G = sp.expand(gz * (4 * g1 + gm) - 36)
    E_mode = sp.Poly(
        sp.expand(sp.Rational(57**2, 56**2) * _modulus_squared(F, x, y)
                  - _modulus_squared(G, x, y)),
        x,
        y,
        s,
    )
    mode_terms = _even_y_terms(E_mode)
    return hom_terms, mode_terms


def write_certificate(path: Path) -> None:
    hom, mode = modulus_polynomials()
    obj = {
        "homogeneous": {
            "variables": ["x", "z=y^2"],
            "description": "|1+lambda|^2 |P(lambda)|^2-|R(lambda)|^2",
            "terms": [
                {"powers": list(k), "coefficient": str(v)}
                for k, v in sorted(hom.items())
            ],
        },
        "mode_isolation": {
            "variables": ["x", "z=y^2", "s=t-1"],
            "description": "(57/56)^2 |F(lambda,t)|^2-|G(lambda,t)|^2",
            "terms": [
                {"powers": list(k), "coefficient": str(v)}
                for k, v in sorted(mode.items())
            ],
        },
    }
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def self_test() -> None:
    lam, t = sp.symbols("lambda t")
    # Full sparse-vs-dense symbolic checks at genuinely independent small sizes.
    for m in [3, 4, 5]:
        diff = sp.cancel(product_formula(m, lam, t) - direct_characteristic(m, lam, t))
        assert diff == 0, (m, diff)
        assert sp.factor(product_formula(m, 0, 1)) == 0

    # Larger-size checks use several exact evaluation points, avoiding a costly
    # dense symbolic determinant while still mutation-testing the recurrence.
    for m in [6, 8, 10]:
        A = jacobian_factor(m, 1, 1)
        D = sp.diag(*dlist(m))
        for lv, tv in [(0, 1), (sp.Rational(2, 3), sp.Rational(7, 5)), (2, 4)]:
            lhs = sp.factor((lv * sp.eye(m + 1) - A + tv * D).det(method="domain-ge"))
            rhs = sp.factor(product_formula(m, lv, tv))
            assert lhs == rhs, (m, lv, tv)

    # The critical chain product telescopes for every m.
    for m in range(3, 40):
        q = sp.prod(1 + d for d in dlist(m)[1 : m - 1])
        assert sp.factor(q - sp.Rational(57, 56)) == 0

    hom, mode = modulus_polynomials()
    assert hom and mode
    assert all(c > 0 for c in hom.values())
    assert all(c > 0 for c in mode.values())
    assert (0, 0) not in hom
    assert (0, 0, 0) not in mode
    print(f"spectral certificates pass: {len(hom)} homogeneous terms, {len(mode)} mode terms")


if __name__ == "__main__":
    self_test()
    out = Path(__file__).resolve().parents[1] / "critical_mode" / "modulus_certificate.json"
    write_certificate(out)
    print(out)
