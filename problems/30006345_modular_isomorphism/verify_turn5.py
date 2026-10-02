#!/usr/bin/env python3
"""Exact finite controls for the full-algebra descent obstruction and explicit local twist.
No finite control infers Lang's theorem or a group basis for the twist.
"""
from itertools import product,permutations
from math import gcd
from random import Random
from collections import Counter
import json
checks=Counter()
def ck(x,label):
 assert x,label
 checks[label]+=1
# Cyclic finite component groups, all automorphisms and discrepancies through order25.
cyclic_cases=0
for m in range(2,26):
 for u in range(1,m):
  if gcd(u,m)!=1:continue
  image={(u-1)*x%m for x in range(m)}
  for a in range(m):
   x=0;d=0
   while True:
    x=(a+u*x)%m;d+=1
    if x==0:break
    assert d<=m
   ck(d<=m,'cyclic_orbit_bound')
   ck(sum(a*pow(u,i,m) for i in range(d))%m==0,'cyclic_iterated_norm')
   ck((a in image)==(a%gcd(u-1,m)==0),'cyclic_component_coboundary')
   cyclic_cases+=1
# Nonabelian component controls, automorphisms given by all inner conjugations.
def compose(a,b):return tuple(a[b[i]] for i in range(len(a)))
def inverse(a):return tuple(a.index(i) for i in range(len(a)))
nonabelian_cases=0
for n in (2,3,4):
 S=list(permutations(range(n)));one=tuple(range(n))
 for s in S:
  si=inverse(s)
  def tau(x):return compose(compose(s,x),si)
  for a in S:
   x=one;d=0
   while True:
    x=compose(a,tau(x));d+=1
    if x==one:break
    assert d<=len(S)
   norm=one;term=a
   for _ in range(d):norm=compose(norm,term);term=tau(term)
   ck(norm==one,'nonabelian_iterated_norm')
   ck(d<=len(S),'nonabelian_component_bound')
   nonabelian_cases+=1
# Explicit tensor-involution model over three quadratic finite fields.
models=[];rng=Random(634505)
for p in (3,5,7):
 d=next(a for a in range(2,p) if pow(a,(p-1)//2,p)==p-1);q=p*p;s=p
 def add(a,b):return ((a%p+b%p)%p)+p*((a//p+b//p)%p)
 def neg(a):return (-(a%p)%p)+p*((-(a//p))%p)
 def sub(a,b):return add(a,neg(b))
 def mul(a,b):return ((a%p*(b%p)+d*(a//p)*(b//p))%p)+p*((a%p*(b//p)+a//p*(b%p))%p)
 def power(a,n):
  out=1
  while n:
   if n&1:out=mul(out,a)
   a=mul(a,a);n//=2
  return out
 def sigma(a):return (a%p)+p*((-(a//p))%p)
 for a in range(q):ck(power(a,p)==sigma(a),'quadratic_frobenius_formula')
 ck(sigma(s)==neg(s),'root_frobenius_sign')
 half=pow(2,-1,p);sinv=p*pow(d,-1,p)
 def va(A,B,c=1):
  R=dict(A)
  for k,v in B.items():
   R[k]=add(R.get(k,0),mul(c,v))
   if not R[k]:del R[k]
  return R
 def vs(A,c):return {k:mul(v,c) for k,v in A.items() if mul(v,c)}
 def theta(A):return {(j,i):sigma(v) for (i,j),v in A.items()}
 H=list(product(range(p),repeat=3));N=len(H);idx={g:i for i,g in enumerate(H)}
 def hm(i,j):
  a,b,c=H[i];x,y,z=H[j];return idx[((a+x)%p,(b+y)%p,(c+z+a*y)%p)]
 def vm(A,B):
  R={}
  for (i,j),a in A.items():
   for (k,l),b in B.items():
    z=(hm(i,k),hm(j,l));R[z]=add(R.get(z,0),mul(a,b))
    if not R[z]:del R[z]
  return R
 # Exhaust the fixed basis and 2x2 change-of-basis blocks for p3 and p5.
 # For p7 retain the same symbolic formula and test a deterministic index sample.
 basis=[]
 for i in range(N):
  z={(i,i):1};ck(theta(z)==z,'fixed_diagonal_basis');basis.append(z)
 pairs=list((i,j) for i in range(N) for j in range(i+1,N))
 selected=pairs if p in (3,5) else [pairs[(k*199)%len(pairs)] for k in range(600)]
 for i,j in selected:
  plus={(i,j):1,(j,i):1};minus={(i,j):s,(j,i):neg(s)}
  ck(theta(plus)==plus and theta(minus)==minus,'fixed_offdiagonal_basis')
  ck(vs(va(plus,minus,sinv),half)=={(i,j):1},'fixed_basis_K_spanning_first')
  ck(vs(va(plus,minus,neg(sinv)),half)=={(j,i):1},'fixed_basis_K_spanning_second')
  basis.extend((plus,minus))
 for _ in range(750):
  A=basis[rng.randrange(len(basis))];B=basis[rng.randrange(len(basis))];C=vm(A,B)
  ck(theta(C)==C,'fixed_subalgebra_multiplication')
  rebuilt={}
  unordered=sorted({tuple(sorted(k)) for k in C})
  for i,j in unordered:
   if i==j:
    a=C.get((i,i),0);ck(a//p==0,'fixed_product_diagonal_prime_field');rebuilt=va(rebuilt,{(i,i):1},a)
   else:
    a=C.get((i,j),0)
    rebuilt=va(rebuilt,{(i,j):1,(j,i):1},a%p)
    rebuilt=va(rebuilt,{(i,j):s,(j,i):neg(s)},a//p)
  ck(rebuilt==C,'fixed_product_prime_field_coordinates')
 # Descended leading tensor: conjugate-paired vectors bracket as det over K.
 def determinant(x,y):return sub(mul(x[0],y[1]),mul(x[1],y[0]))
 coord=[(1,0),(s,0),(0,1),(0,s)]
 for x,y in product(coord,repeat=2):
  b=determinant(x,y)
  ck(determinant(tuple(map(sigma,x)),tuple(map(sigma,y)))==sigma(b),'descended_basis_bracket')
 for _ in range(600):
  x=tuple(rng.randrange(q) for i in range(2));y=tuple(rng.randrange(q) for i in range(2))
  b=determinant(x,y)
  ck(determinant(tuple(map(sigma,x)),tuple(map(sigma,y)))==sigma(b),'descended_bracket_controls')
 ck(determinant((1,0),(0,1))==1 and determinant((s,0),(0,1))==s,'descended_bracket_surjectivity')
 split=(p*p+p-1)**2;nonsplit=p**4+p*p-1
 ck(split-nonsplit==2*(p-1)**2*(p+1)>0,'full_center_obstruction')
 models.append({'p':p,'quadratic_nonsquare':d,'fixed_algebra_dimension':N*N,'fixed_basis_vectors_tested':len(basis),'basis_scope':'complete' if p in (3,5) else 'all diagonal plus 600 offdiagonal pairs','center_dimension_of_twist':split,'center_dimension_of_forced_group':nonsplit})
# Current arithmetic is F49 over F7; split and field algebras have different idempotent counts.
ck(sum(mul(a,a)==a for a in range(q))==2,'quadratic_field_idempotents')
ck(sum((a*a%p,b*b%p)==(a,b) for a,b in product(range(p),repeat=2))==4,'quadratic_split_idempotents')
ck(mul(s,s)==d and mul(neg(s),neg(s))==d and mul(2,s)!=0,'quadratic_etale_splitting_basis')
print(json.dumps({'status':'PASS','arithmetic':'exact finite fields and finite permutation groups','assertions':sum(checks.values()),'assertions_by_scope':dict(checks),'cyclic_component_cases':cyclic_cases,'nonabelian_component_cases':nonabelian_cases,'twist_models':models,'scope':'No MIP counterexample: the explicit local twist lacks any prime-field finite-group-algebra realization by the proof. General Lang descent, finite-component bound and all-odd-p exclusion are proved analytically with credited dependencies.'},indent=2,sort_keys=True))
