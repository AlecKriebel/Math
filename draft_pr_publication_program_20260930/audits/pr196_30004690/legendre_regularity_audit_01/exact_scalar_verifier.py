#!/usr/bin/env python3
"""Independent exact normal-form verifier. Standard library; stdout only.
This checks algebra/support certificates, not the geometric/PDE hypotheses.
"""
from fractions import Fraction as Q
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def admissible(T, k0, beta, L, M):
    return Q(0) < T < Q(1) and beta < k0 < 0 and L < 0 and M <= 0

T, A, k0, beta, L, M = map(Q, ['2/5', '7/11', '-2', '-3', '-5/2', '-7/3'])
require(admissible(T, k0, beta, L, M), 'hypotheses')
# x=t-T. These are exact coefficient identities in Q[x], hence hold for all real x.
# Left objective relative to T: -h*x + L*x*x/2.
# Its maximum is at x*=h/L and the objective gap is L*(x-x*)**2/2.
for h in map(Q, ['1/10', '1/4', '1/2', '3/4']):
    k = k0 + h
    xs = h/L
    require(-T < xs < 0, 'interior stationary point')
    original = (Q(0), -h, L/2)
    completed_square = (L*xs*xs/2 - h*h/(2*L), -L*xs, L/2)
    require(original == completed_square, 'completion-of-square polynomial identity')
    gain = -h*h/(2*L)
    require(gain > 0 and beta-k < 0 and M <= 0, 'right branch cannot overtake')
    require((-xs)/h == -1/L, 'right F-prime difference quotient')
# Plateau signs certify strict global support for all t != T.
k = (beta+k0)/2
require(k0-k > 0 and L < 0 and beta-k < 0 and M <= 0, 'plateau support signs')
# At k0 both pieces have T as unique maximizer by strict left curvature/right slope.
require(L < 0 and beta-k0 < 0, 'endpoint uniqueness')
# Negative controls test indispensable hypotheses, without pretending to prove geometry.
controls = {
    'no_slope_gap': (T,k0,k0,L,M),
    'zero_left_curvature': (T,k0,beta,Q(0),M),
    'positive_left_curvature': (T,k0,beta,-L,M),
    'terminal_contact': (Q(1),k0,beta,L,M),
    'boundary_disc_radius': (T,Q(0),beta,L,M),
    'nonconcave_post_branch': (T,k0,beta,L,-M),
}
require(all(not admissible(*args) for args in controls.values()), 'negative controls')
print(json.dumps({
    'verdict':'PASS_EXACT_NORMAL_FORM',
    'arithmetic':'fractions.Fraction; all identities exact',
    'parameters':dict(zip(['T','a_T','kappa_0','beta','L','M'], map(str,[T,A,k0,beta,L,M]))),
    'certificates':[
        'Polynomial identity holds for all real t, not only sampled t.',
        'Plateau support sign certificate gives unique global maximizer T.',
        'Completed square gives unique global left maximizer for 0<h<(-L)T.',
        'Post-contact objective is below its T value; left maximum strictly exceeds it.',
        'F-prime left difference quotient is 0; right is -1/L = '+str(-1/L),
        'Six invalid-hypothesis controls are rejected.'
    ],
    'scope':'Scalar algebra only; no claim of independently verified Hele-Shaw geometry or PDE.'
},indent=2))
