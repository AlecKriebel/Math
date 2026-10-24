#!/usr/bin/env python3
"""Exact Q-homology of explicit finite-index Hydra subgroups; stdlib only."""
from fractions import Fraction as Q
import argparse, json, math
from pathlib import Path


def theta_words(m, r):
    out = [[i] for i in range(m)]
    for _ in range(r):
        out = [[j for k in w for j in ([k] if k == 0 else [k, k - 1])] for w in out]
    return out


def sparse_reduce(vec, basis):
    out = {i: Q(x) for i, x in vec.items() if x}
    for p, row in sorted(basis.items()):
        a = out.get(p, 0)
        if not a:
            continue
        for j, x in row.items():
            v = out.get(j, 0) - a * x
            if v: out[j] = v
            elif j in out: del out[j]
    return out


def span_basis(rows):
    basis = {}
    for row in rows:
        rem = sparse_reduce(row, basis)
        if rem:
            p = min(rem)
            a = rem[p]
            basis[p] = {j: x / a for j, x in rem.items()}
    return basis


def dot(a,b):
    return sum(x * b.get(i, 0) for i, x in a.items())


def add(*terms):
    out = {}
    for scale, row in terms:
        for i, x in row.items():
            v = out.get(i,0) + scale*x
            if v: out[i] = v
            elif i in out: del out[i]
    return out


def encode(row):
    return {str(i): str(x) for i,x in sorted(row.items())}


def run(m, p=2):
    # Full abelian mod-p characteristic fiber cover.
    q = p**m
    def digits(v):
        return [(v // p**i) % p for i in range(m)]
    def vertex(ds): return sum(x * p**i for i,x in enumerate(ds))
    def step(v, i):
        ds=digits(v); ds[i]=(ds[i]+1)%p
        return vertex(ds)
    def path(v):
        return [i for i,d in enumerate(digits(v)) for _ in range(d)]
    # Tree has edge from the word with the last letter of path(v) deleted.
    tree = set()
    for v in range(1,q):
        word=path(v); i=word[-1]; ds=digits(v); ds[i]-=1
        tree.add((vertex(ds),i))
    non_tree=[(v,i) for v in range(q) for i in range(m) if (v,i) not in tree]
    ind={e:j for j,e in enumerate(non_tree)}
    n=len(non_tree)
    assert n == 1 + (m-1)*q
    # Unipotent Jordan block has p-power order, bounded by first p-power >= m.
    r=1
    while r<m: r*=p
    tw=theta_words(m,r)
    for i,w in enumerate(tw):
        counts=[w.count(j)%p for j in range(m)]
        assert counts==[int(j==i) for j in range(m)]
    def walk(word, start=0, full=False):
        v=start; out={}
        for i in word:
            edge=(v,i)
            j=v*m+i if full else ind.get(edge)
            if j is not None: out[j]=out.get(j,0)+1
            v=step(v,i)
        return v,out
    mapped_paths=[]
    ordinary_paths=[]
    for v in range(q):
        vw=path(v)
        end,a=walk([j for i in vw for j in tw[i]])
        assert end==v
        mapped_paths.append(a)
        ordinary_paths.append(walk(vw, full=True)[1])
    columns=[]
    # Fundamental cycle is root->v, the edge (v,i), then inverse root->w.
    for e,j in ind.items():
        v,i=e; w=step(v,i)
        end,a=walk(tw[i],v)
        assert end==w
        col=add((1,mapped_paths[v]),(1,a),(-1,mapped_paths[w]),(-1,{j:1}))
        columns.append(col)
    basis=span_basis(columns)
    witnesses=[]
    for i in range(m):
        end,target=walk([i]*p)
        assert end==0
        rem=sparse_reduce(target,basis)
        if rem:
            free=min(rem)
            ell={free:Q(1)}
            for pivot,row in sorted(basis.items(),reverse=True):
                val=-sum(x*ell.get(k,0) for k,x in row.items() if k!=pivot)
                if val: ell[pivot]=val
            val=dot(ell,target)
            assert val
            ell={k:x/val for k,x in ell.items()}
            assert all(dot(ell,c)==0 for c in columns)
            assert dot(ell,target)==1
            witnesses.append({'generator':i+1,'power':p,'visible':True,'functional':encode(ell)})
        else:
            witnesses.append({'generator':i+1,'power':p,'visible':False})
    return {'m':m,'p':p,'fiber_cover_degree':q,'stable_letter_power':r,
            'subgroup_index':q*r,'fiber_rank':n,'coinvariant_dimension':n-len(basis),
            'H1_subgroup_Q_dimension':1+n-len(basis),'basis_edges':non_tree,
            'theta_word_lengths':list(map(len,tw)), 'witnesses':witnesses}

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--max-rank',type=int,default=5)
    parser.add_argument('--prime',type=int,default=2); parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    assert args.prime in (2,3,5,7)
    data={'scope':'Characteristic mod-p fiber cover followed by theta^r, exact rational homology; no virtual-specialness claim',
          'results':[run(m,args.prime) for m in range(1,args.max_rank+1)]}
    text=json.dumps(data,indent=2)+'\n'
    if args.output: args.output.write_text(text)
    else: print(text)
    print(json.dumps([{'m':x['m'],'index':x['subgroup_index'],'b1':x['H1_subgroup_Q_dimension'],'visible':[w['generator'] for w in x['witnesses'] if w['visible']]} for x in data['results']]))
