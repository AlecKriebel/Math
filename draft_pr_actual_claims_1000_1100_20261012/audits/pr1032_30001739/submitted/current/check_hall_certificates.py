#!/usr/bin/env python3
"""Independent direct singleton Hall checks for all possible factor partitions."""
import json, itertools
from pathlib import Path
S = {'A': (0, 2), 'B': (1, 4), 'C': (3, 3), 'D': (2, 5), 'E': (4, 6)}
ROWS = [('E', 'DCBA', 'DCBA', 'E', 'D', 'E'), ('D', 'ECBA', 'D', 'ECBA', 'D', 'E'), ('C', 'EDBA', 'C', 'EDBA', 'C', 'E'), ('B', 'EDCA', 'B', 'EDCA', 'B', 'D'), ('A', 'EDCB', 'A', 'EDCB', 'A', 'C'), ('ED', 'CBA', 'CBA', 'ED', 'C', 'E'), ('EC', 'DBA', 'DBA', 'EC', 'D', 'E'), ('EB', 'DCA', 'EB', 'DCA', 'B', 'D'), ('EA', 'DCB', 'EA', 'DCB', 'A', 'C'), ('DC', 'EBA', 'DC', 'EBA', 'D', 'E'), ('DB', 'ECA', 'DB', 'ECA', 'D', 'E'), ('DA', 'ECB', 'DA', 'ECB', 'D', 'E'), ('CB', 'EDA', 'CB', 'EDA', 'C', 'E'), ('CA', 'EDB', 'CA', 'EDB', 'C', 'E'), ('BA', 'EDC', 'BA', 'EDC', 'B', 'D')]

def before(t, u):
    T = set(range(t[0], t[1] + 1))
    U = set(range(u[0], u[1] + 1))
    W = T | U
    return min(T) < min(U) and (not T <= U) and (not U <= T) and (max(W) - min(W) + 1 == len(W))

def ladder(s):
    pairs = [S[c] for c in sorted(s, key=lambda c: S[c][0], reverse=True)]
    return all((pairs[i][1] > pairs[i + 1][1] for i in range(len(pairs) - 1)))

def main():
    records = []
    seen = set()
    for l, r, m, n, a, b in ROWS:
        if not (set(l).isdisjoint(r) and set(l + r) == set(S)):
            raise RuntimeError('Diagnostic invariant failed')
        if not {frozenset(l), frozenset(r)} == {frozenset(m), frozenset(n)}:
            raise RuntimeError('Diagnostic invariant failed')
        if not (ladder(l) or ladder(r)):
            raise RuntimeError('Diagnostic invariant failed')
        if not (a in m and b in n and before(S[a], S[b])):
            raise RuntimeError('Diagnostic invariant failed')
        Y = [(c, d) for c in m for d in n if before((S[c][0] - 1, S[c][1] - 1), S[d])]
        neighbors = [(c, d) for c, d in Y if c == a and before(S[d], S[b]) or (d == b and before(S[a], S[c]))]
        if not neighbors == []:
            raise RuntimeError('Diagnostic invariant failed')
        key = frozenset((frozenset(l), frozenset(r)))
        if not key not in seen:
            raise RuntimeError('Diagnostic invariant failed')
        seen.add(key)
        records.append({'partition': [l, r], 'ladder_sides': [x for x in (l, r) if ladder(x)], 'failed_LC': [m, n], 'isolated_X_vertex': [a, b], 'Y': Y, 'neighbors': neighbors, 'hall_defect': 1})
    expected = {frozenset((frozenset(p), frozenset(set(S) - set(p)))) for k in (1, 2) for p in itertools.combinations(S, k)}
    if not (seen == expected and len(seen) == 15):
        raise RuntimeError('Diagnostic invariant failed')
    out = {'all_15_partitions_covered': True, 'all_have_a_ladder_side': True, 'all_Hall_singleton_obstructions_verified': True, 'multiplicity_computed': False, 'certificates': records}
    print(json.dumps(out, indent=2, sort_keys=True))
if __name__ == '__main__':
    main()
