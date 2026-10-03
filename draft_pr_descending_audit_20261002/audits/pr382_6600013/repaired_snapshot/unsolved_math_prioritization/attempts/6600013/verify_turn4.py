from cyclic_cover import complex,projection
from rational_linear import rank,matmul,eye
from cochain_images import transpose
import json
checks=0
def check(x):
 global checks
 assert x;checks+=1
# Free group words: a=1,b=2, inverses negative.
def reduce(w):
 s=[]
 for x in w:
  if s and s[-1]==-x:s.pop()
  else:s.append(x)
 return s
def inverse(w):return [-x for x in w[::-1]]
def apply(images,w):return reduce([y for x in w for y in (images[x] if x>0 else inverse(images[-x]))])
tau={1:[1,1,2],2:[1,2]};inv={1:[1,-2],2:[2,-1,2]}
for x in [1,2,-1,-2]:check(apply(tau,apply(inv,[x]))==[x]);check(apply(inv,apply(tau,[x]))==[x])
a=b=1
for k in range(1,20):a,b=2*a+b,a+b;check(b<=a<=2*b)
# Minimal-level block length bound for all n in a finite range.
for n in range(2,1000):
 a=b=1
 while b<n:a,b=2*a+b,a+b
 check(a<6*n)
records=[]
for q in range(1,13):
 D1,D2=complex(q);check(all(x==0 for row in matmul(D1,D2) for x in row));r1=rank(D1);r2=rank(D2);betti=[q-r1,4*q-r1-r2,4*q-r2];check(betti==[1,4,q+3]);records.append(dict(degree=q,betti=betti))
for q,Q in [(1,2),(2,4),(3,6),(4,8)]:
 a1,a2=complex(q);b1,b2=complex(Q);F0,F1,F2=projection(q,Q);d=Q//q
 check(matmul(a1,F1)==matmul(F0,b1));check(matmul(a2,F2)==matmul(F1,b2))
 # Summation on lifts is a cochain transfer as well.
 check(matmul(F1,transpose(b1))==matmul(transpose(a1),F0));check(matmul(F2,transpose(b2))==matmul(transpose(a2),F1))
 for F in [F0,F1,F2]:check(matmul(F,transpose(F))==[[d*x for x in row] for row in eye(len(F))])
print(json.dumps(dict(assertions=checks,cyclic_cover_betti=records,scope='Exact finite cover and proper-substitution controls; each constructed tiling has finite rank and covering-degree-dependent complexity.'),indent=2,sort_keys=True))
