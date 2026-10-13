#!/usr/bin/env python3
"""Independent exact audit. Requires SymPy; never imports the author's code.

Usage: python independent_math.py AUTHOR_SAFE_DIRECTORY [OUTPUT_JSON]
Only the author's published coefficient certificate is read as test data.
"""
import hashlib
import itertools
import json
import pathlib
import sys
import sympy as s
from sympy.polys.matrices import DomainMatrix

if not __debug__:
    raise SystemExit('Run without -O; the checks use assertions.')

def exponents(n, d):
    if n == 1:
        yield (d,)
    else:
        for k in range(d + 1):
            for tail in exponents(n - 1, d - k):
                yield (k,) + tail

def monomial(v, e):
    return s.prod(a**k for a, k in zip(v, e))

def qdomain(M):
    return DomainMatrix.from_Matrix(M).convert_to(s.QQ)

def exact_rank(M):
    return qdomain(M).rank()

def hilbert(G, maxdegree):
    leads = [tuple(p.LM(order=G.order).exponents) for p in G.polys]
    return [sum(not any(all(a >= b for a, b in zip(m, t)) for t in leads)
                for m in exponents(len(G.gens), d)) for d in range(maxdegree + 1)]

def signature(M):
    """Use exact rational isolating intervals of the characteristic polynomial.

    Symmetric real matrices have real roots. This is a different algorithm from
    the author's pivot/congruence routine and does not use numeric eigenvalues.
    """
    p = s.Poly(M.charpoly().as_expr())
    counts = [0, 0, 0]
    for interval, multiplicity in s.polys.polytools.intervals(p, eps=s.Rational(1, 10**8)):
        a, b = interval
        if a == b == 0:
            counts[2] += multiplicity
        elif a >= 0 and b > 0:
            counts[0] += multiplicity
        elif b <= 0 and a < 0:
            counts[1] += multiplicity
        else:
            raise AssertionError('Root interval straddles zero.')
    assert sum(counts) == M.rows
    return counts

def primitive(Q, L):
    basis = (L.T * Q).nullspace()
    K = s.Matrix.hstack(*basis)
    return -K.T * Q * K

def base_algebra():
    u, x, y, z = v = s.symbols('u x y z')
    relations = [x*x+y*z+u*u, x*u, x*x+x*y, x*z+y*u, z*u+u*u, y*y+z*z]
    G = s.groebner(relations, *v, order='grevlex', domain=s.QQ)
    assert hilbert(G, 4) == [1, 4, 4, 0, 0]
    b = [x*y, x*z, y*z, z*z]
    quadratic_monomials = list(exponents(4, 2))
    coeff = lambda f: s.Matrix([s.Poly(f, *v).coeff_monomial(m) for m in quadratic_monomials])
    B = s.Matrix.hstack(*[coeff(G.reduce(t)[1]) for t in b])
    assert exact_rank(B) == 4
    multiplication = {}
    for i in range(4):
        for j in range(i, 4):
            ans, parameters = B.gauss_jordan_solve(coeff(G.reduce(v[i]*v[j])[1]))
            assert parameters.rows == 0
            multiplication[i, j] = ans
    for m in exponents(4, 3):
        assert G.reduce(monomial(v, m))[1] == 0
    return v, G, multiplication

def bar_check(mul, author):
    symbols = [(1, i) for i in range(4)] + [(2, i) for i in range(4)]
    words = {k: [w for w in itertools.product(symbols, repeat=k)
                 if sum(a for a, _ in w) == 4] for k in (2, 3, 4)}
    matrices = {}
    for k in (3, 4):
        lookup = {w: i for i, w in enumerate(words[k-1])}
        entries = {}
        for col, w in enumerate(words[k]):
            for pos in range(k-1):
                if w[pos][0] == w[pos+1][0] == 1:
                    product = mul[tuple(sorted((w[pos][1], w[pos+1][1])))]
                    for j, c in enumerate(product):
                        if c:
                            t = w[:pos] + ((2, j),) + w[pos+2:]
                            key = lookup[t], col
                            entries[key] = entries.get(key, 0) + (-1)**pos*c
        matrices[k] = s.SparseMatrix(len(words[k-1]), len(words[k]), entries)
    D3, D4 = matrices[3], matrices[4]
    assert D3*D4 == s.zeros(D3.rows, D4.cols)
    ranks = [exact_rank(D3), exact_rank(D4)]
    assert ranks == [16, 175]
    assert D3.cols - sum(ranks) == 1
    word_index = {w: i for i, w in enumerate(words[3])}
    c = s.zeros(D3.cols, 1)
    c[word_index[((1, 0), (1, 0), (2, 3))]] = 1
    c[word_index[((1, 0), (1, 3), (2, 3))]] = 1
    assert D3*c == s.zeros(D3.rows, 1)
    # Construct a fresh separating functional through SymPy's exact nullspace.
    annihilator = qdomain(D4.T).nullspace().to_Matrix()
    lam = next(row.T/(row*c)[0] for row in [annihilator.row(k) for k in range(annihilator.rows)]
               if (row*c)[0] != 0)
    assert D4.T*lam == s.zeros(D4.cols, 1) and (lam.T*c)[0] == 1
    names = {1: ['u', 'x', 'y', 'z'], 2: ['xy', 'xz', 'yz', 'zz']}
    name_to_symbol = {name: (d, k) for d, ns in names.items() for k, name in enumerate(ns)}
    certificate = json.loads((author/'MATH_RESULTS.json').read_text())['base_R']['explicit_nonzero_bar_class']
    decoded = {}
    for kind in ['cycle', 'separating_cocycle']:
        vector = s.zeros(D3.cols, 1)
        for term in certificate[kind]:
            word = tuple(name_to_symbol[a] for a in term['word'])
            vector[word_index[word]] += s.Rational(term['coefficient'])
        decoded[kind] = vector
    assert decoded['cycle'] == c
    assert D4.T*decoded['separating_cocycle'] == s.zeros(D4.cols, 1)
    assert (decoded['separating_cocycle'].T*c)[0] == 1
    assert exact_rank(D4.row_join(c)) == 176
    return {'dimensions_C2_C3_C4': [len(words[k]) for k in (2, 3, 4)],
            'ranks_d3_d4': ranks, 'Tor_3_4_dimension': 1,
            'rank_boundaries_with_cycle': 176, 'author_certificate_valid': True,
            'fresh_separating_cocycle': [{'word': [names[d][i] for d, i in words[3][k]],
                                         'coefficient': str(a)} for k, a in enumerate(lam) if a],
            'fresh_pairing': '1', 'arithmetic': 'exact QQ; no finite-field lifting'}

def idealization_check(mul):
    def product(i, j):
        if i < 4 and j < 4:
            return mul[tuple(sorted((i, j)))].col_join(s.zeros(4, 1))
        if i >= 4 and j >= 4:
            return s.zeros(8, 1)
        if i >= 4:
            i, j = j, i
        return s.zeros(4, 1).col_join(s.Matrix([mul[tuple(sorted((i, k)))][j-4] for k in range(4)]))
    v = s.symbols('a0:8')
    pairs = list(itertools.combinations_with_replacement(range(8), 2))
    M = s.Matrix.hstack(*[product(i, j) for i, j in pairs])
    assert exact_rank(M) == 8
    relations = [sum(c*v[i]*v[j] for c, (i, j) in zip(vec, pairs)) for vec in M.nullspace()]
    assert len(relations) == 28
    G = s.groebner(relations, *v, order='grevlex', domain=s.QQ)
    h = hilbert(G, 5)
    assert h == [1, 8, 8, 1, 0, 0]
    rank_counts = [s.binomial(7+d, d)-h[d] for d in (2, 3, 4)]
    assert rank_counts == [28, 119, 330]
    L = s.Matrix([0, 0, 0, 1, 0, 0, 0, 1])
    P = s.zeros(8)
    for i in range(4):
        P[i, i+4] = P[i+4, i] = 1
    Q = s.Matrix(8, 8, lambda i, j: (product(i, j).T*P*L)[0])
    T = s.Matrix.hstack(*[mul[tuple(sorted((3, i)))] for i in range(4)])
    assert T.det() == -1 and Q.det() != 0
    assert (L.T*Q*L)[0] == 3
    assert signature(Q) == [4, 4, 0]
    assert signature(primitive(Q, L)) == [4, 3, 0]
    for i in range(4, 8):
        for j in range(4, 8):
            assert product(i, j) == s.zeros(8, 1)
    # Check all generator triples for the dual-module associativity law.
    for i, j, k in itertools.product(range(8), repeat=3):
        assert (product(i, j).T*P[:, k])[0] == (product(j, k).T*P[:, i])[0]
    return {'hilbert_through_degree_5': h, 'quadratic_relation_count': 28,
            'quadratic_ideal_Macaulay_ranks_2_3_4': list(map(int, rank_counts)),
            'independent_groebner_basis_size': len(G.polys),
            'multiplication_by_z': [[str(a) for a in T.row(i)] for i in range(4)],
            'det_T': '-1', 'det_B_L': str(Q.det()), 'L_cube': '3',
            'B_L_inertia': signature(Q), 'primitive_Q1_inertia': signature(primitive(Q, L)),
            'square_zero_subspace_dimension': 4, 'all_generator_associativity_checks': 512}

def positive_check():
    results = []
    for n in range(2, 13):
        z = s.symbols('z0:'+str(n-2))
        u, v, t = s.symbols('u v t')
        relations = [u*u, v*v]
        relations += [a*u for a in z] + [a*v for a in z]
        relations += [a*a+u*v for a in z]
        relations += [a*b for a, b in itertools.combinations(z, 2)]
        G = s.groebner(relations, *z, u, v, order='grevlex', domain=s.QQ)
        H = s.groebner(relations+[t*t], *z, u, v, t, order='grevlex', domain=s.QQ)
        assert all(p.total_degree() == 2 for p in G.polys+H.polys)
        assert len(G.polys) == len(relations) and len(H.polys) == len(relations)+1
        assert hilbert(G, 4) == [1, n, 1, 0, 0]
        assert hilbert(H, 5) == [1, n+1, n+1, 1, 0, 0]
        B = s.diag(*([0, 0]+[-1]*(n-2)))
        B[0, 1] = B[1, 0] = 1
        def form(a, r):
            return (r*B).row_join(B*a).col_join((a.T*B).row_join(s.zeros(1)))
        ell = s.Matrix([1, 1]+[0]*(n-2)+[1])
        Q = form(ell[:-1, :], 1)
        primitive_columns = [s.Matrix([1, -1]+[0]*(n-2)+[0])]
        primitive_columns += [s.eye(n+1)[:, j] for j in range(2, n)]
        primitive_columns += [s.Matrix([1, 1]+[0]*(n-2)+[-2])]
        K = s.Matrix.hstack(*primitive_columns)
        assert ell.T*Q*K == s.zeros(1, n)
        assert -K.T*Q*K == s.diag(*([2]+[1]*(n-2)+[6]))
        assert (ell.T*Q*ell)[0] == 6
        points = [(s.Matrix([j+3, j+2]+[s.Rational((-1)**(j+k), n+2) for k in range(n-2)]),
                   s.Rational(j+1, 3)) for j in range(3)]
        for a, r in points:
            assert (a.T*B*a)[0] > 0
            Q = form(a, r)
            assert signature(Q) == [1, n, 0]
            for b, q in points:
                L0 = b.col_join(s.Matrix([q]))
                assert (L0.T*Q*L0)[0] > 0
                P = primitive(Q, L0)
                # Sylvester criterion avoids reusing a signature implementation.
                assert all(P[:j, :j].det() > 0 for j in range(1, n+1))
        for (a, r), (b, q), (c, k) in itertools.product(points, repeat=3):
            assert (r*b.T*B*c + q*a.T*B*c + k*a.T*B*b)[0] > 0
        results.append({'n': n, 'quadratic_GB_verified': True, 'points': 3,
                        'mixed_pairs': 9, 'mixed_triples': 27,
                        'explicit_primitive_diagonal': [2]+[1]*(n-2)+[6]})
    return results

def apolar_check():
    X, Y, x, y = s.symbols('X Y x y')
    F = X**3-Y**3
    l = {X: 2, Y: 1}
    Q = s.hessian(F, (X, Y)).subs(l)/6
    L = s.Matrix([2, 1])
    assert Q == s.diag(2, -1) and F.subs(l) == 7
    K = s.Matrix([1, 4])
    assert L.T*Q*K == s.zeros(1)
    assert -(K.T*Q*K)[0] == 14
    G = s.groebner([x*y, x**3+y**3], x, y, order='grevlex')
    assert hilbert(G, 5) == [1, 2, 2, 1, 0, 0]
    assert s.groebner([x*y], x, y).reduce(x**3+y**3)[1] != 0
    return {'hilbert_through_degree_5': [1, 2, 2, 1, 0, 0], 'cube': 7,
            'primitive_Q1_value': 14, 'independent_cubic_relation': True,
            'quadratic': False}

def main():
    if len(sys.argv) not in (2, 3):
        raise SystemExit(__doc__)
    author = pathlib.Path(sys.argv[1])
    v, G, mul = base_algebra()
    result = {'status': 'PASS; scoped results only', 'problem_id': 30005418,
              'general_target': 'UNSOLVED', 'sympy_version': s.__version__,
              'author_math_results_sha256': hashlib.sha256((author/'MATH_RESULTS.json').read_bytes()).hexdigest(),
              'R_hilbert_through_degree_4': hilbert(G, 4),
              'bar': bar_check(mul, author), 'idealization': idealization_check(mul),
              'positive_families': positive_check(), 'apolar': apolar_check()}
    text = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if len(sys.argv) == 3:
        pathlib.Path(sys.argv[2]).write_text(text)
    print(text, end='')

if __name__ == '__main__':
    main()
