#!/usr/bin/env python3
"""Exact algebra checks only, not a formal verification of the theorem.

No network calls or file writes. Requires an already available SymPy.
"""
import json
import sympy as sp

r = sp.symbols("r", positive=True)
t, s, sigma = sp.symbols("t s sigma", real=True)
Q = sp.symbols("Q", real=True)
k = sp.symbols("k", positive=True)
m = sp.symbols("m", nonnegative=True)
A, B = sp.symbols("A B", real=True)
V = sp.Function("V")(r)
w = sp.Function("w")(r)
U = sp.Function("U")(t)
F = sp.Function("F")

def zero(expr):
    return sp.simplify(sp.expand(expr)) == 0

p = r**(Q-1)*V
correction = (Q-1)*(r**(Q-3)*V-r**(Q-2)*sp.diff(V,r))
radial_integrand = p*(sp.diff(w,r)+(Q-1)*w/r)**2-correction*w**2-p*sp.diff(w,r)**2
total_derivative = sp.diff((Q-1)*r**(Q-2)*V*w**2,r)

V_t = sp.exp(2*t)*U
V_prime = sp.exp(-t)*sp.diff(V_t,t)
V_second = sp.exp(-t)*sp.diff(V_prime,t)
side = (Q-5)*sp.exp(-2*t)*V_t+3*sp.exp(-t)*V_prime-V_second

Y = A*sp.cosh(k*s)+B/k*sp.sinh(k*s)-sp.Integral(
    sp.sinh(k*(s-sigma))*F(sigma)/k,(sigma,0,s)
)

checks = {
    "radial_core_defect_is_exact_total_derivative": zero(radial_integrand-total_derivative),
    "Euler_side_condition_transform": zero(side-((Q-1)*U-sp.diff(U,t,2))),
    "variation_of_constants_negative_forcing": zero(sp.diff(Y,s,2)-k**2*Y+F(s)),
    "variation_initial_value": zero(Y.subs(s,0)-A),
    "variation_initial_derivative": zero(sp.diff(Y,s).subs(s,0)-B),
    "unit_integral_bump_derivative_scaling_exponent": zero((Q+1-k)-4+1-(Q-2-k)),
    "threshold_square_gap_Q_equals_m_plus_4": zero(((Q-2)**2-(Q-1)).subs(Q,m+4)-(m**2+3*m+1)),
    "threshold_square_gap_positive": bool((m**2+3*m+1).is_positive),
    "historical_Q3_exponent_negative": bool((1-sp.sqrt(2)).is_negative),
}
mutant_rejections = {
    "reversing_Vprime_correction_rejected": not zero(
        p*(sp.diff(w,r)+(Q-1)*w/r)**2
        -(Q-1)*(r**(Q-3)*V+r**(Q-2)*sp.diff(V,r))*w**2
        -p*sp.diff(w,r)**2-total_derivative
    ),
    "wrong_Euler_constant_Q_minus_5_rejected": not zero(side-((Q-5)*U-sp.diff(U,t,2))),
    "missing_unit_integral_normalization_rejected": not zero((Q+1-k)-2+1-(Q-2-k)),
}
checks = {key:bool(value) for key,value in checks.items()}
mutant_rejections = {key:bool(value) for key,value in mutant_rejections.items()}
report = {
    "scope":"Exact symbolic identities only; support, growth, sign, and global positivity are proved in the manuscript.",
    "sympy_version":sp.__version__,
    "checks":checks,
    "deliberately_incorrect_formula_rejections":mutant_rejections,
    "all_checks_pass":all(checks.values()) and all(mutant_rejections.values()),
}
print(json.dumps(report,indent=2,sort_keys=True))
raise SystemExit(0 if report["all_checks_pass"] else 1)
