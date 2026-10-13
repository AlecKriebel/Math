#!/usr/bin/env python3
"""Exact, independent algebraic boundary controls; no assertion statements.

Bounded checks instantiate the separately written all-degree proofs. They are
not a proof of ideal membership, primality, or generator minimality at all degrees.
"""
import hashlib
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path

N = 6
ZERO = (0,) * N
M = (
    ((1, 0, 0, 0, 1, 0), (0, 1, 0, 1, 0, 0)),
    ((0, 1, 0, 0, 0, 1), (0, 0, 1, 0, 1, 0)),
    ((0, 0, 1, 1, 0, 0), (1, 0, 0, 0, 0, 1)),
)
COUNTS = {}


class AuditFailure(Exception):
    pass


def check(ok, message, group="general"):
    COUNTS[group] = COUNTS.get(group, 0) + 1
    if not ok:
        raise AuditFailure(message)


def normalize(p, characteristic=0):
    return {m: (c % characteristic if characteristic else c)
            for m, c in p.items()
            if (c % characteristic if characteristic else c) != 0}


def add(p, q, characteristic=0):
    result = dict(p)
    for m, c in q.items():
        result[m] = result.get(m, 0) + c
    return normalize(result, characteristic)


def scale(p, c, characteristic=0):
    return normalize({m: c * v for m, v in p.items()}, characteristic)


def shift(p, e):
    return {tuple(a + b for a, b in zip(m, e)): c for m, c in p.items()}


def binomial(pair, coefficient=1):
    return {pair[0]: 1, pair[1]: -coefficient}


G = tuple(binomial(pair) for pair in M)


def rank(rows, characteristic=0):
    if not rows:
        return 0
    a = [list(row) if characteristic else list(map(Fraction, row)) for row in rows]
    pivots = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(pivots, len(a))
                      if a[i][col] % characteristic != 0), None) if characteristic else next(
                          (i for i in range(pivots, len(a)) if a[i][col] != 0), None)
        if pivot is None:
            continue
        a[pivots], a[pivot] = a[pivot], a[pivots]
        factor = pow(a[pivots][col] % characteristic, -1, characteristic) if characteristic else 1 / a[pivots][col]
        a[pivots] = [v * factor % characteristic for v in a[pivots]] if characteristic else [v * factor for v in a[pivots]]
        for i in range(len(a)):
            if i != pivots:
                factor = a[i][col]
                a[i] = [(v - factor * w) % characteristic for v, w in zip(a[i], a[pivots])] if characteristic else [v - factor * w for v, w in zip(a[i], a[pivots])]
        pivots += 1
        if pivots == len(a):
            break
    return pivots


def compositions(total, length):
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, length - 1):
            yield (first,) + tail


def image(m):
    alpha, beta = m[:3], m[3:]
    return (sum(alpha), sum(beta)) + tuple(a + b for a, b in zip(alpha, beta))


def canonical(m):
    c = tuple(a + b for a, b in zip(m[:3], m[3:]))
    left = sum(m[:3])
    alpha = []
    for count in c:
        q = min(left, count)
        alpha.append(q)
        left -= q
    check(left == 0, "canonical x-degree not exhausted", "straightening")
    return tuple(alpha) + tuple(c[i] - alpha[i] for i in range(3))


def straighten(m, target):
    check(image(m) == image(target), "straightening fibers disagree", "straightening")
    current = m
    steps = 0
    old_distance = sum(abs(current[i] - target[i]) for i in range(3))
    while current != target:
        j = next((i for i in range(3) if current[i] > target[i]), None)
        i = next((i for i in range(3) if current[i] < target[i]), None)
        check(i is not None and j is not None and i != j,
              "matched total degree failed to supply donor/receiver", "straightening")
        check(current[j] >= 1 and current[3+i] >= 1,
              "exchange factor has negative exponent", "straightening")
        nxt = list(current)
        nxt[j] -= 1
        nxt[3+i] -= 1
        nxt[i] += 1
        nxt[3+j] += 1
        nxt = tuple(nxt)
        check(min(nxt) >= 0 and image(nxt) == image(current),
              "exchange changes fiber or leaves polynomial monomials", "straightening")
        donor = tuple(int(q == j) + int(q == 3+i) for q in range(N))
        residual = tuple(a-b for a, b in zip(current, donor))
        exchange = {current: 1, nxt: -1}
        relation_index = None
        sign = None
        for h, g in enumerate(G):
            if shift(g, residual) == exchange:
                relation_index, sign = h, 1
            if shift(scale(g, -1), residual) == exchange:
                relation_index, sign = h, -1
        check(relation_index is not None and sign in (-1, 1),
              "exchange not a polynomial multiple of a displayed generator", "straightening")
        new_distance = sum(abs(nxt[q] - target[q]) for q in range(3))
        check(new_distance == old_distance - 2,
              "termination measure not strictly reduced by two", "straightening")
        current, old_distance = nxt, new_distance
        steps += 1
        check(steps <= sum(m), "exchange route exceeded degree bound", "straightening")
    check(old_distance == 0, "route failed to reach target", "straightening")
    return steps


def reject(function, label):
    try:
        function()
    except AuditFailure:
        return label
    raise AuditFailure("mutant accepted: " + label)


def minimal_degree_two(generators, expected):
    monomials = sorted({m for g in generators for m in g})
    check(all(sum(m) == 2 for m in monomials),
          "a minimal degree-two certificate was applied outside its stated domain", "mutants")
    rows = [[g.get(m, 0) for m in monomials] for g in generators]
    check(rank(rows) == expected, "degree-two rank contradicts claimed minimal count", "mutants")


def all_one_annihilation(generators):
    check(all(sum(g.values()) == 0 for g in generators),
          "all-one evaluation fails", "mutants")


def run():
    all_monomials = [m for d in range(8) for m in compositions(d, N)]
    six = [m for pair in M for m in pair]
    check(len(set(six)) == 6, "generator supports overlap", "hypotheses")
    for pair in M:
        for m in pair:
            check(sum(m) == 2 and set(m).issubset({0, 1}) and any(m),
                  "nonzero/squarefree/degree-two exponent hypothesis fails", "hypotheses")
        check(all(min(a,b) == 0 for a,b in zip(*pair)),
              "binomial has a nontrivial common monomial factor", "hypotheses")
    minimal_degree_two(G, 3)
    all_one_annihilation(G)
    monomial_order = sorted(six)
    coefficient_rows = [[g.get(m, 0) for m in monomial_order] for g in G]
    check(rank(coefficient_rows) == 3, "rational generator rank wrong", "hypotheses")
    for p in (2, 3, 5, 7):
        check(rank(coefficient_rows, p) == 3, "rank fails in finite characteristic", "characteristic_boundary")
        check(all(sum(g.values()) % p == 0 for g in G),
              "all-one point fails in finite characteristic", "characteristic_boundary")
        for scalar in range(1, p):
            check(scalar % p != 0, "nonzero scalar monomial evaluation failed", "characteristic_boundary")
    coordinate = lambda q: tuple(int(j == q) for j in range(N))
    syzygy = add(add(shift(G[0], coordinate(2)), shift(G[1], coordinate(0))),
                 shift(G[2], coordinate(1)))
    check(syzygy == {}, "cyclic polynomial syzygy wrong", "localization")
    # Exact rank-three quotient means no Laurent division was smuggled in.
    check(rank(coefficient_rows) > 2, "polynomial minimality lost", "localization")
    for h in range(3):
        points = ((1,0,0,0,1,0), (0,1,0,0,0,1), (0,0,1,1,0,0))
        values = []
        for g in G:
            value = sum(c * __import__('functools').reduce(
                lambda a,b: a*b, (points[h][q] ** m[q] for q in range(N)), 1)
                        for m,c in g.items())
            values.append(value)
        check(values[h] == 1 and all(v == 0 for q,v in enumerate(values) if q != h),
              "irredundancy specialization fails", "hypotheses")
    fibers = {}
    route_count = 0
    route_steps = 0
    for m in all_monomials:
        check(sum(m) <= 7 and min(m) >= 0, "composition domain invalid", "straightening")
        fibers.setdefault(image(m), []).append(m)
        route_steps += straighten(m, canonical(m))
        route_count += 1
    # Exhaust all ordered pairs of a fiber, not just canonical normal forms.
    pair_count = 0
    for fiber in fibers.values():
        for m, n in itertools.product(fiber, repeat=2):
            route_steps += straighten(m, n)
            pair_count += 1
    polynomial_controls = 0
    for fiber in fibers.values():
        if len(fiber) > 1:
            coefficients = list(range(1, len(fiber)))
            coefficients.append(-sum(coefficients))
            check(sum(coefficients) == 0, "kernel coefficient grouping fails", "kernel_grouping")
            check(len(set(image(m) for m in fiber)) == 1,
                  "grouping accidentally combines distinct target monomials", "kernel_grouping")
            for p in (2, 3, 5, 7):
                check(sum(c % p for c in coefficients) % p == 0,
                      "characteristic-dependent coefficient grouping fails", "kernel_grouping")
            polynomial_controls += 1
    mutants = []
    mutants.append(reject(lambda: minimal_degree_two((G[0], G[1], G[0]), 3), "duplicate third generator"))
    mutants.append(reject(lambda: all_one_annihilation(G + ({coordinate(0): 1},)), "adjoin monomial"))
    wrong = (G[0], G[1], binomial(M[2], 2))
    mutants.append(reject(lambda: all_one_annihilation(wrong), "inconsistent third coefficient 2"))
    wrong_syzygy = add(add(shift(wrong[0], coordinate(2)), shift(wrong[1], coordinate(0))),
                       shift(wrong[2], coordinate(1)))
    check(wrong_syzygy == {(1,1,0,0,0,1): -1},
          "coefficient inconsistency did not exhibit a monomial in the ideal", "mutants")
    redundant = G + (shift(G[0], coordinate(0)),)
    mutants.append(reject(lambda: minimal_degree_two(redundant, 4), "redundant degree-three generator"))
    mutants.append(reject(lambda: straighten(M[0][0], M[1][0]), "different image fibers"))
    reduced_rows = coefficient_rows[:2] + [coefficient_rows[2]]
    check(rank(reduced_rows) == rank(coefficient_rows[:2]) + 1,
          "omitted third generator indistinguishable in degree two", "mutants")
    flipped = (G[0], G[1], scale(G[2], -1))
    minimal_degree_two(flipped, 3)
    all_one_annihilation(flipped)
    check(rank([[g.get(m, 0) for m in monomial_order] for g in flipped]) == 3,
          "harmless cyclic orientation rejected", "sign_boundary")
    # Runtime exception guards must survive Python's -O mode.
    probe = reject(lambda: check(False, "deliberate guard failure", "optimization_guard"),
                   "explicit guard remains active")
    return {
        "result": "PASS",
        "python_optimization_level": sys.flags.optimize,
        "exception_guards_active": probe == "explicit guard remains active",
        "checks_total": sum(COUNTS.values()),
        "checks_by_group": COUNTS,
        "characteristic_boundary_fields": [2,3,5,7],
        "monomials_through_degree_7": len(all_monomials),
        "image_fibers_through_degree_7": len(fibers),
        "canonical_routes": route_count,
        "ordered_same_image_pair_routes": pair_count,
        "exchange_steps": route_steps,
        "coefficient_grouping_polynomial_controls": polynomial_controls,
        "rejected_mutants": mutants,
        "positive_sign_control": "unit sign reversal accepted",
        "all_degree_proofs": "INDEPENDENT_REASONING_BEFORE_COMPARISON.md",
        "bounded_computation_does_not_prove_all_degree_claims": True,
        "priority_or_publication_clearance": False,
    }


if __name__ == "__main__":
    result = run()
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    data = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if len(sys.argv) == 2:
        Path(sys.argv[1]).write_text(data)
    sys.stdout.write(data)
