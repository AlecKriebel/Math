from fractions import Fraction as Q
from pathlib import Path
import json,hashlib
n=0
for r in [Q(1,3),Q(1),Q(7),Q(100)]:
 for a,b in [(Q(1),Q(2)),(Q(2,3),Q(9,4))]:
  for d in [Q(-3),Q(0),Q(2),Q(1,5)]:
   minus=2*r*(a+b)*d;plus=-2*r*(a+b)*d
   assert minus == -plus;n+=1
   assert not (minus<0 and plus<0);n+=1
   if d>0: assert minus>0;n+=1
# Algebra of log I2 over three constant-coefficient intervals.
for a in range(-3,4):
 for b in range(-3,4):
  segments=[(Q(a),Q(1,2)),(Q(b),Q(3,4)),(Q(a-b),Q(2))]
  exponent=sum(-2*x*t for x,t in segments)
  assert exponent == -Q(a)-Q(3,2)*b-4*(a-b);n+=1
result={'assertions':n,'all_pass':True,'artifact_sha256':hashlib.sha256(Path('PARTIAL_RESULT.md').read_bytes()).hexdigest(),'scope':'Exact scalar drift and integrating-factor algebra only; no stochastic existence verification.'}
Path('verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
