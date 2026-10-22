from itertools import product,combinations
from pathlib import Path
import hashlib,json
N=5;checks=0
def ck(x):
 global checks
 assert x;checks+=1
def mul(a,b):
 c={}
 for u,x in a.items():
  for v,y in b.items():
   w=u+v
   if len(w)<=N:c[w]=c.get(w,0)+x*y
 return {w:x for w,x in c.items() if x}
def expgen(i,sign=1):return {():1,(i,):1} if sign==1 else {tuple([i]*n):(-1)**n for n in range(N+1)}
def powr(a,k):
 r={():1}
 for _ in range(k):r=mul(r,a)
 return r
def word(w):
 r={():1}
 for i,sign in w:r=mul(r,expgen(i,sign))
 return r
for i in range(4):ck(mul(expgen(i),expgen(i,-1))=={():1});ck(mul(expgen(i,-1),expgen(i))=={():1})
for i,j in combinations(range(4),2):
 for m,n in product(range(-5,6),repeat=2):
  wx=[(i,1 if m>=0 else -1)]*abs(m);wy=[(j,1 if n>=0 else -1)]*abs(n)
  inv=lambda w:[(k,-s) for k,s in reversed(w)]
  r=word(wx+wy+inv(wx)+inv(wy));ck(r.get((i,j),0)==m*n);ck(r.get((j,i),0)==-m*n)
  ck(all(r.get((k,),0)==0 for k in range(4)));ck(r.get((),0)==1)
for mu in range(4,16):
 labels=range(mu)
 for pair in combinations(labels,2):ck(not set((0,1,2)).issubset(pair))
 ck(len(tuple(combinations(labels,2)))==mu*(mu-1)//2)
for a,b,k in product(range(-10,11),repeat=3):
 for c in range(-3,4):ck((b+k*a)-a*(c+k)==b-a*c)
r={'artifact_sha256':hashlib.sha256(Path('PARTIAL_RESULT.md').read_bytes()).hexdigest(),'exact_assertions':checks,'scope':'Formal Magnus series through degree5, component-label bookkeeping, and delta2 polynomial identity only; not a geometric link classification or imported theorem verification.'}
Path('verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
