"""Exact algebraic controls for the weighted first-moment obstruction."""
from fractions import Fraction as F
import itertools as it,json
N=0
def check(x):
 global N
 N+=1
 assert x

def main():
 substitutions=0;cev=0;loss=0
 for t,q in it.product([F(i,j) for i in range(1,10) for j in range(1,8)],[F(i,j) for i in range(1,13) for j in range(1,9)]):
  h=q/(1+2*t*q);jac=(1-2*t*h)**(-2)
  check(0<h<1/(2*t));check(q==h/(1-2*t*h));check(q*(1+2*t*q)**(-3)*jac==h);substitutions+=1
 for a in [F(i,j) for i in range(1,30) for j in range(1,15)]:
  v=a**4;r=4/a
  check(4**4/r**4==v)
  for t in [F(1,10),F(1),F(7)]:
   check(r*r/(2*t)==8/(t*a*a));cev+=1
 # e^b >= 1+b+b²/2 implies 0<(1+b)e^-b<1.
 for b in [F(i,j) for i in range(1,100) for j in range(1,12)]:
  check(0<(1+b)/(1+b+b*b/2)<1);loss+=1
 # The clock exponent is twice alpha=1/2 for alpha=1/4.
 check(2*F(1,4)==F(1,2));check(2*F(5,2)+1==6)
 print(json.dumps({'problem_id':30005935,'turn':3,'status':'PASS','exact_assertions':N,'Laplace_substitution_cases':substitutions,'CEV_scale_cases':cev,'strict_mean_loss_controls':loss,'scope':'Exact algebra only; time-change, optional sampling and weighted-SPDE testing are justified in TURN_3.md and require independent review.'},indent=2))
if __name__=='__main__':main()
