#!/usr/bin/env python3
"""Independent finite audit diagnostics. Not a production optimization algorithm."""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import math
import os
import random
import sys


class AuditFailure(RuntimeError):
    pass


def need(value, reason):
    if not value:
        raise AuditFailure(reason)


def scalar(a, b):
    need(len(a) == len(b), 'dimension mismatch')
    return sum((x * y for x, y in zip(a, b)), Q(0))


def ceil(q):
    return -((-q.numerator) // q.denominator)


def decompose(d, mutant=None):
    terms = []
    for sign in ((1,) if mutant == 'positive_only' else (1, -1)):
        previous = Q(0)
        for level in sorted(set(sign * x for x in d if sign * x > 0)):
            entries = tuple(sign if sign * x >= level else 0 for x in d)
            if mutant == 'reverse_negative' and sign == -1:
                entries = tuple(-x for x in entries)
            terms.append((level - previous, entries))
            previous = level
    return terms


def verify_decomposition(d, mutant=None):
    terms = decompose(d, mutant)
    need(len(terms) <= len(d), 'too many threshold layers')
    need(tuple(sum((lam * r[i] for lam, r in terms), Q(0))
               for i in range(len(d))) == d, 'layer reconstruction')
    for lam, r in terms:
        need(lam > 0 and any(r), 'nonpositive or empty layer')
        for i in range(len(d)):
            need(r[i] * d[i] >= 0 and abs(lam * r[i]) <= abs(d[i]),
                 'coordinate conformity')
            for j in range(len(d)):
                delta, step = d[i] - d[j], r[i] - r[j]
                need(delta * step >= 0 and abs(lam * step) <= abs(delta),
                     'difference conformity')
    return terms


def solve_square(rows, rhs):
    n = len(rhs)
    mat = [list(row) + [value] for row, value in zip(rows, rhs)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if mat[i][col]), None)
        if pivot is None:
            return None
        mat[col], mat[pivot] = mat[pivot], mat[col]
        pivot_value = mat[col][col]
        mat[col] = [x / pivot_value for x in mat[col]]
        for i in range(n):
            if i != col:
                multiplier = mat[i][col]
                mat[i] = [x - multiplier * y for x, y in zip(mat[i], mat[col])]
    return tuple(mat[i][-1] for i in range(n))


def valid(edges, y):
    return all(y[u] - y[v] >= b for u, v, b in edges)


def vertex_lp(n, edges, a, fixed):
    """Independent tiny exact oracle; caller certifies a nonnegative row combination."""
    fixed = dict(fixed)
    neighbors = [set() for _ in range(n)]
    for u, v, b in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    unseen = set(range(n))
    while unseen:
        component = {min(unseen)}
        frontier = list(component)
        while frontier:
            for v in neighbors[frontier.pop()]:
                if v not in component:
                    component.add(v)
                    frontier.append(v)
        unseen -= component
        if not component.intersection(fixed):
            need(sum(a[i] for i in component) == 0, 'uncertified lineality cost')
            fixed[min(component)] = Q(0)
    free = [i for i in range(n) if i not in fixed]
    eqs = []
    for u, v, b in edges:
        coeff = tuple(Q(int(i == u) - int(i == v)) for i in free)
        eqs.append((coeff, b - fixed.get(u, Q(0)) + fixed.get(v, Q(0))))
    candidates = []
    for selected in combinations(eqs, len(free)):
        x = solve_square([r for r, b in selected], [b for r, b in selected])
        if x is None:
            continue
        y = dict(fixed)
        y.update(zip(free, x))
        point = tuple(y[i] for i in range(n))
        if valid(edges, point):
            candidates.append((scalar(a, point), point))
    return min(candidates) if candidates else None


def ring_sets(lo, hi, d, mutant=None):
    ground = [(i, t) for i in range(2) for t in range(lo[i] + 1, hi[i] + 1)]
    family = []
    for mask in range(1 << len(ground)):
        S = {v for j, v in enumerate(ground) if mask & (1 << j)}
        prefix = mutant == 'omit_chains' or all(
            t == lo[i] + 1 or (i, t - 1) in S for i, t in S)
        base = mutant == 'omit_base' or all((0, t) in S for t in
            range(lo[0] + 1, min(hi[0], lo[1] + d) + 1)) and lo[1] + d <= hi[0]
        implication = True
        for i, t in S:
            if i == 1:
                target = t + d if mutant != 'reverse_implication_shift' else t - d
                implication &= target <= lo[0] or (0, target) in S
        if prefix and base and implication:
            family.append(frozenset(S))
    return ground, family


def intended_ring(lo, hi, d):
    return {frozenset((i, t) for i in range(2) for t in range(lo[i] + 1, p[i] + 1))
            for p in product(*(range(lo[i], hi[i] + 1) for i in range(2)))
            if p[0] - p[1] >= d}


def expect_failure(operation, label):
    try:
        operation()
    except AuditFailure as error:
        reasons = {'positive_only': 'layer reconstruction', 'reverse_negative': 'layer reconstruction', 'omit_base': 'mutated ring', 'omit_chains': 'mutated ring', 'reverse_implication_shift': 'mutated ring', 'floor_instead_of_ceiling': 'floor-rounded assignment infeasible', 'omit_bipartition_sign_change': 'cover min fails', 'remove_subunit_layer': 'subunit removal infeasible', 'replace_hull_with_relaxation': 'LP point outside mixed hull', 'replace_hull_with_mixed_set': 'hull point need not be mixed integral', 'explicit_exception_control': 'explicit guard remains live'}
        need(label in reasons and str(error) == reasons[label], 'unintended rejection reason')
        return label
    raise AuditFailure('mutant survived: ' + label)


def main():
    need(os.getuid() == os.geteuid() == 1000, 'UID=EUID=1000 required')
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode, '-I -S -B required')
    root = Path(__file__).resolve().parent
    for name, expected in [
        ('CURRENT_PROOF.md', 'c90d5a287718b26026cbee07f77d8710807a2c7a85f2057a1b7d00f5bb72ce32'),
        ('exact_checks.py', 'd05fb84dff9f21e40bc66611a5b537cea4cd0b71db7c8d71f852d2b7865efb63')]:
        path = root / name
        need(hashlib.sha256(path.read_bytes()).hexdigest() == expected, 'snapshot hash mismatch')
        try:
            with path.open('ab'):
                pass
        except PermissionError:
            pass
        else:
            raise AuditFailure('read-only file write unexpectedly permitted')
    try:
        with (root / 'forbidden-create').open('xb'):
            pass
    except PermissionError:
        pass
    else:
        raise AuditFailure('read-only directory create unexpectedly permitted')

    count = dict(layer_vectors=0, signed_difference_checks=0, instances=0,
                 slices=0, submodular_pairs=0, removal_checks=0, ring_instances=0,
                 ring_subsets=0, boundary_checks=0, unbounded_ray_checks=0,
                 ring_extension_pairs=0, nonroot_readonly_probes=3)
    # Exhaustive ties, zero entries, opposite signs, unit-size coefficients.
    values = [Q(-2), Q(-1), Q(-1, 2), Q(0), Q(1, 2), Q(1), Q(2)]
    for d in product(values, repeat=4):
        terms = verify_decomposition(d)
        count['layer_vectors'] += 1
        count['signed_difference_checks'] += len(terms) * 16
    rng = random.Random(110130001102)
    for _ in range(200):
        d = tuple(Q(rng.randrange(-10**12, 10**12), rng.randrange(1, 10**8))
                  for i in range(rng.randrange(1, 9)))
        verify_decomposition(d)
        count['layer_vectors'] += 1

    # Each objective is explicitly a nonnegative combination of inequality rows.
    specifications = [(1, [], set()), (1, [], {0}), (3, [(0, 1, Q(1, 2))], {0, 2})]
    for n in [2, 3]:
        for mask in range(1 << n):
            edges = [(0, i, Q((-1)**i * (i + 1), 2 * i + 1)) for i in range(1, n)]
            specifications.append((n, edges, {i for i in range(n) if mask & (1 << i)}))
    specifications += [(2, [(0, 1, Q(10**60 + 13, 2**127 - 1))], {0, 1}),
                       (3, [(0, 1, Q(-17, 5)), (0, 2, Q(19, 7))], {1, 2})]
    for n, edges, I in specifications:
        k = math.lcm(*(b.denominator for u, v, b in edges))
        B = max([1] + [ceil(abs(b)) for u, v, b in edges])
        a = [Q(0)] * n
        for j, (u, v, b) in enumerate(edges):
            a[u] += j + 1
            a[v] -= j + 1
        relaxation = vertex_lp(n, edges, a, {})
        need(relaxation is not None, 'feasible relaxation missing')
        _, ystar = relaxation
        need(max(map(abs, ystar)) <= n * B, 'anchored optimal-vertex bound')
        ids = sorted(I)
        lo = {i: ceil(ystar[i] - n) for i in ids}
        hi = {i: (ystar[i] + n).__floor__() for i in ids}
        need(all(hi[i] - lo[i] <= 2 * n for i in ids), 'numeric-width dependence')
        oracle = {}
        for p in product(*(range(lo[i], hi[i] + 1) for i in ids)):
            fixed = dict(zip(ids, map(Q, p)))
            result = vertex_lp(n, edges, a, fixed)
            domain = all(fixed[u] - fixed[v] >= b for u, v, b in edges if u in I and v in I)
            need(domain == (result is not None), 'projection of integer coordinates')
            count['slices'] += 1
            if result is None:
                continue
            value, z = result
            need(all((k * value).denominator == 1 for value in z), 'TU slice denominator bound')
            oracle[p] = value
            for lam, r in verify_decomposition(tuple(z[i] - ystar[i] for i in range(n))):
                need(valid(edges, tuple(ystar[i] + lam * r[i] for i in range(n))), 'layer LP feasibility')
                need(scalar(a, r) >= 0, 'negative layer slope at LP optimum')
                if lam >= 1:
                    moved = tuple(z[i] - r[i] for i in range(n))
                    need(valid(edges, moved), 'removed layer infeasible')
                    need(all(moved[i].denominator == 1 for i in I), 'removed layer noninteger')
                    need(scalar(a, moved) <= value, 'removed layer raises objective')
                    need(sum(abs(moved[i] - ystar[i]) for i in range(n)) <
                         sum(abs(z[i] - ystar[i]) for i in range(n)), 'distance not strictly reduced')
                    count['removal_checks'] += 1
        need(bool(oracle), 'empty proximity domain')
        for p, q in product(oracle, repeat=2):
            meet = tuple(min(x, y) for x, y in zip(p, q))
            join = tuple(max(x, y) for x, y in zip(p, q))
            need(meet in oracle and join in oracle, 'domain not a sublattice')
            need(oracle[p] + oracle[q] >= oracle[meet] + oracle[join], 'submodular inequality')
            count['submodular_pairs'] += 1
        count['instances'] += 1

    for lo in [(-1, -1), (0, 0), (-2, 1)]:
        for lengths in product(range(3), repeat=2):
            hi = tuple(lo[i] + lengths[i] for i in range(2))
            for d in range(-3, 4):
                ground, family = ring_sets(lo, hi, d)
                need(set(family) == intended_ring(lo, hi, d), 'ring all-subset equivalence')
                if family:
                    minimum = set.intersection(*(set(S) for S in family))
                    need(frozenset(minimum) in family, 'missing minimum')
                    for v in ground:
                        members = [set(S) for S in family if v in S]
                        if members:
                            need(frozenset(set.intersection(*members)) in family, 'missing containing-element minimum')
                    for A, B in product(family, repeat=2):
                        need(A & B in family and A | B in family, 'ring not closed')
                count['ring_instances'] += 1
                count['ring_subsets'] += 1 << len(ground)

    # Check Schrijver's closure-based reduction on a genuinely nonlinear slice value.
    ground = [(i, t) for i in range(2) for t in [1, 2]]
    all_sets = [frozenset(v for j, v in enumerate(ground) if mask & (1 << j))
                for mask in range(16)]
    def closure(S):
        return frozenset((i, u) for i, t in S for u in range(1, t + 1))
    ideals = [S for S in all_sets if closure(S) == S]
    def f(S):
        p = [sum(i == j for j, t in S) for i in range(2)]
        return 2 * max(p[0] + Q(1, 2), p[1] - Q(1, 3)) - sum(p)
    costs = {}
    for v in ground:
        Lv = frozenset().union(*(S for S in ideals if v not in S))
        need(Lv | {v} in ideals, 'ring quotient prerequisite')
        costs[v] = max(Q(0), f(Lv) - f(Lv | {v}))
    def h(S):
        C = closure(S)
        return f(C) + sum(costs[v] for v in C) - sum(costs[v] for v in S)
    for A, B in product(all_sets, repeat=2):
        need(h(A) + h(B) >= h(A & B) + h(A | B), 'ring extension is not submodular')
        count['ring_extension_pairs'] += 1
    best = min(all_sets, key=h)
    need(h(best) == f(closure(best)) == min(map(f, ideals)), 'ring extension reconstruction')

    # Explicit integral recession witnesses; no floating-point or sign assumptions.
    for c, ray in [((Q(1), Q(0)), (-1, 1)),
                   ((Q(-1), Q(0)), (1, 0)),
                   ((Q(0), Q(1)), (1, -1)),
                   ((Q(-1), Q(-1)), (1, 1))]:
        need(sum(ray) >= 0 and scalar(c, ray) < 0, 'invalid original-coordinate ray')
        y_ray = (Q(ray[0]), Q(-ray[1]))
        a = (c[0], -c[1])
        need(y_ray[0] - y_ray[1] >= 0 and scalar(a, y_ray) < 0,
             'invalid sign-changed ray')
        need(all((Q(2) + 10**30 * x).denominator == 1 for x in ray),
             'ray loses integrality at large time')
        count['unbounded_ray_checks'] += 1

    # Exact near-boundary checks for a one-edge all-integer model: hull x0+x1>=1.
    eps = Q(1, 2**256 + 297)
    for x, inside in [((Q(1, 2), Q(1, 2)), True),
                      ((Q(1, 2), Q(1, 2) - eps), False),
                      ((Q(1, 2), Q(1, 2) + eps), True),
                      ((Q(1, 4), Q(1, 4)), False)]:
        need((sum(x) >= ceil(Q(1, 2))) == inside, 'exact hull boundary')
        count['boundary_checks'] += 1

    mutants = []
    for mutation in ['positive_only', 'reverse_negative']:
        mutants.append(expect_failure(lambda m=mutation: verify_decomposition((Q(-1), Q(2)), m), mutation))
    for mutation, lo, hi, d in [
        ('omit_base', (0, 0), (1, 1), 1),
        ('omit_chains', (0, 0), (2, 2), -3),
        ('reverse_implication_shift', (-1, -1), (2, 2), 1)]:
        mutants.append(expect_failure(lambda m=mutation, l=lo, h=hi, v=d:
            need(set(ring_sets(l, h, v, m)[1]) == intended_ring(l, h, v), 'mutated ring'), mutation))
    mutants.append(expect_failure(lambda: need(Q(0) >= Q(1, 2), 'floor-rounded assignment infeasible'), 'floor_instead_of_ceiling'))
    mutants.append(expect_failure(lambda: need(min(1, 0) + min(0, 1) >= 1, 'cover min fails'), 'omit_bipartition_sign_change'))
    mutants.append(expect_failure(lambda: need(Q(1, 2) - 1 >= 0, 'subunit removal infeasible'), 'remove_subunit_layer'))
    mutants.append(expect_failure(lambda: need(Q(1, 4) + Q(1, 4) >= 1, 'LP point outside mixed hull'), 'replace_hull_with_relaxation'))
    mutants.append(expect_failure(lambda: need(Q(1, 2).denominator == 1, 'hull point need not be mixed integral'), 'replace_hull_with_mixed_set'))
    mutants.append(expect_failure(lambda: need(False, 'explicit guard remains live'), 'explicit_exception_control'))
    print(json.dumps({'status': 'PASS_INDEPENDENT_FINITE_DIAGNOSTICS', 'uid': os.geteuid(),
        'python_optimize': sys.flags.optimize, 'counts': count,
        'killed_function_mutants': mutants[:5], 'rejected_counterexample_controls': mutants[5:],
        'limitations': 'Finite exact diagnostics only. Universal validity and bit complexity are audited in the written report, not certified by these tests.'}, indent=2))


if __name__ == '__main__':
    main()
