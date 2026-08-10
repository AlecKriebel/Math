"""Derive, rather than import, a finite JC quartet invariant family."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import itertools
import math
from typing import Dict, Iterable, List, Sequence, Tuple

import sympy as sp

from jc_exact import (
    ORBITS4, Polynomial, coordinate_poly, descriptor_from_graph,
    p_add, p_hash, p_mul, quartet_coordinates,
)


Term = Tuple[int, Tuple[int, ...]]
Relation = Tuple[Term, ...]


def normalize_relation(terms: Iterable[Term]) -> Relation:
    d = Counter()
    for c, mon in terms: d[tuple(sorted(mon))] += int(c)
    d = Counter({m: c for m, c in d.items() if c})
    if not d: raise ValueError("zero relation vector")
    g = 0
    for c in d.values(): g = math.gcd(g, abs(c))
    out = tuple(sorted((c // g, m) for m, c in d.items()))
    if next(c for c, _ in out if c) < 0: out = tuple((-c, m) for c, m in out)
    return out


def coordinate_permutation(leaf_permutation: Sequence[int]):
    index = {q: i for i, q in enumerate(ORBITS4)}
    ans = []
    for q in ORBITS4:
        moved = tuple(q[leaf_permutation[k]] for k in range(4))
        canonical = min(
            tuple({0: 0, 1: p[0], 2: p[1], 3: p[2]}[x] for x in moved)
            for p in itertools.permutations((1, 2, 3))
        )
        ans.append(index[canonical])
    return tuple(ans)


COORDINATE_PERMUTATIONS = tuple(coordinate_permutation(p) for p in itertools.permutations(range(4)))


def _monomial_poly(coords: Sequence[Polynomial], mon: Sequence[int], nvar: int):
    out = {tuple([0] * nvar): 1}
    for i in mon: out = p_mul(out, coords[i])
    return out


def derive_family(source_graphs, max_degree: int = 3) -> Tuple[Relation, ...]:
    """Exact RREF nullspaces of all arm-homogeneous coordinate monomials.

    Every relation is regenerated from a source displayed-tree tensor.  The
    family is then closed under the 24 quartet slot permutations.
    """
    raw = set()
    descriptors = []
    for g in source_graphs:
        d = descriptor_from_graph(g)
        p = len([c for c in g.label_map.values() if c.startswith("L_")])
        for quartet in itertools.combinations(range(p), 4): descriptors.append((d, quartet))
    # Duplicate marginal descriptors do not change a nullspace.
    uniq = {}
    for d, q in descriptors: uniq[(d.key, q)] = (d, q)
    for degree in range(1, max_degree + 1):
        groups = defaultdict(list)
        for mon in itertools.combinations_with_replacement(range(15), degree):
            arm = tuple(sum(int(ORBITS4[i][k] != 0) for i in mon) for k in range(4))
            groups[arm].append(mon)
        for d, quartet in uniq.values():
            coords = quartet_coordinates(d, quartet); cache = {}
            for mons in groups.values():
                if len(mons) < 2: continue
                polys = []
                for mon in mons:
                    if mon not in cache: cache[mon] = _monomial_poly(coords, mon, d.variable_count)
                    polys.append(cache[mon])
                rows = sorted(set().union(*(x.keys() for x in polys)))
                matrix = sp.polys.matrices.DomainMatrix.from_list_sympy(
                    len(rows), len(mons), [[poly.get(m, 0) for poly in polys] for m in rows]
                )
                ns = matrix.nullspace().to_Matrix()
                for rr in range(ns.rows):
                    vals = [int(ns[rr, c]) for c in range(ns.cols)]
                    raw.add(normalize_relation((c, mon) for c, mon in zip(vals, mons) if c))
    closed = set()
    for rel in raw:
        for mp in COORDINATE_PERMUTATIONS:
            closed.add(normalize_relation((c, tuple(mp[i] for i in mon)) for c, mon in rel))
    return tuple(sorted(closed, key=repr))


def relation_poly(coords: Sequence[Polynomial], rel: Relation, nvar: int):
    out = {}
    for c, mon in rel: out = p_add(out, _monomial_poly(coords, mon, nvar), c)
    return out


def relation_value(values: Sequence[int], rel: Relation, prime: int):
    total = 0
    for c, mon in rel:
        z = c % prime
        for i in mon: z = z * values[i] % prime
        total = (total + z) % prime
    return total


def family_metadata(family: Sequence[Relation]):
    return {
        "count": len(family),
        "by_total_degree": dict(sorted(Counter(len(rel[0][1]) for rel in family).items())),
        "by_term_count": dict(sorted(Counter(len(rel) for rel in family).items())),
    }


def exact_relation_pullback(desc, quartet, rel):
    coords = quartet_coordinates(desc, quartet)
    return relation_poly(coords, rel, desc.variable_count)

