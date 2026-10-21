"""Exact arithmetic certificate for consumed Roydor Lemma 3.1 bounds.

The analytic compression lower bound and ||qT(p)q|| <= 1+140*s
are cited primary inequalities. This script checks their resulting
scalar bounds, not the full geometric theorem.
"""
from fractions import Fraction as F
import json

smax = F(1, 10000)
denominator_lower = 1 - 742*smax*(1+smax*smax)
inverse_margin_lower = 106 - 733097*smax - 882*smax**2 - 733096*smax**3
forward_margin_lower = 2 - 19881*smax
assert denominator_lower > 0
assert inverse_margin_lower > 0
assert forward_margin_lower > 0

# The primary rough intermediate inferences do fail at a strict interior point.
s = F(999, 10000000)
rough_unit_inverse = 1/(1-140*s)
rough_final_inverse = 1/(1/(1+s*s)-986*s)
assert rough_unit_inverse > 1+141*s
assert rough_final_inverse > 1+988*s

def exact(x):
    return {"fraction": str(x), "decimal": float(x)}

result = {
    "status": "all_assertions_passed",
    "interval": "0 < s = sqrt(t) <= 1/10000",
    "analytic_upper_inverse": "(1+140*s)*(1+s^2)/(1-742*s*(1+s^2))",
    "inverse_cross_multiplication_margin_divided_by_s":
        "106-733097*s-882*s^2-733096*s^3",
    "inverse_margin_lower": exact(inverse_margin_lower),
    "forward_cross_multiplication_margin_divided_by_s": "2-19881*s",
    "forward_margin_lower": exact(forward_margin_lower),
    "denominator_lower": exact(denominator_lower),
    "strict_interior_counterexample_s": exact(s),
    "rough_141_inference_gap": exact(rough_unit_inverse-(1+141*s)),
    "rough_988_inference_gap": exact(rough_final_inverse-(1+988*s)),
    "scope": "exact scalar arithmetic; consumed 142 and 988 constants follow from sharper primary inequalities",
}
print(json.dumps(result, indent=2))
