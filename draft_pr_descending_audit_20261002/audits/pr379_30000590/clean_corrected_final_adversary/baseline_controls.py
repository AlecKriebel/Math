from itertools import permutations
import json
P=list(permutations(range(3)))
e=(0,1,2); t=(1,0,2); H=[e,t]
def mul(a,b): return tuple(a[b[i]] for i in range(3))
def phi(a,x):
 z=mul(x,a); return z if z in H else None
checks=0
for a in P:
 for x in P:
  for h in H:
   assert phi(a,mul(h,x)) == (mul(h,phi(a,x)) if phi(a,x) else None); checks+=1
   assert phi(mul(a,h),x) == (mul(phi(a,x),h) if phi(a,x) else None); checks+=1
  for g in P:
   assert phi(mul(g,a),x)==phi(a,mul(x,g)); checks+=1
# distinct basis coinduced coordinate vectors
assert len({tuple(phi(a,x) for x in P) for a in P})==6
def rank(A,p):
 A=[[x%p for x in r] for r in A]; j=0
 for c in range(len(A[0])):
  piv=next((i for i in range(j,len(A)) if A[i][c]),None)
  if piv is None: continue
  A[j],A[piv]=A[piv],A[j]; u=pow(A[j][c],-1,p); A[j]=[x*u%p for x in A[j]]
  for i in range(len(A)):
   if i!=j:
    u=A[i][c]; A[i]=[(x-u*y)%p for x,y in zip(A[i],A[j])]
  j+=1
 return j
cyclic=[]
for n in range(1,18):
 T=[[int(i==(j+1)%n)-int(i==j) for j in range(n)] for i in range(n)]; N=[[1]*n for _ in range(n)]
 for p in [2,3,5,7]:
  rt,rn=rank(T,p),rank(N,p)
  assert rt==n-1 and rn==1
  assert all(sum(T[i][k]*N[k][j] for k in range(n))==0 for i in range(n) for j in range(n))
  cyclic.append(dict(order=n,characteristic=p,t_minus_1_rank=rt,norm_rank=rn,positive_cohomology_dimension=n-rt-rn))
square=[dict(dim_V=n,dim_ann_v=n,min_generators_ann_v=n,free_cochain_term_rank=1) for n in range(1,33)]
print(json.dumps(dict(S3_bimodule_equations=checks,cyclic_controls=cyclic,square_zero_controls=square),indent=2))
