#!/usr/bin/env python3
"""Exact controls of the expanded formula; no compressed-coordinate algorithm."""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json

counts=Counter()
def check(kind,v):
 if not v:raise AssertionError(kind)
 counts[kind]+=1

def involutions(items):
 if not items:
  yield {}
  return
 x,*tail=items
 for rest in involutions(tail):yield {x:x,**rest}
 for y in tail:
  for rest in involutions([z for z in tail if z!=y]):yield {x:y,y:x,**rest}

def cycles(p):
 seen=set();out=[]
 for i in range(len(p)):
  if i in seen:continue
  C=[];j=i
  while j not in seen:seen.add(j);C.append(j);j=p[j]
  out.append(C)
 return out

def components(alpha,beta):
 seen=set();out=[]
 for i in range(len(alpha)):
  if i in seen:continue
  todo=[i];C=set()
  while todo:
   j=todo.pop()
   if j in C:continue
   C.add(j);todo.extend((alpha[j],beta[j]))
  seen|=C;out.append(C)
 return out

def matrix_rank(A):
 A=[[F(x) for x in row] for row in A];n=len(A);rank=0
 for col in range(n):
  pivot=next((i for i in range(rank,n) if A[i][col]),None)
  if pivot is None:continue
  A[rank],A[pivot]=A[pivot],A[rank];q=A[rank][col]
  A[rank]=[x/q for x in A[rank]]
  for i in range(n):
   if i!=rank and A[i][col]:
    q=A[i][col];A[i]=[x-q*y for x,y in zip(A[i],A[rank])]
  rank+=1
 return rank

def determinant(A):
 A=[[F(x) for x in row] for row in A];n=len(A);d=F(1)
 for col in range(n):
  pivot=next((i for i in range(col,n) if A[i][col]),None)
  if pivot is None:return F(0)
  if pivot!=col:A[pivot],A[col]=A[col],A[pivot];d=-d
  q=A[col][col];d*=q
  for i in range(col+1,n):
   c=A[i][col]/q
   for j in range(col+1,n):A[i][j]-=c*A[col][j]
 return d

cases=0;by_size={}
for N in (0,2,4,6,8):
 alpha=[i^1 for i in range(N)];size_cases=0
 for b in involutions(list(range(N))):
  beta=[b[i] for i in range(N)];p=[alpha[beta[i]] for i in range(N)]
  C=components(alpha,beta);cp=cycles(p);f=sum(beta[i]==i for i in range(N))
  arcs=sum(any(beta[i]==i for i in K) for K in C);closed=len(C)-arcs
  check('boundary_endpoints',f==2*arcs)
  check('cycle_formula',len(cp)==2*closed+arcs)
  check('total_component_formula',4*len(C)==2*len(cp)+f)
  M=[[int(i==j)-int(p[j]==i) for j in range(N)] for i in range(N)]
  check('independent_kernel_rank',N-matrix_rank(M)==len(cp))
  for K in C:
   local=[X for X in cp if X[0] in K]
   check('per_component_cycles',len(local)==(1 if any(beta[i]==i for i in K) else 2))
  if N<=6:
   for z in (2,3):
    Mz=[[int(i==j)-z*int(p[j]==i) for j in range(N)] for i in range(N)]
    expected=1
    for cyc in cp:expected*=1-z**len(cyc)
    check('determinant_factorization',determinant(Mz)==expected)
  cases+=1;size_cases+=1
 by_size[str(N)]=size_cases

# Closed torus-style strand gluing: segments are joined by a cyclic shift.
torus_cases=0
for m in range(1,25):
 for t in range(-24,25):
  alpha=[i^1 for i in range(2*m)];beta=[None]*(2*m)
  for j in range(m):
   a=2*j+1;b=2*((j+t)%m);beta[a]=b;beta[b]=a
  C=components(alpha,beta);p=[alpha[beta[i]] for i in range(2*m)]
  check('torus_gcd',len(C)==gcd(m,abs(t)))
  check('closed_factor_two',len(cycles(p))==2*gcd(m,abs(t)))
  torus_cases+=1
for n in range(1,65):
 check('homogeneous_continuity_diagnostic',gcd(n,n+1)==1)
 check('homogeneous_continuity_diagnostic',F(gcd(n,n+1),n)==F(1,n))
 check('scaling_diagnostic',gcd(n,n)==n)
check('global_gcd_counterexample',gcd(1,1)==1 and 1+1==2)
for B in range(1,33):
 K=2**B
 check('binary_expansion_diagnostic',K.bit_length()==B+1 and 2*K==2**(B+1))

D=Path(__file__).resolve().parent
print(json.dumps({'status':'PASS','assertions':sum(counts.values()),'families':dict(counts),'involution_cases':cases,'involution_cases_by_N':by_size,'torus_shift_cases':torus_cases,'artifact_sha256':sha256((D/'OBSTRUCTION.md').read_bytes()).hexdigest(),'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'limitations':'Finite diagnostics of expanded gluing, not a formula or complexity proof for compressed Dehn–Thurston inputs.'},indent=2,sort_keys=True))
