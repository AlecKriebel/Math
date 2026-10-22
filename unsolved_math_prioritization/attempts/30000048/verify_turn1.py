"""Exact controls for the product-SU2 partial. The written argument is essential."""
from itertools import product
from fractions import Fraction as Q
from math import comb
import json
count=0

def ck(x):
 global count
 assert x
 count+=1

def add(a,b):
 c=dict(a)
 for k,v in b.items():c[k]=c.get(k,0)+v
 return {k:v for k,v in c.items() if v}

def mul(a,b):
 c={}
 for k,v in a.items():
  for l,w in b.items():c[k+l]=c.get(k+l,0)+v*w
 return {k:v for k,v in c.items() if v}

def neg(a):return {k:-v for k,v in a.items()}

def chi(d):return {j:1 for j in range(1-d,d,2)}
w={0:2,2:-1,-2:-1}
# Every rank-one character square, its exact density polynomial, and Haar mean.
for d in range(1,61):
 sq=mul(chi(d),chi(d));F=mul(sq,w)
 ck(F=={0:2,2*d:-1,-2*d:-1})
 ck(Q(F.get(0,0),2)==1)
 # Recurrence and monicity are independently generated in x.
P=[{}, {0:1},{1:1}]
for d in range(2,61):P.append(add(mul({1:1},P[d]),neg(P[d-1])))
for d in range(1,61):
 ck(max(P[d])==d-1 and P[d][d-1]==1)
 sub={}
 for k,v in P[d].items():
  pw={0:1}
  for _ in range(k):pw=mul(pw,{1:1,-1:1})
  sub=add(sub,{e:v*c for e,c in pw.items()})
 ck(sub==chi(d))
# Polynomial Haar integration via Catalan moments agrees with character selection.
def haar_poly(p):
 return sum(Q(v*comb(k,k//2),k//2+1) for k,v in p.items() if k%2==0)
for a,b in product(range(1,21),repeat=2):
 ck(haar_poly(mul(P[a],P[b]))==(1 if a==b else 0))
# Root-of-unity residue sums; no numerical root evaluations.
for M in range(1,31):
 for seed in range(11):
  a={j:(seed*7+j*j+3*j)%9-4 for j in range(M+1)}
  coeff={0:a[0]}
  for j in range(1,M+1):coeff[j]=coeff[-j]=a[j]
  plus=sum(v for j,v in coeff.items() if j%M==0)
  minus=sum(v*(-1 if (j//M)%2 else 1) for j,v in coeff.items() if j%M==0)
  ck(plus==a[0]+2*a[M]);ck(minus==a[0]-2*a[M])
# Tensor-product Haar means and leading-coefficient normalization.
for r in range(1,6):
 for ds in product(range(1,5),repeat=r):
  hmeans=[haar_poly(mul(P[d],P[d])) for d in ds]
  prod=Q(1)
  for h in hmeans:prod*=h
  ck(prod==1)
  Ft=mul(mul(chi(ds[0]),chi(ds[0])),w)
  ck(Ft[max(Ft)]==-1 and Ft[0]==2)
# Integral, real Laurent polynomials with Parseval norm <=1 are constants.
for a in product(range(-2,3),repeat=4):
 norm=a[0]**2+2*sum(x*x for x in a[1:])
 if norm<=1:ck(a[1:]==(0,0,0) and a[0] in [-1,0,1])
# A rational nonintegral countercontrol to the domination conclusion: Q(y)=y/2.
for j in range(-20,21):
 y=Q(j,10);ck(abs(y/2)<=1)
print(json.dumps({'status':'PASS','exact_assertions':count,'scope':'Exact Laurent density/recurrence/Haar orthogonality, root-of-unity averaging and tensor-product controls; the all-r positivity/divisibility theorem is proved in TURN_1.md and remains pending separate review.','original_status':'unresolved','completed_substantive_author_turns':1},indent=2,sort_keys=True))
