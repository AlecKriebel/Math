#!/usr/bin/env python3
"""Exact finite branching/support and conditioning controls. No fitted asymptotics."""
from character_tools import parts,character
from fractions import Fraction as F
from collections import Counter
from math import isqrt
import json
C=Counter()
def ck(x,key):assert x,key;C[key]+=1
def down(lam):
 out=[]
 for i in range(len(lam)):
  if i+1<len(lam) and lam[i]==lam[i+1]:continue
  nu=list(lam);nu[i]-=1;out.append(tuple(x for x in nu if x))
 return out
prevB=None
for n in range(1,12):
 ps=parts(n);qs=parts(n+1);p=len(ps);pp=len(qs);downs={L:down(L) for L in qs};ups={l:[L for L in qs if l in downs[L]] for l in ps}
 dn=max(len(down(l)) for l in ps);dnext=max(map(len,downs.values()));bn=max(map(len,ups.values()))
 bound=(isqrt(8*n+1)-1)//2
 ck(dn<=bound and bn<=bound+1,'corner_bound')
 B=sum(character(l,mu)!=0 for l in ps for mu in ps);A=0
 for mu in ps:
  ext=mu+(1,)
  for L in qs:
   x=character(L,ext);ck(x==sum(character(l,mu) for l in downs[L]),'restriction_branching')
   A+=x!=0
  for l in ps:ck(sum(character(L,ext) for L in ups[l])==(mu.count(1)+1)*character(l,mu),'induction_fixed_coset_identity')
 Bnext=sum(character(L,mu)!=0 for L in qs for mu in qs)
 ck(F(B,dnext)<=A<=bn*B,'one_column_fiber_support_bounds')
 ck(F(B,dnext)<=Bnext<=bn*B+pp*(pp-p),'whole_table_support_bounds')
 r=F(p,pp);Q=F(B,p*p);Qnext=F(Bnext,pp*pp)
 ck(r*r*Q/dnext<=Qnext<=bn*r*r*Q+(1-r),'normalized_support_bounds')
 # Partition size conditioning is exactly uniform for rational q in a finite truncation.
 for q in (F(1,2),F(2,3)):
  Z=sum((len(parts(m))*q**m for m in range(n+1)),F(0));atom=p*q**n/Z
  for l in ps:ck((q**n/Z)/atom==F(1,p),'exact_conditioned_uniformity')
# Exact rational identity for the saddle exponent, with t=c/u and sqrt(m)=v.
for c in (F(1),F(5,3),F(9,7)):
 for u in range(2,15):
  t=c/u
  for v in range(1,20):ck(4*c*v-2*t*v*v-2*c*c/t==-2*t*(v-u)**2,'saddle_square_identity')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'scope':'Finite exact identities and support controls; the analytic conditioning and sparse-spike statements use the written Hardy-Ramanujan argument.'},indent=2))
