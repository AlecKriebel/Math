#!/usr/bin/env python3
"""Exact Laurent-polynomial checks for the cyclic-cover chain certificates.

This checks finite instances of the cellular formulas, not the F_n theorems,
infinite-group classification, literature status, or the original conjecture.
Uses only the Python standard library.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import product
import json


def clean(p):
    return {e: c for e, c in p.items() if c}


def add(p, q, scale=1):
    r = defaultdict(int, p)
    for e, c in q.items():
        r[e] += scale * c
    return clean(r)


def mul(p, q):
    r = defaultdict(int)
    for e, c in p.items():
        for f, d in q.items():
            r[e + f] += c * d
    return clean(r)


def tminusone(w):
    return add({w: 1}, {0: 1}, -1)


def boundary(chain, weights):
    out = {}
    for cell, poly in chain.items():
        before = 0
        for i, edge in enumerate(cell):
            if edge is None:
                continue
            face = cell[:i] + (None,) + cell[i + 1:]
            term = mul(poly, tminusone(weights[i][edge]))
            out[face] = add(out.get(face, {}), term, (-1) ** before)
            before += 1
    return {c: p for c, p in out.items() if p}


def tensor_cycle(weights):
    chain = {(): {0: 1}}
    for p, q in weights:
        # q*a - p*b in the boundary-module sense.
        factors = (tminusone(q), {e: -c for e, c in tminusone(p).items()})
        if p == q == 0:
            factors = ({0: 1}, {0: -1})
        next_chain = {}
        for cell, poly in chain.items():
            for edge, v in enumerate(factors):
                coeff = mul(poly, v)
                if coeff:
                    next_chain[cell + (edge,)] = coeff
        chain = next_chain
    return chain


def standard_cycle(s):
    return {cell: {0: (-1) ** sum(cell)} for cell in product((0, 1), repeat=s)}


def main():
    summary = []
    tested_cells = 0
    for s in range(1, 8):
        weights = [(1, 1)] * s
        for cell in product((None, 0, 1), repeat=s):
            assert boundary(boundary({cell: {0: 1}}, weights), weights) == {}
            tested_cells += 1
        z = standard_cycle(s)
        assert boundary(z, weights) == {}
        assert z[(0,) * s] == {0: 1}
        assert all(all(x is not None for x in c) for c in z)
        summary.append({"s": s, "top_terms": len(z), "boundary_zero": True,
                        "unit_coefficient": True, "ambient_dimension": s})

    weighted = []
    patterns = [(2, 3), (-2, 5), (0, 7), (1, 0), (-3, -1), (0, 0)]
    for s in range(1, 7):
        weights = patterns[:s]
        z = tensor_cycle(weights)
        assert z and boundary(z, weights) == {}
        # A nonzero vector in a free module over Z[t,t^-1] is R-torsion-free.
        weighted.append({"weights": weights, "top_terms": len(z), "boundary_zero": True})

    slopes = []
    for n in range(1, 101):
        r = Fraction(2, 2 * n + 1)
        assert Fraction(1, n + 1) < r < Fraction(1, n)
        slopes.append(str(r))

    result = {
        "passed": True,
        "scope": "Finite exact checks of Laurent cellular differentials, explicit top cycles, and the nonstabilizing-open-set example only.",
        "not_verified_by_computation": ["Bestvina-Brady theorem", "BNSR calculations", "infinite-group finiteness classification", "KOU-21.119"],
        "boundary_squared_cells_checked": tested_cells,
        "standard_top_cycles": summary,
        "weighted_top_cycles": weighted,
        "strict_rational_annulus_checks": len(slopes),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
