from fractions import Fraction as Q
import itertools,math,json
N=0
def ck(x):
 global N
 assert x;N+=1
# Record-path partition identity, enumerate all breakpoint subsets.
for m in range(11):
 for a in [Q(1,3),Q(2,3),Q(1),Q(3,2)]:
  v=sum((a**(k+1)*math.comb(m,k) for k in range(m+1)),Q(0));ck(v==a*(1+a)**m)
# Exchangeable Bernoulli sequences constructed by arbitrary two-point mixing.
for p,q,w in itertools.product([Q(0),Q(1,4),Q(1,2),Q(1)],repeat=3):
 a=w*p+(1-w)*q;b=w*p*p+(1-w)*q*q
 for n in range(1,9):
  e2=a/n+(1-Q(1,n))*b
  for m in [n,n+1,n+5]:
   cross=a/m+(1-Q(1,m))*b
   ck(e2-cross==(a-b)*(Q(1,n)-Q(1,m)))
  positive=w*(p>0)+(1-w)*(q>0)
  ck(b==0 or a*a/b<=positive)
# Dyadic intensity sum coefficients, removing the common pi*p*eta factor.
for j in range(40):ck((Q(1,4)**j-Q(1,4)**(j+1))*2**(j+1)==Q(3,2)*Q(1,2)**j)
for n in range(1,31):ck(sum((Q(3,2)*Q(1,2)**j for j in range(n)),Q(0))==3*(1-Q(1,2)**n))
# Mixture weights: exact truncated versions of cost and amplified output.
for n in range(1,16):
 costs=[Q((j+1)**3) for j in range(1,n+1)]
 Z=sum((Q(1,2**j)/costs[j-1] for j in range(1,n+1)),Q(0))
 weights=[Q(1,2**j)/(Z*costs[j-1]) for j in range(1,n+1)]
 ck(sum(weights)==1)
 ck(sum(weights[j-1]*costs[j-1] for j in range(1,n+1))==(1-Q(1,2**n))/Z)
 ck(sum(weights[j-1]*costs[j-1]*4**j for j in range(1,n+1))==(2**(n+1)-2)/Z)
# Exact scalar bounds used by the affine no-go argument.
for D in range(1,11):
 for denom in range(1,11):
  c=Q(D,denom);lam=8*D/c
  ck(2/lam==c/(4*D));ck(Q(3,4)*c-Q(2,1)/lam*D==c/2)
  ck(6/c<=8*D/c)
print(json.dumps({'status':'PASS','independent_assertions':N,'scope':'Exact record sums, exchangeable mixed-Bernoulli second moments, dyadic intensity constants, mixture weights and affine lower-bound algebra. Infinite-network and analytic implications audited separately.'},indent=2))
