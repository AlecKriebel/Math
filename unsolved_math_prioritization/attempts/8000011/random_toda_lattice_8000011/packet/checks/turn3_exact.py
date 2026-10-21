from fractions import Fraction as F
from itertools import combinations
import json
checks=0
for n in range(2,12):
 lam=[j*j+2*j for j in range(n)];w=[F(j+2,n*(n+3)//2) for j in range(n)]
 def A(k):
  I=range(n-k,n);p=F(1)
  for i in I:p*=w[i]
  for i,j in combinations(I,2):p*=(lam[j]-lam[i])**2
  return p
 for r in range(n-1):
  k=n-r-1 # zero-based r corresponds to one-based gap r+1
  c2=A(k-1)*A(k+1)/A(k)**2
  form=F((lam[r+1]-lam[r])**2)*w[r]/w[r+1]
  for j in range(r+2,n):form*=F(lam[j]-lam[r],lam[j]-lam[r+1])**2
  assert c2==form;checks+=1
print(json.dumps({'assertions':checks,'status':'PASS','scope':'dominant coupling coefficient algebra for finite exact controls'},indent=2))
