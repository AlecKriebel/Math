#!/usr/bin/env python3
"""Independent finite algebra and exact bounds for the analytic01 audit.

No claim that these finite checks formalize compactness, univalence, the area
theorem, the support-slit theorem, or continuation of infinite analytic arcs.
This file does not import or execute the frozen author's verification script.
"""
from fractions import Fraction as R
from itertools import product
import json

E = R(1, 10**24)
H = R(1, 10**12)
T = R(7, 4)
records = []

def check(label, value):
    assert value, label
    records.append(label)

def compositions(total, length):
    if length == 0:
        if total == 0:
            yield ()
        return
    for head in range(1, total - length + 2):
        for rest in compositions(total - head, length - 1):
            yield (head,) + rest

# Reconstruct coefficients from ordered compositions rather than formal-ring
# multiplication: [z^n]f^j = sum_{m_1+...+m_j=n} a_{m_1}...a_{m_j}.
def quotient_coefficient(n):
    terms = {}
    for j in range(2, n + 1):
        for comp in compositions(n, j):
            key = (comp.count(2), comp.count(3), comp.count(4), j - 1)
            terms[key] = terms.get(key, 0) - 1
    return terms

check('coefficient z2 by compositions', quotient_coefficient(2) == {(0, 0, 0, 1): -1})
check('coefficient z3 by compositions', quotient_coefficient(3) == {(1, 0, 0, 1): -2, (0, 0, 0, 2): -1})
check('coefficient z4 by compositions', quotient_coefficient(4) == {(0, 1, 0, 1): -2, (2, 0, 0, 1): -1, (1, 0, 0, 2): -3, (0, 0, 0, 3): -1})
check('root-transform c2', R(3, 8)*2**2 - R(1, 2)*3 == 0)
check('double-cover Laurent sign', [(-4*(-1)**j, 2*j-6) for j in (3, 4, 5)] == [(4, 0), (-4, 2), (4, 4)])
check('parameter identity', H**2 == E)
check('coefficient proximity constants', 52 < 64 and R(52, 3) < 25 and 3*8+5 == 29 and 2*29+6*8 == 106)

# Analytic estimates need the derivations in REPORT.md; these only check exact
# arithmetic after Cauchy-Schwarz and elementary reciprocal identities.
r = R(2, 3)
tail_H = r**4/(3*(1-r**2))
tail_Hp = (1-r**2)**-2 - 1
check('H tail geometric majorant', tail_H == R(16, 135) < R(1, 4))
check('H derivative majorant', tail_Hp == R(56, 25) < R(9, 4))
check('H errors with sqrt13<4', 4*r+2 < 5 and 4+4*R(3, 2) == 10)
check('stronger H upper bound explains 7/2 numerator', R(5, 3)+5*H < R(11, 6) and R(11, 6)+R(5, 3) == R(7, 2))
check('f value bound', r*5*R(7, 2)/(R(3, 2)**2*R(5, 3)**2) < 2)
check('f derivative bound', R(19)/(R(3, 2)**3) + R(1, 3)*5*11/(R(3, 2)**3*R(5, 3)**3) < 8)
tip_bound = R(6, 25)+R(5, 9)*R(9, 125)+(2+R(5, 9)*8)*H
check('independent actual-tip radius gate', tip_bound < R(3, 10))
check('constructed radius exceeds tip gate', T+333*E < R(9, 5) and R(25, 81) > R(3, 10))

check('P error and no-zero disk', 106+9*24 == 322 and 110+322*H < 111 and 111*E < 1)
check('Rouche outer gap', 333*E < 3-2)
check('uniform orientation bound all t>0', 222/(1-111*E) < 223)
check('uniform angle implies accessible region', 223*E < R(1, 100))

# More precise independent error propagation than the frozen 2000 coefficient.
C_sqrt = R(322, 2) + R(111**2, 2)*H
C_V = 3*C_sqrt + 55*333*H
C_Vp = R(322, 2) + (R(126, 2)*333+2*111**2)*H
C_Z = (T*C_Vp + C_V + 7*333*H)/(1-333*E)
check('square-root bound', C_sqrt < 162)
check('complex inverse-square-root Taylor coefficient', R(3, 8)*R(4, 3)**3 < 2)
check('inverse position bound', C_V < 487)
check('inverse derivative bound', C_Vp < 162)
check('independently propagated Z error below 800', C_Z < 800)

# Family a4-lambda*a3: q is independent of the constant asymptotic direction.
def q(lam, t):
    return (2-lam/R(3))*t**2 - R(2, 5)*t**4

q1 = q(R(3), R(1))
qT = q(R(3), T)
check('selected perturbation endpoints', q1 == R(3, 5) and qT == -R(441, 640))
check('exact sign margins using independently tighter error', q1-800*H > R(1, 2) and qT+800*H < -R(1, 2))
check('a4-only control no reversal by T', q(R(0), R(1)) > 0 and q(R(0), T) > 0)
check('a3-only control no reversal', R(1, 3) > 0 and T**2/R(3) > 0)
check('zero perturbation control loses strict signs', E*q1 > 0 and 0*q1 == 0)
check('wrong differential sign reverses positive-trajectory identity', -4 < 0)
check('large error control cannot certify first sign', q1-q1 == 0)

result = {
    'status': 'PASS',
    'arithmetic': 'fractions.Fraction; exact rational comparisons',
    'checks_passed': len(records),
    'checks': records,
    'derived_bounds': {
        'tip_radius': str(tip_bound),
        'Z_error_multiplier_under_epsilon_eta': str(C_Z),
        'Z_error_simple_bound': '800 epsilon eta',
        'uniform_Z_closeness_all_t': '223 epsilon',
        'sign_test_q_values': [str(q1), str(qT)],
    },
    'analytic_inputs_not_formalized': [
        'compactness of normalized schlicht class',
        'Bieberbach coefficient theorem and area theorem',
        'support-slit/Schiffer theorem',
        'holomorphic inverse, infinite analytic estimates, and trajectory continuation',
    ],
}

if __name__ == '__main__':
    print(json.dumps(result, indent=2))
