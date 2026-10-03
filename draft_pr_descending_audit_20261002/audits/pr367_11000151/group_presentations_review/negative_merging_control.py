from itertools import combinations
from pathlib import Path
import json,datetime
D=Path(__file__).resolve().parent
n=3;pairs=list(combinations(range(n),2));weights={p:3**i for i,p in enumerate(pairs)}
def trace(word):
 p=list(range(n));counts=[0]*len(pairs)
 for a in word:
  i=a-1;pair=tuple(sorted(p[i:i+2]));counts[pairs.index(pair)]+=1;p[i],p[i+1]=p[i+1],p[i]
 return tuple(p),tuple(counts)
def action(word):
 images=tuple((j,) for j in range(1,n+1))
 for g in word:
  table=[(j,) for j in range(1,n+1)];table[g-1]=(g,g+1,-g);table[g]=(g,);new=[]
  for w in images:
   reduced=[]
   for a in w:
    part=table[a-1] if a>0 else tuple(-b for b in reversed(table[-a-1]))
    for b in part:
     if reduced and reduced[-1]==-b:reduced.pop()
     else:reduced.append(b)
   new.append(tuple(reduced))
  images=tuple(new)
 return images
u=(1,1,2,2);v=(2,2,1,1);assert trace(u)==trace(v);assert action(u)!=action(v)
full=3**3-1;back={full:tuple(range(n))};queue=[full]
for code in queue:
 p=back[code]
 for i in range(n-1):
  step=weights[tuple(sorted(p[i:i+2]))]
  if code//step%3==0:continue
  np=list(p);np[i],np[i+1]=np[i+1],np[i];nc=code-step
  if nc not in back:back[nc]=tuple(np);queue.append(nc)
code=sum(count*3**i for i,count in enumerate(trace(u)[1]));assert code not in back
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','words':[u,v],'same_strand_permutation_and_pair_counts':trace(u),'different_exact_actions':[action(u),action(v)],'count_code':code,'can_complete_to_all_pairs_two':False,'mechanism':'Pair-count merging alone does not establish braid equality. This collision is outside the coaccessible graph and hence does not challenge the candidate, which explicitly verifies every coaccessible action edge.'}
(D/'receipts/NEGATIVE_MERGING_CONTROL.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
