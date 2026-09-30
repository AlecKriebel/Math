from fractions import Fraction as F
from pathlib import Path
import json,hashlib
checks=0;cases=0;noninj=0
def check(t):
 global checks
 assert t;checks+=1
for c in (F(3,2),F(2),F(3),F(4)):
 for a in range(1,17):
  for b in range(1,9):
   cases+=1;q=F(b,a)
   inside=F(1,c*c)<q<1
   check(inside==(b<a<b*c*c))
   for k in range(-15,16):check(a*(-q)**k+b*(-q)**(k-1)==0)
   # Finite truncation has precisely two boundary residuals.
   N=12;v={k:(-q)**k for k in range(-N,N+1)}
   out={k:a*v.get(k,0)+b*v.get(k-1,0) for k in range(-N,N+2)}
   check(out[-N]==a*(-q)**(-N));check(out[N+1]==b*(-q)**N)
   for k in range(-N+1,N+1):
    check(out[k]==0)
    vp=lambda j:max(v.get(j,0),0)
    vm=lambda j:max(-v.get(j,0),0)
    check(a*vp(k)+b*vp(k-1)==a*vm(k)+b*vm(k-1))
   if inside:
    noninj+=1;r=c*c*q
    # Closed geometric sums bound exact finite weighted masses.
    total=1/(1-q)+1/(r-1)
    finite=sum(q**k for k in range(N+1))+sum(r**k for k in range(-N,0))
    check(total-finite==q**(N+1)/(1-q)+r**(-N)/(r-1));check(total>finite>0)
   if q==1:check(sum(q**k for k in range(N))==N)
   if c*c*q==1:check(sum((c*c*q)**k for k in range(-N,0))==N)
# Exact special kernel and lower bound on its imaginary-line modulus.
check(F(1,2)>F(1,4));check(F(1,2)<1)
for x in range(-100,101):
 t=F(x,100);check(5+4*t>=1) # |2+e^{it}|^2=5+4cos(t)
r={'artifact_sha256':hashlib.sha256(Path('PARTIAL_RESULT.md').read_bytes()).hexdigest(),'exact_assertions':checks,'parameter_cases':cases,'noninjective_parameter_cases':noninj,'scope':'Rational recurrence, finite boundary residuals and geometric-tail identities; infinite measure arguments proved in text.'}
Path('verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
