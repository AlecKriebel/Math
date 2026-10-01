#!/usr/bin/env python3
"""Exact fixed-size partition-fiber/Krawtchouk checks, not an asymptotic proof."""
from character_tools import parts,character
from collections import Counter
from fractions import Fraction as F
from math import comb,factorial
import json
C=Counter()
def ck(x,key):assert x,key;C[key]+=1
def choose(n,k):return comb(n,k) if 0<=k<=n else 0
def K(s,j,r):return sum((-1)**l*choose(r,l)*choose(s-r,j-l) for l in range(j+1))
rows=[]
for n in range(1,16):
 ps=parts(n);p=len(ps);fibers=[]
 for size in range(n+1):
  for nu in parts(size):
   if any(j<3 for j in nu):continue
   R=n-size;s=R//2
   mus=[tuple(sorted(nu+(2,)*r+(1,)*(R-2*r),reverse=True)) for r in range(s+1)]
   fibers.append((nu,R,s,mus))
 ck(sum(s+1 for nu,R,s,mus in fibers)==p,'exact_fiber_mass')
 ck(set(mu for _,_,_,mus in fibers for mu in mus)==set(ps),'fiber_partition_bijection')
 z=0;identical=0;full=0;degree_sum=0;fiber_count=0
 for lam in ps:
  for nu,R,s,mus in fibers:
   f=[character(lam,mu) for mu in mus]
   aa=[F(sum(K(s,r,j)*f[r] for r in range(s+1)),2**s) for j in range(s+1)]
   for a in aa:ck(a.denominator==1,'integral_weight_space_traces')
   for r in range(s+1):ck(sum(aa[j]*K(s,j,r) for j in range(s+1))==f[r],'exact_Krawtchouk_reconstruction')
   d=max((j for j,a in enumerate(aa) if a),default=-1)
   zeros=sum(x==0 for x in f);z+=zeros;fiber_count+=1
   if d<0:identical+=s+1;ck(zeros==s+1,'identically_zero_fiber')
   else:
    ck(zeros<=d,'polynomial_root_bound');degree_sum+=d
    if d==s:full+=s+1
    g=f[:];deg=0
    while len(g)>1:
     g=[g[i+1]-g[i] for i in range(len(g)-1)]
     if any(g):deg+=1
     else:break
    ck(deg==d,'finite_difference_degree')
   if nu==():
    for a in aa:ck(a>=0,'identity_residual_positive_dimensions')
   if lam==(1,)*n:
    ck(d==s and all(x!=0 for x in f),'sign_row_full_degree_no_zeros')
 for eta in range(1,n//2+1):
  short=sum(s+1 for nu,R,s,mus in fibers if s<eta)
  ck(short<=p-len(parts(n-2*eta)),'short_fiber_fixed_point_tail')
 ck(z<=identical+degree_sum,'global_uniform_fiber_root_bound')
 rows.append({'n':n,'p':p,'fiber_count_with_rows':fiber_count,'zero_probability':str(F(z,p*p)),'identically_zero_fiber_entry_mass':str(F(identical,p*p)),'root_bound':str(F(identical+degree_sum,p*p)),'full_degree_nonzero_fiber_entry_mass':str(F(full,p*p))})
for s in range(1,24):
 f=[factorial(2*s)]+[0]*s;a=factorial(2*s)//(2**s)
 for r in range(s+1):ck(a*sum(K(s,j,r) for j in range(s+1))==f[r],'regular_character_countercontrol')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'small_fiber_tables':rows,'scope':'Finite exact transform and measure checks only. A bulk effective-degree or root estimate remains unproved.'},indent=2))
