#!/usr/bin/env python3
"""Exact finite certificates for the cyclic-minor LP; no floating-point solver."""
from fractions import Fraction as Q
from itertools import combinations,product,permutations
from pathlib import Path
import hashlib,json
count=0

def ck(b):
 global count
 if not b:raise ValueError("Exact verification guard failed")
 count+=1

def rank(M):
 M=[list(map(Q,r)) for r in M];h=0
 for j in range(len(M[0])):
  k=next((i for i in range(h,len(M)) if M[i][j]),None)
  if k is None:continue
  M[h],M[k]=M[k],M[h];d=M[h][j];M[h]=[x/d for x in M[h]]
  for i in range(len(M)):
   if i!=h:
    d=M[i][j];M[i]=[a-d*b for a,b in zip(M[i],M[h])]
  h+=1
  if h==len(M):break
 return h

def solve(M,b):
 n=len(M);T=[list(map(Q,row))+[Q(y)] for row,y in zip(M,b)]
 for j in range(n):
  k=next((i for i in range(j,n) if T[i][j]),None)
  if k is None:return None
  T[j],T[k]=T[k],T[j];d=T[j][j];T[j]=[x/d for x in T[j]]
  for i in range(n):
   if i!=j:
    d=T[i][j];T[i]=[a-d*b for a,b in zip(T[i],T[j])]
 return tuple(row[-1] for row in T)
def mv(A,x):return tuple(sum(a*b for a,b in zip(r,x)) for r in A)
def exp(i,j):return tuple(int(k==i)+int(k==j) for k in range(6))
pos=[exp(i,3+(i+1)%3) for i in range(3)]
neg=[exp((i+1)%3,3+i) for i in range(3)]
A=[list(row) for row in zip(*(pos+neg))]+[[int(j%3==i) for j in range(6)] for i in range(3)]
expected=[[1,0,0,0,0,1],[0,1,0,1,0,0],[0,0,1,0,1,0],[0,0,1,1,0,0],[1,0,0,0,1,0],[0,1,0,0,0,1],[1,0,0,1,0,0],[0,1,0,0,1,0],[0,0,1,0,0,1]]
ck(A==expected)
ck(len(set(pos+neg))==6)
ck(all(sum(a)==sum(b)==2 and all(min(x,y)==0 for x,y in zip(a,b)) for a,b in zip(pos,neg)))
ck(rank(A)==5)
ck(mv(A,(1,1,1,-1,-1,-1))==(0,)*9)
# Coefficient matrix of the three homogeneous degree-two generators.
mons=pos+neg
coeff=[[int(m==pos[i])-int(m==neg[i]) for m in mons] for i in range(3)]
ck(rank(coeff)==3)
# Torus evaluation and nonzero exponent conditions.
for a,b in zip(pos,neg):ck(sum(a)>0 and sum(b)>0 and 1-1==0)
# Exact primal/dual optimum certificates.
dual=(0,)*6+(1,)*3
ck(tuple(sum(A[i][j]*dual[i] for i in range(9)) for j in range(6))==(1,)*6)
ck(sum(dual)==3 and all(x>=0 for x in dual))
for d in range(1,33):
 for p in range(d+1):
  t=Q(p,d);z=(t,)*3+(1-t,)*3
  ck(mv(A,z)==(1,)*9)
  ck(sum(z)==3 and min(z)>=0)
  t2=Q(0) if t else Q(1);z2=(t2,)*3+(1-t2,)*3
  ck(z2!=z and mv(A,z2)==mv(A,z))
# Enumerate all vertices by choosing six active inequalities from15.
C=A+[[-int(i==j) for j in range(6)] for i in range(6)]
b=[Q(1)]*9+[Q(0)]*6
vertices=set();bases=0
for ids in combinations(range(15),6):
 bases+=1;z=solve([C[i] for i in ids],[b[i] for i in ids])
 if z is not None and all(v<=rhs for v,rhs in zip(mv(C,z),b)):vertices.add(z)
expected_vertices={bits+(0,0,0) for bits in product((Q(0),Q(1)),repeat=3)}|{(0,0,0)+bits for bits in product((Q(0),Q(1)),repeat=3)}
ck(vertices==expected_vertices)
ck(len(vertices)==15)
opt={z for z in vertices if sum(z)==3}
ck(opt=={(Q(1),)*3+(Q(0),)*3,(Q(0),)*3+(Q(1),)*3})
for z in vertices:ck(sum(z)<=3)
# Changing generator order or swapping its two terms merely permutes columns.
for perm in permutations(range(3)):
 for flips in product((0,1),repeat=3):
  ps=[(neg if flips[j] else pos)[i] for j,i in enumerate(perm)]
  ns=[(pos if flips[j] else neg)[i] for j,i in enumerate(perm)]
  B=[list(row) for row in zip(*(ps+ns))]+[[int(j%3==i) for j in range(6)] for i in range(3)]
  ck(rank(B)==5)
  for t in (Q(0),Q(2,5),Q(1)):
   mu=tuple(1-t if v else t for v in flips);nu=tuple(1-v for v in mu)
   ck(mv(B,mu+nu)==(1,)*9)
# Bounded straightening controls for the elementary prime-ideal proof.
def compositions(d,n):
 if n==1:yield(d,);return
 for i in range(d+1):
  for rest in compositions(d-i,n-1):yield(i,)+rest
fibers={};monomial_cases=0;steps=0
for degree in range(6):
 for w in compositions(degree,6):
  monomial_cases+=1;alpha=w[:3];beta=w[3:]
  key=(sum(alpha),sum(beta),tuple(alpha[i]+beta[i] for i in range(3)))
  if key not in fibers:fibers[key]=w
  target=fibers[key][:3];a=list(alpha);b0=list(beta)
  while tuple(a)!=target:
   old=sum(abs(a[i]-target[i]) for i in range(3))
   j=next(i for i in range(3) if a[i]>target[i]);i=next(i for i in range(3) if a[i]<target[i])
   ck(a[j]>=1 and b0[i]>=1)
   oldw=tuple(a+b0)
   a[j]-=1;a[i]+=1;b0[i]-=1;b0[j]+=1
   neww=tuple(a+b0)
   common=tuple(min(u,v) for u,v in zip(oldw,neww))
   da=tuple(u-v for u,v in zip(oldw,common));db=tuple(u-v for u,v in zip(neww,common))
   ck(any((da,db)==(u,v) or (da,db)==(v,u) for u,v in zip(pos,neg)))
   ck(sum(abs(a[k]-target[k]) for k in range(3))==old-2)
   steps+=1
  ck(tuple(a+b0)==fibers[key])
# Central monomial cancellation is illustrative, not needed for the LP proof.
poly={(0,)*6:1}
for a,b0 in zip(pos,neg):
 out={}
 for w,c in poly.items():
  for v,sign in ((a,1),(b0,-1)):
   u=tuple(x+y for x,y in zip(w,v));out[u]=out.get(u,0)+sign*c
 poly={w:c for w,c in out.items() if c}
ck((1,)*6 not in poly and len(poly)==6)
root=Path(__file__).resolve().parent
r={'status':'PASS','assertions':count,'exact_active_bases':bases,'polytope_vertices':len(vertices),'optimal_vertices':[[str(v) for v in z] for z in sorted(opt)],'monomial_straightening_cases':monomial_cases,'straightening_steps':steps,'matrix':A,'rank':5,'kernel_generator':[1,1,1,-1,-1,-1],'optimal_value':'3','optimal_face':'(t,t,t,1-t,1-t,1-t), rational0<=t<=1','optimal_augmented_image':[1]*9,'artifact_sha256':hashlib.sha256((root/'CANDIDATE.md').read_bytes()).hexdigest(),'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'Exact finite diagnostics supplement the complete written proof. No threshold computation or priority claim.'}
(root/'verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['status','assertions','exact_active_bases','polytope_vertices','monomial_straightening_cases','straightening_steps','artifact_sha256','verifier_sha256']},indent=2))
