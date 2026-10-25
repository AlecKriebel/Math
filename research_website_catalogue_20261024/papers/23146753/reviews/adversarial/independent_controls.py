"""Bounded exact diagnostics; not a replacement for the universal proofs.

Only writes the requested result path in this review namespace. No target
program is imported. Standard-library arithmetic only. Use a wall-clock alarm.
"""
from collections import deque
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import hashlib, json, signal, sys, time

if sys.flags.optimize:
    raise SystemExit('Exact diagnostics require assertions enabled; remove -O.')
signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError()))
signal.alarm(90)
START = time.time()

def mtp(weights, n):
    return all(weights[x & y] * weights[x | y] >= weights[x] * weights[y]
               for x in range(1 << n) for y in range(1 << n))

def support_geometry():
    result = []
    for n in range(5):
        states = range(1 << n)
        pairs = list(combinations(range(n), 2))
        lattices = []
        for mask in range(1, 1 << (1 << n)):
            S = [x for x in states if mask >> x & 1]
            if all((mask >> (x & y) & 1) and (mask >> (x | y) & 1)
                   for x in S for y in S):
                lattices.append(S)
        count = witness_count = pin_cases = ties = 0
        for S in lattices:
            unary = [{x >> i & 1 for x in S} for i in range(n)]
            projections = {e: {(x >> e[0] & 1, x >> e[1] & 1) for x in S}
                           for e in pairs}
            for graph in range(1 << len(pairs)):
                edges = [e for j, e in enumerate(pairs) if graph >> j & 1]
                feasible = [x for x in states if
                            all((x >> i & 1) in unary[i] for i in range(n)) and
                            all((x >> i & 1, x >> j & 1) in projections[i, j]
                                for i, j in edges)]
                if feasible != S:
                    continue
                count += 1
                active = [i for i in range(n) if len(unary[i]) == 2]
                pin_cases += len(active) < n
                implications = []
                for i, j in edges:
                    if i not in active or j not in active:
                        continue
                    pr = projections[i, j]
                    assert (0, 0) in pr and (1, 1) in pr
                    if (1, 0) not in pr:
                        implications.append((i, j))
                    if (0, 1) not in pr:
                        implications.append((j, i))
                D = lambda x: sum((x >> i & 1) not in unary[i] for i in range(n)) + sum(
                    (x >> i & 1) * (1 - (x >> j & 1)) for i, j in implications)
                assert [x for x in states if D(x) == 0] == S
                reach = {(i, i) for i in active} | set(implications)
                for k in active:
                    for i in active:
                        for j in active:
                            if (i, k) in reach and (k, j) in reach:
                                reach.add((i, j))
                classes = []
                unused = set(active)
                while unused:
                    i = min(unused)
                    c = {j for j in unused if (i, j) in reach and (j, i) in reach}
                    classes.append(c)
                    unused -= c
                ties += any(len(c) > 1 for c in classes)
                # Check connectedness of each equality class in original edges.
                for c in classes:
                    seen = {min(c)}
                    while True:
                        nxt = seen | {j for i, j in edges if i in seen and j in c} | {
                            i for i, j in edges if j in seen and i in c}
                        if nxt == seen:
                            break
                        seen = nxt
                    assert seen == c
                reps = [min(c) for c in classes]
                for a, b in combinations(range(len(classes)), 2):
                    i, j = reps[a], reps[b]
                    if (i, j) in reach or (j, i) in reach:
                        continue
                    base = {k for k, rep in enumerate(reps)
                            if (i, rep) in reach or (j, rep) in reach} - {a, b}
                    for extra in (set(), {a}, {b}, {a, b}):
                        ones = set().union(*(classes[k] for k in base | extra))
                        ones |= {k for k in range(n) if unary[k] == {1}}
                        x = sum(1 << k for k in ones)
                        assert x in S
                    witness_count += 1
        result.append(dict(n=n, nonempty_lattices=len(lattices), graphs=1 << len(pairs),
                           feasible_graph_support_pairs=count, incomparable_squares=witness_count,
                           pinned_pairs=pin_cases, tied_pairs=ties))
    return result

def exact_examples():
    n = 4
    bit = lambda x, i: x >> i & 1
    S = [x for x in range(16) if bit(x, 0) == bit(x, 1) and bit(x, 2) == bit(x, 3)]
    w = [Q(2) ** (-2 * bit(x, 0) * bit(x, 2) + 3 * bit(x, 1) * bit(x, 3))
         if x in S else Q(0) for x in range(16)]
    assert mtp(w, 4) and sum(w) == 5
    p = [z / sum(w) for z in w]
    eps = Q(1, 16)
    naive = [Q(2) ** (-2 * bit(x, 0) * bit(x, 2) + 3 * bit(x, 1) * bit(x, 3)) *
             eps ** ((bit(x, 0) != bit(x, 1)) + (bit(x, 2) != bit(x, 3))) for x in range(16)]
    x, y = 1, 4
    assert naive[x & y] * naive[x | y] < naive[x] * naive[y]
    errors = []
    for k in (1, 2, 4, 8):
        q = [Q(2) ** (bit(x, 0) * bit(x, 2)) * Q(1, 2 ** k) **
             ((bit(x, 0) != bit(x, 1)) + (bit(x, 2) != bit(x, 3))) for x in range(16)]
        q = [z / sum(q) for z in q]
        assert mtp(q, 4)
        errors.append(dict(k=k, l1=str(sum(abs(a - b) for a, b in zip(p, q)))))
    # The previously published four-cycle law, bit i corresponds to manuscript x_(i+1).
    c4 = [Q(2 if x == 15 else 1, 9) if bit(x, 2) == bit(x, 3) else Q(0)
          for x in range(16)]
    assert mtp(c4, 4)
    edges = [(0, 1), (1, 2), (2, 3), (0, 3)]
    lhs, rhs = [0, 14, 13, 3], [12, 2, 1, 15]
    for i, j in edges:
        assert sorted((bit(x, i), bit(x, j)) for x in lhs) == sorted(
            (bit(x, i), bit(x, j)) for x in rhs)
    mult = lambda arr: __import__('functools').reduce(lambda a, b: a * b, arr, Q(1))
    assert mult(c4[x] for x in lhs) != mult(c4[x] for x in rhs)
    # Check all disjoint nonempty separated A,B and every conditioned marginal minor.
    sep_count = minors = 0
    for A in range(1, 16):
        for B in range(1, 16):
            if A & B:
                continue
            for C in range(16):
                if C & (A | B):
                    continue
                reached = A
                while True:
                    nxt = reached
                    for i, j in edges:
                        if reached >> i & 1 and not C >> j & 1:
                            nxt |= 1 << j
                        if reached >> j & 1 and not C >> i & 1:
                            nxt |= 1 << i
                    if nxt == reached:
                        break
                    reached = nxt
                if reached & B:
                    continue
                sep_count += 1
                av, bv, cv = sorted({x & A for x in range(16)}), sorted({x & B for x in range(16)}), sorted({x & C for x in range(16)})
                for c in cv:
                    mass = {(a, b): sum(c4[x] for x in range(16)
                                       if (x & A, x & B, x & C) == (a, b, c))
                            for a in av for b in bv}
                    for a, aa in combinations(av, 2):
                        for b, bb in combinations(bv, 2):
                            assert mass[a, b] * mass[aa, bb] == mass[a, bb] * mass[aa, b]
                            minors += 1
    # Attraction cannot be omitted from a finite-factor closure statement.
    antiferro = [Q(0) if x in (0, 7) else Q(1, 6) for x in range(8)]
    assert not mtp(antiferro, 3)
    assert all({(x >> i & 1, x >> j & 1) for x in range(8) if antiferro[x]} ==
               set(product((0, 1), repeat=2)) for i, j in combinations(range(3), 2))
    # Compact local factors alone do not protect a normalizer from collapsing.
    collapse = [dict(k=k, bounded_entries=[str(Q(1, 2**k)), str(Q(1, 2**k))],
                     normalizer=str(Q(2, 2**k)), probability=["1/2", "1/2"])
                for k in (1, 4, 16)]
    return dict(tied_support=S, tied_probability=[str(v) for v in p],
                naive_smoothing_ratio=str(naive[0] * naive[5] / (naive[1] * naive[4])),
                attractive_errors=errors, c4_mtp_pairs=256, c4_separations=sep_count,
                c4_conditional_minors=minors, c4_quartic=[str(mult(c4[x] for x in side)) for side in (lhs, rhs)],
                nonattractive_limit_not_mtp=True, normalizer_collapse_control=collapse)

def residual_controls():
    cases = cuts = reverse_flow_cases = wrong_reverse_rejections = 0
    for n in range(1, 5):
        pairs = list(combinations(range(n), 2))
        for graph in range(1 << len(pairs)):
            edges = [e for k, e in enumerate(pairs) if graph >> k & 1]
            for seed in range(12):
                h = [Q(((seed + 2) * (i + 3)) % 9 - 4, 3) for i in range(n)]
                J = {e: Q((seed + 3 * k) % 6, 2) for k, e in enumerate(edges)}
                if seed == 0:
                    h, J = [Q(0)] * n, {e: Q(0) for e in edges}
                s, t, N = n, n + 1, n + 2
                c = [[Q(0) for _ in range(N)] for _ in range(N)]
                b = [-v for v in h]
                for k, (a, z) in enumerate(edges):
                    i, j = (a, z) if (seed + k) % 2 else (z, a)
                    c[i][j] += J[a, z]
                    b[i] -= J[a, z]
                for i in range(n):
                    if b[i] >= 0:
                        c[i][t] = b[i]
                    else:
                        c[s][i] = -b[i]
                r = [row[:] for row in c]
                value = Q(0)
                while True:
                    parent = {s: None}
                    queue = deque([s])
                    while queue and t not in parent:
                        u = queue.popleft()
                        for v in range(N):
                            if r[u][v] > 0 and v not in parent:
                                parent[v] = u
                                queue.append(v)
                    if t not in parent:
                        break
                    path, v = [], t
                    while v != s:
                        u = parent[v]
                        path.append((u, v))
                        v = u
                    delta = min(r[u][v] for u, v in path)
                    for u, v in path:
                        r[u][v] -= delta
                        r[v][u] += delta
                    value += delta
                f = [[max(Q(0), c[u][v] - r[u][v]) for v in range(N)] for u in range(N)]
                assert all(0 <= f[u][v] <= c[u][v] and
                           r[u][v] == c[u][v] - f[u][v] + f[v][u]
                           for u in range(N) for v in range(N))
                assert all(sum(f[i]) == sum(f[u][i] for u in range(N)) for i in range(n))
                E = [-sum(h[i] * (x >> i & 1) for i in range(n)) -
                     sum(J[i, j] * (x >> i & 1) * (x >> j & 1) for i, j in edges)
                     for x in range(1 << n)]
                cut_values = []
                wrong_detected = False
                reverse_flow_cases += any(r[u][v] > 0 and c[u][v] == 0 for u in range(n) for v in range(n))
                for x in range(1 << n):
                    U = {s} | {i for i in range(n) if x >> i & 1}
                    C = sum(c[u][v] for u in U for v in range(N) if v not in U)
                    R = sum(r[u][v] for u in U for v in range(N) if v not in U)
                    wrong = sum(c[u][v] - f[u][v] - f[v][u]
                                for u in U for v in range(N) if v not in U)
                    assert R == C - value == E[x] - min(E)
                    wrong_detected |= wrong != R
                    cut_values.append(C)
                    cuts += 1
                assert min(cut_values) == value
                assert len({cut_values[x] - E[x] for x in range(1 << n)}) == 1
                wrong_reverse_rejections += wrong_detected
                cases += 1
    return dict(networks=cases, all_cut_equalities=cuts,
                cases_with_internal_reverse_residual=reverse_flow_cases,
                wrong_minus_reverse_formula_rejected=wrong_reverse_rejections,
                capacities="exact nonnegative rationals; both orientations, zeros, signed fields")

if __name__ == '__main__':
    target = Path(sys.argv[1]).resolve()
    assert target.parent == Path(__file__).resolve().parent
    result = dict(status="PASS", limitations="Finite diagnostics only; universal proof separately reconstructed.",
                  support_geometry=support_geometry(), examples=exact_examples(), residual=residual_controls(),
                  elapsed_seconds=round(time.time() - START, 4),
                  driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
