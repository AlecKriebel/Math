#!/usr/bin/env python3
"""Exact finite controls for the independent covering-space audit; no surface construction."""
from itertools import permutations,product
from functools import lru_cache
from fractions import Fraction as Q
from math import factorial,gcd
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json
C=Counter();root=Path(__file__).resolve().parent
def check(k,v):
 assert v,k;C[k]+=1
def mul(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):return tuple(p.index(i) for i in range(len(p)))
def pw(p,n):
 a=tuple(range(len(p)))
 for _ in range(n):a=mul(p,a)
 return a
def conjug(p,s):return mul(mul(s,p),inv(s))
def trans(a,b):
 seen={0};todo=[0]
 while todo:
  x=todo.pop()
  for y in (a[x],b[x]):
   if y not in seen:seen.add(y);todo.append(y)
 return len(seen)==len(a)
class_counts={};transitive_counts={};cover_returns=0
for D in range(1,5):
 ps=tuple(permutations(range(D)))
 @lru_cache(None)
 def canonical(a,b):return min((conjug(a,s),conjug(b,s)) for s in ps)
 reps=sorted({canonical(a,b) for a,b in product(ps,repeat=2) if trans(a,b)})
 transitive_counts[D]=sum(trans(a,b) for a,b in product(ps,repeat=2));class_counts[D]=len(reps)
 check('cover_count_bound',len(reps)<=factorial(D)**3)
 for N in range(1,9):
  for horizontal in (True,False):
   def step(v):
    a,b=v
    return canonical(a,mul(b,pw(a,N))) if horizontal else canonical(mul(a,pw(b,N)),b)
   images=[step(v) for v in reps]
   check('congruence_twist_class_permutation',set(images)==set(reps) and len(images)==len(set(images)))
   for v in reps:
    u=step(v);n=1
    while u!=v:
     u=step(u);n+=1;assert n<=len(reps)
    cover_returns+=1
    check('unbased_return_bound',1<=n<=len(reps)<=factorial(D)**3)
    a,b=v
    raw=(a,mul(b,pw(a,N*n))) if horizontal else (mul(a,pw(b,N*n)),b)
    witness=next(s for s in ps if (conjug(raw[0],s),conjug(raw[1],s))==v)
    check('explicit_lift_relabelling',conjug(raw[0],witness)==a and conjug(raw[1],witness)==b)
    check('connected_cover_preserved',trans(*raw))
# All subgroups of S4, not merely cyclic or dihedral chosen examples.
ps=tuple(permutations(range(4)));ident=tuple(range(4))
@lru_cache(None)
def generated(gs):
 seen={ident};todo=[ident]
 while todo:
  a=todo.pop()
  for b in gs:
   c=mul(a,b)
   if c not in seen:seen.add(c);todo.append(c)
 return frozenset(seen)
subgroups={frozenset((ident,))};todo=list(subgroups)
while todo:
 H=todo.pop()
 for p in ps:
  if p in H:continue
  K=generated(tuple(sorted(H|{p})))
  if K not in subgroups:subgroups.add(K);todo.append(K)
check('S4_subgroup_count',len(subgroups)==30)
valid=0;failed_hypothesis=0
for H in subgroups:
 for phi in H:
  cyc=generated((phi,))
  for z in range(4):
   O={z};x=phi[z];k=1
   while x!=z:O.add(x);x=phi[x];k+=1
   stab={g for g in H if g[z]==z}
   expected=generated((pw(phi,k),))
   setwise={g for g in H if {g[x] for x in O}==O}
   if stab==expected:
    valid+=1;check('conditional_stabilizer_lemma',setwise==cyc)
    for g in setwise:
     j=next(j for j in range(k) if pw(phi,j)[z]==g[z])
     check('point_stabilizer_factorization',mul(inv(pw(phi,j)),g) in expected)
   elif setwise!=cyc:failed_hypothesis+=1
check('finite_orbit_alone_insufficient',failed_hypothesis>0)
# Rational periodic points with hyperbolic matrices of both trace signs.
def mm(A,B):return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def mv(A,x):return tuple(sum(A[i][j]*x[j] for j in range(2)) for i in range(2))
def det(A):return A[0][0]*A[1][1]-A[0][1]*A[1][0]
I=((1,0),(0,1));mats=[]
for s,t,sign in product(range(1,7),range(1,7),(-1,1)):
 A=((sign*(1+s*t),sign*s),(sign*t,sign));mats.append(A);Ak=I
 for k in range(1,7):
  Ak=mm(Ak,A);B=tuple(tuple(Ak[i][j]-I[i][j] for j in range(2)) for i in range(2));d=det(B)
  check('negative_and_positive_hyperbolic_trace',abs(A[0][0]+A[1][1])>2 and det(A)==1 and d!=0)
  for z in ((2,-1),(-3,4),(5,7)):
   x=(Q(B[1][1]*z[0]-B[0][1]*z[1],d),Q(-B[1][0]*z[0]+B[0][0]*z[1],d))
   check('periodic_lattice_equation',mv(B,x)==z)
   N=x[0].denominator*x[1].denominator//gcd(x[0].denominator,x[1].denominator)
   for m in range(1,5):
    for M in (((1,m*N),(0,1)),((1,0),(m*N,1))):
     check('congruence_fixing',all((a-b).denominator==1 for a,b in zip(mv(M,x),x)))
for N,a,b in product(range(1,15),range(1,9),range(1,9)):
 U=((1,a*N),(0,1));L=((1,0),(b*N,1));P=mm(U,L);Qm=mm(L,U)
 check('projective_noncommutation',P!=Qm and P!=tuple(tuple(-x for x in row) for row in Qm))
 check('unipotents_and_hyperbolic_product',det(U)==det(L)==1 and P[0][0]+P[1][1]>2)
check('frozen_proof_hash',sha256((root/'author_replay/PARTIAL.md').read_bytes()).hexdigest()=='896057b85ea65f53c0c380c0f0708ec895dd0a706c9f667b1fc6c9830feda8f5')
out={'verdict':'PASS','assertions':sum(C.values()),'categories':dict(C),'unbased_cover_classes_by_degree':class_counts,'transitive_labelled_covers_by_degree':transitive_counts,'explicit_cover_returns':cover_returns,'S4_subgroups':len(subgroups),'conditional_cases':valid,'missing_hypothesis_countercontrols':failed_hypothesis,'scope':'Finite exact diagnostic controls only; covering-space completion, compactness, area and general group arguments are independently proved in REVIEW.md.'}
(root/'independent_results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
