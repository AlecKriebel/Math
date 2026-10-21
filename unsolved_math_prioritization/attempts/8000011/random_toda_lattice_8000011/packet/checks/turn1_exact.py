from fractions import Fraction as F
from itertools import combinations
import json
count=0
for n in range(2,7):
 for off in [0,3]:
  lam=[j*j+j+off for j in range(n)]
  w=[F(j+1,n*(n+1)//2) for j in range(n)]
  def coeff(I):
   v=F(1)
   for i in I:v*=w[i]
   for i,j in combinations(I,2):v*=F((lam[j]-lam[i])**2)
   return v
  A=[coeff(tuple(range(n-k,n))) for k in range(n+1)]
  S=[sum(lam[n-k:]) for k in range(n+1)]
  tau0=[sum((coeff(I) for I in combinations(range(n),k)),F(0)) for k in range(n+1)]
  M=[tau0[k]/A[k] for k in range(n+1)]
  for z in [F(1),F(3,2),F(2),F(5)]:
   tau=[sum((coeff(I)*z**sum(lam[i] for i in I) for I in combinations(range(n),k)),F(0)) for k in range(n+1)]
   for k in range(1,n):
    b2=tau[k-1]*tau[k+1]/tau[k]**2
    d=lam[n-k]-lam[n-k-1]
    c2=A[k-1]*A[k+1]/A[k]**2
    assert c2*z**(-d)/M[k]**2 <= b2 <= c2*M[k-1]*M[k+1]*z**(-d)
    count+=2
    # Each tau lies inside the termwise spectral envelope.
   for k in range(n+1):
    assert A[k]*z**S[k] <= tau[k] <= tau0[k]*z**S[k]
    count+=2
# Rational square control of the nonmonotone n=2 example.
assert F(16*99,10000)<F(1,4)<F(4)
count+=2
print(json.dumps({'assertions':count,'status':'PASS','scope':'exact finite envelope controls; analytic proof required for all data'},indent=2))
