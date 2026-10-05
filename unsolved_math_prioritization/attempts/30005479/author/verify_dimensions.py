#!/usr/bin/env python3
"""Independent exact checks for the already-published amoeba-dimension claim.
No third-party code or datasets are needed. Python standard library only.
Finite checks are regression tests, not a substitute for the cited theorem.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
import json, random


def subsets(s):
    t=s
    while t:
        yield t
        t=(t-1)&s


def rank_matrix(rows):
    a=[[Fraction(v) for v in row] for row in rows]
    if not a:return 0
    h=0
    for c in range(len(a[0])):
        p=next((i for i in range(h,len(a)) if a[i][c]),None)
        if p is None:continue
        a[h],a[p]=a[p],a[h]
        q=a[h][c];a[h]=[v/q for v in a[h]]
        for i in range(h+1,len(a)):
            q=a[i][c]
            if q:a[i]=[x-q*y for x,y in zip(a[i],a[h])]
        h+=1
        if h==len(a):break
    return h


def vector(s,n):return [int(bool(s&(1<<i))) for i in range(n)]


class Matroid:
    def __init__(self,n,rank,name):
        self.n=n;self.E=(1<<n)-1;self.name=name
        self.r=[rank(s) for s in range(1<<n)];self.d=self.r[-1]
        assert self.r[0]==0
        for s in range(1<<n):
            assert 0<=self.r[s]<=s.bit_count()
            outside=[1<<i for i in range(n) if not (s>>i&1)]
            for e in outside:
                assert self.r[s]<=self.r[s|e]<=self.r[s]+1
            for e,f in combinations(outside,2):
                assert self.r[s|e]+self.r[s|f]>=self.r[s]+self.r[s|e|f]
        assert all(self.r[1<<i]==1 for i in range(n))
        levels=[[] for _ in range(self.d+1)]
        for s in range(1<<n):
            if all(self.r[s|(1<<i)]>self.r[s] for i in range(n) if not (s>>i&1)):
                levels[self.r[s]].append(s)
        @lru_cache(None)
        def extend(s):
            if s==self.E:return ((),)
            return tuple((t^s,)+p for t in levels[self.r[s]+1] if s&t==s for p in extend(t))
        self.flags=sorted(set(tuple(sorted(p)) for p in extend(0)))

    def optimum(self):
        @lru_cache(None)
        def dp(s):
            if not s:return 0,()
            first=s&-s;best=(10**9,())
            for t in subsets(s):
                if t&first:
                    v,p=dp(s^t);cand=(v+2*self.r[t]-1,(t,)+p)
                    if cand[0]<best[0]:best=cand
            return best
        return dp(self.E)


def pair_dimension(p,q):
    # Exact rank of the bipartite incidence matrix of two layer partitions.
    parent=list(range(len(p)+len(q)))
    def find(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]];i=parent[i]
        return i
    for i,a in enumerate(p):
        for j,b in enumerate(q):
            if a&b:parent[find(i)]=find(len(p)+j)
    return len(parent)-len({find(i) for i in range(len(parent))})


def partitions(s):
    if not s:yield ();return
    bit=s&-s
    for p in partitions(s^bit):
        yield (bit,)+p
        for i in range(len(p)):
            yield p[:i]+(p[i]|bit,)+p[i+1:]


def check(m,full=False,random_count=0):
    opt,p=m.optimum()
    D=max(pair_dimension(a,b) for i,a in enumerate(m.flags) for b in m.flags[i:])
    obj=lambda q:2*max(pair_dimension(f,q) for f in m.flags)-len(q)
    assert D==opt==obj(p),(m.name,D,opt,obj(p))
    count=0;strict=0
    if full:
        best=10**9
        for q in partitions(m.E):
            a=obj(q);b=sum(2*m.r[t]-1 for t in q)
            assert opt<=a<=b
            strict+=a<b;best=min(best,a);count+=1
        assert best==opt
    rng=random.Random(30005479+m.n)
    for _ in range(random_count):
        U=[[rng.randint(-2,2) for _ in range(m.n)] for _ in range(rng.randrange(m.n+1))]
        u=rank_matrix(U)
        q=max(rank_matrix(U+[vector(s,m.n) for s in f]) for f in m.flags)
        assert 2*q-u>=D
    # Cross-check graph-rank implementation against unrelated rational elimination.
    for _ in range(10):
        a=rng.choice(m.flags);b=rng.choice(m.flags)
        assert pair_dimension(a,b)==rank_matrix([vector(s,m.n) for s in a+b])
    return dict(name=m.name,n=m.n,rank=m.d,flag_spans=len(m.flags),partition_minimum=opt,
                self_sum_dimension=D,optimal_partition_objective=obj(p),optimal_partition=list(p),
                all_partitions_checked=count,strict_nonoptimal_partition_bounds=strict,
                random_rational_subspaces_checked=random_count)


def uniform(r,n):return Matroid(n,lambda s:min(r,s.bit_count()),f'U{r},{n}')

def binary_rank(s):
    piv={}
    for i in range(7):
        if s>>i&1:
            x=i+1
            while x:
                b=x.bit_length()-1
                if b not in piv:piv[b]=x;break
                x^=piv[b]
    return len(piv)


def main():
    results=[];small=0
    for r in range(1,5):
        choices=[sum(1<<i for i in b) for b in combinations(range(4),r)]
        for family in range(1,1<<len(choices)):
            bases=[b for i,b in enumerate(choices) if family>>i&1]
            try:m=Matroid(4,lambda s:max((s&b).bit_count() for b in bases),f'four_{r}_{family}')
            except AssertionError:continue
            results.append(check(m,True,3));small+=1
    assert small==27
    for n in range(1,8):
        for r in range(1,n+1):results.append(check(uniform(r,n),n<=6,2 if n<=5 else 0))
    fano=Matroid(7,binary_rank,'Fano_F7');results.append(check(fano,True,12))
    dual=Matroid(7,lambda s:s.bit_count()-3+binary_rank(127^s),'dual_Fano');results.append(check(dual,True,4))
    holes={15,51,195,60,204}
    vamos=Matroid(8,lambda s:min(s.bit_count(),4)-(s in holes),'Vamos_V8')
    results.append(check(vamos,False,3))
    # A connected free extension of F7 plus two coloops: nontrivial partition min.
    rank9=lambda s:binary_rank(s&127)+(s>>7).bit_count()
    m=Matroid(10,lambda s:min(rank9(s&511)+bool(s&512),5),'free_extension_Fano_plus_2_coloops')
    assert all(m.r[s]+m.r[m.E^s]>m.d for s in range(1,m.E))  # connected
    result=check(m,False,0);assert result['partition_minimum']==8<min(m.n,2*m.d-1)
    results.append(result)
    # Pin the overstrong per-partition identity's smallest convenient counterexample.
    m=uniform(2,4);p=(3,12)
    defect={'matroid':'U2,4','partition':[[1,2],[3,4]],
            'partition_cost':sum(2*m.r[t]-1 for t in p),
            'braid_objective':2*max(pair_dimension(f,p) for f in m.flags)-len(p)}
    assert defect['partition_cost']==6 and defect['braid_objective']==4
    print(json.dumps({'passed':True,'labelled_loopless_matroids_on_4':small,
                      'total_matroid_instances':len(results),'checks':results,
                      'nonoptimal_partition_identity_counterexample':defect},indent=2))

if __name__=='__main__':main()
