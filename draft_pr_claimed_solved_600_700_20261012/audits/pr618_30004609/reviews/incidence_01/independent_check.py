#!/usr/bin/env python3
"""Fresh exact diagnostics. Standard library only; candidate code is not imported.
Finite tests support, and do not substitute for, the proof audit in FINDINGS.md.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product, permutations
from collections import Counter
import json


def reduced(rows, width):
    mat = [[Fraction(v) for v in row] for row in rows]
    pivot_cols = []
    at = 0
    for col in range(width):
        choices = [i for i in range(at, len(mat)) if mat[i][col]]
        if not choices:
            continue
        i = choices[0]
        mat[i], mat[at] = mat[at], mat[i]
        scale = mat[at][col]
        mat[at] = [v / scale for v in mat[at]]
        for j in range(len(mat)):
            if j != at and mat[j][col]:
                scale = mat[j][col]
                mat[j] = [v - scale * u for v, u in zip(mat[j], mat[at])]
        pivot_cols.append(col)
        at += 1
        if at == len(mat):
            break
    return mat[:at], pivot_cols


def kernel(rows, width):
    mat, pivots = reduced(rows, width)
    out = []
    for free in set(range(width)) - set(pivots):
        vec = [Fraction(0)] * width
        vec[free] = 1
        for row, pivot in zip(mat, pivots):
            vec[pivot] = -row[free]
        out.append(vec)
    return out


class Representation:
    def __init__(self, vectors, ambient=None):
        self.vectors = tuple(tuple(v) for v in vectors)
        self.n = len(vectors)
        self.ambient = len(vectors[0]) if vectors else (ambient or 0)
        self.full = (1 << self.n) - 1

    @lru_cache(None)
    def rank(self, mask):
        return len(reduced([self.vectors[i] for i in range(self.n) if mask & (1 << i)], self.ambient)[1])

    @lru_cache(None)
    def closure(self, mask):
        r = self.rank(mask)
        return sum(1 << i for i in range(self.n) if self.rank(mask | (1 << i)) == r)

    def flats(self):
        known = {0}
        todo = [0]
        while todo:
            f = todo.pop()
            for i in range(self.n):
                g = self.closure(f | (1 << i))
                if g not in known:
                    known.add(g)
                    todo.append(g)
        return sorted(known, key=lambda f: (self.rank(f), f))

    def lines(self):
        return sorted({self.closure((1 << i) | (1 << j)) for i,j in combinations(range(self.n),2)})

    def audit(self):
        assert all(self.rank(1 << i) == 1 for i in range(self.n))
        assert all(self.closure(1 << i) == 1 << i for i in range(self.n))
        lines = self.lines()
        rich = [line for line in lines if line.bit_count() > 2]
        local = []
        for line in rich:
            inds = [i for i in range(self.n) if line & (1 << i)]
            mat = [[self.vectors[i][c] for i in inds] for c in range(self.ambient)]
            for rel in kernel(mat, len(inds)):
                v = [0] * self.n
                for i,c in zip(inds,rel):
                    v[i] = c
                local.append(v)
        r = self.rank(self.full)
        localrank = len(reduced(local,self.n)[1])
        adj = {i: set() for i in range(self.n+len(rich))}
        for j,line in enumerate(rich):
            for i in range(self.n):
                if line & (1 << i):
                    adj[i].add(self.n+j)
                    adj[self.n+j].add(i)
        remaining=set(adj); components=0
        while remaining:
            components += 1
            todo = [remaining.pop()]
            while todo:
                for nei in adj[todo.pop()] & remaining:
                    remaining.remove(nei)
                    todo.append(nei)
        flats = self.flats()
        modular = [f for f in flats if all(self.rank(f)+self.rank(g) == self.rank(f|g)+self.rank(f&g) for g in flats)]
        chains={0:[0]}
        for f in modular:
            if f == 0: continue
            for g in chains:
                if g & f == g and self.rank(g) == self.rank(f)-1:
                    chains[f]=chains[g]+[f]
                    break
        mu={0:1}
        for f in flats[1:]:
            mu[f] = -sum(mu[g] for g in mu if g & f == g)
        characteristic=[sum(mu[f] for f in flats if r-self.rank(f)==i) for i in range(r+1)]
        return dict(n=self.n,rank=r,ambient=self.ambient,relation_dim=self.n-r,local_relation_rank=localrank,
                    formal=localrank==self.n-r,rich_lines=[[i for i in range(self.n) if l & (1<<i)] for l in rich],
                    multiplicities=dict(Counter(l.bit_count() for l in lines)),
                    components=components,beta=sum(map(len,adj.values()))//2-len(adj)+components,
                    characteristic_ascending=characteristic,flat_count=len(flats),
                    modular_masks=modular,modular_chain=chains.get(self.full),supersolvable=self.full in chains)


def attach(vectors, at, slopes=(-2,3)):
    old=[tuple(a)+(0,) for a in vectors]
    u=(0,)*(len(old[0])-1)+(1,)
    return old + [tuple(x+s*y for x,y in zip(u,old[at])) for s in slopes]


def fixture_checks():
    tri=[(1,0),(0,1),(1,2)]
    quad=[(1,0),(0,1),(1,2),(1,-3)]
    core=[(1,0,0),(0,1,0),(1,1,0),(0,0,1),(1,0,1),(0,1,-1)]
    nonfano=[(1,0,0),(0,1,0),(0,0,1),(1,-1,0),(1,0,-1),(0,1,-1),(1,1,-1)]
    withdrawal=[(1,0,0,0),(0,1,0,0),(1,1,0,0),(1,2,0,0),(1,0,1,0),(0,0,1,0),(0,0,0,1),(0,0,1,1)]
    fixtures={"empty":[],"rank_one":[(3,)],"rank_two_boolean":[(1,0),(0,1)],
              "triple":tri,"quad":quad,"K4":core,"nonFano":nonfano,
              "withdrawal":withdrawal,"withdrawal_deleted":[v for i,v in enumerate(withdrawal) if i!=4],
              "nonessential_K4":[v+(0,0) for v in core],
              "product_quad_tri":[v+(0,0) for v in quad]+[(0,0)+v for v in tri]}
    out={}
    for name,vectors in fixtures.items():
        result=Representation(vectors).audit()
        assert result['formal']
        assert result['supersolvable'] == (name != 'nonFano')
        out[name]=result
    assert out['K4']['rich_lines']==[[0,1,2],[0,3,4],[1,3,5],[2,4,5]]
    assert out['K4']['beta']==3 and out['K4']['relation_dim']==3
    assert out['nonFano']['beta']==6
    attachments=[]
    for kind,base in [('triple',tri),('quad',quad),('K4',core)]:
        original_beta=out[kind]['beta']
        for at in [0,len(base)-1,1]:
            before=Representation(base).audit()
            expanded=attach(base,at)
            after=Representation(expanded).audit()
            W=(1<<len(base))-1
            assert after['formal'] and after['supersolvable']
            assert after['rank']==before['rank']+1
            assert after['relation_dim']==before['relation_dim']+1
            assert after['beta']==original_beta
            assert W in after['modular_masks']
            assert all(f in after['modular_masks'] for f in before['modular_chain'])
            attachments.append(dict(kind=kind,attachment_index=at,before_rank=before['rank'],after_rank=after['rank'],
                                    old_span_modular=True,old_chain_lifts=True))
            base=expanded
        out[kind+'_rank'+str(after['rank'])]=after
    return dict(fixtures=out,attachment_checks=attachments)


def support_enumeration():
    triples=list(combinations(range(6),3))
    masks=[sum(1<<i for i in t) for t in triples]
    checked=0; kept=[]
    for inds in combinations(range(len(triples)),4):
        checked += 1
        chosen=[masks[i] for i in inds]
        if any((a&b).bit_count()>1 for a,b in combinations(chosen,2)):
            continue
        ds=[sum((a>>i)&1 for a in chosen) for i in range(6)]
        if min(ds)<2:
            continue
        assert ds==[2]*6
        assert all((a&b).bit_count()==1 for a,b in combinations(chosen,2))
        kept.append([triples[i] for i in inds])
    assert checked==4845 and len(kept)==30
    return dict(families_checked=checked,min_degree_two_linear_families=len(kept),all_K4=True)


def rank3_pool_check():
    pool=[]
    for vec in product((-1,0,1),repeat=3):
        if not any(vec): continue
        if next(x for x in vec if x)!=1: continue
        pool.append(vec)
    rep=Representation(pool)
    lines=rep.lines()
    candidates=0; formal=0; nonsuper=[]
    for inds in combinations(range(13),6):
        mask=sum(1<<i for i in inds)
        if rep.rank(mask)!=3: continue
        induced={l&mask for l in lines if (l&mask).bit_count()>=2}
        sizes=[l.bit_count() for l in induced]
        if max(sizes)>4 or sum((m-1)*(m-2)//2 for m in sizes)!=4:
            continue
        candidates += 1
        result=Representation([pool[i] for i in inds]).audit()
        formal += result['formal']
        if result['formal'] and not result['supersolvable']:
            nonsuper.append(inds)
    assert not nonsuper
    return dict(pool_size=13,six_subsets_checked=1716,necessary_signature_matches=candidates,
                formal_matches=formal,formal_nonsupersolvable_matches=0)

# Exact polynomials in four variables, independently checking the withdrawal example.
Z=(0,0,0,0)
def add(p,q):
    out=dict(p)
    for m,c in q.items(): out[m]=out.get(m,0)+c
    return {m:c for m,c in out.items() if c}
def scale(p,c): return {m:v*c for m,v in p.items() if v*c}
def mul(p,q):
    out={}
    for m,c in p.items():
        for n,d in q.items():
            k=tuple(x+y for x,y in zip(m,n))
            out[k]=out.get(k,0)+c*d
    return {m:c for m,c in out.items() if c}
def power(p,k):
    out={Z:1}
    for _ in range(k): out=mul(out,p)
    return out
def variable(i): return {tuple(int(j==i) for j in range(4)):1}
def linear(a):
    out={}
    for i,c in enumerate(a): out=add(out,scale(variable(i),c))
    return out
def restrict(poly,form):
    at=next(i for i,c in enumerate(form) if c)
    substitution=linear([Fraction(-c,form[at]) if i!=at else 0 for i,c in enumerate(form)])
    out={}
    for m,c in poly.items():
        mon={Z:c}
        for i,k in enumerate(m): mon=mul(mon,power(substitution if i==at else variable(i),k))
        out=add(out,mon)
    return out

def saito_withdrawal():
    x,y,z,w=[variable(i) for i in range(4)]
    zero={}
    basis=[[x,y,z,w], [zero,mul(mul(y,add(x,y)),add(x,scale(y,2))),zero,zero],
           [zero,zero,mul(z,add(x,z)),mul(w,add(x,z))], [zero,zero,zero,mul(w,add(z,w))]]
    vectors=[(1,0,0,0),(0,1,0,0),(1,1,0,0),(1,2,0,0),(1,0,1,0),(0,0,1,0),(0,0,0,1),(0,0,1,1)]
    tests=0
    for a in vectors:
        for theta in basis:
            val={}
            for c,p in zip(a,theta): val=add(val,scale(p,c))
            assert restrict(val,a)=={}
            tests+=1
    det={}
    for perm in permutations(range(4)):
        inversions=sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))
        mon={Z:(-1)**inversions}
        for col,row in enumerate(perm): mon=mul(mon,basis[col][row])
        det=add(det,mon)
    Q={Z:1}
    for a in vectors: Q=mul(Q,linear(a))
    assert det==Q
    # Conditions on a generic degree-one logarithmic derivation: restrictions of theta(a).
    coefficients={}
    for a in vectors:
        for col in range(16):
            row,j=divmod(col,4)
            val=restrict(scale(variable(j),a[row]),a)
            for mon,c in val.items():
                key=(a,mon)
                coefficients.setdefault(key,[0]*16)[col]=c
    dimension=16-len(reduced(list(coefficients.values()),16)[1])
    assert dimension==1
    return dict(tangency_checks=tests,determinant_equals_Q=True,degrees=[1,3,2,2],
                linear_logarithmic_derivation_dimension=dimension,degree_eight_terms=len(Q))


def main():
    results=dict(arithmetic='rational and sparse integer polynomials; standard library only',
                 independence='candidate checker and earlier audit code not imported',
                 finite_tests_do_not_replace_universal_proof=True,
                 support=support_enumeration(),rank3_pool=rank3_pool_check(),
                 saito=saito_withdrawal(),**fixture_checks())
    print(json.dumps(results,indent=2))
if __name__=='__main__': main()
