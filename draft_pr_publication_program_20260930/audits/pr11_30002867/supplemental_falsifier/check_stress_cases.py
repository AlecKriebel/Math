#!/usr/bin/env python3
"""Exact identities stress-testing the optional supplemental proof.

Run with an environment containing SymPy. This script verifies polynomial
identities only; the universal argument is checked in REPORT.md.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

x, y = sp.symbols("x y")
checks: dict[str, object] = {"sympy_version": sp.__version__}

def equal(lhs, rhs):
    return sp.expand(lhs - rhs) == 0

# I=(x,y); f1=y+y², f2=x+y². The bad point over J=(x) is (0,-1).
f1, f2, g = y + y**2, x + y**2, 1 + x
checks["maximal_ideal_case"] = {
    "bad_point_crt_value": (y**2).subs({x: 0, y: -1}) == 1,
    "g_times_x_membership": equal(g*x, (-x-y)*f1 + (1+x+y)*f2),
    "g_times_y_membership": equal(g*y, (1-y)*f1 + y*f2),
    "cover_identity": equal(g-x, 1),
    "extraneous_point_survives_away_from_J": f1.subs({x: -1, y: -1}) == 0 and f2.subs({x: -1, y: -1}) == 0,
}
u1, u2 = (-x-y)/(g*x), (1+x+y)/(g*x)
U = sp.Matrix([[u1, -f2], [u2, f1]])
checks["rank_two_overlap"] = {
    "determinant_one": sp.cancel(U.det()-1) == 0,
    "row_completion": all(sp.cancel(a-b) == 0 for a,b in zip((sp.Matrix([[f1,f2]])*U), [1,0])),
}

# I=(x,y)², r=3, length(R/I)=3, J=(x²). h=y³ and m=2.
f1, f2, f3 = y**2+y**6, x*y-y**4, x**2+x**4
alpha = -y**10/sp.Integer(2) + y**8/sp.Integer(2) + y**6/sp.Integer(2) - y**4 + 1
beta = (y**2-1)/sp.Integer(2)
A = (x*y+y**4)*f2
H = y**2*f3 - (1+x**2+y**6)*A
certificate_y2 = alpha*f1 + beta*H
g = 1+x**2
G = sp.groebner([f1,f2,f3], x, y)
checks["non_lci_case"] = {
    "intermediate_univariate_identity": equal(H, y**8+y**14),
    "y_squared_in_F_exact_certificate": equal(certificate_y2, y**2),
    "xy_in_F_exact_certificate": equal(f2+y**2*certificate_y2, x*y),
    "g_times_x_squared_is_f3": equal(g*x**2, f3),
    "g_times_I_remainders_zero": all(G.reduce(g*a)[1] == 0 for a in (x**2,x*y,y**2)),
    "cover_identity": equal(g-x**2, 1),
    "crt_value_at_all_bad_roots": sp.rem((-y**4)-1, y**4+1, y) == 0,
    "all_conormal_changes_in_m_fourth": all(all(sum(mon)>=4 for mon,coef in sp.Poly(a,x,y).terms()) for a in (y**6,-y**4,x**4)),
    "reduced_groebner_basis": [str(a) for a in G.polys],
}

boolean_results = []
for group in checks.values():
    if isinstance(group, dict):
        boolean_results.extend(v for v in group.values() if isinstance(v,bool))
checks["all_identity_checks_passed"] = all(boolean_results)
assert checks["all_identity_checks_passed"], checks
destination = Path(__file__).with_name("stress_results.json")
destination.write_text(json.dumps(checks, indent=2) + "\n")
print(json.dumps(checks, indent=2))
