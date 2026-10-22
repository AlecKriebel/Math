#!/usr/bin/env python3
"""Exact algebra only; does not certify localized tests or global positivity.

No network calls or file writes. Requires an already available SymPy.
"""
import json
import sympy as sp

r = sp.symbols("r", positive=True)
p, q, g, w = (sp.Function(name)(r) for name in ("p", "q", "g", "w"))
a = sp.diff(g,r)/g
K = -q-sp.diff(p*sp.diff(g,r),r)/g
q_integrand = p*sp.diff(w,r)**2-q*w**2
remainder = p*g**2*sp.diff(w/g,r)**2
total_derivative = sp.diff(p*a*w**2,r)

def zero(expr):
    return sp.simplify(sp.expand(expr)) == 0

checks = {
    "quotient_square_expansion":zero(remainder-p*(sp.diff(w,r)-a*w)**2),
    "logarithmic_derivative_coefficient":zero(
        sp.diff(p*a,r)+p*a**2-sp.diff(p*sp.diff(g,r),r)/g
    ),
    "multiplication_form_identity_modulo_total_derivative":zero(
        q_integrand-remainder-K*w**2-total_derivative
    ),
    "supersolution_sign":zero(K*g+q*g+sp.diff(p*sp.diff(g,r),r)),
}
mutants = {
    "wrong_flux_sign_rejected":not zero(
        q_integrand-remainder-(-q+sp.diff(p*sp.diff(g,r),r)/g)*w**2-total_derivative
    ),
    "missing_divisor_g_rejected":not zero(
        q_integrand-remainder-(-q-sp.diff(p*sp.diff(g,r),r))*w**2-total_derivative
    ),
}
report = {
    "scope":"Exact symbolic identities only; localized zero-mean tests and the positive exact solution are established analytically.",
    "sympy_version":sp.__version__,
    "checks":checks,
    "deliberately_incorrect_formula_rejections":mutants,
    "all_checks_pass":all(checks.values()) and all(mutants.values()),
}
print(json.dumps(report,indent=2,sort_keys=True))
raise SystemExit(0 if report["all_checks_pass"] else 1)
