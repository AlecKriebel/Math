"""Independent exact finite controls; no simulation or stochastic-limit proof.

Uses only Python standard library, with rational deterministic weights.
"""
from fractions import Fraction
from itertools import combinations, product
from heapq import heappush, heappop
from math import inf
import json
import argparse
from pathlib import Path

def distances(n, edges, source, type_index, excluded=frozenset()):
    out = [inf] * n
    if source in excluded:
        return out
    out[source] = Fraction(0)
    heap = [(Fraction(0), source)]
    while heap:
        t, x = heappop(heap)
        if t != out[x]:
            continue
        for a, b, weights in edges:
            if x not in (a, b):
                continue
            y = b if x == a else a
            if y in excluded:
                continue
            candidate = t + weights[type_index]
            if candidate < out[y]:
                out[y] = candidate
                heappush(heap, (candidate, y))
    return out

def competing(n, edges, weak_seeds, fast_root):
    labels, arrivals, heap = ([None] * n, [inf] * n, [])

    def schedule(x, t, kind):
        for a, b, weights in edges:
            if x in (a, b):
                y = b if x == a else a
                heappush(heap, (t + weights[kind], -kind, x, y, kind))
    for x in weak_seeds:
        labels[x], arrivals[x] = (0, Fraction(0))
    labels[fast_root], arrivals[fast_root] = (1, Fraction(0))
    for x in weak_seeds:
        schedule(x, Fraction(0), 0)
    schedule(fast_root, Fraction(0), 1)
    while heap:
        t, _, x, y, kind = heappop(heap)
        if labels[y] is not None:
            continue
        labels[y], arrivals[y] = (kind, t)
        schedule(y, t, kind)
    return (labels, arrivals)

def run():
    pairs = list(combinations(range(4), 2))
    choices = [None] + [(Fraction(a), Fraction(b)) for a, b in product((1, 2), repeat=2)]
    graphs = protected_cases = comparisons = 0
    for states in product(choices, repeat=len(pairs)):
        edges = [(a, b, w) for (a, b), w in zip(pairs, states) if w is not None]
        labels, arrivals = competing(4, edges, [0], 1)
        fast = distances(4, edges, 1, 1)
        graphs += 1
        for T in map(Fraction, (1, 2, 3, 4)):
            ball = frozenset((x for x in range(4) if fast[x] <= T))
            protected = distances(4, edges, 0, 0, ball)
            for target in (2, 3):
                comparisons += 1
                if protected[target] <= T:
                    protected_cases += 1
                    if not (labels[target] == 1 and arrivals[target] <= T):
                        raise RuntimeError('Finite control failed: labels[target] == 1 and arrivals[target] <= T')
    edges = [(0, 2, (Fraction(1), Fraction(100))), (2, 3, (Fraction(1), Fraction(100))), (1, 2, (Fraction(100), Fraction(1, 10))), (1, 3, (Fraction(100), Fraction(3)))]
    weak = distances(4, edges, 0, 0)
    fast = distances(4, edges, 1, 1)
    labels, arrivals = competing(4, edges, [0], 1)
    if not weak[3] == 2 < fast[3] == 3:
        raise RuntimeError('Finite control failed: weak[3] == 2 < fast[3] == 3')
    if not (labels[3] == 1 and arrivals[3] == 3):
        raise RuntimeError('Finite control failed: labels[3] == 1 and arrivals[3] == 3')
    ball_at_two = frozenset((x for x in range(4) if fast[x] <= 2))
    if not 2 in ball_at_two:
        raise RuntimeError('Finite control failed: 2 in ball_at_two')
    if not distances(4, edges, 0, 0, ball_at_two)[3] == inf:
        raise RuntimeError('Finite control failed: distances(4, edges, 0, 0, ball_at_two)[3] == inf')
    multigraph = [(1, 1, (Fraction(1, 100), Fraction(1, 100))), (1, 2, (Fraction(5), Fraction(2))), (1, 2, (Fraction(5), Fraction(1)))]
    ml, mt = competing(3, multigraph, [0], 1)
    if not (ml[2] == 1 and mt[2] == 1):
        raise RuntimeError('Finite control failed: ml[2] == 1 and mt[2] == 1')
    repair_cases = 0
    for ds in product((2, 3, 10), repeat=4):
        for v in range(4):
            repaired = list(ds)
            repaired[v] += sum(ds) % 2
            for k in range(2, 13):
                old_count = sum((d >= k for d in ds))
                new_count = sum((d >= k for d in repaired))
                old_sum = sum((d for d in ds if d >= k))
                new_sum = sum((d for d in repaired if d >= k))
                if not 0 <= new_count - old_count <= 1:
                    raise RuntimeError('Finite control failed: 0 <= new_count - old_count <= 1')
                if not 0 <= new_sum - old_sum <= ds[v] + 1:
                    raise RuntimeError('Finite control failed: 0 <= new_sum - old_sum <= ds[v] + 1')
                if not sum((d * d for d in repaired)) - sum((d * d for d in ds)) == (2 * ds[v] + 1 if sum(ds) % 2 else 0):
                    raise RuntimeError('Finite control failed: sum((d * d for d in repaired)) - sum((d * d for d in ds)) == (2 * ds[v] + 1 if sum(ds) % 2 else 0)')
                repair_cases += 1
    tails = {str(j): str(Fraction(j + 1, 2 ** j)) for j in (1, 2, 3, 10)}
    missing_min_degree = {'law': 'P(D=1)=1/2; P(D=2m)=2^(-m-1), m>=1', 'mean_degree': str(Fraction(5, 2)), 'second_moment': str(Fraction(25, 2)), 'limiting_fraction_in_isolated_degree_one_pairs': str(Fraction(1, 10)), 'explanation': 'Proved in report by exact matching expectation and covariance; no simulation.'}
    return {'kind': 'exact finite controls and independently derived boundary constants', 'random_seed': None, 'stochastic_limit_claims_proved_by_simulation': False, 'protected_path_exhaustion': {'graphs': graphs, 'comparisons': comparisons, 'protected_target_cases': protected_cases, 'false_protected_predictions': 0, 'domain': 'Four vertices; each simple edge absent or both type weights in {1,2}; T in {1,2,3,4}; roots 0 and 1.'}, 'voronoi_negative_control': {'weak_unopposed_target_distance': str(weak[3]), 'fast_unopposed_target_distance': str(fast[3]), 'actual_target_label': 'fast', 'actual_target_arrival': str(arrivals[3]), 'wrong_voronoi_prediction_detected': True}, 'loop_parallel_control': 'passed', 'repair_cases': repair_cases, 'example_size_biased_tails': tails, 'outside_scope_minimum_degree_counterexample': missing_min_degree}
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Optional result file; default prints only for sealed read-only reruns.')
    args = parser.parse_args()
    result = run()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
