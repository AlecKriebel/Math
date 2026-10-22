#!/usr/bin/env python3
"""Independent exact review controls; does not import any author checker.
Requires preinstalled SymPy. Topology for unbounded dimensions is reviewed in prose.
"""
from fractions import Fraction as F
from itertools import combinations,product,permutations
from collections import Counter
from random import Random
import json
import sympy as sp
counts=Counter()
def check(x,label):
    assert x,label
    counts[label]+=1

def monomial_derivative(S,j,y):
    if j not in S:return 0
    ans=1
    for k in S:
        if k!=j:ans*=y[k]
    return ans
# Full-support tangent-functional isolation, with nonuniform powers-of-two points.
for n in range(3,8):
 for d in range(3,n+1):
  supports=list(combinations(range(n),d))
  for S in supports:
   for ell in S:
    T=[j for j in S if j!=ell];i=T[0];y=[0]*n
    for k,j in enumerate(T[:-1]):y[j]=2**k
    y[T[-1]]=-sum(y)
    check(sum(y)==0 and all(y[j] for j in T),'turn1_tangent_point')
    expected=1
    for j in T:expected*=y[j]
    for U in supports:
     val=monomial_derivative(U,ell,y)-monomial_derivative(U,i,y)
     check(val==(expected if U==S else 0),'turn1_coefficient_isolation')
# Independent row-space, zero-feasibility and degree matching checks.
rng=Random(30006211);systems=0
for n in range(1,7):
 for rows in range(1,4):
  for repeat in range(13):
   A=sp.Matrix([[rng.randrange(-2,3) for _ in range(n)] for _ in range(rows)])
   h=sp.Matrix([rng.randrange(-3,4) for _ in range(n)]);c=A*h
   N=A.nullspace();fixed=[]
   for i in range(n):
    e=sp.zeros(1,n);e[i]=1
    isfixed=all(v[i]==0 for v in N)
    check(isfixed==(A.col_join(e).rank()==A.rank()),'turn2_rowspace_criterion')
    zero_possible=A.col_join(e).rank()==A.col_join(e).row_join(c.col_join(sp.Matrix([0]))).rank()
    check(zero_possible==(not isfixed or h[i]==0),'turn2_zero_coordinate_feasibility')
    if isfixed and h[i]!=0:fixed.append(i)
   check(len(fixed)<=A.rank(),'turn2_fixed_count_rank_bound')
   sizes=[rng.randrange(1,6) for _ in range(n)]
   degrees=[max([sizes[i] for i in range(n) if A[a,i]!=0] or [0]) for a in range(rows)]
   matched=any(all(A[a,i]!=0 for a,i in zip(choice,fixed)) for choice in permutations(range(rows),len(fixed)))
   check(matched,'turn2_nonzero_matching')
   check(sum(sizes[i]-1 for i in fixed)<=sum(max(d-1,0) for d in degrees),'turn2_degree_sensitive_bound')
   systems+=1
# Rational Gram-section reconstruction for rank-drop attachments.
regular_models=attachments=0
for m in range(3,8):
 for diag in [(1,)*(m-1)+(0,),(1,)+(0,)*(m-2)+(2,),(0,)*m]:
  C=sp.diag(*diag)
  if diag==(0,)*m:
   for i in range(m-1):C[i,i+1]=1
  U=sp.eye(m)
  for i in range(m-1):U[i,i+1]=(i%3)+1
  C=U*C*U.inv();CT=C.T
  if C.rank()<2:continue
  regular_models+=1
  for x0 in CT.nullspace():
   for sign in [-1,1]:
    x0=sign*x0
    delta=next(sp.eye(m)[:,i] for i in range(m) if sp.Matrix.hstack(x0,CT[:,i]).rank()==2)
    v=CT*delta
    for t in [sp.Rational(-1,17),sp.Rational(1,19),sp.Rational(1,23)]:
     x=x0+t*delta;M=sp.Matrix.vstack(x.T,v.T)
     y=M.T*(M*M.T).inv()*sp.Matrix([1,0])
     check((x.T*y)[0]==1 and (x.T*C*y)[0]==0,'turn3_gram_attachment')
     check(sp.Matrix.hstack(x,CT*x).rank()==2,'turn3_rank_two_nearby')
     attachments+=1
# Singular blocks: exact Gram inverse computed directly, different values/control grid.
def dot(a,b):return sum(x*y for x,y in zip(a,b))
short_vectors=0
for eps in range(1,7):
 for z in product((-2,0,3),repeat=eps):
  if not any(z):continue
  a=list(z)+[0];b=[0]+list(z)
  aa,bb,ab=dot(a,a),dot(b,b),dot(a,b);D=aa*bb-ab*ab
  check(D>0,'turn4_singular_gram_positive')
  short_vectors+=1
  for c,d in [(0,0),(1,-2),(-3,4),(F(2,7),F(-5,11))]:
   alpha=(bb*c-ab*d)/F(D);beta=(aa*d-ab*c)/F(D)
   w=[alpha*x+beta*y for x,y in zip(a,b)]
   check(dot(a,w)==c and dot(b,w)==d,'turn4_singular_exact_section')
  for t in [F(-1,3),0,F(2,5)]:
   check(dot([t*x for x in a],[0]*(eps+1))==0 and dot([t*x for x in b],[0]*(eps+1))==0,'turn4_zero_stratum_attachment')
# Sparse polynomial arithmetic with t_i abstractions (substitution t_i=x_i*y_i).
def add(a,b,factor=1):
 r=dict(a)
 for k,v in b.items():
  r[k]=r.get(k,0)+factor*v
  if not r[k]:del r[k]
 return r
def mul(a,b):
 r={}
 for x,c in a.items():
  for y,d in b.items():
   z=tuple(u+v for u,v in zip(x,y));r[z]=r.get(z,0)+c*d
 return {z:v for z,v in r.items() if v}
def var(n,i):return {tuple(int(j==i) for j in range(n)):1}
for m in range(2,21):
 n=m+1;one={(0,)*n:1};t=[var(n,i+1) for i in range(m)];x0=var(n,0)
 T={};Fpoly={};E={};H={};squares={};fi=[add(v,one,-1) for v in t]
 for v,f in zip(t,fi):T=add(T,v);Fpoly=add(Fpoly,f);squares=add(squares,mul(f,f))
 for i,j in combinations(range(m),2):E=add(E,mul(t[i],t[j]));H=add(H,mul(fi[i],fi[j]))
 P=add(x0,T,-1);Q=add(add(add(mul(x0,T),E,-2),T,-2),one,m)
 check(add(mul(Fpoly,Fpoly),H,-2)==squares,'turn5_campaign_identity')
 check(add(Q,mul(T,P),-1)==squares,'turn5_prior_identity')
 centeredP=add(x0,Fpoly,-1);centeredQ=add(mul(x0,Fpoly),H,-2)
 check(add(centeredQ,mul(Fpoly,centeredP),-1)==squares,'turn5_centered_prior_identity')
 specializedP={k:v for k,v in centeredP.items() if k[0]==0};specializedQ={k:v for k,v in centeredQ.items() if k[0]==0}
 check(specializedP=={k:-v for k,v in Fpoly.items()} and specializedQ=={k:-2*v for k,v in H.items()},'turn5_exact_prior_specialization')
 for poly,degree in [(Fpoly,2),(H,4),(P,2),(Q,4)]:
  check(all(max(k)<=1 for k in poly),'turn5_multi_affinity')
  check(max(k[0]+2*sum(k[1:]) for k in poly)==degree,'turn5_total_degrees')
# Distinct exact sign witnesses, with rational sizes unrelated to the author's grid.
for m in range(2,10):
 seen=set()
 for signs in product((-1,1),repeat=m):
  xy=[(s*F(2*i+3,2*i+5),s*F(2*i+5,2*i+3)) for i,s in enumerate(signs)]
  check(all(x*y==1 for x,y in xy),'turn5_sign_witness_on_variety')
  actual=tuple(1 if x>0 else -1 for x,y in xy)
  check(actual==signs,'turn5_sign_witness_distinction');seen.add(actual)
 check(len(seen)==2**m,'turn5_sign_class_coverage')
print(json.dumps({'status':'PASS','arithmetic':'exact integer/rational; SymPy '+sp.__version__,'assertions':sum(counts.values()),'by_scope':dict(counts),'linear_systems':systems,'regular_models':regular_models,'regular_attachments':attachments,'singular_short_vectors':short_vectors,'limits':'Independent finite algebraic controls only. General topology and all-dimension claims are verified in the accompanying proof audit, not inferred from these tests.'},indent=2,sort_keys=True))
