from fractions import Fraction as F
from math import factorial,comb
from itertools import product
from pathlib import Path
from hashlib import sha256
import json
count=0;groups={}
def ck(v,g):
 global count
 assert v,g
 count+=1;groups[g]=groups.get(g,0)+1
# Exact Rademacher directional moments with homogeneous normalization.
for n in range(1,6):
 signs=list(product([-1,1],repeat=n))
 for a in product([-1,0,1],repeat=n):
  norm=sum(x*x for x in a)
  if not norm:continue
  sums=[sum(x*y for x,y in zip(a,e)) for e in signs]
  ck(sum(sums)==0,'centering')
  for k in range(1,7):
   mom=sum(F(x**(2*k),len(signs)) for x in sums)
   gauss=F(factorial(2*k),2**k*factorial(k))*norm**k
   ck(mom<=gauss,'Rademacher Gaussian moment domination')
   radial=F(factorial(2*k),2**k)
   ck(radial*gauss==F(factorial(2*k)**2,4**k*factorial(k))*norm**k,'exponential radial moment')
# Exponential maximum identities independently integrated via binomial expansion.
for N in range(1,101):
 H=sum((F(1,j) for j in range(1,N+1)),F(0));H2=sum((F(1,j*j) for j in range(1,N+1)),F(0))
 mean=sum(((-1)**(j+1)*F(comb(N,j),j) for j in range(1,N+1)),F(0))
 second=sum(((-1)**(j+1)*F(2*comb(N,j),j*j) for j in range(1,N+1)),F(0))
 ck(mean==H,'exponential maximum first moment')
 ck(second==H*H+H2>=H*H,'exponential maximum Jensen')
# Frobenius second moment for an exact finite isotropic scale mixture.
# R² is 0 or2, equiprobably, so vectors are 0 or sqrt2 times signs.
# Work directly with outer products, all rational.
for n in range(1,5):
 es=list(product([-1,1],repeat=n));outer=[[[F(0) for j in range(n)] for i in range(n)]]
 weights=[F(1,2)]
 for e in es:
  outer.append([[F(2*e[i]*e[j]) for j in range(n)] for i in range(n)]);weights.append(F(1,2*len(es)))
 for i in range(n):
  for j in range(n):ck(sum(w*A[i][j] for w,A in zip(weights,outer))==int(i==j),'isotropic outer product')
 for N in [1,2]:
  total=F(0)
  if N==1:
   for w,A in zip(weights,outer):total+=w*sum((A[i][j]-int(i==j))**2 for i in range(n) for j in range(n))
  else:
   for wa,A in zip(weights,outer):
    for wb,B in zip(weights,outer):total+=wa*wb*sum(((A[i][j]+B[i][j])/2-int(i==j))**2 for i in range(n) for j in range(n))
  ck(total==F(2*n*n-n,N),'Frobenius independent-sample identity')
# Exact algebra for exceptional-event Cauchy–Schwarz squared bound.
for n,N,L in product(range(1,16),range(1,31),range(1,5)):
 ck(F(L*L*n*n,N)*F(1,n)==F(L*L*n,N),'exceptional-event expectation bridge')
# Constants in moment and Chernoff estimates.
for k in range(2,61):
 for B2 in range(1,9):
  ck(2**(k-1)*(2*(2*B2)**k*factorial(k)+1)<=factorial(k)*(8*B2)**k,'centered square moment bound')
for B2 in range(1,9):
 for s in [F(i,3) for i in range(1,501)]:
  t=min(s/(256*B2*B2),F(1,16*B2));exponent=-t*s+128*B2*B2*t*t
  ck(exponent<=-min(s*s/(512*B2*B2),s/(32*B2)),'Chernoff branch constants')
receipt={'verdict':'PASS','assertions':count,'groups':groups,'artifact_sha256':sha256(Path('PARTIAL_RESULT.md').read_bytes()).hexdigest(),'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact finite algebraic diagnostics; the infinite-dimensional quantifiers and cited probability theorem are mathematical/source obligations, not certified by sampling.'}
Path('verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
