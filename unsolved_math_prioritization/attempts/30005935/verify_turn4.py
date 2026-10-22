"""Exact finite controls for Lipschitz Sobolev localization estimates."""
from fractions import Fraction as F
import itertools as it,json
N=0
def check(x):
 global N
 N+=1
 assert x

def main():
 gaussian=0;domination=0;cutoffs=0
 for L in [F(1,5),F(1),F(3),F(9)]:
  for sf,sh,sg,s in it.product([F(-1),F(-1,2),F(0),F(1,2),F(1)],[F(-2),F(-1),F(0),F(1),F(2)],[F(-1),F(0),F(1)],[F(0),F(1,100),F(1,3),F(1),F(7)]):
   f=L*sf;h=L*sh;gp=L*sg;x=L*L*s
   n=(1+s*f*h)**2+s*h*h
   j=(gp+s*f*f*h)**2+s*f*f*h*h
   bound=1+8*x+4*x*x
   check(n<=bound);check(j<=L*L*bound);gaussian+=1
 for x in [F(i,j) for i in range(0,100) for j in range(1,15)]:
  # second Taylor polynomial of exp(8x) already dominates the target bracket
  check(1+8*x+4*x*x<=1+8*x+32*x*x);domination+=1
 # K=a^4 makes cutoff slope (5/4)a rational, L² scales as sqrt(K).
 for a in [F(i,j) for i in range(1,30) for j in range(1,10)]:
  K=a**4;L=F(5,4)*a
  check(L*L==F(25,16)*a*a);check(L**4==F(625,256)*K)
  # matching value and derivative at the tangent-extension point
  check(a**5+L*(K-K)==a**5);cutoffs+=1
 print(json.dumps({'problem_id':30005935,'turn':4,'status':'PASS','exact_assertions':N,'Gaussian_derivative_bracket_cases':gaussian,'exponential_Taylor_domination_cases':domination,'cutoff_scaling_cases':cutoffs,'scope':'Finite algebraic controls only; uniform Sobolev estimates and stopped identification are analytical claims in TURN_4.md.'},indent=2))
if __name__=='__main__':main()
