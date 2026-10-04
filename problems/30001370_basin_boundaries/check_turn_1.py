#!/usr/bin/env python3
"""Exact finite controls. The infinite-dimensional proof is in TURN_1.md."""
from fractions import Fraction as F
import itertools,json
import sympy as s
checks=0
def ck(test):
 global checks
 assert test
 checks+=1
x,r=s.symbols('x r')
h=lambda z,t:(z+t/4)/(1+t*z)
for expr in [h(h(x,r),-r)-x,h(s.Rational(1,2),r)-s.Rational(1,2),h(-s.Rational(1,2),r)+s.Rational(1,2),s.diff(h(x,r),x)-(1-r*r/4)/(1+r*x)**2,s.diff(h(x,r),r)-(s.Rational(1,4)-x*x)/(1+r*x)**2,2*h(x,r)+s.Rational(1,2)-((r+4)*x+r+1)/(2*r*x+2),h(-r/4,r)]:
 ck(s.factor(expr)==0)
symbolic=checks
# Branchwise sections: zero target density and zero individual branches included.
branch_cases=0
for a,b,c in itertools.product(range(5),repeat=3):
 v=F(a+b,2)
 qa=F(a,1)/v if v else F(1)
 qb=F(b,1)/v if v else F(1)
 ck(0<=qa<=2 and 0<=qb<=2)
 ck((qa+qb)/2==1)
 ck(qa*v==a and qb*v==b)
 ck((qa*c+qb*c)/2==c)
 ck((abs(qa*c-a)+abs(qb*c-b))/2==abs(c-v))
 branch_cases+=1
branch_checks=checks-symbolic
# All symmetric dyadic tables with half-table entries 0,1,2 up to depth 4.
def P(tab):
 n=len(tab)//2
 return [(tab[j]+tab[j+n])/2 for j in range(n)]
dyadic_cases=0
before=checks
for depth in range(1,5):
 n=2**depth
 for half in itertools.product(range(3),repeat=n//2):
  if not any(half):continue
  tab=list(map(F,half+half[::-1])); total=sum(tab)
  tab=[n*v/total for v in tab]
  for j in range(depth):
   ck(tab==tab[::-1])
   m=len(tab)
   mean=sum(tab[k]*F(2*k+1-m,2*m) for k in range(m))/m
   ck(mean==0)
   tab=P(tab)
  ck(tab==[F(1)])
  dyadic_cases+=1
print(json.dumps({'status':'PASS','symbolic_identities':symbolic,'branch_cases':branch_cases,'branch_assertions':branch_checks,'symmetric_dyadic_cases':dyadic_cases,'dyadic_assertions':checks-before,'exact_assertions':checks,'limitations':'Finite controls do not certify infinite-dimensional topology or the unresolved closure in (7).'},indent=2,sort_keys=True))
