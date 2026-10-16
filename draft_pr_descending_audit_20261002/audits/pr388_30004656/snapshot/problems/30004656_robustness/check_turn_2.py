from fractions import Fraction as F
from math import comb,factorial
import json
checks=0
def ck(x):
 global checks
 checks+=1
 assert x
for M in range(1,9):
 dp={(0,)*M:1};st=[1]+[0]*15
 for n in range(0,15):
  total=sum(dp.values());prob=F(total,(2*M)**n)
  form=sum(F((-1)**j*comb(M,j)*2**(M-j))*F(M-j,2*M)**n for j in range(M+1))
  ck(prob==form)
  occ=sum(F(factorial(M),factorial(M-k))*st[k]*2**k for k in range(min(M,n)+1))/((2*M)**n)
  ck(occ==prob);ck(0<=prob<=1)
  nxt={}
  for s,count in dp.items():
   for i in range(M):
    for sign in (-1,1):
     if s[i] in (0,sign):
      t=list(s);t[i]=sign;t=tuple(t);nxt[t]=nxt.get(t,0)+count
  dp=nxt
  st=[0]+[st[k-1]+k*st[k] for k in range(1,16)]
for den in range(1,101):
 for num in range(0,den+1):
  x=F(num,den);ck(x/(1+x)>=x/2)
for s in range(1,11):
 for m in range(1,101):
  # If x lies in(m-1,m] with x>=1, ceil(x)<=2x; test its smallest relevant endpoint.
  x=F(max(2*m-1,2),2);ceil=(x.numerator+x.denominator-1)//x.denominator
  ck(x**s<=ceil**s<=2**s*x**s)
  A0=F(1,s+1);A=F(3);B=64*2**s*(A+1)/A0**2
  ck(A0**2*B/(64*2**s)==A+1)
print(json.dumps({'assertions':checks,'equal_cell_counts':[1,8],'fixed_sample_sizes':[0,14],'scope':'Exact occupancy and rational inequality controls; chart and asymptotic probability theorem proved in text'},indent=2,sort_keys=True))
