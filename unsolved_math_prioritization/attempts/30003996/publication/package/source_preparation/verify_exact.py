#!/usr/bin/env python3
"""Portable exact diagnostics for the research note; Python 3.10+, stdlib only.

No finite run proves NP-hardness. All tests use every root and whole orientation.
This adapted checker uses the audited mechanism with B=2 and B=n+1.
"""
import argparse
import datetime
import hashlib
import itertools
import json
import os
from collections import Counter
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COUNTS = Counter()


def require(condition, message):
    """An explicit guard, deliberately independent of removable assert syntax."""
    if not condition:
        raise AssertionError(message)
    COUNTS[message] += 1


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(clauses):
    """Signed nonzero integer labels; remove duplicates/tautologies, then relabel.

    No unused declaration or largest numeric label contributes to n. An empty
    clause dominates even if other clauses are tautologies. At most 3 raw
    literals are accepted; every raw clause is validated before any empty-clause
    shortcut. Malformed-input rejection is independent of clause order.
    """
    raw_clauses = tuple(tuple(clause) for clause in clauses)
    for clause in raw_clauses:
        require(len(clause) <= 3, 'at_most_three_input_literals')
        require(all(type(lit) is int and lit != 0 for lit in clause),
                'literal_labels_are_nonzero_integers')
    if any(not clause for clause in raw_clauses):
        return {'kind': 'no', 'clauses': [], 'symbols': []}
    cleaned = []
    for clause in raw_clauses:
        distinct = set(clause)
        if any(-lit in distinct for lit in distinct):
            continue
        cleaned.append(tuple(sorted(distinct, key=lambda lit: (abs(lit), lit))))
    if not cleaned:
        return {'kind': 'yes', 'clauses': [], 'symbols': []}
    symbols = sorted({abs(lit) for clause in cleaned for lit in clause})
    dense = {symbol: i + 1 for i, symbol in enumerate(symbols)}
    clauses = [tuple(dense[abs(lit)] * (1 if lit > 0 else -1)
                     for lit in clause) for clause in cleaned]
    return {'kind': 'ordinary', 'clauses': clauses, 'symbols': symbols}


def construct(clauses, B=2, shift=0):
    normalized = normalize(clauses)
    require(type(B) is int and B >= 2, 'B_integer_at_least_two')
    require(type(shift) is int and shift >= 0, 'nonnegative_integer_shift')
    if normalized['kind'] != 'ordinary':
        val = int(normalized['kind'] == 'no')
        instance = {'N': 2, 'edges': [(0, 1)],
                    'costs': [[val + shift, val + shift] for _ in range(2)],
                    'K': (1 if val else 0) + 2 * shift,
                    'normalization': normalized, 'B': B, 'shift': shift}
        return instance
    cs = normalized['clauses']
    n, m = len(normalized['symbols']), len(cs)
    N = n + m + 2
    edges = {(0, 1)} | {(hub, i + 2) for hub in (0, 1) for i in range(n)}
    for j, clause in enumerate(cs):
        edges.update((abs(lit) + 1, n + 2 + j) for lit in clause)
    edges = sorted(edges)
    arcs = [arc for u, v in edges for arc in ((u, v), (v, u))]
    index = {arc: k for k, arc in enumerate(arcs)}
    # Every root explicitly supplies every directed edge cost, including zeros.
    costs = [[shift for _ in arcs] for _ in range(N)]
    for u, v in edges:
        value = 0 if (u, v) == (0, 1) else B if v >= n + 2 else 1
        costs[0][index[u, v]] += value
        costs[0][index[v, u]] += value
    for j, clause in enumerate(cs):
        for lit in clause:
            # The false hub: f=1 for positive literals; t=0 for negative ones.
            costs[n + 2 + j][index[abs(lit) + 1, int(lit > 0)]] += 1
    return {'N': N, 'edges': edges, 'costs': costs,
            'K': B * m + n + shift * N * (N - 1),
            'normalization': normalized, 'B': B, 'shift': shift}


def validate_table(instance):
    N, edges, costs = instance['N'], instance['edges'], instance['costs']
    require(N >= 1 and len(edges) == len(set(map(tuple, edges))), 'simple_graph')
    require(all(0 <= u < v < N for u, v in edges), 'valid_undirected_endpoints')
    require(len(costs) == N and all(len(row) == 2 * len(edges) for row in costs),
            'full_dense_root_arc_table')
    require(all(type(c) is int and c >= 0 for row in costs for c in row),
            'finite_nonnegative_integral_costs')


@lru_cache(None)
def spanning_trees(N, edges):
    """Enumerate all edge subsets of the right cardinality; reject cycles."""
    result = []
    for chosen in itertools.combinations(edges, N - 1):
        parent = list(range(N))

        def find(u):
            while parent[u] != u:
                u = parent[u]
            return u

        for u, v in chosen:
            a, b = find(u), find(v)
            if a == b:
                break
            parent[a] = b
        else:
            if len({find(u) for u in range(N)}) == 1:
                result.append(tuple(chosen))
    return tuple(result)


def adjacency(N, tree):
    adj = [[] for _ in range(N)]
    for u, v in tree:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def oriented_totals(instance, tree, inward=False, transpose=False):
    """BFS from each root, summing all selected directed arcs at that root."""
    N, edges, costs = instance['N'], instance['edges'], instance['costs']
    arc_index = {arc: index for edge_pos, (u, v) in enumerate(edges)
                 for arc, index in (((u, v), 2*edge_pos), ((v, u), 2*edge_pos+1))}
    adj = adjacency(N, tree)
    totals = []
    for root in range(N):
        seen, queue, total = {root}, [root], 0
        for u in queue:
            for v in adj[u]:
                if v in seen:
                    continue
                seen.add(v)
                queue.append(v)
                arc = (v, u) if inward else (u, v)
                if transpose:
                    arc = arc[::-1]
                total += costs[root][arc_index[arc]]
        require(len(seen) == N, 'whole_root_orientation_visits_every_vertex')
        totals.append(total)
    return totals


def cut_totals(instance, tree):
    """Independent evaluator: each root's side of each fundamental cut."""
    N, edges, costs = instance['N'], instance['edges'], instance['costs']
    edge_index = {tuple(edge): k for k, edge in enumerate(edges)}
    adj = adjacency(N, tree)
    totals = [0] * N
    for u, v in tree:
        reached, queue = {u}, [u]
        for a in queue:
            for b in adj[a]:
                if (a == u and b == v) or (a == v and b == u):
                    continue
                if b not in reached:
                    reached.add(b)
                    queue.append(b)
        require(v not in reached and 0 < len(reached) < N, 'proper_edge_cut')
        index = 2 * edge_index[u, v]
        for root in range(N):
            totals[root] += costs[root][index + int(root not in reached)]
    return totals


def assignments(n, clauses):
    return [a for a in itertools.product((False, True), repeat=n)
            if all(any(a[abs(lit)-1] == (lit > 0) for lit in clause)
                   for clause in clauses)]


def inspect_formula(raw_clauses, B, negative_cost=False):
    instance = construct(raw_clauses, B)
    validate_table(instance)
    if negative_cost:
        instance['costs'][0][0] += 1  # Corrupt t->f, which should cost zero.
    N, E, K = instance['N'], tuple(map(tuple, instance['edges'])), instance['K']
    normalized = instance['normalization']
    trees = spanning_trees(N, E)
    require(bool(trees), 'constructed_graph_connected')
    totals_by_tree = {}
    for tree in trees:
        totals = oriented_totals(instance, tree)
        require(totals == cut_totals(instance, tree), 'BFS_equals_edge_cut_full_cost')
        require(oriented_totals(instance, tree, inward=True, transpose=True) == totals,
                'inward_transpose_preserves_every_root_cost')
        totals_by_tree[tree] = totals
    if normalized['kind'] != 'ordinary':
        require((min(map(sum, totals_by_tree.values())) <= K)
                == (normalized['kind'] == 'yes'), 'normalized_fixed_yes_no')
        return instance, len(trees), None
    cs = normalized['clauses']
    n, m = len(normalized['symbols']), len(cs)
    feasible = set()
    shifted = construct(raw_clauses, B, 1)
    validate_table(shifted)
    require(set(c for row in shifted['costs'] for c in row) <= {1, 2, B+1},
            'positive_shift_cost_alphabet')
    for tree, totals in totals_by_tree.items():
        q = sum(v >= n+2 for u, v in tree)
        h = int((0, 1) in tree)
        p = len(tree) - q - h
        value = sum(totals)
        require(q >= m, 'every_clause_has_incident_tree_edge')
        require(totals[0] == p+B*q == K+(1-h)+(B-1)*(q-m),
                'unrestricted_structural_identity')
        require(value >= totals[0], 'nonnegative_root_domination')
        require(oriented_totals(shifted, tree) == [c+N-1 for c in totals],
                'uniform_shift_every_root_and_whole_objective')
        require(shifted['K'] == K+N*(N-1), 'uniform_shift_threshold')
        structured = h == 1 and q == m
        if not structured:
            require(value > K, 'every_unstructured_tree_excluded_at_threshold')
        else:
            assignment = tuple((0, i+2) in tree for i in range(n))
            require(all(int((0, i+2) in tree)+int((1, i+2) in tree) == 1
                        for i in range(n)), 'exactly_one_hub_per_variable')
            penalty = 0
            for j, clause in enumerate(cs):
                selected = [u-1 for u, v in tree if v == n+2+j]
                require(len(selected) == 1, 'exactly_one_selected_clause_literal')
                literal = next(lit for lit in clause if abs(lit) == selected[0])
                false = int(assignment[abs(literal)-1] != (literal > 0))
                require(totals[n+2+j] == false, 'individual_full_clause_root_literal_cost')
                penalty += false
            require(value == K+penalty, 'structured_only_total_identity')
        if value <= K:
            feasible.add(tree)
    sats = assignments(n, cs)
    require(bool(feasible) == bool(sats), 'SAT_iff_tree_at_threshold')
    for assignment in sats:
        witness = {(0, 1)} | {(0 if val else 1, i+2)
                             for i, val in enumerate(assignment)}
        for j, clause in enumerate(cs):
            lit = next(lit for lit in clause if assignment[abs(lit)-1] == (lit > 0))
            witness.add((abs(lit)+1, n+2+j))
        require(tuple(sorted(witness)) in feasible, 'every_satisfying_assignment_has_witness')
    return instance, len(trees), min(map(sum, totals_by_tree.values()))


def formula_suite():
    # All multisets of 1--3 nonempty n<=2 clauses, plus selected n=3 cases.
    for n in (1, 2):
        choices = []
        for size in range(1, n+1):
            for vs in itertools.combinations(range(1, n+1), size):
                choices += [tuple(v*s for v, s in zip(vs, signs))
                            for signs in itertools.product((-1, 1), repeat=size)]
        for m in (1, 2, 3):
            yield from itertools.combinations_with_replacement(choices, m)
    choices = [tuple((i+1)*s for i, s in enumerate(signs))
               for signs in itertools.product((-1, 1), repeat=3)]
    yield from itertools.combinations_with_replacement(choices, 2)
    yield ((1,), (-1,), (1, 2, 3))
    yield ((1, 2, 3), (-1, -2, -3), (1, -2, 3))
    yield ((1,), (-2,), (2, 3))


def boundaries():
    cases = [([], 'yes'), ([[]], 'no'), ([(9, -9)], 'yes'),
             ([(9, -9), ()], 'no'), ([(10000001, 10000001)], 'ordinary')]
    for cs, expected in cases:
        normalized = normalize(cs)
        require(normalized['kind'] == expected, 'normalization_boundary_kind')
        inspect_formula(cs, 2)
    normalized = normalize([(10000001, 10000001), (-41,), (41, 10000001)])
    require(normalized['symbols'] == [41, 10000001]
            and normalized['clauses'] == [(2,), (-1,), (1, 2)],
            'sparse_labels_repeated_literals_dense_relabeling')
    inspect_formula([(10000001, 10000001), (-41,), (41, 10000001)], 2)
    malformed = [([0], 'literal_labels_are_nonzero_integers'),
                 ([True], 'literal_labels_are_nonzero_integers'),
                 ([1, 2, 3, 4], 'at_most_three_input_literals')]
    for clause, intended_guard in malformed:
        # Standalone malformed clause, malformed suffix, and its order reversal.
        for invalid in ([clause], [[], clause], [clause, []]):
            for entry_point in (normalize, construct):
                try:
                    entry_point(invalid)
                except AssertionError as error:
                    require(str(error) == intended_guard, 'malformed_input_rejected_at_intended_guard')
                    COUNTS[entry_point.__name__+'_malformed_clause_rejected'] += 1
                else:
                    require(False, 'invalid_formula_must_not_be_accepted')
    # A single-use outer iterable and single-use clause iterables are supported.
    from_iterator = normalize(iter((iter((9, -9)), iter((10000001, 10000001)))))
    require(from_iterator == normalize([(9, -9), (10000001, 10000001)]),
            'single_use_iterables_materialized_once')
    for entry_point in (normalize, construct):
        try:
            entry_point(iter((iter(()), iter((0,)))))
        except AssertionError as error:
            require(str(error) == 'literal_labels_are_nonzero_integers',
                    'single_use_malformed_suffix_intended_guard')
        else:
            require(False, 'single_use_malformed_suffix_must_not_be_accepted')
    one = {'N': 1, 'edges': [], 'costs': [[]], 'K': 0}
    validate_table(one)
    require(spanning_trees(1, ()) == ((),), 'single_vertex_unique_empty_tree')
    require(oriented_totals(one, ()) == cut_totals(one, ()) == [0],
            'single_vertex_zero_cost')
    two = {'N': 2, 'edges': [(0, 1)], 'costs': [[3, 5], [7, 11]], 'K': 14}
    validate_table(two)
    require(oriented_totals(two, ((0, 1),)) == cut_totals(two, ((0, 1),)) == [3, 11],
            'two_vertex_independent_root_directions')
    edges = tuple(itertools.combinations(range(4), 2))
    k4 = {'N': 4, 'edges': edges, 'costs': [[1]*12 for _ in range(4)], 'K': 12}
    trees = spanning_trees(4, edges)
    require(len(trees) == 16, 'K4_all_tree_census')
    require(all(sum(oriented_totals(k4, tree)) == 12 for tree in trees),
            'symmetric_unit_cost_charges_whole_tree_at_all_roots')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='optional JSON receipt path')
    parser.add_argument('--export-fixture', type=Path, help='optional dense exact example JSON')
    parser.add_argument('--negative-control', choices=('guard', 'cost', 'proof',
                                                     'literal-suffix', 'boolean-suffix', 'size-suffix'))
    args = parser.parse_args()
    if args.negative_control == 'guard':
        require(False, 'intentional_false_guard')
    if args.negative_control in ('literal-suffix', 'boolean-suffix', 'size-suffix'):
        malformed = {'literal-suffix':[0], 'boolean-suffix':[True], 'size-suffix':[1,2,3,4]}
        entry_point = construct if args.negative_control == 'size-suffix' else normalize
        entry_point([[], malformed[args.negative_control]])
        require(False, 'malformed_suffix_must_not_complete')
    binding = json.loads((ROOT/'PROOF_BINDING.json').read_text())
    expected = binding['paper_sha256']
    if args.negative_control == 'proof':
        expected = '0'*64
    require(sha256(ROOT/binding['paper_relative_path']) == expected,
            'exact_research_note_binding')
    require(sha256(ROOT/binding['historical_proof_relative_path'])
            == binding['historical_proof_sha256'], 'exact_historical_audited_proof_binding')
    if args.negative_control == 'cost':
        inspect_formula([(1,)], 2, negative_cost=True)
        require(False, 'corrupt_cost_must_not_complete')
    boundaries()
    cases = tree_cases = 0
    for cs in formula_suite():
        normalized = normalize(cs)
        n = len(normalized['symbols'])
        for B in sorted({2, n+1}):
            _, count, _ = inspect_formula(cs, B)
            cases += 1
            tree_cases += count
    fixture, count, minimum = inspect_formula([(1, 2), (1, -2), (-1, 2), (-1, -2)], 2)
    require(count == 384 and minimum == 11 and fixture['K'] == 10,
            'four_clause_unsatisfiable_exact_all_tree_countercheck')
    if args.export_fixture:
        args.export_fixture.write_text(json.dumps({'arc_order':'for each listed edge (u,v): (u,v), (v,u)',
                                                  'instance':fixture, 'tree_count':count,
                                                  'exact_minimum':minimum}, indent=2)+'\n')
    report = {'schema':'pr108-portable-exact-verification/v1',
              'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'actual_operator_PID':os.getpid(), 'python_optimization_level':__import__('sys').flags.optimize,
              'all_pass':True, 'checks':dict(sorted(COUNTS.items())), 'total_checks':sum(COUNTS.values()),
              'formula_parameter_cases':cases, 'tree_formula_parameter_cases':tree_cases,
              'B_values':'2 and actual normalized n+1; duplicate parameter choices tested once',
              'distinct_graphs':spanning_trees.cache_info().currsize,
              'paper_sha256':expected, 'historical_proof_sha256':binding['historical_proof_sha256'],
              'verifier_sha256':sha256(Path(__file__)),
              'scope':'Finite exact all-tree diagnostics supplement the written all-size proof; no novelty inference.'}
    if args.output:
        args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
