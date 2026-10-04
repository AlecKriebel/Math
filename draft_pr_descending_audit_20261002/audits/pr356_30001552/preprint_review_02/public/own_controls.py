"""Reviewer02 literal controls. No imported candidate or prior control code."""
import itertools
import json
from math import gcd


def image(w, sigma):
    return tuple(sigma[x] for x in w[::-1])


def prefix(w, p, sigma):
    assert p > 0
    if len(w) <= p:
        return True
    u = w[:p]
    b = u + image(u, sigma)
    return w == (b * ((len(w) + len(b) - 1) // len(b)))[:len(w)]


def ordinary(w, p):
    return w[p:] == w[:-p] if p < len(w) else True


models = [(0,), (0, 1), (1, 0), (0, 1, 2), (1, 0, 2)]
words = queries = large = 0
for sigma, limit in zip(models, [12, 9, 9, 7, 7]):
    assert all(sigma[sigma[a]] == a for a in range(len(sigma)))
    for n in range(limit + 1):
        for w in itertools.product(range(len(sigma)), repeat=n):
            words += 1
            assert image(image(w, sigma), sigma) == w
            ps = []
            for p in range(1, n + 3):
                queries += 1
                if prefix(w, p, sigma):
                    ps.append(p)
                    if p <= n:
                        assert ordinary(image(w, sigma) + w, 2 * p)
            for p in ps:
                for q in ps:
                    d = gcd(p, q)
                    if n >= p + q - d:
                        assert prefix(w, d, sigma)
                        W = image(w, sigma) + w
                        assert ordinary(W, 2 * d)
                        for i in range(n):
                            r = i % (2 * d)
                            j = r if r < d else r - 2 * d
                            assert -n <= j < n
                            assert W[n + i] == W[n + j]

for sigma in models:
    for p in range(1, 41):
        u = tuple((i * i + 3 * i + p) % len(sigma) for i in range(p))
        b = u + image(u, sigma)
        for n in sorted({p, 2 * p - 1, 2 * p, 2 * p + 1, 3 * p + 1}):
            w = (b * ((n + 2 * p - 1) // (2 * p)))[:n]
            assert prefix(w, p, sigma)
            assert ordinary(image(w, sigma) + w, 2 * p)
            for q in range(1, min(n, 40) + 1):
                if prefix(w, q, sigma) and n >= p + q - gcd(p, q):
                    assert prefix(w, gcd(p, q), sigma)
            large += 1

# All five mutations have concrete hand-checked witnesses, independent of
# enumeration. These checks would fail if an oracle accepted the mutation.
w = (0, 1, 1)
assert prefix(w, 2, (0, 1)) and not ordinary(w + w, 4)
b = (0, 1, 1, 0)
i = 1
assert b[(-1 - i) % 4] == b[i]
assert b[(-i) % 4] != b[i]
assert prefix(b, 2, (0, 1)) and b != (0, 1, 0, 1)
w = (0, 0, 1)
assert len(w) == 2 + 3 - gcd(2, 3) - 1
assert prefix(w, 2, (1, 0)) and prefix(w, 3, (1, 0))
assert not prefix(w, 1, (1, 0))
w = (0, 0, 0, 0)
assert len(w) == 2 + 3 - gcd(2, 3)
for p in (2, 3):
    u = w[:p]
    assert w == (u * ((len(w) + p - 1) // p))[:len(w)]
assert not prefix(w, 1, (1, 0))

print(json.dumps({
    'status': 'PASS',
    'mechanism': 'literal finite templates, central coordinates, and concrete mutation witnesses',
    'word_cases': words,
    'literal_period_queries': queries,
    'larger_template_truncations': large,
    'mutations_falsified': [
        {'mutation': 'ww extension', 'word': [0, 1, 1], 'sigma': [0, 1], 'p': 2},
        {'mutation': 'reflection center -i', 'block': [0, 1, 1, 0], 'i': 1},
        {'mutation': 'second block without reversal', 'word': [0, 1, 1, 0], 'p': 2},
        {'mutation': 'one less threshold', 'word': [0, 0, 1], 'sigma': [1, 0], 'p': 2, 'q': 3},
        {'mutation': 'arbitrary block choices', 'word': [0, 0, 0, 0], 'sigma': [1, 0], 'p': 2, 'q': 3}
    ],
    'scope': 'finite falsifiers only; universal result is the independently checked written proof'
}, indent=2))
