from collections import Counter

# Independent reconstruction; no source code imported.
def certify(tree, m):
    labs = tuple(sorted(tree))
    cnt = Counter()

    def check(labels):
        S = [frozenset((labels[(i - 1) % m], labels[i])) for i in range(m)]

        def good(J):
            return len(J) == 2 or bool(S[J[1]] & S[J[-2]])

        def ext(J):
            d = 1 if (J[1] - J[0]) % m == 1 else -1
            x = J[-1]
            E = [x]
            while x != J[0]:
                x = (x + d) % m
                E.append(x)
            return E

        cells = []

        def rec(J):
            s = len(J) - 1
            assert s % 2 == 1 and S[J[0]] & S[J[-1]]
            if s == 1:
                return
            P = min(S[J[0]] & S[J[-1]])
            a = [labels[J[i]] if (J[i + 1] - J[i]) % m == 1
                 else labels[J[i + 1]] for i in range(s)]
            E = ext(J)
            if good(E):
                if P not in a:
                    assert a[0] == a[-1]
                    P = a[0]
                odd = [i for i, v in enumerate(a) if v == P and i % 2]
                pos = [i for i, v in enumerate(a) if v == P]
                if odd:
                    p1, p2 = odd[0], odd[0] + 1
                elif pos[0] > 0:
                    p1, p2 = pos[0] - 1, pos[0]
                elif pos[-1] < s - 1:
                    p1, p2 = pos[-1] + 1, pos[-1] + 2
                else:
                    p1, p2 = 1, s - 1
            else:
                if P in S[E[-2]]:
                    assert P not in S[E[1]]
                    J = list(reversed(J))
                    E = ext(J)
                    a = [labels[J[i]] if (J[i + 1] - J[i]) % m == 1
                         else labels[J[i + 1]] for i in range(s)]
                assert a[0] == P
                if a[-1] == P:
                    p1, p2 = 1, s - 1
                else:
                    t = max(i for i, v in enumerate(a) if v == P) + 1
                    if t % 2 == 0:
                        p1, p2 = 1, t
                    else:
                        p1, p2 = t, s - 1
            assert 0 < p1 < p2 < s and p1 % 2 and not p2 % 2
            arcs = [J[:p1 + 1], J[p1:p2 + 1], J[p2:], E]
            assert all((len(X) - 1) % 2 and S[X[0]] & S[X[-1]]
                       for X in arcs)
            gs = [good(X) for X in arcs]
            lng = [len(X) > 2 for X in arcs]
            assert (gs[0] and gs[2]) or (gs[1] and gs[3])
            assert not (lng[0] and lng[2]) or (gs[1] and gs[3])
            assert not (lng[1] and lng[3]) or (gs[0] and gs[2])
            cells.append(arcs)
            for X in arcs[:3]:
                rec(X)

        rec(list(range(m)))
        assert len(cells) == (m - 2) // 2
        cnt['walks'] += 1
        cnt['cells'] += len(cells)

        def pat(X):
            T = [tuple(sorted((X[i], X[i + 1])))
                 for i in range(0, len(X) - 1, 2)]
            N = [tuple(sorted((X[i], X[i + 1])))
                 for i in range(1, len(X) - 1, 2)]
            chord = tuple(sorted((X[0], X[-1])))
            C = N + [chord]
            return T, N, C, chord

        def pm(edges):
            degrees = Counter(v for edge in edges for v in edge)
            assert len(edges) == m // 2 and all(degrees[v] == 1
                                               for v in range(m))

        for arcs in cells:
            patterns = [pat(X) for X in arcs]
            for pair in [(0, 2), (1, 3)]:
                pm([e for q, (_, N, _, chord) in enumerate(patterns)
                    for e in N + ([chord] if q in pair else [])])
            for pair in [(0, 2), (1, 3)]:
                if all(good(arcs[q]) for q in pair):
                    B = [e for T, _, _, _ in patterns for e in T]
                    for q in pair:
                        X = arcs[q]
                        T = patterns[q][0]
                        if len(X) == 2:
                            B.remove(T[0])
                        else:
                            B.remove(T[0])
                            B.remove(T[-1])
                            B.append(tuple(sorted((X[1], X[-2]))))
                    pm(B)
                    cnt['repairs'] += 1

    def walk(prefix):
        if len(prefix) == m:
            if prefix[-1] == prefix[0] or prefix[0] in tree[prefix[-1]]:
                check(prefix)
            return
        for nxt in (prefix[-1], *tree[prefix[-1]]):
            walk(prefix + [nxt])

    for first in labs:
        walk([first])
    return dict(cnt)


trees = {
    'path3': {0: (1,), 1: (0, 2), 2: (1,)},
    'star4': {0: (1, 2, 3), 1: (0,), 2: (0,), 3: (0,)},
    'fork5': {0: (1,), 1: (0, 2, 3), 2: (1, 4), 3: (1,), 4: (2,)}
}
for name, tree in trees.items():
    for m in [4, 6, 8, 10]:
        print(name, m, certify(tree, m))
print('ALL QUADRANGULATION AND REPAIR CHECKS PASSED')
