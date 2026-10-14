from pathlib import Path
from tempfile import TemporaryDirectory
from fractions import Fraction as F
from copy import deepcopy
import json,contextlib,io,sys
import check_cover as C
checks=0
# An independent alternating-series enclosure for log(1+x), x in (0,1).
for den in range(3,35):
 for num in range(1,den//2+1):
  x=F(num,den);s=F(0)
  for k in range(1,151):s+=(-1)**(k+1)*x**k/k
  lo,hi=C.logbound(1+x);nextterm=x**151/151
  assert F(lo,C.S)<=s+nextterm and F(hi,C.S)>=s;checks+=1
# Exact channel reversal controls over every positive integer table of small range.
from itertools import product
for values in product(range(1,3),repeat=8):
 p=[F(v,sum(values)) for v in values]
 for bit in [1,2,4]:
  s0=[i for i in range(8) if not i&bit];tau=min(p[x^bit]/p[x] for x in s0);r=p.copy()
  for x in s0:r[x]=(1+tau)*p[x];r[x^bit]=p[x^bit]-tau*p[x]
  assert min(r)>=0 and sum(r)==1 and sum(x>0 for x in r)<8;checks+=1
  for x in s0:
   assert r[x]/(1+tau)==p[x] and r[x^bit]+tau*r[x]/(1+tau)==p[x^bit];checks+=1
# Explicit certificate rejection controls, without running any producer code.
source=Path(sys.argv[1]);base=json.loads((source/'two.json').read_text());bad=[]
d=deepcopy(base);d['leaves'].pop();bad.append(d)
d=deepcopy(base);d['splits'][0]['edge']=[0,0];bad.append(d)
d=deepcopy(base);d['leaves'][0]['witness']['numerators'][0]=-1;bad.append(d)
d=deepcopy(base);d['leaves'].append(deepcopy(d['leaves'][0]));bad.append(d)
d=deepcopy(base);d['leaves'][0]['path']='9:orphan';bad.append(d)
d=deepcopy(base);d['format']='wrong';bad.append(d)
d=deepcopy(base);d['leaves'][0]['witness']['numerators']=[0]*7;bad.append(d)
with TemporaryDirectory() as tmp:
 for i,d in enumerate(bad):
  f=Path(tmp)/str(i);f.write_text(json.dumps(d))
  try:
   with contextlib.redirect_stdout(io.StringIO()):C.runfile(f)
  except (ValueError,KeyError,TypeError):checks+=1
  else:raise AssertionError('malformed certificate accepted')
result={'verdict':'PASS','controls':checks,'malformed_certificates_rejected':len(bad),'producer_code_executed':False}
Path('independent_test_results.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
