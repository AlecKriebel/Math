#!/usr/bin/env python3
"""Exact rational-function and scalar controls for the bulk ULC proof."""
from fractions import Fraction as F
from collections import Counter
import json
C=Counter()
def ck(x,k):assert x,k;C[k]+=1
def trim(p):
 while len(p)>1 and not p[-1]:p.pop()
 return p
def add(p,q):
 a=[F(0)]*max(len(p),len(q))
 for r in [p,q]:
  for i,c in enumerate(r):a[i]+=c
 return trim(a)
def neg(p):return [-x for x in p]
def mul(p,q):
 a=[F(0)]*(len(p)+len(q)-1)
 for i,x in enumerate(p):
  for j,y in enumerate(q):a[i+j]+=x*y
 return trim(a)
def der(p):return [F(i)*p[i] for i in range(1,len(p))] or [F(0)]
def val(p,t):return sum(c*t**i for i,c in enumerate(p))
class Rat:
 def __init__(self,p,q=[1]):self.p=list(map(F,p));self.q=list(map(F,q))
 def __add__(a,b):
  if not isinstance(b,Rat):b=Rat([b])
  return Rat(add(mul(a.p,b.q),mul(b.p,a.q)),mul(a.q,b.q))
 __radd__=__add__
 def __neg__(a):return Rat(neg(a.p),a.q)
 def __sub__(a,b):return a+(-b if isinstance(b,Rat) else -F(b))
 def __rsub__(a,b):return -a+b
 def __mul__(a,b):
  if not isinstance(b,Rat):b=Rat([b])
  return Rat(mul(a.p,b.p),mul(a.q,b.q))
 __rmul__=__mul__
 def __truediv__(a,b):
  if not isinstance(b,Rat):b=Rat([b])
  return Rat(mul(a.p,b.q),mul(a.q,b.p))
 def derivative(a):return Rat(add(mul(der(a.p),a.q),neg(mul(a.p,der(a.q)))),mul(a.q,a.q))
 def same(a,b):return add(mul(a.p,b.q),neg(mul(b.p,a.q)))==[0]
 def value(a,t):return val(a.p,t)/val(a.q,t)
T=Rat([0,1]);U=Rat([-5,0,1]);W=Rat([-7,2,1]);lam=(T+1)*W/8
D=lambda f:U/(2*T)*f.derivative()
a=U*Rat([-5,6,3])/(2*T*(T+1)*W)
p6=Rat([175,250,-235,-4,57,10,3]);p4=Rat([105,100,-42,36,9])
v=U*p6/(4*T*T*T*(T+1)*(T+1)*W*W)
gap=U*U*p4/(8*T*T*T*(T+1)*(T+1)*W*W)
ck(a.same(D(lam)/lam),'symbolic_alpha_identity')
ck(v.same(D(a)),'symbolic_variance_identity')
ck(gap.same(a*(F(3,2)-a)-F(3,2)*v),'symbolic_strict_ULC_gap')
ck((F(3,2)-a).same(Rat([-25,9,5,3])/(2*T*(T+1)*W)),'symbolic_upper_endpoint_identity')
ck(add(add(add([175,250,0,0,0,0,3],[0,0,0,-4,0,10]),[0,0,-235,0,57]),[0])==p6.p,'variance_positive_grouping')
# Dense rational t mesh, always checking the exact condition t^2>5.
for den in range(1,31):
 for num in range(1,20*den+1):
  t=F(num,den)
  if t*t<=5:continue
  alpha=a.value(t);var=v.value(t);G=gap.value(t)
  ck(0<alpha<F(3,2),'rational_alpha_range')
  ck(var>0,'rational_variance_positive')
  ck(G>0,'rational_ULC_gap_positive')
  ck(1/var-1/alpha-1/(F(3,2)-alpha)==G/(var*alpha*(F(3,2)-alpha)),'rational_inverse_variance_gap')
# Direct Gaussian moment arithmetic for the first saddle correction term.
for s in [F(1,7),F(1,2),F(1),F(5,2)]:
 for H,H1,H2,k3,k4 in [(F(2),F(1),F(-3),F(2),F(5)),(F(3),F(-2),F(7),F(-3),F(1))]:
  moments={0:F(1),2:1/s,4:3/s**2,6:15/s**3}
  integral=-H2*moments[2]/2+(H1*k3/6+H*k4/24)*moments[4]-H*k3*k3*moments[6]/72
  formula=H*(-H2/(2*H*s)+H1*k3/(2*H*s*s)+k4/(8*s*s)-5*k3*k3/(24*s**3))
  ck(integral==formula,'saddle_correction_moment_identity')
# The rejected generic Lorentzian-symbol shortcut: Hessian of x^2+2xv+yv.
M=[[2,0,2],[0,0,1],[2,1,0]]
det=M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])-M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])+M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0])
ck(det==-2,'rejected_lift_symbol_determinant')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),'scope':'Exact spectral/variance algebra and first-correction arithmetic; the uniform asymptotic theorem is justified by the analytic proof, not these bounded controls.'},indent=2,sort_keys=True))
