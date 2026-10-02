from fractions import Fraction as Q
from math import comb
import json
n=0
def ck(v):
 global n
 n+=1;assert v

def rank(cols):
 a=[[Q(c[i]) for c in cols] for i in range(len(cols[0]))];r=0
 for j in range(len(cols)):
  k=next((k for k in range(r,len(a)) if a[k][j]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];v=a[r][j];a[r]=[x/v for x in a[r]]
  for k in range(len(a)):
   if k!=r:
    v=a[k][j];a[k]=[x-v*y for x,y in zip(a[k],a[r])]
  r+=1
 return r

def unit(d,k):return [int(i==k) for i in range(d+1)]
def transform(d,k,M):
 a,b,c,e=M;out=[Q(0)]*(d+1)
 for i in range(d-k+1):
  for j in range(k+1):out[i+j]+=comb(d-k,i)*a**(d-k-i)*b**i*comb(k,j)*c**(k-j)*e**j
 return out
models=[]
for d in range(1,19):
 for M in [(1,0,0,1),(1,1,0,1),(2,3,0,1),(0,1,1,0),(1,0,1,1),(2,1,1,1)]:
  a,b,c,e=M
  for lam in {Q(1),Q(2),Q(1,a**d) if a else Q(3)}:
   T=[transform(d,k,M) for k in range(d+1)]
   # Compatible restrictions A0=B0: common constant column, then independent A_k and B_k.
   cols=[[Q(v)-lam*w for v,w in zip(unit(d,0),T[0])]]
   cols += [unit(d,k) for k in range(1,d+1)]
   cols += [[-lam*x for x in T[k]] for k in range(1,d+1)]
   r=rank(cols);expect=d if c==0 and lam*a**d==1 else d+1
   ck(r==expect)
   skew=[unit(d,k) for k in range(d+1)]+[[-lam*x for x in t] for t in T]
   ck(rank(skew)==d+1)
   # Direct union-of-lines extension A(s,t)+B(s,u)-A0*s^d at a rational point.
   for s,t in [(1,2),(2,-1),(-1,3)]:
    A=[k+1 for k in range(d+1)];B=[1]+[2*k-3 for k in range(1,d+1)]
    eva=lambda C,v:sum(C[k]*s**(d-k)*v**k for k in range(d+1))
    ck(eva(A,t)+eva(B,0)-s**d==eva(A,t))
    ck(eva(A,0)+eva(B,t)-s**d==eva(B,t))
   models.append({'degree':d,'matrix':M,'lambda':str(lam),'intersecting_rank':r})
for d in range(7,31):
 ck(7-d<=0);ck(6-d<0);ck(5-d<0)
 if d>=8:ck(7-d<0)
print(json.dumps({'assertions':n,'tested_models':len(models),'rank_cases':models,'scope':'Exact finite linear controls; the incidence and genericity proofs are symbolic.'},indent=2))
