#!/usr/bin/env python3
"""Reproducible finite checks of the fixed-P4-graph matching theorem only."""
from pathlib import Path
from itertools import combinations
from hashlib import sha256
import importlib.util
import json
import random

spec=importlib.util.spec_from_file_location('flow_note',Path(__file__).with_name('check_flow.py'))
f=importlib.util.module_from_spec(spec)
spec.loader.exec_module(f)
LABELS={'L':'ab','M':'bc','R':'cd'}


def coordinate(n, types, edges, charges, x):
    vs=[v for v in range(n) if x in LABELS[types[v]]]
    index={v:i for i,v in enumerate(vs)}
    xe=[(index[u],index[v]) for u,v,y in edges if y==x]
    q=[charges[v].get(x,0) for v in vs]
    return vs,xe,q


def feasible(n,types,edges,charges,D):
    for x in 'abcd':
        vs,xe,q=coordinate(n,types,edges,charges,x)
        req={i for i,v in enumerate(vs) if v in D}
        if f.flow(len(vs),xe,q,req) is None:
            return False
    return True


def matching_size(U,V,links):
    adj=[[] for _ in U]
    for a,b in links:
        adj[a].append(b)
    mate={}
    def augment(a,seen):
        for b in adj[a]:
            if b in seen:
                continue
            seen.add(b)
            if b not in mate or augment(mate[b],seen):
                mate[b]=a
                return True
        return False
    for a in range(len(U)):
        augment(a,set())
    return len(mate)


def formula(n,types,edges,charges,D):
    forced={v for v in D if (types[v]=='L' and charges[v].get('a',0))
            or (types[v]=='R' and charges[v].get('d',0))}
    target=D-forced
    bad={}
    for x in 'bc':
        vs,xe,q=coordinate(n,types,edges,charges,x)
        bad[x]=[]
        for cs,es in f.components(len(vs),xe):
            base={vs[i] for i in cs}
            if len(es)==len(cs)-1 and base<=target and sum(q[i] for i in cs):
                bad[x].append(base)
    links=[]
    for i,C in enumerate(bad['b']):
        for j,E in enumerate(bad['c']):
            links.extend((i,j) for v in C&E)
    nu=matching_size(bad['b'],bad['c'],links)
    return len(forced)+len(bad['b'])+len(bad['c'])-nu


def brute(n,types,edges,charges,D):
    for k in range(len(D)+1):
        for ex in combinations(sorted(D),k):
            if feasible(n,types,edges,charges,D-set(ex)):
                return k
    raise AssertionError('all vertices as reservoirs must work')


def main():
    rng=random.Random(2112703)
    forests=0
    covers=0
    snapshots=[]
    for trial in range(250):
        n=rng.randrange(1,10)
        types=[rng.choice('LMR') for _ in range(n)]
        parent=list(range(n))
        def root(v):
            while parent[v]!=v:
                v=parent[v]
            return v
        edges=[]
        pairs=[(u,v) for u in range(n) for v in range(u+1,n)
               if {types[u],types[v]} in [{'L','M'},{'M','R'}]]
        rng.shuffle(pairs)
        for u,v in pairs:
            if root(u)!=root(v) and rng.randrange(2):
                parent[root(u)]=root(v)
                edges.append((u,v,'b' if 'L' in (types[u],types[v]) else 'c'))
        charges=[{x:rng.randrange(-1,2) for x in LABELS[t]} for t in types]
        D={v for v in range(n) if rng.randrange(4)}
        predicted=formula(n,types,edges,charges,D)
        actual=brute(n,types,edges,charges,D)
        assert predicted==actual
        forests+=1
        # Add arbitrary additional allowable edges, possibly cycles/parallel edges.
        for _ in range(rng.randrange(4)):
            if pairs:
                u,v=rng.choice(pairs)
                edges.append((u,v,'b' if 'L' in (types[u],types[v]) else 'c'))
        base=formula(n,types,edges,charges,D)
        m=rng.randrange(2,6)
        ee=[]
        for u,v,x in edges:
            perm=list(range(m))
            rng.shuffle(perm)
            ee.extend((u*m+s,v*m+perm[s],x) for s in range(m))
        tt=[t for t in types for _ in range(m)]
        qq=[q.copy() for q in charges for _ in range(m)]
        DD={v*m+s for v in D for s in range(m)}
        lifted=formula(n*m,tt,ee,qq,DD)
        assert lifted==m*base
        covers+=1
        if trial<8:
            snapshots.append({'n':n,'types':types,'edges':edges,'charges':charges,
                              'D':sorted(D),'stable_loss':base,'cover_degree':m,
                              'cover_stable_loss':lifted})
    # A cyclic charged b-component has stable loss 0 but finite loss at least 1.
    cyclic=[]
    for m in range(1,41):
        types=['L']*m+['M']*m
        edges=[(s,m+s,'b') for s in range(m)]+[(s,m+(s+1)%m,'b') for s in range(m)]
        q=[{'a':0,'b':1} for _ in range(m)]+[{'b':0,'c':0} for _ in range(m)]
        D=set(range(2*m))
        assert formula(2*m,types,edges,q,D)==0
        assert not feasible(2*m,types,edges,q,D)
        assert feasible(2*m,types,edges,q,D-{0})
        cyclic.append({'cover_degree':m,'stable_loss':0,'finite_minimum_exceptions':1})
    out={'scope':'fixed-P4-graph relative disk loss; not absolute scl',
         'bruteforce_forest_cases':forests,'arbitrary_cover_scaling_cases':covers,
         'cyclic_nonattainment_cases':cyclic,'sample_certificates':snapshots,
         'all_checks_passed':True,'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(__file__).with_name('P4_OPTIMIZATION_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['bruteforce_forest_cases','arbitrary_cover_scaling_cases','all_checks_passed']}))

if __name__=='__main__':
    main()
