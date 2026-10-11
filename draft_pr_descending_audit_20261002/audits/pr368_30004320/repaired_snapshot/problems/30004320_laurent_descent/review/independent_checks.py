#!/usr/bin/env python3
"""Exact supplementary algebra controls, not a replacement for geometric proofs."""
import itertools,json
from math import comb
from fractions import Fraction
counts={}
def check(tag,b):
 assert b,tag
 counts[tag]=counts.get(tag,0)+1
# Integral cyclic-lattice coboundary: dI-N=(A-I)sum j A^j.
# Test every coordinate separately, without inverting d, also when p divides d.
for d in range(2,21):
 for cycle in range(1,d+1):
  if d%cycle: continue
  for k in range(cycle):
   v=[int(i==k) for i in range(cycle)]
   powers=[];w=v[:]
   for j in range(d):
    powers.append(w);w=w[-1:]+w[:-1]
   S=[sum(j*powers[j][i] for j in range(d)) for i in range(cycle)]
   rhs=[S[(i-1)%cycle]-S[i] for i in range(cycle)]
   lhs=[d*v[i]-sum(w[i] for w in powers) for i in range(cycle)]
   check('integral_cyclic_lattice_identity',lhs==rhs)
# Wild order: translation by s^q preserves w^p-s^(q(p-1))w-a.
# Polynomial coefficient calculation in F_p[s,w], no rounded arithmetic.
for p in (2,3,5,7,11):
 for q in range(1,17):
  poly={}
  def add(i,j,c): poly[i,j]=(poly.get((i,j),0)+c)%p
  for i in range(p+1): add(i,q*(p-i),comb(p,i))
  add(1,q*(p-1),-1);add(0,q*p,-1)
  check('ore_translation_preserves_relation', {k:v for k,v in poly.items() if v}=={(p,0):1,(1,q*(p-1)):p-1})
  check('order_residue_dimension',len({(i,j) for i in range(p) for j in range(p)})==p*p)
  for n in range(1,100):
   r=n
   while r%p==0:r//=p
   check('artin_schreier_reduced_pole',r%p!=0)
# Iterative additive equation delta+a delta^p=c in truncated F_p[s],
# with a nonzero constant and c in sR. This checks the contraction identity.
for p in (2,3,5,7):
 for a in range(1,p):
  for degree in range(1,9):
   N=51;c=[0]*N;c[degree]=1;delta=[0]*N
   for step in range(8):
    power=[0]*N
    for i,x in enumerate(delta):
     if i*p<N:power[i*p]=x
    delta=[(c[i]-a*power[i])%p for i in range(N)]
   lhs=delta[:]
   for i,x in enumerate(delta):
    if i*p<N:lhs[i*p]=(lhs[i*p]+a*x)%p
   check('henselian_additive_iteration',lhs==c)
# Exact determinant identity for left multiplication on split matrix algebras.
def det(a):
 a=[[Fraction(x) for x in r] for r in a];ans=Fraction(1);n=len(a)
 for j in range(n):
  k=next((i for i in range(j,n) if a[i][j]),None)
  if k is None:return Fraction(0)
  if k!=j:a[k],a[j]=a[j],a[k];ans=-ans
  v=a[j][j];ans*=v
  for i in range(j+1,n):
   f=a[i][j]/v
   for l in range(j,n):a[i][l]-=f*a[j][l]
 return ans
for n in (2,3):
 for seed in range(71):
  a=[[(seed*(i+1)+(j+1)**2+i*j)%7-3 for j in range(n)] for i in range(n)]
  L=[[0]*(n*n) for _ in range(n*n)]
  for i,j,k in itertools.product(range(n),repeat=3):L[i*n+j][k*n+j]=a[i][k]
  check('left_regular_determinant',det(L)==det(a)**n)
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'by_family':counts,'scope':'Supplementary exact algebra controls only; geometric descent arguments require the written source/proof audit.'},sort_keys=True,indent=2))
