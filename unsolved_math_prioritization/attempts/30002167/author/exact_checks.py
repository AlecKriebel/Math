#!/usr/bin/env python3
"""Exact finite certificate, not a proof of a universal upper bound."""
import json
import math
import sys
from fractions import Fraction
from itertools import permutations, combinations
from pathlib import Path
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent
POINTS = [(95, 0), (96, 0), (-50, 83), (-51, 83), (-50, -83), (-51, -83)]


def matchings(vertices):
    if not vertices:
        yield ()
        return
    a = vertices[0]
    for i in range(1, len(vertices)):
        b = vertices[i]
        for rest in matchings(vertices[1:i] + vertices[i + 1:]):
            yield ((a, b),) + rest


def verify_certificate(certificate):
    checks = 0

    def require(condition, label):
        nonlocal checks
        checks += 1
        if not condition:
            raise ValueError(label)

    require(certificate['point_numerators'] == [list(p) for p in POINTS], 'point data')
    require(certificate['coordinate_denominator'] == 100, 'coordinate denominator')
    require(certificate['clusters'] == [[0, 1], [2, 3], [4, 5]], 'cluster partition')
    require(len(set(POINTS)) == 6, 'distinct points')
    require(len(POINTS) % 2 == 0, 'even cardinality')
    for x, y in POINTS:
        require(x*x + y*y < 10000, 'strict disk membership')
    d = lambda i, j: sum((a-b)**2 for a, b in zip(POINTS[i], POINTS[j]))
    pair_costs = {(i, j): d(i, j) for i, j in combinations(range(6), 2)}
    for (i, j), cost in pair_costs.items():
        require(cost > 0, 'positive pair distance')
        if i//2 != j//2:
            require(cost >= 27556, 'intercluster lower bound')
    require(min(v for (i, j), v in pair_costs.items() if i//2 != j//2) == 27556,
            'sharp intercluster minimum')
    require(certificate['intercluster_squared_minimum'] == str(Fraction(27556, 10000)),
            'claimed intercluster minimum')
    lower = Fraction(3 * 27556, 10000)
    require(lower > 8, 'analytic counterexample margin')
    require(certificate['analytic_tour_lower_bound'] == str(lower), 'claimed analytic bound')

    cycles = []
    for tail in permutations(range(1, 6)):
        if tail[0] < tail[-1]:
            cycle = (0,) + tail
            edges = list(zip(cycle, cycle[1:] + cycle[:1]))
            crossing = sum(i//2 != j//2 for i, j in edges)
            require(crossing >= 3, 'three cluster crossings')
            value = sum(d(i, j) for i, j in edges)
            require(value >= 3*27556, 'every tour exceeds analytic bound')
            cycles.append((value, cycle))
    require(len(cycles) == math.factorial(5)//2 == 60, 'exhaustive cycle count')
    require(certificate['undirected_tour_count'] == len(cycles), 'claimed cycle count')
    require(min(cycles)[0] == 83678, 'exact optimal tour numerator')
    require(certificate['minimum_squared_tour_cost'] == str(Fraction(min(cycles)[0], 10000)),
            'claimed tour minimum')
    witness = tuple(certificate['optimal_tour'])
    require((83678, witness) in cycles, 'attaining tour witness')
    require(min(value for value, _ in cycles) > 80000, 'all tours exceed 8')

    matches = list(matchings(tuple(range(6))))
    require(len(matches) == 15, 'exhaustive matching count')
    values = [sum(d(i, j) for i, j in matching) for matching in matches]
    require(min(values) == 3, 'exact matching minimum numerator')
    require(certificate['minimum_squared_matching_cost'] == str(Fraction(min(values), 10000)),
            'claimed matching minimum')
    require(Fraction(min(values), 10000) < 4, 'matching claim not refuted')
    return {'checks': checks, 'tours_exhausted': len(cycles), 'matchings_exhausted': len(matches),
            'tour_optimum': str(Fraction(min(cycles)[0], 10000)),
            'matching_optimum': str(Fraction(min(values), 10000))}


if __name__ == '__main__':
    print(json.dumps(verify_certificate(json.loads((ROOT / 'CERTIFICATE.json').read_text())),
                     sort_keys=True))
