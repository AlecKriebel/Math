#!/usr/bin/env python3
"""Exact rational/quadratic-field certificate of the k107 counterexample."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json
C=Counter()
def ck(g,b):
 assert b,g
 C[g]+=1

def field(d):
 rn=isqrt(d.numerator);rd=isqrt(d.denominator)
 root=F(rn,rd) if rn*rn==d.numerator and rd*rd==d.denominator else None
 class Q:
  def __init__(self,a=0,b=0):
   if isinstance(a,Q):self.a,self.b=a.a,a.b;return
   self.a,self.b=F(a),F(b)
   if root is not None:self.a+=self.b*root;self.b=F(0)
  def __add__(self,o):o=Q(o);return Q(self.a+o.a,self.b+o.b)
  __radd__=__add__
  def __neg__(self):return Q(-self.a,-self.b)
  def __sub__(self,o):return self+-Q(o)
  def __rsub__(self,o):return Q(o)+-self
  def __mul__(self,o):o=Q(o);return Q(self.a*o.a+d*self.b*o.b,self.a*o.b+self.b*o.a)
  __rmul__=__mul__
  def inv(self):
   norm=self.a*self.a-d*self.b*self.b
   assert norm!=0
   return Q(self.a/norm,-self.b/norm)
  def __truediv__(self,o):return self*Q(o).inv()
  def __rtruediv__(self,o):return Q(o)*self.inv()
  def __eq__(self,o):o=Q(o);return self.a==o.a and self.b==o.b
  def sign(self):
   def sg(v):return (v>0)-(v<0)
   if not self.b:return sg(self.a)
   if not self.a:return sg(self.b)
   if sg(self.a)==sg(self.b):return sg(self.a)
   return sg(self.a)*sg(self.a*self.a-d*self.b*self.b)
  def rational(self):assert self.b==0;return self.a
 return Q

def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def add(p,q):return (p[0]+q[0],p[1]+q[1])
def sub(p,q):return (p[0]-q[0],p[1]-q[1])
def scale(z,p):return (z*p[0],z*p[1])
def tangent_intersection(p,q,a,b):
 n=(p[0]/(a*a),p[1]/(b*b));m=(q[0]/(a*a),q[1]/(b*b));D=det(n,m)
 return ((m[1]-n[1])/D,(n[0]-m[0])/D)
def area(poly):return sum(det(poly[i],poly[(i+1)%4]) for i in range(4))/2

def check_family(a,b,s,co,si):
 ck('parameter_circle',co*co+si*si==1)
 d=a**4*si**2+b**4*co**2;Q=field(d);delta=Q(0,1)
 p=(Q(a*co),Q(b*si));q=(-a**3*si/delta,b**3*co/delta)
 P=[p,q,scale(-1,p),scale(-1,q)]
 vdot=dot(p,q);lm=s-vdot/s;lp=s+vdot/s;lengths=[lm,lp,lm,lp]
 ca=a**4/(s*s);cb=b**4/(s*s);lam=a*a-ca
 ck('confocality',lam==b*b-cb and 0<lam<b*b)
 ck('primitive_four',all(P[i]!=P[j] for i in range(4) for j in range(i)))
 half=[]
 for i in range(4):
  z=P[i];z1=P[(i+1)%4];prev=P[(i-1)%4]
  ck('outer_ellipse',z[0]*z[0]/(a*a)+z[1]*z[1]/(b*b)==1)
  ck('orientation',det(z,z1).sign()>0)
  edge=sub(z1,z);ell=lengths[i]
  ck('positive_edge_length',ell.sign()>0 and ell*ell==dot(edge,edge))
  n=(edge[1],-edge[0]);h=dot(n,z)
  ck('caustic_line_tangency',ca*n[0]*n[0]+cb*n[1]*n[1]==h*h)
  touch=(ca*n[0]/h,cb*n[1]/h)
  ck('contact_on_caustic',touch[0]*touch[0]/ca+touch[1]*touch[1]/cb==1)
  ck('contact_on_line',dot(n,touch)==h)
  tau=dot(sub(touch,z),edge)/(ell*ell)
  ck('contact_inside_segment',tau.sign()>0 and (1-tau).sign()>0)
  vin=scale(1/lengths[(i-1)%4],sub(z,prev));vout=scale(1/ell,edge)
  normal=(z[0]/(a*a),z[1]/(b*b))
  reflected=sub(vin,scale(2*dot(vin,normal)/dot(normal,normal),normal))
  ck('physical_reflection',reflected==vout)
  ck('joachimsthal',dot(normal,vin)==1/s)
  cosine=-dot(vin,vout);half.append((1-cosine)/2)
 ck('opposite_half_angles',half[0]==half[2] and half[1]==half[3])
 prod=half[0]*half[1]
 outer=[tangent_intersection(P[i],P[(i+1)%4],a,b) for i in range(4)]
 A=area(P);Ap=area(outer)
 ck('positive_areas',A.sign()>0 and Ap.sign()>0)
 ck('perimeter',sum(lengths)==4*s)
 ck('even_area_product_control',A*Ap==8*a*a*b*b)
 ck('quarter_map_denominator',a**4*(b*b*co/delta)*(b*b*co/delta)+b**4*(-a*a*si/delta)*(-a*a*si/delta)==a**4*b**4/d)
 return A,Ap,prod,Ap/A*prod

# The advertised exact two orbits, plus rational Pythagorean-axis controls.
cases=0;main={}
for a,b,s in [(F(4),F(3),F(5)),(F(12),F(5),F(13)),(F(15),F(8),F(17)),(F(24),F(7),F(25))]:
 D=check_family(a,b,s,F(1),F(0));R=check_family(a,b,s,a/s,b/s);cases+=2
 expectedD=[2*a*b,4*a*b,a*a*b*b/s**4,2*a*a*b*b/s**4]
 expectedR=[4*a*a*b*b/s**2,2*s*s,F(1,4),s**4/(8*a*a*b*b)]
 for actual,expected in zip(D,expectedD):ck('diamond_values',actual==expected)
 for actual,expected in zip(R,expectedR):ck('rectangle_values',actual==expected)
 ck('different_k107_values',D[3].rational()<F(1,2)<R[3].rational())
 ck('quotient_comparison_only',(D[1]/D[0]/D[2]).rational()==(R[1]/R[0]/R[2]).rational())
 if a==4:main={'diamond':[str(x.rational()) for x in D],'rectangle':[str(x.rational()) for x in R],'difference':str(R[3].rational()-D[3].rational())}
 for den in range(2,12):
  for num in range(1,den):
   t=F(num,den);co=(1-t*t)/(1+t*t);si=2*t/(1+t*t)
   check_family(a,b,s,co,si);cases+=1
ck('advertised_pair',main=={'diamond':['24','48','144/625','288/625'],'rectangle':['576/25','50','1/4','625/1152'],'difference':'58849/720000'})
p=Path(__file__).resolve().parent
out={'problem_id':5100001,'verdict':'PASS_EXACT_COUNTEREXAMPLE_CONTROLS','assertions':sum(C.values()),'categories':dict(sorted(C.items())),'family_members_checked':cases,'exact_values':main,'artifact_sha256':sha256((p/'COUNTEREXAMPLE.md').read_bytes()).hexdigest(),'scope':'Exact rational and real quadratic-field calculations; no numerical orbit fitting or corrected all-period theorem.'}
print(json.dumps(out,indent=2,sort_keys=True))
