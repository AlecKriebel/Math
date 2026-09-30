#!/usr/bin/env python3
from pathlib import Path
from tempfile import TemporaryDirectory
from copy import deepcopy
from contextlib import redirect_stdout
from io import StringIO
import json
import independent_cover as C
root=Path(__file__).resolve().parent
base=json.loads((root/'certificates/two.json').read_text());cases=[]
def add(name,fun):
 d=deepcopy(base);fun(d);cases.append((name,d))
add('missing leaf',lambda d:d['leaves'].pop())
add('duplicate leaf',lambda d:d['leaves'].append(deepcopy(d['leaves'][0])))
add('orphan record',lambda d:d['leaves'].append({'path':'9:','witness':deepcopy(d['leaves'][0]['witness'])}))
add('degenerate split',lambda d:d['splits'][0].update(edge=[0,0]))
add('invalid endpoint',lambda d:d['splits'][0].update(edge=[0,2]))
add('negative parameter',lambda d:d['leaves'][0]['witness']['numerators'].__setitem__(0,-1))
add('wrong format',lambda d:d.update(format='bad'))
add('wrong support',lambda d:d.update(support=[0,1]))
add('zero support witness',lambda d:d['leaves'][0]['witness'].update(numerators=[0]*7))
with TemporaryDirectory() as tmp:
 for name,d in cases:
  p=Path(tmp)/'case.json';p.write_text(json.dumps(d))
  try:
   with redirect_stdout(StringIO()):C.certificate(p,(0,7))
  except (AssertionError,ValueError,TypeError,KeyError):pass
  else:raise AssertionError('accepted '+name)
res={'verdict':'PASS','malformed_certificates_rejected':len(cases),'cases':[x[0] for x in cases]}
(root/'rejection_results.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res))
