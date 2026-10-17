#!/usr/bin/env python3
"""Authored algebra and numerical diagnostics for the WXY proof reconstruction.

These checks complement the proof; numerical quadrature does not certify it.
No third-party source text or data is embedded.
"""
import json
import math
from pathlib import Path

import scipy
import scipy.integrate as integrate
import scipy.special as special
import sympy as sp


def spectral_checks():
    x = sp.symbols("x")
    out = []
    for n in range(3, 11):
        a = sp.Rational(n - 2, 2)
        sphere_area = 2 * sp.pi ** sp.Rational(n - 1, 2) / sp.gamma(sp.Rational(n - 1, 2))
        for m in range(1, 20, 2):
            C = sp.gegenbauer(m, a, x)
            # Integrating the Gegenbauer ODE over [0,1] gives this
            # Funk-Hecke eigenvalue with unnormalized spherical area.
            lam = sphere_area * sp.diff(C, x).subs(x, 0) / (m * (m + n - 2) * C.subs(x, 1))
            claimed = sp.pi ** a * (-1) ** ((m - 1) // 2) * sp.gamma(sp.Rational(m, 2)) / sp.gamma(sp.Rational(m + n, 2))
            residual = sp.simplify(lam - claimed)
            assert residual == 0, (n, m, residual)
            out.append({"n": n, "odd_degree": m, "exact_residual": str(residual)})
    # Check the low-dimensional normalized latitude primitives exactly.
    t = sp.symbols("t", real=True)
    s3 = (3 * t - t**3) / 2
    s4 = 2 / (3 * sp.pi) * (3 * sp.asin(t) + t * (5 - 2 * t**2) * sp.sqrt(1 - t**2))
    assert sp.simplify(sp.diff(s3, t) - sp.Rational(3, 2) * (1 - t**2)) == 0
    assert sp.simplify(sp.diff(s4, t) - 16 / (3 * sp.pi) * (1 - t**2) ** sp.Rational(3, 2)) == 0
    return out


def step(z):
    if z <= 0:
        return 0.0
    if z >= 1:
        return 1.0
    # expit form avoids simultaneous underflow in the smooth-step ratio.
    return special.expit(1 / (1 - z) - 1 / z)


def angle(r):
    return math.pi * (step(6 * r - 1) + step(6 * r - 4))


def quadrature_checks():
    out = []
    for n in (3, 4, 5, 8):
        W = 0.5 * special.beta(0.5, (n + 1) / 2)
        def alpha(t):
            t = abs(t)
            s = special.betainc(0.5, (n + 1) / 2, t * t)
            return angle(s)
        re, er = integrate.quad(lambda t: 2 * (1 - t*t)**((n-1)/2) * math.cos(alpha(t)), 0, 1,
                                epsabs=2e-12, epsrel=2e-12, limit=400)
        im, ei = integrate.quad(lambda t: 2 * (1 - t*t)**((n-1)/2) * math.sin(alpha(t)), 0, 1,
                                epsabs=2e-12, epsrel=2e-12, limit=400)
        residual = math.hypot(re, im)
        assert residual < 1e-9, (n, residual)
        shift_error = max(abs(angle(r + 0.5) - angle(r) - math.pi) for r in (j/2000 for j in range(1001)))
        assert shift_error < 1e-12
        out.append({"n": n, "W": W, "weighted_phase_real": re, "weighted_phase_imag": im,
                    "residual_magnitude": residual, "quadrature_error_estimates": [er, ei],
                    "sampled_half_shift_error": shift_error})
    return out


if __name__ == "__main__":
    result = {
        "role": "Diagnostics only; the accompanying authored reconstruction supplies analytic arguments.",
        "sympy_version": sp.__version__, "scipy_version": scipy.__version__,
        "exact_spectral_checks": spectral_checks(),
        "exact_latitude_primitives_n3_n4": "passed",
        "numerical_phase_checks": quadrature_checks(),
    }
    target = Path(__file__).with_name("NORMALIZATION_CHECKS.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"exact_spectral_cases": len(result["exact_spectral_checks"]),
                      "latitude_primitives": "passed", "quadrature_dimensions": [3, 4, 5, 8],
                      "maximum_quadrature_residual": max(r["residual_magnitude"] for r in result["numerical_phase_checks"]),
                      "output": str(target)}, indent=2))
