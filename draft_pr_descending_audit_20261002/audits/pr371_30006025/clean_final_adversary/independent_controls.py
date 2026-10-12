#!/usr/bin/env python3
"""Supplementary independently authored rational controls, never proof oracles."""
from fractions import Fraction as F
from itertools import product
from math import comb
import json

counts = {}


def check(value, name):
    assert value, name
    counts[name] = counts.get(name, 0) + 1


def plus(*polynomials):
    result = {}
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            result[exponent] = result.get(exponent, F(0)) + coefficient
    return {e: c for e, c in result.items() if c}


def times(a, b):
    result = {}
    for ea, ca in a.items():
        for eb, cb in b.items():
            result[ea+eb] = result.get(ea+eb, F(0)) + ca*cb
    return {e: c for e, c in result.items() if c}


def matrix_product(a, b):
    return [[plus(*(times(a[i][k], b[k][j]) for k in (0, 1)))
             for j in (0, 1)] for i in (0, 1)]


for size in range(2, 10):
    for offset in range(9):
        weights = [1 + (3*j+offset) % 7 for j in range(size)]
        parameters = [F(((2*j+offset) % 9) - 4, 7) for j in range(size)]
        rotations = []
        result = [[{0: F(1)}, {}], [{}, {0: F(1)}]]
        leading = F(1)
        for weight, parameter in zip(weights, parameters):
            cosine = (1-parameter**2)/(1+parameter**2)
            sine = 2*parameter/(1+parameter**2)
            check(cosine > 0 and cosine**2+sine**2 == 1, "rotation_domain")
            rotation = [[cosine, sine], [-sine, cosine]]
            rotations.append(rotation)
            result = matrix_product(result, [[{weight: cosine}, {weight: sine}],
                                             [{-weight: -sine}, {-weight: cosine}]])
            leading *= cosine
        trace = plus(result[0][0], result[1][1])
        index_expansion = {}
        for indices in product((0, 1), repeat=size):
            exponent = sum((1-2*i)*w for i, w in zip(indices, weights))
            coefficient = F(1)
            for j in range(size):
                coefficient *= rotations[j][indices[j]][indices[(j+1) % size]]
            index_expansion[exponent] = index_expansion.get(exponent, F(0)) + coefficient
        index_expansion = {e: c for e, c in index_expansion.items() if c}
        check(trace == index_expansion, "weighted_grouped_trace_expansion")
        check(trace[sum(weights)] == leading > 0, "unique_greatest_exponent")
        determinant = plus(times(result[0][0], result[1][1]),
                           {e: -c for e, c in times(result[0][1], result[1][0]).items()})
        check(determinant == {0: F(1)}, "framed_determinant")

# Domain negatives: excluded full turns have zero half-angle cosine; zero
# lengths destroy strict uniqueness of the largest binary-index exponent.
check((1-F(1)**2)/(1+F(1)**2) == 0, "excluded_full_turn_breaks_leading_coefficient")
for weights in ([0, 1], [1, 0, 2], [0, 0, 0]):
    exponents = [sum((1-2*i)*w for i, w in zip(indices, weights))
                 for indices in product((0, 1), repeat=len(weights))]
    check(exponents.count(max(exponents)) > 1, "excluded_zero_length_breaks_uniqueness")


def harmonic(n):
    return sum((F(1, j) for j in range(1, n+1)), F(0))


for edges in range(1, 31):
    ranked = []
    for rank in range(1, edges+1):
        # Integrate exact inclusion-exclusion of translated simplex volumes.
        integral = sum((F((-1)**(r-rank)*comb(r-1, rank-1)*comb(edges, r), r*edges)
                        for r in range(rank, edges+1)), F(0))
        check(integral == (harmonic(edges)-harmonic(rank-1))/edges,
              "simplex_volume_rank_means")
        ranked.append(integral)
    for k in range(edges+1):
        expected = F(k, edges)*(1+harmonic(edges)-harmonic(k))
        check(sum(ranked[:k], F(0)) == expected, "all_top_k_expectations")
    check(sum(ranked, F(0)) == 1, "all_edges_unit_mass")


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(1, total-length+2):
            for rest in compositions(total-first, length-1):
                yield (first,)+rest


for edges in range(1, 7):
    for raw in compositions(edges+3, edges):
        proportions = [F(v, edges+3) for v in raw]
        for mask in range(1 << edges):
            selected = [j for j in range(edges) if (mask >> j) & 1]
            top = sum(sorted(proportions, reverse=True)[:len(selected)], F(0))
            for cap in (F(1), F(5, 4), F(5)):
                output = [x*(cap if j % 2 else F(1, 2)) if j in selected else x
                          for j, x in enumerate(proportions)]
                net = sum(output)-1
                selected_mass = sum((proportions[j] for j in selected), F(0))
                check(net <= (cap-1)*selected_mass <= (cap-1)*top,
                      "adaptive_capacity_including_decreases")
                check(max(y/x for y, x in zip(output, proportions)) >= sum(output),
                      "weighted_maximum_stretch")
                if net > 0:
                    check(top > 0 and max(y/x for y, x in zip(output, proportions)) >= 1+net/top,
                          "uncapped_pointwise_stretch")

# Independent all-genus certificates, plus finite examples outside the theorem.
pi_lower, pi_upper = F(157, 50), F(22, 7)
check(11*pi_lower**2 > 108, "genus_twelve_strict")
check(10*pi_upper**2 < 99, "genus_eleven_permitted_by_necessary_bound")
check(pi_lower**2 > 9, "positive_all_genus_monotonic_coefficient")
check((pi_lower/3)**2*F(99, 100) > F(26, 25)**2, "uniform_four_percent_deficit")
for genus in range(2, 202):
    sides, edges, vertices = 12*genus-6, 6*genus-3, 4*genus-2
    area_pi = sides-2-F(2*sides, 3)
    orbifold_area_pi = F(1, 3)-F(2, sides)
    check(vertices-edges+1 == 2-2*genus and 3*vertices == 2*edges,
          "cubic_one_face_topology")
    check(area_pi == 4*(genus-1) and area_pi/orbifold_area_pi == sides,
          "orientation_preserving_orbifold_index")
check(1+F(1, 8)/(1-F(1, 48)) < F(4, 3), "uniform_systole_analytic_certificate")
check(F(3, 16)/(1+F(3, 16)) == F(3, 19), "poisson_count_gap_certificate")

print(json.dumps({"status": "PASS", "assertions": sum(counts.values()), "by_family": counts,
                  "scope": "Independent finite exact controls only. The sealed mathematical verdict supplies universal reasoning and primary-source dependency validation."}, indent=2))
