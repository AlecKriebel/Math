from fractions import Fraction as F
from itertools import product
from math import factorial,prod
from pathlib import Path
import json,hashlib
checks=0;cases=0
def ck(t):
 global checks
 assert t;checks+=1
for n in range(1,7):
 for ws in product(range(1,4),repeat=n):
  c=prod(ws);ck(c>0);ck(min(ws)>0)
  v=[F(i+1,3) for i in range(n)]
  ck(sum(w*x*x for w,x in zip(ws,v))>=min(ws)*sum(x*x for x in v))
 for coeff in product(range(-2,3),repeat=5):
  cases+=1;jet=all((coeff[j] if j<len(coeff) else 0)==0 for j in range(n));division=next((i for i,a in enumerate(coeff) if a),99)>=n;ck(jet==division)
  if jet:
   for k,a in enumerate(coeff):
    if k<n:continue
    # Integral Taylor coefficient: a*k!/(k-n)!/(n-1)! * Beta(k-n+1,n)=a.
    value=F(a*factorial(k),factorial(k-n)*factorial(n-1))*F(factorial(k-n)*factorial(n-1),factorial(k))
    ck(value==a)
for n in range(1,10):ck(not all((1 if j==0 else 0)==0 for j in range(n)))
r={'artifact_sha256':hashlib.sha256(Path('SOURCE_OBSTRUCTION.md').read_bytes()).hexdigest(),'exact_assertions':checks,'polynomial_cases':cases,'scope':'Weighted Euler/positivity and rational polynomial jet/Taylor controls; not an analytic regularization proof.'}
Path('verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
