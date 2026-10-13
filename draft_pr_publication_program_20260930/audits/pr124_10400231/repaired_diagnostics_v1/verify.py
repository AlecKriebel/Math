from itertools import permutations,product
from pathlib import Path
import random,hashlib,json
checks=0;cases=0;rng=random.Random(1226)
def ck(x):
 global checks
 if not x:raise AssertionError("Encoded author check failed")
 checks+=1
def rank(M,p):
 a=[row[:] for row in M];r=0
 for j in range(len(a[0])):
  k=next((k for k in range(r,len(a)) if a[k][j]%p),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];v=pow(a[r][j]%p,-1,p);a[r]=[v*x%p for x in a[r]]
  for k in range(len(a)):
   if k!=r:
    v=a[k][j];a[k]=[(x-v*y)%p for x,y in zip(a[k],a[r])]
  r+=1
  if r==len(a):break
 return r
def pmul(a,b,p):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
 return c
def detpoly(A,p):
 n=len(A);d=[0]*(2*n+1)
 for perm in permutations(range(n)):
  sign=(-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n));v=[1]
  for i in range(n):v=pmul(v,A[i][perm[i]],p)
  for k,x in enumerate(v):d[k]=(d[k]+sign*x)%p
 return d
for p in (2,3,5,7):
 for n in range(1,5):
  for rep in range(300):
   A=[[[rng.randrange(p) for k in range(3)] for j in range(n)] for i in range(n)]
   if rep%3==0:
    for i in range(rep%n,n):
     for j in range(n):A[i][j][0]=0
   A0=[[A[i][j][0] for j in range(n)] for i in range(n)];r=n-rank(A0,p);d=detpoly(A,p)
   ck(all(v==0 for v in d[:r]));cases+=1
   if n>1:
    B=[[v[:] for v in row] for row in A]
    for j in range(n):B[0][j]=[(x+2*y)%p for x,y in zip(A[0][j],A[1][j])]
    ck(detpoly(B,p)==d)
for p in (2,3,5,7,11,13,17,19,23,29,31):
 coeff=[1,p**3-2,1]
 ck(sum(coeff)==p**3);ck(coeff==coeff[::-1])
 shifted=[sum(coeff),coeff[1]+2*coeff[2],coeff[2]]
 ck(shifted==[p**3,p**3,1]);ck([x%p for x in shifted]==[0,0,1])
 ck(3-rank([[p if i==j else 0 for j in range(3)] for i in range(3)],p)==3)
for vals in product((0,1),repeat=9):
 A0=[list(vals[3*i:3*i+3]) for i in range(3)]
 A=[[[A0[i][j],int(i==j),0] for j in range(3)] for i in range(3)]
 d=detpoly(A,2);r=3-rank(A0,2);ck(all(x==0 for x in d[:r]));cases+=1
r={'artifact_sha256':hashlib.sha256(Path('COUNTEREXAMPLE.md').read_bytes()).hexdigest(),'exact_assertions':checks,'finite_field_matrix_cases':cases,'candidate_primes_checked':11,'scope':'Exact determinant/rank and candidate-polynomial controls only; topological square-presentation lemma requires independent proof review.'}
Path('verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
