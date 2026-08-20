#!/usr/bin/env python3
"""Verify the exact identities printed in the proof-exposition pass.

This verifier deliberately reconstructs every rational bridge from its
displayed numerator and denominator.  Positivity of a detached coefficient
list is not accepted as a substitute for the identity that the list is meant
to certify.
"""
from __future__ import annotations

if not __debug__:
    raise SystemExit(
        "Exact verifier requires assertions; unset PYTHONOPTIMIZE and do not use python -O"
    )

import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Optional

import sympy as sp

import core as dc
import pareto_core as pc


HERE = Path(__file__).resolve().parent


def _even_y_to_z(expr: sp.Expr, y: sp.Symbol, z: sp.Symbol) -> sp.Expr:
    """Replace every even power y**(2j) by z**j, rejecting odd powers."""

    out = sp.Integer(0)
    for (power,), coefficient in sp.Poly(sp.expand(expr), y).terms():
        assert power % 2 == 0
        out += coefficient * z ** (power // 2)
    return sp.expand(out)


def verify_reference_cubic_identities() -> None:
    m, nu, z = sp.symbols("m nu z", integer=True)

    Qcal = (
        589180301 * m**3
        - 3500015940 * m**2
        + 6930529579 * m
        - 4574434500
    )
    P_R = (
        68605040480814208768 * m**4
        - 550882186169626030957 * m**3
        + 1658612632937449670852 * m**2
        - 2219226476204103501323 * m
        + 1113379274975809565700
    )
    P_C = (
        652054120726848 * m**4
        - 5151971981328467 * m**3
        + 15265080924982572 * m**2
        - 20102347725659113 * m
        + 9927281930180400
    )
    R_m = P_R / (sp.Integer(286118780220) * (8 * m - 17) * Qcal)
    C_m = -sp.Integer(215) * P_C / (
        sp.Integer(11645046) * (8 * m - 17) * Qcal
    )

    # The displayed R_m and C_m are exactly the constant and harmonic-sum
    # coefficients in the independently reconstructed reference numerator.
    assert sp.factor(R_m - pc.N0(m, sp.Integer(0))) == 0
    assert sp.factor(C_m - (pc.N0(m, sp.Integer(1)) - pc.N0(m, sp.Integer(0)))) == 0
    assert sp.factor(Qcal - pc.Q3(m)) == 0

    q_coefficients = sp.Poly(sp.expand(Qcal.subs(m, z + 3)), z).all_coeffs()
    r_coefficients = sp.Poly(sp.expand(P_R.subs(m, z + 3)), z).all_coeffs()
    c_coefficients = sp.Poly(sp.expand(P_C.subs(m, z + 3)), z).all_coeffs()
    assert q_coefficients == [589180301, 1802606769, 1838302066, 624878904]
    assert r_coefficients == [
        68605040480814208768,
        272378299600144474259,
        405345143374782665711,
        267974666768626234894,
        66402795166594173768,
    ]
    assert c_coefficients == [
        652054120726848,
        2672677467393709,
        4108255612276161,
        2806739366867294,
        719107361052288,
    ]
    assert all(value > 0 for value in q_coefficients + r_coefficients + c_coefficients)

    L_m = (
        2729945147827667886720 * m**5
        - 27755132420474170999952 * m**4
        + 112813395868533457497683 * m**3
        - 229153280695458887386228 * m**2
        + 232620996871721820873517 * m
        - 94412163900120968220300
    )
    clearing_denominator = (
        sp.Integer(286118780220)
        * (8 * m - 17)
        * (90 * m - 179)
        * Qcal
    )
    clearing_identity = (
        R_m + C_m * (m - 2) / (90 * m - 179) - L_m / clearing_denominator
    )
    assert sp.factor(clearing_identity) == 0
    assert all(
        value > 0
        for value in sp.Poly(sp.expand(L_m.subs(m, z + 3)), z).all_coeffs()
    )

    P_ref = (
        3790502986637265684840 * nu**5
        - 974216530468600286489 * nu**4
        - 53103567440921218871 * nu**3
        - 576386186827093561 * nu**2
        + 3649732858601219 * nu
        + 55281268032918
    )
    D_ref = (
        sp.Integer(715296950550)
        * (8 * nu - 1)
        * (90 * nu + 1)
        * (
            589180301 * nu**3
            + 35065866 * nu**2
            + 629431 * nu
            + 3306
        )
    )
    lower_comparison = (
        R_m + C_m * (m - 2) / (90 * m - 179) - sp.Rational(1, 100)
    ).subs(m, nu + 2)
    assert sp.factor(lower_comparison - P_ref / D_ref) == 0
    ref_coefficients = sp.Poly(sp.expand(P_ref.subs(nu, z + 1)), z).all_coeffs()
    assert ref_coefficients == [
        3790502986637265684840,
        17978298402717728137711,
        33955060177057334483573,
        31899843595051464379292,
        14895188986348368035728,
        2762610207555043720056,
    ]
    assert all(value > 0 for value in ref_coefficients)


def verify_gauge_identities() -> None:
    nu, harmonic, L, y = sp.symbols("nu harmonic L y", positive=True)
    m = nu + 2
    A_tau = (
        1494249120 * harmonic * L * nu**2
        - 69786990 * harmonic * L * nu
        + 108738630 * L * nu**2
        + 1214388 * L * nu
        - 8521 * L
        - 125249670 * nu**2
        + 1031940 * nu
    )
    B_tau = 32760 * harmonic * L * nu + 32760 * L * nu**2 + 4 * L - 4095 * nu
    tau = -A_tau / (sp.Integer(15876) * (8 * nu - 1) * B_tau)
    assert sp.factor(tau - pc.tau_formula(m, harmonic, L)) == 0

    derivative_harmonic = (
        -sp.Integer(4225)
        * L
        * nu**2
        * (182448 * L * nu + 1008 * L - 7513)
        / (2 * B_tau**2)
    )
    derivative_L = (
        -sp.Integer(65)
        * nu
        * (
            -61531470 * harmonic * nu
            + 125249670 * nu**2
            + 1031940 * nu
            - 7513
        )
        / (252 * B_tau**2)
    )
    assert sp.factor(sp.diff(tau, harmonic) - derivative_harmonic) == 0
    assert sp.factor(sp.diff(tau, L) - derivative_L) == 0

    P_up = (
        -sp.Rational(189709065, 2) * nu**3
        - 507201030 * nu**2
        - 935658 * nu
        + 58481
    )
    assert sp.diff(P_up, nu) == (
        -sp.Rational(569127195, 2) * nu**2
        - 1014402060 * nu
        - 935658
    )
    assert P_up.subs(nu, 2) == -2789453215

    # Recover the exact endpoint comparison.  With y^2=3*nu, the sign of
    # tau(1/91,1/y)-1/20 is the sign of P below because its other denominator
    # factors are positive except for the displayed negative D_inner.
    endpoint_difference = sp.factor(
        tau.subs({harmonic: sp.Rational(1, 91), L: 1 / y})
        - sp.Rational(1, 20)
    )
    P = (
        -1040195520 * nu**3
        + 756272790 * nu**2 * y
        - 507201030 * nu**2
        - 21412755 * nu * y
        - 935658 * nu
        + 58481
    )
    D_inner = -32760 * nu**2 + 4095 * nu * y - 360 * nu - 4
    expected_difference = -P / (sp.Integer(79380) * (8 * nu - 1) * D_inner)
    assert sp.factor(endpoint_difference - expected_difference) == 0

    # The exact comparisons used in the sign proof are retained as gates.
    assert sp.expand(D_inner.subs(y, 2 * nu)) < 0
    assert sp.expand(P.subs({nu: 1, y: sp.Rational(7, 4)})) < 0
    assert sp.factor(
        (
            P
            + 21412755 * nu * y
        ).subs(y, sp.Rational(5, 4) * nu)
        - P_up
    ) == 0


def verify_second_harmonic_boundary_system() -> None:
    """Reconstruct the displayed four-variable solve for ``w_2`` exactly."""

    m = sp.symbols("m", integer=True, positive=True)
    Qcal = (
        589180301 * m**3
        - 3500015940 * m**2
        + 6930529579 * m
        - 4574434500
    )
    K = lambda i: 91 * m - 181 - i
    T_last = sp.factor(
        K(m - 4) * K(m - 3) * K(m - 2) * K(m - 1)
        / (K(-1) * K(0) * K(1) * K(2))
    )
    boundary_matrix = sp.Matrix(
        [
            [-sp.Rational(218, 63), -T_last, -1, 2],
            [-1, -(1 + 4 / K(2)), 2, 0],
            [1, 2 * T_last, -sp.Rational(39, 7), 2],
            [2, 0, 2, -sp.Rational(244, 45)],
        ]
    )
    displayed_determinant = (
        sp.Integer(64)
        * Qcal
        / (
            sp.Integer(6615)
            * (91 * m - 183)
            * (91 * m - 181)
            * (91 * m - 180)
        )
    )
    assert sp.factor(boundary_matrix.det() - displayed_determinant) == 0
    shifted_Q = sp.Poly(sp.expand(Qcal.subs(m, sp.Symbol("u") + 3)))
    assert shifted_Q.all_coeffs() == [589180301, 1802606769, 1838302066, 624878904]

    # Verify that the displayed right-hand side is exactly what remains after
    # substituting the interior recurrence into the four boundary rows.  The
    # base dimension m=3 is included: then the recurrence range is empty and
    # T_{m-1}=T_2=1, so the same four-variable system still applies.
    for dimension in (3, 4, 5, 6, 8, 10):
        r, d, _ = dc.selected(dimension)
        D = sp.diag(*d)
        b2 = -sp.Rational(1, 4) * dc.B(dimension, r, r)
        sigma = sp.Rational(1, 126 * (dimension - 2))
        T = dc.T(dimension, dimension - 1)
        K2 = dc.K(dimension, 2)
        Klast = dc.K(dimension, dimension - 1)
        M = boundary_matrix.subs(m, dimension)
        rhs = sp.Matrix(
            [
                b2[0] + T * sigma * K2 / 3 - sigma * Klast / 3,
                b2[1],
                b2[dimension - 1]
                - 2 * T * sigma * K2 / 3
                + 2 * sigma * Klast / 3,
                b2[dimension],
            ]
        )
        w2 = dc.w2(dimension)
        boundary_values = sp.Matrix([w2[0], w2[1], w2[dimension - 1], w2[dimension]])
        assert sp.simplify(M * boundary_values - rhs) == sp.zeros(4, 1)
        assert sp.simplify(M.inv() * rhs - boundary_values) == sp.zeros(4, 1)
        for i in range(3, dimension):
            recurrence_value = (
                dc.T(dimension, i) * (w2[1] + sigma * K2 / 3)
                - sigma * dc.K(dimension, i) / 3
            )
            assert sp.factor(w2[i - 1] - recurrence_value) == 0
        assert sp.simplify((dc.Avec(dimension) - 4 * D) * w2 - b2) == sp.zeros(
            dimension + 1, 1
        )


def verify_modulus_source_polynomials(
    unit_certificate: Optional[Path] = None,
    pareto_certificate: Optional[Path] = None,
) -> None:
    x, y, z, s, A = sp.symbols("x y z s A", real=True)
    lam = x + sp.I * y
    t = 1 + s
    g1 = lam + 2 + sp.Rational(23, 63) * t
    gm = lam + 5 + sp.Rational(1, 7) * t
    gZ = lam + 4 + sp.Rational(16, 45) * t
    F = sp.expand(g1 * gm * gZ - 4 * g1 - 4 * gm + gZ)
    G = sp.expand(gZ * (4 * g1 + gm) - 36)
    modulus_F = _even_y_to_z(F * sp.conjugate(F), y, z)
    modulus_G = _even_y_to_z(G * sp.conjugate(G), y, z)

    E77 = sp.Poly(
        sp.expand((sp.Rational(91, 90) ** 2 + z) * modulus_F - modulus_G),
        x,
        z,
        s,
    )
    if unit_certificate is None:
        unit_certificate = HERE / "improved_modulus_certificate.json"
    if pareto_certificate is None:
        pareto_certificate = HERE / "pareto_all_m_certificate.json"
    unit_data = json.loads(unit_certificate.read_text())
    unit_section = unit_data["improved_mode"]
    unit_terms = {
        tuple(term["powers"]): sp.Rational(term["coefficient"])
        for term in unit_section["terms"]
    }
    assert unit_section["term_count"] == 77 == len(E77.terms())
    assert unit_terms == {monomial: coefficient for monomial, coefficient in E77.terms()}
    assert all(coefficient > 0 for coefficient in unit_terms.values())
    assert E77.coeff_monomial(x) > 0
    assert E77.coeff_monomial(z) > 0
    assert E77.coeff_monomial(s) > 0

    E84 = sp.Poly(
        sp.expand(
            sp.Rational(91, 90) ** 2
            * (1 + A * x + sp.Rational(1, 3) * z)
            * modulus_F
            - modulus_G
        ),
        x,
        z,
        s,
    )
    pareto_data = json.loads(pareto_certificate.read_text())
    spatial_section = pareto_data["modulus"]["spatial"]
    spatial_terms = {
        tuple(term["powers"]): [
            sp.Rational(value) for value in term["coefficient_in_A_ascending"]
        ]
        for term in spatial_section["terms"]
    }
    assert spatial_section["term_count"] == 84 == len(E84.terms())
    for monomial, coefficient in E84.terms():
        actual = list(reversed(sp.Poly(coefficient, A).all_coeffs()))
        assert spatial_terms[monomial] == actual
        assert all(value >= 0 for value in actual) and any(value > 0 for value in actual)
    assert E84.coeff_monomial(x).subs(A, 1) > 0
    assert E84.coeff_monomial(z).subs(A, 1) > 0
    assert E84.coeff_monomial(s).subs(A, 1) > 0


def verify_contrast_product_identity() -> None:
    m, nu, L = sp.symbols("m nu L", positive=True)
    certificate = json.loads((HERE / "frontier_certificate.json").read_text())
    family = certificate["pareto_family"]
    local = {"r": nu, "L": L, "sqrt": sp.sqrt}
    chi_D = sp.sympify(family["chi_D"], locals=local)
    chi_H = sp.sympify(family["chi_H"], locals=local)
    recorded_product = sp.sympify(family["product"], locals=local)
    chi_D_unit = sp.Rational(23, 63) * (91 * m - 183)
    assert sp.factor(chi_D * chi_H - recorded_product) == 0
    assert sp.factor((chi_D * chi_H).subs(nu, m - 2) - chi_D_unit) == 0


def verify_printed_scalar_table(sign_table: Optional[Path] = None) -> None:
    """Tie every generated signed/scalar coefficient row to exact values."""

    if sign_table is None:
        sign_table = HERE.parent / "data" / "sign_certificate_tables.tex"
    result = subprocess.run(
        [
            sys.executable,
            str(HERE.parent / "computation" / "generate_sign_certificate_tables.py"),
            "--check-sign-table",
            str(sign_table),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    text = sign_table.read_text()
    rows = (
        (
            "Unit-profile boundary denominator.",
            [589180301, 1802606769, 1838302066, 624878904],
        ),
        (
            "Unit-profile critical-denominator bound.",
            [633906000, 1311540570, 678120443],
        ),
        (
            "Unit-profile cubic numerator lower bound.",
            [
                2729945147827667886720,
                13194044796940847300848,
                25446870127333515303059,
                24475321329207325509911,
                11736484608366875120374,
                2243933770033305838488,
            ],
        ),
        (
            "Reference coefficient $R_m$.",
            [
                68605040480814208768,
                272378299600144474259,
                405345143374782665711,
                267974666768626234894,
                66402795166594173768,
            ],
        ),
        (
            "Unit-profile coefficient $C_m$.",
            [
                652054120726848,
                2672677467393709,
                4108255612276161,
                2806739366867294,
                719107361052288,
            ],
        ),
        (
            "Reference cubic margin.",
            [
                3790502986637265684840,
                17978298402717728137711,
                33955060177057334483573,
                31899843595051464379292,
                14895188986348368035728,
                2762610207555043720056,
            ],
        ),
        (
            "Gauge upper-bound tail.",
            [sp.Rational(-189709065, 2), -507201030, -935658, 58481],
        ),
    )
    for title, expected in rows:
        marker = rf"\paragraph{{{title}}}"
        start = text.index(marker)
        end = text.find(r"\paragraph{", start + len(marker))
        block = text[start : len(text) if end < 0 else end]
        gathered = re.search(
            r"\\begin\{gathered\}(.*?)\\end\{gathered\}", block, re.S
        )
        assert gathered is not None
        printed = [sp.Rational(token) for token in re.findall(r"-?\d+(?:/\d+)?", gathered.group(1))]
        assert printed == expected
        flat_block = " ".join(block.split())
        assert "descending powers" in flat_block
        assert "external" in flat_block
        assert "positive" in flat_block or "negative" in flat_block

    assert "This sign is certified separately from $P_C$" in text
    assert r"S_m=-\frac{4(1760850\mathfrak h_m-10253)}{462105}" in text
    assert r"\eqref{eq:Lmpoly}" in text
    compact = "".join(text.split())
    exact_formula_fragments = (
        r"\mathcalQ_m=589180301m^3-3500015940m^2+6930529579m-4574434500",
        r"L_m={}&2729945147827667886720m^5-27755132420474170999952m^4\\&+112813395868533457497683m^3-229153280695458887386228m^2\\&+232620996871721820873517m-94412163900120968220300",
        r"P_R(m)={}&68605040480814208768m^4-550882186169626030957m^3\\&+1658612632937449670852m^2-2219226476204103501323m\\&+1113379274975809565700",
        r"R_m=\frac{P_R(m)}{286118780220(8m-17)\mathcalQ_m}",
        r"P_C(m)={}&652054120726848m^4-5151971981328467m^3\\&+15265080924982572m^2-20102347725659113m+9927281930180400",
        r"C_m=-\frac{215P_C(m)}{11645046(8m-17)\mathcalQ_m}",
        r"R_m+C_m\frac{m-2}{90m-179}=\frac{L_m}{286118780220(8m-17)(90m-179)\mathcalQ_m}",
        r"P_{\rmref}(\nu)={}&3790502986637265684840\nu^5-974216530468600286489\nu^4\\&-53103567440921218871\nu^3-576386186827093561\nu^2\\&+3649732858601219\nu+55281268032918",
        r"D_{\rmref}(\nu)=715296950550(8\nu-1)(90\nu+1)(589180301\nu^3+35065866\nu^2+629431\nu+3306)",
        r"N_m^{\rmref}-\frac1{100}\ge\frac{P_{\rmref}(\nu)}{D_{\rmref}(\nu)}",
        r"\tau_m(L)=-\frac{A_\tau}{15876(8\nu-1)B_\tau}",
        r"A_\tau={}&1494249120\mathfrakh_mL\nu^2-69786990\mathfrakh_mL\nu+108738630L\nu^2\\&+1214388L\nu-8521L-125249670\nu^2+1031940\nu",
        r"B_\tau=32760\mathfrakh_mL\nu+32760L\nu^2+4L-4095\nu",
        r"P_{\rmup}(\nu)=-\frac{189709065}{2}\nu^3-507201030\nu^2-935658\nu+58481",
    )
    for fragment in exact_formula_fragments:
        assert fragment in compact


def verify_printed_modulus_table(certificate_table: Optional[Path] = None) -> None:
    """Require the displayed 35/77/22/84 tables to match exact generation."""

    if certificate_table is None:
        certificate_table = HERE.parent / "data" / "certificate_tables.tex"
    result = subprocess.run(
        [
            sys.executable,
            str(HERE.parent / "computation" / "generate_tables.py"),
            "--check-certificate-table",
            str(certificate_table),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def verify_printed_triad_table(triad_table: Optional[Path] = None) -> None:
    """Require every printed boundary-triad Routh coefficient to be exact."""

    if triad_table is None:
        triad_table = HERE.parent / "data" / "triad_routh_gap.tex"
    result = subprocess.run(
        [
            sys.executable,
            str(HERE.parent / "computation" / "generate_sign_certificate_tables.py"),
            "--check-triad-table",
            str(triad_table),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def verify() -> None:
    verify_reference_cubic_identities()
    verify_gauge_identities()
    verify_second_harmonic_boundary_system()
    verify_modulus_source_polynomials()
    verify_contrast_product_identity()
    project_root = HERE.parent
    printed_inputs = (
        project_root / "data" / "sign_certificate_tables.tex",
        project_root / "data" / "certificate_tables.tex",
        project_root / "data" / "triad_routh_gap.tex",
        project_root / "computation" / "generate_sign_certificate_tables.py",
        project_root / "computation" / "generate_tables.py",
    )
    if all(path.is_file() for path in printed_inputs):
        verify_printed_scalar_table()
        verify_printed_modulus_table()
        verify_printed_triad_table()
    elif not any(path.exists() for path in printed_inputs):
        # Minimal specialist packets intentionally ship no manuscript tables or
        # table generators.  Their verifier still checks every exact identity
        # and source polynomial above; artifact freshness is enforced in the
        # canonical and portable repositories where those artifacts exist.
        print("PRINTED_TABLE_FRESHNESS_NOT_APPLICABLE_MINIMAL_PACKET")
    else:
        missing = [str(path) for path in printed_inputs if not path.is_file()]
        raise AssertionError("incomplete printed-table audit inputs: " + ", ".join(missing))


if __name__ == "__main__":
    verify()
    print("VERIFY_EXPOSITION_IDENTITIES_PASS")
