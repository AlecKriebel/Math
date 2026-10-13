#!/usr/bin/env python3
"""Independent all-parameter polynomial checks; standard library only.

No candidate imports and no writes to the frozen packet. These identities
supplement, rather than replace, the smooth/measure-theoretic proof.
"""
from fractions import Fraction
from itertools import permutations
import json

N = 4  # formal variables s, b=h'(E), c=h''(E), t
ZERO_EXP = (0,) * N

class Poly:
    def __init__(self, x=0):
        self.d = {k: Fraction(v) for k, v in x.items() if v} if isinstance(x, dict) else ({ZERO_EXP: Fraction(x)} if x else {})
    def __add__(self, other):
        other = cv(other); d = self.d.copy()
        for k, v in other.d.items(): d[k] = d.get(k, 0) + v
        return Poly(d)
    __radd__ = __add__
    def __neg__(self): return Poly({k: -v for k, v in self.d.items()})
    def __sub__(self, other): return self + -cv(other)
    def __rsub__(self, other): return cv(other) + -self
    def __mul__(self, other):
        other = cv(other); d = {}
        for k, v in self.d.items():
            for j, w in other.d.items():
                e = tuple(k[i] + j[i] for i in range(N))
                d[e] = d.get(e, 0) + v * w
        return Poly(d)
    __rmul__ = __mul__
    def __eq__(self, other): return self.d == cv(other).d

def cv(x): return x if isinstance(x, Poly) else Poly(x)
def var(i): return Poly({tuple(int(j == i) for j in range(N)): 1})
s, b, c, t = [var(i) for i in range(N)]
def eye(n): return [[cv(int(i == j)) for j in range(n)] for i in range(n)]
def tr(A): return list(map(list, zip(*A)))
def mm(A, B): return [[sum((x*y for x, y in zip(r, col)), cv(0)) for col in zip(*B)] for r in A]
def det(A):
    z = cv(0)
    for p in permutations(range(len(A))):
        sign = (-1) ** sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1, len(p)))
        v = cv(sign)
        for i in range(len(A)): v = v * A[i][p[i]]
        z = z + v
    return z
def frame(u):
    R = eye(4); R[1][0] = -u; return R
def shear(u, v=0):
    R = eye(4); R[1][0] = u; R[2][3] = cv(v); return R
J = [[cv(x) for x in row] for row in [[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]]]
D = shear(1)
checks = {}
def check(label, result):
    if not result: raise AssertionError(label)
    checks[label] = True

check('deck_preserves_omega', mm(mm(tr(D), J), D) == J)
check('deck_preserves_orientation', det(D) == 1)
check('global_frame_equivariance_for_all_t', mm(D, frame(t)) == frame(t-1))
check('frame_is_symplectic_for_all_t', mm(mm(tr(frame(t)), J), frame(t)) == J)
check('frame_is_nondegenerate_for_all_t', det(frame(t)) == 1)
check('omega_nondegenerate', det(J) == 1)
# Covering-space flow (x,y,t,E) -> (x,y,t+s*b(E),E).
CoverD = eye(4); CoverD[2][3] = s*c
S = shear(s*b, s*c)
check('full_derivative_in_global_frame_all_parameters', mm(CoverD, frame(t)) == mm(frame(t+s*b), S))
check('full_derivative_symplectic_all_parameters', mm(mm(tr(S), J), S) == J)
check('full_derivative_inverse_all_parameters', mm(S, shear(-s*b, -s*c)) == eye(4))
check('unit_speed_full_derivative', mm(frame(t+s), shear(s)) == frame(t))
check('Hamiltonian_contraction_all_speeds', mm([[cv(0),cv(0),b,cv(0)]], J) == [[cv(0),cv(0),cv(0),b]])
# The Pfaffian is the coefficient of omega^2 / 2 in dx dy dt dE.
check('liouville_density_is_one', J[0][1]*J[2][3]-J[0][2]*J[1][3]+J[0][3]*J[1][2] == 1)
L, R = Fraction(1,8), Fraction(3,8)
check('band_length_exactly_one_quarter', R-L == Fraction(1,4))
check('cutoff_plateau_left', 16*(L-Fraction(1,16)) == 1)
check('cutoff_plateau_right', 16*(Fraction(7,16)-R) == 1)
check('cutoff_support_away_from_circle_seam', 0 < Fraction(1,16) < L < R < Fraction(7,16) < 1)
controls = {}
Bad = eye(4); Bad[1][0] = t
BadTarget = eye(4); BadTarget[1][0] = t-1
controls['positive_t_frame_sign_fails_descent'] = mm(D,Bad) != BadTarget
controls['reverse_return_sign_fails_descent'] = mm(shear(-1),frame(t)) != frame(t-1)
controls['omitting_energy_transverse_term_fails'] = mm(CoverD,frame(t)) != mm(frame(t+s*b),shear(s*b))
controls['constant_speed_zero_shear_is_wrong'] = mm(frame(t+s),eye(4)) != frame(t)
assert all(controls.values())
print(json.dumps({'result':'PASS','symbolic_identity_checks':len(checks),'checks':checks,'negative_controls':controls,
 'limits':['Formal polynomial identities are universal in the indicated real parameters.',
 'Smooth cutoff, quotient compactness, ergodicity, spectral noncompactness, and Lyapunov limits require the written arguments.']},indent=2,sort_keys=True))
