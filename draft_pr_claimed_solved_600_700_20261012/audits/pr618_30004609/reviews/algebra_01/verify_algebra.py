#!/usr/bin/env python3
"""Independent exact diagnostic checks, without importing candidate code.

This is finite evidence for the algebra/geometry audit, not a universal proof.
Requires SymPy 1.14.0. Uses exact linear systems and generic polynomial
derivation spaces, rather than accepting the supplied Saito witnesses.
"""
import json
from functools import cache
from itertools import combinations, product
from pathlib import Path
import sympy as s


class Represented:
    def __init__(self, normals):
        self.normals = tuple(tuple(map(s.Rational, a)) for a in normals)
        self.n = len(self.normals)
        self.d = len(self.normals[0])
        self.all = frozenset(range(self.n))
        assert all(any(a) for a in self.normals)
        assert all(self.rank(frozenset(p)) == 2 for p in combinations(range(self.n), 2))

    @cache
    def rank(self, ids):
        return s.Matrix([self.normals[i] for i in sorted(ids)]).rank() if ids else 0

    @cache
    def closure(self, ids):
        r = self.rank(ids)
        return frozenset(i for i in range(self.n) if self.rank(ids | {i}) == r)

    @cache
    def flats(self):
        # Enumerate independent generating sets; never need more than r elements.
        flats = {frozenset()}
        r = self.rank(self.all)
        for k in range(1, r + 1):
            for ids in combinations(range(self.n), k):
                ids = frozenset(ids)
                if self.rank(ids) == k:
                    flats.add(self.closure(ids))
        return tuple(sorted(flats, key=lambda f: (self.rank(f), tuple(sorted(f)))))

    @cache
    def lines(self):
        return tuple(sorted({self.closure(frozenset(p))
                             for p in combinations(range(self.n), 2)},
                            key=lambda f: tuple(sorted(f))))

    @cache
    def relations(self, ids):
        ids = sorted(ids)
        if not ids:
            return ()
        normal_map = s.Matrix([self.normals[i] for i in ids]).T
        out = []
        for v in normal_map.nullspace():
            out.append(tuple(v[ids.index(i)] if i in ids else s.Integer(0)
                             for i in range(self.n)))
        return tuple(out)

    def local_vectors(self):
        return tuple(v for line in self.lines() if len(line) >= 3
                     for v in self.relations(line))

    @cache
    def formal(self):
        vecs = self.local_vectors()
        rk = s.Matrix(vecs).rank() if vecs else 0
        return rk == self.n - self.rank(self.all)

    @cache
    def modular(self, f):
        return all(self.rank(f) + self.rank(g) == self.rank(f | g) + self.rank(f & g)
                   for g in self.flats())

    def modular_chain(self):
        predecessor = {frozenset(): None}
        for f in self.flats():
            if not f or not self.modular(f):
                continue
            pred = next((g for g in predecessor
                         if g < f and self.rank(g) + 1 == self.rank(f)), None)
            if pred is not None:
                predecessor[f] = pred
        if self.all not in predecessor:
            return None
        out = []
        f = self.all
        while f is not None:
            out.append(sorted(f))
            f = predecessor[f]
        return out[::-1]

    def summary(self):
        return {'normals': [[str(x) for x in a] for a in self.normals],
                'rank': self.rank(self.all), 'relation_dimension': len(self.relations(self.all)),
                'local_relation_dimension': s.Matrix(self.local_vectors()).rank()
                 if self.local_vectors() else 0,
                'formal': self.formal(), 'flat_count': len(self.flats()),
                'nontrivial_lines': [sorted(f) for f in self.lines() if len(f) >= 3],
                'modular_coatoms': [sorted(f) for f in self.flats()
                                    if self.rank(f) == self.rank(self.all)-1 and self.modular(f)],
                'modular_chain': self.modular_chain()}


TRI = [(1, 0), (0, 1), (1, 1)]
QUAD = [(1, 0), (0, 1), (1, 1), (1, 2)]
K4 = [(1, 0, 0), (0, 1, 0), (0, 0, 1),
      (1, -1, 0), (1, 0, -1), (0, 1, -1)]
NONFANO = K4 + [(1, 1, -1)]
WITHDRAWAL = [(1,0,0,0),(0,1,0,0),(1,1,0,0),(1,2,0,0),
              (1,0,1,0),(0,0,1,0),(0,0,0,1),(0,0,1,1)]


def exponents_of_monomials(d, degree):
    return [a for a in product(range(degree+1), repeat=d) if sum(a) == degree]


def derivation_space(normals, degree):
    """Solve every homogeneous tangency equation, with no proposed basis input."""
    d = len(normals[0])
    x = s.symbols('x:'+str(d))
    monomials = [s.prod(v**a for v,a in zip(x,e))
                 for e in exponents_of_monomials(d, degree)]
    c = s.symbols('c:'+str(d*len(monomials)))
    theta = [sum(c[i*len(monomials)+j]*m for j,m in enumerate(monomials))
             for i in range(d)]
    equations = []
    for a in normals:
        alpha = sum(ai*xi for ai,xi in zip(a,x))
        pivot = next(i for i in range(d) if a[i])
        value = sum(ai*ti for ai,ti in zip(a,theta))
        replacement = -sum(ai*xi for i,(ai,xi) in enumerate(zip(a,x)) if i != pivot)/a[pivot]
        remainder = s.expand(value.subs(x[pivot],replacement))
        equations.extend(s.Poly(remainder,*x).coeffs())
    matrix, rhs = s.linear_eq_to_matrix(equations,c)
    assert rhs == s.zeros(rhs.rows,1)
    basis = []
    for vector in matrix.nullspace():
        basis.append(tuple(s.expand(t.subs(dict(zip(c,vector)))) for t in theta))
    return x, tuple(basis)


def saito_from_full_spaces(normals, degrees):
    x, euler_space = derivation_space(normals, 1)
    assert len(euler_space) == 1
    euler = euler_space[0]
    spaces = {1:euler_space}
    for degree in set(degrees):
        if degree not in spaces:
            xx, spaces[degree] = derivation_space(normals,degree)
            assert xx == x
    q = s.prod(sum(ai*xi for ai,xi in zip(a,x)) for a in normals)
    columns = [euler]
    def search(k):
        if k == len(degrees):
            det = s.factor(s.Matrix.hstack(*map(s.Matrix,columns)).det())
            if det:
                ratio = s.cancel(det/q)
                assert not ratio.free_symbols and ratio != 0
                return {'basis': [[str(p) for p in col] for col in columns],
                        'degrees': degrees, 'determinant_over_Q': str(ratio),
                        'degree_space_dimensions': {str(d):len(b) for d,b in spaces.items()}}
            return None
        for col in spaces[degrees[k]]:
            columns.append(col)
            # Stop extending polynomially dependent partial columns.
            if s.Matrix.hstack(*map(s.Matrix,columns)).rank() == len(columns):
                result = search(k+1)
                if result is not None:
                    return result
            columns.pop()
        return None
    result = search(1)
    assert result is not None
    return result


def terminal_check(base_rows, attachment, slopes):
    """Arbitrary pencil parameters; verify kernel split, all flats, and lifting."""
    normals = [tuple(a)+(0,) for a in base_rows]
    a = normals[attachment]
    u = (0,)*(len(a)-1)+(1,)
    normals += [tuple(ui+t*ai for ui,ai in zip(u,a)) for t in slopes]
    rep = Represented(normals)
    inside = frozenset(range(len(base_rows)))
    pencil = frozenset({attachment} | set(range(len(base_rows),len(normals))))
    assert pencil in rep.lines()
    assert all(not (line & (pencil - {attachment})) for line in rep.lines()
               if len(line) >= 3 and line != pencil)
    assert rep.formal()
    base = Represented(base_rows)
    assert base.formal()
    assert rep.rank(inside) == rep.rank(rep.all)-1
    assert rep.closure(inside) == inside
    rlocal = rep.relations(pencil)
    rinside = rep.relations(inside)
    rglobal = rep.relations(rep.all)
    assert len(rlocal) == len(pencil)-2
    assert s.Matrix(rlocal+rinside).rank() == len(rglobal) == len(rlocal)+len(rinside)
    assert rep.modular(inside)
    for f in base.flats():
        if base.modular(f):
            assert rep.modular(f), ('failed modular-chain lift',base_rows,attachment,slopes,f)
    assert (rep.modular_chain() is not None) == (base.modular_chain() is not None)
    return {'base_size':len(base_rows),'attachment':attachment,'slopes':list(slopes),
            'rank':rep.rank(rep.all),'pencil_size':len(pencil),'flat_count':len(rep.flats()),
            'coatom_modular':True,'all_base_modular_flats_lift':True,
            'supersolvable':rep.modular_chain() is not None}


def main():
    output = {'arithmetic':'exact rational/symbolic', 'sympy_version':s.__version__}
    saito = {}
    for name, normals, degrees in [('k4',K4,[1,2,3]),
                                  ('nonfano',NONFANO,[1,3,3]),
                                  ('withdrawal',WITHDRAWAL,[1,2,2,3])]:
        saito[name] = saito_from_full_spaces(normals,degrees)
    output['independently_solved_saito_certificates'] = saito
    # Fully formal bases include a nonsupersolvable one: the pruning statement
    # concerns modularity, and supersolvability still needs the base hypothesis.
    output['terminal_pencil_tests'] = [terminal_check(base,attachment,slopes)
        for base in [TRI,QUAD,K4,NONFANO]
        for attachment in [0,len(base)-1]
        for slopes in [(-2,3),(0,2),(0,1,3)]]
    summaries = {name:Represented(normals).summary()
                 for name,normals in [('k4',K4),('nonfano',NONFANO),('withdrawal',WITHDRAWAL)]}
    assert summaries['k4']['formal'] and summaries['k4']['modular_chain'] is not None
    assert summaries['nonfano']['formal'] and summaries['nonfano']['modular_chain'] is None
    assert len(summaries['k4']['nontrivial_lines']) == 4
    assert len(summaries['nonfano']['nontrivial_lines']) == 6
    assert summaries['nonfano']['modular_coatoms'] == []
    output['lattice_summaries'] = summaries
    # Attempt to invalidate pruning by omitting its formality premise.
    bad = Represented([(1,0,0),(0,1,0),(1,1,0),(0,0,1),(1,2,3)])
    inside = frozenset({0,3,4})
    assert bad.lines().count(frozenset({0,1,2})) == 1
    assert [f for f in bad.lines() if len(f)>=3] == [frozenset({0,1,2})]
    assert not bad.formal()
    assert bad.rank(inside) == bad.rank(bad.all) == 3
    assert bad.closure(inside) == bad.all
    _,d1=derivation_space(bad.normals,1)
    assert len(d1)==1
    output['formality_premise_failure_witness'] = bad.summary() | {
        'remaining_indices':sorted(inside),'remaining_rank':bad.rank(inside),
        'remaining_flat_closure':sorted(bad.closure(inside)),
        'degree_one_derivation_dimension':len(d1),
        'meaning':'Without formality, a terminal triple need not lower rank, be a flat, or force reducibility from incidence components.'}
    # Reproduce the withdrawal counterexample to its erroneous factor-size step.
    deleted = WITHDRAWAL[:4]+WITHDRAWAL[5:]
    _,d1=derivation_space(deleted,1)
    assert len(d1)==2
    output['withdrawal_deletion']={'factor_sizes':[4,3],'degree_one_dimension':len(d1),
                                  'rank':Represented(deleted).rank(frozenset(range(7)))}
    output['interpretation']='All exact assertions passed; finite diagnostics support but do not replace the proof.'
    target=Path(__file__).with_name('ALGEBRA_CHECKS.json')
    target.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'output':str(target),'terminal_pencil_tests':len(output['terminal_pencil_tests']),
                      'saito_certificates':list(saito),'premise_failure_witness':True,
                      'assertions':'passed'},indent=2))


if __name__ == '__main__':
    main()
