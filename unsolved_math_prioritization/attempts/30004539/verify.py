#!/usr/bin/env python3
"""Exact formal coefficients from signed simplex Gaussian moments."""
from fractions import Fraction as F
from math import factorial,comb,prod
from pathlib import Path
from hashlib import sha256
import json
N=24
checks=0

def ck(v):
 global checks
 assert v
 checks+=1

def add(p,q):
 r=p.copy()
 for k,v in q.items():r[k]=r.get(k,F(0))+v
 return {k:v for k,v in r.items() if v}
def scale(p,c):return {k:v*c for k,v in p.items() if v*c}
def mul(p,q):
 r={}
 for k,v in p.items():
  for l,w in q.items():r[k+l]=r.get(k+l,F(0))+v*w
 return {k:v for k,v in r.items() if v}
def vectors(k,budget,i=1):
 if i>k:yield ();return
 for j in range(budget//i+1):
  for tail in vectors(k,budget-i*j,i+1):yield (j,)+tail
kap={};moment_terms=0
for k in range(1,N+1):
 d=k*(k+1)//2
 if d>N:break
 kap[k]=[{} for _ in range(N+1)]
 for js in vectors(k,(N-d)//2):
  J=sum(js);weight=sum((i+1)*j for i,j in enumerate(js));degree=d+2*weight
  h=(k+1)//2
  den=prod(factorial(j) for j in js)*prod(sum(2*j+1 for j in js[i:]) for i in range(k))
  sign=(-1)**(k*(k-1)//2+J)
  if k%2:coeff=F(sign*factorial(h+J-1),2*den)
  else:
   h=k//2;coeff=F(sign*factorial(2*(h+J)),2**(2*(h+J)+1)*factorial(h+J)*den)
  kap[k][degree]=add(kap[k][degree],{h:coeff});moment_terms+=1
  ck(degree>=h and (degree-h)%2==0)
ck(kap[1][1]=={1:F(1,2)})
ck(kap[1][3]=={1:F(-1,6)})
ck(kap[2][3]=={1:F(-1,8)})
for j in range((N-1)//2+1):ck(kap[1][2*j+1]=={1:F((-1)**j,2*(2*j+1))})
K=max(kap)
L=[{} for _ in range(N+1)];L[0]={0:F(1,2)}
B={k:[{} for _ in range(N+1)] for k in kap}
for k in B:B[k][0]={0:F(2**k)}
for n in range(1,N+1):
 val={}
 for k in kap:
  for j in range(1,n+1):val=add(val,mul(kap[k][j],B[k][n-j]))
 L[n]=val
 for k in B:
  val={}
  for i in range(1,n+1):val=add(val,scale(mul(L[i],B[k][n-i]),F(n+(k-1)*i)))
  B[k][n]=scale(val,F(-2,n))
 # inverse-power recurrence is independently checked below by multiplication.
 for h in L[n]:ck(h<=n and (n-h)%2==0)
 a=F((-1)**(n-1)*2**(n-1)*comb(2*n-2,n-1),n)
 ck(L[n].get(n)==a)
 if n>=3:
  m=n-2;am=F((-1)**(m-1)*2**(m-1)*comb(2*m-2,m-1),m)
  ck(L[n].get(n-2)==-am*F(8*(n-3)+5,6))
# Independent direct convolution verifies all inverse powers used.
for n in range(N+1):
 z={}
 for i in range(n+1):z=add(z,mul(L[i],B[1][n-i]))
 ck(z==({0:F(1)} if n==0 else {}))
for k in range(2,K+1):
 for n in range(N+1):
  z={}
  for i in range(n+1):z=add(z,mul(B[k-1][i],B[1][n-i]))
  ck(z==B[k][n])
# All eight printed coefficients, not only their leading terms.
published={1:{1:F(1)},2:{2:F(-2)},3:{1:F(-5,6),3:F(8)},4:{2:F(13,3),4:F(-40)},5:{1:F(23,40),3:F(-28),5:F(224)},6:{2:F(-1069,180),4:F(580,3),6:F(-1344)},7:{1:F(-37,112),3:F(842,15),5:F(-4144,3),7:F(8448)},8:{2:F(943,168),4:F(-1535,3),6:F(10080),8:F(-54912)}}
for n,v in published.items():ck(L[n]==v)
receipt={'status':'PASS','assertions':checks,'maximum_Taylor_order':N,'simplex_moment_terms':moment_terms,'artifact_sha256':sha256(Path('PARTIAL_RESULT.md').read_bytes()).hexdigest() if Path('PARTIAL_RESULT.md').exists() else None,'scope':'Exact formal polynomial controls only; no convergence-radius inference','coefficients':{str(n):{str(h):str(v) for h,v in sorted(L[n].items())} for n in range(N+1)}}
Path('verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print({k:v for k,v in receipt.items() if k!='coefficients'})
