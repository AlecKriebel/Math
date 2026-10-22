#!/usr/bin/env python3
"""Finite controls for the standard weakly fundamental deletion construction."""
import itertools as it,json,math,random
from pathlib import Path
if not __debug__:
    raise SystemExit("Run this assertion-based checker without Python -O.")
from verify import presentation,eliminate

def adjof(ed):
    adj={v:set() for e in ed for v in e}
    for a,b in ed:adj[a].add(b);adj[b].add(a)
    return adj

def connected_path(ed,s,t):
    adj=adjof(ed);par={s:None};q=[s]
    for v in q:
        if v==t:
            out=[t]
            while out[-1]!=s:out.append(par[out[-1]])
            return out[::-1]
        for w in sorted(adj.get(v,[])):
            if w not in par:par[w]=v;q.append(w)
    return None

def build(ed):
    adj=adjof(ed);seen=set();components=[]
    for s in sorted(adj):
        if s in seen:continue
        c={s};q=[s];seen.add(s)
        for v in q:
            for w in adj[v]:
                if w not in seen:seen.add(w);c.add(w);q.append(w)
        components.append(c)
    for comp in components:
        if all(len(adj[v])==2 for v in comp):
            s=min(comp);pp=[s];prev=None;v=s
            while True:
                w=min(adj[v]-({prev} if prev is not None else set()))
                pp.append(w)
                if w==s:return ('circle',pp)
                prev,v=v,w
    branches={v for v in adj if len(adj[v])>=3};visited=set();paths=[]
    for s in sorted(branches):
        for w in sorted(adj[s]):
            if tuple(sorted((s,w))) in visited:continue
            pp=[s,w];visited.add(tuple(sorted((s,w))));prev,v=s,w
            while v not in branches:
                z=next(iter(adj[v]-{prev}));visited.add(tuple(sorted((v,z))));pp.append(z);prev,v=v,z
            paths.append(pp)
    assert len(visited)==len(ed)
    # A shortest cycle in the multigraph; retain edge indices and directed vertices.
    madj={v:[] for v in branches}
    for i,pp in enumerate(paths):a,b=pp[0],pp[-1];madj[a].append((b,i));madj[b].append((a,i))
    best=None
    for i,pp in enumerate(paths):
        s,t=pp[0],pp[-1]
        if s==t:cand=[(i,s,t)]
        else:
            par={t:None};q=[t]
            for v in q:
                if v==s:break
                for w,j in madj[v]:
                    if j!=i and w not in par:par[w]=(v,j);q.append(w)
            if s not in par:continue
            rev=[];v=s
            while v!=t:
                w,j=par[v];rev.append((j,w,v));v=w
            cand=[(i,s,t)]+rev[::-1]
        if best is None or len(cand)<len(best):best=cand
    assert best
    raw=[]
    for i,a,b in best:
        pp=paths[i]
        if pp[0]!=a:pp=pp[::-1]
        assert pp[-1]==b;raw+=pp[:-1]
    longest=max((i for i,a,b in best),key=lambda i:len(paths[i]))
    return ('other',raw,paths[longest],len(best))

def algorithm(ed):
    ed=set(ed);records=[]
    while True:
        while True:
            adj=adjof(ed);leaves={v for v in adj if len(adj[v])<2}
            if not leaves:break
            ed={e for e in ed if not(set(e)&leaves)}
        if not ed:break
        b=build(ed)
        if b[0]=='circle':pp=b[1];cc=pp[:-1];num=1
        else:_,cc,pp,num=b
        pe={tuple(sorted(e)) for e in zip(pp,pp[1:])}
        assert len(cc)==len(set(cc)) and all(tuple(sorted(e)) in ed for e in zip(cc,cc[1:]+cc[:1]))
        records.append((cc,pe,num));ed-=pe
    return records

def run():
    rng=random.Random(353);graphs=[]
    for n in range(3,12):
        for j in range(8):
            ed={(i,i+1) for i in range(n-1)}
            ed.update(e for e in it.combinations(range(n),2) if rng.random()<.27)
            if len(ed)>=n:graphs.append((list(range(n)),sorted(ed)))
    # Two cycles joined by a long bridge path, and a plain cycle.
    graphs += [(list(range(10)),[(0,1),(1,2),(0,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(7,9)]),(list(range(5)),[(0,1),(1,2),(2,3),(3,4),(0,4)])]
    data=[];steps=0
    for vs,ed in graphs:
        r=len(ed)-len(vs)+1;k=1 if r==1 else 2*math.ceil(math.log2(2*r))+1
        cyc_edges={e for e in ed if connected_path(set(ed)-{e},*e)}
        rr=algorithm(ed);assert len(rr)==r
        charged=set();later=set()
        for cc,pp,ns in rr:
            assert not(pp&charged);charged|=pp;assert pp<=cyc_edges
            assert ns<=k and len(cc)<=k*len(pp)
        for cc,pp,ns in reversed(rr):
            assert pp-later
            later.update(tuple(sorted(e)) for e in zip(cc,cc[1:]+cc[:1]))
        gs,rels=presentation(vs,ed,[x[0] for x in rr]);gg,re,_=eliminate(gs,rels);assert not gg and not re
        cost=sum(len(x[0]) for x in rr);assert cost<=k*len(cyc_edges);steps+=r
        data.append(dict(vertices=len(vs),edges=len(ed),rank=r,cyclic_edges=len(cyc_edges),k=k,cost=cost))
    out={'status':'pass','graph_cases':len(graphs),'deletion_steps':steps,'scope':'Finite cycle/path, disjoint charging, reversed weak-fundamental, and Tietze checks; no universal-proof or optimum certificate.','records':data}
    Path(__file__).with_name('DELETION_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2))
if __name__=='__main__':run()
