#!/usr/bin/env python3
from check_covers import path,rels,cover
from pathlib import Path
from datetime import datetime,timezone
import json
ps={'a':(0,1,3,2),'b':(1,0,2,3),'c':(2,3,0,1),'t':(0,1,2,3)}
weights=[1,0,0,0,-1,0,0,4,0,2,0,2,0,0,0,2]
checks=[]
for i in range(4):
 for rel in rels(4):
  end,v=path(rel,i,ps);val=sum(x*y for x,y in zip(v,weights))
  assert end==i and val==0
  checks.append({'vertex':i,'relator':rel,'endpoint':end,'weight':val})
end,v=path('a',0,ps);assert end==0
assert sum(x*y for x,y in zip(v,weights))==1
out={'utc':datetime.now(timezone.utc).isoformat(),'k':4,'degree':4,'right_action':ps,'edge_weights_by_vertex': [weights[4*i:4*i+4] for i in range(4)],'lifted_relators':checks,'a_loop_at_zero_weight':1,'exact_homology':cover(4,ps),'claim':'the stabilizer H of0 has index4, contains a, and h->a^{weight(h)} retracts H onto <a>; H is not normal'}
Path(__file__).with_name('nonnormal_witness.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
