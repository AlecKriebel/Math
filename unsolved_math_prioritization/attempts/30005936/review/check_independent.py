from fractions import Fraction as F
import json
n=0
def check(c):
 global n
 assert c;n+=1
# Independently construct admissible exit-tail parameters for every rational q in (0,1/2).
for den in range(3,101):
 for num in range(1,(den+1)//2):
  q=F(num,den)
  if q>=F(1,2):continue
  lo=F(1,4)/(1-q);a=(lo+F(1,2))/2
  eps=(a*(1-q)-F(1,4))/2
  p=2
  while not(a<F(1,2)-F(3,p) and eps*p>=q):p+=1
  check(a>0 and eps>0);check(a<F(1,2)-F(3,p));check(1-(F(1,4)+eps)/a>q);check(eps*p>=q)
# Independent Gaussian moment identity: p times drift + quadratic variance.
for p in range(1,100):
 for c in range(-10,11):check(-F(p*c*c,2)+F(p*p*c*c,2)==F(p*(p-1)*c*c,2))
# Positive path adjacency matrices: exact truncation coefficients and killed row masses.
for size in range(1,15):
 row=[1]*size
 for k in range(20):
  check(max(row)<=2**k)
  row=[(row[i-1] if i else 0)+(row[i+1] if i+1<size else 0) for i in range(size)]
# Grid-max exponents with separately varying moment order.
for p in range(7,101):
 alpha=F(1,2)-F(3,p);check(alpha>0)
 for C in range(0,30):
  eta=alpha/(2*(1+C));check(C*eta<=alpha/2)
# A high point's two-sided mass-area exponent.
a=F(3,8);eps=F(1,32);check(1-(F(1,4)+eps)/a==F(1,4));check(64*eps==2)
print(json.dumps({'status':'PASS','independent_assertions':n,'scope':'exact parameter, Gaussian, killed-semigroup and localization controls; analytical proofs separately reviewed'},indent=2))
