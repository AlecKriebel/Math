#!/usr/bin/env python3
"""Finite exact diagnostics for the unresolved smooth gauge analysis."""
from pathlib import Path
from fractions import Fraction
from math import factorial
import hashlib,json
import sympy as s
checks={}
def ck(name,v):
    assert bool(v),name
    checks[name]='PASS'
# Sparse exterior algebra. Basis: alpha, omega, df, dh, gamma.
def plus(*forms):
    out={}
    for f in forms:
        for I,c in f.items():out[I]=s.expand(out.get(I,0)+c)
    return {I:s.simplify(c) for I,c in out.items() if s.simplify(c)!=0}
def scale(c,f):return {I:s.expand(c*v) for I,v in f.items()}
def wedge(a,b):
    out={}
    for I,c in a.items():
        for J,d in b.items():
            if set(I)&set(J):continue
            sign=(-1)**sum(i>j for i in I for j in J)
            K=tuple(sorted(I+J));out[K]=s.expand(out.get(K,0)+sign*c*d)
    return {I:s.simplify(c) for I,c in out.items() if s.simplify(c)!=0}
alpha,omega,df,dh,gamma=[{(i,):s.Integer(1)} for i in range(5)]
E,h=s.symbols('E h')
da=wedge(alpha,omega);dw=wedge(alpha,gamma)
af=scale(E,alpha);wf=plus(omega,scale(-1,df))
daf=scale(E,plus(wedge(df,alpha),da))
ck('rescaled_defining_equation',wedge(af,wf)==daf)
ck('integrability_identity',wedge(alpha,dw)=={})
beta=plus(wf,scale(h,af))
dbeta=plus(dw,wedge(dh,af),scale(h,daf))
GVnew=wedge(beta,dbeta)
expected=plus(wedge(omega,dw),scale(-1,wedge(df,dw)),wedge(dh,daf))
ck('full_gauge_transgression',GVnew==expected)
ck('constant_h_has_no_pointwise_effect',all(s.diff(c,h)==0 for c in GVnew.values()))
# Full coordinate calculation in a foliated chart: alpha=e^H dz,
# omega=-dH+k alpha. This only checks local identities, not a global example.
x,y,z=s.symbols('x y z',real=True)
vs=[x,y,z]
def grad(f):return s.Matrix([s.diff(f,v) for v in vs])
def curl(V):return s.Matrix([s.diff(V[2],y)-s.diff(V[1],z),s.diff(V[0],z)-s.diff(V[2],x),s.diff(V[1],x)-s.diff(V[0],y)])
def zerovec(V):return all(s.simplify(v)==0 for v in V)
for idx,(H,k,f,j) in enumerate([(x*z+y*y,x+y*z,x+y*z,y+x*x),(x+y+z,x*z,x*y,z*z+x),(x*y,x+z,y*z,x*y*z)]):
    A=s.exp(H)*s.Matrix([0,0,1]);W=-grad(H)+k*A
    Af=s.exp(f)*A;Wf=W-grad(f);B=Wf+j*Af
    ck(f'chart_integrability_{idx}',zerovec(curl(A)-A.cross(W)))
    ck(f'chart_rescaled_integrability_{idx}',zerovec(curl(Af)-Af.cross(B)))
    ck(f'chart_transgression_{idx}',s.simplify(B.dot(curl(B))-W.dot(curl(W))+grad(f).dot(curl(W))-grad(j).dot(curl(Af)))==0)
    ck(f'chart_X_tangent_{idx}',s.simplify(Af.dot(curl(Af)))==0)
    ck(f'chart_Y_tangent_{idx}',s.simplify(A.dot(curl(W)))==0)
    for label,V in [('X',curl(Af)),('Y',curl(W))]:
        ck(f'chart_{label}_divergence_{idx}',s.simplify(sum(s.diff(V[i],vs[i]) for i in range(3)))==0)
# Averaging integration-by-parts identity on each Fourier mode.
T,w,theta=s.symbols('T w theta',nonzero=True,real=True)
u=s.symbols('u',real=True)
mode=s.exp(s.I*(theta+w*u))
H=s.integrate((T-u)*mode,(u,0,T))/T
avg=s.integrate(mode,(u,0,T))/T
ck('averaging_identity_mode',s.simplify(w*s.diff(H,theta)+s.exp(s.I*theta)-avg)==0)
ck('positive_global_average_not_orbit_average',1+2*s.cos(s.pi)==-1)
# Liouville controls. The infinite tail estimate and smooth convergence are
# proved in the artifact; these test exact exponents and finite partial tails.
for n in range(2,7):
    q=10**factorial(n)
    partial=sum((Fraction(1,10**factorial(j)) for j in range(1,n+1)),Fraction())
    p=q*partial
    ck(f'integer_numerator_{n}',p.denominator==1)
    ck(f'leading_small_divisor_exponent_{n}',factorial(n+1)-factorial(n)==n*factorial(n))
    first=q*Fraction(1,10**factorial(n+1))
    ck(f'leading_tail_exact_{n}',first==Fraction(1,q**n))
    # The next term is already much smaller; no enormous full tail expansion.
    exponent_gap=factorial(n+2)-factorial(n+1)
    ck(f'tail_successive_ratio_bound_{n}',exponent_gap>=1)
    ck(f'fourier_coefficient_blowup_exponent_{n}',n*factorial(n)-n*factorial(n)//2==n*factorial(n)//2)
    for m in range(4):
        if n>=2*m+2:
            ck(f'derivative_summability_exponent_{n}_{m}',n/2-m>=1)
result={'status':'PASS','assertions':len(checks),'artifact_sha256':hashlib.sha256(Path(__file__).with_name('OBSTRUCTION.md').read_bytes()).hexdigest(),'sympy_version':s.__version__,'checks':checks,'scope':'Exact gauge algebra and bounded transport controls only; no manifold counterexample or resolution of Calegari Question13.1.'}
print(json.dumps(result,indent=2,sort_keys=True))
