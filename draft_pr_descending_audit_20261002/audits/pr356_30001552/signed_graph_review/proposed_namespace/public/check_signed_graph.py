"""Independent, exact source-definition controls. Standard library only."""
from itertools import product
from math import gcd
import json


def fold(t, h):
    residue = t % (2 * h)
    return (residue, 0) if residue < h else (2 * h - 1 - residue, 1)


class SignedDSU:
    def __init__(self, size):
        self.parent = list(range(size))
        self.parity = [0] * size
        self.rank = [0] * size

    def find(self, x):
        if self.parent[x] != x:
            old = self.parent[x]
            root, sign = self.find(old)
            self.parity[x] ^= sign
            self.parent[x] = root
        return self.parent[x], self.parity[x]

    def join(self, x, y, sign):
        rx, sx = self.find(x)
        ry, sy = self.find(y)
        if rx == ry:
            assert sx ^ sy == sign, ("unexpected odd cycle", x, y, sign)
            return
        if self.rank[rx] > self.rank[ry]:
            rx, ry = ry, rx
        self.parent[rx] = ry
        self.parity[rx] = sx ^ sy ^ sign
        if self.rank[rx] == self.rank[ry]:
            self.rank[ry] += 1

    def entails(self, x, y, sign):
        rx, sx = self.find(x)
        ry, sy = self.find(y)
        return rx == ry and sx ^ sy == sign


def build_graph(n, periods):
    graph = SignedDSU(n)
    for h in periods:
        for t in range(h, n):
            c, sign = fold(t, h)
            graph.join(t, c, sign)
    return graph


def entails_period(graph, n, d):
    return all(graph.entails(t, *fold(t, d)) for t in range(d, n))


def theta(word, tau):
    return tuple(tau[x] for x in reversed(word))


def direct_alt(word, h, tau):
    """Source definition also permits a seed longer than the observed prefix."""
    if len(word) < h:
        return True
    block = word[:h] + theta(word[:h], tau)
    return all(value == block[t % (2 * h)] for t, value in enumerate(word))


def constraint_alt(word, h, tau):
    return all(word[t] == (tau[word[c]] if sign else word[c])
               for t in range(h, len(word)) for c, sign in [fold(t, h)])


def ordinary_period(word, h):
    return all(word[t] == word[t + h] for t in range(len(word) - h))


counts = {"endpoint_pairs": 0, "longer_pairs": 0, "below_endpoint_pairs": 0,
          "below_endpoint_failures": 0, "divisor_sign_checks": 0,
          "word_encoding_checks": 0, "word_pair_conclusions": 0,
          "reflection_word_checks": 0, "lift_translation_checks": 0,
          "witness_checks": 0}
first_witness = None

for p in range(1, 221):
    for q in range(1, p + 1):
        d = gcd(p, q)
        n0 = p + q - d
        for n in (n0, n0 + 1, n0 + p):
            graph = build_graph(n, (p, q))
            assert entails_period(graph, n, d), (p, q, n, "gcd failure")
            counts["endpoint_pairs" if n == n0 else "longer_pairs"] += 1
            for h in (p, q):
                for t in range(h, n):
                    c, sign = fold(t, h)
                    cd, sd = fold(t, d)
                    ccd, scd = fold(c, d)
                    assert cd == ccd and sd ^ scd == sign
                    counts["divisor_sign_checks"] += 1
        n = n0 - 1
        graph = build_graph(n, (p, q))
        good = entails_period(graph, n, d)
        counts["below_endpoint_pairs"] += 1
        if not good:
            counts["below_endpoint_failures"] += 1
            if first_witness is None:
                roots = {}
                witness = []
                for t in range(n):
                    root, sign = graph.find(t)
                    if root not in roots:
                        roots[root] = len(roots)
                    witness.append(2 * roots[root] + sign)
                word = tuple(witness)
                tau = tuple(t ^ 1 for t in range(2 * len(roots)))
                assert direct_alt(word, p, tau) and direct_alt(word, q, tau)
                assert not direct_alt(word, d, tau)
                counts["witness_checks"] += 3
                first_witness = {"p": p, "q": q, "d": d, "n": n,
                                 "word": word, "tau": tau}

# A separate unsigned DSU verifies the signed-slot/reflected-interval mapping.
for n in range(1, 91):
    for h in range(1, n + 1):
        lifted = SignedDSU(2 * n)
        translated = SignedDSU(2 * n)
        for t in range(h, n):
            c, sign = fold(t, h)
            # Slot zero is t; slot one is -1-t in the reflected interval.
            for bit in (0, 1):
                a = n + t if bit == 0 else n - 1 - t
                bbit = bit ^ sign
                b = n + c if bbit == 0 else n - 1 - c
                lifted.join(a, b, 0)
        for a in range(2 * n - 2 * h):
            translated.join(a, a + 2 * h, 0)
        # Partition equivalence is checked by both directions of root maps.
        lr_to_tr = {}
        tr_to_lr = {}
        for a in range(2 * n):
            lr = lifted.find(a)[0]
            tr = translated.find(a)[0]
            assert lr_to_tr.setdefault(lr, tr) == tr
            assert tr_to_lr.setdefault(tr, lr) == lr
            counts["lift_translation_checks"] += 1

for tau, max_length in [((0, 1, 2), 8), ((0, 2, 1), 8), ((1, 0), 10)]:
    alphabet = range(len(tau))
    for n in range(max_length + 1):
        for word in product(alphabet, repeat=n):
            ps = []
            for h in range(1, n + 2):
                direct = direct_alt(word, h, tau)
                assert direct == constraint_alt(word, h, tau), (word, h, tau)
                counts["word_encoding_checks"] += 1
                if h <= n and direct:
                    ps.append(h)
                    doubled = theta(word, tau) + word
                    assert ordinary_period(doubled, 2 * h)
                    counts["reflection_word_checks"] += 1
            for p in ps:
                for q in ps:
                    d = gcd(p, q)
                    if n >= p + q - d:
                        assert direct_alt(word, d, tau)
                        counts["word_pair_conclusions"] += 1

word = (0, 1, 1)
tau = (0, 1)
assert direct_alt(word, 2, tau) and direct_alt(word, 3, tau)
assert not direct_alt(word, 1, tau)
counts["witness_checks"] += 3

print(json.dumps({"status": "PASS", "counts": counts,
                  "first_below_endpoint_complement_witness": first_witness,
                  "graph_period_maximum": 220,
                  "scope": "finite exact controls; uniform result uses credited Fine-Wilf",
                  "involutions": ["three fixed letters", "one fixed letter and one pair", "one complement pair"],
                  "sharpness_scope": "uniform formula only; no pairwise claim"}, indent=2))
