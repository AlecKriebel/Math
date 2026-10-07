#!/usr/bin/env python3
"""Exact rational audit of selected-bin exponent margins in family 362.

This certificate checks arithmetic used in an analytic contradiction. It does
not certify the force identities or the relativistic Vlasov--Maxwell theorem.
Dependencies: Python standard library only. Run from any working directory.
"""

from fractions import Fraction as F
import json


epsilon = F(1, 100000)
beta = F(29, 25)
delta_over_z = F(1, 1000)

# d_* < 4 z + 5 Delta and Delta=epsilon*d_*.
delta_sharp = 4 * epsilon / (1 - 5 * epsilon)
assert delta_sharp == F(4, 99995)
assert delta_sharp < delta_over_z

# The actual-bin exponent window, using the manuscript's conservative bounds.
actual_lower_z = F(3, 2) / (F(3, 2) + F(753, 1000))
assert actual_lower_z == F(500, 751)
assert actual_lower_z > F(66, 100)
assert F(623, 1000) > F(3, 10)

# Near selection plus the baseline far inequality.
H_middle_upper = (F(1001, 1000) - F(328, 1000)) / F(5, 6)
assert H_middle_upper == F(2019, 2500)  # .8076 exactly
assert H_middle_upper < F(81, 100)
H_lower = F(1, 2) - 4 * delta_over_z
assert H_lower == F(62, 125)
alpha_c_upper = (H_middle_upper - H_lower) / 3
assert alpha_c_upper < F(105, 1000)
z_improved_lower = 1 / (1 + F(105, 1000))
assert z_improved_lower == F(200, 221)
assert z_improved_lower > F(90, 100)
source_exponent_lower = 1 - F(105, 1000)
assert source_exponent_lower == F(895, 1000)

y_lower_ratio = F(1, 3) - H_middle_upper / 6 - 2 * delta_over_z / 3
assert y_lower_ratio > F(19, 100)
assert F(19, 100) * z_improved_lower > F(171, 1000)
assert F(171, 1000) > F(16, 100)

# Exact final contradiction. Ignore nonnegative alpha,c contributions.
# Improved far+unsafe: beta*y > H/3 + z/3 - 8*Delta/3.
# Near: beta*y < (beta/2)*z - (beta/4)*H + (beta/2)*Delta.
H_final_upper = (
    beta / 2 - F(1, 3) + (F(8, 3) + beta / 2) * delta_over_z
) / (F(1, 3) + beta / 4)
assert H_final_upper == F(37487, 93500)
margin = H_lower - H_final_upper
assert margin == F(8889, 93500)
assert margin > 0

# The paper uses looser intermediate roundings; check those too.
assert F(1, 3) - F(8, 3) * delta_over_z > F(33, 100)
assert beta / 2 * (1 + delta_over_z) < F(582, 1000)
paper_H_upper = (F(582, 1000) - F(33, 100)) / (F(1, 3) + F(29, 100))
assert paper_H_upper == F(378, 935)
assert paper_H_upper < F(41, 100) < H_lower

# Absorption margin in direction-based occupation.
absorption_power = F(14, 125) * (beta - 1)
assert absorption_power == F(56, 3125)
assert absorption_power > 0

# Positivity of angular/radial geometric tails in the time-weight estimate.
radial_exponent = 1 - 6 * epsilon / (1 - epsilon)
angular_exponent = 3 - 4 * epsilon / (1 - epsilon)
theta_exponent = (1 - 4 * epsilon) / (1 - 2 * epsilon)
assert radial_exponent > 0 and angular_exponent > 0 and theta_exponent > 0

result = {
    "status": "all exact rational assertions passed",
    "delta_over_z_sharp": str(delta_sharp),
    "baseline_H_over_z_upper": str(H_middle_upper),
    "final_H_over_z_lower": str(H_lower),
    "final_H_over_z_upper": str(H_final_upper),
    "contradiction_margin": str(margin),
    "paper_rounded_H_over_z_upper": str(paper_H_upper),
    "occupation_absorption_power": str(absorption_power),
    "limits": "arithmetic certificate only; force/PDE premises are not certified",
}
print(json.dumps(result, indent=2))
