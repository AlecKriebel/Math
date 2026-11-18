#!/usr/bin/env python3
"""Independent exact Vandermonde/flux/cyclotomic diagnostics; not a global mesh theorem."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from math import factorial
import json
import sympy as S
r,t,c,s,z=S.symbols('r t c s z');C=Counter()
def ck(k,v):
 assert bool(v),k;C[k]+=1
def eq(k,a,b):ck(k,S.cancel(S.expand(a-b))==0)
def mons(k):return [(a,b) for a in range(k+1) for b in range(k+1-a)]
def vandermonde(k):
 ms=mons(k);ns=[(S.Rational(a,k),S.Rational(b,k)) for a,b in ms]
 V=S.Matrix([[x**a*y**b for a,b in ms] for x,y in ns]);J=V.inv()
 for val in V*J-S.eye(len(ms)):eq('exact_vandermonde_inverse',val,0)
 return ms,ns,J
Vs={k:vandermonde(k) for k in (2,3,4)}
def interp(p,k):
 ms,ns,J=Vs[k];values=S.Matrix([p.subs({r:x,t:y},simultaneous=True) for x,y in ns]);v=J*values
 return S.expand(sum(v[i]*r**a*t**b for i,(a,b) in enumerate(ms)))
# Integration by boundary flux rather than the author's triangle-moment integration.
u=S.symbols('u')
def flux(g,axis):
 # Integral derivative_r g = integral_0^1 [g(1-t,t)-g(0,t)]dt.
 if axis==r:return S.integrate(S.expand(g.subs(r,1-t)-g.subs(r,0)),(t,0,1))
 return S.integrate(S.expand(g.subs(t,1-r)-g.subs(t,0)),(r,0,1))
p=((r+c*t)**2+(s*t)**2)**2;e=interp(p,3)-p
lap_int=S.factor(((s*s+c*c)*flux(S.diff(e,r),r)-2*c*flux(S.diff(e,r),t)+flux(S.diff(e,t),t))/s)
eq('quartic_trace_by_boundary_flux',lap_int,-(c*c+s*s)*((c-1)**2+s*s)/(3*s))
ck('quartic_circle_reduction',S.rem(S.Poly(S.cancel((lap_int-2*(c-1)/(3*s))*s),s),S.Poly(s*s+c*c-1,s)).is_zero)
for n in range(1,31):
 cc=S.Rational(1-n*n,1+n*n);ss=S.Rational(2*n,1+n*n)
 ck('negative_quartic_rational_wedge',lap_int.subs({c:cc,s:ss})<0)
# Independently derive Gaussian curvature times area from first/second fundamental forms.
a,b,h11,h12,h22,epsilon=S.symbols('a b h11 h12 h22 epsilon',real=True)
metric=S.Matrix([[1+a*a,a*b],[a*b,1+b*b]]);H=S.Matrix([[h11,h12],[h12,h22]])
eq('metric_determinant',metric.det(),1+a*a+b*b)
second=H/S.sqrt(1+a*a+b*b)
eq('graph_curvature_area_density',second.det()/S.sqrt(metric.det()),H.det()/(1+a*a+b*b)**S.Rational(3,2))
x,y,w=S.symbols('x y w');E=S.Matrix([[x,y],[y,w]])
cof=lambda A:S.Matrix([[A[1,1],-A[0,1]],[-A[1,0],A[0,0]]])
eq('determinant_directional_derivative',S.diff((H+epsilon*E).det(),epsilon).subs(epsilon,0),sum(u*v for u,v in zip(cof(H),E)))
for M in [S.Matrix([[i,j],[j,k]]) for i in range(-3,4) for j in range(-2,3) for k in range(-3,4) if i*i+j*j+k*k]:
 HH=cof(M);v=sum(u*w for u,w in zip(cof(HH),M));ck('all_jet_necessity_positive',v==sum(x*x for x in M)>0)
# Direct interpolation and Hessian flux on each rotating triangle over Q[z]/Phi_q.
# Complex coordinates Z,W are independent; no floating trigonometric substitutions.
fan_cases=[]
for k,q in ((2,7),(4,11)):
 phi=S.Poly(S.cyclotomic_poly(q,z),z)
 def red(v):return S.Poly(S.expand(v),z).rem(phi).as_expr()
 zz=[red(z**j) for j in range(q)]
 delta=red(zz[q-1]-z);invdelta=S.invert(delta,phi.as_expr(),z)
 def rp(p):
  return S.Poly.from_dict({ij:red(v) for ij,v in S.Poly(S.expand(p),r,t).terms()},(r,t)).as_expr()
 def interp_ring(p):
  ms,ns,J=Vs[k];vals=[red(p.subs({r:x,t:y},simultaneous=True)) for x,y in ns]
  coefs=[red(sum(J[i,j]*vals[j] for j in range(len(vals)))) for i in range(len(ms))]
  return S.Poly.from_dict({ab:coefs[i] for i,ab in enumerate(ms)},(r,t)).as_expr()
 def flux_ring(g,axis):return red(flux(g,axis))
 for A in range(k+2):
  B=k+1-A;totals=[0,0,0]
  for j in range(q):
   Z=zz[j]*r+zz[(j+1)%q]*t;W=zz[(-j)%q]*r+zz[(-j-1)%q]*t
   p=rp(Z**A*W**B);e=rp(interp_ring(p)-p)
   # inverse coordinate Jacobian, independently assembled on this triangle
   det=red(zz[j]*zz[(-j-1)%q]-zz[(j+1)%q]*zz[(-j)%q])
   invdet=S.invert(det,phi.as_expr(),z)
   drZ=red(zz[(-j-1)%q]*invdet);dtZ=red(-zz[(-j)%q]*invdet)
   drW=red(-zz[(j+1)%q]*invdet);dtW=red(zz[j]*invdet)
   ck('complex_coordinate_inverse',red(drZ*zz[j]+dtZ*zz[(j+1)%q])==1 and red(drZ*zz[(-j)%q]+dtZ*zz[(-j-1)%q])==0)
   drr=flux_ring(S.diff(e,r),r);drt=flux_ring(S.diff(e,r),t);dtt=flux_ring(S.diff(e,t),t)
   vals=[red(drZ**2*drr+2*drZ*dtZ*drt+dtZ**2*dtt),red(drZ*drW*drr+(drZ*dtW+dtZ*drW)*drt+dtZ*dtW*dtt),red(drW**2*drr+2*drW*dtW*drt+dtW**2*dtt)]
   for i,v in enumerate(vals):totals[i]=red(totals[i]+v)
  for v in totals:eq('whole_fan_direct_hessian_flux',v,0)
  fan_cases.append([k,q,A,B])
 for j in range(q):ck('odd_fan_no_antipodal_vertex',red(zz[j]+1)!=0)
# Finite nonresonance diagnostics for higher even degrees, including composite q.
for k in range(2,42,2):
 for q in (k+5,k+9,k+15):
  for a0 in range(k+2):
   ell=2*a0-k-1
   for j in range(3):
    n=ell+2-2*j
    ck('odd_character_nonresonance',n%2!=0 and 0<abs(n)<q and n%q!=0)
# Explicit scale identities on a nonunit rational affine triangle via monomial interpolation.
h=S.symbols('h',positive=True)
for k in (2,3,4):
 for A in range(k+2):
  p=r**A*t**(k+1-A);err=interp(p,k)-p
  for i,j in ((2,0),(1,1),(0,2)):
   scaled=interp((h*r)**A*(h*t)**(k+1-A),k)-(h*r)**A*(h*t)**(k+1-A)
   eq('hessian_error_scaling',S.diff(scaled,r,i,t,j)/h**2,h**(k-1)*S.diff(err,r,i,t,j))
 ck('quadratic_remainder_exponent',2*k-2>=k)
root=Path(__file__).resolve().parent
ck('frozen_artifact_hash',sha256((root/'author_replay/PARTIAL.md').read_bytes()).hexdigest()=='edfa4b49222d53f440b888179798371e17d78049c2f3344e50c91928b2613c36')
out={'verdict':'PASS','assertions':sum(C.values()),'categories':dict(C),'whole_fan_cases':fan_cases,'sympy_version':S.__version__,'scope':'Exact polynomial/interpolation/cyclotomic controls only. The analytic all-jet equivalence and weighted bounds are audited in REVIEW.md; no fixed-domain global odd-fan mesh family is supplied.'}
(root/'independent_results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
