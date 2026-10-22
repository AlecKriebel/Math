#!/usr/bin/env python3
"""Pass the directory containing the pinned 12mut.out and 13mut.out reading copies."""
from pathlib import Path
import hashlib,json,sys
root=Path(__file__).resolve().parent
src=Path(sys.argv[1]) if len(sys.argv)>1 else root.parent.parent/'sources'
m=json.loads((root/'SOURCE_ADDITION_TURN_4.json').read_text())
hashes={r['file']:r['sha256'] for r in m['sources']}
checks=0;receipt=[]
for n,off,targets in [(12,1288,[288,491,501]),(13,4878,[3370])]:
 f=f'{n}mut.out';data=(src/f).read_bytes()
 if hashlib.sha256(data).hexdigest()!=hashes[f]:raise SystemExit('Pinned table hash mismatch: '+f)
 groups=[[[int(x) for x in l.split()] for l in g.splitlines() if l.strip()] for g in data.decode().strip().split('\n\n')]
 for g in groups:
  assert len(g)>=2;checks+=1
  for row in g:
   k,idx,*dt=row;assert len(dt)==k and sorted(map(abs,dt))==list(range(2,2*k+1,2));checks+=1
  assert len({v[0] for v in g})==1;checks+=1
 absent={str(t):not any(row[0]==n and row[1]==off+t for g in groups for row in g) for t in targets}
 assert all(absent.values());checks+=len(targets)
 receipt.append({'file':f,'group_count':len(groups),'alternating_offset':off,'nonalternating_target_indices':targets,'all_absent':absent})
print(json.dumps({'status':'PASS_TABLE_SCREEN_ONLY','exact_sanity_assertions':checks,'tables':receipt,'scope':'Absence from these pinned published groups only; not a no-mutants theorem or independent table classification. Mirrors not distinguished.'},indent=2))
