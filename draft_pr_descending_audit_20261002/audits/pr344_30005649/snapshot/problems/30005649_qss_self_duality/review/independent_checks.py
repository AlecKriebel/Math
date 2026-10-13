import json
N=0
def ck(v):
 global N
 assert v;N+=1
def rank(A,p):
 A=[list(r) for r in A];i=0
 if not A:return 0
 for j in range(len(A[0])):
  k=next((k for k in range(i,len(A)) if A[k][j]%p),None)
  if k is None:continue
  A[i],A[k]=A[k],A[i];q=pow(A[i][j]%p,-1,p);A[i]=[(x*q)%p for x in A[i]]
  for k in range(len(A)):
   if k!=i:
    q=A[k][j];A[k]=[(a-q*b)%p for a,b in zip(A[k],A[i])]
  i+=1
  if i==len(A):break
 return i
def mul(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def tr(A):return [list(x) for x in zip(*A)]
def cat(A,B):return [a+b for a,b in zip(A,B)]
def col(vs):return [list(x) for x in zip(*vs)]
F=[[0]*6 for _ in range(6)];V=[[0]*6 for _ in range(6)]
for i,j in [(1,0),(2,1),(4,3)]:F[i][j]=1
for i,j in [(5,0),(2,3),(4,5)]:V[i][j]=1
basis=[[int(i==j) for i in range(6)] for j in range(6)]
u=[0,1,0,1,0,1];v=[0,0,1,0,1,0];w=[0,2,0,1,0,0];z=basis[2]
B=col([u,v,w,z,basis[0],basis[1]]);L=col([basis[0],basis[3],basis[5]])
ck(mul(F,V)==mul(V,F)==[[0]*6 for _ in range(6)])
for p in [5,7,11,13,17,19,23,29,31,37]:
 ck(rank(B,p)==6);ck(rank(cat(F,L),p)==6);ck(rank(mul(V,L),p)==3)
 ck(rank(F,p)==rank(V,p)==3)
 for k in [2,4]:
  C=[r[:k] for r in B];ck(rank(cat(C,mul(F,C)),p)==k);ck(rank(cat(C,mul(V,C)),p)==k)
 for n in range(3,18):
  m=2*n;FF=[[0]*m for _ in range(m)];VV=[[0]*m for _ in range(m)]
  for i in range(6):
   for j in range(6):FF[i][j]=F[i][j];VV[i][j]=V[i][j]
  for i in range(6,m,2):FF[i+1][i]=VV[i+1][i]=1
  f2=mul(FF,FF);v2=mul(VV,VV);df2=mul(tr(VV),tr(VV));dv2=mul(tr(FF),tr(FF))
  ck(rank(f2,p)+rank(v2,p)-rank(cat(f2,v2),p)==0)
  ck(rank(df2,p)+rank(dv2,p)-rank(cat(df2,dv2),p)==1)
# Basis action identities are literal integer identities, hence all prime characteristics.
expectedF=col([v,[0]*6,[v[i]+z[i] for i in range(6)],[0]*6,basis[1],z])
expectedV=col([v,[0]*6,z,[0]*6,[u[i]-w[i]+basis[1][i] for i in range(6)],[0]*6])
ck(mul(F,B)==expectedF);ck(mul(V,B)==expectedV)
print(json.dumps({'status':'PASS','independent_exact_assertions':N,'prime_fields':10,'direct_sum_n_range':[3,17],'all_characteristic_basis_identities':True},indent=2))
