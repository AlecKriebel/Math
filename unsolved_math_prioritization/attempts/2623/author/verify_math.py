#!/usr/bin/env python3
"""Exact finite controls for KOU-21.114; no downloaded data or dependencies.

This is a reproducible bounded check, not a proof of a uniform derived-length bound.
"""
import hashlib
import itertools
import json
from collections import Counter, deque
from pathlib import Path


class Group:
    def __init__(self, name, elements, multiply):
        self.name = name
        self.elements = tuple(elements)
        self.index = {x:i for i,x in enumerate(elements)}
        self.n = len(elements)
        self.t = tuple(tuple(self.index[multiply(x,y)] for y in elements) for x in elements)
        assert all(self.t[0][x] == x == self.t[x][0] for x in range(self.n))
        self.inv = tuple(next(y for y in range(self.n) if self.t[x][y] == self.t[y][x] == 0) for x in range(self.n))
        self.all = frozenset(range(self.n))

    def verify_axioms(self):
        t,n = self.t,self.n
        for x in range(n):
            for y in range(n):
                xy=t[x][y]
                for z in range(n):
                    assert t[xy][z] == t[x][t[y][z]], (self.name,x,y,z)

    def closure(self, generators):
        gens=tuple(set(generators) | {self.inv[x] for x in generators})
        found={0};todo=[0]
        for x in todo:
            for y in gens:
                z=self.t[x][y]
                if z not in found:found.add(z);todo.append(z)
        return frozenset(found)

    def commutator(self, x,y):
        t=self.t
        return t[t[t[self.inv[x]][self.inv[y]]][x]][y]

    def comm(self,A,B):
        return self.closure({self.commutator(x,y) for x in A for y in B})

    def derived(self,A):return self.comm(A,A)
    def ab_order(self,A):return len(A)//len(self.derived(A))

    def subgroups(self):
        """Breadth-first adjoining one element, one representative per left coset xH.
        Every subgroup has a finite generating sequence; induction proves completeness.
        """
        identity=frozenset({0})
        known={identity:()};todo=[identity]
        for H in todo:
            remaining=set(self.all-H)
            while remaining:
                x=min(remaining)
                remaining.difference_update(self.t[x][h] for h in H)
                gens=known[H]+(x,)
                K=self.closure(gens)
                if K not in known:known[K]=gens;todo.append(K)
        return known

    def series(self):
        der=[self.all]
        while len(der[-1])>1:
            nxt=self.derived(der[-1]);assert nxt!=der[-1];der.append(nxt)
        lower=[self.all]
        while len(lower[-1])>1:
            nxt=self.comm(lower[-1],self.all);assert nxt!=lower[-1];lower.append(nxt)
        return [len(x) for x in der],[len(x) for x in lower]

    def table_hash(self):
        raw=json.dumps(self.t,separators=(',',':')).encode()
        return hashlib.sha256(raw).hexdigest()


def cyclic_holomorph(p,n,full=True):
    m=p**n
    units=tuple(u for u in range(m) if u%p == 1) if p>2 else tuple(range(1,m,2))
    if not full:units=(1,m-1)
    return Group(f"C{m}_semidirect_"+("SylowAut" if full else "inversion"),
                 tuple((a,u) for a in range(m) for u in units),
                 lambda x,y:((x[0]+x[1]*y[0])%m,x[1]*y[1]%m))


def cyclic(p):
    return Group(f"C{p}",tuple(range(p)),lambda x,y:(x+y)%p)


def wreath(G,p):
    el=tuple((v,k) for v in itertools.product(range(G.n),repeat=p) for k in range(p))
    def mul(x,y):
        a,k=x;b,l=y
        return tuple(G.t[a[i]][b[(i-k)%p]] for i in range(p)),(k+l)%p
    return Group(f"({G.name})_wr_C{p}",el,mul)


def unitriangular(n,p):
    positions=tuple((i,j) for i in range(n) for j in range(i+1,n))
    pos={ij:k for k,ij in enumerate(positions)}
    def mul(a,b):
        return tuple((a[pos[i,j]]+b[pos[i,j]]+sum(a[pos[i,k]]*b[pos[k,j]] for k in range(i+1,j)))%p for i,j in positions)
    return Group(f"UT{n}({p})",tuple(itertools.product(range(p),repeat=len(positions))),mul)


def inspect(G, exhaustive=True):
    G.verify_axioms()
    der,low=G.series()
    result={'name':G.name,'order':G.n,'abelianization_order':G.ab_order(G.all),
            'derived_series_orders':der,'lower_central_series_orders':low,
            'derived_length':len(der)-1,'nilpotency_class':len(low)-1,
            'multiplication_table_sha256':G.table_hash(),'all_associativity_triples_checked':G.n**3}
    if exhaustive:
        sg=G.subgroups(); data=[]
        for H,gens in sg.items():
            assert G.closure(gens)==H
            assert all(G.t[x][y] in H for x in H for y in H)
            data.append((len(H),G.ab_order(H)))
        maxab=max(a for n,a in data)
        aG=result['abelianization_order']
        result.update({'all_subgroups_enumerated':len(sg),'max_subgroup_abelianization_order':maxab,
                       'weakly_ab_maximal':maxab==aG,
                       'strictly_ab_maximal':all(a<aG for n,a in data if n<G.n),
                       'subgroup_order_abelianization_histogram':[[n,a,c] for (n,a),c in sorted(Counter(data).items())]})
    return result


def run():
    result={'scope':'Bounded exact controls only; no solution of KOU-21.114 is asserted.','cases':[], 'negative_controls':[]}
    for p,n in [(2,2),(2,3),(2,4),(3,2),(3,3),(5,2)]:
        G=cyclic_holomorph(p,n)
        r=inspect(G);assert r['weakly_ab_maximal'] and not r['strictly_ab_maximal']
        assert r['abelianization_order']==p**n and r['derived_length']==2 and r['nilpotency_class']==n
        result['cases'].append(r)
    D16=cyclic_holomorph(2,3,False)
    r=inspect(D16);assert not r['weakly_ab_maximal']; assert r['max_subgroup_abelianization_order']==8>r['abelianization_order']==4
    result['cases'].append(r)
    result['negative_controls'].append({'invalid_inference':'Weak ab-maximality is subgroup-closed','rejected_by':'C8 semidirect Aut(C8) contains its inversion subgroup D16','ambient_ab':8,'subgroup_ab':4,'cyclic_subgroup_ab':8})
    W2=wreath(cyclic(2),2)
    r=inspect(W2);assert r['weakly_ab_maximal'] and not r['strictly_ab_maximal'];result['cases'].append(r)
    W3=wreath(W2,2)
    r=inspect(W3,False)
    base=frozenset(i for i,x in enumerate(W3.elements) if x[1]==0)
    assert len(base)==64 and W3.ab_order(base)==16>r['abelianization_order']==8
    r['disqualifying_section']={'subgroup':'base W2 x W2','order':64,'derived_order':4,'abelianization_order':16}
    center=frozenset(x for x in W3.all if all(W3.t[x][y]==W3.t[y][x] for y in W3.all))
    assert len(center)==2 and center <= W3.derived(base)
    r['central_product_obstruction']={'center_order':2,'center_is_contained_in_base_derived':True}
    result['cases'].append(r)
    result['negative_controls'].append({'invalid_inference':'Iterating a regular wreath product preserves weak ab-maximality','rejected_by':'W3=(C2 wr C2) wr C2','base_ab':16,'ambient_ab':8})
    W3prime=wreath(cyclic(3),3)
    r=inspect(W3prime,False)
    base=frozenset(i for i,x in enumerate(W3prime.elements) if x[1]==0)
    assert W3prime.ab_order(base)==27>r['abelianization_order']==9
    r['disqualifying_section']={'subgroup':'base C3^3','order':27,'derived_order':1,'abelianization_order':27};result['cases'].append(r)
    U=unitriangular(4,2)
    r=inspect(U)
    assert not r['weakly_ab_maximal'] and r['abelianization_order']==8
    result['cases'].append(r)
    result['negative_controls'].append({'invalid_inference':'Unbounded nilpotency class disproves a uniform derived-length bound','rejected_by':'cyclic holomorphs have class n but derived length exactly 2'})
    result['negative_controls'].append({'invalid_inference':'Replace the non-strict inequality by a strict one','rejected_by':'D8 is weakly ab-maximal but has a proper cyclic C4 with equal abelianization order'})
    # Arbitrarily large integer exponent checks exercise the exact witness inequalities.
    checks=[]
    for p in [2,3,5,7,11]:
        for r in range(2,13):
            a=p**r; b=p**(p*(r-1))
            assert (b>a)==(p*(r-1)>r)
            if r>=3 or p>=3:assert b>a
            checks.append((p,r,a,b))
    result['wreath_inequality_samples']=len(checks)
    result['unitriangular_rectangular_witness_samples']=sum(1 for n in range(4,101) if (n//2)*(n-n//2)>n-1)
    assert result['unitriangular_rectangular_witness_samples']==97
    return result


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    result=run();target=Path(__file__).with_name('CHECK_RESULTS.json')
    if args.write:target.write_text(json.dumps(result,indent=2)+'\n')
    else:assert json.loads(target.read_text())==result,'Stored certificate differs from exact replay'
    print(json.dumps({'ok':True,'case_count':len(result['cases']),'negative_controls':len(result['negative_controls']),'subgroup_counts':{x['name']:x.get('all_subgroups_enumerated') for x in result['cases'] if 'all_subgroups_enumerated'in x}},indent=2))
