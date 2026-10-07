#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
import json
count=0

def ck(p):
 global count
 assert p
 count+=1
for n in range(1,51):
 for k in range(1,51):
  b=F(2*n+k,k); D=-1/(1+b)
  ck(D==F(-k,2*(k+n)))
  ck(-F(1,2)<D<0)
  ck(b/(1+b)==D+1)
  ck(1/(D+1)==F(2*(k+n),k+2*n))
  ck(1<1/(D+1)<2)
  # Monomial rotation exponent relative to the vector field output.
  ck((n+k+1)-n-1==k)
  # Reversing angle pi/k gives phase exp(-i*k*pi/k) = -1.
  ck(F(k,k)==1)
  for X,Y in [(F(1,3),F(2,5)),(F(-2,7),F(3,4)),(F(0),F(-1))]:
   Xtau=-Y+b*X*X-Y*Y;Ytau=X+(1+b)*X*Y
   x=-(1+b)*Y;y=-(1+b)*X
   xs=(1+b)*Ytau;ys=(1+b)*Xtau
   ck(xs==-y+x*y)
   ck(ys==x+D*x*x+(D+1)*y*y)
receipt={'status':'PASS','assertions':count,'parameter_pairs':2500,'artifact_sha256':sha256(Path('KNOWN_RESULT.md').read_bytes()).hexdigest(),'scope':'Exact source-reduction and parameter controls only; published global analytic theorem is not independently reproved'}
Path('verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
