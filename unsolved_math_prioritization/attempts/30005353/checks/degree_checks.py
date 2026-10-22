#!/usr/bin/env python3
"""Finite exact controls for graph blow-ups; standard library only."""
import itertools as it,json,random
from pathlib import Path
if not __debug__:
    raise SystemExit("Run this assertion-based checker without Python -O.")
from verify import presentation,eliminate,short_cycles

def cycles(vs,ed):return list(short_cycles(vs,ed,len(vs)))
def bitrank_add(piv,x):
    while x:
        b=x.bit_length()-1
        if b in piv:x^=piv[b]
        else:piv[b]=x;return True
    return False

def cbasis(vs,ed):
    ix={e:i for i,e in enumerate(ed)};piv={};out=[]
    for cc in sorted(cycles(vs,ed),key=lambda c:(len(c),c)):
        x=0
        for a,b in zip(cc,cc[1:]+cc[:1]):x^=1<<ix[tuple(sorted((a,b))) ]
        if bitrank_add(piv,x):out.append(cc)
    assert len(out)==len(ed)-len(vs)+1
    return out

def path(adj,s,t):
    par={s:None};todo=[s]
    for v in todo:
        if v==t:break
        for w in sorted(adj[v]):
            if w not in par:par[w]=v;todo.append(w)
    out=[t]
    while out[-1]!=s:out.append(par[out[-1]])
    return out[::-1]

def fundamental(vs,ed):
    adj={v:[] for v in vs}
    for a,b in ed:adj[a].append(b);adj[b].append(a)
    tree={v:[] for v in vs};seen={vs[0]};todo=[vs[0]]
    for v in todo:
        for w in sorted(adj[v]):
            if w not in seen:seen.add(w);todo.append(w);tree[v].append(w);tree[w].append(v)
    return [path(tree,a,b) for a,b in ed if b not in tree[a]]

def blowup(vs,ed,L,seed):
    rng=random.Random(seed);adj={v:[] for v in vs}
    for a,b in ed:adj[a].append(b);adj[b].append(a)
    nv=[];ee=[];trees={};ports={};external={};D=0
    def vertex():v=len(nv);nv.append(v);return v
    def edge(a,b):ee.append(tuple(sorted((a,b))))
    for v in vs:
        nbr=adj[v][:];rng.shuffle(nbr);d=len(nbr)
        if d==1:
            pp=[vertex()];te=[]
        elif d==2:
            pp=[vertex(),vertex()];te=[tuple(pp)];edge(*pp)
        else:
            bb=[vertex() for _ in nbr];pp=[vertex() for _ in nbr];te=[]
            for a,b in zip(bb,bb[1:]):edge(a,b);te.append((a,b))
            for a,b in zip(bb,pp):edge(a,b);te.append((a,b))
        tadj={x:[] for e in te for x in e}
        if d==1:tadj={pp[0]:[]}
        for a,b in te:tadj[a].append(b);tadj[b].append(a)
        trees[v]=tadj
        for w,u in zip(nbr,pp):ports[v,w]=u
        D=max(D,max(len(path(tadj,a,b))-1 for a in pp for b in pp))
    for eidx,(v,w) in enumerate(ed):
        pp=[ports[v,w]]+[vertex() for _ in range(L-1)]+[ports[w,v]]
        external[v,w]=pp
        for a,b in zip(pp,pp[1:]):edge(a,b)
    def lift(cc):
        out=[]
        for i,v in enumerate(cc):
            u=cc[i-1];w=cc[(i+1)%len(cc)]
            pp=path(trees[v],ports[v,u],ports[v,w]);out.extend(pp[:-1])
            ep=external.get((v,w))
            if ep is None:ep=external[w,v][::-1]
            out.extend(ep[:-1])
        assert len(out)==len(set(out))
        return out
    return nv,sorted(ee),D,external,lift

def run():
    sample=[(list(range(5)),[(0,1),(0,2),(0,3),(0,4),(1,2),(3,4)])]
    rng=random.Random(85353)
    for n in range(3,7):
        for rep in range(4):
            ee={(i,i+1) for i in range(n-1)}
            rest=[e for e in it.combinations(range(n),2) if e not in ee];rng.shuffle(rest)
            ee.update(rest[:min(len(rest),1+rep)])
            sample.append((list(range(n)),sorted(ee)))
    records=[];projected_nonsimple=0;cycles_checked=0;normal_checks=0
    for j,(vs,ed) in enumerate(sample):
        base=cbasis(vs,ed);a2=sum(map(len,base));r=len(base)
        for L in [1,2,4]:
            vv,ee,D,external,lift=blowup(vs,ed,L,j)
            assert len(ee)-len(vv)+1==r
            deg={v:0 for v in vv}
            for a,b in ee:deg[a]+=1;deg[b]+=1
            assert max(deg.values())<=3
            lifted=[lift(c) for c in base]
            for c,z in zip(base,lifted):assert L*len(c)<=len(z)<=(L+D)*len(c)
            b2=cbasis(vv,ee);a2new=sum(map(len,b2));assert L*a2<=a2new<=(L+D)*a2
            fam=[lift(c) for c in fundamental(vs,ed)]
            gs,rs=presentation(vv,ee,fam);gg,rr,_=eliminate(gs,rs);assert not gg and not rr;normal_checks+=1
            epaths={e:set(tuple(sorted(z)) for z in zip(pp,pp[1:])) for e,pp in external.items()}
            for cc in cycles(vv,ee):
                used={tuple(sorted(z)) for z in zip(cc,cc[1:]+cc[:1])};active=[]
                for e,es in epaths.items():
                    intersection=used&es
                    assert not intersection or intersection==es
                    if intersection:active.append(e)
                assert active and L*len(active)<=len(cc)
                dd={v:0 for v in vs}
                for a,b in active:dd[a]+=1;dd[b]+=1
                assert all(x%2==0 for x in dd.values())
                if any(x>2 for x in dd.values()):projected_nonsimple+=1
                cycles_checked+=1
            records.append(dict(case=j,L=L,D=D,rank=r,vertices=len(vv),edges=len(ee),alpha2_original=a2,alpha2_expanded=a2new))
    assert projected_nonsimple>0
    out={'status':'pass','scope':'Finite homology optima, degree and full-path traversal controls, and explicit normal-generation Tietze reductions; no exhaustive pi1 optimization.','graph_cases':len(sample),'expanded_cases':len(records),'cycles_checked':cycles_checked,'projected_nonsimple_cycles':projected_nonsimple,'normal_generation_checks':normal_checks,'records':records}
    Path(__file__).with_name('DEGREE_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2))
if __name__=='__main__':run()
