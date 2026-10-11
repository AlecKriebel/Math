#!/usr/bin/env python3
"""Exact controls for the cut-open lift and conjugation-transport formula."""
from collections import Counter
from itertools import product,permutations
import json
C=Counter()
def ck(x,name):
 assert x,name
 C[name]+=1

def inverse(w):return tuple(-a for a in reversed(w))
def expand(w):
 out={():1}
 for a in w:
  x=abs(a);sgn=1 if a>0 else -1
  factor={():1,(x,):sgn}
  if sgn<0:factor[(x,x)]=1
  nxt=Counter()
  for u,c in out.items():
   for v,d in factor.items():
    if len(u+v)<=2:nxt[u+v]+=c*d
  out={u:c for u,c in nxt.items() if c}
 return out

def exp_sum(w,i):return sum((1 if a>0 else -1) for a in w if abs(a)==i)
def conjugate(h,a,sign):return h+(sign*a,)+inverse(h)
def formula(factors,i,j):
 O=sum(e*f for r,(h,a,e) in enumerate(factors) for hh,b,f in factors[r+1:] if a==i and b==j)
 correction=sum(e*((a==j)*exp_sum(h,i)-(a==i)*exp_sum(h,j)) for h,a,e in factors)
 return O+correction

hs=[w for n in range(4) for w in product((1,-1,2,-2,3,-3),repeat=n)]
for h in hs:
 for a,sign in product(range(1,4),(-1,1)):
  E=expand(conjugate(h,a,sign))
  for i,j in permutations(range(1,4),2):
   ck(E.get((i,j),0)==formula([(h,a,sign)],i,j),'all_single_factor_transports')
# Non-independent factor lists are deliberately allowed: the algebraic identity
# concerns arbitrary deterministic choices, not a probabilistic sampling model.
for n in range(1,6):
 for code in range(1200):
  factors=[];word=()
  for r in range(n):
   h=hs[(code*(r+1)+17*r*r)%len(hs)]
   a=1+((code//(r+1)+r)%4);sign=(-1)**((code+r)//2)
   factors.append((h,a,sign));word+=conjugate(h,a,sign)
  E=expand(word)
  for i,j in permutations(range(1,5),2):
   ck(E.get((i,j),0)==formula(factors,i,j),'ordered_product_transport')
  # A meridian-4 framing factor cannot alter coefficients only involving1,2.
  for power in (-3,2):
   frame=tuple([4 if power>0 else -4]*abs(power))
   ck(expand(word+frame).get((1,2),0)==E.get((1,2),0),'framing_factor_exclusion')

# Closure relator lattice in class two, for every small symmetric linking matrix.
for b12,b13,b23 in product(range(-2,3),repeat=3):
 B=[[0,b12,b13],[b12,0,b23],[b13,b23,0]]
 rel=[]
 for a in range(3):
  ell=()
  for b in range(3):
   power=B[a][b]
   ell+=tuple([b+1 if power>=0 else -(b+1)]*abs(power))
  comm=(a+1,)+ell+(-(a+1),)+inverse(ell)
  E=expand(comm);rel.append(E)
  ck(all(E.get((i,),0)==0 for i in range(1,4)),'closure_relators_central')
  for i,j in permutations(range(1,4),2):
   expected=(B[a][j-1] if a==i-1 else 0)-(B[a][i-1] if a==j-1 else 0)
   ck(E.get((i,j),0)==expected,'closure_relator_coordinates')
 for z in product(range(-2,3),repeat=3):
  for i,j in ((1,2),(1,3),(2,3)):
   ck(sum(z[a]*rel[a].get((i,j),0) for a in range(3))==B[i-1][j-1]*(z[i-1]-z[j-1]),'closure_kernel_coefficient_lattice')

# Independent normal form in Z² * Z verifies the Hopf-plus-split-unknot control.
def quotient_normal(w):
 blocks=[]
 for x in w:
  factor='A' if abs(x) in (1,2) else 'B'
  value=((1 if x>0 else -1),0) if abs(x)==1 else ((0,1 if x>0 else -1) if abs(x)==2 else (1 if x>0 else -1,))
  if blocks and blocks[-1][0]==factor:
   old=blocks.pop()[1];value=tuple(a+b for a,b in zip(old,value))
  if any(value):blocks.append((factor,value))
 return tuple(blocks)
comm=(1,2,-1,-2)
ck(quotient_normal(comm)==quotient_normal(()),'closed_group_nonunique_lift')
ck(expand(comm).get((1,2),0)==1 and expand(()).get((1,2),0)==0,'closed_group_nonunique_lift')
for h in hs:
 ck(quotient_normal(h+comm+inverse(h))==(),'normal_closure_negative_control')

# Explicit transport cannot be omitted even for a single conjugated meridian.
E=expand((2,1,-2))
ck(E.get((1,2),0)==-1 and E.get((2,1),0)==1,'nonzero_transport_example')
ck(formula([((2,),1,1)],1,2)==-1,'nonzero_transport_example')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'groups':dict(sorted(C.items())),'arithmetic':'exact integers only','scope':'Finite class-two Magnus, conjugation, framing and closed-group controls. The cut-open exterior, canonical basing and actual Wirtinger geometry are justified in the written argument; the original all-order derived-surface target remains unresolved.'},indent=2,sort_keys=True))
