#!/usr/bin/env python3
"""Independent exact checks; Python 3.9+, standard library only.

Uses component partitions (no union-find) to obtain barcode ranks, takes
mixed differences to recover finite intervals, and independently performs
oriented reduction over Q and five prime fields. Checks path reversal too.
The proof in the paper is sufficient without this program.
"""
from fractions import Fraction
from itertools import permutations

VERTICES = ('a', 'b', 'c', 'd')
EDGES = ('cd', 'bd', 'ac')
FILTRATION = VERTICES + EDGES
EXPECTED = [(4, 5), (3, 6), (2, 7)]  # one-based birth and death


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def components(stage):
    """Reconstruct each stage from scratch by undirected reachability."""
    cells = FILTRATION[:stage]
    remaining = {s for s in cells if len(s) == 1}
    adjacency = {v: set() for v in remaining}
    for edge in (s for s in cells if len(s) == 2):
        a, b = edge
        require(a in remaining and b in remaining, 'invalid filtration')
        adjacency[a].add(b)
        adjacency[b].add(a)
    answer = []
    while remaining:
        todo = [min(remaining)]
        group = set()
        while todo:
            v = todo.pop()
            if v not in group:
                group.add(v)
                todo.extend(adjacency[v] - group)
        remaining -= group
        answer.append(group)
    return answer


def rank(i, j):
    # Image rank H0(K_i)->H0(K_j) is the number of j-components
    # intersecting the set of vertices already present at i.
    old = {s for s in FILTRATION[:i] if len(s) == 1}
    return sum(bool(c & old) for c in components(j))


def barcode_pairs():
    pairs = []
    for death in range(1, 8):
        for birth in range(1, death):
            m = (rank(birth, death - 1) - rank(birth - 1, death - 1)
                 - rank(birth, death) + rank(birth - 1, death))
            require(m >= 0, 'negative interval multiplicity')
            pairs.extend([(birth, death)] * m)
    require(rank(1, 7) == 1, 'oldest component does not survive')
    return pairs


def oriented_reduction(prime=None):
    scalar = Fraction if prime is None else lambda x: x % prime
    columns, owners, pairs = [], {}, []
    for j, edge in enumerate(EDGES, 5):
        col = [scalar(int(v == edge[1]) - int(v == edge[0])) for v in VERTICES]
        while any(col):
            p = max(i for i, value in enumerate(col) if value)
            if p not in owners:
                owners[p] = len(columns)
                pairs.append((p + 1, j))
                break
            old = columns[owners[p]]
            factor = col[p] / old[p] if prime is None else col[p] * pow(old[p], -1, prime) % prime
            col = [scalar(x - factor * y) for x, y in zip(col, old)]
        columns.append(col)
    return pairs, columns


def arrows(matching):
    adjacency = {s: [] for s in FILTRATION}
    for e in EDGES:
        for v in e:
            start, end = (v, e) if (v, e) in matching else (e, v)
            adjacency[start].append(end)
    return adjacency


def all_paths(adjacency, start, target, trail=()):
    require(start not in trail, 'cycle encountered')
    if start == target:
        return [trail + (start,)]
    return [p for nxt in adjacency[start]
            for p in all_paths(adjacency, nxt, target, trail + (start,))]


def main():
    pairs = barcode_pairs()
    require(pairs == EXPECTED, 'rank-invariant pairing disagrees')
    print('H0 rank-invariant finite pairs:', pairs)
    for prime in (None, 2, 3, 5, 7, 101):
        result, columns = oriented_reduction(prime)
        require(result == pairs, 'oriented pairing disagrees')
        if prime is None:
            require(columns == [[0, 0, -1, 1], [0, -1, 1, 0], [-1, 1, 0, 0]],
                    'unexpected rational reduced columns')
        print('Oriented reduction over', 'Q' if prime is None else f'F_{prime}', ': AGREES')
    matching = {(FILTRATION[i-1], FILTRATION[j-1]) for i, j in pairs
                if FILTRATION[i-1] in FILTRATION[j-1]}
    require(matching == {('d', 'cd')}, 'wrong matching')
    adjacency = arrows(matching)
    # Exhaust all starts; the path enumerator refuses cycles.
    for s in FILTRATION:
        for t in FILTRATION:
            all_paths(adjacency, s, t)
    require(all_paths(adjacency, 'ac', 'b') == [], 'path exists in fixed field')
    require(all_paths(adjacency, 'bd', 'c') == [('bd', 'd', 'cd', 'c')],
            'wrong earlier cancellation path')
    modified = arrows({('d', 'bd'), ('c', 'cd')})
    require(all_paths(modified, 'ac', 'b') == [('ac', 'c', 'cd', 'd', 'bd', 'b')],
            'wrong path after earlier cancellation')
    print('Fixed-field ac -> b paths: 0; after cancelling (c,bd): 1')
    # Every label relabeling leaves the combinatorial reachability unchanged.
    for perm in permutations(VERTICES):
        mapping = dict(zip(VERTICES, perm))
        rename = lambda s: ''.join(sorted(mapping[v] for v in s))
        renamed = {rename(s): [rename(t) for t in out] for s, out in adjacency.items()}
        require(all_paths(renamed, rename('ac'), rename('b')) == [], 'label dependence')
    print('All 24 vertex relabelings: zero-path obstruction unchanged')
    print('INDEPENDENT CHECK PASSED')


if __name__ == '__main__':
    main()
