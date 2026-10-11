#!/usr/bin/env python3
"""Exact controls of the nilpotent-cover cocycle and lower-data closure."""
from itertools import combinations
from collections import Counter
import json
C=Counter()
def ck(x,key):
 assert x,key
 C[key]+=1

def I(n):return tuple(tuple(int(i==j) for j in range(n)) for i in range(n))
def mul(A,B):
 n=len(A)
 return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(i,j+1)) if i<=j else 0 for j in range(n)) for i in range(n))
def inverse(A):
 n=len(A);B=[list(x) for x in I(n)]
 for d in range(1,n):
  for i in range(n-d):
   j=i+d;B[i][j]=-sum(A[i][k]*B[k][j] for k in range(i+1,j+1))
 return tuple(map(tuple,B))
def T(n,p,q,c=1):
 A=[list(x) for x in I(n)];A[p][q]=c;return tuple(map(tuple,A))
def section(A):
 B=[list(x) for x in A];B[0][-1]=0;return tuple(map(tuple,B))
def qm(A,B):return section(mul(A,B))
def sample(n,seed):
 A=[list(x) for x in I(n)]
 for p,q in combinations(range(n),2):A[p][q]=(seed*(p+2)*(q+3)+11*p-7*q)%7-3
 return tuple(map(tuple,A))
def central(A):return all(A[p][q]==0 for p,q in combinations(range(len(A)),2) if (p,q)!=(0,len(A)-1))
def b(q,g):
 end=qm(q,section(g));z=mul(mul(q,g),inverse(end))
 assert central(z)
 return z[0][-1]
def comm(A,B):return mul(mul(mul(A,B),inverse(A)),inverse(B))
def comm_word(p,q):
 if q==p+1:return (p+1,)
 a=(p+1,);v=comm_word(p+1,q)
 return a+v+tuple(-x for x in reversed(a))+tuple(-x for x in reversed(v))
def evaluate(w,n):
 A=I(n)
 for x in w:A=mul(A,T(n,abs(x)-1,abs(x),1 if x>0 else -1))
 return A

for n in range(2,8):
 for p,q in combinations(range(n),2):
  w=comm_word(p,q)
  ck(evaluate(w,n)==T(n,p,q),'all_adjacent_commutator_transvections')
  if q>p+1:
   ck(all(sum((1 if x>0 else -1) for x in w if abs(x)==j)==0 for j in range(1,n)),'zero_abelianization')
 for seed in range(120):
  G=sample(n,seed);H=sample(n,seed+17);q=section(sample(n,seed+43));end=qm(q,section(G))
  ck(b(q,G)+b(end,H)==b(q,mul(G,H)),'cover_cocycle_concatenation')
  ck(b(end,inverse(G))==-b(q,G),'lifted_edge_reversal')
  ck(qm(qm(q,section(G)),section(H))==qm(q,qm(section(G),section(H))),'quotient_associativity')
  ck(b(q,I(n))==0,'identity_edge')
  # Corrected closure depends on the zero-top section, never the top target.
  lower=section(G);eta=inverse(lower);closed=mul(G,eta)
  ck(closed==T(n,0,n-1,G[0][-1]),'lower_only_closure')
  modified=mul(G,T(n,0,n-1,13))
  ck(section(modified)==lower,'target_not_used_by_section')
  ck(mul(modified,eta)==T(n,0,n-1,G[0][-1]+13),'target_retained_exactly')
  # Explicit transvection factorization of eta, with integral coefficients.
  factors=[]
  for p in range(n-2,-1,-1):
   for qq in range(p+1,n):factors.append(T(n,p,qq,eta[p][qq]))
  product=I(n)
  for F in factors:product=mul(product,F)
  ck(product==eta,'boundary_word_elimination')
  # Any section change is an exact vertex coboundary on the cover.
  phi=lambda Q:sum((p+1)*(j+2)*Q[p][j] for p,j in combinations(range(n),2) if (p,j)!=(0,n-1))
  sq=mul(q,T(n,0,n-1,phi(q)));se=mul(end,T(n,0,n-1,phi(end)))
  changed=mul(mul(sq,G),inverse(se))
  ck(changed==T(n,0,n-1,b(q,G)+phi(q)-phi(end)),'section_coboundary')

for n in range(3,8):
 w=comm_word(0,n-1);q=I(n);total=0;hol=I(n)
 for x in w:
  g=T(n,abs(x)-1,abs(x),1 if x>0 else -1)
  total+=b(q,g);q=qm(q,section(g));hol=mul(hol,g)
 ck(q==I(n) and central(hol),'closed_lift_of_central_commutator')
 ck(total==1 and hol[0][-1]==1,'surface_class_descent_obstruction')

# The triple return word x1^(-a) x2^(-b) cancels the lower entries exactly.
for a in range(-30,31):
 for bb in range(-30,31):
  S=mul(T(3,1,2,bb),T(3,0,1,a));eta=mul(T(3,0,1,-a),T(3,1,2,-bb))
  ck(S==section(S) and mul(S,eta)==I(3),'triple_return_word')
  for c in (-3,0,4):
   G=mul(S,T(3,0,2,c))
   ck(mul(G,eta)==T(3,0,2,c),'triple_integer_retained')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'groups':dict(sorted(C.items())),'arithmetic':'exact integer matrices and group words only','scope':'Finite controls for the cover cocycle, lower-data correction, section independence and descent obstruction. Proper smooth surface realization and the cohomology pairing are written topological arguments; no downstairs iterated-derived-link comparison is claimed.'},indent=2,sort_keys=True))
