#!/usr/bin/env python3
"""Exact independent finite grid enumeration, explicitly not a global optimum oracle."""
from collections import Counter
from itertools import combinations
import json
import os

grid = tuple((x,y) for x in range(-1,2) for y in range(-1,2))
results = []
for n in range(1,10):
    histogram = Counter()
    best = -1
    best_points = None
    best_counts = None
    for p in combinations(grid, n):
        assert len(set(p)) == n
        counts = [len({(x-u)*(x-u)+(y-v)*(y-v) for j,(u,v) in enumerate(p)
                       if j != i}) for i,(x,y) in enumerate(p)]
        m = len(set(counts))
        assert m <= (1 if n==1 else n-1)
        histogram[m] += 1
        if m > best:
            best, best_points, best_counts = m, p, counts
    if n <= 4:
        assert best == (1 if n<=2 else n-1)
    results.append({"n":n,"grid_subsets":sum(histogram.values()),"max_M_on_grid":best,
                    "witness":best_points,"witness_counts":best_counts,
                    "M_histogram":dict(sorted(histogram.items()))})
assert sum(r["grid_subsets"] for r in results)==511
print(json.dumps({"pid":os.getpid(),"arithmetic":"integer squared distances",
    "global_g_n_claim":"Only n<=4 use the independently proved universal upper bound; n>=5 maxima are grid-restricted.",
    "results":results},indent=2))
