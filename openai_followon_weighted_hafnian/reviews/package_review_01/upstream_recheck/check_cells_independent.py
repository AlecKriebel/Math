"""Independent finite checks transcribed from the pinned primary proof.

No project verification implementation is imported. These checks test
cell construction, both guide encodings, and the signed identity. They
do not implement the upstream FPRAS or certify its asymptotic guarantee.
"""
from collections import Counter
from itertools import product
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
SOURCE = PROJECT / 'sources/preprints/A-Fully-Polynomial-Randomized-Approximation-Scheme-for-Perfect-Matchings-in-General-Graphs-September-23-2026/build/main.tex'


def edge(u, v, color):
    assert u != v
    return (min(u, v), max(u, v), color)


def inverse_tag_check(A, B, I1, I2, corner):
    """Reconstruct both input layers from output pair and permitted tag."""
    original, encoded = Counter(I1) + Counter(I2), Counter(A) + Counter(B)
    added, dropped = encoded - original, original - encoded
    restored = encoded.copy()
    restored.subtract(added)
    restored.update(dropped)
    incident = {}
    for e, multiplicity in (+restored).items():
        for v in e[:2]:
            incident.setdefault(v, []).extend([e] * multiplicity)
    assert all(len(es) == 2 for es in incident.values())
    first = next(e for e in I1 if corner in e[:2])
    orientation_bit = sorted(incident[corner]).index(first)
    e = sorted(incident[corner])[orientation_bit]
    v = corner
    recovered_layers = [set(), set()]
    active_vertices = {corner}
    steps = 0
    while True:
        recovered_layers[steps % 2].add(e)
        v = e[1] if v == e[0] else e[0]
        steps += 1
        if v == corner:
            break
        assert v not in active_vertices
        active_vertices.add(v)
        alternatives = [f for f in incident[v] if f != e]
        assert len(alternatives) == 1
        e = alternatives[0]
    assert steps >= 4 and steps % 2 == 0
    for j, output in enumerate((A, B)):
        recovered_layers[j].update(e for e in output if not (set(e[:2]) & active_vertices))
    assert recovered_layers[0] == set(I1)
    assert recovered_layers[1] == set(I2)


class Check:
    def __init__(self, labels, tree):
        self.labels = labels
        self.n = len(labels)
        self.tree = tree
        self.S = [{labels[(i - 1) % self.n], labels[i]} for i in range(self.n)]
        self.original = tuple(edge(i, (i + 1) % self.n, labels[i]) for i in range(self.n))
        self.O = [frozenset(self.original[0::2]), frozenset(self.original[1::2])]

    def common(self, u, v):
        return self.S[u] & self.S[v]

    def exterior(self, arc):
        direction = 1 if (arc[1] - arc[0]) % self.n == 1 else -1
        a = [arc[-1]]
        while a[-1] != arc[0]:
            a.append((a[-1] + direction) % self.n)
        return a

    def path_edge(self, u, v):
        i = u if (u + 1) % self.n == v else v
        assert (i + 1) % self.n in {u, v}
        return self.original[i]

    def chord(self, arc):
        return self.path_edge(*arc) if len(arc) == 2 else edge(arc[0], arc[-1], min(self.common(arc[0], arc[-1])))

    def good(self, arc):
        return len(arc) == 2 or bool(self.common(arc[1], arc[-2]))

    def split(self, arc):
        s = len(arc) - 1
        if s == 1:
            return []
        assert s % 2 == 1 and self.common(arc[0], arc[-1])
        P = min(self.common(arc[0], arc[-1]))
        ext = self.exterior(arc)
        a = [self.path_edge(arc[i], arc[i + 1])[2] for i in range(s)]
        if self.good(ext):
            if P not in a:
                assert a[0] == a[-1]
                P = a[0]
            odd = [i for i in range(1, s, 2) if a[i] == P]
            occurrences = [i for i, x in enumerate(a) if x == P]
            if odd:
                p1, p2 = odd[0], odd[0] + 1
            elif occurrences[0] > 0:
                p1, p2 = occurrences[0] - 1, occurrences[0]
            elif occurrences[-1] < s - 1:
                p1, p2 = occurrences[-1] + 1, occurrences[-1] + 2
            else:
                p1, p2 = 1, s - 1
        else:
            if P in self.S[ext[-2]]:
                assert P not in self.S[ext[1]]
                arc = list(reversed(arc))
                ext = self.exterior(arc)
                a = [self.path_edge(arc[i], arc[i + 1])[2] for i in range(s)]
            assert a[0] == P
            if a[-1] == P:
                p1, p2 = 1, s - 1
            else:
                t = max(i for i, x in enumerate(a) if x == P) + 1
                if t % 2 == 0:
                    p1, p2 = 1, t
                else:
                    p1, p2 = t, s - 1
        assert 0 < p1 < p2 < s and p1 % 2 == 1 and p2 % 2 == 0
        children = [arc[:p1 + 1], arc[p1:p2 + 1], arc[p2:]]
        cell = children + [ext]
        return [cell] + [c for child in children for c in self.split(child)]

    def patterns(self, arc):
        T = frozenset(self.path_edge(arc[i], arc[i + 1]) for i in range(0, len(arc) - 1, 2))
        N = frozenset(self.path_edge(arc[i], arc[i + 1]) for i in range(1, len(arc) - 1, 2))
        return T, N, N | {self.chord(arc)}

    def legal(self, M):
        counts = Counter(v for e in M for v in e[:2])
        assert len(M) == self.n // 2
        assert counts == Counter({v: 1 for v in range(self.n)})
        assert all(c in self.common(u, v) for u, v, c in M)

    def repair(self, union, arc):
        union = set(union)
        union.remove(self.path_edge(arc[0], arc[1]))
        if len(arc) > 2:
            union.remove(self.path_edge(arc[-2], arc[-1]))
            union.add(edge(arc[1], arc[-2], min(self.common(arc[1], arc[-2]))))
        return frozenset(union)

    def union_check(self, A, B):
        self.legal(A)
        self.legal(B)
        original = Counter(self.O[0]) + Counter(self.O[1])
        encoded = Counter(A) + Counter(B)
        added, dropped = encoded - original, original - encoded
        assert sum(added.values()) == sum(dropped.values()) <= 4
        restored = encoded.copy()
        restored.subtract(added)
        restored.update(dropped)
        assert +restored == original
        inverse_tag_check(A, B, self.O[0], self.O[1], 0)
        # Exercise unchanged outside cycles and a doubled identical edge.
        outside1 = frozenset(edge(u, v, 0) for u, v in ((100, 101), (102, 103), (104, 105), (200, 201)))
        outside2 = frozenset(edge(u, v, 0) for u, v in ((101, 102), (103, 104), (105, 100), (200, 201)))
        inverse_tag_check(A | outside1, B | outside2, self.O[0] | outside1, self.O[1] | outside2, 0)

    @staticmethod
    def f(M):
        # Deterministic arbitrary nonlinear function on perfect matchings.
        digest = hashlib.sha256(repr(sorted(M)).encode()).digest()
        return int.from_bytes(digest[:4], 'big') % 2003 - 1001

    def check(self):
        cells = self.split(list(range(self.n)))
        assert len(cells) == (self.n - 2) // 2
        total = 0
        errors = 0
        for cell in cells:
            assert all((len(J) - 1) % 2 == 1 and self.common(J[0], J[-1]) for J in cell)
            pairs = [[0, 2], [1, 3]]
            goodpairs = [p for p in pairs if all(self.good(cell[i]) for i in p)]
            assert goodpairs
            for p in pairs:
                if all(len(cell[i]) > 2 for i in p):
                    assert all(self.good(cell[i]) for i in set(range(4)) - set(p))
            patterns = [self.patterns(J) for J in cell]
            P = [i for i, (T, _, _) in enumerate(patterns) if T <= self.O[0]]
            Q = [i for i in range(4) if i not in P]
            assert P in pairs and Q in pairs
            base = frozenset().union(*(N for _, N, _ in patterns))
            AP = base | {self.chord(cell[i]) for i in P}
            AQ = base | {self.chord(cell[i]) for i in Q}
            allT = frozenset().union(*(T for T, _, _ in patterns))
            B = allT
            for i in goodpairs[0]:
                B = self.repair(B, cell[i])
            self.union_check(AP, B)
            gains = []
            for T, _, C in patterns:
                orientation = 0 if T <= self.O[0] else 1
                H = (self.O[orientation] - T) | C
                self.legal(H)
                gains.append(self.f(self.O[orientation]) - self.f(H))
            E = []
            for pair, orientation in [(P, 0), (Q, 1)]:
                Y, X = pair
                TY, _, CY = patterns[Y]
                TX, _, CX = patterns[X]
                A0 = self.O[orientation]
                A1 = (A0 - TY) | CY
                converted0 = (A0 - TX) | CX
                converted1 = (A1 - TX) | CX
                value = self.f(A1) - self.f(converted1) - self.f(A0) + self.f(converted0)
                E.append(value)
                if len(cell[Y]) == 2 or len(cell[X]) == 2:
                    assert value == 0
                    continue
                other = [i for i in range(4) if i not in pair]
                B0 = self.O[1 - orientation] | {self.chord(cell[Y]), self.chord(cell[X])}
                for i in other:
                    B0 = self.repair(B0, cell[i])
                B1 = (B0 - CY) | TY
                for A, B in [(A0, B0), (A1, B1)]:
                    self.union_check(A, B)
                    assert TX <= A and CX <= B
                errors += 1
            delta = self.f(AP) - self.f(AQ)
            D = self.f(self.O[0]) - self.f(self.O[1])
            assert D == delta + sum(gains[i] for i in P) - sum(gains[i] for i in Q) + E[0] - E[1]
            total += delta + E[0] - E[1]
        assert total == self.f(self.O[0]) - self.f(self.O[1])
        return len(cells), errors


def all_walks(tree, n):
    nodes = sorted(tree)
    for walk in product(nodes, repeat=n):
        if all(walk[(i + 1) % n] == walk[i] or walk[(i + 1) % n] in tree[walk[i]] for i in range(n)):
            yield walk


def residual_assignment_check():
    scenarios = []
    for tiers, replicas in product(range(1, 6), range(1, 4)):
        slots = [(t, i) for t in range(tiers - 1, -1, -1) for i in range(replicas)]
        pairs = [(x, y) for x in range(len(slots)) for y in range(len(slots)) if slots[x][0] == slots[y][0] + 1]
        seen = set()
        for x, y in pairs:
            assert x < y
            for prefix in range(1 << x):
                S = prefix | (1 << x) | (1 << y)
                assert S not in seen
                seen.add(S)
        scenarios.append({'tiers': tiers, 'replicas': replicas, 'slots': len(slots), 'pairs': len(pairs), 'residual_components': len(seen)})
    return scenarios


def main():
    trees = {
        'chain3': {0: {1}, 1: {0, 2}, 2: {1}},
        'star4': {0: {1, 2, 3}, 1: {0}, 2: {0}, 3: {0}},
        'chain4': {0: {1}, 1: {0, 2}, 2: {1, 3}, 3: {2}},
    }
    rows = []
    for name, tree in trees.items():
        for n in (4, 6, 8):
            walks = cells = errors = 0
            for walk in all_walks(tree, n):
                c, e = Check(walk, tree).check()
                walks += 1
                cells += c
                errors += e
            rows.append({'tree': name, 'cycle_length': n, 'walks': walks, 'cells': cells, 'two_long_error_encodings': errors})
    result = {
        'completed_utc': datetime.now(timezone.utc).isoformat(),
        'primary_source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'cell_cases': rows,
        'residual_assignment_cases': residual_assignment_check(),
        'all_checks_passed': True,
        'limitations': 'Finite cycle/cell checks; no complete FPRAS implementation, no Lean kernel build, no full product-chain state-space enumeration.',
    }
    (HERE / 'independent_check_results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
