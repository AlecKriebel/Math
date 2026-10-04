#!/usr/bin/env python3
"""Exact, finite certificate construction for the explicitly scoped rank <= 4 model.

Requires Python 3.10+ and SymPy 1.14.0. No network, floating point, or Groebner
basis oracle is used. Algebraic operations are affine elimination and division
by explicitly nonvanishing linear forms. Run --check to replay the receipt.
"""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path
import sympy as S

ROOT = Path(__file__).resolve().parent

def transforms(t, bar):
    k, j, i = t
    return {(k,j,i), (j,bar[i],bar[k]), (bar[i],k,bar[j]),
            (bar[j],bar[k],bar[i]), (bar[k],i,j), (i,bar[j],k)}

def support_orbits(n, bar):
    remaining = set(it.product(range(1,n), repeat=3))
    out = []
    while remaining:
        orbit = {min(remaining)}
        while True:
            expanded = set().union(*(transforms(t,bar) for t in orbit))
            if expanded == orbit:
                break
            orbit = expanded
        assert orbit <= remaining
        out.append(tuple(sorted(orbit)))
        remaining -= orbit
    return out

def is_forest(n, edges):
    parent = list(range(2*n))
    def root(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for i,j in edges:
        x,y = root(i),root(n+j)
        if x == y:
            return False
        parent[x] = y
    return True

def canonical(n, graphs):
    a,b = {},{}
    for i,j,k in it.product(range(n),repeat=3):
        aa,bb = [0]*n,[0]*n
        if (i,j) in graphs[k]:
            if k == 0:
                aa[i] = 1
            elif i == 0:
                aa[0] = 1
            elif j == 0:
                bb[0] = 1
            else:
                component = {i}
                while True:
                    expanded = set(component)
                    for u,v in graphs[k]:
                        if (u,v) != (i,j) and (u in component or n+v in component):
                            expanded.update((u,n+v))
                    if expanded == component:
                        break
                    component = expanded
                for s in range(n):
                    aa[s] = int(s in component)
                    bb[s] = -int(n+s in component)
        for s in range(n):
            a[i,j,s,k], b[i,j,s,k] = aa[s],bb[s]
        # Exact edge-incidence check of source equation (3.4).
        for u,v in graphs[k]:
            assert aa[u]+bb[v] == int(u==i and v==j)
    return a,b

def model(n,bar,bits,orbits):
    present = set(t for bit,orbit in zip(bits,orbits) if bit for t in orbit)
    graphs = [[] for _ in range(n)]
    for k,j,i in it.product(range(n),repeat=3):
        if 0 in (k,j,i):
            edge = (i==0 and k==bar[j]) or (k==0 and j==i) or (j==0 and k==i)
        else:
            edge = (k,j,i) in present
        if edge:
            graphs[k].append((i,j))
    if not all(is_forest(n,g) for g in graphs):
        return None
    a,b = canonical(n,graphs)
    d = [S.Integer(1)]+list(S.symbols('d1:'+str(n)))
    # Source (3.7), with normalized d0 = 1 and its conjugate index retained.
    N = {(i,j,k):S.expand(sum((a[i,bar[j],s,k]+b[i,bar[j],s,k])*d[s]
                               for s in range(n)))
         for i,j,k in it.product(range(n),repeat=3)}
    E = set()
    counts = {}
    def add(category,p):
        p = S.expand(p)
        counts[category] = counts.get(category,0)+1
        if p != 0:
            E.add(p)
    for i in range(n):
        add('dimension_dual',d[i]-d[bar[i]])
    for k,j,i in it.product(range(n),repeat=3):
        for kk,jj,ii in sorted(transforms((k,j,i),bar)):
            add('reciprocity',N[k,j,i]*d[i]-N[kk,jj,ii]*d[ii])
        add('coefficient_dual',N[k,j,i]-N[bar[j],bar[k],bar[i]])
        if (i,j) not in graphs[k]:
            assert N[k,j,i] == 0
    for i,j in it.product(range(n),repeat=2):
        add('unit',N[i,j,0]-int(i==bar[j])*d[i])
        add('trace',d[i]*d[j]-sum(N[i,j,s]*d[s] for s in range(n)))
    for i,j,k,l in it.product(range(n),repeat=4):
        add('associativity',sum(N[i,j,s]*N[s,k,l]-N[i,s,l]*N[j,k,s]
                                for s in range(n)))
    # Both displayed equations (3.5) and (3.6) in arXiv v1 are identical.
    # On the exact support stratum their nonzero leading factor can be canceled.
    for i,j,k,x,y,z in it.product(range(n),repeat=6):
        if (x,y) not in graphs[z]:
            continue
        add('displayed_move',sum(
            a[j,k,s,z]*N[s,i,x]+b[j,k,s,z]*N[s,i,y]
            -a[bar[i],j,s,bar[x]]*N[s,bar[k],bar[y]]
            -b[bar[i],j,s,bar[x]]*N[s,bar[k],z] for s in range(n)))
        # Also compare source proof expressions (3.12) and (3.16).
        # This guards against relying on the duplicated display (3.5)/(3.6).
        add('third_expansion_move',sum(
            a[j,k,s,z]*N[s,i,x]+b[j,k,s,z]*N[s,i,y]
            -a[k,bar[i],s,y]*N[s,bar[j],bar[z]]
            -b[k,bar[i],s,y]*N[s,bar[j],bar[x]] for s in range(n)))
    H = set(d[1:]+[N[k,j,i] for k in range(n) for i,j in graphs[k]])
    return d,N,sorted(E,key=str),sorted(H,key=str),counts,present

def polynomial_degree(p,variables):
    return S.Poly(p,*variables,domain=S.QQ).total_degree()

def affine_certificate(variables,E,H):
    """Sound elementary localized-ideal elimination, or stop as inconclusive.

    Each new equation is an old equation modulo already justified affine
    equations, divided only by factors explicitly required nonzero. All
    substitutions are simultaneous. Constants are exact rationals.
    """
    constraints = []
    rounds = []
    while True:
        values = tuple(variables)
        if constraints:
            solution = S.linsolve(constraints,variables)
            if solution == S.EmptySet:
                return {'disposition':'empty','reason':'inconsistent affine equations',
                        'rounds':rounds}
            values = next(iter(solution))
        substitution = dict(zip(variables,values))
        reduced_H = sorted({S.expand(f.subs(substitution,simultaneous=True)) for f in H},key=str)
        if S.Integer(0) in reduced_H:
            return {'disposition':'empty','reason':'required nonzero form vanishes',
                    'rounds':rounds}
        new = set()
        unresolved = []
        for p in E:
            q = S.expand(p.subs(substitution,simultaneous=True))
            if q == 0:
                continue
            before = q
            factors = []
            for f in reduced_H:
                if not f.free_symbols:
                    continue
                while q != 0 and q.free_symbols:
                    quotient,remainder = S.div(q,f,*variables,domain=S.QQ)
                    assert S.expand(q-quotient*f-remainder) == 0
                    if remainder != 0:
                        break
                    q = S.expand(quotient)
                    factors.append(str(f))
            if not q.free_symbols:
                return {'disposition':'empty','reason':'nonzero constant after allowed divisions',
                        'witness':{'reduced_equation':str(before),'divisors':factors,
                                   'constant':str(q)},'rounds':rounds}
            if polynomial_degree(q,variables)==1:
                new.add(q)
            else:
                unresolved.append(q)
        if new:
            ordered = sorted(new,key=str)
            # Every listed equation follows by affine substitution and unit division.
            rounds.append([str(q) for q in ordered])
            constraints.extend(ordered)
            assert len(rounds) <= len(variables)+1
            continue
        if unresolved:
            raise AssertionError('INCONCLUSIVE: uneliminated nonlinear equations '+str(unresolved))
        # Every original equation is identically zero on this affine space,
        # and each required nonzero factor is a nonzero polynomial there.
        for p in E:
            assert S.expand(p.subs(substitution,simultaneous=True))==0
        basis = [S.expand(x-v) for x,v in zip(variables,values) if x!=v]
        free = set().union(*(v.free_symbols for v in values))
        return {'disposition':'affine_open','dimension':len(free),
                'affine_generators':[str(q) for q in basis],
                'excluded_forms':sorted({str(f) for f in reduced_H if f.free_symbols}),
                'normalized_dimension_sum':str(S.expand(1+sum(values))),
                'rounds':rounds}

def label_key(n,bar,present):
    keys=[]
    for perm in it.permutations(range(1,n)):
        p=(0,)+perm
        if all(p[bar[i]]==bar[p[i]] for i in range(n)):
            keys.append(tuple(sorted(tuple(p[x] for x in t) for t in present)))
    return min(keys)

def run():
    receipt={'model':'normalized nonzero-dimension canonical forest charts for the equations and all three W-expansion comparisons in Lu-Liu arXiv:2412.17790v1',
             'algorithm':'exact affine elimination and division only by prescribed nonzero linear forms',
             'families':[],'cases':[]}
    for n,bar in [(2,(0,1)),(3,(0,1,2)),(3,(0,2,1)),
                  (4,(0,1,2,3)),(4,(0,2,1,3))]:
        orbits=support_orbits(n,bar)
        summary={'rank':n,'involution':list(bar),'support_bits':len(orbits),
                 'patterns':2**len(orbits),'forests':0,'empty':0,'nonempty':0,
                 'dimensions':{}}
        label_classes=set()
        for bits in it.product((0,1),repeat=len(orbits)):
            m=model(n,bar,bits,orbits)
            if m is None:
                continue
            summary['forests']+=1
            d,N,E,H,counts,present=m
            c=affine_certificate(d[1:],E,H)
            c.update({'rank':n,'involution':list(bar),'bits':''.join(map(str,bits))})
            receipt['cases'].append(c)
            if c['disposition']=='empty':
                summary['empty']+=1
            else:
                summary['nonempty']+=1
                dimension=str(c['dimension'])
                summary['dimensions'][dimension]=summary['dimensions'].get(dimension,0)+1
                assert c['normalized_dimension_sum']!='0'
                label_classes.add(label_key(n,bar,present))
        summary['nonempty_label_classes']=len(label_classes)
        receipt['families'].append(summary)
    expected=[(2,0,2,2),(13,4,9,5),(3,1,2,2),(358,289,69,15),(50,41,9,9)]
    for f,e in zip(receipt['families'],expected):
        assert (f['forests'],f['empty'],f['nonempty'],f['nonempty_label_classes'])==e
    # Rank-two degeneration and the nonpositive rank-three point are explicit controls.
    assert any(c.get('affine_generators')==['d1 + 1','d2 + 1']
               for c in receipt['cases'] if c['rank']==3)
    return receipt

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    receipt=run()
    payload=(json.dumps(receipt,indent=2,sort_keys=True)+'\n').encode()
    path=ROOT/'verification.json'
    if args.check:
        assert path.read_bytes()==payload,'Receipt mismatch'
    else:
        path.write_bytes(payload)
    print(json.dumps({'status':'PASS','cases':len(receipt['cases']),
                      'families':receipt['families'],
                      'verification_sha256':hashlib.sha256(payload).hexdigest()},sort_keys=True))
if __name__=='__main__':
    main()
