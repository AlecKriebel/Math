#!/usr/bin/env python3
"""Independent reproduction of the prior general alcoved-polytope formula.

No import of the PR's proof, verifier, order-poset construction or natural labels.
Integer vertices of cumulative-coordinate type-A alcoves are constructed directly.
Adjacency is computed from shared facets, and coefficients count BFS incoming arcs,
as in Benedetti--Knauer--Valencia-Porras 2023, Theorem 2.6.
"""
import argparse
import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path


def check(ok, message):
    if not ok:
        raise RuntimeError(message)


def determinant(matrix):
    a = [list(row) for row in matrix]
    n = len(a)
    sign = 1
    previous = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot = next((i for i in range(k + 1, n) if a[i][k]), None)
            if pivot is None:
                return 0
            a[k], a[pivot] = a[pivot], a[k]
            sign *= -1
        current = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                value = a[i][j] * current - a[i][k] * a[k][j]
                check(value % previous == 0, 'Bareiss division not exact')
                a[i][j] = value // previous
            a[i][k] = 0
        previous = current
    return sign * a[-1][-1]


def x_from_y(y):
    return tuple(y[i] - (y[i - 1] if i else 0) for i in range(len(y)))


def constraints(x, signs, bound=1):
    return (all(0 <= q <= bound for q in x)
            and all((x[i] + x[i + 1] <= bound if s == '-'
                     else x[i] + x[i + 1] >= bound)
                    for i, s in enumerate(signs)))


def alcoves(n):
    """Classify all n! cube alcoves by exact barycenter's adjacent-sum signs.

    For an ordering w of fractional cumulative coordinates, put rank_i=j
    when w_j=i. The integer part k_i increments exactly on a descent of
    rank_0=0,rank_1,...,rank_n. Then x_i=y_i-y_(i-1) lies strictly in (0,1).
    The simplex has y-vertices k plus the suffix indicators in order w.
    """
    grouped = defaultdict(list)
    for word in itertools.permutations(range(n)):
        rank = [0] * n
        for j, i in enumerate(word, 1):
            rank[i] = j
        integer = []
        total = 0
        last = 0
        for r in rank:
            total += (r < last)
            integer.append(total)
            last = r
        bary_y_numerator = tuple((n + 1) * integer[i] + rank[i] for i in range(n))
        bary_x_numerator = x_from_y(bary_y_numerator)
        check(all(0 < v < n + 1 for v in bary_x_numerator), 'cube alcove escaped')
        signs = ''.join('-' if bary_x_numerator[i] + bary_x_numerator[i + 1] < n + 1
                        else '+' for i in range(n - 1))
        check(all(bary_x_numerator[i] + bary_x_numerator[i + 1] != n + 1
                  for i in range(n - 1)), 'barycenter on sign boundary')
        vertices = [tuple(integer)]
        for cut in range(n):
            suffix = set(word[cut:])
            vertices.append(tuple(integer[i] + (i in suffix) for i in range(n)))
        vertices = tuple(sorted(vertices))
        check(len(set(vertices)) == n + 1, 'degenerate simplex')
        origin = vertices[0]
        matrix = [[vertices[j + 1][i] - origin[i] for j in range(n)] for i in range(n)]
        check(abs(determinant(matrix)) == 1, 'nonunimodular alcove')
        check(all(constraints(x_from_y(v), signs) for v in vertices), 'closed alcove escaped signed target')
        grouped[signs].append({'word':tuple(i + 1 for i in word), 'vertices':vertices})
    check(len(grouped) == 2 ** (n - 1), 'some sign word has no full-dimensional alcove')
    return grouped


def adjacency(cells, n):
    facets = defaultdict(list)
    for i, cell in enumerate(cells):
        for omitted in range(n + 1):
            facets[cell['vertices'][:omitted] + cell['vertices'][omitted + 1:]].append(i)
    graph = [set() for _ in cells]
    for owners in facets.values():
        check(len(owners) <= 2, 'facet with more than two cells')
        if len(owners) == 2:
            i, j = owners
            graph[i].add(j)
            graph[j].add(i)
    return graph


def incoming_polynomial(graph, root, n):
    distance = {root:0}
    todo = deque([root])
    while todo:
        i = todo.popleft()
        for j in graph[i]:
            if j not in distance:
                distance[j] = distance[i] + 1
                todo.append(j)
    check(len(distance) == len(graph), 'disconnected alcove graph')
    coefficients = [0] * (n + 1)
    for i, neighbors in enumerate(graph):
        check(all(abs(distance[i] - distance[j]) == 1 for j in neighbors), 'nonbipartite BFS edge')
        incoming = sum(distance[j] < distance[i] for j in neighbors)
        check(incoming <= n, 'too many incoming facets')
        coefficients[incoming] += 1
    return coefficients


def lattice_count(signs, m):
    # Direct original-coordinate transfer: includes all weak boundary equalities.
    previous = [1] * (m + 1)
    for sign in signs:
        previous = [sum(previous[a] for a in range(m + 1)
                        if (a + b <= m if sign == '-' else a + b >= m))
                    for b in range(m + 1)]
    return sum(previous)


def ehrhart_coefficients(signs):
    n = len(signs) + 1
    values = [lattice_count(signs, m) for m in range(n + 4)]
    coefficients = [sum((-1) ** j * math.comb(n + 1, j) * values[k - j]
                        for j in range(k + 1)) for k in range(n + 2)]
    check(coefficients[n + 1] == 0, 'Ehrhart degree boundary failed')
    return coefficients[:n + 1], values


def run(max_n):
    rows = []
    total_cells = root_checks = evaluations = 0
    raw_descent_mismatches = []
    for n in range(1, max_n + 1):
        for signs, cells in sorted(alcoves(n).items()):
            graph = adjacency(cells, n)
            hstar, values = ehrhart_coefficients(signs)
            roots = list(range(len(cells))) if n <= 5 else sorted({0,len(cells)//2,len(cells)-1})
            for root in roots:
                derived = incoming_polynomial(graph, root, n)
                check(derived == hstar, f'prior graph formula disagrees for n={n}, signs={signs}, root={root}')
                root_checks += 1
            for m, value in enumerate(values):
                reconstructed = sum(c * math.comb(m + n - d, n) for d, c in enumerate(hstar) if m >= d)
                check(reconstructed == value, 'binomial Ehrhart reconstruction failed')
                evaluations += 1
            raw = Counter(sum(a > b for a, b in zip(c['word'],c['word'][1:])) for c in cells)
            raw_vector = [raw[k] for k in range(n + 1)]
            if raw_vector != hstar and len(raw_descent_mismatches) < 6:
                raw_descent_mismatches.append({'n':n,'signs':signs,'hstar':hstar,'raw_fraction_order_descents':raw_vector})
            rows.append({'n':n,'signs':signs,'cells':len(cells),'edges':sum(map(len,graph))//2,
                         'roots_checked':len(roots),'hstar':hstar,'lattice_values_m_0_to_n_plus_3':values})
            total_cells += len(cells)
    check(bool(raw_descent_mismatches), 'negative raw-descent control did not reject')
    period_two_count = sum(a + b <= 1 and b + c <= 2 and c + d <= 1
                           for a,b,c,d in itertools.product(range(2),repeat=4))
    check(lattice_count('---',1) == 8 and period_two_count == 9, '2026 period-two domain control')
    # Centering x->2x-1 gives a different lattice: Q triangle has 3 grid points,
    # whereas the centered signed-order triangle has 6. No type-B transfer inferred.
    centered_triangle_points = sum(a+b <= 0 for a in range(-1,2) for b in range(-1,2))
    check(lattice_count('-',1) == 3 and centered_triangle_points == 6, 'type-B scaling control')
    return {'format':'pr407-independent-prior-alcoved-coverage-v1',
            'result':'PASS_PRIOR_ALCOVED_GRAPH_COVERAGE_FINITE_CONTROLS',
            'max_n':max_n,'patterns':len(rows),'alcoves':total_cells,'root_checks':root_checks,
            'ehrhart_evaluations':evaluations,'raw_descent_negative_controls':raw_descent_mismatches,
            'type_B_scaling_negative_control':{'Q_triangle_L1':3,'centered_triangle_L1':6},
            '2026_period_two_bound_negative_control':{'all_upper_Q4_L1':lattice_count('---',1),'period_two_bound_1_2_1_L1':period_two_count},
            'scope':'Finite reproduction supports the published general theorem application; it is not an all-dimension proof or evidence of explicit historical attribution to the OWR question.',
            'cases':rows}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-n',type=int,default=7)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    check(1 <= args.max_n <= 8, 'max-n outside intended finite audit bounds')
    started = datetime.now(timezone.utc).isoformat()
    result = run(args.max_n)
    result['started_utc'] = started
    result['completed_utc'] = datetime.now(timezone.utc).isoformat()
    result['script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('cases','raw_descent_negative_controls')},sort_keys=True))
