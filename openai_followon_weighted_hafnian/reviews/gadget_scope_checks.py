"""Preserved independent adversary's additional finite-check procedure.

Run from the dedicated project directory:
    python3 -u reviews/gadget_scope_checks.py

The original successful procedure was supplied as a Python shell heredoc.
This file preserves its checks; setting dont_write_bytecode in-process replaces
PYTHONDONTWRITEBYTECODE=1. It does not write the main test report. No upstream
FPRAS or efficient sampler is certified. Do not treat finite checks as proof.
"""
import sys
sys.dont_write_bytecode = True
import hashlib, platform, random
from fractions import Fraction
from itertools import combinations
from collections import Counter
sys.path.insert(0, 'code')
from gadget import (Graph, count_perfect_matchings, enumerate_perfect_matchings,
                    integer_gadget, expand_rational_matrix, dag_path_count)
from test_gadget import run_checks

def independent_matchings(n, edges, deleted=()):
    edge_set = {frozenset(e) for e in edges}
    def visit(left):
        if not left:
            yield ()
            return
        u = left[0]
        for idx in range(1, len(left)):
            v = left[idx]
            if frozenset((u, v)) in edge_set:
                for rest in visit(left[1:idx] + left[idx+1:]):
                    yield ((u, v),) + rest
    yield from visit(tuple(v for v in range(n) if v not in deleted))

r = run_checks()
assert r['status'] == 'all finite exact checks passed'
print('Repository suite:', r['status'], 'seconds:', r['elapsed_seconds'])
num_graphs = 0
for n in (0, 2, 4, 6):
    pairs = list(combinations(range(n), 2))
    for bits in range(1 << len(pairs)):
        edges = tuple(e for k, e in enumerate(pairs) if bits & (1 << k))
        g = Graph(n, edges)
        independent = list(independent_matchings(n, edges))
        assert count_perfect_matchings(g) == len(independent), (n, bits)
        ours = {tuple(sorted(m)) for m in enumerate_perfect_matchings(g)}
        other = {tuple(sorted(m)) for m in independent}
        assert ours == other, (n, bits)
        num_graphs += 1
print('Independent counter/enumerator graph cases:', num_graphs)

for w in range(1, 65):
    g = integer_gadget(w).graph
    sig = tuple(sum(1 for _ in independent_matchings(g.order, g.edges, deletion))
                for deletion in ((), (0, 1), (0,), (1,)))
    assert sig == (w, 1, 0, 0), (w, sig)
print('Independent four-state gadget signatures: 64')

rng = random.Random(17012027)
pairs = list(combinations(range(4), 2))
for trial in range(80):
    weights = {e: Fraction(rng.randrange(3)) for e in pairs}
    for e in rng.sample(pairs, 2):
        weights[e] = rng.choice([Fraction(0), Fraction(1, 3), Fraction(1, 2),
                                 Fraction(2, 3), Fraction(1)])
    mat = [[Fraction(0) for _ in range(4)] for _ in range(4)]
    for (u, v), q in weights.items():
        mat[u][v] = mat[v][u] = q
    ex = expand_rational_matrix(mat)
    observed = Counter(ex.project(m) for m in
                       independent_matchings(ex.graph.order, ex.graph.edges))
    support = tuple(e for e, q in weights.items() if q)
    expected = {}
    for m in independent_matchings(4, support):
        value = Fraction(ex.denominator**2)
        for e in m:
            value *= weights[e]
        assert value.denominator == 1
        expected[tuple(sorted(m))] = value.numerator
    assert observed == expected, (trial, observed, expected)
print('Independent complete rational projection-fiber cases: 80')

for length in (1000, 2048, 4096):
    w = (1 << (length - 1)) + 1
    gadget = integer_gadget(w)
    assert dag_path_count(gadget.dag) == w
    assert gadget.graph.order == 4 * length - 2
    assert len(gadget.graph.edges) <= 6 * length - 5
print('Large-weight construction/path-count/simplicity/bounds: 1000,2048,4096 bits')

matrix = [[0, 2, 1, 1], [2, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]]
ex = expand_rational_matrix(matrix)
m = next(independent_matchings(ex.graph.order, ex.graph.edges))
assert ex.project(tuple((v, u) for u, v in m)) == ex.project(m)
for malformed in ((), m[:-1], m + (m[0],), ((0, ex.graph.order + 1),) + m):
    try:
        ex.project(malformed)
    except ValueError:
        pass
    else:
        raise AssertionError('malformed certificate accepted')
print('Malformed projection certificates: four rejected; reversed edges accepted')
print('Python:', platform.python_version())
for path in ('proofs/GADGET_PROOF.md', 'code/gadget.py', 'code/test_gadget.py'):
    print(path, hashlib.sha256(open(path, 'rb').read()).hexdigest())
