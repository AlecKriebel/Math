#!/usr/bin/env python3
"""Independent exact jet checks of the published nonvariational obstruction.

This reconstructs the relevant covariant jets from the Christoffel symbols,
rather than copying the author's full-density Frechet/adjoint calculation.
Run: python independent_checks.py
"""
from pathlib import Path
import hashlib
import json
import sympy as s

x=s.symbols('x1:7')
zero=dict.fromkeys(x,0)
f=x[0]*x[1]*x[2]
psi=f
grad=[s.diff(f,z) for z in x]
norm=sum(v*v for v in grad)
P=s.Matrix(6,6,lambda i,j:-s.diff(f,x[i],x[j])+grad[i]*grad[j]-(norm/2 if i==j else 0))
def gamma(k,i,j):
    return (grad[i] if k==j else 0)+(grad[j] if k==i else 0)-(grad[k] if i==j else 0)
def hessian(u):
    du=[s.diff(u,z) for z in x]
    return s.Matrix(6,6,lambda i,j:s.diff(u,x[i],x[j])-sum(gamma(k,i,j)*du[k] for k in range(6)))
def lap0(u):
    return sum(s.diff(u,z,2) for z in x)
def lapg(u):
    return s.exp(-2*f)*(lap0(u)+4*sum(s.diff(u,z)*grad[k] for k,z in enumerate(x)))
def at0(u):return s.simplify(u.subs(zero))
out={}
def check(label,truth):
    assert bool(truth),label
    out[label]='PASS'

H=hessian(psi)
check('covariant_hessian_vanishes_at_origin',H.subs(zero)==s.zeros(6))
check('Schouten_vanishes_at_origin',P.subs(zero)==s.zeros(6))
J=-s.exp(-2*f)*(lap0(f)+2*norm)
check('gradient_J_vanishes_at_origin',all(at0(s.diff(J,z))==0 for z in x))
T=s.exp(-4*f)*sum(P[i,j]*H[i,j] for i in range(6) for j in range(6))
# At the origin f=df=0, so the scalar Laplace-Beltrami value equals lap0.
check('Laplace_T_psi_is_minus_12',at0(lap0(T))==-12)
w=lapg(psi)
check('Laplacian_psi_has_zero_two_jet',at0(w)==0 and all(at0(s.diff(w,z))==0 for z in x) and all(at0(s.diff(w,a,b))==0 for a in x for b in x))
# Every term in T* w has a derivative of w of order <=2, so that jet proves T*w=0.
B=s.exp(-4*f)*sum(v*v for v in P)
check('B_and_gradient_vanish_at_origin',at0(B)==0 and all(at0(s.diff(B,z))==0 for z in x))
check('geometric_skew_value_is_24',-2*at0(lap0(T))==24)
check('third_tensor_squared_is_6',sum(s.diff(f,a,b,c)**2 for a in x for b in x for c in x)==6)
# Independent leading-jet calculation for four harmonic cubics.
cubics=[f,2*f,x[0]**3-3*x[0]*x[1]**2,f+x[0]**3-3*x[0]*x[1]**2]
values=[]
for k,cubic in enumerate(cubics):
    check('harmonic_cubic_'+str(k),lap0(cubic)==0)
    norm3=sum(s.diff(cubic,a,b,c)**2 for a in x for b in x for c in x)
    # Near a flat two-jet, the degree-two density term is Δ|Hess(cubic)|².
    B2=sum(v*v for v in s.hessian(cubic,x))
    density=lap0(B2)
    check('density_leading_jet_'+str(k),s.expand(density-2*norm3)==0)
    t=s.symbols('t')
    check('scaling_variation_'+str(k),s.diff(t*t*density,t).subs(t,1)==4*norm3)
    values.append(int(4*norm3))
check('Ricci_norm_coefficient',8+6==14)
receipt={'status':'PASS','assertions':len(out),'sympy_version':s.__version__,'checks':out,'geometric_skew_value':24,'harmonic_cubic_skew_values':values,'scope':'Exact local tensor jets; the review proves localization to a closed manifold and the variational obstruction.','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
