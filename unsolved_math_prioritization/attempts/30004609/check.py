#!/usr/bin/env python3
"""Exact, finite diagnostics for the proof; no external data or network reads.

Python 3 standard library suffices for lattice/graph tests. Optional SymPy is
used only by saito_checks. Finite tests are diagnostics, not the universal proof.
"""
from fractions import Fraction as F
from itertools import combinations, product
from functools import lru_cache
import json


def rref(rows, width):
    a = [[F(x) for x in row] for row in rows]
    i = 0
    for j in range(width):
        k = next((k for k in range(i, len(a)) if a[k][j]), None)
        if k is None:
            continue
        a[i], a[k] = a[k], a[i]
        z = a[i][j]
        a[i] = [x / z for x in a[i]]
        for k in range(len(a)):
            if k != i and a[k][j]:
                z = a[k][j]
                a[k] = [x - z*y for x,y in zip(a[k], a[i])]
        i += 1
        if i == len(a):
            break
    return tuple(tuple(row) for row in a[:i])


def nullspace(rows, width):
    a = rref(rows, width)
    pivots = [next(i for i,x in enumerate(row) if x) for row in a]
    out = []
    for j in range(width):
        if j not in pivots:
            v = [F(0)] * width
            v[j] = F(1)
            for row,p in zip(a,pivots):
                v[p] = -row[j]
            out.append(tuple(v))
    return out


class Configuration:
    def __init__(self, rows):
        self.rows = tuple(tuple(F(x) for x in row) for row in rows)
        self.n = len(rows)
        self.ambient = len(rows[0])
        self.full = (1 << self.n) - 1
        assert len({rref([a],self.ambient) for a in self.rows}) == self.n
        self.rank = len(self.basis(self.full))

    @lru_cache(None)
    def basis(self, mask):
        return rref([a for i,a in enumerate(self.rows) if mask>>i&1],self.ambient)

    def rk(self, mask):
        return len(self.basis(mask))

    @lru_cache(None)
    def close(self, mask):
        b = self.basis(mask)
        return sum(1 << i for i,a in enumerate(self.rows)
                   if len(rref(b+(a,),self.ambient)) == len(b))

    def lines(self):
        return sorted({self.close((1<<i)|(1<<j))
                       for i,j in combinations(range(self.n),2)})

    def flats(self):
        seen = {0}
        todo = [0]
        while todo:
            mask = todo.pop()
            for i in range(self.n):
                if not mask>>i&1:
                    new = self.close(mask|(1<<i))
                    if new not in seen:
                        seen.add(new)
                        todo.append(new)
        return sorted(seen,key=lambda m:(self.rk(m),m))

    def local_relations(self, line):
        ids = [i for i in range(self.n) if line>>i&1]
        ns = nullspace([[self.rows[i][j] for i in ids]
                        for j in range(self.ambient)],len(ids))
        return [tuple(v[ids.index(i)] if i in ids else F(0)
                      for i in range(self.n)) for v in ns]

    def analyze(self):
        lines = self.lines()
        nontrivial = [m for m in lines if m.bit_count()>=3]
        relations = [r for m in nontrivial for r in self.local_relations(m)]
        rr = len(rref(relations,self.n))
        edges = sum(m.bit_count() for m in nontrivial)
        adj = [set() for _ in range(self.n+len(nontrivial))]
        for k,m in enumerate(nontrivial):
            for i in range(self.n):
                if m>>i&1:
                    adj[i].add(self.n+k)
                    adj[self.n+k].add(i)
        seen=set(); components=0
        for v in range(len(adj)):
            if v not in seen:
                components+=1; todo=[v]; seen.add(v)
                while todo:
                    for w in adj[todo.pop()]:
                        if w not in seen:
                            seen.add(w);todo.append(w)
        flats=self.flats()
        ranks={m:self.rk(m) for m in flats}
        modular=[]
        for m in flats:
            if all(ranks[m]+ranks[k]==self.rk(m|k)+ranks[m&k]
                   for k in flats):
                modular.append(m)
        chains={0:[0]}
        for k in range(1,self.rank+1):
            for m in modular:
                if ranks[m]==k:
                    previous=next((q for q in chains
                                   if ranks[q]==k-1 and q&m==q),None)
                    if previous is not None:
                        chains[m]=chains[previous]+[m]
        chain=chains.get(self.full)
        hist={}
        for m in lines:
            hist[str(m.bit_count())]=hist.get(str(m.bit_count()),0)+1
        mobius={0:1}
        for m in flats[1:]:
            mobius[m]=-sum(v for k,v in mobius.items() if k&m==k)
        char=[sum(mobius[m] for m in flats if self.rank-ranks[m]==j)
              for j in range(self.rank+1)]
        return {'n':self.n,'rank':self.rank,'ambient':self.ambient,
                'rank_two_multiplicity_counts':hist,
                'relation_dimension':self.n-self.rank,
                'local_relation_span_rank':rr,
                'formal':rr==self.n-self.rank,
                'incidence_components':components,
                'incidence_cycle_rank':edges-len(adj)+components,
                'flat_count':len(flats),
                'characteristic_coefficients_ascending':char,
                'supersolvable':chain is not None,
                'modular_chain_indices':None if chain is None else
                    [[i for i in range(self.n) if m>>i&1] for m in chain],
                'nontrivial_lines_indices':[[i for i in range(self.n) if m>>i&1]
                                           for m in nontrivial]}


def attach_triangle(rows, attachment):
    """Add a new coordinate u and the two forms u and u+a_attachment."""
    rows=[tuple(a)+(0,) for a in rows]
    u=(0,)*(len(rows[0])-1)+(1,)
    rows += [u,tuple(x+y for x,y in zip(u,rows[attachment]))]
    return rows


def fixtures():
    tri=[(1,0),(0,1),(1,1)]
    quad=[(1,0),(0,1),(1,1),(1,2)]
    k4=[(1,0,0),(0,1,0),(0,0,1),(1,-1,0),(1,0,-1),(0,1,-1)]
    nonfano=k4+[(1,1,-1)]
    withdrawal=[(1,0,0,0),(0,1,0,0),(1,1,0,0),(1,2,0,0),
                (1,0,1,0),(0,0,1,0),(0,0,0,1),(0,0,1,1)]
    all2=tri
    for i in [0,3,1,7]:
        all2=attach_triangle(all2,i)
    quadtree=quad
    for i in [0,2,5,8]:
        quadtree=attach_triangle(quadtree,i)
    k4tree=k4
    for i in [0,6,4]:
        k4tree=attach_triangle(k4tree,i)
    return {'triple_pencil':tri,'four_pencil':quad,'k4_core':k4,
            'withdrawal_example':withdrawal,
            'withdrawal_deletion':[a for i,a in enumerate(withdrawal) if i!=4],
            'nonfano_two_cubic_boundary':nonfano,
            'all2_rank6_tree':all2,'one3_rank6_four_pencil_tree':quadtree,
            'one3_rank6_k4_tree':k4tree,
            'nonessential_k4':[a+(0,) for a in k4],
            'product_triple_four_pencil':
                 [a+(0,0) for a in tri]+[(0,0)+a for a in quad]}


def saito_checks():
    import sympy as s
    x,y,z,w=s.symbols('x y z w')
    variables=(x,y,z,w)
    forms=[x,y,x+y,x+2*y,x+z,z,w,z+w]
    basis=[(x,y,z,w), (0,y*(x+y)*(x+2*y),0,0),
           (0,0,z*(x+z),w*(x+z)), (0,0,0,w*(z+w))]
    det=s.factor(s.Matrix.hstack(*map(s.Matrix,basis)).det())
    Q=s.prod(forms)
    def restrict(value, form):
        v=next(v for v in variables if s.diff(form,v)!=0)
        return s.expand(value.subs(v,s.solve(form,v)[0]))
    remainders=[]
    for a in forms:
        for theta in basis:
            val=sum(s.diff(a,v)*c for v,c in zip(variables,theta))
            remainder=restrict(val,a)
            assert remainder==0
            remainders.append(str(remainder))
    assert s.expand(det-Q)==0
    # Exact D_1 dimension independently checks irreducibility.
    unknown=s.symbols('c:16')
    generic=[sum(unknown[4*i+j]*variables[j] for j in range(4)) for i in range(4)]
    eq=[]
    for a in forms:
        val=sum(s.diff(a,v)*c for v,c in zip(variables,generic))
        eq.extend(s.Poly(restrict(val,a),*variables).coeffs())
    mat,_=s.linear_eq_to_matrix(eq,unknown)
    dim=16-mat.rank()
    assert dim==1
    return {'withdrawal_basis':[list(map(str,t)) for t in basis],
            'degrees':[1,3,2,2], 'determinant':str(det),
            'determinant_equals_Q':True,
            'logarithmic_divisibility_checks':len(remainders),
            'degree_one_derivation_dimension':dim,
            'deletion_factor_sizes':[4,3]}


def rank3_exhaustion():
    """All 1716 six-subsets of 13 rational ternary projective points.

    Necessary rank-two counts only; no freeness or coverage beyond this pool
    is inferred. The universal result is proved in PROOF.md.
    """
    rows=[]
    for a in product((-1,0,1),repeat=3):
        if any(a) and next(x for x in a if x)!=-1:
            rows.append(a)
    assert len(rows)==13
    total=0; signature=0; nonsuper=[]; formal=0
    # Precompute the complete rank-two flats of the fixed ambient pool.
    full=Configuration(rows)
    pool_lines=full.lines()
    for ids in combinations(range(13),6):
        total+=1
        mask=sum(1<<i for i in ids)
        if full.rk(mask)!=3:
            continue
        lines={m&mask for m in pool_lines if (m&mask).bit_count()>=2}
        hist=[m.bit_count() for m in lines]
        if max(hist)>4 or sum((m-1)*(m-2)//2 for m in hist)!=4:
            continue
        signature+=1
        result=Configuration([rows[i] for i in ids]).analyze()
        formal+=int(result['formal'])
        if result['formal'] and not result['supersolvable']:
            nonsuper.append(ids)
    assert total==1716
    assert not nonsuper
    return {'pool_size':13,'subsets_checked':total,
            'rank3_one3_count_signature':signature,
            'formal_signature_matches':formal,
            'formal_nonsupersolvable_matches':len(nonsuper)}


def graph_support_check():
    """Exhaust six-point four-triple supports, independently of coordinates."""
    triples=list(combinations(range(6),3))
    retained=[]
    for family in combinations(triples,4):
        if any(len(set(a)&set(b))>1 for a,b in combinations(family,2)):
            continue
        degrees=[sum(i in t for t in family) for i in range(6)]
        if any(d<2 for d in degrees):
            continue
        assert degrees==[2]*6
        assert all(len(set(a)&set(b))==1 for a,b in combinations(family,2))
        retained.append(family)
    assert len(retained)==30
    return {'four_triple_families_checked':4845,
            'linear_families_with_all_degrees_at_least_two':len(retained),
            'all_have_k4_incidence':True}


def main():
    results={name:Configuration(rows).analyze() for name,rows in fixtures().items()}
    for name,result in results.items():
        assert result['formal'], name
        assert result['supersolvable']==(name!='nonfano_two_cubic_boundary'),name
    assert results['withdrawal_example']['rank_two_multiplicity_counts']['4']==1
    assert results['withdrawal_example']['incidence_cycle_rank']==0
    assert results['withdrawal_deletion']['incidence_components']==2
    assert results['k4_core']['incidence_cycle_rank']==3
    assert results['one3_rank6_k4_tree']['incidence_cycle_rank']==3
    assert results['nonfano_two_cubic_boundary']['incidence_cycle_rank']==6
    out={'arithmetic':'exact rational and symbolic; no floating point',
         'fixtures':results,'saito':saito_checks(),
         'rank3_exhaustion':rank3_exhaustion(),
         'support_exhaustion':graph_support_check(),
         'interpretation':'All assertions passed. Finite diagnostics do not replace the proof.'}
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
