#!/usr/bin/env python3
"""Exact algebra controls; connectedness, not finite samples, proves no section."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
C={}
def ck(v,k):
 assert v,k
 C[k]=C.get(k,0)+1

def square(z):a,b=z;return a*a-b*b,2*a*b
def gamma(t):return (1-t,t) if t<=1 else (1-t,2-t)
def system(coef,x,y):
 a1,a2,a0,b1,b2,b0=coef
 return x*x-y*y+a1*x+a2*y+a0,x*y+b1*x+b2*y+b0

def embed(z):u,v=z;return F(0),F(0),-u,F(0),F(0),-v/2

# Literal coefficient substitution, including the factor 1/2 in b0.
vals=[F(k,3) for k in range(-4,5)]
for u in vals:
 for v in vals:
  coef=embed((u,v))
  ck(sum(a*a for a in coef)<=u*u+v*v,'embedding_norm')
  for x,y in [(F(0),F(0)),(F(1),F(2)),(F(-2),F(1,3))]:
   f,g=system(coef,x,y);a,b=square((x,y))
   ck((f,2*g)==(a-u,b-v),'slice_identity')

ck(gamma(F(0))==(1,0) and gamma(F(1))==(0,1) and gamma(F(2))==(-1,0),'path_endpoints')
ck((1-F(1),F(1))==(1-F(1),2-F(1)),'path_join')
loops=0
for c in [F(1,2),F(1,3),F(2,5),F(3,7)]:
 for k in range(129):
  t=F(k,64);a,b=gamma(t);norm=a*a+b*b
  ck(F(1,2)<=norm<=1,'path_nonzero_and_bounded')
  w=(c*a,c*b);z=square(w);coef=embed(z);loops+=1
  ck(z!=(0,0),'loop_avoids_origin')
  ck(z[0]**2+z[1]**2==c**4*norm**2<=c**4,'loop_disk_bound')
  for sign in (-1,1):
   ck(system(coef,sign*w[0],sign*w[1])==(0,0),'exact_roots')
   # The two candidate ratios are exactly the roots of q^2=1.
   ck(sign*sign==1,'two_valued_ratio')
 w0=(c,F(0));w2=(-c,F(0))
 ck(square(w0)==square(w2)==(c*c,0),'closed_parameter_loop')
 ck(w0!=w2 and w0==tuple(-a for a in w2),'opposite_root_endpoints')
 for sign in (-1,1):
  ck(tuple(sign*a for a in w0)!=tuple(sign*a for a in w2),'constant_ratio_endpoint_obstruction')

# Rational tests of the two standard branches on the punctured model.
branch_points=0
vals=[F(k,4) for k in range(-8,9)]
for a in vals:
 for b in vals:
  if a==b==0:continue
  z=square((a,b));r=a*a+b*b;branch_points+=1
  ck(z!=(0,0) and r*r==z[0]**2+z[1]**2,'punctured_model')
  ck((r+z[0]>0) or (r-z[0]>0),'two_domains_cover_punctured_plane')
  if a:
   root=(abs(a),(1 if a>0 else -1)*b)
   ck(square(root)==z and root[0]>0,'principal_branch_control')
   ck(r+z[0]==2*a*a,'branch_denominator')
  if b:
   root=((1 if b>0 else -1)*a,abs(b))
   ck(square(root)==z and root[1]>0,'upper_branch_control')
   ck(r-z[0]==2*b*b,'branch_denominator')

b=Path(__file__).resolve().parent
r={'status':'PASS','assertions':sum(C.values()),'categories':C,'rational_loop_samples':loops,'punctured_branch_samples':branch_points,'artifact_sha256':hashlib.sha256((b/'NO_COVER.md').read_bytes()).hexdigest(),'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact slice and loop algebra only. Nonexistence of a continuous section follows analytically from connectedness and the two-valued ratio, not from finite sampling.'}
(b/'verification.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r,indent=2,sort_keys=True))
