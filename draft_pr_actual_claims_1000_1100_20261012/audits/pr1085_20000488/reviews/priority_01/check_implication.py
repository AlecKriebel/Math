"""Exact supplementary guards for the priority-audit relativistic bridge.

This checks finite algebra/constant cases, not a universal spectral theorem.
The proof and source assumptions are in DERIVATIONS.md.
"""
from fractions import Fraction as F
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


theta = F(1, 4)
factor = theta**2 / (1 - 2 * theta)**2
require(factor == F(1, 4), "HHRV theta factor")
v_bound = F(1, 5000) * F(25, 24) * F(2501, 1250)
require(v_bound == F(2501, 6000000), "bump potential comparison")
s_bound = 16 * v_bound
require(s_bound < F(1, 100), "boundary potential scaled for source theorem")
require(F(1, 100) * (F(1, 100) + 2) == F(201, 10000), "phase-volume arithmetic")
require(F(201, 10000) < F(1, 40), "integer-count margin")
require(F(1, 240) < 1, "strict count exclusion")

# For U(t)=A exp(-r t)+B exp(-s t), exact one-frequency integration.
# rho^2 = p^2 + beta^2. Completion of the rho square must match E_beta.
square_guards = 0
for beta, p, rho in [(F(3), F(4), F(5)), (F(5), F(12), F(13)),
                      (F(1), F(0), F(1)), (F(3, 5), F(4, 5), F(1))]:
    require(rho**2 == p**2 + beta**2, "Fourier mass/rho relation")
    for A in [F(-2), F(0), F(1), F(3, 2)]:
        for B in [F(-1), F(0), F(2)]:
            for r, s in [(F(1), F(2)), (F(3, 2), F(5, 2)), (rho, rho+1)]:
                integral_u2 = A*A/(2*r) + 2*A*B/(r+s) + B*B/(2*s)
                integral_dt2 = A*A*r/2 + 2*A*B*r*s/(r+s) + B*B*s/2
                trace = (A+B)**2
                shifted = integral_dt2 + (p*p+beta*beta)*integral_u2 - beta*trace
                square = ((rho-r)*A)**2/(2*r)
                square += 2*(rho-r)*(rho-s)*A*B/(r+s)
                square += ((rho-s)*B)**2/(2*s)
                require(shifted == square + (rho-beta)*trace,
                        "exact Fourier square identity")
                require(square >= 0, "square integration nonnegativity")
                square_guards += 1

# Scaling at the source phase-volume bound: for m=4 the power is integral,
# so this identity can be guarded exactly without irrational approximations.
scaling_guards = 0
for beta in [F(1, 20), F(1, 3), F(1), F(7)]:
    for C in [F(1, 100), F(1, 2), F(3)]:
        v = beta*C
        lhs = (16*v*(16*v+2*beta))**2
        rhs = beta**4 * (16*C*(16*C+2))**2
        require(lhs == rhs, "beta^m scaling of HHRV bound")
        scaling_guards += 1

print(json.dumps({
    "passed": True,
    "square_identity_exact_guards": square_guards,
    "mass_scaling_exact_guards": scaling_guards,
    "bump_v_upper": str(v_bound),
    "scaled_potential_upper": str(s_bound),
    "coarse_N_upper_under_pi_gt_one": "1/240",
    "scope": "Finite exact guards only; DERIVATIONS.md supplies the universal proof and primary theorem interface.",
}, indent=2))
