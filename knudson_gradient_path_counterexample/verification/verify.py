#!/usr/bin/env python3
"""Exact verification of a counterexample to OWR-2040-002.

Python 3.9+, standard library only. Run:
    python3 gradient_path_counterexample.py

Checks the simplex-wise filtration, computes persistence over F_2,
independently computes the H_0 pairing by union-find, constructs V_P,
checks the modified Hasse diagram is acyclic, and enumerates every
path between the two nonincident persistence pairs.

Source: Kevin P. Knudson, "Persistent homology and discrete Morse
 theory", Oberwolfach Report 29/2008, pp. 1628-1630, Conjecture 2.
DOI of the workshop report: 10.4171/OWR/2008/29.
"""
from __future__ import annotations

from collections import deque
from functools import lru_cache

Simplex = tuple[str, ...]


def check(condition: bool, message: str) -> None:
    """Unlike assert, these checks also run when Python uses -O."""
    if not condition:
        raise RuntimeError(message)


def facets(s: Simplex) -> tuple[Simplex, ...]:
    if len(s) == 1:
        return ()  # Ordinary, unaugmented homology.
    return tuple(s[:i] + s[i + 1:] for i in range(len(s)))


def name(s: Simplex) -> str:
    return ''.join(s)


def main() -> None:
    simplices: tuple[Simplex, ...] = (
        ('a',), ('b',), ('c',), ('d',),
        ('c', 'd'), ('b', 'd'), ('a', 'c'),
    )
    index = {s: i for i, s in enumerate(simplices)}
    check(len(index) == len(simplices), 'Duplicate simplex')
    for j, s in enumerate(simplices):
        check(tuple(sorted(set(s))) == s, 'Invalid simplex')
        for face in facets(s):
            check(face in index and index[face] < j,
                  'A face is absent or appears after its coface')

    # First computation: ordinary left-to-right boundary reduction over F_2.
    boundary = [{index[f] for f in facets(s)} for s in simplices]
    reduced: list[set[int]] = []
    pivot_owner: dict[int, int] = {}
    pairing: list[tuple[int, int]] = []
    for j, original in enumerate(boundary):
        column = set(original)
        while column and max(column) in pivot_owner:
            column.symmetric_difference_update(reduced[pivot_owner[max(column)]])
        reduced.append(column)
        if column:
            low = max(column)
            pivot_owner[low] = j
            pairing.append((low, j))

    check(pairing == [(3, 4), (2, 5), (1, 6)], 'Incorrect persistence pairing')
    check(reduced[4:] == [{2, 3}, {1, 2}, {0, 1}],
          'Incorrect reduced columns')

    # Second, independent computation: H_0 components and the elder rule.
    parent: dict[str, str] = {}
    birth: dict[str, int] = {}

    def root(v: str) -> str:
        while parent[v] != v:
            v = parent[v]
        return v

    component_pairing: list[tuple[int, int]] = []
    for j, s in enumerate(simplices):
        if len(s) == 1:
            parent[s[0]] = s[0]
            birth[s[0]] = j
        else:
            check(len(s) == 2, 'Union-find verifier expects a graph')
            u, v = map(root, s)
            if u != v:
                older, younger = sorted((u, v), key=birth.__getitem__)
                component_pairing.append((birth[younger], j))
                parent[younger] = older
    check(component_pairing == pairing, 'Independent pairing methods disagree')

    # V_P contains precisely the incident persistence pairs.
    matching = {
        (simplices[i], simplices[j]) for i, j in pairing
        if simplices[i] in facets(simplices[j])
    }
    check(matching == {(('d',), ('c', 'd'))}, 'Incorrect V_P')
    endpoints = [s for pair in matching for s in pair]
    check(len(set(endpoints)) == len(endpoints), 'V_P is not a matching')

    # Hasse incidences point down, except matched incidences, which point up.
    adjacency: dict[Simplex, list[Simplex]] = {s: [] for s in simplices}
    for coface in simplices:
        for face in facets(coface):
            if (face, coface) in matching:
                adjacency[face].append(coface)
            else:
                adjacency[coface].append(face)

    # Independently check acyclicity by topological sorting.
    indegree = {s: 0 for s in simplices}
    for neighbors in adjacency.values():
        for s in neighbors:
            indegree[s] += 1
    queue = deque(s for s in simplices if indegree[s] == 0)
    visited = 0
    while queue:
        s = queue.popleft()
        visited += 1
        for t in adjacency[s]:
            indegree[t] -= 1
            if indegree[t] == 0:
                queue.append(t)
    check(visited == len(simplices), 'The modified Hasse diagram has a cycle')

    @lru_cache(maxsize=None)
    def paths(start: Simplex, target: Simplex) -> tuple[tuple[Simplex, ...], ...]:
        if start == target:
            return ((start,),)
        return tuple(
            (start,) + tail
            for next_simplex in adjacency[start]
            for tail in paths(next_simplex, target)
        )

    check(paths(('b', 'd'), ('c',)) ==
          ((('b', 'd'), ('d',), ('c', 'd'), ('c',)),),
          'Unexpected paths for (c,bd)')
    check(paths(('a', 'c'), ('b',)) == (),
          'Counterexample failed: a path from ac to b exists')

    print('Filtration: ' + ', '.join(map(name, simplices)))
    for j in range(4, len(simplices)):
        support = ' + '.join(name(simplices[i]) for i in sorted(reduced[j]))
        print(f'R({name(simplices[j])}) = {support}')
    print('P = ' + str([(name(simplices[i]), name(simplices[j])) for i, j in pairing]))
    print('Independent union-find pairing: AGREES')
    print('V_P = ' + str(sorted((name(a), name(b)) for a, b in matching)))
    print('Modified Hasse diagram: ACYCLIC')
    for i, j in pairing:
        sigma, tau = simplices[i], simplices[j]
        if (sigma, tau) not in matching:
            found = paths(tau, sigma)
            print(f'Paths {name(tau)} -> {name(sigma)}: {len(found)}')
            for path in found:
                print('  ' + ' -> '.join(map(name, path)))
    print('VERIFIED: (b,ac) is a nonincident persistence pair with ZERO gradient paths.')


if __name__ == '__main__':
    main()
