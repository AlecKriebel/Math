#!/usr/bin/env python3
"""Exact locally authored character-table and residual-zero controls. No imported executable code."""
from functools import lru_cache
from collections import Counter
from fractions import Fraction
import math,json
C=Counter()
def ck(v,key):assert v,key;C[key]+=1
@lru_cache(None)
def parts(n,cap=None):
 if n==0:return ((),)
 if cap is None:cap=n
 return tuple((j,)+p for j in range(min(cap,n),0,-1) for p in parts(n-j,j))
@lru_cache(None)
def hooks(lam):
 return tuple(lam[i]-j+sum(row>j for row in lam[i+1:]) for i in range(len(lam)) for j in range(lam[i]))
@lru_cache(None)
def strip(lam,t):
 l=len(lam);B={lam[i]+l-1-i for i in range(l)};out=[]
 for b in B:
  a=b-t
  if a<0 or a in B:continue
  Bs=sorted(B-{b}|{a},reverse=True);nu=tuple(x-l+1+i for i,x in enumerate(Bs));nu=tuple(x for x in nu if x)
  sign=(-1)**sum(a<x<b for x in B);out.append((nu,sign))
 return tuple(out)
@lru_cache(None)
def character(lam,mu):
 if not mu:return int(not lam)
 return sum(e*character(nu,mu[1:]) for nu,e in strip(lam,mu[0]))
@lru_cache(None)
def paths(lam,mu):
 if not mu:return int(not lam)
 return sum(paths(nu,mu[1:]) for nu,e in strip(lam,mu[0]))
def centralizer(mu):
 c=Counter(mu);v=1
 for t,n in c.items():v*=t**n*math.factorial(n)
 return v
def types(lam,mu):
 hs=hooks(lam);I=not any(x%mu[0]==0 for x in hs);II=any(not any(x%t==0 for x in hs) for t in mu)
 III=any(sum(x//t for x in mu if x%t==0)>sum(x%t==0 for x in hs) for t in range(2,sum(mu)+1))
 return I,II,III
def mobius(n):
 sign=1;p=2
 while p*p<=n:
  if n%p==0:
   n//=p;sign=-sign
   if n%p==0:return 0
   while n%p==0:n//=p
  p+=1
 if n>1:sign=-sign
 return sign
rows=[]
for n in range(1,13):
 ps=parts(n);tab=[[character(lam,mu) for mu in ps] for lam in ps]
 stats=Counter()
 for i,lam in enumerate(ps):
  # Hook length dimension formula is independent of the recursive one-cycle removals.
  ck(tab[i][-1]==math.factorial(n)//math.prod(hooks(lam)),'dimension_hook_formula')
  for j,mu in enumerate(ps):
   I,II,III=types(lam,mu);val=tab[i][j]
   ck((not I or II) and (not II or III),'type_inclusions')
   if III:ck(val==0,'type_III_sufficient')
   if val==0:
    stats['zeros']+=1
    if not III:stats['outside_III']+=1
    if paths(lam,mu)>0:stats['cancellation_zeros']+=1
    else:stats['no_strip_chain_zeros']+=1
 for j,mu in enumerate(ps):
  ck(sum(row[j]**2 for row in tab)==centralizer(mu),'column_norm')
 if n<=9:
  for j in range(len(ps)):
   for h in range(j):ck(sum(row[j]*row[h] for row in tab)==0,'column_orthogonality')
 # Correctly distinguish uniform classes from uniform elements.
 P=Fraction(stats['zeros'],len(ps)**2);Pg=sum((Fraction(sum(row[j]==0 for row in tab),len(ps)*centralizer(mu)) for j,mu in enumerate(ps)),Fraction(0))
 rows.append({'n':n,'p':len(ps),**dict(stats),'uniform_classes':str(P),'uniform_elements':str(Pg)})
for m in range(2,32):
 n=m+1;lam=(n-1,1);actual=0
 for nu in parts(m):
  if nu[-1]==1:continue
  mu=nu+(1,);g=math.gcd(*nu);III=types(lam,mu)[2]
  ck(character(lam,mu)==0,'standard_character_one_fixed_point')
  ck(III==(g>1),'standard_type_III_exact_gcd')
  ck(types(lam,mu)[1]==(nu==(m,)),'standard_type_II_exact_single_part')
  if g==1:actual+=1
 expected=len(parts(m))-len(parts(m-1))+sum(mobius(d)*len(parts(m//d)) for d in range(2,m+1) if m%d==0)
 ck(actual==expected,'mobius_residual_zero_count')
# A concrete sequential extinction zero outside all three standard types.
lam=(5,1);mu=(3,2,1)
ck(character(lam,mu)==0 and paths(lam,mu)==0 and not any(types(lam,mu)),'six_letter_multistep_obstruction')
ck(paths((5,1),(1,3,2))==2 and character((5,1),(1,3,2))==0,'same_witness_order_dependence')
ck(character((2,2),(2,1,1))==0 and paths((2,2),(2,1,1))==2 and not types((2,2),(2,1,1))[2],'genuine_signed_cancellation_outside_III')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'small_tables':rows,'witness':{'lambda':lam,'mu':mu,'value':character(lam,mu),'unsigned_strip_chain_count':paths(lam,mu),'first_one_order_chain_count':paths(lam,(1,3,2))},'scope':'Finite exact checks only; no asymptotic inference from the table rows.'},indent=2))
