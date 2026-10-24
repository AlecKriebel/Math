#!/usr/bin/env python3
"""Exhaustive symmetric-group checks for a necessary RAAG-cover condition.
No certificate here asserts that an allowed cover embeds in any RAAG.
"""
from itertools import permutations
from collections import Counter
from pathlib import Path
from datetime import datetime,timezone
import json, math, argparse

def partitions(n, low=1):
    if n==0:
        yield ()
    for x in range(low,n+1):
        for tail in partitions(n-x,x): yield (x,)+tail

def representative(part):
    p=[]; k=0
    for x in part:
        p.extend(list(range(k+1,k+x))+[k]); k+=x
    return tuple(p)

def inverse(p):
    q=[0]*len(p)
    for i,x in enumerate(p):q[x]=i
    return tuple(q)

def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))

def conjugator_step(a,t,ti):
    # a^-1 t^-1 a t, with composition p*q=p after q.
    ai=inverse(a)
    return tuple(ai[ti[a[t[i]]]] for i in range(len(a)))

def derangement(a):return all(i!=x for i,x in enumerate(a))

def run(d):
    identity=tuple(range(d)); by_rank=Counter(); examples={}; max_depth=0
    terminating=0; pair_count=0
    for part in partitions(d):
        t=representative(part); ti=inverse(t)
        # A simultaneous conjugation makes t this representative. All a remain.
        for a in permutations(range(d)):
            pair_count+=1
            seen=set(); trajectory=[]; v=a
            while v!=identity and v not in seen:
                seen.add(v); trajectory.append(v)
                v=conjugator_step(v,t,ti)
            if v!=identity:continue
            terminating+=1; depth=len(trajectory);max_depth=max(max_depth,depth)
            # At m=rank, a2 is E_(m-2), and E_m must be identity.
            for k in range(max(0,depth-2),depth):
                if not derangement(trajectory[k]):continue
                m=k+2
                by_rank[m]+=1
                examples.setdefault(m,{'a_m':a,'t':t,'engels':trajectory,'depth':depth,'cycle_type_t':part})
    return {'degree':d,'representative_pairs_checked':pair_count,
            'expected_pairs':math.factorial(d)*sum(1 for _ in partitions(d)),
            'terminating_pairs':terminating,'maximum_terminating_depth':max_depth,
            'permitted_ranks':sorted(by_rank),
            'counts_up_to_simultaneous_conjugacy_redundancy':dict(sorted(by_rank.items())),
            'witnesses':examples}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--max-degree',type=int,default=7)
    args=ap.parse_args()
    results=[]
    for d in range(1,args.max_degree+1):
        r=run(d);results.append(r)
        print(d,r['maximum_terminating_depth'],r['permitted_ranks'],flush=True)
    p=Path(__file__).with_name('index_obstruction_checks.json')
    p.write_text(json.dumps({'created_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'Exact finite search, necessary condition only. S_d conjugacy representatives for t; all a_m. No transitivity restriction, so exclusions include all index-d subgroups.',
        'results':results},indent=2)+'\n')
