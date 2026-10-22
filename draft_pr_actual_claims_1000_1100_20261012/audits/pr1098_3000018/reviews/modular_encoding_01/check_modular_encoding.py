#!/usr/bin/env python3
"""Fresh exact finite diagnostics. No candidate executable is imported.

All proof obligations use explicit exceptions, so -O retains checks.
The global CRT period is computed only by these bounded diagnostics, never
by the reduction constructor. No finite result certifies the universal proof.
"""
import collections
import hashlib
import itertools
import json
import math
import pathlib
import random


def need(condition, label):
    if not condition:
        raise ValueError(label)


def bank(q, allowed):
    allowed = set(allowed)
    need(q >= 2 and all(0 <= a < q for a in allowed), "bank input")
    h = lambda k: int(k % q in allowed)
    multiplicities = [1 + h(-a - 1) - h(-a) for a in range(q)]
    offsets = [a for a, c in enumerate(multiplicities) for _ in range(c)]
    return offsets, multiplicities, q * (q - 1) // 2 - len(allowed)


def primes(n):
    found = []
    candidate = 3
    while len(found) < n:
        if all(candidate % d for d in range(2, math.isqrt(candidate) + 1)):
            found.append(candidate)
        candidate += 1
    return found


def normalize(formula):
    clauses = []
    for clause in formula:
        vals = set(clause)
        need(all(isinstance(a, int) and a for a in vals), "literal input")
        if any(-a in vals for a in vals):
            continue
        if not vals:
            return False, [], []
        need(len(vals) <= 3, "three literal restriction")
        clauses.append(tuple(sorted(vals)))
    names = sorted({abs(a) for clause in clauses for a in clause})
    mapping = {name: i + 1 for i, name in enumerate(names)}
    relabeled = [tuple(mapping[abs(a)] * (1 if a > 0 else -1) for a in clause)
                 for clause in clauses]
    return True, names, relabeled


def sat_truth(formula):
    names = sorted({abs(a) for c in formula for a in c})
    for bits in itertools.product((0, 1), repeat=len(names)):
        truth = dict(zip(names, bits))
        if all(any(bool(truth[abs(a)]) == (a > 0) for a in c) for c in formula):
            return True
    return False


def reduction(formula, oriented=False):
    valid, names, clauses = normalize(formula)
    if not valid or not clauses:
        size = 3 if oriented else 2
        adj = [[(i + 1) % size] for i in range(size)]
        return {"adj": adj, "chips": [int(not valid)] + [0] * (size - 1),
                "banks": [], "counter_data": [], "Q": 1, "P": 0,
                "trivial": True, "clauses": clauses, "names": names}
    ps = primes(len(names))
    banks = [(p, {0, 1}) for p in ps]
    for clause in clauses:
        ids = sorted({abs(a) - 1 for a in clause})
        q = math.prod(ps[i] for i in ids)
        # Independent residue scan, not the report's local CRT implementation.
        allowed = set()
        for residue in range(q):
            bits = {i + 1: residue % ps[i] for i in ids}
            if all(bit in (0, 1) for bit in bits.values()):
                if any(bool(bits[abs(a)]) == (a > 0) for a in clause):
                    allowed.add(residue)
        need(len(allowed) == 2 ** len(ids) - 1, "clause predicate cardinality")
        banks.append((q, allowed))
    Q = sum(q for q, _ in banks)
    P = max(q for q, _ in banks)
    num_returns = P if oriented else P - 1
    adj = [[] for _ in range(1 + Q + num_returns)]
    counter_data = []
    next_v = 1
    B = 0
    for q, allowed in banks:
        offsets, _, K = bank(q, allowed)
        B += K + q
        for offset in offsets:
            adj[0].append(next_v)
            adj[next_v] = ([] if oriented else [0]) + list(range(Q + 1, Q + 1 + q - (0 if oriented else 1)))
            counter_data.append((next_v, q, offset))
            next_v += 1
    for v in range(Q + 1, len(adj)):
        adj[v] = [0]
    chips = [0] * len(adj)
    for v, _, offset in counter_data:
        chips[v] = offset
    C = Q + B - 1
    chips[0] = C - sum(chips)
    return {"adj": adj, "chips": chips, "banks": banks,
            "counter_data": counter_data, "Q": Q, "P": P,
            "B": B, "C": C, "trivial": False,
            "clauses": clauses, "names": names}


def reachable(adj, start):
    seen = {start}
    pending = [start]
    while pending:
        for v in adj[pending.pop()]:
            if v not in seen:
                seen.add(v)
                pending.append(v)
    return seen


def graph_checks(g, oriented):
    adj = g["adj"]
    N = len(adj)
    need(all(adj), "positive outdegrees")
    need(all(v not in row and len(row) == len(set(row)) for v, row in enumerate(adj)), "loop/parallel arc")
    need(all(len(reachable(adj, v)) == N for v in range(N)), "strong connectivity")
    need(all(not adj[w] or all(z == 0 for z in adj[w])
             for v in range(1, N) for w in adj[v] if w != 0), "root-free depth")
    if oriented:
        need(all(v not in adj[w] for v, row in enumerate(adj) for w in row), "antiparallel arc")
    need(min(g["chips"]) >= 0, "nonnegative chips")
    if not g["trivial"]:
        Q, P = g["Q"], g["P"]
        need(N == Q + P + int(oriented), "vertex formula")
        E = sum(map(len, adj))
        need(E == Q + sum(q * q for q, _ in g["banks"]) + P - 1 + int(oriented), "arc formula")
        need(sum(g["chips"]) == g["C"], "total chips")
        need(E - N - g["C"] == sum(q * (q - 3) // 2 + len(a) for q, a in g["banks"]), "stable capacity")
        need(g["C"] <= Q + sum(q * (q + 1) // 2 for q, _ in g["banks"]), "polynomial chip bound")


def fire(adj, chips, v):
    need(chips[v] >= len(adj[v]), "illegal firing")
    chips[v] -= len(adj[v])
    for w in adj[v]:
        chips[w] += 1


def certificate(adj, x, f):
    if len(f) != len(adj) or any(type(a) is not int or a < 0 for a in f):
        return False
    z = list(x)
    for v, row in enumerate(adj):
        z[v] -= len(row) * f[v]
        for w in row:
            z[w] += f[v]
    return all(0 <= a < len(row) for a, row in zip(z, adj))


def canonical(g):
    adj, chips = g["adj"], list(g["chips"])
    f = [0] * len(adj)
    k = 0
    checkpoints = 0
    period = math.lcm(*(q for q, _ in g["banks"])) if g["banks"] else len(adj)
    initial = tuple(chips)
    while True:
        checkpoints += 1
        if not g["trivial"]:
            for v, q, offset in g["counter_data"]:
                need(chips[v] == (offset + k) % q, "counter checkpoint")
            need(all(chips[v] == 0 for v in range(g["Q"] + 1, len(adj))), "relay checkpoint")
            S = sum(K + q * int(k % q in allowed)
                    for q, allowed in g["banks"] for K in [q * (q - 1) // 2 - len(allowed)])
            need(chips[0] == g["C"] - S, "root checkpoint")
            need((chips[0] < len(adj[0])) == all(k % q in a for q, a in g["banks"]), "threshold equivalence")
        if all(chips[v] < len(row) for v, row in enumerate(adj)):
            need(certificate(adj, g["chips"], f), "terminal certificate")
            return True, sum(f), checkpoints, f
        if k >= period:
            need(tuple(chips) == initial, "one-period legal lasso")
            return False, sum(f), checkpoints, f
        fire(adj, chips, 0)
        f[0] += 1
        for v in range(1, len(adj)):
            while chips[v] >= len(adj[v]):
                fire(adj, chips, v)
                f[v] += 1
        k += 1


def arbitrary(g, chooser, seed):
    adj, chips = g["adj"], list(g["chips"])
    counts = [0] * len(adj)
    seen = set()
    rng = random.Random(seed)
    while True:
        state = tuple(chips)
        if state in seen:
            return False, sum(counts), counts
        seen.add(state)
        legal = [v for v, row in enumerate(adj) if chips[v] >= len(row)]
        if not legal:
            need(certificate(adj, g["chips"], counts), "arbitrary certificate")
            return True, sum(counts), counts
        v = min(legal) if chooser == "min" else max(legal) if chooser == "max" else rng.choice(legal)
        fire(adj, chips, v)
        counts[v] += 1


def compositions(total, n):
    if n == 1:
        yield (total,)
    else:
        for a in range(total + 1):
            for rest in compositions(total - a, n - 1):
                yield (a,) + rest


def tree_counts(adj):
    N = len(adj)
    counts = []
    for root in range(N):
        nonroots = [v for v in range(N) if v != root]
        count = 0
        for choices in itertools.product(*(adj[v] for v in nonroots)):
            parents = dict(zip(nonroots, choices))
            good = True
            for v in nonroots:
                visited = set()
                while v != root and v not in visited:
                    visited.add(v)
                    v = parents[v]
                good &= v == root
            count += good
        counts.append(count)
    return counts


def generic_certificates():
    totals = collections.Counter()
    for N in (2, 3):
        pairs = [(v, w) for v in range(N) for w in range(N) if v != w]
        for mask in range(1 << len(pairs)):
            adj = [[] for _ in range(N)]
            for i, (v, w) in enumerate(pairs):
                if mask >> i & 1:
                    adj[v].append(w)
            if not all(adj) or any(len(reachable(adj, v)) != N for v in range(N)):
                continue
            totals["graphs"] += 1
            trees = tree_counts(adj)
            divisor = math.gcd(*trees)
            pi = [a // divisor for a in trees]
            need(min(pi) >= 1 and max(pi) <= (N - 1) ** (N - 1), "primitive tree bound")
            balance = [len(adj[v]) * pi[v] - sum(pi[u] for u in range(N) if v in adj[u]) for v in range(N)]
            need(not any(balance), "tree kernel orientation")
            capacity = sum(map(len, adj)) - N
            for total in range(capacity + 2):
                for x in compositions(total, N):
                    totals["configurations"] += 1
                    pending = collections.deque([x])
                    odometers = {x: (0,) * N}
                    edges = []
                    terminals = []
                    while pending:
                        state = pending.popleft()
                        f = odometers[state]
                        legal = [v for v in range(N) if state[v] >= len(adj[v])]
                        if not legal:
                            terminals.append((state, f))
                        for v in legal:
                            y = list(state)
                            fire(adj, y, v)
                            nxt = tuple(y)
                            fc = list(f)
                            fc[v] += 1
                            edges.append((state, nxt, tuple(fc)))
                            if nxt not in odometers:
                                odometers[nxt] = tuple(fc)
                                pending.append(nxt)
                    totals["reachable_states"] += len(odometers)
                    if terminals:
                        totals["halting_configurations"] += 1
                        need(len(terminals) == 1, "stable uniqueness")
                        z, f = terminals[0]
                        need(certificate(adj, x, f), "generic certificate")
                        need(any(a < b for a, b in zip(f, pi)), "least-action period subtraction")
                        need(all(a + 1 <= (N - 1) ** (2 * N - 2) for a in f), "explicit bit bound")
                        need(all(all(a <= b for a, b in zip(g, f)) for g in odometers.values()), "least-action prefix count")
                        need(all(odometers[nxt] == fc for _, nxt, fc in edges), "legal cycle in halting case")
                        for u, row in enumerate(adj):
                            for v in row:
                                need(f[u] + 1 <= len(adj[v]) * (f[v] + 1), "arc-path slack")
    return dict(totals)


def expect_rejection(fn, label):
    try:
        fn()
    except ValueError:
        return label
    raise ValueError("negative control not rejected: " + label)


def main():
    summary = {"checker_schema": 1, "historical_replay": False,
               "scope": "Fresh exact bounded diagnostics supplement independent universal derivation."}
    stats = collections.Counter()
    for q in range(2, 12):
        for mask in range(1 << q):
            allowed = {a for a in range(q) if mask >> a & 1}
            offsets, cs, K = bank(q, allowed)
            need(len(offsets) == q and sum(cs) == q and set(cs) <= {0, 1, 2}, "counter multiplicities")
            stats["sets"] += 1
            stats["empty_sets"] += not allowed
            stats["full_sets"] += len(allowed) == q
            stats["sets_with_multiplicity_two"] += 2 in cs
            for k in range(-q - 2, 2 * q + 3):
                S = sum((a + k) % q for a in offsets)
                need(S == K + q * int(k % q in allowed), "bank identity")
                if allowed:
                    need((S == K + q) == (k % q in allowed), "maximum predicate")
                stats["positions"] += 1
    summary["banks"] = dict(stats)
    prime_sample = primes(256)
    need(len(set(prime_sample)) == 256 and prime_sample[0] == 3, "distinct prime sample")
    need(all(p <= 3 * (i + 2) ** 2 for i, p in enumerate(prime_sample)), "integer polynomial prime bound")
    summary["prime_bound_samples"] = {"first_primes_starting_at_three": 256,
                                       "largest": prime_sample[-1],
                                       "bound": "p_(n+1) <= 3(n+1)^2; finite diagnostic only"}
    # CRT reconstruction is checked separately against independent residue scans.
    crt_checks = 0
    ps = primes(3)
    for size in range(1, 4):
        for ids in itertools.combinations(range(3), size):
            moduli = [ps[i] for i in ids]
            M = math.prod(moduli)
            for bits in itertools.product((0, 1), repeat=size):
                k = sum(b * (M // p) * pow(M // p, -1, p) for b, p in zip(bits, moduli)) % M
                need(all(k % p == b for p, b in zip(moduli, bits)), "CRT forward")
                need([a for a in range(M) if all(a % p == b for p, b in zip(moduli, bits))] == [k], "CRT unique local representative")
                crt_checks += 1
    summary["local_crt_assignments"] = crt_checks
    base_clauses = [(1,), (-1,), (2,), (-2,), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    formulas = [[base_clauses[i] for i in range(8) if mask >> i & 1] for mask in range(256)]
    formulas += [[], [()], [(1, 1)], [(1, -1)], [(1, 1, 2), (-1, -1)],
                 [(10 ** 100,), (-7,)], [(1, 2, 3)],
                 [(1,), (-1,)], [(1, 2, 3), (-1,), (-2,), (-3,)]]
    for bits in itertools.product((0, 1), repeat=3):
        formulas.append([(i + 1 if b else -i - 1,) for i, b in enumerate(bits)])
    formulas.append([tuple(i + 1 if b else -i - 1 for i, b in enumerate(bits))
                     for bits in itertools.product((0, 1), repeat=3)])
    graph_stats = collections.Counter()
    samples = []
    for index, formula in enumerate(formulas):
        truth = sat_truth(formula)
        for oriented in (False, True):
            g = reduction(formula, oriented)
            graph_checks(g, oriented)
            halted, firings, checkpoints, f = canonical(g)
            need(halted == truth, "SAT/full graph equivalence")
            graph_stats["cases"] += 1
            graph_stats["oriented_cases"] += oriented
            graph_stats["sat_cases"] += truth
            graph_stats["unsat_cases"] += not truth
            graph_stats["individual_firings"] += firings
            graph_stats["checkpoints"] += checkpoints
            graph_stats["maximum_vertices"] = max(graph_stats["maximum_vertices"], len(g["adj"]))
            graph_stats["maximum_arcs"] = max(graph_stats["maximum_arcs"], sum(map(len, g["adj"])))
            if index in (0, 1, 7, 63, 127, 255, 258, 270):
                samples.append((g, truth, f, index, oriented))
    summary["full_graph"] = dict(graph_stats)
    schedules = collections.Counter()
    for g, truth, canonical_f, index, oriented in samples:
        for chooser in ("min", "max", "random"):
            halted, firings, f = arbitrary(g, chooser, index + 1000 * oriented)
            need(halted == truth, "arbitrary order outcome")
            if truth:
                need(f == canonical_f, "order-independent odometer")
            schedules["cases"] += 1
            schedules["individual_firings"] += firings
    summary["arbitrary_schedules"] = dict(schedules)
    summary["generic_membership"] = generic_certificates()
    negatives = []
    q, A = 5, {0, 2}
    h = lambda k: int(k % q in A)
    for name, cs in [("reversed difference", [1 - h(-a - 1) + h(-a) for a in range(q)]),
                     ("shifted index", [1 + h(-a + 1) - h(-a) for a in range(q)])]:
        negatives.append(expect_rejection(lambda cs=cs: need(all(sum(c * ((a + k) % q) for a, c in enumerate(cs)) == q * (q - 1) // 2 - len(A) + q * h(k) for k in range(q)), name), name))
    offsets, _, K = bank(q, A)
    negatives.append(expect_rejection(lambda: need(sum(offsets) == q * (q - 1) // 2 + q * h(0), "omitted allowed-set constant"), "omitted allowed-set constant"))
    negatives.append(expect_rejection(lambda: need(len(set(offsets)) == q, "collapsed multiplicity-two counters"), "collapsed multiplicity-two counters"))
    g = reduction([(1,), (-1,)], False)
    g["adj"][0].append(g["adj"][0][0])
    negatives.append(expect_rejection(lambda: graph_checks(g, False), "parallel root arc"))
    g = reduction([(1,)], True)
    g["adj"][1].append(0)
    negatives.append(expect_rejection(lambda: graph_checks(g, True), "oriented counter-to-root fault"))
    g = reduction([(1,)], False)
    g["chips"][0] += 1
    g["C"] += 1
    negatives.append(expect_rejection(lambda: canonical(g), "one excess root chip"))
    g = reduction([(1,), (-1,)], False)
    g["chips"][0] -= 3
    g["C"] -= 3
    negatives.append(expect_rejection(lambda: canonical(g), "three missing root chips"))
    original = [(1,), (-1,)]
    wrong_sign_graph = reduction([(1,), (1,)], False)
    negatives.append(expect_rejection(lambda: need(canonical(wrong_sign_graph)[0] == sat_truth(original), "erased negative literal"), "erased negative literal"))
    negatives.append(expect_rejection(lambda: need(certificate([[1], [0]], [1, 0], [0, 0]), "invalid certificate"), "invalid certificate"))
    negatives.append(expect_rejection(lambda: normalize([(0,)]), "zero literal"))
    slack_adj = [[1, 2], [0, 2], [0, 1]]
    need(certificate(slack_adj, [2, 0, 0], [1, 0, 0]), "slack witness really halts")
    negatives.append(expect_rejection(lambda: need(1 <= len(slack_adj[1]) * 0, "omitted additive path slack"), "omitted additive path slack"))
    summary["negative_controls"] = negatives
    summary["all_checks_passed"] = True
    summary["checker_sha256"] = hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    print(json.dumps(summary, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
