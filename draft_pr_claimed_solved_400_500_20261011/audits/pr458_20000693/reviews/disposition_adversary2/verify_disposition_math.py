#!/usr/bin/env python3
"""Exact finite formula sanity checks for the reviewed heuristic. No actual moment theorem."""
from fractions import Fraction as F
from math import factorial,prod
import json

def need(c,m):
 if not c:raise RuntimeError(m)
checks=[]
def check(c,n):need(c,n);checks.append(n)
def coeff(weights,values,N):
 b=[F(1)]
 for n in range(1,N+1):b.append(sum(sum(a*c**k for a,c in zip(weights,values))*b[n-k] for k in range(1,n+1))/n)
 return b
def G(n):return prod(factorial(j) for j in range(1,n-1))
def matrix(m,N):return prod(F(factorial(j-1)*factorial(j+2*m-1),factorial(j+m-1)**2) for j in range(1,N+1))
b=coeff([F(1),F(1)],[F(1),F(1)],20);check(b==[F(r+1) for r in range(21)],'repeated coefficient r+1')
x=F(1,2);j_one=1/(1-x);j_two=(1+x)/(1-x)**3
check((j_one,j_two)==(2,12),'p2 one and repeated local means')
check(j_one/j_two==F(1,6),'deleted local ratio one sixth')
check(j_two!=j_one*j_one and j_one*j_one==4,'common phase versus separate phase')
check(sum(a for a in [1,1])**2==4 and sum(a*a for a in [1,1])==2,'same versus distinct primitive exponent')
check(coeff([F(1),F(1)],[F(1),F(-1)],20)==[F(int(r%2==0)) for r in range(21)],'opposite local values even coefficients')
for eps in [-1,1]:
 for x in [F(1,2),F(1,5),F(1,11)]:
  local=(1+x)/(1-x)**3 if eps==1 else 1/(1-x*x)
  u=local*(1-x)**2
  check(u==(1+eps*x)/(1-eps*x),'Heap residual exact '+str(eps)+' '+str(x))
  check(u*(1-eps*x)**2==1-x*x,'cross regulator exact '+str(eps)+' '+str(x))
check(F(G(3)**2,G(5))==F(1,12),'Barnes weight2 one twelfth')
for N in range(1,9):
 check(matrix(0,N)==1,'CUE zero '+str(N))
 check(matrix(1,N)==N+1,'CUE weight1 '+str(N))
 check(matrix(2,N)==F((N+1)*(N+2)**2*(N+3),12),'CUE weight2 '+str(N))
lower=sum(F(1,2**r*factorial(r)**2) for r in range(3));upper=lower+F(1,288)/(1-F(1,32))
check(lower<upper<F(13,8)<2,'finite sharp exp(z) versus full Euler rigorous enclosure')
check(coeff([],[],20)==[F(1)]+[F(0)]*20,'zero weights exact local series')
print(json.dumps({'claim_kind':'finite exact formula checks only; no actual L-moment or model assumptions proved','guards':len(checks),'checks':checks,'sharp_mean_rational_enclosure':[str(lower),str(upper)],'irrational_ratio_limit':'No finite search is used as proof. If sqrt2=e2/e1, parity of e2^2=2e1^2 gives infinite descent.','original_proof_search_attempts':0},indent=2))
