from fractions import Fraction as Q
from random import Random
import json
r=Random(3000058);checks=0
def ck(x):
 global checks;checks+=1;assert x

def rank(A):
 a=[[Q(x) for x in row] for row in A];k=0
 for j in range(len(a[0])):
  z=next((z for z in range(k,len(a)) if a[z][j]),None)
  if z is None:continue
  a[k],a[z]=a[z],a[k];v=a[k][j];a[k]=[x/v for x in a[k]]
  for z in range(len(a)):
   if z!=k:
    v=a[z][j];a[z]=[x-v*y for x,y in zip(a[z],a[k])]
  k+=1
 return k

def family(V):
 out={frozenset(V)}
 if len(V)>1:
  a=list(V);r.shuffle(a);k=r.randrange(1,len(a));out|=family(a[:k])|family(a[k:])
 return out

def solve(n,L,K):
 V=frozenset(range(n));Z={S for S in L if K[S]==0}|{V};atoms=[]
 for S in Z:
  ch=[T for T in Z if T<S and not any(T<U<S for U in Z)]
  R=S-frozenset().union(*ch)
  if R:atoms.append(R)
 ck(frozenset().union(*atoms)==V);ck(sum(map(len,atoms))==n)
 v=[0]*n
 for R in atoms:
  F={S&R for S in L if S&R}|{R}|{frozenset([i]) for i in R}
  def pair(S):
   if len(S)==1:return next(iter(S))
   ch=[T for T in F if T<S and not any(T<U<S for U in F)]
   ck(frozenset().union(*ch)==S)
   rem=[x for T in sorted(ch,key=lambda x:sorted(x)) if (x:=pair(T)) is not None]
   for k in range(0,len(rem)-1,2):v[rem[k]]=1;v[rem[k+1]]=-1
   return rem[-1] if len(rem)%2 else None
  pair(R);ck(sum(v[i] for i in R)==0);ck(sum(v[i]==0 for i in R)==len(R)%2)
 for sign in [-1,1]:
  ck(sum(v)==0)
  for S in L:ck(sign*sum(v[i] for i in S)<=K[S])
  A=[[int(i==j) for j in range(n)] for i in range(n) if v[i]]
  A += [[int(i in S) for i in range(n)] for S in Z]
  ck(rank(A)==n)
 return v
cases=0
for n in range(1,31):
 for _ in range(30):
  V=frozenset(range(n));L=family(V);L={S for S in L if r.randrange(4)!=0}|{V};K={S:r.randrange(4) for S in L};K[V]=0
  for S in L:
   for T in L:ck(not(S&T) or S<=T or T<=S)
  solve(n,L,K);cases+=1
print(json.dumps({'assertions':checks,'families':cases,'max_ground_size':30,'scope':'Feasibility and exact active-rank checks; general theorem is in TURN_3.md.'},indent=2))
