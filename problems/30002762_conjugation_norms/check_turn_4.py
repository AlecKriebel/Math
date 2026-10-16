from fractions import Fraction as F
from itertools import combinations,product
import random,json
rng=random.Random(300027624);checks=0
def ck(x):
 global checks
 checks+=1
 assert x
def rref(A):
 a=[list(map(F,row)) for row in A]
 if not a:return []
 r=0
 for j in range(len(a[0])):
  z=next((i for i in range(r,len(a)) if a[i][j]),None)
  if z is None:continue
  a[r],a[z]=a[z],a[r];v=a[r][j];a[r]=[x/v for x in a[r]]
  for i in range(len(a)):
   if i!=r:
    v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
  r+=1
  if r==len(a):break
 return a[:r]
def solve(A,b):
 n=len(b);a=rref([list(row)+[v] for row,v in zip(A,b)])
 if len(a)!=n or any(a[i][j]!=(i==j) for i in range(n) for j in range(n)):return None
 return [row[-1] for row in a]
def compute(R,v):
 d=len(v);R=rref(R);r=len(R);k=d-r;E=[[int(i==j) for j in range(d)] for i in range(d)]
 dual=[];primal=[]
 for S in combinations(range(d),k):
  for signs in product((-1,1),repeat=k):
   u=solve(R+[E[i] for i in S],[0]*r+list(signs))
   if u is not None and max(map(abs,u),default=0)<=1:
    ck(all(sum(a*b for a,b in zip(row,u))==0 for row in R));dual.append(sum(a*b for a,b in zip(u,v)))
  cols=R+[E[i] for i in S];co=solve(list(map(list,zip(*cols))),v)
  if co is not None:
   w=[sum(co[r+j]*E[S[j]][i] for j in range(k)) for i in range(d)]
   ck(all(v[i]==w[i]+sum(co[j]*R[j][i] for j in range(r)) for i in range(d)));primal.append(sum(map(abs,w)))
 ck(bool(dual) and bool(primal));ck(max(dual)==min(primal));return max(dual)
values=[]
for d in range(1,6):
 for _ in range(80):
  R=[[rng.randrange(-3,4) for i in range(d)] for j in range(rng.randrange(d+1))];v=[rng.randrange(-5,6) for i in range(d)]
  value=compute(R,v);ck(value>=0);values.append(str(value))
ck(compute([[2,-3]],[0,1])==F(2,3));ck(compute([[0,0,-1],[0,0,0]],[2,-3,19])==5)
print(json.dumps({'assertions':checks,'random_integer_presentations':400,'exact_examples':['2/3','5'],'scope':'Rational primal/dual certificate controls, not recognition of the promised group class'},indent=2,sort_keys=True))
