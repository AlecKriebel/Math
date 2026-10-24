#!/usr/bin/env python3
"""Exhaust all zero-containing subsets of sizes 3..7 in two larger groups."""
import hashlib
import itertools
import json
from pathlib import Path
import time
from datetime import datetime,timezone
from search import addition_table,find_cycle,group_label

root=Path(__file__).parent/'exhaustive_sizes7'
root.mkdir(exist_ok=True)
summary={'started_utc':datetime.now(timezone.utc).isoformat(),'sizes':list(range(3,8)),'groups':[]}
for moduli in ((3,3,3),(5,5)):
    start=time.perf_counter(); label=group_label(moduli); plus=addition_table(moduli); q=len(plus)
    target=root/(label+'.jsonl'); count=0; total_calls=0; worst=None
    with target.open('w') as f:
        f.write(json.dumps({'format':'odd-rainbow-cycle-v1','domain':'sizes','sizes':list(range(3,8)),'moduli':moduli,'order':q,'fixed_start':0})+'\n')
        for n in range(3,8):
            for tail in itertools.combinations(range(1,q),n-1):
                vertices=[0,*tail]
                mask=sum(1<<v for v in vertices)
                cycle,stats=find_cycle(vertices,plus)
                assert cycle is not None, (moduli,vertices)
                f.write(json.dumps({'mask':mask,'cycle':cycle},separators=(',',':'))+'\n')
                count+=1; total_calls+=stats['calls']
                if worst is None or worst['calls']<stats['calls']:
                    worst={'mask':mask,'vertices':vertices,'cycle':cycle,**stats}
            print(f'{label}: size {n} done; {count} total; {time.perf_counter()-start:.2f}s',flush=True)
    result={'group':label,'moduli':moduli,'order':q,'subsets':count,'total_dfs_calls':total_calls,'hardest':worst,'elapsed_seconds':time.perf_counter()-start,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
    summary['groups'].append(result); print(json.dumps(result),flush=True)
summary['finished_utc']=datetime.now(timezone.utc).isoformat()
(root/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
