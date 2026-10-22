"""Exact algebraic controls for the two-step moment obstruction; no Monte Carlo."""
from fractions import Fraction as F
import itertools as it,json
N=0
def check(x):
 global N
 N+=1
 assert x

def main():
 cross=0;maxima=0;tails=0;kernel=0
 vals=[F(a,b) for a in range(1,9) for b in range(1,6)]
 for a,b,t in it.product(vals,vals,[F(1,100),F(1,7),F(1),F(3)]):
  exponent=t*(a+b)**2/2-t*a*a/2-t*b*b/2
  check(exponent==t*a*b);check(exponent>0);cross+=1
 for a,t in it.product(vals,[F(1,1000),F(1,9),F(1),F(7)]):
  z=t*a-4/a
  check(4/a+z-t*a==0);check(-4/(a*a)-t<0);check(t*a*a-z*a-4==0);maxima+=1
 # exp(b*z/2)>=b^3*z^3/48, and at a threshold this dominates z²/tau.
 for b,D,t in it.product([F(1,10),F(1,2),F(1),F(3)],[F(1,100),F(1),F(5)],[F(1,100),F(1,2),F(1),F(4)]):
  threshold=48/(D*b**3*t)
  for multiplier in [1,2,5,10]:
   z=threshold*multiplier
   check(D*b**3*z**3/48>=z*z/t)
   check(2*b*z+D*b**3*z**3/48-z*z/(2*t)>=z*z/(2*t));tails+=1
 # Positive discrete-kernel cross coefficients. This is only an algebra control.
 for n in range(1,9):
  a=[F(j+1,n+1) for j in range(n)];V=[x**4 for x in a];w=[F(j+2,(n+1)*(n+2)) for j in range(n)]
  for j,k in it.product(range(n),repeat=2):
   check(w[j]*w[k]*V[j]*V[k]>0);check(a[j]*a[k]>=min(a)**2);kernel+=1
 print(json.dumps({'problem_id':30005935,'turn':1,'status':'PASS','exact_assertions':N,'gaussian_cross_exponent_cases':cross,'positive_maximum_stationarity_cases':maxima,'explicit_cubic_tail_lower_bounds':tails,'positive_kernel_cross_terms':kernel,'scope':'Exact finite algebra controls only. Infinite second moment and continuum positivity are established by the accompanying proof, not numerical integration.'},indent=2))
if __name__=='__main__':main()
