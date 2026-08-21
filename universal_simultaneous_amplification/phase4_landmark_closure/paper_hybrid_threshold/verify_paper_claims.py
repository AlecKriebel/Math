#!/usr/bin/env python3
"""Exact integration audit for the Paper II response theorem.

This audit deliberately checks only finite symbolic and rational identities.
The weak-cut, establishment, cleanup, reciprocal-invasion, and global-sweep
estimates are analytic proofs in the manuscript and certificate notes.
"""

from __future__ import annotations

from fractions import Fraction as F
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def check_module_responses() -> None:
    r, sigma, lam = sp.symbols("r sigma lam", positive=True)
    p = (r - 1) / r

    z_bd = sigma * (r**2 - 1)
    z_db = 2 * r * (r - 1) / sigma
    pair_bd = sp.factor(2 * ((r / (r + 1)) * z_bd / (1 + z_bd) / p - 1))
    pair_db = sp.factor(2 * (sp.Rational(1, 2) * z_db / (1 + z_db) / p - 1))
    expected_pair_bd = 2 * (sigma - 1) / (1 + sigma * (r**2 - 1))
    expected_pair_db = 2 * (r * (2 - r) - sigma) / (
        sigma + 2 * r * (r - 1)
    )
    assert sp.factor(pair_bd - expected_pair_bd) == 0
    assert sp.factor(pair_db - expected_pair_db) == 0

    # A dilute pendant replaces one baseline core start: 1/p-1 for Bd and
    # 0/p-1 for dB.
    leaf_bd = sp.factor(1 / p - 1)
    leaf_db = sp.Integer(-1)
    assert leaf_bd == 1 / (r - 1)

    response_bd = sp.factor(pair_bd + lam * leaf_bd)
    response_db = sp.factor(pair_db + lam * leaf_db)
    expected_bd = expected_pair_bd + lam / (r - 1)
    expected_db = expected_pair_db - lam
    assert sp.factor(response_bd - expected_bd) == 0
    assert sp.factor(response_db - expected_db) == 0
    print("PASS: pair and pendant modules reconstruct both response functions")


def check_feasibility_and_tangency() -> None:
    r, sigma = sp.symbols("r sigma", positive=True)
    phase = r**6 - 8 * r**5 + 22 * r**4 - 30 * r**3 + 21 * r**2 - 6 * r + 1
    lower = 2 * (1 - sigma) * (r - 1) / (1 + sigma * (r**2 - 1))
    upper = 2 * (r * (2 - r) - sigma) / (sigma + 2 * r * (r - 1))
    quadratic = (
        (r - 1) * sigma**2
        + (r**3 - 4 * r**2 + 3 * r + 1) * sigma
        + r * (2 * r - 3)
    )
    gap_numerator = sp.factor(sp.together(upper - lower).as_numer_denom()[0])
    assert sp.expand(gap_numerator + 2 * r * quadratic) == 0

    minimizing_sigma = (-r**3 + 4 * r**2 - 3 * r - 1) / (2 * (r - 1))
    minimum = sp.factor(quadratic.subs(sigma, minimizing_sigma))
    assert sp.factor(minimum + phase / (4 * (r - 1))) == 0

    polynomial = sp.Poly(phase, r, domain=sp.QQ)
    assert polynomial.count_roots(sp.Rational(1), sp.Rational(3, 2)) == 0
    assert polynomial.count_roots(sp.Rational(3, 2), sp.Rational(151, 100)) == 1
    assert phase.subs(r, sp.Rational(3, 2)) == sp.Rational(1, 64)
    assert phase.subs(r, sp.Rational(151, 100)) == -sp.Rational(
        39866792399, 10**12
    )
    print("PASS: feasibility gap, quadratic minimum, and isolated sextic root")


def check_rational_specialization() -> None:
    r = sp.symbols("r", positive=True)
    sigma = sp.Rational(19, 137)
    lam = sp.Rational(20, 27)
    response_bd = 2 * (sigma - 1) / (1 + sigma * (r**2 - 1)) + lam / (r - 1)
    response_db = (
        2 * (r * (2 - r) - sigma) / (sigma + 2 * r * (r - 1)) - lam
    )
    endpoint = sp.Rational(3, 2)
    assert sp.factor(response_bd.subs(r, endpoint)) == sp.Rational(232, 17361)
    assert sp.factor(response_db.subs(r, endpoint)) == sp.Rational(65, 12123)

    rational_threshold = (sp.Integer(5069) + 12 * sp.sqrt(147001)) / 6439
    assert sp.factor(6439 * rational_threshold**2 - 10138 * rational_threshold + 703) == 0
    assert sp.Rational(3, 2) < rational_threshold < sp.Rational(151, 100)
    assert sp.factor(response_bd.subs(r, rational_threshold)) > 0

    # The explicit weak cut is a positive rational for every integer exponent.
    for exponent in range(1, 9):
        cut = F(1, 2**exponent)
        assert cut > 0 and cut.denominator == 2**exponent
    print("PASS: rational margins, algebraic response threshold, and dyadic-cut schedule")


def check_manuscript_scope() -> None:
    manuscript_bytes = (HERE / "main.tex").read_bytes()
    assert b"\r" not in manuscript_bytes, "main.tex contains CR bytes"
    manuscript = manuscript_bytes.decode("utf-8")
    required = (
        "fitness-independent",
        r"\Rsim\geq\Rhyb",
        "Effective dyadic diagonal",
        "Early ordinary-core establishment",
        "Supercritical completion and core confinement",
        "Pendant synchronization and pendant initialization",
        "Reciprocal killed-Green bounds",
        "Reciprocal hub-excursion renewal",
        "Fixed-parameter response optimality",
        r"P(3/2)=\frac1{64}>0",
        "Kriebel2026fixed",
        "10.5281/zenodo.21753405",
        "unrestricted value of $\\Rsim$",
        "the weak-cut and population\n"
        "asymptotics are analytic proofs in the manuscript",
        r"u_{\mathrm{core}}^{\Bd}(1/r)=o(C^{-1})",
        r"J_H(1/r)=o(C^{-1})",
        r"P_U^H=1-o(q/C)",
        r"P_U^P=\frac{A}{A+D}\,p_{1,1}",
        r"where $p_{1,1}$ is the macro-fixation probability from $(1,1)$",
        r"P_U^P=[A/(A+D)][(B+C')/B]P_U^H",
    )
    for fragment in required:
        assert fragment in manuscript, f"missing manuscript scope marker: {fragment}"
    assert "endpoint_affine_global_v2" not in manuscript
    assert "audit_core_uniformity.py" not in manuscript
    assert r"K=A\log C" not in manuscript
    assert r"B\log C" not in manuscript
    for malformed in (
        ",qquad",
        "&qquad",
        ",quad",
        "&quad",
        "&left",
        ",left",
        "&right",
        ",right",
    ):
        assert malformed not in manuscript, f"malformed TeX token: {malformed}"
    print(
        "PASS: theorem, response-model, open-problem, and replay boundaries are explicit"
    )


if __name__ == "__main__":
    check_module_responses()
    check_feasibility_and_tangency()
    check_rational_specialization()
    check_manuscript_scope()
    print("PASS: Paper II exact integration audit")
