#!/usr/bin/env python3
"""Independent finite checks of family 113's cells and signed identity.

This is a proof-device test, not an FPRAS implementation or certificate.
Only Python standard-library modules are used; no upstream code is imported.
"""
import collections
import hashlib
import itertools
import json
import random
from pathlib import Path


def edge(a, b, color):
    assert a != b
    return (min(a, b), max(a, b), color)


def matching(es, n):
    es = tuple(sorted(es))
    assert len(es) == n // 2
    counts = collections.Counter(v for e in es for v in e[:2])
    assert counts == collections.Counter(range(n)), (es, counts)
    return es


def f(es):
    # An arbitrary deterministic function on colored perfect matchings.
    return int.from_bytes(hashlib.sha256(repr(tuple(sorted(es))).encode()).digest()[:4], 'big') % 101 - 50


def run_cycle(labels):
    n = len(labels)
    S = [set((labels[(v - 1) % n], labels[v])) for v in range(n)]

    def arc(a, b):
        out = [a]
        while out[-1] != b:
            out.append((out[-1] + 1) % n)
        return out

    def admissible(J):
        return bool(S[J[0]] & S[J[-1]]) and (len(J) - 1) % 2 == 1

    def good(J):
        return len(J) == 2 or bool(S[J[1]] & S[J[-2]])

    cells = []

    def recurse(J):
        s = len(J) - 1
        assert admissible(J)
        if s == 1:
            return
        P = min(S[J[0]] & S[J[-1]])
        direction = 1 if J[1] == (J[0] + 1) % n else -1
        ext = [J[-1]]
        while ext[-1] != J[0]:
            ext.append((ext[-1] + direction) % n)
        # These recursive arcs may run in either cyclic direction after reversal.
        a = [labels[J[i]] if J[i + 1] == (J[i] + 1) % n else labels[J[i + 1]] for i in range(s)]
        if good(ext):
            if P not in a:
                assert a[0] == a[-1]
                P = a[0]
            odd = [i for i, lab in enumerate(a) if lab == P and i % 2]
            if odd:
                p1, p2 = odd[0], odd[0] + 1
            else:
                pos = [i for i, lab in enumerate(a) if lab == P]
                if pos[0] > 0:
                    p1, p2 = pos[0] - 1, pos[0]
                elif pos[-1] < s - 1:
                    p1, p2 = pos[-1] + 1, pos[-1] + 2
                else:
                    p1, p2 = 1, s - 1
        else:
            # Compute the true complementary arc in J's current direction.
            if P in S[ext[-2]]:
                J = list(reversed(J))
                a = list(reversed(a))
            assert a[0] == P
            if a[-1] == P:
                p1, p2 = 1, s - 1
            else:
                t = max(i for i, lab in enumerate(a) if lab == P) + 1
                p1, p2 = (1, t) if t % 2 == 0 else (t, s - 1)
        assert 0 < p1 < p2 < s and p1 % 2 and p2 % 2 == 0
        parts = [J[:p1 + 1], J[p1:p2 + 1], J[p2:]]
        # Convert the cell's corners back to clockwise order, and use full-cycle arcs.
        corners = sorted((J[0], J[p1], J[p2], J[-1]))
        sides = [arc(corners[i], corners[(i + 1) % 4]) for i in range(4)]
        assert all(admissible(A) for A in sides)
        gp = [good(A) for A in sides]
        assert (gp[0] and gp[2]) or (gp[1] and gp[3])
        for k in (0, 1):
            if len(sides[k]) > 2 and len(sides[k + 2]) > 2:
                assert gp[1 - k] and gp[3 - k]
        cells.append(sides)
        for child in parts:
            recurse(child)

    recurse(list(range(n)))
    assert len(cells) == (n - 2) // 2
    chord_colors = {}

    def patterns(J):
        T = [edge(J[i], J[i + 1], labels[J[i]]) for i in range(0, len(J) - 1, 2)]
        N = [edge(J[i], J[i + 1], labels[J[i]]) for i in range(1, len(J) - 1, 2)]
        key = tuple(sorted((J[0], J[-1])))
        color = labels[J[0]] if len(J) == 2 else chord_colors.setdefault(key, min(S[J[0]] & S[J[-1]]))
        return set(T), set(N) | {edge(*key, color)}

    O = [set(edge(i, (i + 1) % n, labels[i]) for i in range(k, n, 2)) for k in (0, 1)]
    for es in O:
        matching(es, n)
    total = 0
    encoded = 0
    for sides in cells:
        pats = [patterns(J) for J in sides]
        which = [0 if T <= O[0] else 1 for T, C in pats]
        assert which[0] == which[2] and which[1] == which[3] and which[0] != which[1]
        A = []
        E = []
        for k in (0, 1):
            indexes = [i for i in range(4) if which[i] == k]
            Y, X = indexes
            Ty, Cy = pats[Y]
            Tx, Cx = pats[X]
            H_y = O[k] - Ty | Cy
            H_x = O[k] - Tx | Cx
            A_k = H_y - Tx | Cx
            for M in (H_y, H_x, A_k):
                matching(M, n)
            E.append((f(H_y) - f(A_k)) - (f(O[k]) - f(H_x)))
            A.append(A_k)
            assert len(A[0] ^ A_k) <= 4 if k else True
            if len(sides[X]) == 2 or len(sides[Y]) == 2:
                assert E[-1] == 0
        assert len(A[0] - A[1]) == 2 and len(A[1] - A[0]) == 2
        delta = f(A[0]) - f(A[1])
        gains = [f(O[which[i]]) - f(O[which[i]] - T | C) for i, (T, C) in enumerate(pats)]
        assert f(O[0]) - f(O[1]) == delta + sum(g if w == 0 else -g for g, w in zip(gains, which)) + E[0] - E[1]
        total += delta + E[0] - E[1]

        def repair(B, indexes):
            for i in indexes:
                J = sides[i]
                assert good(J)
                B.remove(edge(J[0], J[1], labels[J[0]]))
                if len(J) > 2:
                    B.remove(edge(J[-2], J[-1], labels[J[-2]]))
                    B.add(edge(J[1], J[-2], min(S[J[1]] & S[J[-2]])))
            return B

        def check_union(Aout, Bout):
            matching(Aout, n); matching(Bout, n)
            source = collections.Counter(O[0]) + collections.Counter(O[1])
            target = collections.Counter(Aout) + collections.Counter(Bout)
            added, dropped = target - source, source - target
            assert sum(added.values()) == sum(dropped.values()) <= 4
            assert target - added + dropped == source
            return target

        selected = next(pair for pair in ([0, 2], [1, 3]) if all(good(sides[i]) for i in pair))
        B = repair(set().union(*(T for T, C in pats)), selected)
        check_union(A[0], B); encoded += 1
        for k in (0, 1):
            ix = [i for i in range(4) if which[i] == k]
            if all(len(sides[i]) > 2 for i in ix):
                Y, X = ix; other = [i for i in range(4) if which[i] != k]
                B0 = set(O[1 - k])
                for i in ix:
                    B0.add(next(e for e in pats[i][1] if e not in pats[i][0] and e[:2] == tuple(sorted((sides[i][0], sides[i][-1])))))
                B0 = repair(B0, other)
                assert pats[X][1] <= B0
                u0 = check_union(O[k], B0)
                Ty, Cy = pats[Y]
                A1 = O[k] - Ty | Cy
                B1 = B0 - Cy | Ty
                assert pats[X][1] <= B1
                assert check_union(A1, B1) == u0
                encoded += 2
    assert total == f(O[0]) - f(O[1])
    return len(cells), encoded


def sequences(adj, n):
    for start in range(len(adj)):
        def rec(a):
            if len(a) == n:
                if start in adj[a[-1]]:
                    yield tuple(a)
                return
            for v in sorted(adj[a[-1]]):
                yield from rec(a + [v])
        yield from rec([start])


def main():
    graphs = [({0, 1}, {0, 1, 2}, {1, 2}), ({0, 1, 2, 3}, {0, 1}, {0, 2}, {0, 3})]
    tested = cells = encodings = 0
    for adj in graphs:
        for n in (4, 6, 8):
            for a in sequences(adj, n):
                c, e = run_cycle(a)
                tested += 1; cells += c; encodings += e
    rng = random.Random(11305)
    for _ in range(6000):
        adj = rng.choice(graphs)
        n = rng.choice((10, 12, 14, 16, 20, 24))
        while True:
            a = [rng.randrange(len(adj))]
            for i in range(n - 1):
                a.append(rng.choice(sorted(adj[a[-1]])))
            if a[0] in adj[a[-1]]:
                break
        c, e = run_cycle(a)
        tested += 1; cells += c; encodings += e
    result = {'cycles_checked': tested, 'cells_checked': cells, 'encodings_checked': encodings,
              'seed': 11305, 'status': 'PASS',
              'limits': 'Finite proof-device checks only; no chain simulation, source compilation, or theorem certificate.'}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
