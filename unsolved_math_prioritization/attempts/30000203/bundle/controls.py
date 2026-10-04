#!/usr/bin/env python3
"""Exact, bounded controls for problem 30000203; Python standard library only.
No internet, no source PDFs, no enumeration of the 60**6-point socle.
The optional full subgroup lattice is restricted to A6 (order 360).
"""
import argparse
from collections import Counter, deque
from fractions import Fraction
from itertools import permutations
from math import factorial, prod, comb
import json
from pathlib import Path
import time


def compose(p, q):
    """p*q means p after q; this convention is used throughout."""
    return tuple(p[q[i]] for i in range(len(p)))


def inverse(p):
    q = [0] * len(p)
    for i, x in enumerate(p):
        q[x] = i
    return tuple(q)


def even(p):
    return sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p))) % 2 == 0


def cycle_type(p):
    left = set(range(len(p))); sizes = []
    while left:
        x = min(left); y = x; size = 0
        while y in left:
            left.remove(y); size += 1; y = p[y]
        sizes.append(size)
    return tuple(sorted(sizes))


def permutation(n, *cycles):
    p = list(range(n))
    for cyc in cycles:
        for i, x in enumerate(cyc):
            p[x - 1] = cyc[(i + 1) % len(cyc)] - 1
    return tuple(p)


def partitions(n, minimum=1):
    if n == 0:
        yield ()
    for first in range(minimum, n + 1):
        for tail in partitions(n - first, first):
            yield (first,) + tail


def class_data(n):
    """All nonidentity even cycle types, including A_n class splitting."""
    rows = []
    for part in partitions(n):
        if len(part) == n or (n - len(part)) % 2:
            continue
        counts = Counter(part)
        symmetric_centralizer = prod(length**count * factorial(count)
                                    for length, count in counts.items())
        split = all(length % 2 == 1 and count == 1
                    for length, count in counts.items())
        alternating_centralizer = symmetric_centralizer if split else symmetric_centralizer // 2
        rows.append({"type": list(part), "centralizer": alternating_centralizer,
                     "class_size": factorial(n) // 2 // alternating_centralizer,
                     "number_of_classes": 2 if split else 1})
    assert sum(r["class_size"] * r["number_of_classes"] for r in rows) + 1 == factorial(n) // 2
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='CONTROL_RESULTS.json')
    parser.add_argument('--full-lattice', action='store_true')
    args = parser.parse_args()
    start = time.monotonic()
    degree = 6
    P = list(p for p in permutations(range(degree)) if even(p))
    ids = {p: i for i, p in enumerate(P)}
    e = ids[tuple(range(degree))]
    assert e == 0 and len(P) == 360
    mult = [[ids[compose(p, q)] for q in P] for p in P]
    inv = [ids[inverse(p)] for p in P]
    Q = frozenset(i for i, p in enumerate(P) if p[5] == 5)
    assert len(Q) == 60
    centralizers = {t: frozenset(q for q in Q if mult[q][t] == mult[t][q])
                    for t in Q if t != e}
    cstar = max(map(len, centralizers.values()))
    m = len(Q) // cstar
    assert (cstar, m) == (5, 12)

    def closure(gens):
        found = {e}; todo = [e]
        for x in todo:
            for g in gens:
                y = mult[x][g]
                if y not in found:
                    found.add(y); todo.append(y)
        return frozenset(found)

    def centralizer_in_Q(subgroup):
        return frozenset(t for t in Q if all(mult[t][x] == mult[x][t] for x in subgroup))

    # A_6 stabilizer of three unordered pairs has order 24.
    pairs = frozenset((frozenset((0, 2)), frozenset((1, 3)), frozenset((4, 5))))
    R = frozenset(i for i, p in enumerate(P)
                  if frozenset(frozenset(p[x] for x in pair) for pair in pairs) == pairs)
    t = ids[permutation(6, (1, 3), (2, 4))]
    D = R & Q
    assert len(R) == 24 and len(D) == 4 and D <= centralizers[t]
    assert set(P[r][5] for r in R) == set(range(6))

    # Construct the equivariant function on P, and independently test its full stabilizer.
    f = {}
    for r in R:
        for q in Q:
            x = mult[r][q]
            value = mult[mult[inv[q]][t]][q]
            if x in f:
                assert f[x] == value
            f[x] = value
    for x in range(len(P)):
        f.setdefault(x, e)
    assert all(f[mult[x][q]] == mult[mult[inv[q]][f[x]]][q]
               for x in range(len(P)) for q in Q)
    stabilizer = frozenset(g for g in range(len(P))
                          if all(f[mult[g][x]] == f[x] for x in range(len(P))))
    assert stabilizer == R
    witness_orbit_size = len(P) // len(stabilizer)
    assert witness_orbit_size == 15

    # Direct cycle-type control for the elementary exclusion of order-30 R.
    involutions = [i for i in range(1, len(P)) if mult[i][i] == e]
    assert len(involutions) == 45
    assert all(sum(P[i][j] == j for j in range(6)) == 2 for i in involutions)
    t5 = ids[permutation(6, (1, 2, 3, 4, 5))]
    C5 = centralizers[t5]
    N5 = frozenset(g for g in range(len(P))
                  if frozenset(mult[mult[inv[g]][c]][g] for c in C5) == C5)
    assert len(N5) == 10 and N5 <= Q

    # Left-coset transversal of Q in P, and its induced left multiplication action.
    cosets = []
    coset_id = {}
    for x in range(len(P)):
        if x not in coset_id:
            cid = len(cosets)
            coset = frozenset(mult[x][q] for q in Q)
            cosets.append((x, coset))
            for z in coset:
                coset_id[z] = cid
    assert len(cosets) == 6

    def fixed_count(subgroup):
        # B^R is a product over R\P/Q of centralizers in Q=T.
        unused = set(range(len(cosets))); answer = 1; factors = []
        while unused:
            c = min(unused); s = cosets[c][0]
            orbit = {coset_id[mult[r][s]] for r in subgroup}
            unused -= orbit
            intersection = frozenset(mult[mult[inv[s]][r]][s] for r in subgroup) & Q
            factor = len(centralizer_in_Q(intersection))
            factors.append(factor); answer *= factor
        return answer, sorted(factors)

    fixed_by_type = {}
    burnside_sum = 0
    for g, perm in enumerate(P):
        subgroup = closure([g])
        fixed, factors = fixed_count(subgroup)
        typ = str(cycle_type(perm))
        if typ in fixed_by_type:
            assert fixed_by_type[typ]["fixed_points"] == fixed
        else:
            fixed_by_type[typ] = {"fixed_points": fixed, "centralizer_factors": factors, "count": 0}
        fixed_by_type[typ]["count"] += 1
        burnside_sum += fixed
    assert burnside_sum % 360 == 0
    orbits = burnside_sum // 360
    population = 60**6
    average = Fraction(population - 1, orbits - 1)
    assert average >= 72  # Global averaging does not detect the short orbit of length 15.

    # Bounded optional exhaustive verification; every subgroup is reached by adjoining one element.
    lattice = None
    if args.full_lattice:
        trivial = frozenset((e,))
        records = {trivial: ()}; queue = deque((trivial,))
        while queue:
            subgroup = queue.popleft(); gens = records[subgroup]
            unused = set(range(len(P))) - subgroup
            while unused:
                g = min(unused)
                unused -= {mult[h][g] for h in subgroup}
                bigger = closure(gens + (g,))
                if bigger not in records:
                    records[bigger] = gens + (g,); queue.append(bigger)
            if time.monotonic() - start > 120:
                raise RuntimeError('A6-only 120-second budget exceeded; no partial output is accepted')
        by_order = Counter(map(len, records))
        best = 0; best5 = 0; admissible = 0
        for subgroup in records:
            fixed = centralizer_in_Q(subgroup & Q) - {e}
            if fixed:
                admissible += 1; best = max(best, len(subgroup))
            if (subgroup & Q) <= C5:
                best5 = max(best5, len(subgroup))
        assert len(records) == 501 and best == 24 and best5 == 5
        lattice = {"subgroups": len(records), "by_order": dict(sorted(by_order.items())),
                   "admissible_subgroups": admissible, "largest_admissible_order": best,
                   "largest_admissible_order_for_fixed_5_cycle": best5,
                   "minimum_subdegree_from_5_cycle_value": 360 // best5}

    # Cycle-type enumeration, not permutation enumeration, for 5 <= n <= 30.
    minima = []
    for n in range(5, 31):
        rows = class_data(n); minimum = min(row['class_size'] for row in rows)
        minima.append({"n": n, "minimum_class_size": minimum,
                       "minimizing_types": [r['type'] for r in rows if r['class_size'] == minimum]})
    assert [row['minimum_class_size'] for row in minima[:5]] == [12, 40, 70, 105, 168]
    a8_rows = class_data(8)
    a8_involution = next(row for row in a8_rows if row['type'] == [2, 2, 2, 2])
    assert a8_involution['centralizer'] == 192 and a8_involution['class_size'] == 105
    # For P=A9, Q=A8, the 3-cycle witness has stabilizer at least 1080, so s(G)<=168<945.
    assert 181440 // 1080 == 168 < 9 * 105

    # Countercontrol to the universal sufficiency of the Sylow-size route.
    # For P=A20,Q=A19 the explicitly available 3-cycle centralizer in Q is already larger
    # than every Sylow subgroup of P, so cstar is too large, without any asymptotic assumption.
    order_A20 = factorial(20) // 2
    sylow_sizes_A20 = {}
    value = order_A20
    for prime in range(2, 21):
        if prime > 2 and any(prime % q == 0 for q in range(2, prime)):
            continue
        power = 1
        while value % prime == 0:
            power *= prime; value //= prime
        if power > 1:
            sylow_sizes_A20[str(prime)] = power
    assert value == 1
    available_centralizer_A19 = 3 * factorial(16) // 2
    assert max(sylow_sizes_A20.values()) < available_centralizer_A19

    result = {
        "problem_id": 30000203, "universal_claim_resolved": False,
        "A6_A5": {"P_order": 360, "Q_order": 60, "k": 6, "component_minimum": m,
                  "component_centralizer_orders": sorted(set(map(len, centralizers.values()))),
                  "upper_bound": 72, "witness_R_order": len(R), "intersection_order": len(D),
                  "direct_function_stabilizer_order": len(stabilizer), "witness_orbit_size": witness_orbit_size,
                  "proved_minimum": 15, "five_cycle_normalizer_order": len(N5),
                  "five_cycle_normalizer_contained_in_Q": True,
                  "lattice": lattice},
        "burnside_A6_A5": {"fixed_points_by_cycle_type": fixed_by_type, "orbits_including_identity": orbits,
                           "population": population, "nontrivial_average_orbit_size": str(average),
                           "average_is_at_least_72": True},
        "alternating_class_minima_5_through_30": minima,
        "A8_exception": {"involution_class": a8_involution, "three_cycle_class_size": 112,
                         "P_A9_twisted_upper_bound_from_three_cycle": 168, "k_times_component_minimum": 945},
        "Sylow_route_countercontrol": {"P": "A20", "Q": "A19",
                                         "available_Q_centralizer_order": available_centralizer_A19,
                                         "Sylow_orders_in_P": sylow_sizes_A20},
        "limits": {"largest_permutation_group_order": 360, "largest_partition_degree": 30,
                   "socle_points_enumerated": 0, "full_lattice_requested": args.full_lattice,
                   "large_search": False, "global_conclusion_from_finite_checks": False}
    }
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({"all_assertions_passed": True, "elapsed_seconds": round(time.monotonic() - start, 3),
                      "output": args.output, "A6_minimum": 15, "A8_minimum_class": 105,
                      "A6_subgroups": lattice['subgroups'] if lattice else None,
                      "burnside_orbits": orbits, "average": str(average)}, sort_keys=True))

if __name__ == '__main__':
    main()
