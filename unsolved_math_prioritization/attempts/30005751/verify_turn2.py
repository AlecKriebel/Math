"""Exact polynomial certificates for the oddless-model obstruction."""
from fractions import Fraction as F
import itertools as it,json
N=0
def check(x):
 global N
 N+=1
 assert x

def clean(p):return {q:a for q,a in p.items() if a}
def const(p):return p.get(F(0),F(0))
def scale(p,a):return clean({q:a*b for q,b in p.items()})
def mul(p,r):
 s={}
 for q,a in p.items():
  for w,b in r.items():s[q+w]=s.get(q+w,F(0))+a*b
 return clean(s)
def inring(p):return const(p).denominator==1 and all(q>=0 for q in p)
def positive(p):return bool(p) and p[max(p)]>0
def nonstd(p):return bool(p) and max(p)>0
def greaterone(p):
 d=dict(p);d[F(0)]=d.get(F(0),F(0))-1;return positive(clean(d))
def even(p):return inring(scale(p,F(1,2)))

def main():
 cases=0;divchecks=0
 for e1,e2,lead,mid,c in it.product([F(1,2),F(1),F(3,2)],[F(0),F(1,4)],[F(1,3),F(1),F(7,2)],[F(-2),F(0),F(3,5)],range(-12,13)):
  p=clean({e1:lead,e2:mid,F(0):F(c)})
  check(inring(p));check(positive(p));check(nonstd(p))
  for n in range(1,15):check(inring(scale(p,F(1,n)))==(c%n==0));divchecks+=1
  if c==0:d={F(0):F(3)};r=scale(p,F(1,3))
  else:
   z=abs(c);e=0
   while z%2==0:z//=2;e+=1
   d=scale(p,F(1,2**e));r={F(0):F(2**e)}
  check(inring(d) and inring(r));check(positive(d) and positive(r));check(greaterone(d));check(not even(d));check(mul(d,r)==p);cases+=1
 for u in range(1,1001):
  oddless=all(d==1 or d%2==0 for d in range(1,u+1) if u%d==0)
  check(oddless==(u&(u-1)==0))
 check(mul({F(0):F(3)},{})=={})
 print(json.dumps({'problem_id':30005751,'turn':2,'status':'PASS','exact_assertions':N,'nonstandard_polynomial_divisor_certificates':cases,'standard_divisibility_checks':divchecks,'standard_oddless_checks':1000,'scope':'Finite rational-coefficient algebra controls inside a credited nonstandard model; not a finite IOpen-model or a solution of finite axiomatizability.'},indent=2))
if __name__=='__main__':main()
