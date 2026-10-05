#!/usr/bin/env python3
"""Exact reduced Khovanov cube controls; no external packages or knot database.

0 smoothing = (a,b),(c,d), 1 smoothing = (a,d),(b,c).
Frobenius algebra: Z[x]/x^2; marked circle always labelled x.
Orientational/quantum grading shifts are omitted: total rank is unchanged.
This program does NOT decide ribbonness or prove the universal conjecture.
"""
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json


def circles(pd, state):
    labels = {x for crossing in pd for x in crossing}
    parent = {x: x for x in labels}
    def root(x):
        while x != parent[x]:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def join(x, y):
        parent[root(x)] = root(y)
    for k, (a,b,c,d) in enumerate(pd):
        for x,y in ([(a,d),(b,c)] if state >> k & 1 else [(a,b),(c,d)]):
            join(x,y)
    groups = defaultdict(set)
    for x in labels:
        groups[root(x)].add(x)
    return tuple(sorted((frozenset(v) for v in groups.values()), key=min))


def build_cube(pd, marked=1):
    if not pd:
        return [[('unknot', 0)]], [[]]
    counts = Counter(x for crossing in pd for x in crossing)
    assert all(v == 2 for v in counts.values()) and marked in counts
    n = len(pd)
    states = [circles(pd, s) for s in range(1 << n)]
    bases = [[] for _ in range(n+1)]
    masks = []
    for s, cs in enumerate(states):
        bp = next(k for k,c in enumerate(cs) if marked in c)
        allowed = [m for m in range(1 << len(cs)) if m >> bp & 1]
        masks.append(allowed)
        bases[s.bit_count()].extend((s,m) for m in allowed)
    indices = [{item:k for k,item in enumerate(b)} for b in bases]
    diffs = [[{} for _ in b] for b in bases]
    for h,basis in enumerate(bases[:-1]):
        for col,(s,m) in enumerate(basis):
            src = states[s]
            for k in range(n):
                if s >> k & 1:
                    continue
                t = s | (1 << k)
                dst = states[t]
                common = set(src) & set(dst)
                lost = [i for i,c in enumerate(src) if c not in common]
                gained = [i for i,c in enumerate(dst) if c not in common]
                base = 0
                for c in common:
                    base |= ((m >> src.index(c)) & 1) << dst.index(c)
                outputs = []
                if len(lost) == 2 and len(gained) == 1:
                    degree = sum((m >> i) & 1 for i in lost)
                    if degree <= 1:
                        outputs = [base | (degree << gained[0])]
                elif len(lost) == 1 and len(gained) == 2:
                    if (m >> lost[0]) & 1:
                        outputs = [base | (1 << gained[0]) | (1 << gained[1])]
                    else:
                        outputs = [base | (1 << gained[0]), base | (1 << gained[1])]
                else:
                    raise AssertionError(('not a merge or split',s,t,lost,gained))
                sign = (-1) ** ((s & ((1 << k)-1)).bit_count())
                for out in outputs:
                    assert out in masks[t], 'marked-circle subcomplex not preserved'
                    row = indices[h+1][(t,out)]
                    diffs[h][col][row] = diffs[h][col].get(row,0) + sign
    return bases, diffs


def square_zero(diffs):
    products = 0
    for h in range(len(diffs)-2):
        for column in diffs[h]:
            accum = defaultdict(int)
            for middle,a in column.items():
                for row,b in diffs[h+1][middle].items():
                    accum[row] += a*b
                    products += 1
            assert all(v == 0 for v in accum.values()), ('d squared nonzero',h)
    return products


def column_rank(columns, p=0):
    """Sparse exact column echelon form, over Q when p=0, otherwise F_p."""
    pivots = {}
    for c in columns:
        v = {i: (a % p if p else Fraction(a)) for i,a in c.items()}
        v = {i:a for i,a in v.items() if a}
        while v:
            pivot = min(v)
            if pivot not in pivots:
                factor = pow(v[pivot], -1, p) if p else 1/v[pivot]
                pivots[pivot] = {i: (a*factor % p if p else a*factor) for i,a in v.items()}
                break
            factor = v[pivot]
            for i,a in pivots[pivot].items():
                value = v.get(i,0) - factor*a
                if p:
                    value %= p
                if value:
                    v[i] = value
                elif i in v:
                    del v[i]
    return len(pivots)


def calculate(pd, p=0, marked=1):
    bases,diffs = build_cube(pd,marked)
    square_products = square_zero(diffs)
    dims = list(map(len,bases))
    ranks = [column_rank(d,p) for d in diffs]
    homology = [d-ranks[h]-(ranks[h-1] if h else 0) for h,d in enumerate(dims)]
    assert all(h>=0 for h in homology)
    canonical = json.dumps(diffs,sort_keys=True,separators=(',',':')).encode()
    return dict(field='Q' if p==0 else 'F_'+str(p),chain_dimensions=dims,
                differential_ranks=ranks,homology_dimensions_cube_degree=homology,
                total_reduced_rank=sum(homology),integer_d_squared_zero=True,
                checked_composition_terms=square_products,differential_sha256=hashlib.sha256(canonical).hexdigest())


def mirror(pd):
    return [(b,c,d,a) for a,b,c,d in pd]


def connected_sum(first, second):
    """Cut arc 1 in each knot, then cross-connect its two cut ends."""
    offset = max(x for c in first for x in c)
    a = [list(c) for c in first]
    b = [[x+offset for x in c] for c in second]
    ia = [(i,j) for i,c in enumerate(a) for j,x in enumerate(c) if x==1]
    ib = [(i,j) for i,c in enumerate(b) for j,x in enumerate(c) if x==1+offset]
    assert len(ia)==len(ib)==2
    i,j = ia[0]; a[i][j] = offset+1
    i,j = ib[0]; b[i][j] = 1
    return a+b


def braid_closure(strands, word):
    """Build a PD diagram from a downward braid; require every strand participates."""
    top=list(range(1,strands+1)); active=top[:]; nxt=strands+1; pd=[]
    for generator in word:
        k=abs(generator)-1
        assert 0 <= k < strands-1
        tl,tr=active[k:k+2]; bl,br=nxt,nxt+1; nxt+=2
        pd.append([tr,tl,bl,br] if generator>0 else [tl,bl,br,tr])
        active[k:k+2]=[bl,br]
    assert all(x not in top for x in active), 'unused strand not supported'
    close=dict(zip(active,top))
    return [tuple(close.get(x,x) for x in c) for c in pd]


# Small explicitly named braid witnesses, not a copied census or source PD table.
TREFOIL = braid_closure(2,[-1,-1,-1])
STEVEDORE = braid_closure(4,[-1,-1,-2,1,3,-2,3])
SIX_TWO = braid_closure(3,[-1,-1,-1,2,-1,2])


def run_controls():
    examples = [('unknot',[],1),('trefoil',TREFOIL,3),('mirror_trefoil',mirror(TREFOIL),3),
                ('stevedore_6_1',STEVEDORE,9),('negative_control_6_2',SIX_TWO,11),
                ('square_knot',connected_sum(TREFOIL,mirror(TREFOIL)),9)]
    out = []
    for name,pd,expected in examples:
        fields=[]
        for p in (0,2,3,5):
            result=calculate(pd,p)
            assert result['total_reduced_rank']==expected,(name,p,result)
            fields.append(result)
        # Redundant diagram controls: crossing order, cyclic start, and basepoint.
        if pd:
            for variant in (pd[::-1],pd[1:]+pd[:1]):
                assert calculate(variant,3)['total_reduced_rank']==expected
            assert calculate(pd,3,marked=max(x for c in pd for x in c))['total_reduced_rank']==expected
        out.append(dict(name=name,pd=pd,expected_reduced_rank=expected,computations=fields))
    return dict(examples=out,status='PASS',scope='Small exact knot controls, not universal proof or ribbon-decision algorithm.')


if __name__ == '__main__':
    print(json.dumps(run_controls(),indent=2))
