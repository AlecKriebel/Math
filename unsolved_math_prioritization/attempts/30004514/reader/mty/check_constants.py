"""Exact checks plus optional quadrature diagnostics for the authored MTY audit.

These checks do not replace the all-direction argument or prove existence of the
intermediate-value parameters. No source text or datasets are used.
"""
import json
from pathlib import Path

import mpmath as mp
import sympy as sp


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def main():
    a = sp.Rational(1, 100)
    b = a**-2 - 1
    t = sp.symbols("t", real=True)
    q = 2 * a**3 / sp.sqrt(1 + b*t*t)
    q_prime = -2*a**3*b*t/(1+b*t*t)**sp.Rational(3, 2)
    q_second = (-2*a**3*b/(1+b*t*t)**sp.Rational(3, 2)
                + 6*a**3*b*b*t*t/(1+b*t*t)**sp.Rational(5, 2))
    require(sp.simplify(sp.diff(q, t) - q_prime) == 0, "q first derivative")
    require(sp.simplify(sp.diff(q, t, 2) - q_second) == 0, "q second derivative")
    margin = 1 - 2*a**3 - 8*a - 2*a*a
    require(margin == sp.Rational(459899, 500000), "convexity margin")
    require(margin > 0, "positive convexity margin")
    delta = a*a/(4*(1-a*a))
    require(delta == sp.Rational(1, 39996), "cap width")
    cap_denominator = 1 - (1-a*a)*(1-delta)
    require(cap_denominator == 5*a*a/4, "cap denominator bound")
    cap_weight = 1 - 2*a**4/cap_denominator**2
    require(cap_weight == -sp.Rational(7, 25), "cap inverse-transform sign")
    omega = 2*sp.pi**2
    w_m = (1 - 2*a**4/(1-(1-a*a)*t*t)**2)/omega
    require(sp.simplify(w_m.subs(t, 1) + 1/omega) == 0, "polar inverse value")

    eigenvalues = []
    for k in range(13):
        gegenbauer = sp.gegenbauer(2*k, sp.Rational(3, 2), t)
        from_zonal = sp.cancel(gegenbauer.subs(t, 0)/gegenbauer.subs(t, 1))
        from_catalan = (-1)**k * sp.catalan(k)/4**k
        require(sp.simplify(from_zonal-from_catalan) == 0, f"eigenvalue {2*k}")
        require(abs(from_zonal) > 0, f"nonzero eigenvalue {2*k}")
        require(1/abs(from_zonal) <= (k+1)*(2*k+1), f"inverse bound {2*k}")
        eigenvalues.append({"degree": 2*k, "eigenvalue_div_omega": str(from_zonal)})

    radial_transform = lambda exponent: (
        2**(5-exponent)*sp.pi**sp.Rational(5, 2)
        * sp.gamma((5-exponent)/2)/sp.gamma(exponent/2))
    c1 = sp.simplify(radial_transform(sp.Integer(1)))
    c4 = sp.simplify(radial_transform(sp.Integer(4)))
    require(c1 == 16*sp.pi**2 and c4 == 2*sp.pi**3, "radial Fourier constants")
    require(sp.simplify(c1-c4) != 0, "counterexample to complementary-degree identity")

    # A numerical illustration of the exact ellipsoid identities, not a proof
    # for unsampled directions. R f at a normal with fifth coordinate u5 is
    # |S^2| integral_{-1}^1 f(sqrt(1-u5^2) z) sqrt(1-z^2) dz.
    mp.mp.dps = 60
    aa = mp.mpf(1)/100
    om = 2*mp.pi**2
    rm = lambda z: 1-2*aa**3/mp.sqrt(1+(aa**-2-1)*z*z)
    wm = lambda z: (1-2*aa**4/(1-(1-aa*aa)*z*z)**2)/om
    wh = lambda z: (1-(1+3*z*z)**-2)/om
    hh = lambda z: 1-(4-3*z*z)**mp.mpf("-0.5")
    split = [mp.mpf(x) for x in ["0", ".8", ".95", ".99", ".999", ".9999", ".99999", "1"]]
    def radon(fn, u5):
        s = mp.sqrt(1-u5*u5)
        return 8*mp.pi*mp.quad(lambda z: fn(s*z)*mp.sqrt(1-z*z), split)
    quadrature = []
    for u in ["0", ".2", ".9", ".9999", "1"]:
        u5 = mp.mpf(u)
        em = abs(radon(wm, u5)-rm(u5))
        eh = abs(radon(wh, u5)-hh(u5))
        require(em < mp.mpf("1e-45"), f"M quadrature diagnostic {u}")
        require(eh < mp.mpf("1e-45"), f"H quadrature diagnostic {u}")
        quadrature.append({"u5": u, "abs_error_RwM": mp.nstr(em, 8),
                           "abs_error_RwH": mp.nstr(eh, 8)})

    result = {
        "status": "PASS",
        "proof_role": "diagnostics_only; rigorous global proof is in the authored verification",
        "seed_parameter": str(a),
        "convexity_margin_lower_bound": str(margin),
        "cap_delta": str(delta),
        "omega_times_cap_weight_upper_bound": str(cap_weight),
        "fourier_r_minus_1_constant": str(c1),
        "fourier_r_minus_4_constant": str(c4),
        "inverse_radon_eigenvalue_checks": eigenvalues,
        "ellipsoid_transform_quadrature": quadrature,
    }
    destination = Path(__file__).with_name("DIAGNOSTIC_RESULTS.json")
    destination.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
