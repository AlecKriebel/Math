import sys,json,numpy as np
sys.path.insert(0,'degenerate_mtw_30000997')
from probe_mtw import tensor
p=json.load(open('degenerate_mtw_30000997/NUMERICAL_PROBE.json'))['lowest'][:3]
out=[]
for q in p:
 for h in [.002,.0005,.0001,.00002]:
  d=tensor(q['x0'],np.array(q['v']),h=h,tol=2e-13);out.append(d); print(json.dumps(d),flush=True)
json.dump(out,open('degenerate_mtw_30000997/NUMERICAL_REFINEMENT.json','w'),indent=2)
