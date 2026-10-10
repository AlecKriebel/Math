"""Read-only exact certificate audit, with edge-subset ranks and BFS connectivity.

This validates existing examples and the stated proof constructions. It is not a
counterexample search. No use of assertions, floating-point arithmetic, or files
opened for writing. Set GREEDY_PACKET to a frozen copy of the author's packet.
"""
from fractions import Fraction as Q
from itertools import combinations, permutations
from pathlib import Path
from functools import lru_cache
import importlib.util
import json
import os
import sys

sys.dont_write_bytecode = True
PACKET = Path(os.environ.get('GREEDY_PACKET', Path(__file__).resolve().parents[2] / 'greedy_spanning_tree_30001934'))
spec = importlib.util.spec_from_file_location('author_exact_model', PACKET / 'tests/exact_model.py')
author = importlib.util.module_from_spec(spec)
spec.loader.exec_module(author)


def need(value, message):
    if not value:
        raise RuntimeError(message)


def rank(n, edges, subset):
    adjacency = [set() for _ in range(n)]
    for i in subset:
        u, v = edges[i]
        adjacency[u].add(v)
        adjacency[v].add(u)
    unseen = set(range(n))
    components = 0
    while unseen:
        components += 1
        frontier = {next(iter(unseen))}
        while frontier:
            vertex = frontier.pop()
            if vertex not in unseen:
                continue
            unseen.remove(vertex)
            frontier.update(adjacency[vertex] & unseen)
    return n - components


@lru_cache(None)
def edge_rank_rows(n, edges):
    rows = []
    for mask in range(1 << len(edges)):
        indices = tuple(i for i in range(len(edges)) if mask & (1 << i))
        rows.append((indices, rank(n, edges, indices)))
    return tuple(rows)


def independent_trees(n, edges):
    return tuple(t for t in combinations(range(len(edges)), n - 1) if rank(n, edges, t) == n - 1)


def independent_member(n, edges, z, mass):
    if mass < 0 or any(a < 0 for a in z) or sum(z) != mass * (n - 1):
        return False
    if mass == 0:
        return all(a == 0 for a in z)
    return all(sum(z[i] for i in subset) <= mass * r for subset, r in edge_rank_rows(n, edges))


def independent_maximum(n, edges, w, k, tree):
    need(independent_member(n, edges, w, k), 'independent input membership')
    need(tree in independent_trees(n, edges), 'independent spanning tree')
    selected = set(tree)
    bounds = [Q(k)] + [Q(w[i]) for i in tree]
    for subset, r in edge_rank_rows(n, edges):
        d = r - sum(i in selected for i in subset)
        if d:
            bounds.append(Q(k * r - sum(w[i] for i in subset), d))
    return min(bounds)


def certify_endpoint(n, edges, w, k, tree, alleged):
    actual = independent_maximum(n, edges, w, k, tree)
    need(actual == alleged, 'alleged endpoint differs from independent rank endpoint')
    for coefficient, expected in ((actual, True), (actual + Q(1, 1009), False)):
        z = [Q(a) - coefficient * (i in tree) for i, a in enumerate(w)]
        need(independent_member(n, edges, z, k - coefficient) is expected,
             'endpoint or strict continuation test failed')
    need(author.maximum(n, edges, list(w), k, tree)[0] == actual, 'author endpoint disagreement')
    return actual


def reject(label, fn):
    try:
        fn()
    except RuntimeError:
        return label
    raise RuntimeError('intended mutant survived: ' + label)


def check_recorded_examples():
    cases = json.loads((PACKET / 'results/exact_selection_certificates.json').read_text())
    need(len(cases) == 3, 'expected exactly three published example cases')
    total = 0
    summaries = []
    for case in cases:
        n, k, w = case['n'], case['k'], case['w']
        edges = tuple(map(tuple, case['edges']))
        trees = independent_trees(n, edges)
        listed = tuple(tuple(row['tree_edge_indices']) for row in case['rows'])
        need(listed == trees, 'record lacks a tree or contains a duplicate/non-tree')
        need(case['tree_count'] == len(trees), 'case tree count')
        values = []
        for tree, row in zip(trees, case['rows']):
            value = certify_endpoint(n, edges, w, k, tree, Q(row['maximum']))
            kind, *extra = row['limiting_constraint']
            if kind == 'mass':
                need(value == k, 'unbound mass witness')
            elif kind == 'edge':
                need(extra[0] in tree and value == w[extra[0]], 'unbound edge witness')
            elif kind == 'subset':
                vertices = {v for v in range(n) if extra[0] & (1 << v)}
                internal = [i for i, (a, b) in enumerate(edges) if a in vertices and b in vertices]
                deficit = len(vertices) - 1 - sum(i in tree for i in internal)
                need(deficit > 0, 'nonpositive witness denominator')
                need(value * deficit == k * (len(vertices) - 1) - sum(w[i] for i in internal), 'unbound subset witness')
            else:
                raise RuntimeError('unknown witness type')
            values.append(value)
        good = sum(v.denominator == 1 for v in values)
        need(good == case['integer_maxima'] and good > 0, 'integer count or fake target counterexample')
        need(case['membership'] is True and case['target_counterexample'] is False, 'case scope flags')
        total += len(trees)
        summaries.append({'label': case['label'], 'trees': len(trees), 'integer_maxima': good,
                          'smallest': str(min(values)), 'largest': str(max(values))})
    need(total == 157, 'total example trees')
    need(summaries[1]['largest'] == '9/2' and summaries[1]['integer_maxima'] == 105, 'global selection example')
    return summaries


def check_small_graph_construction():
    checked = 0
    nonpath = 0
    for n in range(1, 5):
        possible = tuple(combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            edges = tuple(e for i, e in enumerate(possible) if mask & (1 << i))
            trees = independent_trees(n, edges)
            if not trees:
                continue
            paths = []
            for order in permutations(range(n)):
                pairs = tuple(tuple(sorted(e)) for e in zip(order, order[1:]))
                if all(e in edges for e in pairs):
                    paths.append(tuple(edges.index(e) for e in pairs))
            if paths:
                chosen = paths[0]
                for vertex_mask in range(1, (1 << n) - 1):
                    vertices = {v for v in range(n) if vertex_mask & (1 << v)}
                    selected_inside = sum(edges[i][0] in vertices and edges[i][1] in vertices for i in chosen)
                    need(len(vertices) - 1 - selected_inside <= 1, 'small-graph path denominator')
            else:
                nonpath += 1
                need(n == 4 and len(trees) == 1 and len(edges) == 3, 'nonpath graph is not a unique-tree star')
            checked += 1
    need(checked == 44 and nonpath == 4, 'labeled small connected graph totals')
    return {'connected_labeled_graphs': checked, 'nonpath_stars': nonpath}


def check_k5_structure():
    vertices = set(range(5))
    edges = tuple(combinations(range(5), 2))
    triples = list(combinations(range(5), 3))
    need(all(sum(a in s and b in s for s in triples) == 3 for a, b in edges), 'inside multiplicity')
    need(all(sum((a in s) != (b in s) for s in triples) == 6 for a, b in edges), 'crossing multiplicity')
    checked = 0
    for triple in triples:
        inside = set(triple)
        outside = vertices - inside
        crossing = [(a, b) for a in inside for b in outside]
        need(len(crossing) == 6, 'K5 cut size')
        for a, b in crossing:
            rest = sorted(inside - {a})
            other = next(iter(outside - {b}))
            order = (a, b, rest[0], other, rest[1])
            tree = tuple(edges.index(tuple(sorted(e))) for e in zip(order, order[1:]))
            exceptional = []
            for mask in range(1, 31):
                subset = {v for v in vertices if mask & (1 << v)}
                d = len(subset) - 1 - sum(edges[i][0] in subset and edges[i][1] in subset for i in tree)
                if d > 1:
                    exceptional.append((subset, d))
            need(exceptional == [(inside, 2)], 'K5 exceptional path subset')
            checked += 1
    need(checked == 60, 'K5 path choices')
    return {'triple_crossing_edge_choices': checked, 'inside_multiplicity': 3, 'crossing_multiplicity': 6}


def check_parallel_projection():
    simple = tuple(combinations(range(4), 2))
    extended = (simple[0],) + simple + ((2, 2),)
    weights = [1, 2] + [3] * 5 + [0]
    lift_count = 0
    for tree in independent_trees(4, extended):
        projected = tuple(sorted(0 if i < 2 else i - 1 for i in tree))
        projected_maximum = independent_maximum(4, simple, [3] * 6, 6, projected)
        expected = min([projected_maximum] + [Q(weights[i]) for i in tree])
        certify_endpoint(4, extended, weights, 6, tree, expected)
        lift_count += 1
    need(lift_count == 24, 'parallel-extension tree count')
    return {'all_lifted_trees': lift_count, 'parallel_classes_split': 1, 'loops': 1}


def check_endpoints_and_mutants():
    e4 = tuple(combinations(range(4), 2))
    star, path = (0, 1, 2), (0, 3, 5)
    w4 = [3] * 6
    need(certify_endpoint(4, e4, w4, 6, star, Q(3, 2)) == Q(3, 2), 'star')
    need(certify_endpoint(4, e4, w4, 6, path, Q(3)) == 3, 'path')
    certify_endpoint(1, ((0, 0),), [0], 7, (), Q(7))
    certify_endpoint(2, ((0, 0), (0, 1)), [0, 4], 4, (1,), Q(4))
    parallel_edges = ((0, 1), (0, 1), (1, 1))
    certify_endpoint(2, parallel_edges, [2, 3, 0], 5, (0,), Q(2))
    certify_endpoint(2, parallel_edges, [2, 3, 0], 5, (1,), Q(3))
    zero_w = [4, 4, 4, 0, 0, 0]
    certify_endpoint(4, e4, zero_w, 4, path, Q(0))
    need(not independent_member(1, ((0, 0),), [1], 1), 'nonzero loop accepted')
    need(not independent_member(3, ((0, 1),), [2], 1), 'disconnected positive input accepted')
    weighted = [11, 13, 11, 8, 8, 9]
    all_trees = independent_trees(4, e4)
    scores = {t: sum(weighted[i] for i in t) for t in all_trees}
    best = [t for t, s in scores.items() if s == max(scores.values())]
    need(best == [star] and scores[star] == 35, 'unique maximum-weight star')
    certify_endpoint(4, e4, weighted, 20, star, Q(15, 2))
    e5 = tuple(combinations(range(5), 2))
    w5 = [3, 6, 5, 5, 4, 5, 4, 2, 3, 3]
    five_values = [independent_maximum(5, e5, w5, 10, t) for t in independent_trees(5, e5)]
    mutant_checks = [
        ('omit_subset_bounds', lambda: certify_endpoint(4, e4, w4, 6, star, Q(3))),
        ('floor_fractional_endpoint', lambda: certify_endpoint(4, e4, w4, 6, star, Q(1))),
        ('treat_any_fractional_tree_as_target_counterexample', lambda: need(all(independent_maximum(4, e4, w4, 6, t).denominator != 1 for t in all_trees), 'integer tree exists')),
        ('require_globally_largest_endpoint_integral', lambda: need(max(five_values).denominator == 1, 'largest endpoint fractional')),
        ('require_maximum_weight_tree_integral', lambda: need(independent_maximum(4, e4, weighted, 20, star).denominator == 1, 'weighted star fractional')),
        ('exclude_zero_maximum', lambda: need(independent_maximum(4, e4, zero_w, 4, path) > 0, 'zero is a valid exact endpoint')),
        ('omit_rank_zero_mass_bound', lambda: certify_endpoint(1, ((0, 0),), [0], 7, (), Q(8))),
        ('collapse_parallel_coordinate_bounds', lambda: certify_endpoint(2, parallel_edges, [2, 3, 0], 5, (0,), Q(5))),
        ('accept_negative_remaining_mass', lambda: need(independent_member(2, ((0, 1),), [-1], -1), 'negative mass')),
    ]
    return [reject(label, fn) for label, fn in mutant_checks]


def run():
    return {'passed': True, 'uid': os.getuid(), 'euid': os.geteuid(),
            'optimization': sys.flags.optimize,
            'examples': check_recorded_examples(),
            'small_graph_structure': check_small_graph_construction(),
            'k5_structure': check_k5_structure(),
            'parallel_projection': check_parallel_projection(),
            'mutants_rejected': check_endpoints_and_mutants(),
            'all_graph_resolution': False, 'new_research_approaches': 0}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
