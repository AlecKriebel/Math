#!/usr/bin/env python3
"""Exact diagnostics; no Monte Carlo and no claim to prove Brownian limits."""
from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import factorial
from pathlib import Path
import hashlib,json
N=0
counts={}
def ck(b,group):
 global N
 assert b,group
 N+=1;counts[group]=counts.get(group,0)+1

def solve(a,b):
 a=[list(map(F,row))+[F(v)] for row,v in zip(a,b)]
 n=len(b)
 for c in range(n):
  r=next(r for r in range(c,n) if a[r][c])
  a[c],a[r]=a[r],a[c]
  z=a[c][c];a[c]=[x/z for x in a[c]]
  for r in range(n):
   if r!=c and a[r][c]:
    z=a[r][c];a[r]=[x-z*y for x,y in zip(a[r],a[c])]
 return [a[r][-1] for r in range(n)]

def next_probs(A,z,L):
 # Distances in both directions on the cyclic lattice.
 dl=min((z-q)%L for q in A);dr=min((q-z)%L for q in A)
 left=(z-dl)%L;right=(z+dr)%L
 out={q:F(0) for q in A}
 out[left]+=F(dr,dl+dr);out[right]+=F(dl,dl+dr)
 return out

def product_order(targets,z,L,pi):
 ans=F(1);A=set(targets)
 for q in pi:
  ans*=next_probs(A,z,L)[q];A.remove(q);z=q
 return ans

def direct_order(targets,start,L,pi):
 # One global absorbing-chain system on (correct-prefix length, current site).
 m=len(pi);states=[]
 for r in range(m):
  remain=set(pi[r:])
  states.extend((r,z) for z in range(L) if z not in remain)
 ix={s:i for i,s in enumerate(states)};n=len(states)
 a=[[F(0)]*n for _ in states];b=[F(0)]*n
 for (r,z),i in ix.items():
  a[i][i]=1;remain=set(pi[r:])
  for w in ((z-1)%L,(z+1)%L):
   if w in remain:
    if w!=pi[r]:continue
    if r+1==m:b[i]+=F(1,2);continue
    dest=(r+1,w)
   else:dest=(r,w)
   a[i][ix[dest]]-=F(1,2)
 return solve(a,b)[ix[(0,start)]]

orders=0
for L in range(3,8):
 for m in range(1,min(4,L-1)+1):
  targets=tuple(range(0,m))
  for start in (L-1,):
   tot=F(0)
   for pi in permutations(targets):
    p=product_order(targets,start,L,pi)
    ck(p==direct_order(targets,start,L,pi),'global_absorbing_chain_order')
    ck(0<=p<=1,'order_bounds');tot+=p;orders+=1
   ck(tot==1,'order_normalization')
# All cyclic target configurations and all valid starting sites, including singleton.
configs=0
for L in range(3,9):
 for m in range(1,min(4,L-1)+1):
  for A in combinations(range(L),m):
   for z in range(L):
    if z in A:continue
    p=next_probs(A,z,L)
    ck(sum(p.values())==1,'endpoint_mass')
    ck(all(0<=x<=1 for x in p.values()),'endpoint_positivity')
    for shift in (1,2):
     pp=next_probs(tuple((q+shift)%L for q in A),(z+shift)%L,L)
     ck(all(p[q]==pp[(q+shift)%L] for q in A),'rotation_invariance')
    pr=next_probs(tuple((-q)%L for q in A),(-z)%L,L)
    ck(all(p[q]==pr[(-q)%L] for q in A),'reflection_invariance')
    if m==1:ck(next(iter(p.values()))==1,'singleton_two_endpoints')
    configs+=1

# Formal Laplace coefficients of sinh(alpha sqrt(2s))/sinh(ell sqrt(2s)).
# Independently compare their polynomial coefficients against u_j''=2u_(j-1),
# u_0=x/ell, and u_j(0)=u_j(ell)=0 for j>=1.
def val(p,x):return sum(c*x**i for i,c in enumerate(p))
def ode_coeffs(ell,degree):
 out=[[F(0),1/ell]]
 for _ in range(degree):
  old=out[-1];v=[F(0)]*(len(old)+2)
  for i,c in enumerate(old):v[i+2]=2*c/F((i+1)*(i+2))
  v[1]=-val(v,ell)/ell;out.append(v)
 return out
for ell in (F(1),F(2,3),F(7,4)):
 pol=ode_coeffs(ell,6)
 for r in range(1,8):
  alpha=ell*F(r,8)
  den=[ell**(2*j)*2**j/F(factorial(2*j+1)) for j in range(7)]
  num=[alpha**(2*j+1)*2**j/(ell*factorial(2*j+1)) for j in range(7)]
  ratio=[]
  for j in range(7):
   ratio.append(num[j]-sum(den[t]*ratio[j-t] for t in range(1,j+1)))
   ck(ratio[j]==val(pol[j],alpha),'laplace_sinh_ode')
   ck((-1)**j*ratio[j]>=0,'exit_moment_signs')
  ck(val(pol[0],alpha)+val(pol[0],ell-alpha)==1,'exit_mass')
  ck(-(val(pol[1],alpha)+val(pol[1],ell-alpha))==alpha*(ell-alpha),'mean_exit_time')
# Exact owner cones on a grid of positive increments: one owner or a boundary tie.
cone_cases=0
for k,m in ((2,1),(2,2),(3,1)):
 for pis in product(list(permutations(range(m))),repeat=k):
  for flat in product((1,2,3),repeat=k*m):
   h=[[0]*m for _ in range(k)]
   for i,pi in enumerate(pis):
    t=0
    for r,j in enumerate(pi):t+=flat[i*m+r];h[i][j]=t
   winners=[]
   for a in product(range(k),repeat=m):
    if all(h[a[j]][j]<h[i][j] for j in range(m) for i in range(k) if i!=a[j]):winners.append(a)
   unique=all(sum(h[i][j]==min(h[v][j] for v in range(k)) for i in range(k))==1 for j in range(m))
   ck(len(winners)==int(unique),'owner_cone_partition');cone_cases+=1
# Finite probability-space analogue of the complete tensor-moment identity.
# Each outcome specifies the owners of equal-length pieces; no independence assumed.
patterns=[(0,0,1),(1,0,1),(1,1,1)]
weights=[F(1,6),F(1,3),F(1,2)];theta=(F(2,3),F(7,4))
for m in range(7):
 lhs=sum(w*(sum(theta[a] for a in pat)/3)**m for w,pat in zip(weights,patterns))
 rhs=F(0)
 for xs in product(range(3),repeat=m):
  for labels in product(range(2),repeat=m):
   prob=sum(w for w,pat in zip(weights,patterns) if all(pat[x]==a for x,a in zip(xs,labels)))
   term=F(1)
   for a in labels:term*=theta[a]
   rhs+=prob*term/F(3**m)
 ck(lhs==rhs,'correlated_tensor_moments')
 ck(lhs<=max(theta)**m,'bounded_moments')
# Factorial outer remainder tends to zero and is uniform over probability mixtures.
for t in (F(0),F(1,2),F(1),F(7,3),F(10)):
 for m in range(12,25):
  b=t**(m+1)/factorial(m+1);bb=t**(m+2)/factorial(m+2)
  ck(bb<=b,'factorial_decay')
root=Path(__file__).resolve().parent
receipt={'problem_id':30003818,'verdict':'PASS_EXACT_DIAGNOSTICS','assertions':N,'groups':counts,'finite_cycle_order_instances':orders,'cyclic_configurations':configs,'owner_cone_cases':cone_cases,'artifact_sha256':hashlib.sha256((root/'JOINT_LAW.md').read_bytes()).hexdigest(),'scope':'Exact finite and algebraic diagnostics, not numerical evaluation or independent proof of the Brownian law.'}
print(json.dumps(receipt,indent=2,sort_keys=True))
