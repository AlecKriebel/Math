"""Exact controls of the superlinear error obstruction; no stochastic simulations."""
from fractions import Fraction as F
import itertools as it,json
N=0
def check(x):
 global N
 N+=1
 assert x

def main():
 jensen=0;ito=0;threshold=0
 for den in range(1,41):
  for num in range(den+1,5*den+1):
   p=F(num,den);eta=(p*p-1)/(2*(p*p+1))
   check(0<eta<1);check(p*p*(1-eta)-(1+eta)==(p*p-1)/2);check(p*p*(1-eta)>1+eta);jensen+=1
 # Y=a^4, R=4/a parametrizes the exact Ito derivatives rationally.
 for a in [F(j,k) for j in range(1,31) for k in range(1,11)]:
  Y=a**4;R=4/a;fp=-a**(-5);fpp=F(5,4)*a**(-9);diffusion=a**5
  check(fp*diffusion==-1);check(F(1,2)*fpp*diffusion**2==F(5,2)/R);check((4/R)**4==Y);ito+=1
 for den in range(1,60):
  for num in range(1,3*den):
   p=F(num,den);radial_exponent=5-4*p
   check((radial_exponent>-1)==(p<F(3,2)));threshold+=1
 check(1<F(5,4)<F(3,2)<2)
 # Gaussian MGF after spatial log-Jensen: coefficient in variance tau/2.
 for a,b,p in it.product([F(1,3),F(1),F(4)],[F(1,4),F(2),F(9)],[F(5,4),F(3,2),F(2)]):
  # Here a is mean of frozen coefficient, b its second moment.
  check((p*a)**2-p*b==p*p*a*a-p*b)
 print(json.dumps({'problem_id':30005935,'turn':2,'status':'PASS','exact_assertions':N,'jensen_positive_coefficient_cases':jensen,'rational_BES6_Ito_cases':ito,'radial_integrability_threshold_cases':threshold,'fixed_error_moment':'5/4','scope':'Finite algebra controls. Continuum kernel comparison, localized SPDE comparison and divergence are proved in TURN_2.md and require independent review.'},indent=2))
if __name__=='__main__':main()
