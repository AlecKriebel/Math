#!/usr/bin/env python3
"""Independent finite local calculations with bit-mask exterior algebra.

No prior audit verdict is used. This does not certify topology or novelty.
All checks use explicit exceptions, including in optimized execution.
"""
import json
import sys
sys.dont_write_bytecode = True
import sympy as S

u, v, x, t = S.symbols("u v x t", real=True)
coords = (u, v, x, t)
checks = []

def clean(a):
    return {m: S.simplify(c) for m, c in a.items() if S.simplify(c) != 0}

def add(*forms):
    return clean({m: sum(a.get(m, 0) for a in forms) for m in set().union(*forms)})

def scale(c, a):
    return clean({m: c*z for m, z in a.items()})

def wedge(a, b):
    out = {}
    for m, c in a.items():
        for n, d in b.items():
            if m & n:
                continue
            inversions = sum((n & ((1 << i)-1)).bit_count() for i in range(4) if m & (1 << i))
            out[m | n] = out.get(m | n, 0) + (-1)**inversions*c*d
    return clean(out)

def exterior(a):
    return add(*[wedge({1 << i: S.diff(c, q)}, {m: 1}) for m, c in a.items() for i, q in enumerate(coords)])

def require(name, condition):
    if not condition:
        raise RuntimeError(name)
    checks.append(name)

def equal(name, a, b):
    require(name, add(a, scale(-1, b)) == {})

def matrix(a):
    out = S.zeros(4)
    for m, c in a.items():
        indices = [i for i in range(4) if m & (1 << i)]
        i, j = indices
        out[i,j], out[j,i] = c, -c
    return out

alpha, beta = {5: 1, 10: -1}, {9: 1, 6: 1}
R = S.Function("R")(*coords)
gamma = add(scale(u, alpha), scale(-v, beta))
delta = exterior({2: R})
beta_e = add(beta, delta)
gamma_e = add(gamma, scale(-1, exterior({2: R*v})))
equal("general d beta_e=0 including all cutoff derivatives", exterior(beta_e), {})
equal("general d gamma_e=0 including all cutoff derivatives", exterior(gamma_e), {})
equal("d(R v dv)=v d(R dv)", exterior({2: R*v}), scale(v, delta))
equal("pointwise retained third-form relation", gamma_e, add(scale(u, alpha), scale(-v, beta_e)))
equal("alpha square sign in du dv dx dt orientation", wedge(alpha, alpha), {15: 2})
equal("beta_e square", wedge(beta_e, beta_e), {15: 2*(1-S.diff(R,x))})
equal("mixed wedge sign", wedge(alpha, beta_e), {15: S.diff(R,t)})
ru, rx, rt, q = S.symbols("ru rx rt q", real=True, nonzero=True)
D = 1-rx-rt**2/4
eta = add({9: 1, 6: 1-rx, 10: -rt, 3: ru}, scale(-rt/2, alpha))
equal("Gram orthogonalization", wedge(alpha, eta), {})
equal("Gram discriminant", wedge(eta, eta), {15: 2*D})
A, B = matrix(alpha), matrix(scale(1/q, eta))
J = -A.inv()*B
def reduce_q(z):
    return S.simplify(S.together(z).subs(q**2, D))
require("general full-cutoff J square", all(reduce_q(z) == 0 for z in J*J+S.eye(4)))
require("general full-cutoff alpha anti-invariance", all(reduce_q(z) == 0 for z in J.T*A*J+A))
require("general full-cutoff beta anti-invariance", all(reduce_q(z) == 0 for z in J.T*B*J+B))
Psi = add(alpha, scale(S.I/q, eta))
require("general decomposability", all(reduce_q(z) == 0 for z in wedge(Psi,Psi).values()))
require("general conjugate product", reduce_q(wedge(Psi,add(alpha,scale(-S.I/q,eta)))[15]-4) == 0)
# The exact sufficient box rx in [-1/4,1/4], |rt|<=1 has D>=1/2.
require("positivity bound endpoint", 1-S.Rational(1,4)-S.Rational(1,4) == S.Rational(1,2))
eps = S.symbols("epsilon", real=True, nonzero=True)
k = 1-eps*x
Jcore = J.subs({ru:0, rt:0, rx:eps*x, q:S.sqrt(k)})
def bracket(V,W):
    # A Jacobian-vector implementation differs from the preserved checkers.
    return W.jacobian(coords)*V-V.jacobian(coords)*W
U, X = S.eye(4)[:,0], S.eye(4)[:,2]
N = bracket(Jcore*U,Jcore*X)-Jcore*bracket(Jcore*U,X)-Jcore*bracket(U,Jcore*X)
require("core Nijenhuis vector", all(S.simplify(z) == 0 for z in N-S.Matrix([-eps/(2*k),0,0,0])))
phi1 = {1:1,2:S.I*S.sqrt(k)}
phi2 = {4:1,8:S.I/S.sqrt(k)}
equal("Frobenius obstruction independent exterior representation", wedge(exterior(phi1),wedge(phi1,phi2)), {15:-eps/(2*k)})
require("nonzero obstruction at origin", S.simplify(N[0].subs(x,0)+eps/2)==0 and S.simplify(N[0].subs(x,0))!=0)
for name, wrong, right in [
    ("wrong mixed-wedge sign detected", {15:-S.diff(R,t)}, wedge(alpha,beta_e)),
    ("wrong gamma perturbation sign detected", add(gamma,exterior({2:R*v})), gamma_e),
    ("omitted cutoff terms detected", {9:1,6:1-S.diff(R,x)}, beta_e),
]:
    require(name, add(wrong,scale(-1,right)) != {})
print(json.dumps({"result":"pass", "sympy_version":S.__version__, "checks":checks,
                  "canonical_math":{"alpha_square":2,"mixed_coefficient":"R_t","beta_square":"2*(1-R_x)","D":"1-R_x-R_t**2/4","N_u_x_u":"-epsilon/(2*(1-epsilon*x))","Frobenius":"-epsilon/(2*(1-epsilon*x))"},
                  "limits":"Finite local symbolic identities; no topology, global cutoff existence, novelty, or formal-proof certification."},indent=2))
