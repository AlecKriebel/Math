#!/usr/bin/env python3
"""Independent exact audit: iterated integer square roots, transformed odd
boundary polynomials, and direct distance-based linear systems. No author code
is imported or executed. Certificate supplies proposed rational root brackets
only; every bracket sign is re-evaluated by independent arithmetic."""
from fractions import Fraction as F
from math import isqrt, comb
from itertools import combinations
from pathlib import Path
import json, hashlib

PREC=10**70
class I:
 def __init__(self,a,b=None):
  self.lo=F(a); self.hi=F(a if b is None else b)
  assert self.lo<=self.hi
 def __add__(self,o):
  o=iv(o);return I(self.lo+o.lo,self.hi+o.hi)
 __radd__=__add__
 def __neg__(self):return I(-self.hi,-self.lo)
 def __sub__(self,o):return self+-iv(o)
 def __rsub__(self,o):return iv(o)+-self
 def __mul__(self,o):
  o=iv(o);p=[self.lo*o.lo,self.lo*o.hi,self.hi*o.lo,self.hi*o.hi];return I(min(p),max(p))
 __rmul__=__mul__
 def __truediv__(self,o):
  o=iv(o);assert not o.lo<=0<=o.hi;return self*I(1/o.hi,1/o.lo)
 def sq(self):return I(0 if self.lo<=0<=self.hi else min(self.lo**2,self.hi**2),max(self.lo**2,self.hi**2))
 def pw(self,n):
  assert self.lo>=0;return I(self.lo**n,self.hi**n)
 def sign(self):return 1 if self.lo>0 else -1 if self.hi<0 else 0
 def packed(self):return [str(self.lo),str(self.hi)]
 def coarse(self):return [str(F(self.lo.numerator*10**12//self.lo.denominator,10**12)),str(F(-((-self.hi.numerator*10**12)//self.hi.denominator),10**12))]
def iv(x):return x if isinstance(x,I) else I(x)
def sqrt_once(x):
 x=iv(x);assert x.lo>=0
 def low(q):
  k=isqrt(q.numerator*PREC**2//q.denominator)
  assert F(k,PREC)**2<=q<F(k+1,PREC)**2
  return k
 return I(F(low(x.lo),PREC),F(low(x.hi)+1,PREC))
def eighth(x):return sqrt_once(sqrt_once(sqrt_once(x)))
def vsub(a,b):return tuple(x-y for x,y in zip(a,b))
def n2(a):return sum((x.sq() for x in a),I(0))
def dp(a,b):return n2(vsub(a,b)).pw(8)
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def separated(a,b):return any(x.hi<y.lo or y.hi<x.lo for x,y in zip(a,b))
b=F(2073,10000);c=F(4719,10000);d=F(64,10000);lam=F(27,1250)
A=(I(0),I(0));B=(I(b),I(0));C=(I(c),I(d))
# z=1-2t, so (t-1)^2+h^2 = z^2/4+h^2+1/4+z/2.
# Difference of eighth powers has only odd terms in z/2.
def zpoly(qx,qy,h,lev,z):
 k=z*z/4+h*h+F(1,4)
 return (qx*qx+qy*qy)**8*2*sum(F(comb(8,j))*k**(8-j)*(z/2)**j for j in [1,3,5,7])-lev
def boundary(qx,qy,h,lev,base):
 l=F(-32);r=F(32)
 assert zpoly(qx,qy,h,lev,l)<0<zpoly(qx,qy,h,lev,r)
 for _ in range(190):
  m=(l+r)/2
  if zpoly(qx,qy,h,lev,m)<0:l=m
  else:r=m
 assert zpoly(qx,qy,h,lev,l)<0<zpoly(qx,qy,h,lev,r)
 t=(I(1)-I(l,r))/2
 return (base[0]+qx*t-h*qy,base[1]+qy*t+h*qx),t
P1,t1=boundary(c,d,F(10),F(1),(I(0),I(0)))
P3,t3=boundary(b,F(0),F(1),lam,(I(0),I(0)))
P5,t5=boundary(c-b,d,F(-10),1-lam,(I(b),I(0)))
P=[P1,A,P3,B,P5,C]
# General trilateration using input coordinates, not specialized author x/y.
def solve(s,origin,p,q,levp,levq):
 v=vsub(p,origin);w=vsub(q,origin)
 u=eighth(iv(s));vp=eighth(iv(s)+levp);vq=eighth(iv(s)+levq)
 rp=n2(v)+u-vp;rq=n2(w)+u-vq
 disc=2*det(v,w)
 y=((rp*w[1]-rq*v[1])/disc,(v[0]*rq-w[0]*rp)/disc)
 return tuple(o+z for o,z in zip(origin,y)),n2(y)-u
cuts=[F(9,10000),F(11,10000),F(13,10000),F(1,2),F(1),F(10**16)]
outsign=[]
for i,s in enumerate(cuts):
 _,g=solve(I(s),A,B,C,lam,I(1));assert g.sign()==(-1)**i
 outsign.append({'s':str(s),'G':g.coarse()})
L=dp(B,P5)-dp(B,P3);M=dp(A,P1)-dp(A,P3)
assert L.sign()==1 and M.sign()==1
inends=[]
for s,sg in [(F(1,100),1),(F(11,1000),-1)]:
 _,h=solve(I(s),P3,P5,P1,L,M);assert h.sign()==sg
 inends.append({'s':str(s),'H':h.coarse()})
Z,_=solve(I(F(1,100),F(11,1000)),P3,P5,P1,L,M)
assert all(separated(Z,p) for p in P)
assert all(det(vsub(Z,p),vsub(q,p)).sign()!=0 for p,q in combinations(P,2))
assert all(separated(p,q) for p,q in combinations(P,2))
assert all(det(vsub(q,p),vsub(r,p)).sign()!=0 for p,q,r in combinations(P,3))
assert det(vsub(B,A),vsub(C,A)).sign()==1
odd=det(vsub(P3,P1),vsub(P5,P1));assert odd.sign()==1
# Independently check candidate refinements recorded in the author certificate.
R=Path(__file__).resolve().parent
package=R.parent/'publication_package_v2'
cert=json.loads((package/'exact_certificate.json').read_text())
centers=[]
for i,record in enumerate(cert['outgoing_root_boxes']):
 l,r=map(F,record['s'])
 assert cuts[i]<l<r<cuts[i+1]
 for s,sg in [(l,(-1)**i),(r,-(-1)**i)]:
  _,g=solve(I(s),A,B,C,lam,I(1));assert g.sign()==sg
 X,_=solve(I(l,r),A,B,C,lam,I(1))
 assert all(separated(X,p) for p in P)
 assert all(det(vsub(X,p),vsub(q,p)).sign()!=0 for p,q in combinations(P,2))
 centers.append([x.coarse() for x in X])
assert all(separated(tuple(I(F(x[0]),F(x[1])) for x in p),tuple(I(F(x[0]),F(x[1])) for x in q)) for p,q in combinations(centers,2))
cross=[det(vsub(P[j],P[i]),vsub(P[k],P[i])).sign() for i,j,k in [(0,1,2),(0,1,3),(2,3,0),(2,3,1)]]
assert cross==[-1,1,1,-1]
# Formal linear algebra of all face identities using independent coefficient
# vectors for a,f,g,lambda and r3/qA. Each residual must be identically zero.
from collections import Counter
def v(**kwargs):return Counter(kwargs)
def plus(*args):
 out=Counter()
 for a in args:
  for k,x in a.items():out[k]+=x
 return out
def neg(a):return Counter({k:-x for k,x in a.items()})
def residual(*args):assert not any(plus(*args).values())
a=v(a=1);f=v(f=1);g=v(g=1);l=v(l=1);one=v(one=1);r3=v(r3=1);qa=v(qa=1)
r1=plus(r3,a,neg(f));r5=plus(r3,g,neg(f),neg(l));qb=plus(qa,l);qc=plus(qa,one)
residual(a,r3,neg(r1),neg(f))
residual(f,l,r5,neg(r3),neg(g))
residual(g,one,neg(l),r1,neg(r5),neg(a),neg(one))
residual(f,qb,neg(qa),neg(f),neg(l))
residual(g,qc,neg(qb),neg(g),neg(one),l)
residual(a,one,qa,neg(qc),neg(a))
# Exact alpha=2 limiting case: three noncollinear foci give a unique linear
# solution for arbitrary levels. Thus five-center mechanism uses higher power.
assert b*d!=0
out={'status':'PASS_INDEPENDENT_EXACT_ARITHMETIC','method':'three exact isqrt square-root enclosures; 190 bisections of transformed odd boundary polynomials; direct general trilateration; exact symbolic face coefficient cancellation','precision':70,'boundary_t':[x.coarse() for x in [t1,t3,t5]],'G_signs':outsign,'H_signs':inends,'boundary_points':[[x.coarse() for x in p] for p in P],'incoming_levels':[L.coarse(),M.coarse()],'odd_determinant':odd.coarse(),'incoming_whole_box':[x.coarse() for x in Z],'outgoing_center_boxes':centers,'strict_boundary_crossing_signs':cross,'all_20_boundary_triples_noncollinear':True,'all_15_boundary_pair_lines_avoided_by_whole_incoming_box_and_all_5_selected_outgoing_boxes':True,'all_6_face_identities_symbolically_zero':True}
(R/'INDEPENDENT_EXACT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
