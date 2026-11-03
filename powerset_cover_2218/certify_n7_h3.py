"""Complete, solver-independent exhaustive proof for n=7,h=3.
Color 0 on the empty set is reserved. Colors of all other sets are 1..6.
See README for the reduction to two singleton multiplicity patterns.
"""
from itertools import combinations, product
import json, time
from pathlib import Path
OUT = Path(__file__).parent
ALL = (1 << 6) - 1

def bits(d):
    while d:
        t = d & -d
        yield t
        d -= t

def solve(vcolors):
    edges = list(combinations(range(7), 2))
    index = {e: i for i, e in enumerate(edges)}
    constraints = []
    adj = [[] for e in edges]
    for t in combinations(range(7), 3):
        ids = tuple((index[e] for e in combinations(t, 2)))
        vm = sum(set((1 << vcolors[x] - 1 for x in t)))
        table = tuple((v for v in product(tuple(bits(ALL)), repeat=3) if (vm | v[0] | v[1] | v[2]).bit_count() >= 5))
        j = len(constraints)
        constraints.append((ids, table))
        for i in ids:
            adj[i].append(j)
    domains = [ALL] * 21
    if max(vcolors) == 4:
        domains[index[0, 1]] = 1 << 4
    stats = {'calls': 0, 'failures': 0, 'branch_nodes': 0, 'maximum_depth': 0, 'arc_revisions': 0}

    def search(ds, depth=0):
        stats['calls'] += 1
        stats['maximum_depth'] = max(stats['maximum_depth'], depth)
        queue = list(range(len(constraints)))
        pending = set(queue)
        while queue:
            j = queue.pop()
            pending.remove(j)
            ids, table = constraints[j]
            supp = [0, 0, 0]
            for v in table:
                if all((ds[i] & a for i, a in zip(ids, v))):
                    for k in range(3):
                        supp[k] |= v[k]
            if not supp[0]:
                stats['failures'] += 1
                return None
            for i, s in zip(ids, supp):
                nd = ds[i] & s
                if nd != ds[i]:
                    ds[i] = nd
                    stats['arc_revisions'] += 1
                    for jj in adj[i]:
                        if jj not in pending:
                            queue.append(jj)
                            pending.add(jj)
        if all((d.bit_count() == 1 for d in ds)):
            return ds
        i = min((i for i, d in enumerate(ds) if d.bit_count() > 1), key=lambda i: ds[i].bit_count())
        stats['branch_nodes'] += 1
        for a in bits(ds[i]):
            dd = ds.copy()
            dd[i] = a
            sol = search(dd, depth + 1)
            if sol:
                return sol
        return None
    t = time.monotonic()
    solution = search(domains)
    result = {'singleton_colors': vcolors, 'satisfiable': solution is not None, 'statistics': stats}
    if solution:
        result['edges'] = {str(e): d.bit_length() for e, d in zip(edges, solution)}
    return result
if __name__ == '__main__':
    results = []
    for p in [[1, 1, 2, 2, 3, 4, 5], [1, 1, 2, 2, 3, 3, 4]]:
        r = solve(p)
        results.append(r)
        print(json.dumps(r), flush=True)
    if not not any((r['satisfiable'] for r in results)):
        raise ValueError('Validation failed')
