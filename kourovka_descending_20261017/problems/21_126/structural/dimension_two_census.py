#!/usr/bin/env python3
"""Expanded sufficient class using Huang–Osajda2019; standard library only."""
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import json
from graph_census import adjacency, components, induce, canonical


@lru_cache(None)
def sufficient(rows):
    n = len(rows)
    if not n:
        return True
    # Triangle-free RAAGs have cohomological dimension <=2.
    if not any(rows[i] >> j & 1 and rows[i] & rows[j]
               for i, j in combinations(range(n), 2)):
        return True
    anti = components(rows, complement=True)
    if len(anti) <= 3 and all(
        all(not (rows[v] >> w & 1) for v, w in combinations(part, 2))
        for part in anti
    ):
        return True
    comps = components(rows)
    if len(comps) > 1:
        return all(sufficient(induce(rows, part)) for part in comps)
    universals = {v for v in range(n) if rows[v].bit_count() == n - 1}
    if universals:
        return sufficient(induce(rows, tuple(v for v in range(n) if v not in universals)))
    return False


def main():
    result = {'meaning': 'expanded sufficient polynomial exclusion class only',
              'seed': 'triangle-free graphs or complete multipartite with <=3 parts',
              'closure': 'disjoint unions; adding universal vertices',
              'labelled_counts': [], 'isomorphism_counts': []}
    for n in range(7):
        inside, outside = [], []
        for mask in range(1 << (n * (n - 1) // 2)):
            (inside if sufficient(adjacency(n, mask)) else outside).append(mask)
        result['labelled_counts'].append(dict(vertices=n, inside=len(inside), outside=len(outside)))
        if n <= 5:
            yes = {canonical(n, mask) for mask in inside}
            no = {canonical(n, mask) for mask in outside}
            assert not yes & no
            result['isomorphism_counts'].append(dict(vertices=n, inside=len(yes), outside=len(no), outside_canonical_masks=sorted(no)))
            if n == 5:
                pairs = tuple(combinations(range(n), 2))
                result['outside_5vertex_graphs'] = [dict(mask=mask,edges=[list(pair) for k,pair in enumerate(pairs) if mask>>k&1]) for mask in sorted(no)]
    assert all(x['outside']==0 for x in result['labelled_counts'] if x['vertices']<=4)
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
