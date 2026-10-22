"""Exact finite controls for the Hahn construction barriers."""
from fractions import Fraction as F
import json
N=0
def check(x):
 global N
 N+=1
 assert x

def main():
 b=[F(1)]
 for n in range(101):b.append(b[-1]*(F(1,2)-n)/(n+1));check(b[-1]!=0)
 coeffs=0
 for n in range(102):
  c=sum(b[k]*b[n-k] for k in range(n+1));check(c==(1 if n in (0,1) else 0));coeffs+=1
 errors=0
 for m in range(0,100):
  k=m+1;c=sum(b[i]*b[k-i] for i in range(k+1) if i<=m and k-i<=m)
  # Subtract the radicand coefficient for the m=0 case as well.
  error=c-(1 if k==1 else 0)
  check(error==-2*b[m+1]);check(error!=0);check((-2,k)<(0,0));errors+=1
 for n in range(10001):check((-1,n)<(0,0));check((-1,n)<(-1,n+1))
 floors=0
 for den in range(1,40):
  for num in range(-2*den,2*den+1):
   c=F(num,den);n=c.numerator//c.denominator;theta=c-n
   scale=min(theta,1-theta) if theta else F(1)
   for eps in [-scale/4,F(0),scale/4]:
    p=n-1 if theta==0 and eps<0 else n
    check(p<=c+eps<p+1);floors+=1
 print(json.dumps({'problem_id':30005751,'turn':3,'status':'PASS','exact_assertions':N,'binomial_square_coefficients':coeffs,'finite_prefix_infinite_valuation_errors':errors,'lexicographic_exponents_checked':10001,'floor_boundary_controls':floors,'scope':'Finite formal algebra only. Hahn real closedness is credited; the all-series model and base-theory obstruction are proved in the text.'},indent=2))
if __name__=='__main__':main()
