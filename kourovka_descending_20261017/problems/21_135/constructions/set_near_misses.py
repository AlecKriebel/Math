"""Preserve degree-set near misses without misclassifying them as solutions."""
import json
from pathlib import Path
from collections import defaultdict
P=Path(__file__).resolve().parent
rows=[json.loads(l) for l in (P/'artifacts/library_scan.ndjson').read_text().splitlines()]
buckets=defaultdict(list)
for x in rows:
    d=dict(x[2]);buckets[(x[1],tuple(d),d.get(1,0))].append(x)
result=[]
for b in buckets.values():
    for g in b:
        if g[3]!=1:continue
        for h in b:
            if h[3]==1:continue
            gd,hd=dict(g[2]),dict(h[2]);delta={d:hd.get(d,0)-gd.get(d,0) for d in set(gd)|set(hd) if hd.get(d,0)!=gd.get(d,0)}
            result.append({'radical_free_table':g,'radical_nontrivial_table':h,'H_minus_G_multiplicities':delta,'status':'NOT a multiset match'})
(P/'artifacts/set_near_misses.json').write_text(json.dumps(result,indent=2)+'\n')
print('Exact equal-order degree-set/linear-count near misses:',len(result))
