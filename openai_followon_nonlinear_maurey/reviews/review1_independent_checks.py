from fractions import Fraction as F
import random,json,datetime
from pathlib import Path
rng=random.Random(497233)
phi=lambda x:3*x*x-2*x*x*x
quartic=0
for _ in range(1000):
 d=rng.randint(1,9);w=[F(rng.randint(1,12),rng.randint(1,15))*F(10)**rng.randint(-3,3) for _ in range(d)]
 e=[F(rng.randrange(2)) for _ in range(d)];u=[F(rng.randint(0,12),12) for _ in range(d)];v=[F(rng.randint(0,12),12) for _ in range(d)]
 a=[u[i]-e[i] for i in range(d)];z=[v[i]-u[i] for i in range(d)]
 A=sum(w[i]*a[i]**2 for i in range(d));B=sum(w[i]*z[i]**2 for i in range(d));c=sum(w[i]*a[i]*z[i] for i in range(d))
 R=sum(w[i]*(v[i]-e[i])**2 for i in range(d))**2-A*A-4*A*c
 assert R==2*A*B+(2*c+B)**2
 assert sum(w[i]*abs(phi(v[i])-phi(u[i])) for i in range(d))**2<=108*R
 quartic+=1
def mul(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def solve(A,B):
 n=len(A);d=len(B[0]);C=[A[i]+B[i] for i in range(n)]
 for k in range(n):
  j=next(j for j in range(k,n) if C[j][k]);C[k],C[j]=C[j],C[k]
  m=C[k][k];C[k]=[x/m for x in C[k]]
  for j in range(n):
   if j!=k:
    m=C[j][k];C[j]=[C[j][i]-m*C[k][i] for i in range(n+d)]
 return [row[n:] for row in C]
chains=0;nonreversible=0;maxratio=F(0)
for sample in range(180):
 n=rng.randint(2,5);d=rng.randint(1,7);t=rng.choice([1,2,3,7,13])
 A=[[F(0) for _ in range(n)] for _ in range(n)]
 for _ in range(3):
  perm=list(range(n));rng.shuffle(perm)
  for i in range(n):A[i][perm[i]]+=F(1,3)
 pi=[F(1,n)]*n
 if A!=[list(row) for row in zip(*A)]:nonreversible+=1
 z=[[F(rng.randrange(2)) for _ in range(d)] for _ in range(n)];w=[F(rng.randint(1,9),rng.randint(1,7)) for _ in range(d)]
 p=F(1,t+1);q=1-p
 h=solve([[F(i==j)-q*A[i][j] for j in range(n)] for i in range(n)],[[p*x for x in row] for row in z])
 assert all(0<=x<=1 for row in h for x in row)
 y=[[phi(x) for x in row] for row in h]
 dist=lambda u,v:sum(w[k]*abs(u[k]-v[k]) for k in range(d))
 lhs=sum(pi[i]*dist(z[i],y[i])**2 for i in range(n))+t*sum(pi[i]*A[i][j]*dist(y[i],y[j])**2 for i in range(n) for j in range(n))
 Ap=[[F(i==j) for j in range(n)] for i in range(n)];W=F(0)
 for s in range(t):
  Ap=mul(Ap,A)
  W+=sum(pi[i]*Ap[i][j]*dist(z[i],z[j])**2 for i in range(n) for j in range(n))/t
 assert lhs<=3024*W,(sample,lhs,W)
 if W:maxratio=max(maxratio,lhs/W)
 chains+=1
result={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'weighted_multidimensional_quartic_cases':quartic,'exact_stationary_chain_cases':chains,'nonreversible_cases':nonreversible,'chain_times':[1,2,3,7,13],'largest_cotype_squared_ratio_exact':str(maxratio),'largest_cotype_squared_ratio_float':float(maxratio),'all_passed':True,'scope':'Deterministic rational error-detection checks; not a proof, formalization or exhaustive search.'}
Path('work/package_review_1/independent_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
