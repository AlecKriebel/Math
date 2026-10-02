from fractions import Fraction as Q
from random import Random
import json
r=Random(20000207);n=0
def rank(a):
 a=[[Q(x) for x in row] for row in a];k=0
 for j in range(len(a[0])):
  i=next((i for i in range(k,len(a)) if a[i][j]),None)
  if i is None:continue
  a[k],a[i]=a[i],a[k];v=a[k][j];a[k]=[x/v for x in a[k]]
  for i in range(len(a)):
   if i!=k:
    v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[k])]
  k+=1
 return k

def ck(x):
 global n;n+=1;assert x
for k in range(1,11):
 for p in range(1,8):
  for m in range(1,5):
   for _ in range(5):
    A=[[r.randrange(-3,4) for _ in range(k)] for _ in range(p)]
    C=[[r.randrange(-3,4) for _ in range(p)] for _ in range(m)]
    B=[[sum(C[i][j]*A[j][t] for j in range(p)) for t in range(k)] for i in range(m)]
    ck(rank(A+B)==rank(A))
# D(x,y)=x; F(x,y)=y violates the hypothesis and adds image dimension.
ck(rank([[1,0],[0,1]])==2);ck(rank([[1,0]])==1)
# F=x^2 has differential a scalar multiple of dD, even with a free y fiber.
for x in range(-100,101):ck(rank([[1,0],[2*x,0]])==1)
print(json.dumps({'assertions':n,'scope':'Exact linear controls; algebraic generic-fiber theorem is written in TURN_4.md.'},indent=2))
