#!/usr/bin/env python3
"""Independent rational checks of raw selected-bin implication margins.

This script checks a re-derivation from the printed inequalities. It does not
prove the force, flow, energy, or PDE premises. Standard library only.
"""
from fractions import Fraction as F
import json

eps = F(1, 100000)
beta = F(29, 25)
delta_bound = F(1, 1000)
checks = {}

# Near: 2 alpha + H/2 + 2 y < z+Delta.
# Pure-energy far implies b < H-alpha+Delta. Thus
# d*=alpha+b+y+H < 2H+y+Delta < 4z+5Delta.
delta_sharp = 4 * eps / (1 - 5 * eps)
assert delta_sharp < delta_bound
checks["delta_over_z_from_raw_near_and_energy_far"] = str(delta_sharp)

# For H<=2c, unsafe first branch and energy far imply
# H+z+6alpha < 8Delta. Nonnegative H,alpha give z<8Delta,
# impossible under the previous delta bound.
assert 8 * delta_bound < 1
checks["H_le_2c_contradiction_gap"] = str(1 - 8 * delta_bound)

# H>2c: unsafe first branch and energy far imply
# H > z/2+3(alpha+c)-4Delta.
H_lower = F(1, 2) - 4 * delta_bound
assert H_lower == F(62, 125)

# Combining with near gives 3.5alpha+1.5c+2y < .75z+3Delta.
actual_upper = F(3, 4) + 3 * delta_bound
z_actual_lower = F(3, 2) / (F(3, 2) + actual_upper)
assert actual_upper == F(753, 1000)
assert z_actual_lower == F(500, 751)
assert z_actual_lower > F(66, 100)
rounded_y_upper = F(377, 1000)
assert actual_upper / 2 < rounded_y_upper
# With c+z=1, both z-y and 1-alpha-y are greater than .623.
assert 1 - rounded_y_upper == F(623, 1000)
assert F(3, 4) > F(623, 1000)
assert F(7, 4) > F(623, 1000)
assert F(623, 1000) > F(3, 10)
checks["actual_m_phi_lower_power"] = str(F(623, 1000))

# Stable far: b < H/2-min(alpha,c)+y+.002z.
# Unsafe first branch consequently gives
# 2y > H/3 + z/3 + 2min(alpha,c) - 2Delta/3 -.004z.
middle_lower_raw = F(1, 3) - F(2, 3) * delta_bound - F(4, 1000)
middle_lower_rounded = F(328, 1000)
assert middle_lower_raw > middle_lower_rounded
# Near plus this lower bound gives 5H/6 < .673z, after
# dropping nonnegative alpha/min(alpha,c).
H_middle_upper = (1 + delta_bound - middle_lower_rounded) / F(5, 6)
assert H_middle_upper == F(2019, 2500)
alpha_plus_c_upper_raw = (H_middle_upper - H_lower) / 3
assert alpha_plus_c_upper_raw < F(105, 1000)
z_window_lower = 1 / (1 + F(105, 1000))
assert z_window_lower == F(200, 221)
assert z_window_lower > F(9, 10)
assert 1 - F(105, 1000) > F(7, 10)

# Two unsafe branches imply y > z/3-H/6-2Delta/3.
y_over_z_lower = F(1, 3) - H_middle_upper / 6 - F(2, 3) * delta_bound
assert y_over_z_lower > F(19, 100)
assert F(19, 100) * z_window_lower > F(171, 1000)
assert F(171, 1000) > F(4, 25)
# y < .377z-1.75alpha-.75c is strictly below both .49z
# and .49(1-alpha): the following are their positive coefficients.
window_upper_gap_z = F(49, 100) - rounded_y_upper
window_upper_gap_source_alpha = F(7, 4) - F(49, 100)
window_upper_gap_source_c = F(3, 4) + F(49, 100)
assert all(x > 0 for x in (
    window_upper_gap_z, window_upper_gap_source_alpha,
    window_upper_gap_source_c))
checks["stable_window_H_over_z_upper"] = str(H_middle_upper)
checks["stable_window_z_lower"] = str(z_window_lower)
checks["stable_window_y_over_z_lower"] = str(y_over_z_lower)

# Improved far and unsafe first branch give
# beta*y > H/3+z/3+2min(alpha,c)-8Delta/3.
# Near gives beta*y < beta*z/2-beta*H/4+beta*Delta/2-beta*alpha.
# Drop nonnegative min and alpha, then use Delta < .001z.
H_final_upper = (
    beta / 2 - F(1, 3) + (F(8, 3) + beta / 2) * delta_bound
) / (F(1, 3) + beta / 4)
final_gap = H_lower - H_final_upper
assert H_final_upper == F(37487, 93500)
assert final_gap == F(8889, 93500)
assert final_gap > 0
checks["final_H_over_z_lower"] = str(H_lower)
checks["final_H_over_z_upper"] = str(H_final_upper)
checks["final_exact_contradiction_gap"] = str(final_gap)

# Intermediate-angle window phi <= P^(-14/125) absorbs fixed
# C(M,A) L^7 into phi^(-(beta-1)), with one positive P power.
absorption_power = F(14, 125) * (beta - 1)
assert absorption_power == F(56, 3125) and absorption_power > 0
checks["enhanced_occupation_absorption_power"] = str(absorption_power)

# Spatial transition n0 is a positive geometric power of theta.
spatial_theta_power = (1 - 4 * eps) / (1 - 2 * eps)
spatial_lower_tail = (1 - 2 * eps) / (1 + 2 * eps)
time_radial_tail = 1 - 6 * eps / (1 - eps)
time_angular_tail = 3 - 4 * eps / (1 - eps)
assert all(x > 0 for x in (
    spatial_theta_power, spatial_lower_tail,
    time_radial_tail, time_angular_tail))
checks["spatial_transition_theta_power"] = str(spatial_theta_power)
checks["spatial_transition_lower_tail"] = str(spatial_lower_tail)
checks["time_weight_radial_tail"] = str(time_radial_tail)
checks["time_weight_angular_tail"] = str(time_angular_tail)

# The closure constants imply at most a quarter of each bootstrap
# coefficient: C_eta/M <=1/8, 2sqrt(eta)<=1/8, C_eta*M/A<=1/16,
# C_eta/sqrt(A)<=1/16, 2eta<=1/8.
assert F(1, 8) + F(1, 8) == F(1, 4)
assert F(1, 16) + F(1, 16) + F(1, 8) == F(1, 4)
checks["closure_coefficient_fraction"] = "1/4"

print(json.dumps({
    "status": "all independent exact rational assertions passed",
    "checks": checks,
    "limits": "Arithmetic implication margins only; force, energy, flow and PDE premises require separate verification."
}, indent=2))
