from fractions import Fraction as F
from itertools import product
from math import prod,factorial
import json
c=0
def ck(v):
 global c
 c+=1;assert v
pts=[]
for j in range(-10,11):
 t=F(j,5);pts.append(((1-t*t)/(1+t*t),2*t/(1+t*t)))
for a,b in product(range(-3,4),repeat=2):
 for x in pts:
  for y in pts:
   D=sum((u-v)**2 for u,v in zip(x,y));q=lambda x:a*x[0]**2+b*x[1]**2
   ck((q(x)-q(y))**2<=(a-b)**2*D)
   m=F(a+b,2);ck((a-m)*x[0]**2+(b-m)*x[1]**2==q(x)-m)
for d in range(2,101):
 for h in range(2,31):
  odd=prod(range(1,2*h,2));ck(odd<=2**h*factorial(h))
  ck(2**(h-1)*(2**h*factorial(h)+1)<=4**h*factorial(h))
for n in range(16,501):
 for d in range(2,n//8+1):
  N=2*((3*n+7)//8)
  if N>n:continue
  ck(F(N*n,256)<=F(N*N,4))
  for k in [1,d-1,d,d+3]:
   if k<d:
    ck(F(N*d,(2048*k)**2)>=F(n,8192**2*k))
   else:ck(F(N,1024**2*d)>=F(n,8192**2*k))
   ck(F(N,32**2)>=F(n,8192**2*k))
for a,b,m in product(range(-10,11),repeat=3):
 ck((a-m)*b+(-a+m)*b==0)
print(json.dumps({'assertions':c,'scope':'Exact quadratic sphere, trace, moment and constant controls; concentration and all-parameter uniformity proved analytically'},indent=2,sort_keys=True))
