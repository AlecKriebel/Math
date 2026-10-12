#!/usr/bin/env python3
"""Exact finite diagnostics for capped exploration, not an infinite-volume proof."""
from collections import Counter, deque
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib
import json

assertions = 0

def check(condition):
    global assertions
    assertions += 1
    assert condition


def edge(x, y):
    return tuple(sorted((x, y)))

vertices = [(u, n) for u in (0, 1) for n in range(3)]
vertical = sorted({edge((u, n), (u, (n+1) % 3)) for u in (0, 1) for n in range(3)})
horizontal = [edge((0, n), (1, n)) for n in range(3)]
edges = sorted(vertical+horizontal)
neighbors = {v: sorted(w for w in vertices if edge(v, w) in edges) for v in vertices}
root = (0, 0)


def explore(cap, reveal):
    accepted = {root}
    counts = Counter({0: 1})
    queue = deque([root])
    queried = set()
    horizontal_queries = 0
    while queue:
        v = queue.popleft()
        for w in neighbors[v]:
            e = edge(v, w)
            if e in queried:
                continue
            queried.add(e)
            if v[0] != w[0]:
                horizontal_queries += 1
            state = reveal(e)
            if state and w not in accepted and counts[w[0]] < cap:
                accepted.add(w)
                counts[w[0]] += 1
                queue.append(w)
    return tuple(sorted(accepted)), horizontal_queries

results = []
for cap in (1, 2):
    actual_law = Counter()
    reservoir_law = Counter()
    cap_consistent_cases = 0
    for bits in product((0, 1), repeat=len(edges)):
        states = dict(zip(edges, bits))
        reached, queries = explore(cap, states.__getitem__)
        check(queries <= 2*cap)
        check(all(c <= cap for c in Counter(v[0] for v in reached).values()))
        actual_law[reached] += 1
        full, _ = explore(len(vertices), states.__getitem__)
        if all(c <= cap for c in Counter(v[0] for v in full).values()):
            check(reached == full)
            cap_consistent_cases += 1
    pool_open_count = 0
    max_queries = 0
    for bits in product((0, 1), repeat=len(vertical)+2*cap):
        vert_states = dict(zip(vertical, bits[:len(vertical)]))
        pool = bits[len(vertical):]
        position = [0]
        def reveal(e):
            if e[0][0] == e[1][0]:
                return vert_states[e]
            value = pool[position[0]]
            position[0] += 1
            return value
        reached, queries = explore(cap, reveal)
        check(queries == position[0] and queries <= 2*cap)
        max_queries = max(max_queries, queries)
        check(not any(v[0] == 1 for v in reached) or any(pool))
        reservoir_law[reached] += 1
        pool_open_count += bool(any(pool))
    den_actual = 2**len(edges)
    den_reservoir = 2**(len(vertical)+2*cap)
    for event in set(actual_law) | set(reservoir_law):
        check(actual_law[event]*den_reservoir == reservoir_law[event]*den_actual)
    q = Fraction(1)-Fraction(1, 2)**(2*cap)
    check(Fraction(pool_open_count, den_reservoir) == q)
    results.append({'cap':cap,'actual_configurations':den_actual,'reservoir_configurations':den_reservoir,
                    'reached_set_laws_equal':True,'base_edge_parameter':str(q),
                    'maximum_observed_horizontal_queries':max_queries,
                    'configurations_where_cap_preserves_entire_cluster':cap_consistent_cases})

finite_product = Fraction(1)
for n in range(1, 65):
    finite_product *= 1-Fraction(1, 2**(n+1))
    check(finite_product >= Fraction(1, 2))
    check(sum(2**j for j in range(1, n+1)) == 2**(n+1)-2)

report = {'description':'Finite coupling and exact probability diagnostics; no universal percolation conclusion',
          'all_assertions_passed':True,'assertions':assertions,
          'test_graph':'K2 Cartesian product C3, used only as a finite diagnostic',
          'finite_coupling_tests':results,'inhomogeneous_ray_products_checked':64,
          'partial_note_sha256':hashlib.sha256(Path(__file__).with_name('PARTIAL.md').read_bytes()).hexdigest()}
Path(__file__).with_name('check_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
