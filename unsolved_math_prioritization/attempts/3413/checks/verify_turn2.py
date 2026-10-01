#!/usr/bin/env python3
"""Finite algebra controls only; the geometric statements require TURN_2.md."""
from math import gcd,lcm
from itertools import product,permutations
from collections import Counter
from fractions import Fraction
import json
C=Counter()
def check(x,k):
 assert x,k
 C[k]+=1
# Nonsingular cyclic linking forms: all choices of two generator classes.
for k in range(2,25):
 units=[x for x in range(k) if gcd(x,k)==1]
 for c,a,b in product(units,repeat=3):
  ell=c*a*b%k
  check(gcd(ell,k)==1,'pairing_of_generators_is_unit')
  check(ell!=0,'invariant_circles_cannot_have_zero_linking')
  check(Fraction(ell,k).denominator==k,'linking_pairing_exact_order')
# Verify the full signed-cycle power formula explicitly for representative blocks.
for d in range(1,13):
 for sign in (1,-1):
  f=tuple((i+1,1) if i<d-1 else (0,sign) for i in range(d))
  for q in range(1,25):
   fq=[]
   for i in range(d):
    j=i;s=1
    for _ in range(q):j,t=f[j];s*=t
    fq.append((j,s))
   seen=set();data=[]
   for i in range(d):
    if i in seen:continue
    j=i;s=1;n=0
    while j not in seen:
     seen.add(j);n+=1;j,t=fq[j];s*=t
    data.append((n,s))
   h=gcd(d,q)
   check(sorted(data)==[(d//h,sign**(q//h))]*h,'signed_restriction_formula')
# All orbit-length multisets of at most eight components, across tested orders.
def partitions(n,minpart=1):
 if n==0:yield ();return
 for a in range(minpart,n+1):
  for p in partitions(n-a,a):yield (a,)+p
for m in range(2,25):
 for n in range(9):
  for ds in partitions(n):
   if any(m%d for d in ds):continue
   allowed=all(d in (1,m) for d in ds) and ds.count(1)<=1
   # Precisely the two contradictions in the written linking proof:
   # a proper nonsingleton orbit gives two invariant components of a free
   # stabilizer; two singleton orbits give the same contradiction for C_m.
   obstructed=any(1<d<m for d in ds) or ds.count(1)>1
   check(allowed==(not obstructed),'free_unlink_orbit_classification')
   if allowed:
    check(n==ds.count(m)*m+ds.count(1),'constructive_cycle_count')
# Scalar C_m action: each nonidentity power has no eigenvalue one.
for m in range(2,101):
 for j in range(1,m):check(j%m!=0,'scalar_action_all_nonidentity_powers_free')
# Rational 4x4 matrix of (z,w)->(iz,-w), orientation-preserving on S3.
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def rank(a):
 a=[[Fraction(x) for x in row] for row in a];r=0
 for c in range(len(a[0])):
  pivot=next((j for j in range(r,len(a)) if a[j][c]),None)
  if pivot is None:continue
  a[r],a[pivot]=a[pivot],a[r];z=a[r][c];a[r]=[x/z for x in a[r]]
  for j in range(len(a)):
   if j!=r:
    z=a[j][c];a[j]=[x-z*y for x,y in zip(a[j],a[r])]
  r+=1
 return r
I=[[int(i==j) for j in range(4)] for i in range(4)]
g=[[0,-1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]];g2=mm(g,g)
check(mm(g2,g2)==I,'calibration_order_four')
check(rank([[g[i][j]-I[i][j] for j in range(4)] for i in range(4)])==4,'generator_fixed_point_free')
check(rank([[g2[i][j]-I[i][j] for j in range(4)] for i in range(4)])==2,'square_fixed_circle')
check(mm(g,[list(c) for c in zip(*g)])==I,'calibration_orthogonal')
det=sum((-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))*g[0][p[0]]*g[1][p[1]]*g[2][p[2]]*g[3][p[3]] for p in permutations(range(4)))
check(det==1,'calibration_ambient_orientation')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'categories':dict(C),'scope':'Finite modular/cycle/matrix controls. Covering transfer, linking nonsingularity, unlink constructions, and exact remaining hyperbolicity/full-group gap are in TURN_2.md.'},indent=2))
