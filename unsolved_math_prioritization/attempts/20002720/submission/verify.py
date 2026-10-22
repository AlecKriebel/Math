#!/usr/bin/env python3
"""Exact finite controls for scalar boxed convolution; no external dependencies.
Finite tests supplement the proofs in STRUCTURE.md and are not global proofs.
"""
from collections import defaultdict
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product, combinations
import json, math, random
from pathlib import Path

@lru_cache(None)
def partitions(n):
    if n == 0:
        return ((),)
    out=[]
    for p in partitions(n-1):
        out.append(p+((n-1,),))
        for j in range(len(p)):
            out.append(p[:j]+(p[j]+(n-1,),)+p[j+1:])
    return tuple(out)

def noncrossing(p):
    for a,b in combinations(p,2):
        for x,z in combinations(a,2):
            for y,t in combinations(b,2):
                if x<y<z<t or y<x<t<z:
                    return False
    return True

@lru_cache(None)
def nc(n):
    return tuple(p for p in partitions(n) if noncrossing(p))

def canon(p):
    return tuple(sorted((tuple(sorted(b)) for b in p),key=lambda b:b[0]))

@lru_cache(None)
def kreweras(p):
    n=sum(map(len,p)); perm=list(range(n))
    for b in p:
        for i,x in enumerate(b): perm[x]=b[(i+1)%len(b)]
    inv=[0]*n
    for i,x in enumerate(perm):inv[x]=i
    k=[inv[(i+1)%n] for i in range(n)]
    unseen=set(range(n)); out=[]
    while unseen:
        j=min(unseen); b=[]
        while j in unseen:
            unseen.remove(j);b.append(j);j=k[j]
        out.append(tuple(sorted(b)))
    return canon(out)

@lru_cache(None)
def words(s,N):
    return tuple(w for n in range(1,N+1) for w in product(range(s),repeat=n))

def one(s,N):return {w:Q(int(len(w)==1)) for w in words(s,N)}
def red(x,m):return x % m if m else x

def coeff_partition(f,w,p,m=None):
    a=1
    for b in p:a=red(a*f.get(tuple(w[i] for i in b),0),m)
    return a

def box(f,g,s,N,m=None):
    return {w:red(sum(coeff_partition(f,w,p,m)*coeff_partition(g,w,kreweras(p),m) for p in nc(len(w))),m) for w in words(s,N)}

def inverse(f,s,N,m=None):
    g={}
    for w in words(s,N):
        if len(w)==1:g[w]=pow(int(f[w]),-1,m) if m else 1/Q(f[w]);continue
        a=math.prod(f[(i,)] for i in w)
        a_inv=pow(int(a),-1,m) if m else 1/Q(a)
        other=sum(coeff_partition(f,w,p,m)*coeff_partition(g,w,kreweras(p),m) for p in nc(len(w)) if len(p)!=len(w))
        g[w]=red(-a_inv*other,m)
    return g

def random_series(s,N,rng,normalized=True,m=None):
    f={w:(rng.randrange(m) if m else Q(rng.randrange(-3,4))) for w in words(s,N)}
    for i in range(s):f[(i,)]=1 if normalized else (3 if m else Q(rng.choice([-2,-1,1,2,3])))
    return f

def mono_key(a):return (sum(len(w)-1 for w in a),a)
def monomial(a):return tuple(sorted(a,key=lambda w:(len(w),w)))
def pmul(f,g):
    out=defaultdict(Q)
    for a,x in f.items():
        for b,y in g.items():out[monomial(a+b)]+=x*y
    return {a:x for a,x in out.items() if x}

def basis(s,d):
    gens=[w for w in words(s,d+1) if len(w)>=2];out=[]
    def rec(start,remaining,current):
        out.append(tuple(current))
        for j in range(start,len(gens)):
            w=gens[j]
            if len(w)-1<=remaining:rec(j,remaining-len(w)+1,current+[w])
    rec(0,d,[])
    return sorted(out,key=mono_key)

def translate_generator(w,u):
    out=defaultdict(Q)
    for p in nc(len(w)):
        a=monomial(tuple(tuple(w[i] for i in b) for b in p if len(b)>=2))
        out[a]+=coeff_partition(u,w,kreweras(p))
    return dict(out)

def representation(u,s,d):
    bs=basis(s,d);ix={a:i for i,a in enumerate(bs)};columns=[]
    for a in bs:
        p={():Q(1)}
        for w in a:p=pmul(p,translate_generator(w,u))
        columns.append({ix[b]:x for b,x in p.items() if x})
    return bs,columns

def compose(a,b):
    out=[]
    for bj in b:
        col=defaultdict(Q)
        for k,x in bj.items():
            for i,y in a[k].items():col[i]+=y*x
        out.append({i:x for i,x in col.items() if x})
    return out

def mm(a,b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))

def run():
    checks=0; results={};rng=random.Random(20002720)
    def check(x):
        nonlocal checks
        assert x
        checks+=1
    for n in range(1,8):
        check(len(nc(n))==math.comb(2*n,n)//(n+1))
        for p in nc(n):
            k=kreweras(p)
            check(k in nc(n));check(len(p)+len(k)==n+1)
            check(canon(tuple(tuple((i-1)%n for i in b) for b in p))==kreweras(k))
    results['catalan_counts_through_7']=[len(nc(n)) for n in range(1,8)]
    for s,N,reps in [(1,6,5),(2,5,5),(3,4,3)]:
        e=one(s,N)
        for _ in range(reps):
            f,g,h=[random_series(s,N,rng,False) for z in range(3)]
            check(box(e,f,s,N)==f==box(f,e,s,N))
            inv=inverse(f,s,N)
            check(box(f,inv,s,N)==e==box(inv,f,s,N))
            check(box(box(f,g,s,N),h,s,N)==box(f,box(g,h,s,N),s,N))
            lam=[f[(i,)] for i in range(s)]
            t={w:(lam[w[0]] if len(w)==1 else 0) for w in words(s,N)}
            check(box(t,g,s,N)==box(g,t,s,N))
            u={w:f[w]/math.prod(lam[i] for i in w) for w in words(s,N)}
            check(box(t,u,s,N)==f)
    results['rational_series_test_cases']=13
    for mod in (4,8,9):
        s,N=2,4;e={w:int(len(w)==1) for w in words(s,N)}
        f=random_series(s,N,rng,False,mod)
        if mod==9:
            for i in range(s):f[(i,)]=2
        inv=inverse(f,s,N,mod)
        check(box(f,inv,s,N,mod)==e==box(inv,f,s,N,mod))
    results['zero_divisor_base_rings']=['Z/4Z','Z/8Z','Z/9Z']
    s,N=2,6;e=one(s,N)
    for p,q in [(2,2),(2,3),(2,4),(3,3),(3,4),(4,4)]:
        f=random_series(s,N,rng);g=random_series(s,N,rng)
        for w in words(s,N):
            if 2<=len(w)<p:f[w]=0
            if 2<=len(w)<q:g[w]=0
        fg=box(f,g,s,N);gf=box(g,f,s,N)
        check(all(fg[w]==gf[w] for w in words(s,N) if len(w)<p+q-1))
        comm=box(box(fg,inverse(f,s,N),s,N),inverse(g,s,N),s,N)
        check(all(comm[w]==e[w] for w in words(s,N) if len(w)<p+q-1))
    results['filtration_pairs']=[[2,2],[2,3],[2,4],[3,3],[3,4],[4,4]]
    f=e.copy();g=e.copy();f[(0,0)]=1;g[(0,1)]=1
    fg=box(f,g,s,N);gf=box(g,f,s,N)
    check((fg[(0,1,0)],gf[(0,1,0)])==(1,0))
    results['noncommutativity_at_word_121']={'f_box_g':1,'g_box_f':0}
    for _ in range(3):
        c={n:Q(rng.randrange(-3,4)) for n in range(2,N+1)}
        radial={w:(Q(1) if len(w)==1 else c[len(w)]) for w in words(s,N)}
        g=random_series(s,N,rng,False)
        check(box(radial,g,s,N)==box(g,radial,s,N))
    results['radial_centrality_cases_through_degree_6']=3
    for s,d in [(1,4),(2,2),(2,3)]:
        N=d+1;u=random_series(s,N,rng);v=random_series(s,N,rng)
        bs,a=representation(u,s,d);_,b=representation(v,s,d)
        _,ab=representation(box(u,v,s,N),s,d)
        check(compose(a,b)==ab)
        check(all(col.get(j)==1 and all(i<=j for i in col) for j,col in enumerate(a)))
        ix={p:i for i,p in enumerate(bs)}
        check(all(a[ix[(w,)]].get(0,0)==u[w] for w in words(s,N) if len(w)>=2))
        results[f'regular_representation_s{s}_weight{d}_dimension']=len(bs)
    # Nonlinear polynomials of bounded degree do not form a subgroup in the full group.
    f=one(1,3);f[(0,0)]=1
    check(box(f,f,1,3)[(0,0,0)]==3)
    results['degree_2_polynomial_product_degree_3']=3
    # Ordinary boxed formula fails over noncommutative matrix coefficients.
    A=((1,1),(0,1));B=((1,0),(1,1));AB=mm(A,B)
    left=mm(AB,AB);right=mm(mm(A,A),mm(B,B))
    check(left!=right)
    results['matrix_coefficient_associativity_failure']={'left':left,'right':right}
    # The torus is not the entire center: normalized Zeta has nonlinear terms.
    zeta={w:1 for w in words(2,5)};g=random_series(2,5,rng,False)
    check(box(zeta,g,2,5)==box(g,zeta,2,5));check(zeta[(0,0)]==1)
    results['zeta_central_and_nonlinear_control']=True
    # Since normalized degree-2 coordinates add, every commutator has zero degree 2.
    f=random_series(2,4,rng,False);g=random_series(2,4,rng,False)
    comm=box(box(box(f,g,2,4),inverse(f,2,4),2,4),inverse(g,2,4),2,4)
    check(all(comm[w]==0 for w in words(2,2) if len(w)==2))
    results['claimed_full_derived_subgroup_equality_refuted_by_degree_2_quotient']=True
    return {'passed':True,'assertions':checks,'arithmetic':'exact integers and rational numbers','seed':20002720,'results':results,'limitation':'Finite checks only; general arguments are in STRUCTURE.md. No peer-review or novelty certification.'}

if __name__=='__main__':
    result=run();print(json.dumps(result,indent=2))
    if '--write' in __import__('sys').argv:
        Path(__file__).with_name('CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
