from fractions import Fraction as F
from math import comb,factorial
import json
n=0
def ck(x):
 global n
 assert x;n+=1
def gauss(k):return 0 if k%2 else factorial(k)//(2**(k//2)*factorial(k//2))
# Separate rational scalar mixed-moment comparison, including negative odd moments.
for den in range(1,18):
 for num in range(1,den+1):
  p=F(num,den)
  for a in range(0,13,2):
   for b in range(0,10):
    if not a and not b:continue
    x=p*(1-p)**b if a else p*(1-p)**b+(1-p)*(-p)**b
    g=sum(comb(b,j)*(-1)**(b-j)*gauss(a+2*j) for j in range(b+1))
    ck(abs(x)<=p*g)
# Bounds in the parameter argument after sqrt2<3/2.
ck(F(7,70000)==F(1,10000));ck(10*(F(1,100)+F(1,10000))<F(1,3))
for q in range(2,102,2):
 # Gaussian moment proof's two gamma inequalities for even q.
 ck(2**(q+1)*q*factorial(q-1)<=(2*q)**q)
 ck((2**(q//2)*q*factorial(q//2-1))**2<=4**q*q**q)
print(json.dumps({'status':'PASS','independent_exact_assertions':n},indent=2))
