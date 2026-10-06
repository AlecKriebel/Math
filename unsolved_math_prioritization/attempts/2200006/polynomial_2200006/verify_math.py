#!/usr/bin/env python3
"""Exact controls for the written proofs; no numerical root finder or network.

The all-parameter theorems are proved in PROOFS.md. These independent, authored
integer/rational calculations only corroborate the displayed constructions.
"""
import itertools
import json
from fractions import Fraction as Q
from math import comb, prod


class Checks:
    def __init__(self):
        self.count = 0

    def require(self, condition, message):
        self.count += 1
        if not condition:
            raise ValueError(message)


def positive_integer(n):
    if type(n) is not int or n < 1:
        raise ValueError("Expected a positive Python integer")
    return n


def family_count(k, l):
    positive_integer(k)
    positive_integer(l)
    if k % 2 or l < 3:
        raise ValueError("Even k >= 2 and l >= 3 required")
    numerator = (l - 1) * (k - 1) * k ** (l - 1)
    if numerator % 4:
        raise ValueError("Nonintegral purported count")
    return numerator // 4


def selector(d, m, i, t):
    if i == 1:
        return -(t - d) * (t - m * d) * prod(
            (t - r) ** 2 for r in range(1, d))
    a, b = (i - 1) * d, i * d
    return (t - a) * (t - b) * prod(
        (t - r) ** 2 for r in range(a + 1, b))


def well(d, y):
    return prod((y - r) ** 2 for r in range(1, d + 1))


def block_count(s):
    return (s - 1) * 2 ** (s - 3)


def best_blocks(nmax):
    values, witnesses = [1], [[]]
    for n in range(1, nmax + 1):
        options = [(2 * values[n - 1], [1] + witnesses[n - 1])]
        options += [(block_count(s) * values[n - s], [s] + witnesses[n - s])
                    for s in range(3, n + 1)]
        value, witness = max(options, key=lambda item: item[0])
        values.append(value)
        witnesses.append(witness)
    return values, witnesses


def partition_values(total, minimum=1):
    """Separate exhaustive enumeration of unordered admissible partitions."""
    if total == 0:
        yield 1
        return
    for s in range(minimum, total + 1):
        if s == 2:
            continue
        count = 2 if s == 1 else block_count(s)
        for rest in partition_values(total - s, s):
            yield count * rest


def run():
    c = Checks()
    slices, point_codes = [], set()
    # Exact radicands specify real algebraic points without floating square roots.
    for t in range(9):
        a = [t * (8 - t)] + [(t - i + 1) * (t - i) for i in range(1, 9)]
        c.require(all(x >= 0 for x in a), "Infeasible integer slice")
        c.require(sum(x == 0 for x in a) == 2, "Wrong zero-radicand count")
        choices = [(0,) if x == 0 else (-1, 1) for x in a]
        local = list(itertools.product(*choices))
        c.require(len(local) == 128, "Wrong number of sign choices")
        for signs in local:
            code = (t, tuple(zip(a, signs)))
            c.require(code not in point_codes, "Duplicate algebraic point")
            point_codes.add(code)
            c.require(a[0] + t * (t - 8) == 0, "q0 is nonzero")
            for i in range(1, 9):
                c.require(a[i] - (t - i + 1) * (t - i) == 0, "qi is nonzero")
        for z in [Q(1), Q(-1), Q(2), Q(1, 3)]:
            tt = z * t
            c.require(z * z * a[0] + tt * (tt - 8 * z) == 0,
                      "Homogenized q0 is nonzero")
            for i in range(1, 9):
                c.require(z * z * a[i] - (tt - (i - 1) * z) * (tt - i * z) == 0,
                          "Homogenized qi is nonzero")
        slices.append({"t": t, "radicands": a, "count": len(local)})
    c.require(len(point_codes) == 1152, "Base total is wrong")
    c.require(1152 > 2 ** 10, "No strict violation")
    # All roots of the sign polynomials are integer, so each intervening interval
    # has constant sign. The written proof handles the continuum.
    base_forbidden = [Q(-1), Q(9)] + [Q(2 * j + 1, 2) for j in range(8)]
    for t in base_forbidden:
        a = [t * (8 - t)] + [(t - i + 1) * (t - i) for i in range(1, 9)]
        c.require(any(x < 0 for x in a), "Forbidden interval admitted")

    families = []
    for d in range(1, 7):
        for m in range(2, 11):
            k, l, n = 2 * d, m + 1, m * d
            rows = [[selector(d, m, i, j) for i in range(1, m + 1)]
                    for j in range(1, n + 1)]
            eta = min(well(d, Q(r) + Q(s, 3))
                      for r in range(1, d + 1) for s in (-1, 1))
            c.require(eta > 0, "Root-isolation margin not positive")
            bound = max(max(row) for row in rows)
            c.require(bound >= 0, "Invalid scale maximum")
            eps = eta / (2 * (1 + bound))
            total, one, two = 0, 0, 0
            for j, row in enumerate(rows, 1):
                c.require(all(a >= 0 for a in row), "Retained t infeasible")
                zeros = sum(a == 0 for a in row)
                expected_zeros = 2 if j % d == 0 else 1
                c.require(zeros == expected_zeros, "Boundary multiplicity wrong")
                one += zeros == 1
                two += zeros == 2
                total += prod(d if a == 0 else k for a in row)
                for a in row:
                    if a > 0:
                        c.require(0 < eps * a < eta, "Well level outside margin")
            c.require(one == m * (d - 1), "Wrong internal count")
            c.require(two == m, "Wrong boundary count")
            c.require(total == family_count(k, l), "Family formula disagrees")
            forbidden = [Q(0), Q(n + 1)] + [Q(2 * j + 1, 2) for j in range(n)]
            for t in forbidden:
                c.require(any(selector(d, m, i, t) < 0 for i in range(1, m + 1)),
                          "Selector admits forbidden open interval")
            for r in range(1, d + 1):
                c.require(well(d, Q(r)) == 0, "Well center not a root")
                for s in (-1, 1):
                    c.require(well(d, Q(r) + Q(s, 3)) >= eta,
                              "Endpoint isolation margin wrong")
            families.append({"k": k, "l": l, "count": total,
                             "strictly_exceeds_grid": total > k ** l})

    values, witnesses = best_blocks(60)
    for n in range(21):
        c.require(values[n] == max(partition_values(n)), "Block optimum mismatch")
    for n in range(61):
        parts = witnesses[n]
        c.require(sum(parts) == n, "Witness has wrong dimension")
        c.require(prod(2 if s == 1 else block_count(s) for s in parts) == values[n],
                  "Witness product does not attain the recurrence")
        c.require(values[n] >= 2 ** n, "Grid option lost")
        if n:
            c.require(values[n] <= (3 ** n + 1) // 2, "Lower exceeds upper bound")

    # Index-balance arithmetic for a separable square-grid model. This is not
    # a finite replacement for the perturbation/topological-degree proof.
    degree_controls = 0
    for k in range(1, 13):
        for l in range(1, 13):
            positive = sum(comb(l, j) * k ** (l - j) * (k - 1) ** j
                           for j in range(0, l + 1, 2))
            negative = sum(comb(l, j) * k ** (l - j) * (k - 1) ** j
                           for j in range(1, l + 1, 2))
            c.require(positive - negative == 1, "Gradient degree arithmetic wrong")
            c.require(positive + negative == (2 * k - 1) ** l,
                      "Critical-point arithmetic wrong")
            c.require(positive == ((2 * k - 1) ** l + 1) // 2,
                      "Upper-bound arithmetic wrong")
            c.require(k ** l <= positive, "Grid exceeds upper bound")
            degree_controls += 1

    rejected = 0
    for k, l in [(0, 3), (-2, 3), (3, 3), (2, 2), (2.0, 3), (True, 3), (2, 3.0)]:
        try:
            family_count(k, l)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("Invalid family input accepted")
    c.require(rejected == 7, "Missing negative control")
    # Explicitly reject tempting incorrect claims rather than silently report
    # a successful count under a looser or different problem.
    false_claims = {
        "base_has_at_most_2_to_10_zeros": len(point_codes) <= 2 ** 10,
        "all_nine_radicands_are_positive": all(all(a > 0 for a in s["radicands"])
                                               for s in slices),
        "k2_l3_family_equals_grid": family_count(2, 3) == 2 ** 3,
        "all_family_members_beat_grid": all(r["strictly_exceeds_grid"] for r in families),
    }
    for name, claim in false_claims.items():
        c.require(claim is False, "False claim accepted: " + name)

    return {
        "schema": 1,
        "problem_id": "2200006",
        "arithmetic": "Python integers and fractions.Fraction only",
        "assertions": c.count,
        "base_slices": slices,
        "base_distinct_real_algebraic_points": len(point_codes),
        "base_upper_bound": (3 ** 10 + 1) // 2,
        "even_family_cases": families,
        "family_case_count": len(families),
        "restricted_product_optima": [
            {"dimension": n, "count": values[n], "blocks": witnesses[n]}
            for n in (1, 2, 3, 9, 10, 12, 20, 24, 30, 40, 48, 60)
        ],
        "exhaustive_partition_dimensions": list(range(21)),
        "gradient_index_arithmetic_cases": degree_controls,
        "invalid_inputs_rejected": rejected,
        "false_claims_rejected": sorted(false_claims),
        "scope": "Finite exact controls, not a global extremal solution or formal proof"
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
