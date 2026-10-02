"""Exact exponent bookkeeping for the final bounded-test weak rate."""
from fractions import Fraction as F
import itertools as it,json
N=0
def check(x):
 global N
 N+=1
 assert x

def main():
 exponents=0;cutoffs=0;poly=0
 for c in [F(i,j) for i in range(1,30) for j in range(1,20)]:
  root_kappa=1/(8*c);kappa=root_kappa**2
  check(c*root_kappa==F(1,8));check(kappa>0);cutoffs+=1
  growth=c*root_kappa
  check(F(1,2)-growth==F(3,8));check(F(1,4)-growth/2==F(3,16));exponents+=1
 for ell in [F(i,j) for j in range(1,20) for i in range(j,100)]:
  check((1+ell*ell)/ell**4<=2/ell**2)
  check(1+ell<=2*ell);poly+=1
 # Max of ell^3 exp(-a ell) occurs at ell=3/a; sign of log derivative.
 a=F(3,16);point=3/a;check(point==16)
 for ell in range(1,101):check((3/F(ell)-a>=0)==(ell<=16))
 # Explicit cutoff coefficient equality at frozen inputs, independent of substep size.
 for a,b,t in it.product(range(1,11),range(1,11),[F(1,10),F(1),F(3)]):
  v=F(a)**4;K=F(b)**4;gK=F(a)**5 if a<=b else F(b)**5+F(5,4)*b*(v-K)
  if a<=b:
   fK=gK/v;check(fK==a);check(-t*fK*fK/2==-t*a*a/2)
 print(json.dumps({'problem_id':30005935,'turn':5,'status':'PASS','exact_assertions':N,'cutoff_constant_cases':cutoffs,'weak_exponent_cases':exponents,'logarithmic_polynomial_controls':poly,'bounded_test_rate':'O((log(e M))^-2) in dimension one','scope':'Finite algebraic bookkeeping only. The probability localization and analytic cutoff bounds are proved in the turn notes and require independent review.'},indent=2))
if __name__=='__main__':main()
