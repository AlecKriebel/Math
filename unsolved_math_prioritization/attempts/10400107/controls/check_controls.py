#!/usr/bin/env python3
"""Exact, bounded regression controls; not a proof of the infinite CW theorem.
Python >=3.10, standard library only. No downloads or randomness.
Run: python3 controls/check_controls.py > controls/CONTROL_RESULTS.json
"""
from collections import Counter
from functools import lru_cache
from itertools import product
import json

MODELS = {
    'T1': [[0]],
    'T2': [[x for y in range(2)] for x in range(2)],
    'R3': [[(2*y-x)%3 for y in range(3)] for x in range(3)],
    'R4': [[(2*y-x)%4 for y in range(4)] for x in range(4)],
    'A5_t2': [[(2*x-y)%5 for y in range(5)] for x in range(5)],
}
counts = Counter()

def clean(c):
    return {k:v for k,v in c.items() if v}

def deg(w):
    return any(a==b for a,b in zip(w,w[1:]))

def boundary(w, table, normalized=False):
    c=Counter()
    for i,x in enumerate(w):
        sign=(-1)**(i+1)
        d0=w[:i]+w[i+1:]
        d1=tuple(table[a][x] for a in w[:i])+w[i+1:]
        if not normalized or not deg(d0): c[d0]+=sign
        if not normalized or not deg(d1): c[d1]-=sign
    return clean(c)

def apply_boundary(c,table,normalized=False):
    ans=Counter()
    for w,v in c.items():
        for z,b in boundary(w,table,normalized).items(): ans[z]+=v*b
    return clean(ans)

def normalize_chain(c):
    return {w:v for w,v in c.items() if not deg(w)}

def image_chain(c,f):
    ans=Counter()
    for w,v in c.items():
        z=tuple(f[x] for x in w)
        if not deg(z): ans[z]+=v
    return clean(ans)

basis_sizes={}
for name,table in MODELS.items():
    q=len(table)
    for x in range(q):
        assert table[x][x]==x; counts['idempotency']+=1
        assert sorted(table[y][x] for y in range(q))==list(range(q));counts['bijective_right_translations']+=1
    for x,y,z in product(range(q),repeat=3):
        assert table[table[x][y]][z]==table[table[x][z]][table[y][z]]
        counts['self_distributivity']+=1
    basis_sizes[name]=[]
    for n in range(6):
        words=list(product(range(q),repeat=n))
        nd=[w for w in words if not deg(w)]
        assert len(nd)==(1 if n==0 else q*(q-1)**(n-1))
        basis_sizes[name].append(len(nd))
        for w in words:
            b=boundary(w,table)
            assert not apply_boundary(b,table);counts['rack_d_squared_zero']+=1
            if deg(w):
                assert all(deg(z) for z in b);counts['degenerate_subcomplex']+=1
            else:
                qb=boundary(w,table,True)
                assert not apply_boundary(qb,table,True);counts['quandle_d_squared_zero']+=1
                assert normalize_chain(b)==qb;counts['projection_commutes_boundary']+=1

homs={}
noninjective_nondegenerate_to_degenerate=0
for src,st in MODELS.items():
    for dst,tt in MODELS.items():
        ns,nt=len(st),len(tt); fs=[]
        for f in product(range(nt),repeat=ns):
            if all(f[st[x][y]]==tt[f[x]][f[y]] for x,y in product(range(ns),repeat=2)):
                fs.append(f)
        homs[src+'->'+dst]=len(fs)
        for f in fs:
            for n in range(5):
                for w in product(range(ns),repeat=n):
                    if deg(w): continue
                    fw=tuple(f[x] for x in w)
                    image={} if deg(fw) else {fw:1}
                    assert apply_boundary(image,tt,True)==image_chain(boundary(w,st,True),f)
                    counts['naturality_chain_equations']+=1
                    if deg(fw): noninjective_nondegenerate_to_degenerate+=1

# Coordinates are integer multiples of 1/2, stored as 0,1,2.
# Enumerate every shortening rewrite and compare every terminal form.
geometry={}
for name in ['T1','T2','R3','R4']:
    table=MODELS[name]; q=len(table)
    def act(prefix,a,k):
        ans=[]
        for t,x in prefix:
            for _ in range(k): x=table[x][a]
            ans.append((t,x))
        return tuple(ans)
    @lru_cache(None)
    def terminals(w):
        children=[]
        for i,(t,x) in enumerate(w):
            if t==0: children.append(w[:i]+w[i+1:])
            elif t==2: children.append(act(w[:i],x,1)+w[i+1:])
        for i in range(len(w)-1):
            t,a=w[i];u,b=w[i+1]
            if a==b:
                k,r=divmod(t+u,2)
                children.append(act(w[:i],a,k)+(((r,a),) if r else ())+w[i+2:])
        if not children: return frozenset([w])
        out=set()
        for v in children:
            assert len(v)<len(w)
            out.update(terminals(v))
        assert len(out)==1, (name,w,out)
        return frozenset(out)
    roots=0; equal_sum_checks=0
    alphabet=list(product(range(3),range(q)))
    for n in range(5):
        for w in product(alphabet,repeat=n):
            roots+=1;nf=terminals(w)
            for i in range(n-1):
                t,a=w[i];u,b=w[i+1]
                if a!=b:continue
                for r in range(3):
                    s=t+u-r
                    if 0<=s<=2:
                        v=w[:i]+((r,a),(s,a))+w[i+2:]
                        assert terminals(v)==nf
                        equal_sum_checks+=1
    geometry[name]={'grid_denominator':2,'max_word_length':4,'root_words':roots,
                    'equal_sum_relations_checked':equal_sum_checks,
                    'cached_states':terminals.cache_info().currsize}
    counts['geometric_root_words']+=roots
    counts['geometric_equal_sum_relations']+=equal_sum_checks

# Required negative controls and low-degree conventions.
assert basis_sizes['T1']==[1,1,0,0,0,0]
assert all(not boundary((0,)*n,MODELS['T1']) for n in range(1,6))
# Literal cone of a disjoint union of positive-dimensional cubes has H_2 unchanged;
# with singleton rack it is Z, whereas normalized C_2=C_3=0 gives H_2=0.
negative_controls={'singleton_correct_space':'S^1', 'singleton_quandle_H2':'0',
    'singleton_literal_Nosaka_cone_H2':'Z (by cofiber LES)',
    'naive_degenerate_subcomplex_quotient':'point for a nonempty quandle',
    'naive_quotient_singleton_H1':'0, instead of required Z',
    'noninjective_images_collapsing_cells':noninjective_nondegenerate_to_degenerate}
assert noninjective_nondegenerate_to_degenerate>0
print(json.dumps({'result':'PASS','counts':dict(sorted(counts.items())),
 'normalized_basis_sizes_degrees_0_to_5':basis_sizes,'homomorphism_counts':homs,
 'geometry':geometry,'negative_controls':negative_controls,
 'limits':{'chain_degree_max':5,'naturality_degree_max':4,'geometry_coordinate_grid':[0,'1/2',1],
  'geometry_degree_max':4,'quandles':list(MODELS),
  'proof_limits':'Finite controls test formulas and catch errors. They do not establish the all-quandle/all-degree CW structure or replace the written proof.',
  'arithmetic':'integer exact; no random, floating point, network or external packages'}},indent=2,sort_keys=True))
