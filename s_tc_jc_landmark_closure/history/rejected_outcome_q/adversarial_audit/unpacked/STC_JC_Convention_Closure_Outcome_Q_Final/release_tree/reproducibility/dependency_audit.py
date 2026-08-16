#!/usr/bin/env python3
from pathlib import Path
import ast,hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
allowed={'__future__','ast','collections','dataclasses','fractions','functools','hashlib','itertools','json','math','pathlib','queue','re','subprocess','sys','tempfile','copy','sympy'}
records=[]
for p in sorted(list((ROOT/'src').glob('*.py'))+list((ROOT/'review').glob('*.py'))+list((ROOT/'reproducibility').glob('*.py'))):
 tree=ast.parse(p.read_text(),filename=str(p));imports=set()
 for n in ast.walk(tree):
  if isinstance(n,ast.Import):imports|={x.name.split('.')[0] for x in n.names}
  elif isinstance(n,ast.ImportFrom) and n.module:imports.add(n.module.split('.')[0])
 undeclared=sorted(x for x in imports if x not in allowed and x!='review_convention_equivalence')
 assert not undeclared,(p,undeclared)
 records.append({'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'imports':sorted(imports)})
out={'status':'PASS','python':sys.version,'records':records}
(ROOT/'certificates'/'dependency_audit.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('PASS dependency audit')
