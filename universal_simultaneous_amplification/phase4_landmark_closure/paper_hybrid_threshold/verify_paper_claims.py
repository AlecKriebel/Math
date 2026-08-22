#!/usr/bin/env python3
"""Exact integration audit for the Paper II response theorem.

This audit deliberately checks only finite symbolic and rational identities.
The weak-cut, establishment, cleanup, reciprocal-invasion, and global-sweep
estimates are analytic proofs in the manuscript and certificate notes.
"""

from __future__ import annotations

from fractions import Fraction as F
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent


class VerificationError(RuntimeError):
    """Raised when an encoded paper claim does not verify."""


def require(condition: object, message: str) -> None:
    """Fail closed without relying on optimization-sensitive assertions."""
    if not bool(condition):
        raise VerificationError(message)


def reject_optimized_python() -> None:
    if sys.flags.optimize != 0:
        raise SystemExit(
            "ERROR: optimized Python is unsupported because verification "
            "checks must remain active"
        )


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
    require(
        sp.factor(pair_bd - expected_pair_bd) == 0,
        "Bd pair response does not match the claimed formula",
    )
    require(
        sp.factor(pair_db - expected_pair_db) == 0,
        "dB pair response does not match the claimed formula",
    )

    # A dilute pendant replaces one baseline core start: 1/p-1 for Bd and
    # 0/p-1 for dB.
    leaf_bd = sp.factor(1 / p - 1)
    leaf_db = sp.Integer(-1)
    require(
        leaf_bd == 1 / (r - 1),
        "Bd pendant response does not equal 1/(r-1)",
    )

    response_bd = sp.factor(pair_bd + lam * leaf_bd)
    response_db = sp.factor(pair_db + lam * leaf_db)
    expected_bd = expected_pair_bd + lam / (r - 1)
    expected_db = expected_pair_db - lam
    require(
        sp.factor(response_bd - expected_bd) == 0,
        "Bd hybrid response does not reconstruct from pair and pendant terms",
    )
    require(
        sp.factor(response_db - expected_db) == 0,
        "dB hybrid response does not reconstruct from pair and pendant terms",
    )


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
    require(
        sp.expand(gap_numerator + 2 * r * quadratic) == 0,
        "feasibility-gap numerator does not equal the claimed quadratic",
    )

    minimizing_sigma = (-r**3 + 4 * r**2 - 3 * r - 1) / (2 * (r - 1))
    minimum = sp.factor(quadratic.subs(sigma, minimizing_sigma))
    require(
        sp.factor(minimum + phase / (4 * (r - 1))) == 0,
        "quadratic minimum does not reduce to the phase polynomial",
    )

    polynomial = sp.Poly(phase, r, domain=sp.QQ)
    require(
        polynomial.count_roots(sp.Rational(1), sp.Rational(3, 2)) == 0,
        "phase polynomial has an unexpected root in (1,3/2)",
    )
    require(
        polynomial.count_roots(sp.Rational(3, 2), sp.Rational(151, 100)) == 1,
        "phase polynomial does not have exactly one root in (3/2,151/100)",
    )
    require(
        phase.subs(r, sp.Rational(3, 2)) == sp.Rational(1, 64),
        "phase-polynomial value at 3/2 is not 1/64",
    )
    require(
        phase.subs(r, sp.Rational(151, 100))
        == -sp.Rational(39866792399, 10**12),
        "phase-polynomial value at 151/100 is incorrect",
    )


def check_rational_specialization() -> None:
    r = sp.symbols("r", positive=True)
    sigma = sp.Rational(19, 137)
    lam = sp.Rational(20, 27)
    response_bd = 2 * (sigma - 1) / (1 + sigma * (r**2 - 1)) + lam / (r - 1)
    response_db = (
        2 * (r * (2 - r) - sigma) / (sigma + 2 * r * (r - 1)) - lam
    )
    endpoint = sp.Rational(3, 2)
    require(
        sp.factor(response_bd.subs(r, endpoint)) == sp.Rational(232, 17361),
        "rational Bd endpoint margin is incorrect",
    )
    require(
        sp.factor(response_db.subs(r, endpoint)) == sp.Rational(65, 12123),
        "rational dB endpoint margin is incorrect",
    )

    rational_threshold = (sp.Integer(5069) + 12 * sp.sqrt(147001)) / 6439
    require(
        sp.factor(
            6439 * rational_threshold**2 - 10138 * rational_threshold + 703
        )
        == 0,
        "rational-family threshold does not satisfy its defining quadratic",
    )
    require(
        sp.Rational(3, 2) < rational_threshold < sp.Rational(151, 100),
        "rational-family threshold lies outside its claimed interval",
    )
    require(
        sp.factor(response_bd.subs(r, rational_threshold)) > 0,
        "Bd response is not positive at the rational-family threshold",
    )

    # The explicit weak cut is a positive rational for every integer exponent.
    for exponent in range(1, 9):
        cut = F(1, 2**exponent)
        require(
            cut > 0 and cut.denominator == 2**exponent,
            f"invalid dyadic cut at exponent {exponent}: {cut}",
        )


def check_manuscript_scope() -> None:
    manuscript_bytes = (HERE / "main.tex").read_bytes()
    require(b"\r" not in manuscript_bytes, "main.tex contains CR bytes")
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
        r"I-Q(r)$ is a nonsingular $M$-matrix",
        r"\mathcal E_C=\{R\leq\delta c\}",
        r"\tau_\uparrow=\inf\{s\geq0:R_s\geq2\delta c\}",
        r"\widehat\ell_{j\wedge N}-\varepsilon(j\wedge N)",
        r"\mathbb EN\leq m/\varepsilon=O(m)",
        r"\mathbb E_{h,R,\ell}\Sigma=O(Cm)",
        r"At $\ell=0$ a resident-hub phase has no loss",
        "next pendant change or upper-strip exit",
        r"\beta_0-\frac14\geq B_0+2",
        r"\kappa\beta_0\geq B_0+2",
        r"T=\beta_0\log C",
        r"Since $m=O(C^{1/4})$",
        r"V(i)=z^i",
        r"w_{uv}/d_u",
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
        "simultaneous-amplification-beyond-three-halves-v2.0.2",
    )
    for fragment in required:
        require(
            fragment in manuscript,
            f"missing manuscript scope marker: {fragment}",
        )
    require(
        "endpoint_affine_global_v2" not in manuscript,
        "manuscript cites a forbidden discovery artifact",
    )
    require(
        "audit_core_uniformity.py" not in manuscript,
        "manuscript cites a forbidden exploratory audit",
    )
    require(r"K=A\log C" not in manuscript, "obsolete establishment scale remains")
    require(r"B\log C" not in manuscript, "obsolete cleanup scale remains")
    require(
        r"T=B_0\log C" not in manuscript,
        "obsolete dB cleanup-time coefficient remains",
    )
    require(
        r"\mathbb E\tau_{\{\ell=m\}}" not in manuscript,
        "unstopped pendant-hitting expectation remains",
    )
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
        require(
            malformed not in manuscript,
            f"malformed TeX token: {malformed}",
        )


if __name__ == "__main__":
    reject_optimized_python()
    check_module_responses()
    check_feasibility_and_tangency()
    check_rational_specialization()
    check_manuscript_scope()
    print("PASS: Paper II exact integration audit")
