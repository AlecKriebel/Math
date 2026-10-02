"""Finite exact controls for multiplicity counts and the infinite-prefix boundary."""
from fractions import Fraction as F
from math import comb,prod
import json
N=0
def ck(b):
 global N
 N+=1
 assert b
def compositions(n):
 if n==0:yield ()
 else:
  for mask in range(1<<(n-1)):
   a=[];last=0
   for i in range(1,n):
    if mask>>(i-1)&1:a.append(i-last);last=i
   a.append(n-last);yield tuple(a)
def main():
 counts=0
 for D in range(1,15):
  for es in compositions(D):
   ck(sum(es)==D);ck(prod(e+1 for e in es)<=2**D);counts+=1
  ck(2**(D-1)*2**D==2**(2*D-1))
 H=[F(comb(2*k,k),4**k) for k in range(81)]
 ck(H[0]==1)
 for k in range(1,81):
  ck(0<H[k]<1);ck(H[k]==H[k-1]*F(2*k-1,2*k))
 for k in range(81):ck(sum(H[i]*H[k-i] for i in range(k+1))==1)
 for M in range(1,81):
  c=[F(0)]*(2*M+1)
  for i in range(M+1):
   for j in range(M+1):c[i+j]+=H[i]*H[j]
  ck(all(x==1 for x in c[:M+1]));ck(c[-1]==H[M]**2);ck(0<c[-1]<1)
 # A concrete fixed-degree residual check: (1+x)(1+b*x+x^2).
 for den in range(1,51):
  for num in range(den+1):
   b=F(num,den);c=(1,1+b,1+b,1)
   ck(max(abs(x-y) for x,y in zip(c,(1,1,1,1)))==b)
 print(json.dumps({'problem_id':159,'turn':5,'status':'PASS','exact_assertions':N,'root_multiplicity_compositions':counts,'formal_series_coefficients_checked':81,'finite_truncations_checked':80,'scope':'Exact controls of counting bounds and prefix failures. No arbitrary-degree fairness decision or numerical compactness threshold is claimed.'},indent=2))
if __name__=='__main__':main()
