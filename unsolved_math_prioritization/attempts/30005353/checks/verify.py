#!/usr/bin/env python3
"""Exact finite controls. No claim to machine-prove the universal theorems."""
import itertools as it, json, math, random
from pathlib import Path
if not __debug__:
    raise SystemExit("Run this assertion-based checker without Python -O.")

def faces(facets):
    return sorted({tuple(t) for f in facets for k in range(1,len(f)+1) for t in it.combinations(sorted(f),k)},key=lambda s:(len(s),s))
def moore(p,q=3):
    a=list(range(p*q)); b=list(range(p*q,p*q+q)); c=p*q+q
    f=[]
    for i in a:
        j=(i+1)%(p*q)
        f += [(i,j,b[j%q]),(i,b[i%q],b[j%q]),(c,i,j)]
    return faces(f), b

def subdivide(fs):
    ids={s:i for i,s in enumerate(fs)}; ss=[set(s) for s in fs]
    ed=[(i,j) for i in range(len(fs)) for j in range(i+1,len(fs)) if ss[i]<ss[j] or ss[j]<ss[i]]
    tri=[]
    for f in [s for s in fs if len(s)==3]:
        for v in f:
            for e in it.combinations(f,2):
                if v in e:tri.append(tuple(sorted([ids[(v,)],ids[tuple(sorted(e))],ids[f]])))
    return list(range(len(fs))),ed,sorted(tri),ids

def modrank(rows,p):
    piv={}
    for row in rows:
        row=[x%p for x in row]
        while any(row):
            k=next(i for i,x in enumerate(row) if x)
            if k in piv:
                t=row[k];row=[(a-t*b)%p for a,b in zip(row,piv[k])]
            else:
                z=pow(row[k],-1,p);piv[k]=[(z*x)%p for x in row];break
    return len(piv)

def triangle_rows(ed,tri):
    idx={e:i for i,e in enumerate(ed)};rows=[]
    for a,b,c in tri:
        r=[0]*len(ed)
        r[idx[a,b]]=1;r[idx[b,c]]=1;r[idx[a,c]]=-1;rows.append(r)
    return rows

def reduced(w):
    out=[]
    for a in w:
        if out and out[-1]==-a:out.pop()
        else:out.append(a)
    return out

def inv(w):return [-x for x in w[::-1]]
def cyc(w):
    w=reduced(w)
    while len(w)>1 and w[0]==-w[-1]:w=w[1:-1]
    return w

def presentation(vs,ed,cycles):
    adj={v:[] for v in vs}
    for a,b in ed:adj[a].append(b);adj[b].append(a)
    seen={vs[0]};todo=[vs[0]];tree=set()
    for v in todo:
        for w in sorted(adj[v]):
            if w not in seen:seen.add(w);todo.append(w);tree.add(tuple(sorted((v,w))))
    assert len(seen)==len(vs)
    gen={e:i+1 for i,e in enumerate(e for e in ed if e not in tree)}
    rel=[]
    for cc in cycles:
        w=[]
        for a,b in zip(cc,cc[1:]+cc[:1]):
            k=gen.get(tuple(sorted((a,b))))
            if k:w.append(k if a<b else -k)
        rel.append(cyc(w))
    return set(gen.values()),rel

def eliminate(gens,rels):
    gens=set(gens);rels=[r for r in rels if r];steps=0
    while True:
        pick=None
        for ri,r in enumerate(rels):
            for j,x in enumerate(r):
                if sum(abs(y)==abs(x) for y in r)==1:
                    pick=(ri,j,x);break
            if pick:break
        if not pick:break
        ri,j,x=pick;r=rels.pop(ri);pre=r[:j];post=r[j+1:]
        rep=inv(pre)+inv(post) if x>0 else post+pre
        new=[]
        for s in rels:
            t=[]
            for y in s:t.extend(rep if y==abs(x) else inv(rep) if y==-abs(x) else [y])
            t=cyc(t)
            if t:new.append(t)
        rels=new;gens.remove(abs(x));steps+=1
    return gens,rels,steps

def short_cycles(vs,ed,maxlen=5):
    adj={v:set() for v in vs}
    for a,b in ed:adj[a].add(b);adj[b].add(a)
    for start in vs:
        def walk(path):
            for w in sorted(adj[path[-1]]):
                if w==start and len(path)>=3:
                    if path[1]<path[-1]:yield path
                elif len(path)<maxlen and w>start and w not in path:yield from walk(path+[w])
        yield from walk([start])

def cocycle_labels(ed,rows,p):
    # Return one non-gradient cocycle via nullspace elimination, using gauge zero on a tree.
    vs=sorted({v for e in ed for v in e});adj={v:[] for v in vs}
    for e in ed:
        a,b=e;adj[a].append(b);adj[b].append(a)
    seen={vs[0]};todo=[vs[0]];tree=set()
    for v in todo:
        for w in sorted(adj[v]):
            if w not in seen:seen.add(w);todo.append(w);tree.add(tuple(sorted((v,w))))
    cols=[i for i,e in enumerate(ed) if e not in tree]
    mat=[[r[j]%p for j in cols] for r in rows];pr=[];rr=0
    for c in range(len(cols)):
        j=next((j for j in range(rr,len(mat)) if mat[j][c]),None)
        if j is None:continue
        mat[rr],mat[j]=mat[j],mat[rr];z=pow(mat[rr][c],-1,p);mat[rr]=[(x*z)%p for x in mat[rr]]
        for j in range(len(mat)):
            if j!=rr and mat[j][c]:
                z=mat[j][c];mat[j]=[(a-z*b)%p for a,b in zip(mat[j],mat[rr])]
        pr.append(c);rr+=1
    free=next(c for c in range(len(cols)) if c not in pr);x=[0]*len(cols);x[free]=1
    for j,c in enumerate(pr):x[c]=-mat[j][free]%p
    out={e:0 for e in ed}
    for c,z in zip(cols,x):out[ed[c]]=z
    return out

def evaluate(cc,labels,p):return sum(labels[tuple(sorted((a,b)))]*(1 if a<b else -1) for a,b in zip(cc,cc[1:]+cc[:1]))%p

def moore_checks():
    out=[]
    for p in [2,3,5,7,9]:
        fs,b=moore(p);vs,ed,tri,ids=subdivide(fs);r=len(ed)-len(vs)+1
        assert (len(vs),len(ed),len(tri),r)==(24*p+7,78*p+6,54*p,54*p)
        rows=triangle_rows(ed,tri);rank2=modrank(rows,2)
        prime=2 if p==2 else 3 if p%3==0 else p
        rankp=modrank(rows,prime)
        assert rank2==r-(p%2==0) and rankp==r-1
        base=[]
        for i,v in enumerate(b):base.extend([ids[(v,)],ids[tuple(sorted((v,b[(i+1)%3])))]] )
        gs,rs=presentation(vs,ed,[list(t) for t in tri]);gg,rr,steps=eliminate(gs,rs)
        assert len(gg)==1 and len(rr)==1 and len(rr[0])==p and len(set(rr[0]))==1
        # Remove a small triangle lying in the cone cap, then add its six-edge base loop.
        original_cap=next(f for f in fs if len(f)==3 and p*3+3 in f)
        omit=next(t for t in tri if ids[original_cap] in t)
        kept=[list(t) for t in tri if t!=omit]
        gs,rs=presentation(vs,ed,kept);g0,r0,s0=eliminate(gs,rs)
        assert len(g0)==1 and not r0
        gs,rs=presentation(vs,ed,kept+[base]);g1,r1,s1=eliminate(gs,rs)
        assert not g1 and not r1
        labels=cocycle_labels(ed,rows,prime);assert evaluate(base,labels,prime)!=0
        short_count=0
        if p in [2,3]:
            for cc in short_cycles(vs,ed):assert evaluate(cc,labels,prime)==0;short_count+=1
        out.append(dict(p=p,vertices=len(vs),edges=len(ed),triangles=len(tri),cycle_rank=r,triangle_rank_F2=rank2,triangle_rank_Fp=rankp,prime=prime,remaining_relator_length=len(rr[0]),tietze_eliminations=steps,short_cycles_checked=short_count,alpha_F2=3*r+(3 if p==2 else 0),alpha_pi1=3*r+3,base_length=len(base)))
    return out

if __name__=='__main__':
    out={'status':'pass','scope':'Exact finite chain ranks, Tietze certificates, and short-cycle cocycle controls, not universal proof checking.','moore_examples':moore_checks()}
    dest=Path(__file__).with_name('CHECK_RESULTS.json');dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
