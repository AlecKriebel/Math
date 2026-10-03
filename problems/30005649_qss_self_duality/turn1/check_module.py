import json,itertools
checks=0
def ck(x):
 global checks
 checks+=1;assert x

def mat(n,entries):
 A=[[0]*n for _ in range(n)]
 for i,j,x in entries:A[i][j]=x
 return A

def mul(A,B):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*B)] for r in A]
def tr(A):return list(map(list,zip(*A)))
def cat(A,B):return [a+b for a,b in zip(A,B)]
def rank(A,p):
 a=[[x%p for x in r] for r in A];i=0
 for j in range(len(a[0])):
  q=next((q for q in range(i,len(a)) if a[q][j]),None)
  if q is None:continue
  a[i],a[q]=a[q],a[i];d=pow(a[i][j],-1,p);a[i]=[x*d%p for x in a[i]]
  for q in range(len(a)):
   if q!=i:
    d=a[q][j];a[q]=[(x-d*y)%p for x,y in zip(a[q],a[i])]
  i+=1
  if i==len(a):break
 return i
F=mat(6,[(1,0,1),(2,1,1),(4,3,1)]);V=mat(6,[(5,0,1),(2,3,1),(4,5,1)])
T=tr([[0,1,0,1,0,1],[0,0,1,0,1,0],[0,2,0,1,0,0],[0,0,1,0,0,0],[1,0,0,0,0,0],[0,1,0,0,0,0]])
FN=mat(6,[(1,0,1),(1,2,1),(3,2,1),(5,4,1),(3,5,1)])
VN=mat(6,[(1,0,1),(3,2,1),(0,4,1),(2,4,-1),(5,4,1)])
ck(mul(F,T)==mul(T,FN));ck(mul(V,T)==mul(T,VN))
ck(mul(F,V)==mat(6,[]));ck(mul(V,F)==mat(6,[]))
primes=[5,7,11,13,17,19,23,29,31,37]
for p in primes:
 ck(rank(T,p)==6)
 for n in range(3,13):
  d=2*n;f=mat(d,[]);v=mat(d,[])
  for i,j in itertools.product(range(6),repeat=2):f[i][j]=F[i][j];v[i][j]=V[i][j]
  for j in range(6,d,2):f[j+1][j]=v[j+1][j]=1
  L=[[int(i==j) for j in [0,3,5]+list(range(6,d,2))] for i in range(d)]
  ck(rank(f,p)==n);ck(rank(v,p)==n);ck(mul(f,v)==mat(d,[]));ck(mul(v,f)==mat(d,[]))
  ck(rank(cat(f,L),p)==d);ck(rank(L,p)==n);ck(rank(mul(v,L),p)==n)
  f2=mul(f,f);v2=mul(v,v);fd2=mul(tr(v),tr(v));vd2=mul(tr(f),tr(f))
  ck(rank(f2,p)+rank(v2,p)-rank(cat(f2,v2),p)==0)
  ck(rank(fd2,p)+rank(vd2,p)-rank(cat(fd2,vd2),p)==1)
 for a in [FN,VN]:
  for size in [2,4]:ck(all(a[i][j]%p==0 for i in range(size,6) for j in range(size)))
  for b in [0,2,4]:ck([[a[b+i][b+j]%p for j in range(2)] for i in range(2)]==[[0,0],[1,0]])
# F_25 = F_5[t]/(t^2-2), sigma(a+bt)=a-bt.
def add(a,b):return ((a[0]+b[0])%5,(a[1]+b[1])%5)
def times(a,b):return ((a[0]*b[0]+2*a[1]*b[1])%5,(a[0]*b[1]+a[1]*b[0])%5)
def sig(a):return (a[0],-a[1]%5)
def dot(a,b):
 s=(0,0)
 for x,y in zip(a,b):s=add(s,times(x,y))
 return s
def act(A,x):return [dot([(a%5,0) for a in r],[sig(z) for z in x]) for r in A]
state=1729
def vec():
 global state
 out=[]
 for i in range(6):
  state=(1664525*state+1013904223)%2**32;a=state%25;out.append((a%5,a//5))
 return out
for _ in range(2000):
 x=vec();phi=vec();ck(dot(act(tr(V),phi),x)==sig(dot(phi,act(V,x))));ck(dot(act(tr(F),phi),x)==sig(dot(phi,act(F,x))))
 ck(act(F,act(V,x))==[(0,0)]*6);ck(act(V,act(F,x))==[(0,0)]*6)
print(json.dumps({'assertions':checks,'prime_fields':primes,'n_values':list(range(3,13)),'original_delta':0,'dual_delta':1,'semilinear_field':25,'semilinear_vector_pairs':2000,'integer_basis_identities':True},indent=2))
