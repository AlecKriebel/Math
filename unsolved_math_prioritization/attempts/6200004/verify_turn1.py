from exact_linear import *
from fractions import Fraction
import json,random
checks=0;cats={};rng=random.Random(6200004)
def ck(x,k):
 global checks
 assert x,k;checks+=1;cats[k]=cats.get(k,0)+1
def change(n):
 U=eye(n);V=eye(n)
 for _ in range(8):
  if n<2:break
  i,j=rng.sample(range(n),2);a=rng.choice([-2,-1,1,2])
  U[i]=[x+a*y for x,y in zip(U[i],U[j])]
  # V <- V (I-a E_ij)
  for row in V:row[j]-=a*row[i]
 ck(mm(U,V)==eye(n),'integer_basis_inverse')
 return U,V
models=0
for q in range(2,7):
 for d in range(q+1,10):
  for p in [2,3,5,7]:
   cs=[[] for _ in range(d+1)];cs[q].append('free');cs[d-1].append('torsion_in');cs[d].append('torsion_out')
   for k in range(d):cs[k].append(('in',k));cs[k+1].append(('out',k))
   D=[]
   for k in range(d):
    M=zeros(len(cs[k+1]),len(cs[k]))
    M[cs[k+1].index(('out',k))][cs[k].index(('in',k))]=1
    if k==d-1:M[cs[k+1].index('torsion_out')][cs[k].index('torsion_in')]=p
    D.append(M)
   bases=[change(len(c)) for c in cs];Ds=[mm(mm(bases[k+1][0],D[k]),bases[k][1]) for k in range(d)]
   for k in range(d-1):ck(mm(Ds[k+1],Ds[k])==zeros(len(cs[k+2]),len(cs[k])),'cochain_identity')
   for ell in [0,2,3,5,7,11,13]:
    ranks=[rank(M,ell) for M in Ds]
    for k in range(d+1):
     b=len(cs[k])-(ranks[k-1] if k else 0)-(ranks[k] if k<d else 0)
     expected=int(k==q)+(int(k in [d-1,d]) if ell==p else 0)
     ck(b==expected,'coefficient_profile')
    if ell and ell!=p:ck(p*pow(p,-1,ell)%ell==1,'nonexceptional_contraction')
   ck(Fraction(p)*Fraction(1,p)==1,'rational_tail_contraction');models+=1
for q in range(1,20):
 for d in range(q,31):
  ck((Fraction(q,d)<Fraction(2,3))==(3*(q-1)+1<2*(d-1)),'boundary_shift')
  ck((3*q<2*d)==(d>=3*q//2+1),'strict_threshold')
print(json.dumps({'assertions':checks,'categories':cats,'finite_cochain_models':models,'scope':'Finite cochain controls; no group-resolution or hyperbolic-boundary realization is claimed.'},indent=2,sort_keys=True))
