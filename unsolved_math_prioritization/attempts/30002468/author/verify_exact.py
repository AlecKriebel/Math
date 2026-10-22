#!/usr/bin/env python3
"""Exact finite controls for conventions, not an asymptotic proof.

No external dependencies. All graph counts are integer exhaustive counts;
all probability calculations use fractions. The proof of the limit is in
PROOF.md and the external theorem remains an explicitly attributed input.
"""
from fractions import Fraction
from itertools import combinations
from math import comb
import json


def edge_set(n, mask):
    return {e for i, e in enumerate(combinations(range(n), 2)) if mask >> i & 1}


def is_induced_biclique(vertices, edges):
    vertices = tuple(vertices)
    if len(vertices) < 2:
        return False
    # Fix the first vertex on side A to count unordered bipartitions once.
    for bits in range(1 << (len(vertices)-1)):
        A = {vertices[0]} | {v for i, v in enumerate(vertices[1:]) if bits >> i & 1}
        B = set(vertices) - A
        if not B:
            continue
        target = {tuple(sorted((a,b))) for a in A for b in B}
        actual = {e for e in edges if e[0] in vertices and e[1] in vertices}
        if target == actual:
            return True
    return False


def main():
    counts = []
    for n in range(2,6):
        graph_count = 1 << comb(n,2)
        totals = {k:0 for k in range(2,n+1)}
        for mask in range(graph_count):
            edges = edge_set(n,mask)
            for k in totals:
                totals[k] += sum(is_induced_biclique(S,edges)
                                 for S in combinations(range(n),k))
        for k,total in totals.items():
            observed = Fraction(total,graph_count)
            expected = Fraction(comb(n,k)*((1 << (k-1))-1),1 << comb(k,2))
            assert observed == expected, (n,k,observed,expected)
            counts.append({"n":n,"k":k,"graphs":graph_count,
                           "induced_subset_total":total,"expectation":str(expected)})

    # Fixed side patterns at p != 1/2 are not equiprobable: the distinction
    # is exact already for K_(1,3) versus K_(2,2) on four fixed vertices.
    p=Fraction(1,3)
    a=p**3*(1-p)**3
    b=p**4*(1-p)**2
    assert a != b

    # Negative control: K_4 has complete-bipartite SUBGRAPHS on four
    # vertices but has no INDUCED complete bipartite graph on three or more.
    complete=edge_set(4,(1 << 6)-1)
    assert all(not is_induced_biclique(S,complete)
               for k in (3,4) for S in combinations(range(4),k))
    assert is_induced_biclique((0,1),complete)

    # Negative control: two stars can cover K_3 with overlap on edge 01,
    # but that collection is not an edge partition.
    pieces=[{(0,1),(0,2)},{(0,1),(1,2)}]
    assert set.union(*pieces)==edge_set(3,7)
    assert sum(len(x) for x in pieces)!=len(set.union(*pieces))
    print(json.dumps({"status":"PASS","scope":"finite convention controls only",
          "exact_count_checks":counts,
          "negative_controls":["non-induced versus induced",
                               "overlapping cover versus partition",
                               "p unequal to one half changes pattern probabilities"]},indent=2))


if __name__ == '__main__':
    main()
