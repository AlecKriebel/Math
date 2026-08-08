#!/usr/bin/env python3
"""Exact verifier for the heterogeneous dense-pair dB obstruction."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    r, A, x = sp.symbols("r A x", positive=True)
    z = (1 - x) / x
    t = 1 + r * z
    qratio = 1 / (1 + A * t)
    repair = r * z / (1 + r * z)
    q1 = sp.factor(1 / (1 + repair + A - repair * qratio))

    y = r - (r - 1) * x
    B = A * (A + 2)
    C = A * (A + 1)
    D = x + B * y
    survival = sp.factor(1 - q1)
    s_expected = C * y / D
    g = sp.factor(x * survival)
    g_expected = C * x * y / D
    assert sp.factor(survival - s_expected) == 0
    assert sp.factor(g - g_expected) == 0

    # The self-consistency response h_A=g_A/A decreases in A.
    h = sp.factor(g_expected / A)
    dh = sp.factor(sp.diff(h, A))
    dh_expected = x * y * (x - (A**2 + 2 * A + 2) * y) / D**2
    assert sp.factor(dh - dh_expected) == 0

    q = sp.symbols("q", nonnegative=True)
    h_boundary_defect = sp.factor((h.subs(A, r - 1) - 1 / r).subs(x, 1 - q))
    yq = sp.factor(y.subs(x, 1 - q))
    D_boundary_q = sp.factor((x + (r**2 - 1) * y).subs(x, 1 - q))
    h_boundary_expected = -q * (r - 1) * (q * r + 1) / D_boundary_q
    assert sp.factor(h_boundary_defect - h_boundary_expected) == 0
    assert sp.factor(yq - (1 + (r - 1) * q)) == 0

    # Parametric concavity of the upper (increasing) response branch.
    ds = sp.factor(sp.diff(s_expected, x))
    J = B * y**2 - (r - 1) * x**2
    dg = sp.factor(sp.diff(g_expected, x))
    assert sp.factor(ds + C * r / D**2) == 0
    assert sp.factor(dg - C * J / D**2) == 0
    assert sp.factor(sp.diff(J, x) + 2 * (r - 1) * D) == 0
    d2sdg2 = sp.factor(sp.diff(ds / dg, x) / dg)
    concavity_expected = -2 * r * (r - 1) * D**3 / (C * J**3)
    assert sp.factor(d2sdg2 - concavity_expected) == 0

    # The comparison point x_0=A/(r-1).
    x0 = A / (r - 1)
    D0 = sp.factor(D.subs(x, x0))
    g0_defect = sp.factor(g_expected.subs(x, x0) - A / r)
    s0_defect = sp.factor(s_expected.subs(x, x0) - (r - 1) / r)
    assert sp.factor(
        g0_defect + A**2 * (r - 1 - A) ** 2 / (r * (r - 1) * D0)
    ) == 0
    assert sp.factor(
        s0_defect + A * (r - 1 - A) ** 2 / (r * D0)
    ) == 0
    assert sp.factor(g_expected.subs(x, 1) - A / (A + 1)) == 0

    # Exact two-atom fixed-point checks.  Solve E[g_A]=A/r, then verify
    # E[s_A]<=p without floating arithmetic.
    for rv, atoms in [
        (sp.Rational(19, 10), [(sp.Rational(1, 2), sp.Rational(1, 5)),
                               (sp.Rational(1, 2), sp.Rational(4, 5))]),
        (sp.Rational(2), [(sp.Rational(1, 3), sp.Rational(1, 10)),
                          (sp.Rational(2, 3), sp.Rational(3, 4))]),
        (sp.Rational(3, 2), [(sp.Rational(3, 4), sp.Rational(1, 3)),
                             (sp.Rational(1, 4), sp.Rational(1, 1))]),
    ]:
        mean_g = sum(weight * g_expected.subs({r: rv, x: xv}) for weight, xv in atoms)
        fixed_poly = sp.Poly(sp.cancel(mean_g - A / rv).as_numer_denom()[0], A)
        roots = sp.polys.polytools.intervals(fixed_poly, eps=sp.Rational(1, 10**15))
        positive_intervals = [interval for interval, mult in roots if interval[0] > 0]
        assert len(positive_intervals) == 1
        lo, hi = positive_intervals[0]
        assert hi <= rv - 1

        mean_s = sum(weight * s_expected.subs({r: rv, x: xv}) for weight, xv in atoms)
        defect_num = sp.Poly(
            sp.cancel((rv - 1) / rv - mean_s).as_numer_denom()[0], A
        )
        # The unique positive fixed point lies in an interval on which the
        # exact dB defect has positive sign.
        midpoint = (lo + hi) / 2
        assert defect_num.eval(midpoint) > 0
        assert not sp.polys.polytools.intervals(defect_num, inf=lo, sup=hi)

    print("PASS exact heterogeneous dense-pair dB obstruction")


if __name__ == "__main__":
    main()
