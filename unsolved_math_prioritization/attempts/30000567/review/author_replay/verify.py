#!/usr/bin/env python3
"""Finite exact algebra controls only; finite-dimensional maps are not hypercyclic witnesses."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from hashlib import sha256
import json
C={}
def ck(v,k):
 assert v,k
 C[k]=C.get(k,0)+1

def eye(d):return [[F(i==j) for j in range(d)] for i in range(d)]
def mv(A,v):return tuple(sum((a*x for a,x in zip(row,v)),F(0)) for row in A)
def mm(A,B):return [[sum((a*b for a,b in zip(row,col)),F(0)) for col in zip(*B)] for row in A]
def pw(A,n):
 B=eye(len(A))
 for _ in range(n):B=mm(A,B)
 return B

def transporter(u,v):
 d=len(u);I=eye(d)
 pair=next(((i,j) for i in range(d) for j in range(i+1,d) if u[i]*v[j]-u[j]*v[i]),None)
 if pair is None:
  i=next(i for i,x in enumerate(u) if x);lam=v[i]/u[i]
  assert lam and all(v[j]==lam*u[j] for j in range(d))
  return [[lam*z for z in row] for row in I],[[z/lam for z in row] for row in I],None
 i,j=pair;det=u[i]*v[j]-u[j]*v[i]
 f=[F(0)]*d;g=[F(0)]*d
 f[i]=v[j]/det;f[j]=-v[i]/det;g[i]=-u[j]/det;g[j]=u[i]/det
 ck(sum(f[k]*u[k] for k in range(d))==1,'dual_coordinates')
 ck(sum(f[k]*v[k] for k in range(d))==0,'dual_coordinates')
 ck(sum(g[k]*u[k] for k in range(d))==0,'dual_coordinates')
 ck(sum(g[k]*v[k] for k in range(d))==1,'dual_coordinates')
 N=[[(u[i]-v[i])*(g[j]-f[j]) for j in range(d)] for i in range(d)]
 S=[[I[i][j]+N[i][j] for j in range(d)] for i in range(d)]
 ck(mm(N,N)==[[-2*x for x in row] for row in N],'rank_one_formula')
 return S,S,N

pairs=0;independent=0;collinear=0
for d in (2,3):
 vectors=[tuple(map(F,v)) for v in product((-1,0,1),repeat=d) if any(v)]
 Ts=[[[F((i+1) if i==j else 0) for j in range(d)] for i in range(d)],
     [[F(j==(i+1)%d) for j in range(d)] for i in range(d)],
     [[F(i==j)+F(j==i+1) for j in range(d)] for i in range(d)]]
 for u,v in product(vectors,repeat=2):
  S,Sinv,N=transporter(u,v);pairs+=1;independent+=N is not None;collinear+=N is None
  ck(mv(S,u)==v,'transport')
  ck(mm(S,Sinv)==eye(d)==mm(Sinv,S),'inverse')
  if N is not None:ck(mv(S,v)==u,'involution_swap')
  for T in Ts:
   R=mm(mm(S,T),Sinv)
   for n in range(6):
    ck(pw(R,n)==mm(mm(S,pw(T,n)),Sinv),'similarity_powers')
    ck(mv(pw(R,n),v)==mv(S,mv(pw(T,n),u)),'common_vector_orbit')

# Scalar transports include negative and nonintegral multipliers.
for lam in [F(-3),F(-1,2),F(1,3),F(2)]:
 u=(F(1),F(2),F(-1));v=tuple(lam*x for x in u)
 S,Si,N=transporter(u,v)
 ck(N is None,'scalar_case')
 ck(mv(S,u)==v and mm(S,Si)==eye(3),'scalar_case')

# Product-map algebra with a common final vector, independently assembled by blocks.
x=(F(1),F(0),F(0));us=[(F(0),F(1),F(0)),(F(0),F(0),F(1)),(F(1),F(1),F(1))]
T=[[F(0),F(1),F(0)],[F(0),F(0),F(1)],[F(1),F(2),F(3)]]
Ss=[transporter(u,x)[:2] for u in us]
Rs=[mm(mm(S,T),Si) for S,Si in Ss]
for n in range(9):
 lhs=tuple(mv(pw(R,n),x) for R in Rs)
 rhs=tuple(mv(S,mv(pw(T,n),u)) for (S,Si),u in zip(Ss,us))
 ck(lhs==rhs,'simultaneous_product_orbit')

root=Path(__file__).resolve().parent
r={'status':'PASS','assertions':sum(C.values()),'categories':C,'transport_pairs':pairs,'independent_pairs':independent,'collinear_pairs':collinear,'artifact_sha256':sha256((root/'KNOWN_RESULT.md').read_bytes()).hexdigest(),'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Finite exact transporter and similarity algebra only. Infinite-dimensional existence/density is supplied by the credited theorem and topological proof; these matrices are not hypercyclic examples.'}
(root/'verification.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r,indent=2,sort_keys=True))
