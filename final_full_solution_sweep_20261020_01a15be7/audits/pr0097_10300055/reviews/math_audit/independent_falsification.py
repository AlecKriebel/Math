#!/usr/bin/env python3
"""Independent algebraic falsification tests. These do not prove ET or Gray."""
import hashlib, json, platform
from datetime import datetime, timezone
import sympy as sp
checks={}
def ck(k,v):
    if not bool(v): raise AssertionError(k)
    checks[k]='PASS'
A=sp.Matrix(sp.symbols('a0:3'))
W=sp.Matrix(sp.symbols('w0:3'))
K=sp.Matrix(sp.symbols('k0:3'))
s,t=sp.symbols('s t',real=True)
DA=A.cross(W)
# No constraint built into K: the sole residual is the differentiated relation.
raw=sp.expand((W+s*A).dot(K+s*DA)-W.dot(K))
ck('unconstrained_pencil_residual_exactly_s_alpha_domega',sp.expand(raw-s*A.dot(K))==0)
ck('integrability_follows_from_connection',sp.expand(A.dot(DA))==0)
ck('omega_dalpha_vanishes_from_connection',sp.expand(W.dot(DA))==0)
ck('normalized_pencil_residual_exactly_t_alpha_domega',sp.expand((A+t*W).dot(DA+t*K)-t*t*W.dot(K)-t*A.dot(K))==0)
# If A is proportional to W, alpha wedge d omega = 0 contradicts contactness.
k=sp.symbols('lambda',nonzero=True)
ck('pointwise_linear_independence',sp.expand((k*W).dot(K)-k*W.dot(K))==0)
# Coordinate construction satisfying the exact connection relation everywhere.
x,y,z=sp.symbols('x y z',real=True)
coords=(x,y,z)
def curl(V):
    return sp.Matrix([sp.diff(V[2],y)-sp.diff(V[1],z),sp.diff(V[0],z)-sp.diff(V[2],x),sp.diff(V[1],x)-sp.diff(V[0],y)])
a=sp.exp(-z)*sp.Matrix([1,-x*x/2,0])
w=sp.Matrix([0,-x,1])
ck('coordinate_connection',all(sp.simplify(v)==0 for v in curl(a)-a.cross(w)))
ck('coordinate_all_real_s_contact',sp.simplify((w+s*a).dot(curl(w+s*a)))==-1)
h=y*z+x
ck('nonconstant_shift_error_retained',sp.simplify((w+h*a).dot(curl(w+h*a))-w.dot(curl(w))-w.dot(sp.Matrix([sp.diff(h,c) for c in coords]).cross(a)))==0)
# Independent symbolic moving-boundary correction on a genuine periodic graph.
u,v,e=sp.symbols('u v epsilon',real=True)
U=sp.cos(t)+e*sp.cos(2*t)
V=sp.sin(t)+e*sp.sin(3*t)
theta=sp.Matrix([-u,0,1])
eta=theta+e*sp.Matrix([sp.sin(t)+u*v,sp.cos(t)+u,v+sp.sin(2*t)])
def pull(F):
    return sp.expand(F[0].subs({u:U,v:V}, simultaneous=True)+F[1].subs({u:U,v:V}, simultaneous=True)*sp.diff(U,t)+F[2].subs({u:U,v:V}, simultaneous=True)*sp.diff(V,t))
q=pull(eta)
chi=(1-(u-U)**2-(v-V)**2)**2
eta_hat=eta-sp.Matrix([q*chi,0,0])
ck('periodic_moving_boundary_exact_legendrian',sp.simplify(pull(eta_hat))==0)
ck('q_C1_small',sp.simplify(q.subs(e,0))==0 and sp.simplify(sp.diff(q,t).subs(e,0))==0)
for i in range(3):
    err=eta_hat[i]-theta[i]
    ck(f'correction_C0_limit_{i}',sp.simplify(err.subs(e,0))==0)
    for c in (t,u,v):
        ck(f'correction_C1_limit_{i}_{c}',sp.simplify(sp.diff(err,c).subs(e,0))==0)
# Certificate metadata separates these symbolic identities from global imported theorems.
result={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','assertions':len(checks),'python':platform.python_version(),'sympy':sp.__version__,'script_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest(),'checks':checks,'scope':'Universal polynomial identities for arbitrary pointwise jets; one periodic smoothing model. Not a numerical or finite verification of the universal global contact-topology theorem.'}
print(json.dumps(result,indent=2,sort_keys=True))
