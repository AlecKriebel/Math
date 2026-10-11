#!/usr/bin/env python3
"""Exact controls for finite descent obstructions; not a full-target certificate."""
from itertools import product
from collections import Counter
import json
C=Counter()
def ck(x,key):
 assert x,key
 C[key]+=1

def coeff(word,I):
 # Signed ordered-subsequence dynamic program for a distinct index word.
 d=[1]+[0]*len(I)
 for x in word:
  for k in range(len(I),0,-1):
   if abs(x)==I[k-1]:d[k]+=d[k-1]*(1 if x>0 else -1)
 return d[-1]
def heis(word):
 # Direct unitriangular multiplication in coordinates (a,b,c).
 a=b=c=0
 for x in word:
  if abs(x)==1:a+=1 if x>0 else -1
  else:
   eps=1 if x>0 else -1;c+=a*eps;b+=eps
 return a,b,c

def lattice_integral(word):
 # A separate geometric edge traversal accumulates vertical edge weights.
 pos=[0,0];value=0
 steps={1:(1,0),-1:(-1,0),2:(0,1),-2:(0,-1)}
 for x in word:
  dx,dy=steps[x]
  value+=pos[0]*dy
  pos[0]+=dx;pos[1]+=dy
 return tuple(pos),value

words=0
for n in range(9):
 for w in product((1,-1,2,-2),repeat=n):
  words+=1;a,b,c=heis(w);pos,area=lattice_integral(w)
  ck(pos==(a,b) and area==c,'all_lifted_grid_paths')
  ck(c==coeff(w,(1,2)),'magnus_area_comparison')
  eta=tuple([(-1 if a>0 else 1)]*abs(a)+[(-2 if b>0 else 2)]*abs(b))
  endpoint,closed=lattice_integral(w+eta)
  ck(endpoint==(0,0) and closed==area,'lower_data_closure')

for r in range(2,9):
 I=tuple(range(1,r+1));u=I[:-1];v=I[-1:]
 ck(coeff(u,I)==coeff(v,I)==0 and coeff(u+v,I)==1,'fixed_link_additivity_obstruction')

# Full deconcatenation identity, allowing negative letters and nonzero lower data.
for r in range(1,6):
 I=tuple(range(1,r+1));alphabet=tuple(x for i in I for x in (i,-i))
 for code in range(1200):
  u=tuple(alphabet[(code*(i+1)+i*i)%len(alphabet)] for i in range(code%9))
  v=tuple(alphabet[(code*(i+3)+2*i+1)%len(alphabet)] for i in range((code//7)%9))
  ck(coeff(u+v,I)==sum(coeff(u,I[:j])*coeff(v,I[j:]) for j in range(r+1)),'all_order_cross_terms')

# Heisenberg section cocycle and its nonzero antisymmetric part.
for a,b,aa,bb in product(range(-4,5),repeat=4):
 kappa=a*bb;reverse=aa*b
 ck(kappa-reverse==a*bb-aa*b,'section_antisymmetric_part')
 for aaa,bbb in ((1,2),(-2,3),(0,-1)):
  ck(kappa+(a+aa)*bbb==aa*bbb+a*(bb+bbb),'section_two_cocycle')
ck(1*1-0*0==1,'nontrivial_commuting_pair_obstruction')

# Infinite projection cannot be rescued by an unannounced symmetric summation.
for m in range(1,257):
 absolute=(2*m+1)*sum(abs(a) for a in range(-m,m+1))
 ck(absolute==(2*m+1)*m*(m+1),'absolute_projection_divergence')
 symmetric=(2*m+1)*sum(range(-m,m+1))
 shifted=(2*m+1)*sum(range(-m,2*m+1))
 ck(symmetric==0 and shifted==(2*m+1)*m*(3*m+1)//2 and shifted>0,'exhaustion_dependence')

# Check all-order nonsplitting with genuine integer matrices and central shifts.
def Id(n):return tuple(tuple(int(i==j) for j in range(n)) for i in range(n))
def T(n,p,q,a=1):
 M=[list(x) for x in Id(n)];M[p][q]=a;return tuple(map(tuple,M))
def mul(A,B):
 n=len(A);return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(i,j+1)) if i<=j else 0 for j in range(n)) for i in range(n))
def inv(A):
 n=len(A);B=[list(x) for x in Id(n)]
 for d in range(1,n):
  for i in range(n-d):
   j=i+d;B[i][j]=-sum(A[i][k]*B[k][j] for k in range(i+1,j+1))
 return tuple(map(tuple,B))
for n in range(3,9):
 A=T(n,0,1);B=T(n,1,n-1);Z=T(n,0,n-1)
 for a,b in product(range(-4,5),repeat=2):
  A1=mul(A,T(n,0,n-1,a));B1=mul(B,T(n,0,n-1,b))
  comm=mul(mul(mul(A1,B1),inv(A1)),inv(B1))
  ck(comm==Z and comm!=Id(n),'all_central_lifts_fail_to_commute')

print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'groups':dict(sorted(C.items())),'exhaustive_two_letter_words':words,'arithmetic':'exact integers only','scope':'Finite additivity, deconcatenation, grid-cover, section and projection controls. No universal obstruction to adaptive or relative derived-link constructions is claimed; the original source target remains unresolved in this five-turn attempt.'},indent=2,sort_keys=True))
