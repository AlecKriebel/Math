from itertools import permutations
from fractions import Fraction as F
import json
from gaussian_matrix import add as ga,mul as gm
checks=0
def check(x):
 global checks
 assert x;checks+=1
# Laurent polynomials in(E,z,w), Gaussian integer coefficients.
def plus(A,B):
 C=dict(A)
 for k,v in B.items():
  C[k]=ga(C.get(k,(0,0)),v)
  if C[k]==(0,0):del C[k]
 return C
def times(A,B):
 C={}
 for a,u in A.items():
  for b,v in B.items():
   k=tuple(x+y for x,y in zip(a,b));C=plus(C,{k:gm(u,v)})
 return C
def mon(e,z,w,a=1,b=0):return{(e,z,w):(a,b)}
def neg(A):return{k:(-v[0],-v[1]) for k,v in A.items()}
one=mon(0,0,0);E=mon(1,0,0);z=mon(0,1,0);zi=mon(0,-1,0)
a=plus(z,zi);b=plus(mon(0,1,0,0,1),mon(0,-1,0,0,-1));diag=[a,b,neg(a),neg(b)]
M=[[{} for j in range(4)] for i in range(4)]
for i in range(4):M[i][i]=plus(E,neg(diag[i]))
for i in range(3):M[i][i+1]=M[i+1][i]=neg(one)
M[3][0]=neg(mon(0,0,1));M[0][3]=neg(mon(0,0,-1))
det={}
for p in permutations(range(4)):
 t=one
 for i,j in enumerate(p):t=times(t,M[i][j])
 inv=sum(p[i]>p[j] for i in range(4) for j in range(i+1,4));det=plus(det,neg(t) if inv%2 else t)
expected={(4,0,0):(1,0),(2,0,0):(-8,0),(0,0,0):(4,0),(0,4,0):(-1,0),(0,-4,0):(-1,0),(0,0,1):(-1,0),(0,0,-1):(-1,0)}
check(det==expected)
# Laurent rational Chebyshev recurrence T_n((z+z^-1)/2).
def pa(A,B):
 C=dict(A)
 for k,v in B.items():
  C[k]=C.get(k,F(0))+v
  if not C[k]:del C[k]
 return C
def pm(A,B):
 C={}
 for a,u in A.items():
  for b,v in B.items():C=pa(C,{a+b:u*v})
 return C
x={1:F(1,2),-1:F(1,2)};old={0:F(1)};cur=x
for n in range(1,21):
 check(cur=={n:F(1,2),-n:F(1,2)})
 old,cur=cur,pa({k:2*v for k,v in pm(x,cur).items()},{k:-v for k,v in old.items()})
# Derivative of trace g(C(c)) for roots of p(x)-c, via dual numbers.
def da(x,y):return(x[0]+y[0],x[1]+y[1])
def dm(x,y):return(x[0]*y[0],x[0]*y[1]+x[1]*y[0])
def mm(A,B):
 n=len(A);R=[[(F(0),F(0)) for j in range(n)] for i in range(n)]
 for i in range(n):
  for k in range(n):
   for j in range(n):R[i][j]=da(R[i][j],dm(A[i][k],B[k][j]))
 return R
cases=0
for n in range(1,9):
 roots=[F(2*i-n+1,n+1) for i in range(n)];poly=[F(1)]
 for r in roots:
  nxt=[F(0)]*(len(poly)+1)
  for k,a in enumerate(poly):nxt[k]-=r*a;nxt[k+1]+=a
  poly=nxt
 C=[[(F(0),F(0)) for j in range(n)] for i in range(n)]
 for i in range(1,n):C[i][i-1]=(F(1),F(0))
 for i in range(n):C[i][-1]=(-poly[i],F(i==0))
 power=[[(F(i==j),F(0)) for j in range(n)] for i in range(n)]
 for m in range(1,n+7):
  power=mm(power,C);deriv=sum(power[i][i][1] for i in range(n));dd=F(0)
  for i,r in enumerate(roots):
   denom=F(1)
   for j,s in enumerate(roots):
    if i!=j:denom*=r-s
   dd+=m*r**(m-1)/denom
  check(deriv==dd);cases+=1
print(json.dumps(dict(assertions=checks,characteristic_polynomial_terms=len(det),chebyshev_degrees=20,divided_difference_cases=cases,scope='Exact algebraic controls for the proved uniform-flux holonomy optimum and continuum formula; nonuniform energy comparison unresolved.'),indent=2,sort_keys=True))
