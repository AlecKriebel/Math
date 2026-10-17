#!/usr/bin/env python3
"""Exact algebraic checks supporting, not replacing, the proof in the report."""
from fractions import Fraction as F
import json

rows = []
for alpha in [F(11,10), F(5,4), F(7,5)]:
    gain = 1/(alpha*alpha*(9-6*alpha))-F(1,3)
    factor = (alpha-1)**2*(2*alpha+1)/(3*alpha*alpha*(3-2*alpha))
    assert gain == factor and gain > 0
    positive_exponent = 6*alpha-3
    inverse_exponent = 9-6*alpha
    assert positive_exponent > inverse_exponent > 0
    assert positive_exponent-inverse_exponent == 12*(alpha-1)
    rows.append({"alpha": str(alpha), "barrier_gain_coefficient": str(gain),
                 "positive_power_R_exponent": str(positive_exponent),
                 "inverse_power_R_exponent": str(inverse_exponent)})

anisotropic = [F(3,4),F(3,4),F(9,4)]
j_exponent=sum(anisotropic)-3
assert j_exponent == F(3,4)
assert 6*(min(anisotropic)-1)>-3
assert -2*j_exponent>-3
out={"exact_rational_checks": rows,
     "anisotropic_J_exponent": str(j_exponent),
     "anisotropic_gradient_sixth_exponent": str(6*(min(anisotropic)-1)),
     "anisotropic_inverse_J_squared_exponent": str(-2*j_exponent),
     "meaning": "Algebra and radial integrability checks only; no minimizer or counterexample certification."}
print(json.dumps(out, indent=2))
