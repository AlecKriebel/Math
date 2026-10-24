#!/usr/bin/env python3
from fractions import Fraction as F
from math import comb
from pathlib import Path
from datetime import datetime,timezone
import json

def mul(a,b):
 out=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i+j]+=x*y
 return out

def run():
 cases=[]
 for m in range(1,31):
  f=[F(1),-2+F(1,m),F(1)];first=None
  for n in range(4*m-2):
   v=mul(f,[F(comb(n,k)) for k in range(n+1)])
   if min(v)>=0:first=n;break
  assert first==4*m-3
  # Verify the exact normalized falling-factorial formula at every coefficient.
  n=first;M=n+2;v=mul(f,[F(comb(n,k)) for k in range(n+1)])
  for k,c in enumerate(v):
   rhs=F(k*(k-1)+(M-k)*(M-k-1),M*(M-1))+f[1]*F(k*(M-k),M*(M-1))
   assert c/F(comb(M,k))==rhs
  cases.append({'m':m,'first_nonnegative_exponent':first,'zero_coefficients':sum(c==0 for c in v)})
 return {'utc':datetime.now(timezone.utc).isoformat(),'result':'PASS_EXACT_SMOOTHING_FAMILY','cases':cases,'scope':'Finite arithmetic tests of an explicit family; the general height-smoothing lemma is established by the separate uniform-coefficient proof.'}
if __name__=='__main__':
 out=run();Path(__file__).with_name('height_smoothing_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
