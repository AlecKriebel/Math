"""Small exact checks for the geometric constants; no PDE discretization.

The rational checks are certificates. The gamma-function table is illustrative
floating-point arithmetic and is explicitly not a numerical proof of capacity.
Run with Python 3; only the standard library is required.
"""
from fractions import Fraction as F
import json
import math


def atan_interval(x, n=64):
    total = sum(((-1) ** k * x ** (2*k+1) / (2*k+1)
                 for k in range(n)), F(0))
    next_term = (-1) ** n * x ** (2*n+1) / (2*n+1)
    return min(total, total+next_term), max(total, total+next_term)


a, b = atan_interval(F(1, 5))
c, d = atan_interval(F(1, 239))
# Machin's identity: pi = 16 atan(1/5) - 4 atan(1/239).
pi_lo, pi_hi = 16*a-4*d, 16*b-4*c
lo, hi = F(7472461733, 10**10), F(7472461734, 10**10)


def sign_polynomial(x, kappa_squared):
    return x**4-kappa_squared*(1-x)**2*(2*x-1)


assert sign_polynomial(lo, pi_lo**2) < 0
assert sign_polynomial(hi, pi_hi**2) > 0
assert F(2, 3) < lo < hi < 1

# At p=4/3 the geometric coefficient kappa is exactly 4.
alo, ahi = F(2, 3), F(1)
for _ in range(100):
    mid = (alo+ahi)/2
    if sign_polynomial(mid, F(16)) < 0:
        alo = mid
    else:
        ahi = mid
assert sign_polynomial(alo, F(16)) < 0
assert sign_polynomial(ahi, F(16)) >= 0

# Exact Heron identity and area lower bound over a small rational grid.
checks = 0
for den in range(3, 61):
    for aa in range(1, den):
        aa = F(aa, den)
        if not F(2, 3) <= aa < 1:
            continue
        for bb in range(1, den):
            bb = F(bb, den)
            cc = 2-aa-bb
            if not 0 < cc <= bb <= aa:
                continue
            area_squared = (1-aa)*(1-bb)*(1-cc)
            assert area_squared >= (1-aa)**2*(2*aa-1)
            checks += 1

table = []
for p in [1.1, 4/3, 1.5, 1.75, 1.9]:
    q, r = 2-p, p-1
    k = q/(2*r)
    log_j = .5*math.log(math.pi)+math.lgamma(k/2)-math.log(4)-math.lgamma((k+1)/2)
    log_b = math.log(2*math.pi)+r*math.log(q/r)
    log_ell = math.log(2*math.pi)-1.5*q*math.log(2)-r*log_j
    log_upper = min(log_b-q*math.log(math.pi), log_ell)
    kappa = math.exp(2*(log_b-log_upper)/q)/math.pi
    left, right = 2/3, 1.
    for _ in range(70):
        x = (left+right)/2
        if x*x < kappa*(1-x)*math.sqrt(2*x-1):
            left = x
        else:
            right = x
    rho = (left+right)/2
    table.append(dict(p=p, kappa=kappa, rho=rho, capacity_factor=rho**q))

print(json.dumps({
    'status': 'all exact rational assertions passed',
    'heron_rational_cases': checks,
    'rho_bracket': [str(lo), str(hi)],
    'rho_p_four_thirds_exact_bracket': [str(alo), str(ahi)],
    'illustrative_only_float_table': table,
}, indent=2))
