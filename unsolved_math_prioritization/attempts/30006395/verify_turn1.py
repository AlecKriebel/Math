"""Exact finite controls for the unknown Cayley-tree mixture moment formula.
Own Prüfer enumeration, direct pairs, forest inclusion, and partition formula.
No simulations or downloaded code.
"""
from itertools import product,combinations
from collections import Counter
from fractions import Fraction as F
from math import factorial,comb,prod
import json
counts=Counter()
def ck(x,kind):
    assert x,kind
    counts[kind]+=1
def falling(n,v):return prod(range(n-v+1,n+1))
def trees(labels):
    labels=tuple(labels);k=len(labels)
    if k==1:yield ();return
    for code in product(labels,repeat=k-2):
        deg={i:1 for i in labels}
        for i in code:deg[i]+=1
        edges=[]
        for i in code:
            j=min(v for v in labels if deg[v]==1)
            edges.append(tuple(sorted((i,j))));deg[j]-=1;deg[i]-=1
        left=[i for i in labels if deg[i]==1]
        edges.append(tuple(sorted(left)));yield tuple(sorted(edges))
def maskof(edges,idx):return sum(1<<idx[e] for e in edges)
def components(mask,edges):
    verts=set();adj={}
    for i,(u,v) in enumerate(edges):
        if mask>>i&1:
            verts.update([u,v]);adj.setdefault(u,[]).append(v);adj.setdefault(v,[]).append(u)
    sizes=[];seen=set()
    for u in verts:
        if u in seen:continue
        todo=[u];seen.add(u);size=0
        while todo:
            v=todo.pop();size+=1
            for w in adj[v]:
                if w not in seen:seen.add(w);todo.append(w)
        sizes.append(size)
    return len(verts),sorted(sizes)
# Complete fixed-vertex forest inclusion, including the spanning-tree edge case.
forest_total=0
for k in range(2,7):
    edges=list(combinations(range(k),2));idx={e:i for i,e in enumerate(edges)}
    masks=[maskof(t,idx) for t in trees(range(k))]
    ck(len(masks)==k**(k-2),'cayley_enumeration')
    freq=Counter()
    for mask in masks:
        sub=mask
        while True:
            freq[sub]+=1
            if not sub:break
            sub=(sub-1)&mask
    for f,num in freq.items():
        v,sizes=components(f,edges);m=f.bit_count()
        expected=F(prod(sizes),k**m)
        ck(F(num,len(masks))==expected,'all_forest_containment')
        ck(m==v-len(sizes),'forest_edge_components')
        forest_total+=1
# Integer partitions into component sizes >=2 enumerate each support profile.
def parts(total,minimum=2):
    if total==0:yield ();return
    for s in range(minimum,total+1):
        for tail in parts(total-s,s):yield (s,)+tail

def formula(n,k,p):
    ans=F(1);z=1/p-1
    for v in range(2,k+1):
        for sizes in parts(v):
            r=len(sizes);m=v-r
            term=F(falling(k,v)**2,falling(n,v)*k**(2*m))*z**m
            for size in sizes:term*=F(size**size,factorial(size))
            for mult in Counter(sizes).values():term/=factorial(mult)
            ans+=term
    return ans
pair_cases=0;pair_total=0
for n in range(2,8):
    for k in range(2,min(n,5 if n<=6 else 4)+1):
        edges=list(combinations(range(n),2));idx={e:i for i,e in enumerate(edges)}
        masks=[maskof(t,idx) for sub in combinations(range(n),k) for t in trees(sub)]
        ck(len(masks)==comb(n,k)*k**(k-2),'embedded_tree_count')
        hist=Counter((x&y).bit_count() for x in masks for y in masks);pair_total+=len(masks)**2
        for p in [F(1,5),F(1,2),F(4,5),F(1,n),F(n-1,n)]:
            direct=sum(F(num,len(masks)**2)*p**(-e) for e,num in hist.items())
            exact=formula(n,k,p)
            ck(direct==exact,'pair_overlap_equals_forest_formula')
            ck(exact>=1,'second_moment_nonnegative_variance')
            # Expand the same overlap histogram before summation.
            expanded=sum(F(num,len(masks)**2)*sum(F(comb(e,j))*(1/p-1)**j for j in range(e+1)) for e,num in hist.items())
            ck(expanded==direct,'edge_subset_binomial_expansion')
            pair_cases+=1
# Finite population algebra behind the Gaussian component majorant.
for n in range(4,101):
    for k in range(2,n//2+1):
        for v in range(2,k+1):
            ck(F(1,k)-F(1,2*(n-v+1))>=F(1,2*k),'falling_factorial_log_coefficient')
            # Each ordered component split has nonnegative cross terms.
        for v in range(2,min(k,15)+1):
            for sizes in parts(v):
                ck(v*(v-1)>=sum(s*(s-1) for s in sizes),'component_gaussian_allocation')
# Direct normalizing likelihood on all small graphs.
likelihood_cases=0
for n,k in [(3,2),(3,3),(4,2),(4,3),(4,4),(5,3)]:
    edges=list(combinations(range(n),2));idx={e:i for i,e in enumerate(edges)}
    masks=[maskof(t,idx) for sub in combinations(range(n),k) for t in trees(sub)]
    p=F(2,5);mean=F(0);moment=F(0)
    for g in range(1<<len(edges)):
        wt=p**g.bit_count()*(1-p)**(len(edges)-g.bit_count())
        z=sum((g&t)==t for t in masks)
        L=F(z,len(masks))*p**(-(k-1));mean+=wt*L;moment+=wt*L*L
        likelihood_cases+=1
    ck(mean==1,'likelihood_normalization_all_graphs')
    ck(moment==formula(n,k,p),'likelihood_moment_all_graphs')
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'counts':dict(sorted(counts.items())),'labelled_forests_checked':forest_total,'pair_distribution_parameter_cases':pair_cases,'ordered_tree_pairs_counted':pair_total,'small_null_graphs_enumerated':likelihood_cases,'scope':'Exact finite enumeration and algebra controls only; asymptotic bounds and model restrictions are proved in TURN_1.md. No inference of detectability from moment divergence.'},indent=2,sort_keys=True))
