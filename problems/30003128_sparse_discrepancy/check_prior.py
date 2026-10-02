import itertools,json
from fractions import Fraction
checks=0
def ck(x):
 global checks
 checks+=1;assert x

def connected(A):
 seen={0};todo=[0]
 while todo:
  v=todo.pop()
  for w,a in enumerate(A[v]):
   if a and w not in seen:seen.add(w);todo.append(w)
 return len(seen)==len(A)
def cutmax(A,d):
 n=len(A);B=[[n*a-d for a in row] for row in A];sums=[0]*n;old=0;best=0
 for j in range(1<<n):
  g=j^(j>>1)
  if j:
   bit=(g^old).bit_length()-1;sg=1 if g>>bit&1 else -1
   sums=[v+sg*w for v,w in zip(sums,B[bit])]
  ck(sum(sums)==0);best=max(best,sum(v for v in sums if v>0));old=g
 return best
fixtures=[]
for q,k in [(3,1),(4,1),(5,1),(3,2)]:
 vs=list(itertools.product(range(q),repeat=k));N=len(vs);d=(q-1)**k;m=d+1;n=N+m
 H=[[int(all(a!=b for a,b in zip(x,y))) for y in vs] for x in vs]
 ck(all(sum(r)==d for r in H));ck(connected(H))
 basis=[[1]*q]+[[int(j==i)-int(j==q-1) for j in range(q)] for i in range(q-1)]
 for choices in itertools.product(range(q),repeat=k):
  vec=[__import__('math').prod(basis[c][a] for c,a in zip(choices,v)) for v in vs]
  lam=__import__('math').prod((q-1 if c==0 else -1) for c in choices)
  ck(all(sum(a*b for a,b in zip(r,vec))==lam*vec[i] for i,r in enumerate(H)))
 A=[[0]*n for _ in range(n)]
 for i,j in itertools.product(range(N),repeat=2):A[i][j]=H[i][j]
 for i,j in itertools.product(range(N,n),repeat=2):A[i][j]=int(i!=j)
 w=[-m]*N+[N]*m;ck(sum(w)==0);ck(all(sum(a*b for a,b in zip(r,w))==d*w[i] for i,r in enumerate(A)))
 B=[r[:] for r in A]
 for i,j in [(0,N-1),(N,N+1)]:ck(B[i][j]==1);B[i][j]=B[j][i]=0
 for i,j in [(0,N),(N-1,N+1)]:ck(B[i][j]==0);B[i][j]=B[j][i]=1
 ck(all(sum(r)==d for r in B));ck(connected(B));ck(all(B[i][i]==0 for i in range(n)))
 energy=sum(w[i]*(d*w[i]-sum(B[i][j]*w[j] for j in range(n))) for i in range(n));norm=sum(v*v for v in w)
 ck(energy==2*n*n);ck(norm==m*N*n);ck(Fraction(energy,norm)==Fraction(2*n,m*N))
 ca=cutmax(A,d);cb=cutmax(B,d);bound=n*((d//(q-1))*N+4*d*m)
 ck(ca<=bound);ck(cb<=bound+8*n);ck(abs(ca-cb)<=8*n)
 fixtures.append({'q':q,'k':k,'N':N,'d':d,'n':n,'scaled_cutnorm_original':ca,'scaled_cutnorm_connected':cb,'scaled_universal_bound':bound,'laplacian_rayleigh':str(Fraction(energy,norm))})
for q in range(3,31):
 k=q*q;N=q**k;d=(q-1)**k;m=d+1;n=N+m
 ck(Fraction(d,N)<=Fraction(1,q+1));ck(Fraction(m,n)<=Fraction(d+1,N));ck(Fraction(2*n,d*m*N)==Fraction(2,d*m)+Fraction(2,d*N))
print(json.dumps({'assertions':checks,'fixtures':fixtures,'asymptotic_parameter_controls':28,'scope':'exact finite controls of a credited negative mechanism; uniform asymptotics proved in text'},indent=2))
