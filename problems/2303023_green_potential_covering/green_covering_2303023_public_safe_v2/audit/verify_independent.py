#!/usr/bin/env python3
"""Independent finite/symbolic controls for public-safe version 2.

Requires Python 3 and SymPy. No network or remote writes. Prints JSON to stdout.
This is not a formal proof of the imported covering theorem or potential theory.
"""
from collections import Counter
from fractions import Fraction as F
import json
import math
import sys

import sympy as S

counts = Counter()
def check(name, condition):
    if not bool(condition):
        raise AssertionError(name)
    counts[name] += 1

def zero(name, expression):
    check(name, S.factor(expression) == 0)

t, m, x, y, a, q = S.symbols("t m x y a q", real=True)
p = (t - 2) / 18
b = 18 / (t - 2)
g = 27 / (t - 1)
zero("symbolic_parameter_domain", p - 1 - (t - 20) / 18)
zero("symbolic_off_cover_slack", t - (2 + 9*p*m) - (t-2)*(2-m)/2)
zero("symbolic_budget_margin", g - b - 9*(t-4)/((t-1)*(t-2)))
check("piecewise_join_at_28", g.subs(t, 28) == 1)
check("decay_limit", S.limit(g, t, S.oo) == 0)
k = S.symbols("k", integer=True, positive=True)
check("countable_enlargement_exact_total", S.summation(2**(-k), (k, 1, S.oo)) == 1)

# Independent grid, including thresholds far closer to 28 than the author's grid.
thresholds = [F(28) + F(1, 10**j) for j in (1, 2, 8, 20, 50, 100)]
thresholds += [F(n, d) for d in (1, 3, 7) for n in range(29*d, 53*d, 3)]
thresholds += [F(10**j) for j in (3, 6, 12, 30)]
for threshold in thresholds:
    P = (threshold-2)/18
    B, G = 1/P, 27/(threshold-1)
    delta = (G-B)/2
    check("rational_valid_parameter", P > 1)
    check("rational_positive_margin", 0 < delta and B+delta < G)
    for M in (F(1), F(7, 6), F(3, 2), F(199, 100), F(2)):
        check("rational_actual_supremum_slack", threshold-(2+9*P*M) == (threshold-2)*(2-M)/2 >= 0)
    for U in (F(0), F(1), threshold-F(1, 1000), threshold,
              threshold+F(1, 1000), threshold+1, threshold+2, math.inf):
        check("rational_truncation_with_infinity", (min(U, threshold+1) > threshold) == (U > threshold))
    for n in (0, 1, 2, 7, 64):
        increment = sum((delta*F(1, 2**j) for j in range(1, n+1)), F(0))
        check("finite_enlargement_empty_and_nonempty", increment == delta*(1-F(1, 2**n)) and B+increment < G)

# Deliberate error controls: each assertion confirms that a wrong variant fails.
check("negative_control_M_not_always_two", 2-min(F(1), F(30)) == 1 != 2)
check("negative_control_origin_shift", 1-F(1) == 0)
check("negative_control_truncate_at_threshold", (min(F(30), F(29)) > 29) != (F(30) > 29))
check("negative_control_wrong_parameter", 2+18*((F(29)-1)/18) > 29)
check("negative_control_wrong_constant", 2+10*((F(29)-2)/18)*2 > 29)
check("negative_control_parameter_endpoint", (F(20)-2)/18 == 1)
check("negative_control_zero_budget_margin", F(18, 4-2) == F(27, 4-1))

# Harmonic lower example: no source theorem is used in these identities.
den = (1-x)**2+y**2
H = (1-x*x-y*y)/den
c, R = t/(t+1), 1/(t+1)
zero("harmonic_laplacian", S.diff(H, x, 2)+S.diff(H, y, 2))
check("harmonic_normalization", H.subs({x:0,y:0}) == 1)
zero("harmonic_superlevel_disk_identity", 1-x*x-y*y-t*den - (t+1)*(R*R-(x-c)**2-y*y))
zero("harmonic_disk_tangent_identity", c+R-1)
for T in (F(0), F(1,7), F(1), F(28), F(29), F(10**6)):
    C, radius = T/(T+1), 1/(T+1)
    for X in [F(j, 8) for j in range(-7, 8)]:
        for Y in [F(j, 8) for j in range(-7, 8)]:
            if X*X+Y*Y >= 1:
                continue
            value = (1-X*X-Y*Y)/((1-X)**2+Y*Y)
            check("harmonic_exact_disk_membership", (value>T) == ((X-C)**2+Y*Y < radius*radius))

# Green atom lower example: q=a**t is kept separate for polynomial verification.
green_den = (1-a*x)**2+(a*y)**2
green_dist = (x-a)**2+y*y
D = 1-a*a*q*q
C = a*(1-q*q)/D
RR = q*(1-a*a)/D
zero("green_kernel_positive_identity", green_den-green_dist-(1-a*a)*(1-x*x-y*y))
zero("green_superlevel_disk_identity", q*q*green_den-green_dist-D*(RR*RR-(x-C)**2-y*y))
zero("green_right_endpoint_identity", C+RR-(a+q)/(1+a*q))
zero("green_left_endpoint_identity", C-RR-(a-q)/(1-a*q))
zero("green_unit_disk_containment_margin", 1-(C+RR)-(1-a)*(1-q)/(1+a*q))
check("green_threshold_zero_center", S.simplify(C.subs(q, 1)) == 0)
check("green_threshold_zero_radius", S.simplify(RR.subs(q, 1)) == 1)
ss = S.symbols("s", positive=True)
tt = S.symbols("tt", positive=True)
green_s = S.exp(-ss*tt)*(1-S.exp(-2*ss))/(1-S.exp(-2*(tt+1)*ss))
check("green_boundary_limit_for_all_positive_thresholds", S.simplify(S.limit(green_s, ss, 0, dir="+") - 1/(tt+1)) == 0)
check("green_fixed_atom_large_threshold_limit", S.limit(S.Rational(1,2)**t*(1-S.Rational(1,4))/(1-S.Rational(1,4)*S.Rational(1,2)**(2*t)), t, S.oo) == 0)

# Rational thresholds with exact rational q: a=base**denominator, q=base**numerator.
for T in (F(0), F(1,3), F(1), F(2), F(29), F(100)):
    for base in (F(1,2), F(3,4), F(99,100), F(999,1000)):
        A, Q = base**T.denominator, base**T.numerator
        DD = 1-A*A*Q*Q
        CC, radius = A*(1-Q*Q)/DD, Q*(1-A*A)/DD
        check("green_rational_radius_positive", DD>0 and radius>0)
        check("green_rational_containment", CC+radius <= 1 and CC-radius >= -1)
        for alpha, beta in ((F(0),F(0)),(F(1,2),F(0)),(F(0),F(1,2)),(F(1),F(0)),(F(0),F(1)),(F(3,2),F(0))):
            X, Y = CC+alpha*radius, beta*radius
            transformed = Q*Q*((1-A*X)**2+(A*Y)**2)-((X-A)**2+Y*Y)
            disk_gap = radius*radius-(X-CC)**2-Y*Y
            check("green_rational_inside_boundary_outside", transformed == DD*disk_gap and (transformed>0)==(disk_gap>0))

# Finite rational near-boundary controls supplement, but do not replace, the limit proof.
for T in (1, 2, 29, 1000):
    A = 1-F(1,10**8)
    Q = A**T
    radius = Q*(1-A*A)/(1-A*A*Q*Q)
    target = F(1,T+1)
    check("green_near_boundary_limit_control", 0 < target-radius < target*F(1,10**9))

report = {
    "status": "PASS_INDEPENDENT_CONTROLS",
    "checks_by_name": dict(sorted(counts.items())),
    "independent_assertions": sum(counts.values()),
    "independent_threshold_count": len(thresholds),
    "negative_controls": 7,
    "scope": "Exact symbolic identities, rational controls, and explicit rejected mutations. Analytic proof and source inspection are separate.",
    "dependencies": {"python": sys.version.split()[0], "sympy": S.__version__},
}

print(json.dumps(report, indent=2, sort_keys=True))
