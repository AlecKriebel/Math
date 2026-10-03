from fractions import Fraction as F
import json
checks=0
for n in range(2,21):
 for seed in range(7):
  a=[F((i+seed+2)**2-3*i-13,seed+3) for i in range(n)]
  b=[F(i+seed+1,seed+2) for i in range(n-1)]
  J=[[F(0) for _ in range(n)] for _ in range(n)]
  B=[[F(0) for _ in range(n)] for _ in range(n)]
  for i in range(n):J[i][i]=a[i]
  for i in range(n-1):J[i][i+1]=J[i+1][i]=b[i];B[i][i+1]=b[i];B[i+1][i]=-b[i]
  dJ=[[sum((B[i][k]*J[k][j]-J[i][k]*B[k][j] for k in range(n)),F(0)) for j in range(n)] for i in range(n)]
  assert sum((F(i+1)*dJ[i][i] for i in range(n)),F(0))==-2*sum((x*x for x in b),F(0));checks+=1
  assert sum((dJ[i][i] for i in range(n)),F(0))==0;checks+=1
  assert sum((J[i][j]*dJ[j][i] for i in range(n) for j in range(n)),F(0))==0;checks+=1
  for i in range(n-1):
   assert dJ[i][i+1]==b[i]*(a[i+1]-a[i]);checks+=1
  assert sum((F(i+1)-F(n+1,2))**2 for i in range(n))==F(n*(n*n-1),12);checks+=1
print(json.dumps({'assertions':checks,'status':'PASS','scope':'exact rational Lax, Lyapunov, and clock controls'},indent=2))
