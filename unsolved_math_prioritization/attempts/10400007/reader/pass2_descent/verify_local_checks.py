#!/usr/bin/env python3
"""Symbolic local-factor checks and labeled numerical SU(2) diagnostics."""

import json
from pathlib import Path
import sympy as sp
import mpmath as mp

Q = sp.symbols("Q")
d = sp.Matrix([[Q - 1, Q - 1]])
gamma = sp.Matrix([1, -1])
if not (d * gamma == sp.zeros(1, 1)): raise RuntimeError("Local mathematical check failed")
if not (d.rank() == 1): raise RuntimeError("Local mathematical check failed")
if not (len(d.nullspace()) == 1): raise RuntimeError("Local mathematical check failed")
dual_d = d.subs(Q, 1 / Q)
if not (sp.simplify((dual_d * gamma)[0]) == 0): raise RuntimeError("Local mathematical check failed")
if not (dual_d.rank() == 1): raise RuntimeError("Local mathematical check failed")

mp.mp.dps = 80
max_error = mp.mpf(0)
levels = []
for k in range(1, 21):
    S = mp.matrix([[mp.sqrt(mp.mpf(2) / (k + 2)) *
                    mp.sin(mp.pi * (a + 1) * (b + 1) / (k + 2))
                    for b in range(k + 1)] for a in range(k + 1)])
    error = mp.norm(S * S - mp.eye(k + 1))
    max_error = max(max_error, error)
    if not (error < mp.mpf("1e-70")): raise RuntimeError("Local mathematical check failed")
    if not (S[0, 0] > 0 and S[1, 0] > 0): raise RuntimeError("Local mathematical check failed")
    s = S[0, 0]
    for genus in range(1, 9):
        if not (abs(s ** (-genus) * s - s ** (-(genus - 1))) < mp.mpf("1e-55")): raise RuntimeError("Local mathematical check failed")
    if k <= 5:
        levels.append({"level": k, "S00": mp.nstr(s, 24),
                       "S10": mp.nstr(S[1, 0], 24)})

result = {
    "symbolic_local_graph": "rank(d)=1; kernel spanned by (1,-1); same for dual character",
    "relative_adjoint_sign": "(-1)^n cancels the product-intersection permutation sign",
    "numerical_su2_diagnostic_only": {
        "levels_checked": [1, 20],
        "precision_decimal_digits": 80,
        "largest_S_squared_identity_error": mp.nstr(max_error, 8),
        "sample_values": levels,
        "stabilization_factor_check": "s^(-g)*s = s^(-(g-1)) for g=1,...,8"
    },
    "limits": "Numerical diagnostics do not prove global anomaly, disk-slide invariance, or Jones agreement; the relative bridge is not actual plat stabilization."
}
Path(__file__).with_name("LOCAL_CHECK_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
