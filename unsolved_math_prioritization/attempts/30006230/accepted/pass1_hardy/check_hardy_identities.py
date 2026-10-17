#!/usr/bin/env python3
"""Narrow exact-algebra checks for HARDY_CONVERSE_PROOF.md.

This does not certify the analytical theorem, density, exhaustion, or positivity.
It makes no network calls and changes no files; JSON is printed to stdout.
Requires an already available SymPy installation.
"""
import json
import sympy as sp

r, s = sp.symbols("r s", positive=True)
t = sp.symbols("t", real=True)
theta = sp.symbols("theta", real=True)
n = sp.symbols("n", integer=True, positive=True)
us, ut = sp.symbols("u_s u_t", real=True)
rho = (s**4 + 4*t**2)**sp.Rational(1, 4)
psi = s**2/rho**2
radial_s = r*sp.sqrt(sp.sin(theta))
radial_t = r**2*sp.cos(theta)/2
det = sp.det(sp.Matrix([
    [sp.diff(radial_s, r), sp.diff(radial_s, theta)],
    [sp.diff(radial_t, r), sp.diff(radial_t, theta)],
]))

def zero(expression):
    return sp.simplify(sp.trigsimp(expression)) == 0

checks = {}
checks["polar_jacobian_signed"] = zero(det + r**2/(2*sp.sqrt(sp.sin(theta))))
checks["gauge_on_polar_coordinates_fourth_power"] = zero(radial_s**4 + 4*radial_t**2 - r**4)
checks["gauge_gradient_norm"] = zero(sp.diff(rho, s)**2 + s**2*sp.diff(rho, t)**2 - psi)
checks["homogeneous_radial_derivative"] = zero(s*sp.diff(rho, s) + 2*t*sp.diff(rho, t) - rho)
checks["gradient_projection_to_source_radial_derivative"] = zero(
    sp.diff(rho, s)*us + s**2*sp.diff(rho, t)*ut - psi*(s*us+2*t*ut)/rho
)
checks["radial_grushin_laplacian"] = zero(
    sp.diff(rho, s, 2)+(n-1)/s*sp.diff(rho, s)+s**2*sp.diff(rho, t, 2)
    -(n+1)*psi/rho
)

p, f, h = (sp.Function(name)(r) for name in ("p", "f", "h"))
q = -sp.diff(p*sp.diff(f, r), r)/f
v = f*h
checks["ground_state_integrand_total_derivative"] = zero(
    p*sp.diff(v, r)**2-q*v**2-p*f**2*sp.diff(h, r)**2
    -sp.diff(p*f*sp.diff(f, r)*h**2, r)
)

# Verify the polar powers without assumptions about fractional power simplification.
checks["unweighted_radial_measure_exponent"] = (n-1)+2 == n+1
checks["unweighted_angular_measure_exponent"] = sp.simplify((n-1)/2-sp.Rational(1,2)-(n-2)/2) == 0
checks["weighted_angular_measure_exponent"] = sp.simplify((n-2)/2+1-n/2) == 0
checks["historical_n1_angular_integrability"] = sp.Rational(-1,2) > -1 and sp.Rational(1,2) > -1
checks["exact_c2"] = zero(sp.pi*sp.integrate(sp.sin(theta), (theta, 0, sp.pi))-2*sp.pi)
checks["exact_c4"] = zero(sp.pi**2*sp.integrate(sp.sin(theta)**2, (theta, 0, sp.pi))-sp.pi**3/2)

a = sp.symbols("a", positive=True)
Q = sp.symbols("Q", real=True)
V = r**(1-Q)*(r-a)**2
W = -r**(1-Q)
checks["isolated_zero_flux_coefficient"] = zero(r**(Q-1)*V-(r-a)**2)
checks["isolated_zero_potential_coefficient"] = zero(r**(Q-1)*W+1)

mutant_rejections = {
    "omitting_jacobian_half_rejected": not zero(det+r**2/sp.sqrt(sp.sin(theta))),
    "ordinary_s_derivative_in_place_of_gauge_derivative_rejected": not zero(
        sp.diff(rho,s)*us+s**2*sp.diff(rho,t)*ut-psi*us
    ),
    "wrong_potential_sign_rejected": not zero(
        p*sp.diff(v,r)**2+q*v**2-p*f**2*sp.diff(h,r)**2
        -sp.diff(p*f*sp.diff(f,r)*h**2,r)
    ),
}
checks = {key: bool(value) for key,value in checks.items()}
mutant_rejections = {key: bool(value) for key,value in mutant_rejections.items()}
report = {
    "scope": "Exact symbolic identities only; not a formal verification of the analytic proof.",
    "sympy_version": sp.__version__,
    "checks": checks,
    "deliberately_incorrect_formula_rejections": mutant_rejections,
    "all_checks_pass": all(checks.values()) and all(mutant_rejections.values()),
}
print(json.dumps(report, indent=2, sort_keys=True))
raise SystemExit(0 if report["all_checks_pass"] else 1)
