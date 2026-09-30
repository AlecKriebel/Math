from fractions import Fraction as F
from itertools import product
from math import factorial
from pathlib import Path
import json,hashlib
n=0; groups={}
def ck(v,g):
 global n
 assert v,g
 n+=1;groups[g]=groups.get(g,0)+1
# Independent discrete conditional decision laws, including zero weights and atoms.
xs=[F(-2),F(0),F(1),F(5)]
for ws in product(range(4),repeat=4):
 if not sum(ws):continue
 ps=[F(w,sum(ws)) for w in ws]
 risks=[sum(p*abs(x-z) for p,x in zip(ps,xs)) for z in xs]
 best=min(risks);mean=sum(p*x for p,x in zip(ps,xs))
 pair=sum(ps[i]*ps[j]*abs(xs[i]-xs[j]) for i in range(4) for j in range(4))
 ck(pair/2<=best<=sum(p*abs(x-mean) for p,x in zip(ps,xs))<=pair,'decision sandwich')
 for z in [F(k,3) for k in range(-9,19)]:ck(best<=sum(p*abs(x-z) for p,x in zip(ps,xs)),'global piecewise linear median')
 # Uniform quantile representation: median minimizer checked through cumulative mass.
 for j,z in enumerate(xs):
  if sum(ps[:j])<=F(1,2) and sum(ps[j+1:])<=F(1,2):ck(risks[j]==best,'all median atoms')
# Independent rational Gaussian regression: Gram determinant identity on polynomial integrands.
for deg in range(1,6):
 for coeff in product(range(-2,3),repeat=2):
  if coeff[1]==0:continue
  # f(t)=a+b*t^deg on [0,h], conditional on endpoint.
  a,b=map(F,coeff)
  for h in map(F,range(1,6)):
   first=a*h+b*h**(deg+1)/(deg+1)
   second=a*a*h+2*a*b*h**(deg+1)/(deg+1)+b*b*h**(2*deg+1)/(2*deg+1)
   variance=second-first*first/h
   ck(variance==b*b*h**(2*deg+1)*F(deg*deg,(2*deg+1)*(deg+1)**2)>0,'projection residual')
# Exponential weight expansion from double covariance integral, independent of closed form.
# Var integral f dW = 1/(2h) integral integral (f(s)-f(t))^2 ds dt.
for order in range(2,11):
 coeff=F(0)
 for i in range(1,order):
  j=order-i
  coeff+=F(1,2**order*factorial(i)*factorial(j))*(F(1,order+1)-F(1,(i+1)*(j+1)))
 # direct expansion of (exp(h)-1)-4(exp(h/2)-1)^2/h
 direct=F(1,factorial(order+1))-4*sum((F(1,2**(order+2)*factorial(i)*factorial(order+2-i)) for i in range(1,order+2)),F(0))
 ck(coeff==direct,'independent exponential variance coefficients')
 if order==2:ck(coeff==F(1,48),'leading covariance coefficient')
# Reflection exponent and transformed-square support, rational arbitrary partitions.
for y,z,l in product(range(-3,4),range(-3,4),range(7)):
 if min(y,z)+l<0:continue
 ck((z+y+2*l)**2-(z-y)**2==4*(y+l)*(z+l),'reflection exponent')
 ck(z+l>=0,'square monotonicity support')
# One-bridge quantile relation: choose rational positive q and c with q(c+q)>0;
# k=4q(c+q), so sqrt(c²+k)=c+2q.
for q in [F(i,3) for i in range(1,16)]:
 for c in [F(i,2) for i in range(-8,9)]:
  if c+q<=0:continue
  k=4*q*(c+q)
  ck(c*c+k==(c+2*q)**2,'one bridge quantile')
  ck(c+2*q>0 and (c+q)**2>=0,'positive root branch')
result={'verdict':'PASS','assertions':n,'groups':groups,'scope':'Finite exact supporting controls, not CIR rate estimates or stochastic simulation.','checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path('independent_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
