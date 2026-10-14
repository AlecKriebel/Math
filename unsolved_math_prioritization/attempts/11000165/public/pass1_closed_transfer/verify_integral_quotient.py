"""Independent exact pivot/saturation tests; general proof is in the report."""
from itertools import combinations
from math import comb
from fractions import Fraction
import json

def wedge3(t):
    if len(set(t)) != 3:
        return (None, 0)
    sign = (-1) ** sum((t[i] > t[j] for i in range(3) for j in range(i + 1, 3)))
    return (tuple(sorted(t)), sign)
rows = []
for g in range(2, 13):
    monomials = list(combinations(range(2 * g), 3))
    W = [m for m in monomials if any((x < g for x in m))]
    used = set()
    relations = []
    pivots = []
    for x in range(2 * g):
        terms = {}
        for i in range(g):
            m, s = wedge3((x, i, g + i))
            if s:
                terms[m] = terms.get(m, 0) + s
        if not len(terms) == g - 1:
            raise RuntimeError('Exact supplementary check failed')
        if not not used.intersection(terms):
            raise RuntimeError('Exact supplementary check failed')
        used.update(terms)
        i = x % g
        j = (i + 1) % g
        p, s = wedge3((x, j, g + j))
        if not (s in (-1, 1) and terms[p] == s):
            raise RuntimeError('Exact supplementary check failed')
        relations.append(terms)
        pivots.append((p, s))
    if not len({p for p, s in pivots}) == 2 * g:
        raise RuntimeError('Exact supplementary check failed')

    def reduce(v):
        v = dict(v)
        for r, (p, s) in zip(relations, pivots):
            coefficient = v.get(p, 0) * s
            for m, c in r.items():
                v[m] = v.get(m, 0) - coefficient * c
        return {m: c for m, c in v.items() if c}
    if not all((reduce(r) == {} for r in relations)):
        raise RuntimeError('Exact supplementary check failed')
    if not all((not any((p in reduce({m: 1}) for p, s in pivots)) for m in W)):
        raise RuntimeError('Exact supplementary check failed')
    rank = len(W) - 2 * g
    if not rank == comb(2 * g, 3) - comb(g, 3) - 2 * g:
        raise RuntimeError('Exact supplementary check failed')
    rows.append({'genus': g, 'W_rank': len(W), 'kappa_rank': 2 * g, 'quotient_rank': rank, 'all_unit_pivots': True, 'supports_disjoint': True, 'all_relations_reduce_to_zero': True})
print(json.dumps({'status': 'PASS', 'arithmetic': 'exact integers; no rank-over-Q inference', 'note': 'Finite checks supplement, not replace, the uniform support proof. Genus-two quotient check does not transfer Omori generation to genus two.', 'rows': rows}, indent=2))
