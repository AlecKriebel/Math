#!/usr/bin/env python3
"""Exact orthogonal controls, using only the pinned independent implementation.

The exact grevlex initial ideals of explicit rational coordinate changes are
corroboration only. This file makes no generic-initial-ideal inference from them.
"""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path


def load():
    here = Path(__file__).resolve().parent
    pin = json.loads((here/'INDEPENDENCE_FREEZE_01.json').read_text())
    expected = next(x for x in pin['files'] if x['path'] == 'reproduce_exact.py')
    path = here/'reproduce_exact.py'
    assert len(path.read_bytes()) == expected['bytes']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected['sha256']
    spec = importlib.util.spec_from_file_location('pr195_own_independent_core', path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def key(e):
    return (sum(e),)+tuple(-q for q in reversed(e))


def leading(p):
    return max(p, key=key)


def divides(a, b):
    return all(x <= y for x, y in zip(a, b))


def rem(m, f, gs):
    f = dict(f)
    remainder = {}
    while f:
        e = leading(f)
        q = f[e]
        reducer = next((g for g in gs if divides(leading(g), e)), None)
        if reducer is None:
            remainder[e] = q
            del f[e]
        else:
            a = leading(reducer)
            shift = tuple(x-y for x, y in zip(e, a))
            f = m.add(f, m.scale(m.mul({shift: F(1)}, reducer), -q/reducer[a]))
    return remainder


def rows_and_transform(m, rows):
    a = [list(map(F, row)) for row in rows]
    transform = [[F(i == j) for j in range(len(a))] for i in range(len(a))]
    r = 0
    pivots = []
    for j in range(len(a[0])):
        k = next((k for k in range(r, len(a)) if a[k][j]), None)
        if k is None:
            continue
        a[r], a[k] = a[k], a[r]
        transform[r], transform[k] = transform[k], transform[r]
        q = a[r][j]
        a[r] = [x/q for x in a[r]]
        transform[r] = [x/q for x in transform[r]]
        for k in range(len(a)):
            if k != r and a[k][j]:
                q = a[k][j]
                a[k] = [x-q*y for x, y in zip(a[k], a[r])]
                transform[k] = [x-q*y for x, y in zip(transform[k], transform[r])]
        pivots.append(j)
        r += 1
        if r == len(a):
            break
    for i in range(len(a)):
        assert all(sum(transform[i][k]*rows[k][j] for k in range(len(rows))) == a[i][j]
                   for j in range(len(rows[0])))
    return a[:r], transform[:r], pivots


def grevlex_degree(m, fs, n, d):
    mons = sorted(m.monomials(n, d), key=key, reverse=True)
    multipliers = m.monomials(n, d-6)
    source = [(j, e) for j in range(4) for e in multipliers]
    rows = []
    for j, exponent in source:
        v = m.mul(fs[j], {exponent: F(1)})
        rows.append([v.get(e, F(0)) for e in mons])
    rr, transform, pivots = rows_and_transform(m, rows)
    polynomials = [{e: q for e, q in zip(mons, row) if q} for row in rr]
    representations = []
    for tr in transform:
        cs = [{} for _ in range(4)]
        for (j, e), q in zip(source, tr):
            if q:
                cs[j][e] = q
        assert m.relation(fs, cs) == polynomials[len(representations)]
        representations.append(cs)
    return polynomials, representations, [mons[j] for j in pivots]


def groebner_binary(m, fs):
    basis = []
    reps = []
    for d in (6,7,8):
        polynomials, representations, _ = grevlex_degree(m, fs, 2, d)
        for g, rep in zip(polynomials, representations):
            if not any(divides(leading(h), leading(g)) for h in basis):
                basis.append(g)
                reps.append(rep)
    pair_count = 0
    for a, b in combinations(basis, 2):
        ea, eb = leading(a), leading(b)
        lcm = tuple(max(x,y) for x,y in zip(ea,eb))
        ma = {tuple(x-y for x,y in zip(lcm,ea)): 1/a[ea]}
        mb = {tuple(x-y for x,y in zip(lcm,eb)): 1/b[eb]}
        s = m.add(m.mul(ma,a),m.scale(m.mul(mb,b),-1))
        assert not rem(m,s,basis)
        pair_count += 1
    assert all(not rem(m,f,basis) for f in fs)
    return {'ordering':'graded reverse lexicographic, first variable greatest',
            'basis':[m.polyrecord(g) for g in basis],
            'representations_in_ambient_polar_generators':
                [[m.polyrecord(c) for c in rep] for rep in reps],
            'leading_exponents':[list(leading(g)) for g in basis],
            'all_Buchberger_pairs_reduce_to_zero':True,'Buchberger_pairs_checked':pair_count,
            'original_generators_reduce_to_zero':True}


def open_flags(m, n, coordinates):
    factors = [(1,0,0,0),(0,1,0,0),(1,-1,0,0),(1,-2,0,0),
               (0,0,1,0),(0,0,0,1),(1,0,1,1)]
    fs = [m.substitute(m.linear(a), coordinates) for a in factors]
    def vector(a):
        return [a.get(e,F(0)) for e in m.monomials(n,1)]
    vectors = [vector(a) for a in fs]
    nonzero = all(any(a) for a in vectors)
    pairwise = all(any(a[i]*b[j] != a[j]*b[i] for i,j in combinations(range(n),2))
                   for a,b in combinations(vectors,2))
    xy = len(m.rref([vector(coordinates[0]),vector(coordinates[1])])[1]) == 2
    xzw = n != 3 or m.determinant([vector(coordinates[j]) for j in (0,2,3)]) != 0
    return nonzero and pairwise and xy and xzw


def rank_mod(a, p):
    a = [[int(x)%p for x in row] for row in a]
    r = 0
    for j in range(len(a[0])):
        k = next((k for k in range(r,len(a)) if a[k][j]),None)
        if k is None:
            continue
        a[r],a[k] = a[k],a[r]
        inverse = pow(a[r][j],-1,p)
        a[r] = [x*inverse%p for x in a[r]]
        for k in range(r+1,len(a)):
            q = a[k][j]
            a[k] = [(x-q*y)%p for x,y in zip(a[k],a[r])]
        r += 1
        if r == len(a):
            break
    return r


def certificate():
    m = load()
    factors = [(1,0,0,0),(0,1,0,0),(1,-1,0,0),(1,-2,0,0),
               (0,0,1,0),(0,0,0,1),(1,0,1,1)]
    Q = m.one(4)
    for row in factors:
        Q = m.mul(Q,m.linear(row))
    polars = [m.derivative(Q,j) for j in range(4)]
    T = [m.linear(a) for a in [(1,0,0),(0,1,0),(0,0,1),(1,2,3)]]
    ternary = [m.substitute(f,T) for f in polars]
    ternary8,_ = m.macaulay(ternary,3,8)
    assert ternary8['rank'] == 21
    characteristic7_rank = rank_mod([[F(q) for q in row] for row in m.macaulay(ternary,3,7)[0]['matrix']],7)
    assert characteristic7_rank == 11
    degenerate = [m.linear(a) for a in [(1,0,0),(0,1,0),(0,0,1),(2,0,3)]]
    assert not open_flags(m,3,degenerate)
    degenerate_polars = [m.substitute(f,degenerate) for f in polars]
    degenerate7,_ = m.macaulay(degenerate_polars,3,7)
    assert degenerate7['rank'] == 11
    tests = []
    # Enumerate fixed small flags, not random observations or a genericity proof.
    for a in range(1,5):
        C3 = [m.linear(row) for row in [(1,0,0),(0,1,0),(0,0,1),(a,2,3)]]
        assert open_flags(m,3,C3)
        fs3 = [m.substitute(f,C3) for f in polars]
        assert m.coefficient_syzygy_dimension(C3)['nullity'] == 0
        assert [m.macaulay(fs3,3,d)[0]['rank'] for d in (6,7)] == [4,12]
        for b in range(2,5):
            C2 = [m.substitute(v,[m.linear((1,0)),m.linear((0,1)),m.linear((b,b+1))]) for v in C3]
            if not open_flags(m,2,C2):
                tests.append({'a':a,'b':b,'open':False,'not_used_for_genericity':True})
                continue
            fs2 = [m.substitute(f,C2) for f in polars]
            ranks = [m.macaulay(fs2,2,d)[0]['rank'] for d in (6,7,8)]
            assert ranks == [4,7,9]
            assert m.coefficient_syzygy_dimension(C2)['nullity'] == 1
            tests.append({'a':a,'b':b,'open':True,'binary_ranks':ranks})
    C4_rows = [(1,2,3,5),(2,3,5,7),(3,5,7,11),(5,7,11,13)]
    assert m.determinant(C4_rows) == -2
    C4 = [m.linear(a) for a in C4_rows]
    C3 = [m.linear(a[:3]) for a in C4_rows]
    C2 = [m.linear(a[:2]) for a in C4_rows]
    assert open_flags(m,3,C3) and open_flags(m,2,C2)
    fs2 = [m.substitute(f,C2) for f in polars]
    binaryGB = groebner_binary(m,fs2)
    assert binaryGB['leading_exponents'] == [[6,0],[5,1],[4,2],[3,3],[2,5],[1,6],[0,8]]
    initial_controls = []
    for n,C in [(3,C3),(4,C4)]:
        fs = [m.substitute(f,C) for f in polars]
        minimal = []
        degrees = []
        for d in (6,7):
            _,_,leads = grevlex_degree(m,fs,n,d)
            new = [e for e in leads if not any(divides(g,e) for g in minimal)]
            minimal.extend(new)
            degrees.append({'degree':d,'rank':len(leads),'new_minimal_leading_monomials':[list(e) for e in new]})
        assert any(sum(e) == 7 and e[2] for e in minimal)
        initial_controls.append({'variables':n,'coordinate_rows':[list(row[:n]) for row in C4_rows],
                                 'degrees':degrees,
                                 'scope':'Exact initial ideal through degree7 at this flag; not a certification of generic initial ideal.'})
    return {'schema':'PR195_independent_orthogonal_controls_v1',
            'extra_original_flag_ternary_degree8':ternary8,
            'small_open_flag_tests':tests,
            'degenerate_ternary_flag':{'rows':[[1,0,0],[0,1,0],[0,0,1],[2,0,3]],
                                      'rank_degree7':degenerate7['rank'],
                                      'open_condition_X_Z_W_independent_fails':True},
            'characteristic7_original_ternary_degree7_rank':characteristic7_rank,
            'characteristic7_scope':'This control demonstrates that the 7a=0 step cannot be extended to characteristic7.',
            'exact_binary_Groebner':binaryGB,
            'GL4_control_matrix':list(map(list,C4_rows)), 'GL4_determinant':-2,
            'initial_ideal_controls':initial_controls,
            'genericity_warning':'All finite flag experiments are corroborative. The universal open-set scalar proof is required for the gin assertion.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',type=Path)
    args = parser.parse_args()
    result = (json.dumps(certificate(),indent=2,sort_keys=True)+'\n').encode()
    if args.verify:
        assert args.verify.read_bytes() == result
        print(json.dumps({'verified':True,'certificate_bytes':len(result),
                          'certificate_sha256':hashlib.sha256(result).hexdigest()}))
    else:
        print(result.decode(),end='')
