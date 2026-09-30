from pathlib import Path
from itertools import product
from hashlib import sha256
import json
checks=0
def ck(v):
 global checks
 assert v
 checks+=1
def clean(a):return {k:v%3 for k,v in a.items() if v%3}
def add(a,b):
 c=a.copy()
 for k,v in b.items():c[k]=c.get(k,0)+v
 return clean(c)
def neg(a):return clean({k:-v for k,v in a.items()})
def scale(c,a):return clean({k:c*v for k,v in a.items()})
def mul(a,b):
 c={}
 for (i,j),u in a.items():
  for (k,l),v in b.items():c[i+k,j+l]=c.get((i+k,j+l),0)+u*v
 return clean(c)
def bar(a):return {(-i,-j):v for (i,j),v in a.items()}
z={};one={(0,0):1}
K=[[clean({(-1,0):1,(1,0):-1}),clean({(1,0):1,(1,1):1,(0,1):-1,(0,0):1})],[clean({(-1,0):-1,(0,-1):1,(-1,-1):-1,(0,0):-1}),clean({(0,1):1,(0,-1):-1})]]
Ki=[[K[1][1],neg(K[0][1])],[neg(K[1][0]),K[0][0]]]
def mm(A,B):
 return [[sum_poly(mul(A[i][k],B[k][j]) for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def sum_poly(xs):
 a={}
 for b in xs:a=add(a,b)
 return a
def adj(A):return [[bar(A[j][i]) for j in range(len(A))] for i in range(len(A[0]))]
def eq(A,B):
 for ra,rb in zip(A,B):
  for a,b in zip(ra,rb):ck(a==b)
I=[[one,z],[z,one]];O=[[z,z],[z,z]]
eq(adj(K),[[neg(a) for a in r] for r in K]);eq(mm(K,Ki),I);eq(mm(Ki,K),I)
ck(add(mul(K[0][0],K[1][1]),neg(mul(K[0][1],K[1][0])))==one)
V=I+[[scale(2,a) for a in r] for r in K];W=I+K
J=[[z,z,one,z],[z,z,z,one],[neg(one),z,z,z],[z,neg(one),z,z]]
eq(mm(mm(adj(V),J),V),K);eq(mm(mm(adj(W),J),W),[[neg(a) for a in r] for r in K]);eq(mm(mm(adj(V),J),W),O)
Pi=[[scale(2,I[i][j]) for j in range(2)]+Ki[i] for i in range(2)]+[K[i]+[scale(2,I[i][j]) for j in range(2)] for i in range(2)]
eq(mm(Pi,Pi),Pi);eq(mm(Pi,V),V);eq(mm(Pi,W),[[z,z] for _ in range(4)])
for M in [K,Ki,Pi]:
 for row in M:
  for p in row:
   for i,j in p:ck(abs(i)<=1 and abs(j)<=1)
# Coefficient projections on arbitrary single-site physical basis vectors.
for x in range(-4,5):
 for y in range(-4,5):
  for t in range(4):
   v=[[{(x,y):1} if i==t else {}] for i in range(4)]
   pv=mm(Pi,v);qv=[[add(v[i][0],neg(pv[i][0]))] for i in range(4)]
   eq(mm(Pi,pv),pv);eq(mm(Pi,qv),[[z] for _ in range(4)])
   for row in pv+qv:
    for i,j in row[0]:ck(abs(i-x)<=1 and abs(j-y)<=1)
# Direct action of X^a Z^b on a qutrit basis vector j: phase b*j, output j+a.
for a,b,c,d,j in product(range(3),repeat=5):
 left=(d*j+b*((j+c)%3))%3;right=(b*j+d*((j+a)%3))%3
 ck((left-right)%3==(b*c-d*a)%3)
def rank(A):
 A=[[v%3 for v in r] for r in A];r=0
 for j in range(len(A[0])):
  pivot=next((i for i in range(r,len(A)) if A[i][j]),None)
  if pivot is None:continue
  A[r],A[pivot]=A[pivot],A[r];u=pow(A[r][j],-1,3);A[r]=[v*u%3 for v in A[r]]
  for i in range(len(A)):
   if i!=r:
    u=A[i][j];A[i]=[(a-u*b)%3 for a,b in zip(A[i],A[r])]
  r+=1
 return r
windows=[]
for m in range(1,9):
 for n in range(1,9):
  labels=[(x,y,t) for x in range(m) for y in range(n) for t in range(2)]
  for periodic in [False,True]:
   if not periodic:C=[[K[t][s].get((x-u,y-v),0) for u,v,s in labels] for x,y,t in labels]
   else:C=[[sum(c for (dx,dy),c in K[t][s].items() if (dx-x+u)%m==0 and (dy-y+v)%n==0)%3 for u,v,s in labels] for x,y,t in labels]
   for i in range(len(C)):
    ck(C[i][i]==0)
    for j in range(len(C)):ck((C[i][j]+C[j][i])%3==0)
   r=rank(C);ck(r%2==0);q=r//2;zz=len(C)-r
   ck(3**zz*(3**q)**2==3**len(C))
   if periodic:ck(r==len(C)) # follows independently from the Laurent inverse
   windows.append({'m':m,'n':n,'periodic':periodic,'rank':r,'nullity':zz})
for N in range(1,10):
 counts=[0,0,0]
 for labels in product(range(3),repeat=N):counts[sum(labels)%3]+=1
 for c in counts:ck(c==3**(N-1))
 ck(sum(c*c for c in counts)==3**(2*N-1))
result={'artifact_sha256':sha256(Path('PARTIAL_RESULT.md').read_bytes()).hexdigest(),'assertions':checks,'finite_windows':windows,'scope':'Exact local algebra diagnostics; finite windows and periodic quotients do not certify the conjectured two-sided bounded-spread net isomorphism.'}
Path('verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='finite_windows'}))
