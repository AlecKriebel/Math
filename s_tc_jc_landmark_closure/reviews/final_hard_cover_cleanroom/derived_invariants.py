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


_PAIR_SEPARATOR_CACHE = {}


def derive_pair_separator_on_quartet(source_desc, target_desc, quartet,
                                     max_degree: int = 4,
                                     arm_degree_hint=None):
    """Derive a target identity that is nonzero on the source.

    This is a per-pair clean-room construction, not a lookup in the primary
    invariant list.  For each arm-multihomogeneous coordinate-monomial block,
    it computes the exact target nullspace and tests its basis on the source.
    If any relation in the target kernel separates the pair, at least one
    nullspace-basis vector has nonzero source pullback.
    """
    quartet = tuple(quartet)
    arm_degree_hint = (
        tuple(int(x) for x in arm_degree_hint)
        if arm_degree_hint is not None else None
    )
    key = (
        source_desc.key, target_desc.key, quartet, int(max_degree),
        arm_degree_hint,
    )
    if key in _PAIR_SEPARATOR_CACHE:
        return _PAIR_SEPARATOR_CACHE[key]
    source_coords = quartet_coordinates(source_desc, quartet)
    target_coords = quartet_coordinates(target_desc, quartet)
    source_cache = {}
    target_cache = {}
    for degree in range(1, max_degree + 1):
        groups = defaultdict(list)
        for monomial in itertools.combinations_with_replacement(range(15), degree):
            arm_degree = tuple(
                sum(int(ORBITS4[index][arm] != 0) for index in monomial)
                for arm in range(4)
            )
            if arm_degree_hint is None or arm_degree == arm_degree_hint:
                groups[arm_degree].append(monomial)
        for arm_degree, monomials in sorted(groups.items()):
            if len(monomials) < 2:
                continue
            target_polys = []
            for monomial in monomials:
                if monomial not in target_cache:
                    target_cache[monomial] = _monomial_poly(
                        target_coords, monomial, target_desc.variable_count,
                    )
                target_polys.append(target_cache[monomial])
            rows = sorted(set().union(*(poly.keys() for poly in target_polys)))
            matrix = sp.polys.matrices.DomainMatrix.from_list_sympy(
                len(rows), len(monomials),
                [[poly.get(row, 0) for poly in target_polys] for row in rows],
            )
            nullspace = matrix.nullspace().to_Matrix()
            for basis_row in range(nullspace.rows):
                relation = normalize_relation(
                    (int(nullspace[basis_row, column]), monomial)
                    for column, monomial in enumerate(monomials)
                    if nullspace[basis_row, column]
                )
                source_poly = {}
                for coefficient, monomial in relation:
                    if monomial not in source_cache:
                        source_cache[monomial] = _monomial_poly(
                            source_coords, monomial, source_desc.variable_count,
                        )
                    source_poly = p_add(
                        source_poly, source_cache[monomial], coefficient,
                    )
                if not source_poly:
                    continue
                target_poly = relation_poly(
                    target_coords, relation, target_desc.variable_count,
                )
                if target_poly:
                    raise AssertionError("target nullspace vector expanded nonzero")
                result = {
                    "relation": relation,
                    "degree": degree,
                    "arm_degree": arm_degree,
                    "source_polynomial_sha256": p_hash(source_poly),
                    "source_polynomial_term_count": len(source_poly),
                    "target_zero": True,
                }
                _PAIR_SEPARATOR_CACHE[key] = result
                return result
    _PAIR_SEPARATOR_CACHE[key] = None
    return None
