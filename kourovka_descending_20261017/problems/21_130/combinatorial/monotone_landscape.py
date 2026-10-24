#!/usr/bin/env python3
"""Exact 2-opt landscape; certify or falsify monotone-score reachability."""
import itertools, json, collections, random, time
from pathlib import Path

def canonical(a):
    i=a.index(0); a=a[i:]+a[:i]
    return a if a[1]<a[-1] else (a[0],)+tuple(reversed(a[1:]))

def analyze(A,mods):
    n=len(A)
    def add(a,b):return tuple((x+y)%m for x,y,m in zip(a,b,mods))
    colors=[[add(a,b) for b in A] for a in A]
    cyc=[(0,)+tail for tail in itertools.permutations(range(1,n)) if tail[0]<tail[-1]]
    scores={a:len({colors[a[i]][a[(i+1)%n]] for i in range(n)}) for a in cyc}
    reached={a for a,s in scores.items() if s==n}
    queue=collections.deque(reached)
    switches=[(i,j) for i in range(n) for j in range(i+2,n) if (i,j)!=(0,n-1)]
    while queue:
        a=queue.popleft(); s=scores[a]
        for i,j in switches:
            b=canonical(a[:i+1]+tuple(reversed(a[i+1:j+1]))+a[j+1:])
            if b not in reached and scores[b]<=s:
                reached.add(b); queue.append(b)
    bad=[a for a in cyc if a not in reached]
    return {'moduli':mods,'subset':A,'n':n,'cycles':len(cyc),'score_histogram':dict(sorted(collections.Counter(scores.values()).items())), 'monotone_reachable':len(reached),'blocked_count':len(bad),'blocked_witness':bad[0] if bad else None}

if __name__=='__main__':
    random.seed(20261024)
    out=[]; started=time.time()
    instances=[]
    for m in [5,7,9,11]:
        for n in range(4,min(m,8)+1):
            # Translation normalize to contain 0. All for m<=9; deterministic samples otherwise.
            cs=list(itertools.combinations(range(1,m),n-1))
            if m>9 and len(cs)>30:cs=random.sample(cs,30)
            for B in cs:instances.append(([(x,) for x in (0,)+B],(m,)))
    for n in [5,6,7,8,9]:
        E=list(itertools.product(range(3), repeat=2))
        for A in itertools.combinations(E,n):
            if (0,0) in A:instances.append((A,(3,3)))
    for i,(A,M) in enumerate(instances):
        r=analyze(A,M);out.append(r)
        if r['blocked_count']:
            print('TRAP',json.dumps(r),flush=True)
            # Stop early: first exact disproof is decisive for the route.
            break
        if i%50==0:print(i,len(instances),time.time()-started,flush=True)
    Path('monotone_landscape_result.json').write_text(json.dumps({'results':out,'elapsed_seconds':time.time()-started},indent=2)+'\n')
    print('DONE',len(out),time.time()-started,flush=True)
