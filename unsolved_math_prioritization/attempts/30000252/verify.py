from fractions import Fraction as F
from pathlib import Path
import hashlib,json
count=0
for m in range(1,21):
 for n in range(2*m+1,10*m+1):
  p=F(n+2*m,n-2*m);a=1/(p-1)
  assert a+1-a*p==0;count+=1
  assert a+1==p/(p-1);count+=1
  assert p>=2 if n<=6*m else p<2;count+=1
  assert p/(p-1)==F(n+2*m,4*m);count+=1
  assert (p-1)/p==F(4*m,n+2*m);count+=1
assert F(7+6,7-6)==13;count+=1
assert (-1)**3==-1;count+=1
assert F(1,13-1)==F(1,12);count+=1
here=Path(__file__).resolve().parent
r={'status':'PASS','exact_assertions':count,'artifact_sha256':hashlib.sha256((here/'KNOWN_RESULT.md').read_bytes()).hexdigest(),'limitation':'Only rational scaling and admissible-exponent controls. No numerical PDE solution or independent proof of the cited multiplicity/regularity theorem.'}
(here/'verification.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
