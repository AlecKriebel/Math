#!/usr/bin/env python3
"""Generate the sole finite-dimensional numerical source for the final release.

Every number is reconstructed from the indexed reaction family and the current
improved unit-equilibrium diffusion profile.  Exact rationals are serialized as
strings; displayed decimals are derived from those strings in downstream code.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "independent_verifier"))
import core  # current 91m improved profile
import pareto_core

MS = tuple(range(3, 11))


def qstr(x: sp.Expr) -> str:
    return str(sp.factor(x))


def dec(x: sp.Expr, digits: int = 18) -> str:
    return str(sp.N(x, digits))


def vector_strings(v: sp.Matrix | list[sp.Expr]) -> list[str]:
    return [qstr(sp.sympify(x)) for x in list(v)]


def entry(m: int) -> dict:
    A = core.Avec(m)
    r, d, ell = core.selected(m)
    D = sp.diag(*d)
    Hs = core.Hsum(m)
    ell_r_direct = sp.factor((ell.T * r)[0])
    ell_Dr_direct = sp.factor((ell.T * D * r)[0])
    ell_r_formula = sp.factor(core.ellr_formula(m, Hs))
    ell_Dr_formula = sp.factor(core.ellDr_formula(m, Hs))
    assert ell_r_direct == ell_r_formula
    assert ell_Dr_direct == ell_Dr_formula
    assert (A - D) * r == sp.zeros(m + 1, 1)
    assert (A - D).T * ell == sp.zeros(m + 1, 1)

    eta = sp.factor(ell_Dr_direct / ell_r_direct)
    numerator = sp.factor(core.N_formula(m, Hs))
    cubic = sp.factor(numerator / ell_r_direct)
    assert eta > 0 and cubic < 0
    amp_sq = sp.factor(-eta / cubic)
    nu = m - 2
    chi_unit = sp.factor(sp.Rational(23, 63) * (91 * m - 183))
    scale_endpoint = pareto_core.L0(m)
    chi_d_scale = sp.factor(sp.Rational(2093, 63) * nu * scale_endpoint)
    chi_h_scale = sp.factor(sp.Rational(91 * nu - 1, 91 * nu) / scale_endpoint)
    product = sp.factor(sp.Rational(23, 63) * (91 * nu - 1))
    assert sp.simplify(chi_d_scale * chi_h_scale - product) == 0
    assert sp.simplify(chi_unit - product) == 0
    lower = sp.sqrt(8 * nu)

    return {
        "m": m,
        "n": m + 1,
        "right_critical_vector": vector_strings(r),
        "left_critical_vector": vector_strings(ell),
        "diffusion_profile": vector_strings(d),
        "ell_dot_r": qstr(ell_r_direct),
        "ell_dot_Dr": qstr(ell_Dr_direct),
        "eta": {"exact": qstr(eta), "decimal": dec(eta)},
        "cubic": {"exact": qstr(cubic), "decimal": dec(cubic)},
        "amplitude_squared": {"exact": qstr(amp_sq), "decimal": dec(amp_sq)},
        "amplitude_coefficient": {"exact": f"sqrt({qstr(amp_sq)})", "decimal": dec(sp.sqrt(amp_sq))},
        "chi_D_unit": {"exact": qstr(chi_unit), "decimal": dec(chi_unit)},
        "chi_D_scale": {"exact": qstr(chi_d_scale), "decimal": dec(chi_d_scale)},
        "chi_H_scale": {"exact": qstr(chi_h_scale), "decimal": dec(chi_h_scale)},
        "product": {"exact": qstr(product), "decimal": dec(product)},
        "lower": {"exact": qstr(lower), "decimal": dec(lower)},
        "harmonic_sum": qstr(Hs),
        "cubic_numerator": qstr(numerator),
    }


def main() -> None:
    payload = {
        "schema": "current-profile-exact-v1",
        "profile": {
            "description": "Improved unit-equilibrium 91m profile",
            "K_i": "91*m-181-i",
            "d_1": "23/63",
            "d_i": "1/(91*m-181-i), 2<=i<=m-1",
            "d_m": "1/7",
            "d_Z": "16/45",
        },
        "normal_form_convention": "dot(A)=eta*mu*A+c*A^3+higher order; critical perturbation=A*r*cos(xi)",
        "rows": [entry(m) for m in MS],
    }
    out = ROOT / "data" / "current_profile_exact.json"
    out.write_text(json.dumps(payload, indent=2) + "\n")
    # Mandatory regression required by the repair prompt.
    row3 = payload["rows"][0]
    assert row3["ell_dot_r"] == "-7451873/924210"
    assert row3["ell_dot_Dr"] == "-71818/462105"
    assert row3["eta"]["exact"] == "143636/7451873"
    print("CURRENT_PROFILE_EXACT_DATA_PASS")
    print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
