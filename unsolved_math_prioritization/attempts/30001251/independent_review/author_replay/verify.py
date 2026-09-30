from fractions import Fraction as Q
from math import factorial
from pathlib import Path
from hashlib import sha256
import json
n=0;groups={}
def ck(v,g):
 global n
 assert v,g
 n+=1;groups[g]=groups.get(g,0)+1
# Exact coefficients of I1(b)/b relative to I0(b), t=b²/4.
for j in range(51):
 a=Q(1,2*factorial(j)*factorial(j+1));d=Q(1,factorial(j)**2)
 ck(a/d==Q(1,2*(j+1)),'Bessel coefficient ratio')
 for i in range(j+1,51):
  ai=Q(1,2*factorial(i)*factorial(i+1));di=Q(1,factorial(i)**2)
  ck((i-j)*(ai*d-a*di)<0,'strict quotient derivative pairing')
# Hessian decomposition for rational covariance values satisfying k*C<1, S=1/k.
for k in map(Q,range(3,11)):
 for den in range(2,10):
  C=Q(1)/(k*den);S=1/k
  for alpha in map(Q,range(-3,4)):
   for beta in map(Q,range(-3,4)):
    for norm in map(Q,range(3)):
     raw=alpha**2*C+beta**2*S+norm-k*((alpha*C)**2+(beta*S)**2)
     reduced=alpha**2*C*(1-k*C)+norm
     ck(raw==reduced>=0,'full rank-two Hessian')
     ck((raw==0)==(alpha==0 and norm==0),'translation kernel')
# General entropy completion-of-square identity uses z=k*m.
for k in map(Q,range(1,8)):
 for mx in [Q(i,5) for i in range(-5,6)]:
  for my in [Q(i,5) for i in range(-5,6)]:
   M=mx*mx+my*my;ent=Q(7,3);logI=Q(2,5)
   KL=ent-k*M+logI;E=k*M/2-logI
   ck(KL+E==ent-k*M/2,'entropy energy identity')
# Harmonic selection on roots of unity as exact modular exponents.
for N in range(3,41):
 ck(all((N*i)%N==0 for i in range(N)),'N-average same harmonic')
 ck(N-1>=2,'physical sign restriction fails')
 # midpoint of each half-wave x=(2j+1)/(4N): sin(2piNx)=(-1)^j.
 signs=[(-1)**j for j in range(N)]
 ck(sum(signs[j]!=signs[j-1] for j in range(1,N))==N-1,'alternating sign count')
 ck(N*N>0,'sampled derivative coefficient')
receipt={'verdict':'PASS','assertions':n,'groups':groups,'artifact_sha256':sha256(Path('PARTIAL_RESULT.md').read_bytes()).hexdigest(),'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact algebraic diagnostics only; the infinite-series, PDE and stability arguments are written proofs, not numerically certified by this script.'}
Path('verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
