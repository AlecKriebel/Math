#!/usr/bin/env python3
"""Exact small checks, never a proof of the unrestricted existence question."""
import itertools, json
from fractions import Fraction
from pathlib import Path

def rank(rows,p=0):
    if not rows:return 0
    a=[[Fraction(x) if p==0 else x%p for x in row] for row in rows]
    m,n=len(a),len(a[0]); r=0
    for c in range(n):
        j=next((j for j in range(r,m) if a[j][c]),None)
        if j is None:continue
        a[r],a[j]=a[j],a[r]
        z=1/a[r][c] if p==0 else pow(a[r][c],-1,p)
        a[r]=[x*z if p==0 else x*z%p for x in a[r]]
        for j in range(m):
            if j!=r and a[j][c]:
                z=a[j][c];a[j]=[x-z*y if p==0 else (x-z*y)%p for x,y in zip(a[j],a[r])]
        r+=1
        if r==m:break
    return r

def faces(facets):
    s={()}
    for f in facets:
        for n in range(1,len(f)+1):s.update(itertools.combinations(sorted(f),n))
    return s

def homology(facets,p):
    f=faces(facets); d=max(map(len,f))-1
    chain={k:sorted(x for x in f if len(x)==k+1) for k in range(-1,d+1)}
    ranks={-1:0,d+1:0}
    for k in range(d+1):
        prev={x:i for i,x in enumerate(chain[k-1])}; cols=chain[k]
        a=[[0]*len(cols) for _ in prev]
        for j,s in enumerate(cols):
            for z in range(len(s)):a[prev[s[:z]+s[z+1:]]][j]=(-1)**z
        ranks[k]=rank(a,p)
    betti=[len(chain[k])-ranks[k]-ranks[k+1] for k in range(d+1)]
    return [len(chain[k]) for k in range(d+1)],betti

def subdiv(facets):
    f=sorted(faces(facets)-{()},key=lambda s:(len(s),s)); ix={s:i for i,s in enumerate(f)}
    maximal=[]
    for s in facets:
        for perm in itertools.permutations(s):
            maximal.append(tuple(sorted(ix[tuple(sorted(perm[:k]))] for k in range(1,len(s)+1))))
    return maximal

def euler(seq):return sum((-1)**i*x for i,x in enumerate(seq))

def sync(a,b):
    n=max(len(a),len(b));a=list(a)+[0]*(n-len(a));b=list(b)+[0]*(n-len(b))
    assert euler(a)==euler(b)
    aa=a[:];bb=b[:];s=0
    for i in range(n):
        s=a[i]-b[i]-s
        if i==n-1:assert s==0;break
        ca=max(-s,0);cb=max(s,0)
        for j in [i,i+1]:aa[j]+=ca;bb[j]+=cb
    assert aa==bb
    return aa

out={}
examples={"point":[(0,)],"edge":[(0,1)],"path_three_edges":[(0,1),(1,2),(2,3)],"triangle_simplex":[(0,1,2)],"square_cycle":[(0,1),(1,2),(2,3),(0,3)]}
rp=[(0,1,2),(0,1,3),(0,2,4),(0,3,5),(0,4,5),(1,2,5),(1,3,4),(1,4,5),(2,3,4),(2,3,5)]
examples['barycentric_six_vertex_complex']=subdiv(rp)
out['bestvina_brady']={}
for name,c in examples.items():
    vals={}
    for p in [0,2,3,5]:
        f,b=homology(c,p)
        if not any(b):
            h=[];z=1
            for n in range(len(f)):
                h.append(z);z=f[n]-z
            assert z==0
            chi=sum((-1)**i*(i+1)*x for i,x in enumerate(f))
            assert euler(h)==chi
            vals[str(p)]={'reduced_link_betti':b,'group_betti':h,'chi':chi}
        else:vals[str(p)]={'reduced_link_betti':b,'infinite_group_homology_degrees':[i+1 for i,x in enumerate(b) if x]}
    out['bestvina_brady'][name]={'f_vector':f,'fields':vals}
assert out['bestvina_brady']['barycentric_six_vertex_complex']['f_vector']==[31,90,60]
assert out['bestvina_brady']['barycentric_six_vertex_complex']['fields']['2']['reduced_link_betti']==[0,1,1]
assert out['bestvina_brady']['barycentric_six_vertex_complex']['fields']['0']['chi']==31
bs=[]
for m in [2,3,4,5,6,7,11]:
 for p in [0,2,3,5,7]:
    r=rank([[1-m],[0]],p); b=[1,2-r,1-r]
    assert euler(b)==0
    bs.append({'m':m,'characteristic':p,'betti':b,'chi':0})
out['baumslag_solitar']=bs
pairs=0
seqs=list(itertools.product(range(4),repeat=4))
for a in seqs:
 for b in seqs:
    if euler(a)==euler(b):sync(a,b);pairs+=1
out['rank_synchronization']={'equal_euler_pairs_checked':pairs,'entry_range':[0,3],'length':4}
out['status']='PASS: exact finite checks only; unrestricted problem unresolved'
print(json.dumps(out,indent=2))
