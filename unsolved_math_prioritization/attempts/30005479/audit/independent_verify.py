#!/usr/bin/env python3
"""Independent adversarial checks. Standard library only; no author imports.
Bases are enumerated with basis exchange; flag spans with closure extensions;
all dimensions use exact rational/integer elimination, never incidence graphs.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from math import gcd, lcm
import json, random


def rank(rows):
    a=[list(r) for r in rows if any(r)]
    if not a:return 0
    k=0
    for j in range(len(a[0])):
        pivot=next((i for i in range(k,len(a)) if a[i][j]),None)
        if pivot is None:continue
        a[k],a[pivot]=a[pivot],a[k]
        for i in range(k+1,len(a)):
            if a[i][j]:
                p,q=a[k][j],a[i][j]
                a[i]=[p*x-q*y for x,y in zip(a[i],a[k])]
                g=0
                for v in a[i]:g=gcd(g,v)
                if g:a[i]=[v//g for v in a[i]]
        k+=1
        if k==len(a):break
    return k


def canonical(rows):
    a=[[Fraction(v) for v in r] for r in rows]
    if not a:return ()
    k=0
    for j in range(len(a[0])):
        pivot=next((i for i in range(k,len(a)) if a[i][j]),None)
        if pivot is None:continue
        a[k],a[pivot]=a[pivot],a[k]
        z=a[k][j];a[k]=[v/z for v in a[k]]
        for i in range(len(a)):
            if i!=k and a[i][j]:
                z=a[i][j];a[i]=[x-z*y for x,y in zip(a[i],a[k])]
        k+=1
        if k==len(a):break
    result=[]
    for row in a[:k]:
        denom=lcm(*(v.denominator for v in row))
        result.append(tuple(int(v*denom) for v in row))
    return tuple(result)


def vec(mask,n):return tuple((mask>>i)&1 for i in range(n))
@lru_cache(None)
def indicator_rank(n,masks):return rank([vec(s,n) for s in masks])
def mrank(n,masks):return indicator_rank(n,tuple(sorted(set(masks)-{0})))

# Deliberately simple list filtering avoids sharing the author's subset recurrence.
def contained(s):return [j for j in range(1,s+1) if j&s==j]

def set_partitions(n):
    if n==0:return [()]
    result=[(1,)]
    for i in range(1,n):
        new=[]
        for p in result:
            new.append(p+(1<<i,))
            for j in range(len(p)):
                q=list(p);q[j]|=1<<i;new.append(tuple(q))
        result=new
    return result


def validate(n,r):
    assert r[0]==0 and len(r)==1<<n
    for s in range(1<<n):
        assert 0<=r[s]<=s.bit_count()
        for t in range(1<<n):
            assert r[s]+r[t]>=r[s|t]+r[s&t]
            if s&t==s:assert r[s]<=r[t]
    assert all(r[1<<i]==1 for i in range(n))


def labelled(n):
    E=(1<<n)-1
    for d in range(1,n+1):
        candidates=[s for s in range(1<<n) if s.bit_count()==d]
        for select in range(1,1<<len(candidates)):
            bases={b for i,b in enumerate(candidates) if select>>i&1}
            union=0
            for b in bases:union|=b
            if union!=E:continue
            good=True
            for a,b in product(bases,repeat=2):
                for i in range(n):
                    if (a&~b)>>i&1 and not any(((a^(1<<i))|(1<<j)) in bases for j in range(n) if (b&~a)>>j&1):
                        good=False;break
                if not good:break
            if good:
                r=tuple(max((s&b).bit_count() for b in bases) for s in range(1<<n))
                yield n,r


def spans(n,r):
    E=(1<<n)-1
    @lru_cache(None)
    def closure(s):return sum(1<<i for i in range(n) if r[s|(1<<i)]==r[s])
    @lru_cache(None)
    def descend(s):
        if s==E:return ((),)
        successors={closure(s|(1<<i)) for i in range(n) if not(s>>i&1)}
        return tuple((t,)+rest for t in sorted(successors) for rest in descend(t))
    # Deduplicate actual row spaces by exact RREF, preserving a flag representative.
    unique={}
    for f in descend(0):
        unique.setdefault(canonical([vec(t,n) for t in f]),f)
    return tuple(sorted(unique.values()))


def objective(n,flags,rows):
    u=rank(rows)
    return 2*max(rank(list(rows)+[vec(s,n) for s in f]) for f in flags)-u


def one(n,r,name,all_parts=True):
    validate(n,r);flags=spans(n,r);E=(1<<n)-1
    @lru_cache(None)
    def p(s):
        if not s:return 0
        low=s&-s
        return min(2*r[t]-1+p(s^t) for t in contained(s) if t&low)
    value=p(E)
    D=max(mrank(n,a+b) for a in flags for b in flags)
    assert D==value,(name,D,value)
    full=0;strict=0;optimal=0
    if all_parts:
        for partition in set_partitions(n):
            cost=sum(2*r[t]-1 for t in partition)
            obj=2*max(mrank(n,f+partition) for f in flags)-len(partition)
            assert value<=obj<=cost,(name,partition,value,obj,cost)
            if cost==value:assert obj==value;optimal+=1
            strict+=obj<cost;full+=1
    independent_sets=sum(all(j.bit_count()<=2*r[j]-1 for j in contained(s)) for s in range(1<<n))
    assert max(s.bit_count() for s in range(1<<n) if all(j.bit_count()<=2*r[j]-1 for j in contained(s)))==value
    # Explicitly recover a lower-bound certificate via projected flag-pair ranks.
    witness=next(s for s in range(1<<n) if s.bit_count()==value and all(j.bit_count()<=2*r[j]-1 for j in contained(s)))
    assert max(mrank(n,tuple(t&witness for t in a+b)) for a in flags for b in flags)==value
    return dict(name=name,n=n,rank=r[-1],flags=len(flags),value=value,partitions=full,
                optimal_partitions=optimal,strict_upper_bounds=strict,independent_sets=independent_sets),flags


def binary(s):
    points=[i+1 for i in range(7) if s>>i&1]
    basis=[]
    for v in points:
        for b in basis:v=min(v,v^b)
        if v:basis.append(v);basis.sort(reverse=True)
    return len(basis)


def greedy(n,r,t,I):
    # Lemma 3.6 implemented independently, including construction assertions.
    subsets=[s for s in range(1<<n) if s&I==s]
    br=[s for s in subsets if r[s]==s.bit_count()==r[I]]
    bt=[s for s in subsets if t[s]==s.bit_count()==t[I]]
    b,c=next((b,c) for b in br for c in bt if b|c==I)
    U,V=b,c;pos1={};pos2={};order=[]
    while U|V:
        aa=[i for i in range(n) if ((V&~b)>>i&1) and r[U|(1<<i)]>r[U]]
        bb=[i for i in range(n) if ((U&~c)>>i&1) and t[V|(1<<i)]>t[V]]
        if aa:
            i=aa[0];pos2[i]=V.bit_count();V^=1<<i;kind='a'
        elif bb:
            i=bb[0];pos1[i]=U.bit_count();U^=1<<i;kind='b'
        else:
            assert U&V
            i=(U&V).bit_length()-1
            pos1[i]=U.bit_count();pos2[i]=V.bit_count();U^=1<<i;V^=1<<i;kind='c'
        order.append((i,kind))
    def flag(rr,positions):
        partial=0;out=[]
        for i in sorted(positions,key=positions.get):
            partial|=1<<i
            out.append(sum(1<<j for j in range(n) if I>>j&1 and rr[partial|(1<<j)]==rr[partial]))
        return tuple(out)
    A=flag(r,pos1);B=flag(t,pos2)
    assert mrank(n,A+B)==I.bit_count()
    used=set()
    for i,kind in order:
        u=next(k for k,f in enumerate(A) if f>>i&1)
        v=len(A)+next(k for k,f in enumerate(B) if f>>i&1)
        assert u not in used or v not in used
        used|={u,v}
    return len(order)


def main():
    out=[];fours=[];counts={};matroids=[]
    for n in range(1,6):
        mats=list(labelled(n));counts[str(n)]=len(mats)
        for index,(n,r) in enumerate(mats):
            name=f'labelled_loopless_{n}_{index}'
            rec,flags=one(n,r,name);out.append(rec)
            if n==4:fours.append((n,r,flags,rec['value']))
    assert counts=={'1':1,'2':2,'3':6,'4':27,'5':185},counts
    # All small rational subspaces generated by ternary vectors, with sign duplicates removed.
    lines=[v for v in product((-1,0,1),repeat=4) if any(v) and next(x for x in v if x)!=-1]
    spaces={()}
    for k in range(1,4):
        spaces.update(canonical(rows) for rows in combinations(lines,k))
    spaces.add(tuple(vec(1<<i,4) for i in range(4)))
    assert len(spaces)==1084,len(spaces)
    subspace_checks=0
    for n,r,flags,value in fours:
        vals=[objective(n,flags,U) for U in spaces]
        assert min(vals)==value
        subspace_checks+=len(vals)
    # Independent two-matroid strengthening audits Bernstein's exact hypotheses.
    pair_checks=0;greedy_steps=0
    for (n,r,A,_),(_,t,B,_) in product(fours,repeat=2):
        for I in range(16):
            independent=all(J.bit_count()<=r[J]+t[J]-1 for J in contained(I))
            dim=max(mrank(n,tuple(s&I for s in a+b)) for a in A for b in B)
            assert (dim==I.bit_count())==independent
            if independent:greedy_steps+=greedy(n,r,t,I)
            pair_checks+=1
    named=[(7,tuple(binary(s) for s in range(128)),'Fano'),
           (7,tuple(s.bit_count()-3+binary(127^s) for s in range(128)),'dual_Fano'),
           (8,tuple(min(s.bit_count(),4)-(s in {15,51,195,60,204}) for s in range(256)),'Vamos'),
           (10,tuple(min(binary(s&127)+((s&511)>>7).bit_count()+bool(s&512),5) for s in range(1024)),'Fano_2_coloops_free_extension')]
    rng=random.Random(65230005479);random_checks=0
    for n,r,name in named:
        rec,flags=one(n,r,name,n<=8);out.append(rec)
        for _ in range(25):
            rows=[tuple(rng.randint(-3,3) for _ in range(n)) for _ in range(rng.randint(0,n))]
            assert objective(n,flags,rows)>=rec['value'];random_checks+=1
        if n==10:
            assert rec['value']==8 and r[-1]==5
            assert all(r[s]+r[1023^s]>5 for s in range(1,1023))
            assert r[:128]==tuple(binary(s) for s in range(128))
    # E empty uses the zero ambient space, zero fan and empty partition.
    assert rank([])==0 and set_partitions(0)==[()]
    empty=dict(fan_dimension=0,subspace_objective=0,partition_cost=0)
    print(json.dumps(dict(passed=True,all_labelled_loopless_counts=counts,
        total_instances=len(out),all_partitions_checked=sum(x['partitions'] for x in out),
        rational_subspaces_on_four_elements=len(spaces),rational_objective_checks=subspace_checks,
        two_matroid_projection_checks=pair_checks,greedy_constructed_edges=greedy_steps,
        named_random_subspace_checks=random_checks,empty_case=empty,checks=out),indent=2,sort_keys=True))

if __name__=='__main__':main()
