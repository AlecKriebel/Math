#!/usr/bin/env python3
"""Fresh supplemental checks, independent of the authors' evaluators.

All universal conclusions in REVIEW.md rest on the reconstructed proof.
Finite checks include negative controls and noncommutative coefficient rings.
"""
from datetime import datetime, timezone
from itertools import product
from pathlib import Path
import hashlib
import json
import random


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def label(n):
    row = 1
    while row * (row + 1) // 2 < n:
        row += 1
    return n - row * (row - 1) // 2


def generator(word, p, index, exponent=1, offset=0):
    out = list(word)
    if not out:
        return tuple(out)
    if index == 0:
        out[0] = (out[0] + exponent) % p
        return tuple(out)
    j = next((j for j, x in enumerate(out) if x), None)
    if j is not None and out[j] == 1 and j + 1 < len(out):
        if label(offset + j + 1) == index:
            out[j + 1] = (out[j + 1] + exponent) % p
    return tuple(out)


def apply_word(point, p, word):
    for index, exponent in word:
        point = generator(point, p, index, exponent)
    return point


def tree_checks():
    rng = random.Random(21131)
    answer = []
    for p, indices in [(2, (1,)), (2, (1, 2)), (3, (1,)),
                       (3, (2,)), (5, (1,)), (5, (2, 4))]:
        n = next(n for n in range(1, 100) if label(n) not in indices)
        prefixes = list(product(range(p), repeat=n))
        if len(prefixes) > 150:
            prefixes = rng.sample(prefixes, 150)
        prefixes += [(0,) * n]
        points = [(0,) * 7, (1,) + (0,) * 6]
        points += [tuple(rng.randrange(p) for _ in range(7)) for _ in range(12)]
        words = [((i, e),) for i in (0,) + indices for e in (1, -1)]
        words += [tuple((rng.choice((0,) + indices), rng.choice((1, -1)))
                        for _ in range(rng.randint(2, 12))) for _ in range(100)]
        comparisons = 0
        for word in words:
            for initial_prefix in prefixes:
                current = initial_prefix
                tail = {i: 0 for i in indices}
                for i, e in word:
                    if i and not any(current):
                        tail[i] += e
                    current = generator(current, p, i, e)
                for suffix in points:
                    expected_suffix = suffix
                    for i, e in tail.items():
                        expected_suffix = generator(expected_suffix, p, i, e, offset=n)
                    actual = apply_word(initial_prefix + suffix, p, word)
                    assert actual == current + expected_suffix
                    comparisons += 1
        # Every d_i has order p on tested words, and commuting portraits.
        for point in points:
            for i in indices:
                assert apply_word(point, p, ((i, 1),) * p) == point
                for j in indices:
                    assert apply_word(point, p, ((i, 1), (j, 1))) == apply_word(point, p, ((j, 1), (i, 1)))
        # Infinite recurrence is symbolic, but exhibit future support per label.
        recurrence = {i: [n for n in range(1, 500) if label(n) == i][-3:] for i in indices}
        answer.append(dict(p=p, indices=indices, common_zero_depth=n,
                           comparisons=comparisons, later_support_examples=recurrence))
    # A missing common zero would make the claimed tail certificate false.
    bad_prefix = (1,)
    assert label(1) == 1
    assert generator(bad_prefix + (0,), 2, 1) == bad_prefix + (1,)
    assert generator((0,), 2, 1, offset=1) == (0,)
    return answer


class TruncatedFree:
    """Fp<x,y> modulo all degree >=3 monomials, WITH its scalar 1."""
    words = ('', 'x', 'y', 'xx', 'xy', 'yx', 'yy')

    def __init__(self, p):
        self.p = p
        self.zero = (0,) * 7
        self.one = (1,) + (0,) * 6
        self.basis = [tuple(int(j == i) for j in range(7)) for i in range(7)]
        self.table = {(i, j): self.words.index(a + b)
                      for i, a in enumerate(self.words) for j, b in enumerate(self.words)
                      if len(a + b) <= 2}

    def add(self, a, b):
        return tuple((x + y) % self.p for x, y in zip(a, b))

    def neg(self, a):
        return tuple(-x % self.p for x in a)

    def mul(self, a, b):
        out = [0] * 7
        for (i, j), k in self.table.items():
            out[k] += a[i] * b[j]
        return tuple(x % self.p for x in out)

    def scalar(self, a):
        return (a % self.p,) + (0,) * 6

    def inv(self, u):
        assert u[0] == 1
        a = self.add(u, self.neg(self.one))
        return self.add(self.add(self.one, self.neg(a)), self.mul(a, a))


def algebra_checks(p):
    r = TruncatedFree(p)
    rng = random.Random(21131 + p)
    z, o = r.zero, r.one
    ident = tuple(tuple(o if i == j else z for j in range(3)) for i in range(3))

    def madd(a, b):
        return tuple(tuple(r.add(a[i][j], b[i][j]) for j in range(3)) for i in range(3))

    def mneg(a):
        return tuple(tuple(r.neg(a[i][j]) for j in range(3)) for i in range(3))

    def mmul(a, b):
        return tuple(tuple(sum_ring(r.mul(a[i][k], b[k][j]) for k in range(3))
                           for j in range(3)) for i in range(3))

    def sum_ring(xs):
        answer = z
        for x in xs:
            answer = r.add(answer, x)
        return answer

    def e(i, j, a):
        return tuple(tuple(r.add(ident[k][l], a if (k, l) == (i, j) else z)
                           for l in range(3)) for k in range(3))

    def diag(*entries):
        return tuple(tuple(entries[i] if i == j else z for j in range(3)) for i in range(3))

    def chain(*matrices):
        answer = ident
        for matrix in matrices:
            answer = mmul(answer, matrix)
        return answer

    def unit():
        return (1,) + tuple(rng.randrange(p) for _ in range(6))

    def nil_entry():
        return (0,) + tuple(rng.randrange(p) for _ in range(6))

    checks = 0
    for _ in range(18):
        u, v = unit(), unit()
        ui, vi = r.inv(u), r.inv(v)
        uv = r.mul(u, v)
        assert r.mul(u, ui) == r.mul(ui, u) == o
        # Exact six-factor noncommutative elementary identity.
        assert chain(e(0, 1, u), e(1, 0, r.neg(ui)), e(0, 1, u),
                     e(0, 1, r.neg(o)), e(1, 0, o), e(0, 1, r.neg(o))) == diag(u, ui, o)
        assert chain(diag(u, ui, o), diag(v, vi, o),
                     diag(r.inv(uv), uv, o)) == diag(o, chain_ring(r, ui, vi, u, v), o)
        # The actual map used in the proof is a homomorphism.
        assert mmul(diag(o, u, o), diag(o, v, o)) == diag(o, uv, o)
        checks += 4
        for i, j in ((i, j) for i in range(3) for j in range(3) if i != j):
            k = 3 - i - j
            a, b = nil_entry(), nil_entry()
            assert chain(e(i, k, a), e(k, j, b), e(i, k, r.neg(a)),
                         e(k, j, r.neg(b))) == e(i, j, r.mul(a, b))
            # Every degree-two monomial has the required elementary recipe.
            for s in r.basis[1:3]:
                for t in r.basis[1:3]:
                    assert chain(e(i, k, s), e(k, j, t), e(i, k, r.neg(s)),
                                 e(k, j, r.neg(t))) == e(i, j, r.mul(s, t))
            # Random constant conjugation; its difference is square zero.
            qword = [(rng.randrange(3), rng.randrange(3), rng.randrange(p)) for _ in range(6)]
            qword = [(a, b, c) for a, b, c in qword if a != b]
            q = chain(*(e(a, b, r.scalar(c)) for a, b, c in qword))
            qi = chain(*(e(a, b, r.scalar(-c)) for a, b, c in reversed(qword)))
            assert mmul(q, qi) == ident
            for s in r.basis[1:3]:
                conjugate = chain(q, e(i, j, s), qi)
                difference = madd(conjugate, mneg(ident))
                assert mmul(difference, difference) == tuple((z, z, z) for _ in range(3))
                assert all(entry[0] == 0 for row in difference for entry in row)
            checks += 10
        # Stable nil property is witnessed directly in this toy algebra.
        matrix = tuple(tuple(nil_entry() for _ in range(3)) for _ in range(3))
        assert chain(matrix, matrix, matrix) == tuple((z, z, z) for _ in range(3))
        checks += 1
    x, y = r.basis[1:3]
    assert r.mul(x, y) != r.mul(y, x)
    u, v = r.add(o, x), r.add(o, y)
    assert mmul(diag(u, r.inv(u), o), diag(v, r.inv(v), o)) != diag(r.mul(u, v), r.inv(r.mul(u, v)), o)
    checks += 2
    return dict(p=p, exact_assertions=checks, coefficient_dimension=7,
                noncommutative=True, D_not_homomorphism_negative_control=True)


def chain_ring(r, *elements):
    answer = r.one
    for element in elements:
        answer = r.mul(answer, element)
    return answer


def main():
    results = dict(utc=datetime.now(timezone.utc).isoformat(),
                   status='all independently authored assertions passed',
                   tree=tree_checks(), algebra=[algebra_checks(p) for p in (2, 3, 5)],
                   limits='Finite supplements only; universal validity is the independent proof reconstruction in REVIEW.md.')
    results['inputs'] = []
    for relative in ['INTEGRATED_CANDIDATE.md', 'tree_targets/locally_finite_original_at_target.md',
                     'nil_embeddings/EMBEDDING_PROOF.md', 'verification/family_reproduction_results.json']:
        results['inputs'].append(dict(path=relative, sha256=hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()))
    results['evaluator_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (HERE / 'independent_results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
