"""Exact union-bound arithmetic for rank-three, tau-four critical candidates."""
from fractions import Fraction
from math import comb
import json


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def table():
    rows = []
    for maximum in range(4, 8):
        for edges in range(max(7, maximum + 3), 20):
            counts = {degree: sum(choose(degree, j) * choose(edges-degree, 6-j)
                                  for j in range(4, 7))
                      for degree in range(4, maximum + 1)}
            ratio = max(Fraction(count, degree) for degree, count in counts.items())
            upper = (3 * edges * ratio).__floor__()
            needed = comb(edges, 6)
            rows.append(dict(edges=edges, maximum_degree=maximum,
                             per_vertex_counts=counts,
                             maximum_count_per_incidence=[ratio.numerator, ratio.denominator],
                             coverage_upper_bound=upper, six_subsets=needed,
                             survives_counting=upper >= needed))
    return dict(rows=rows, surviving_pairs=[[r["edges"], r["maximum_degree"]]
                                          for r in rows if r["survives_counting"]])


if __name__ == "__main__":
    print(json.dumps(table(), indent=2))
