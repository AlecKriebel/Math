"""Exact, dependency-free triangle-deletion checks for all labeled H on n<=4.

For monotone triangle-freeness, unrestricted edit distance is exactly the
minimum number of deletions hitting every original triangle.  The solver uses
the triangle hitting-set recurrence, never a relaxation or random search.
"""
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import time

def graph_triangles(vertex_count, edges):
    edge_set = set(edges)
    return [(u, v, w) for u, v, w in combinations(range(vertex_count), 3) if (u, v) in edge_set and (u, w) in edge_set and ((v, w) in edge_set)]

def exact_triangle_deletions(vertex_count, edges):
    """Return exact minimum deletions and one deletion witness.

    Each original triangle is a bit in a state. Deleting an edge clears all
    triangles containing it. For any still-present triangle, at least one of
    its three edges must be deleted, so branching on its edges is exhaustive.
    """
    edges = tuple(sorted(edges))
    edge_index = {edge: i for i, edge in enumerate(edges)}
    triangles = graph_triangles(vertex_count, edges)
    cover_masks = [0] * len(edges)
    triangle_edges = []
    for i, (u, v, w) in enumerate(triangles):
        ids = tuple((edge_index[e] for e in ((u, v), (u, w), (v, w))))
        triangle_edges.append(ids)
        for j in ids:
            cover_masks[j] |= 1 << i

    @lru_cache(maxsize=None)
    def solve(state):
        if not state:
            return (0, ())
        available = []
        remaining = state
        while remaining:
            bit = remaining & -remaining
            i = bit.bit_length() - 1
            candidates = triangle_edges[i]
            score = sum(((state & cover_masks[j]).bit_count() for j in candidates))
            available.append((score, i, candidates))
            remaining ^= bit
        _, _, candidates = max(available)
        best = None
        for j in sorted(candidates, key=lambda k: -(state & cover_masks[k]).bit_count()):
            subcost, subedges = solve(state & ~cover_masks[j])
            candidate = (1 + subcost, (j,) + subedges)
            if best is None or candidate[0] < best[0]:
                best = candidate
        return best
    answer, indices = solve((1 << len(triangles)) - 1)
    deleted = [edges[i] for i in indices]
    if not len(set(deleted)) == answer:
        raise AssertionError('verification failed at original line 69')
    repaired = set(edges) - set(deleted)
    if not not graph_triangles(vertex_count, repaired):
        raise AssertionError('verification failed at original line 71')
    return (answer, deleted, len(triangles), solve.cache_info().currsize)

def cover_edges(n, original_edges):
    lifted = []
    for i in range(3):
        for j in range(i + 1, 3):
            for u, v in original_edges:
                lifted.extend(((i * n + u, j * n + v), (i * n + v, j * n + u)))
    return sorted(lifted)

def main():
    began = time.monotonic()
    cases = []
    for n in range(5):
        pairs = list(combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            original = [edge for i, edge in enumerate(pairs) if mask >> i & 1]
            lifted = cover_edges(n, original)
            h_cost, h_witness, h_triangles, h_states = exact_triangle_deletions(n, original)
            l_cost, l_witness, l_triangles, l_states = exact_triangle_deletions(3 * n, lifted)
            if not l_cost >= h_cost:
                raise AssertionError('verification failed at original line 95')
            if not bool(h_triangles) == bool(l_triangles):
                raise AssertionError('verification failed at original line 96')
            if not l_triangles == 6 * h_triangles:
                raise AssertionError('verification failed at original line 97')
            projected = set()
            for x, y in l_witness:
                u, v = (x % n, y % n)
                projected.add(tuple(sorted((u, v))))
            if not len(projected) <= l_cost:
                raise AssertionError('verification failed at original line 103')
            if not not graph_triangles(n, set(original) - projected):
                raise AssertionError('verification failed at original line 104')
            if not all((x // n != y // n for x, y in lifted)):
                raise AssertionError('verification failed at original line 106')
            cases.append({'n': n, 'edge_mask': mask, 'H_edges': original, 'H_triangles': h_triangles, 'H_min_deletions': h_cost, 'H_witness': h_witness, 'L_vertices': 3 * n, 'L_edges_count': len(lifted), 'L_triangles': l_triangles, 'L_min_deletions': l_cost, 'L_witness': l_witness, 'projected_L_witness': sorted(projected), 'H_states': h_states, 'L_states': l_states})
    positive = [case for case in cases if case['H_min_deletions']]
    output = {'method': 'Exact memoized triangle hitting-set recurrence, exhaustive on every labeled graph H with 0<=n<=4.', 'normalization': 'Changed unordered pairs divided by vertex_count squared.', 'cases_checked': len(cases), 'cases_with_triangles': len(positive), 'all_proposed_cover_inequalities_hold': True, 'all_triangle_equivalences_hold': True, 'min_observed_unnormalized_L_over_H_ratio': min((case['L_min_deletions'] / case['H_min_deletions'] for case in positive)), 'elapsed_seconds': round(time.monotonic() - began, 6), 'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(), 'cases': cases}
    destination = Path(__file__).with_name('small_cover_results.json')
    destination.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({key: value for key, value in output.items() if key != 'cases'}, indent=2))
if __name__ == '__main__':
    main()
