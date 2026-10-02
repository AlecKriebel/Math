"""Exact controls for scaling automorphisms and the definability obstruction."""
from fractions import Fraction as F
import itertools as it,json,random
from verify_turn2 import clean,mul,positive,inring
N=0
def check(x):
 global N
 N+=1
 assert x

def add(p,r):
 s=dict(p)
 for q,a in r.items():s[q]=s.get(q,F(0))+a
 return clean(s)
def sub(p,r):return add(p,{q:-a for q,a in r.items()})
def scale_sigma(p,b,d):
 out={}
 for q,a in p.items():
  e=q*d;assert e.denominator==1
  out[q]=a*b**e.numerator
 return clean(out)

def main():
 rng=random.Random(300057514);polys=0;comparisons=0;primechecks=0
 for d in range(1,13):
  b=1+F(1,4*d);A=b**d;check(1<A<2)
  for rep in range(80):
   p={F(j,d):F(rng.randrange(-9,10),rng.randrange(1,5)) for j in range(1,d)};p[F(0)]=F(rng.randrange(-10,11));p[F(1)]=F(2,3);p=clean(p)
   r={F(j,d):F(rng.randrange(-6,7),rng.randrange(1,5)) for j in range(1,d)};r[F(0)]=F(rng.randrange(-10,11));r[F(1)]=F(3,4);r=clean(r)
   sp=scale_sigma(p,b,d);sr=scale_sigma(r,b,d)
   check(inring(sp));check(scale_sigma(sp,1/b,d)==p)
   check(scale_sigma(add(p,r),b,d)==add(sp,sr));check(scale_sigma(mul(p,r),b,d)==mul(sp,sr));polys+=1
   check(positive(sub(sp,p)));check(positive(sub({q:2*a for q,a in p.items()},sp)));comparisons+=1
 # Clearing rational exponents reduces any possible nonstandard intersection
 # of P_p and P_q to ordinary prime powers. Check bounded positive exponents.
 for p,q in it.combinations([3,5,7,11,13],2):
  for m in range(1,25):
   for k in range(-20,21):
    check(F(p,q)**m!=F(2)**k);primechecks+=1
 print(json.dumps({'problem_id':30005751,'turn':4,'status':'PASS','exact_assertions':N,'polynomial_automorphism_cases':polys,'strict_degree_one_intervals':comparisons,'prime_power_disjointness_controls':primechecks,'scope':'Finite algebra controls only. Automorphism invariance and the no-definable-predicate theorem are proved in TURN_4.md.'},indent=2))
if __name__=='__main__':main()
