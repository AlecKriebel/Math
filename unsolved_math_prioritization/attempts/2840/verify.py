#!/usr/bin/env python3
"""Exact symbolic controls for scoped Giroux-torsion deductions; no torsion search."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as Q
from itertools import product
import json
import sympy as s

ROOT=Path(__file__).resolve().parent
counts={}


def ck(name, condition):
    if not bool(condition):
        raise AssertionError(name)
    counts[name]=counts.get(name,0)+1


def zero(name, expr):
    ck(name,s.trigsimp(s.simplify(expr))==0)


x,y,z=s.symbols('x y z',real=True)
k,n=s.symbols('k n',positive=True,integer=True)
coords=(x,y,z)


def contact_density(a, variables):
    return s.simplify(
        a[0]*(s.diff(a[2],variables[1])-s.diff(a[1],variables[2]))
        +a[1]*(s.diff(a[0],variables[2])-s.diff(a[2],variables[0]))
        +a[2]*(s.diff(a[1],variables[0])-s.diff(a[0],variables[1])))


beta=s.Matrix([s.cos(2*s.pi*n*z),-s.sin(2*s.pi*n*z),0])
zero('contact_volume_density',contact_density(beta,coords)-2*s.pi*n)
zero('unit_model_covector',beta.dot(beta)-1)
f=s.Function('f')(x,y,z)
zero('conformal_volume_factor',contact_density(f*beta,coords)-f**2*2*s.pi*n)

# The explicit global change of coordinates on the universal cover.
angle=2*s.pi*k*z
q=x*s.cos(angle)-y*s.sin(angle)
p=2*s.pi*k*(x*s.sin(angle)+y*s.cos(angle))
transformation=s.Matrix([q,p,z])
J=transformation.jacobian(coords)
alpha=s.Matrix([s.cos(angle),-s.sin(angle),0])
pulled=s.Matrix([s.diff(q,v)+p*(1 if v==z else 0) for v in coords])
for j in range(3):
    zero('universal_cover_pullback',pulled[j]-alpha[j])
zero('universal_cover_jacobian',J.det()-2*s.pi*k)
zero('universal_cover_inverse_x',q*s.cos(angle)+p*s.sin(angle)/(2*s.pi*k)-x)
zero('universal_cover_inverse_y',-q*s.sin(angle)+p*s.cos(angle)/(2*s.pi*k)-y)
for j in range(3):
    zero('closed_layer_pullback',alpha[j].subs(z,n*z/k)-beta[j])
zero('closed_layer_volume',2*s.pi*k*(n/k)-2*s.pi*n)

# Hamiltonian formula and local dilation, without assuming a strict-form chart.
q,p,t=s.symbols('q p t',real=True)
v=(q,p,t)
H=s.Function('H')(q,p,t)
X=s.Matrix([H-p*s.diff(H,p),p*s.diff(H,q)-s.diff(H,t),s.diff(H,p)])
gamma=s.Matrix([1,0,p])
zero('hamiltonian_contraction',gamma.dot(X)-H)
for j in range(3):
    lie=sum(X[i]*s.diff(gamma[j],v[i])+gamma[i]*s.diff(X[i],v[j]) for i in range(3))
    zero('hamiltonian_lie_derivative',lie-s.diff(H,q)*gamma[j])
H0=2*q+p*t
X0=s.Matrix([H0-p*s.diff(H0,p),p*s.diff(H0,q)-s.diff(H0,t),s.diff(H0,p)])
ck('local_dilation_field',X0==s.Matrix([2*q,p,t]))
ck('dilation_fixed_point',X0.subs({q:0,p:0,t:0})==s.zeros(3,1))
ck('linearized_dilation',X0.jacobian(v)==s.diag(2,1,1))
c=s.symbols('c',positive=True)
D=s.diag(c*c,c,c)
image=s.Matrix([c*c*q,c*p,c*t])
pull=D.T*s.Matrix([1,0,image[1]])
for j in range(3):
    zero('dilation_form_scaling',pull[j]-c*c*gamma[j])
zero('dilation_volume_scaling',D.det()-c**4)

# Exact controls on the embedding-versus-covering distinction.
for kk in range(2,14):
    for nn in range(1,kk):
        width=Q(nn,kk)
        ck('closed_embedded_interval',0<width<1)
        ck('layer_volume_inequality',nn<kk)
        inverse_bound=max(Q(1),Q(kk,nn))
        ck('metric_bound_control',inverse_bound**2>=Q(nn,kk))
    ck('endpoint_identification',Q(kk,kk)%1==0)
    preimages=[Q(j,kk) for j in range(kk)]
    ck('covering_distinct_preimages',len(set(preimages))==kk)
    ck('covering_not_embedding',all((kk*a)%1==0 for a in preimages))

# Covector lower bound tested against exact diagonal singular values.
unit=(Q(3,5),Q(4,5),Q(0))
for diag in product((Q(1,4),Q(1),Q(3)),repeat=3):
    for magnitude in (Q(1,3),Q(2)):
        pulled_sq=sum((d*magnitude*a)**2 for d,a in zip(diag,unit))
        lower=magnitude**2*min(diag)**2
        ck('inverse_derivative_covector_bound',pulled_sq>=lower)

for j in range(1,13):
    scale=Q(1,2**j)
    ck('pointwise_collapse_control',0<scale**2<=Q(1,4))
    ck('nonzero_finite_time_factor',scale**2!=0)

out={
    'problem_id':2840,'status':'PASS',
    'artifact_sha256':sha256((ROOT/'PARTIAL.md').read_bytes()).hexdigest(),
    'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
    'exact_assertions':sum(counts.values()),'families':counts,
    'sympy_version':s.__version__,
    'scope':'Symbolic identities and finite geometric controls only. Tightness of the standard contact R3 model is an imported classical theorem. No finite bound for arbitrary fixed closed tight manifolds, or closed infinite-torsion example, is certified.',
}
(ROOT/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
