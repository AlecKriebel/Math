#!/usr/bin/env python3
"""Exact basis-conjugation controls over Q and Q(i); no density claims."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from hashlib import sha256
import json
class G:
 def __init__(self,a=0,b=0):
  if isinstance(a,G):self.a,self.b=a.a,a.b
  else:self.a,self.b=F(a),F(b)
 def __add__(self,z):z=G(z);return G(self.a+z.a,self.b+z.b)
 __radd__=__add__
 def __neg__(self):return G(-self.a,-self.b)
 def __sub__(self,z):return self+-G(z)
 def __rsub__(self,z):return G(z)+-self
 def __mul__(self,z):z=G(z);return G(self.a*z.a-self.b*z.b,self.a*z.b+self.b*z.a)
 __rmul__=__mul__
 def __truediv__(self,z):
  z=G(z);d=z.a*z.a+z.b*z.b;return self*G(z.a/d,-z.b/d)
 def __rtruediv__(self,z):return G(z)/self
 def __eq__(self,z):z=G(z);return self.a==z.a and self.b==z.b
 def __bool__(self):return bool(self.a or self.b)
counts={}
def ck(v,key):assert v,key;counts[key]=counts.get(key,0)+1

def I(d,K):return [[K(i==j) for j in range(d)] for i in range(d)]
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def mv(a,v):return tuple(sum(x*y for x,y in zip(row,v)) for row in a)
def inv(a,K):
 n=len(a);b=[row.copy()+i for row,i in zip(a,I(n,K))]
 for j in range(n):
  p=next(p for p in range(j,n) if b[p][j]);b[j],b[p]=b[p],b[j]
  q=b[j][j];b[j]=[x/q for x in b[j]]
  for p in range(n):
   if p==j:continue
   q=b[p][j];b[p]=[x-q*y for x,y in zip(b[p],b[j])]
 return [row[n:] for row in b]
def add(a,b):return [[x+y for x,y in zip(row,col)] for row,col in zip(a,b)]
def scale(a,c):return [[x*c for x in row] for row in a]
def power(a,n,K):
 r=I(len(a),K)
 for _ in range(n):r=mm(r,a)
 return r
cases=0;complex_cases=0
for K,ds in [(F,range(2,6)),(G,range(2,4))]:
 for d in ds:
  for a,b in product(range(-2,3),repeat=2):
   U=I(d,K);L=I(d,K)
   for i in range(d-1):
    U[i][i+1]=G(a,1) if K is G else F(a,2)
    L[i+1][i]=G(b,-1) if K is G else F(b,3)
   P=mm(U,L);Pi=inv(P,K);ck(mm(P,Pi)==I(d,K),'basis inverse')
   W=I(d,K);W[0],W[1]=W[1],W[0]
   S=mm(mm(P,W),Pi)
   u=tuple(row[0] for row in P);v=tuple(row[1] for row in P)
   f,g=Pi[0],Pi[1]
   N=[[(u[i]-v[i])*(g[j]-f[j]) for j in range(d)] for i in range(d)]
   ck(S==add(I(d,K),N),'independent conjugation equals rank-one map')
   ck(mm(S,S)==I(d,K),'involution')
   ck(mm(N,N)==scale(N,-2),'rank-one square')
   ck(mv(S,u)==v and mv(S,v)==u,'swap')
   for j in range(2,d):
    z=tuple(row[j] for row in P)
    ck(mv(S,z)==z,'complement fixed')
   T=[[K((i+1)*(j+2)%5-2) for j in range(d)] for i in range(d)]
   R=mm(mm(S,T),S)
   for n in range(9):
    ck(power(R,n,K)==mm(mm(S,power(T,n,K)),S),'similarity powers')
    ck(mv(power(R,n,K),v)==mv(S,mv(power(T,n,K),u)),'common vector iterate')
   cases+=1;complex_cases+=(K is G)
 for lam in ([F(-3),F(1,3),F(-2,5)] if K is F else [G(0,1),G(1,1),G(F(1,2),-2)]):
  S=scale(I(3,K),lam);Si=scale(I(3,K),1/lam)
  ck(mm(S,Si)==I(3,K),'nonzero scalar inverse')
  u=(K(1),K(2),K(-1));v=tuple(lam*z for z in u)
  ck(mv(S,u)==v,'scalar transport')
# A genuinely multi-coordinate equality, with one common target and common time.
K=G;d=3;x=(G(1),G(0),G(1,1));T=[[G((i+j)%3,i-j) for j in range(d)] for i in range(d)]
Ss=[];Rs=[];us=[]
for i in range(1,5):
 S=I(d,K);S[0][1]=G(i,1);S[1][2]=G(0,i);Si=inv(S,K)
 Ss.append(S);Rs.append(mm(mm(S,T),Si));us.append(mv(Si,x))
for n in range(13):
 ck(tuple(mv(power(R,n,K),x) for R in Rs)==tuple(mv(S,mv(power(T,n,K),u)) for S,u in zip(Ss,us)),'simultaneous complex product orbit')
p=Path(__file__).resolve().parent
print(json.dumps({'problem_id':30000567,'assertions':sum(counts.values()),'sections':counts,'independent_pairs':cases,'gaussian_rational_pairs':complex_cases,'artifact_sha256':sha256((p/'author_replay/KNOWN_RESULT.md').read_bytes()).hexdigest(),'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Finite exact transporter, inverse, and similarity controls over Q and Q(i). Infinite-dimensional mixing and density are proved or credited in the mathematical review, not certified by these finite matrices.'},indent=2,sort_keys=True))
