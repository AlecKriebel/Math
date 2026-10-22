"""Exact rational finite checks of the relative graph complex, not a proof for all n."""
import itertools
import json
import math
from pathlib import Path
from sympy import Matrix, QQ
from sympy.polys.matrices import DomainMatrix


def connected(n, edges, subset):
    seen = {0}
    while True:
        new = seen.copy()
        for k in subset:
            a, b = edges[k]
            if a in seen or b in seen:
                new.update((a, b))
        if new == seen:
            return len(seen) == n
        seen = new


def check(n):
    edges = list(itertools.combinations(range(n), 2))
    m = len(edges)
    basis = [[s for s in itertools.combinations(range(m), p+1)
              if connected(n, edges, s)] for p in range(m)]
    maps = []
    for p in range(m-1):
        rows = {s:i for i,s in enumerate(basis[p+1])}
        a = Matrix.zeros(len(rows), len(basis[p]))
        for j,s in enumerate(basis[p]):
            for e in range(m):
                if e not in s:
                    t = tuple(sorted(s+(e,)))
                    a[rows[t],j] = (-1)**t.index(e)
        maps.append(a)
    for a,b in zip(maps,maps[1:]):
        if b*a != Matrix.zeros(b.rows,a.cols):
            raise RuntimeError('Nonzero coboundary square')
    ranks = [DomainMatrix.from_Matrix(a).convert_to(QQ).rank() for a in maps]
    dims = [len(basis[p])-(ranks[p-1] if p else 0)
            -(ranks[p] if p<len(ranks) else 0) for p in range(m)]
    expected = [math.factorial(n-1) if p==n-2 else 0 for p in range(m)]
    if dims != expected:
        raise RuntimeError((n,dims,expected))
    return {'n':n, 'cochain_dimensions':list(map(len,basis)),
            'exact_rational_differential_ranks':ranks,
            'cohomology_dimensions':dims, 'expected_match':True}


if __name__ == '__main__':
    result = {'method':'Exact rational matrix ranks; coboundary squares checked',
              'scope':'n=2,3,4,5 only; primary theorem supplies all-n result',
              'results':[check(n) for n in range(2,6)]}
    out=Path(__file__).with_name('NEUTRAL_GRAPH_CHECKS.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
