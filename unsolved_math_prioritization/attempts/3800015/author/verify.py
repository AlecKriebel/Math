#!/usr/bin/env python3
"""Exact finite checks accompanying the line-arrangement shortest-path audit.

Standard library only. Fractions are exact; irrational lengths are rejected.
These checks do not establish a universal running-time bound.
"""
import errno
import heapq
import itertools
import json
import math
import os
from pathlib import Path
import random
import sys
from fractions import Fraction as F

MAX_LINES = 18
MAX_VERTICES = 100


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_line(line):
    if len(line) != 3 or any(type(x) is not int for x in line):
        raise ValueError('line coefficients must be three integers')
    a, b, c = line
    if a == b == 0:
        raise ValueError('zero normal')
    g = math.gcd(math.gcd(abs(a), abs(b)), abs(c))
    a, b, c = a // g, b // g, c // g
    if a < 0 or (a == 0 and b < 0):
        a, b, c = -a, -b, -c
    return a, b, c


def intersection(l, m):
    a, b, c = l
    d, e, f = m
    det = a * e - b * d
    if det == 0:
        return None
    return F(c * e - b * f, det), F(a * f - c * d, det)


def on(line, point):
    return line[0] * point[0] + line[1] * point[1] == line[2]


def distance(p, q):
    square = sum((a - b) ** 2 for a, b in zip(p, q))
    rn, rd = math.isqrt(square.numerator), math.isqrt(square.denominator)
    if rn * rn != square.numerator or rd * rd != square.denominator:
        raise ValueError('fixture requires an irrational Euclidean length')
    return F(rn, rd)


class Arrangement:
    def __init__(self, lines):
        if len(lines) > MAX_LINES:
            raise ValueError('line-count guard exceeded')
        self.lines = sorted(set(canonical_line(l) for l in lines))
        self.points = sorted(set(p for l, m in itertools.combinations(self.lines, 2)
                                 if (p := intersection(l, m)) is not None))
        if len(self.points) > MAX_VERTICES:
            raise ValueError('vertex-count guard exceeded')
        self.ids = {p: i for i, p in enumerate(self.points)}
        self.adj = [dict() for p in self.points]
        self.incidence = [{j for j, l in enumerate(self.lines) if on(l, p)}
                          for p in self.points]
        for l in self.lines:
            indices = [i for i, p in enumerate(self.points) if on(l, p)]
            # Lexicographic order is order along a straight nonvertical line;
            # for a vertical line the second coordinate provides the order.
            for i, j in zip(indices, indices[1:]):
                w = distance(self.points[i], self.points[j])
                require(w > 0, 'nonpositive edge')
                self.adj[i][j] = self.adj[j][i] = w

    def index(self, x, y):
        return self.ids[(F(x), F(y))]

    def dijkstra(self, source, hop=False):
        ds, previous = {source: F(0)}, {}
        heap = [(F(0), source)]
        while heap:
            d, i = heapq.heappop(heap)
            if d != ds[i]:
                continue
            for j, w in self.adj[i].items():
                candidate = d + (1 if hop else w)
                if j not in ds or candidate < ds[j]:
                    ds[j], previous[j] = candidate, i
                    heapq.heappush(heap, (candidate, j))
        return ds, previous

    def path(self, previous, source, target):
        result = [target]
        while result[-1] != source:
            require(len(result) <= len(self.points), 'predecessor cycle')
            result.append(previous[result[-1]])
        return result[::-1]

    def floyd(self):
        count = len(self.points)
        require(count <= 36, 'all-pairs finite-check guard exceeded')
        ds = [[None] * count for _ in range(count)]
        for i in range(count):
            ds[i][i] = F(0)
            for j, w in self.adj[i].items():
                ds[i][j] = w
        for k in range(count):
            for i in range(count):
                if ds[i][k] is None:
                    continue
                for j in range(count):
                    if ds[k][j] is None:
                        continue
                    candidate = ds[i][k] + ds[k][j]
                    if ds[i][j] is None or candidate < ds[i][j]:
                        ds[i][j] = candidate
        return ds

    def one_bend(self, source, target):
        s, t = self.points[source], self.points[target]
        values = []
        for l in self.lines:
            if not on(l, s):
                continue
            if on(l, t):
                values.append(distance(s, t))
            for m in self.lines:
                if on(m, t) and (p := intersection(l, m)) is not None:
                    values.append(distance(s, p) + distance(p, t))
        return min(values)


def check_path(a, source, target, d, previous):
    path = a.path(previous, source, target)
    require(sum((a.adj[i][j] for i, j in zip(path, path[1:])), F(0)) == d,
            'reported path length disagrees')
    require(len(set(path)) == len(path), 'path repeats a vertex')
    if source != target:
        bound = len(a.lines) - len(a.incidence[source]) - len(a.incidence[target]) + 2
        require(len(path) - 1 <= bound, 'incidence-sensitive edge bound failed')
    for line in a.lines:
        hits = [i for i, v in enumerate(path) if on(line, a.points[v])]
        require(not hits or hits == list(range(hits[0], hits[-1] + 1)),
                'a line has disconnected intersection with a geodesic')
    if a.incidence[source] & a.incidence[target]:
        require(d == distance(a.points[source], a.points[target]),
                'same-line Euclidean equality failed')


def all_pairs(a, directional=False):
    oracle = a.floyd()
    total = 0
    for s in range(len(a.points)):
        ds, previous = a.dijkstra(s)
        require(len(ds) == len(a.points), 'unexpected disconnected arrangement')
        for t, d in ds.items():
            require(d == oracle[s][t], 'Dijkstra/Floyd mismatch')
            check_path(a, s, t, d, previous)
            if directional:
                dx = a.points[t][0] - a.points[s][0]
                dy = a.points[t][1] - a.points[s][1]
                expected = abs(dx + F(4, 3) * dy) + F(5, 3) * abs(dy)
                require(d == expected, 'two-direction exact formula failed')
            total += 1
    return total


def expect_value_error(function, label):
    try:
        function()
    except ValueError:
        return
    raise RuntimeError('missing input guard: ' + label)


def readonly_checks():
    require(os.getuid() == 1000 and os.geteuid() == 1000,
            'read-only validation requires genuine UID/EUID 1000')
    file = Path(__file__).resolve()
    flags = [('existing_file', file, os.O_WRONLY | os.O_APPEND),
             ('new_file', file.parent / '.validation-write-probe',
              os.O_WRONLY | os.O_CREAT | os.O_EXCL)]
    result = {}
    for label, target, mode in flags:
        try:
            fd = os.open(target, mode, 0o600)
        except OSError as error:
            require(error.errno in (errno.EACCES, errno.EROFS),
                    'probe failed for an unrelated reason')
            result[label] = {'failed_as_required': True, 'errno': error.errno}
        else:
            os.close(fd)
            if label == 'new_file':
                target.unlink()
            raise RuntimeError('read-only probe unexpectedly opened ' + label)
    return result


def main():
    require(sys.argv[1:] in ([], ['--require-readonly']), 'unsupported arguments')
    probes = readonly_checks() if sys.argv[1:] else None
    expect_value_error(lambda: Arrangement([(0, 0, 1)]), 'zero normal')
    expect_value_error(lambda: Arrangement([(0.0, 1, 0)]), 'noninteger input')
    expect_value_error(lambda: Arrangement([(0, 1, i) for i in range(19)]), 'size')
    expect_value_error(lambda: distance((F(0), F(0)), (F(1), F(1))), 'irrational')
    # The explicit require guard must remain active with -O and -OO.
    try:
        require(False, 'negative-control')
    except RuntimeError as error:
        require(str(error) == 'negative-control', 'wrong guard failure')
    else:
        raise RuntimeError('require was disabled')
    require(Arrangement([(0, 1, 0), (0, -2, 0), (1, 0, 0)]).lines ==
            [(0, 1, 0), (1, 0, 0)], 'coincident-line normalization failed')

    fixture_one_bend = Arrangement([(4, 3, 0), (5, -12, 15), (5, -12, -63),
                                   (4, 3, 75), (0, 1, 0)])
    a = fixture_one_bend
    s, t = a.index(-3, 4), a.index(15, 5)
    ds, previous = a.dijkstra(s)
    require(ds[t] == 21 and len(a.path(previous, s, t)) == 4, 'three-edge optimum')
    require(a.one_bend(s, t) == F(65, 3), 'one-bend counterexample')
    require(a.dijkstra(s, hop=True)[0][t] == 2, 'hop metric distinction')
    hop_corner = a.index(F(79, 7), F(209, 21))
    require(hop_corner in a.adj[s] and t in a.adj[hop_corner], 'corrected hop witness edges')
    require(a.adj[s][hop_corner] + a.adj[hop_corner][t] == F(65, 3),
            'corrected hop witness length')
    lower_corner = a.index(F(5, 7), F(-20, 21))
    require(lower_corner not in a.adj[s], 'one bend was confused with one arrangement edge')
    require(F(91, 5) < ds[t], 'directional relaxation gap')

    profile = Arrangement([(0, 1, 0), (3, 4, 12), (3, -4, -12), (5, -12, 0)])
    ds, _ = profile.dijkstra(profile.index(0, 3))
    require([ds[profile.index(x, 0)] for x in (-4, 0, 4)] == [5, 6, 5],
            'nonconvex distance-profile counterexample')
    pairs = all_pairs(a) + all_pairs(profile)
    # Includes parallel lines, multiple concurrence, and same-vertex queries.
    fixed = [Arrangement([(0, 1, 0), (1, 0, 0), (3, 4, 0), (5, 12, 0)]),
             Arrangement([(0, 1, 0), (0, 1, 3), (1, 0, 0), (1, 0, 4), (3, 4, 12)])]
    for arrangement in fixed:
        pairs += all_pairs(arrangement)
    rng = random.Random(3800015)
    normals = [(0, 1), (1, 0), (3, 4), (3, -4), (5, 12), (5, -12), (4, 3), (4, -3)]
    random_counts = []
    for repetition in range(18):
        count = 5 + repetition % 4
        arrangement = Arrangement([(*normal, rng.randrange(-7, 8))
                                   for normal in rng.sample(normals, count)])
        pairs += all_pairs(arrangement)
        random_counts.append({'lines': len(arrangement.lines), 'vertices': len(arrangement.points)})
    for size in range(2, 5):
        arrangement = Arrangement([(0, 1, j) for j in range(size)] +
                                  [(3, 4, i) for i in range(size)])
        pairs += all_pairs(arrangement, directional=True)

    grids = []
    for m in range(2, 9):
        arrangement = Arrangement([(1, 0, i) for i in range(m + 1)] +
                                  [(0, 1, j) for j in range(m + 1)])
        s, t = arrangement.index(0, 0), arrangement.index(m, m)
        ds, previous = arrangement.dijkstra(s)
        require(ds[t] == 2 * m, 'grid optimum')
        ellipse_count = strict_f_count = 0
        for i, (x, y) in enumerate(arrangement.points):
            check_path(arrangement, s, i, ds[i], previous)
            require(ds[i] == x + y, 'grid distance formula')
            u, v = x*x + y*y, (m-x)**2 + (m-y)**2
            remainder = 4*m*m - u - v
            inside = remainder >= 0 and 4*u*v <= remainder*remainder
            ellipse_count += int(inside)
            rest = 2*m - x - y
            strict_f_count += int(rest > 0 and v < rest*rest)
        require(ellipse_count == (m+1)**2, 'ellipse failed to retain complete grid')
        require(strict_f_count == m*m, 'Euclidean A* strict-f count')
        grids.append({'m': m, 'lines': 2*(m+1), 'vertices': (m+1)**2,
                      'ellipse_retained': ellipse_count, 'f_below_optimum': strict_f_count})

    sorting_cases = 0
    for permutation in itertools.permutations(range(1, 6)):
        arrangement = Arrangement([(0, 1, 0), (1, 0, 0), (1, 0, 6)] +
                                  [(1, 0, i) for i in permutation])
        s, t = arrangement.index(0, 0), arrangement.index(6, 0)
        ds, previous = arrangement.dijkstra(s)
        path = arrangement.path(previous, s, t)
        require([arrangement.points[i][0] for i in path] == list(map(F, range(7))),
                'sorting reduction output not ordered')
        require(len(path)-1 == len(arrangement.lines)-2, 'sharp edge bound')
        sorting_cases += 1

    print(json.dumps({'status': 'passed', 'uid': os.getuid(), 'euid': os.geteuid(),
                      'optimization': sys.flags.optimize, 'readonly_probes': probes,
                      'all_pairs_queries': pairs, 'random_fixtures': random_counts,
                      'grid_cases': grids, 'sorting_cases': sorting_cases,
                      'one_bend': {'exact_optimum': '21', 'best_one_bend': '65/3',
                                   'relaxed_direction_bound': '91/5', 'min_hops': 2},
                      'profile_distances': [5, 6, 5],
                      'scope': 'Finite exact checks only; no universal complexity claim.'},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
