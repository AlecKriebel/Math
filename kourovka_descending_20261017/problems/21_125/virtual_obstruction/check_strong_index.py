#!/usr/bin/env python3
"""Additional necessary coset avoidance; independent finite ranks are bounded."""
import check_index_obstruction as base
from itertools import permutations
from collections import Counter
from pathlib import Path
from datetime import datetime,timezone
import json,math,argparse

def coset_avoids_fixed_points(a2,a1,t):
    # Orbits of <a1,t>. Every a2*a1^k*t^r is fixed-point free iff
    # a2 maps every point outside its orbit under <a1,t>.
    d=len(t);parent=list(range(d))
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]];x=parent[x]
        return x
    def union(x,y):
        x,y=find(x),find(y)
        if x!=y:parent[x]=y
    for x in range(d):union(x,a1[x]);union(x,t[x])
    return all(find(x)!=find(a2[x]) for x in range(d))

def run(d):
    identity=tuple(range(d)); counts=Counter();examples={}; checked=0
    for part in base.partitions(d):
        t=base.representative(part);ti=base.inverse(t)
        for a in permutations(range(d)):
            checked+=1;trajectory=[];seen=set();v=a
            while v!=identity and v not in seen:
                seen.add(v);trajectory.append(v);v=base.conjugator_step(v,t,ti)
            if v!=identity:continue
            depth=len(trajectory)
            for k in range(max(0,depth-2),depth):
                a2=trajectory[k];a1=trajectory[k+1] if k+1<depth else identity
                if coset_avoids_fixed_points(a2,a1,t):
                    m=k+2;counts[m]+=1
                    examples.setdefault(m,{'a_m':a,'t':t,'engels':trajectory,'depth':depth,'cycle_type_t':part})
    return {'degree':d,'pairs_checked':checked,'expected_pairs':math.factorial(d)*sum(1 for _ in base.partitions(d)),
            'permitted_ranks':sorted(counts),'counts':dict(sorted(counts.items())),'witnesses':examples}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--max-degree',type=int,default=8);args=ap.parse_args()
    results=[]
    for d in range(1,args.max_degree+1):
        r=run(d);results.append(r);print(d,r['permitted_ranks'],flush=True)
    Path(__file__).with_name('strong_index_checks.json').write_text(json.dumps({'created_utc':datetime.now(timezone.utc).isoformat(),
      'scope':'Necessary condition only: coset a2<a1,t> consists of fixed-point-free permutations. No transitivity required, so excluded degrees apply to every index-d subgroup.',
      'results':results},indent=2)+'\n')
