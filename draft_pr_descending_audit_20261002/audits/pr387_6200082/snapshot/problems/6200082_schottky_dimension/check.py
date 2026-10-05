from fractions import Fraction as F
from itertools import combinations
import json
count=0
def ck(x):
 global count
 count+=1;assert x
for q in range(1,101):
 for a in range(0,3*q+1):
  delta=F(a,q)
  if delta<F(3,2):continue
  for c in [F(1,100),F(1,4),F(1,2),F(1)]:
   ck((delta*(3-delta)>=c)==((2*delta-3)**2<=9-4*c))
   if delta*(3-delta)>=c:ck(delta<3)
tri=list(combinations(range(5),3));edges=list(combinations(range(5),2))
def rank(M):
 M=[[F(x) for x in r] for r in M];r=0
 if not M:return 0
 for j in range(len(M[0])):
  pivot=next((i for i in range(r,len(M)) if M[i][j]),None)
  if pivot is None:continue
  M[r],M[pivot]=M[pivot],M[r];z=M[r][j];M[r]=[x/z for x in M[r]]
  for i in range(r+1,len(M)):
   z=M[i][j]
   if z:M[i]=[x-z*y for x,y in zip(M[i],M[r])]
  r+=1
  if r==len(M):break
 return r
def complex_of(mask):
 T={tri[j] for j in range(10) if mask>>j&1};E=set(e for t in T for e in combinations(t,2));return T,E
def b2(T,E):
 cols=[]
 for t in sorted(T):cols.append({tuple(t[:j]+t[j+1:]):(-1)**j for j in range(3)})
 return len(T)-rank([[col.get(e,0) for col in cols] for e in sorted(E)])
for seed in range(1024):
 A,EA=complex_of(seed);B,EB=complex_of((seed*713+157)%1024)
 ck(b2(A,EA)<=b2(A|B,EA|EB)+b2(A&B,EA&EB))
ck(F(1,1)<F(2,1) and F(4,1)>=2*F(2,1) and F(5,1)>F(4,1))
ck(F(1,4)+F(1,4)<=F(1,2))
print(json.dumps({'assertions':count,'scope':'Exact spectral quadratic equivalence and rational Mayer-Vietoris inequality controls; no numerical Cheeger constant or analytic theorem certified by finite tests'},indent=2,sort_keys=True))
