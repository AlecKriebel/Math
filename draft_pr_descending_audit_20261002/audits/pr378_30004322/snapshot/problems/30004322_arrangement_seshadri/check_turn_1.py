#!/usr/bin/env python3
"""Exact degree-bound and fat-point controls; requires SymPy."""
import itertools,json,math
from fractions import Fraction as F
import sympy as s
N=0
def ck(v):
 global N
 assert v;N+=1
def bound(r,k):
 A=k*k-r;B=2*k-r*k+3*r;C=1-3*r
 assert A>0
 return max((r+2*k-1)//(2*k),(-B+math.isqrt(B*B-4*A*C))//(2*A))
for k in range(2,25):
 for r in range(2,k*k):
  D=bound(r,k);A=k*k-r;B=2*k-r*k+3*r;C=1-3*r
  ck(A*(D+1)**2+B*(D+1)+C>0)
  ck(k*(D+1)+1>=F(r,2))
  ck(2*A*(D+1)+B>0)
  for d in (D+1,D+2,D+10):
   v=(k*d+1)**2-r*(k*d+1)-r*(d*d-3*d+2)
   ck(v==A*d*d+B*d+C and v>0)
def max_collinear(P):
 return max(sum((x-b[0])*(a[1]-b[1])==(y-b[1])*(a[0]-b[0]) for x,y in P) for a,b in itertools.combinations(P,2))
def conic_eval(P):return s.Matrix([[1,x,y,x*x,x*y,y*y] for x,y in P])
star=[(s.Rational(-a-b),s.Rational(-a*b)) for a,b in itertools.combinations(range(5),2)]
ck(len(set(star))==10);ck(max_collinear(star)==4);ck(bound(10,4)==2)
ranks=[]
for J in itertools.combinations(range(10),9):
 rank=conic_eval([star[i] for i in J]).rank();ck(rank==6);ranks.append(rank)
par=[(s.Rational(t),s.Rational(t*t)) for t in range(7)]+[(s.Rational(1,2),s.Rational(1,2))]
ck(max_collinear(par)==3);ck(bound(8,3)==2);ck(conic_eval(par).rank()==6)
deficient=[]
for J in itertools.combinations(range(8),7):
 rank=conic_eval([par[i] for i in J]).rank()
 if rank<6:deficient.append(J)
ck(deficient==[tuple(range(7))]);ck(F(2,7)<F(1,3))
# Exact adjunction and quadratic coefficients.
d,r,k,S=s.symbols('d r k S')
ck(s.expand((k*d+1)**2-r*(k*d+1)-r*(d*d-3*d+2))==s.expand((k*k-r)*d*d+(2*k-r*k+3*r)*d+1-3*r))
print(json.dumps({'status':'PASS','assertions':N,'star_result':'1/4 (credited known family)','arbitrary_point_control':'2/7, not an arrangement counterexample','star_nine_point_ranks':ranks,'parabola_deficient_seven_subset':[list(x) for x in deficient],'scope':'Exact finite controls supplement the all-degree proof; arbitrary r>=k² is outside the algorithm.'},indent=2,sort_keys=True))
