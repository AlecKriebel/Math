#!/usr/bin/env python3
"""Reconstruct frozen mpmath traversal; preserve all raw binary endpoints.
Usage: python export_leaves.py ../packet .
This export is not itself the independent proof: verify_independent.py
checks the resulting partition with independent rational arithmetic.
"""
from pathlib import Path
import hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
source=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(exist_ok=True,parents=True)
assert hashlib.sha256((source/'SHA256SUMS').read_bytes()).hexdigest()=='d218aaade8691a6de5ca584355d83e7e9d02f5ec1452bdb6f993b30eff8c1fa8'
assert hashlib.sha256((source/'verify_controls.py').read_bytes()).hexdigest()=='02e08c1277689db4c7a0ed77d4d096fbbdda0216f17419acda76f5407471ddb2'
spec=importlib.util.spec_from_file_location('frozen',source/'verify_controls.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
result={}
for name,h,co,dmax in [('target',10000.,(1,1,1),30),('negative',8.,(2,0,0),22)]:
 rows=[];stack=[(0.,h,0)]
 while stack:
  lo,hi,d=stack.pop();r,i=mod.line_box(lo,hi,co);ok=mod.excludes_zero(r) or mod.excludes_zero(i)
  if ok or d==dmax:
   rows.append({'lo_hex':lo.hex(),'hi_hex':hi.hex(),'depth':d,'accepted':ok,'original_re_raw':[list(x) for x in r._mpi_],'original_im_raw':[list(x) for x in i._mpi_]})
  else:
   mid=(lo+hi)/2;assert lo<mid<hi;stack.extend([(mid,hi,d+1),(lo,mid,d+1)])
 p=out/(name+'_leaves.jsonl');p.write_text(''.join(json.dumps(x,sort_keys=True,separators=(',',':'))+'\n' for x in rows))
 result[name]={'leaves':len(rows),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(out/'leaf_export.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,sort_keys=True))
