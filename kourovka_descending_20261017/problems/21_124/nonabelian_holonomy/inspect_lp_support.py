#!/usr/bin/env python3
"""Independent combinatorial support reduction; does not modify root LP data."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
import json
PAIRS=((3,2),(20,14),(119,84))
def run():
 source=Path(__file__).parent.parent/'root_orbit/multiset_results.json'
 data=json.loads(source.read_text());res=next(r for r in reversed(data['runs']) if r.get('support'))
 support=res['support'];rows=defaultdict(dict)
 for j,item in enumerate(support):
  a,b,t=item['triple']
  for i,(p,q) in enumerate(PAIRS):
   u,v=abs(p*a+t),abs(q*b+t)
   if u==v:continue
   for k,c in (((i,u),1),((i,v),-1)):rows[k][j]=rows[k].get(j,0)+c
 rows={k:{j:F(c) for j,c in r.items() if c} for k,r in rows.items()}
 initial=Counter(map(len,rows.values()));active=set(range(len(support)));subs={};steps=[]
 # Eliminate a variable via each positive two-term equation. Store w_drop=ratio*w_keep.
 while True:
  piv=next(((k,r) for k,r in rows.items() if len(r)==2 and list(r.values())[0]*list(r.values())[1]<0),None)
  if piv is None:break
  key,row=piv;drop,keep=sorted(row);ratio=-row[keep]/row[drop]
  assert ratio>0
  subs[drop]=(keep,ratio);active.remove(drop);steps.append({'drop':drop,'keep':keep,'ratio':str(ratio),'row':list(key)})
  for k,r in rows.items():
   if drop in r:
    r[keep]=r.get(keep,F())+r.pop(drop)*ratio
    if not r[keep]:r.pop(keep)
 nonzero={k:r for k,r in rows.items() if r}
 out={'source':str(source),'box':res['box'],'support_size':len(support),'initial_row_sizes':dict(initial),'eliminations':len(steps),'active_variables':len(active),'remaining_nonzero_rows':len(nonzero),'final_row_sizes':dict(Counter(map(len,nonzero.values()))),'singletons':[list(k) for k,r in nonzero.items() if len(r)==1],'same_sign_rows':[list(k) for k,r in nonzero.items() if all(c>0 for c in r.values()) or all(c<0 for c in r.values())],'steps':steps,'active_indices':sorted(active),'reduced_rows':[{'key':list(k),'terms':[[j,str(c)] for j,c in sorted(r.items())]} for k,r in sorted(nonzero.items())]}
 Path(__file__).with_name('lp_support_reduction.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('steps','active_indices','reduced_rows')},indent=2))
if __name__=='__main__':run()
