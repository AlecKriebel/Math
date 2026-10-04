#!/usr/bin/env python3
"""Exact, bounded sanity checks. These do not decide the infinite amenability question."""
from fractions import Fraction
from itertools import permutations, combinations
import json


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def inverse(p):
    out = [None] * len(p)
    for i, j in enumerate(p):
        out[j] = i
    return tuple(out)


def image(p, a):
    return frozenset(p[i] for i in a)


def subsets(n):
    return [frozenset(i for i in range(n) if mask >> i & 1) for mask in range(1 << n)]


def swap_partial(n, a, p):
    b = image(p, a)
    assert not a & b
    out = list(range(n))
    for x in a:
        out[x], out[p[x]] = p[x], x
    assert sorted(out) == list(range(n))
    return tuple(out)


def partitions(n):
    # Each set partition once, with blocks ordered by least element.
    def rec(i, blocks):
        if i == n:
            yield tuple(frozenset(b) for b in blocks)
            return
        for j in range(len(blocks)):
            blocks[j].append(i)
            yield from rec(i + 1, blocks)
            blocks[j].pop()
        blocks.append([i])
        yield from rec(i + 1, blocks)
        blocks.pop()
    return list(rec(0, []))


def run():
    counts = {
        'one_swap_restrictions': 0,
        'two_swap_restrictions': 0,
        'partition_normalizers': 0,
        'matrix_embedding_elements': 0,
        'matrix_embedding_products': 0,
        'measure_atom_equalities': 0,
        'measure_invariance_equalities': 0,
        'layer_flattening_pairs': 0,
        'free_word_separations': 0,
    }
    for n in range(1, 6):
        perms = list(permutations(range(n)))
        sets = subsets(n)
        for p in perms:
            for a in sets[1:]:
                if not a & image(p, a):
                    s = swap_partial(n, a, p)
                    assert compose(s, s) == tuple(range(n))
                    assert all(s[x] == p[x] for x in a)
                    counts['one_swap_restrictions'] += 1
        if n <= 4:
            for p in perms:
                for k in perms:
                    for a in sets[1:]:
                        w = image(k, a)
                        if w & (a | image(p, a)):
                            continue
                        s1 = swap_partial(n, a, k)
                        s2 = swap_partial(n, w, compose(p, inverse(k)))
                        s = compose(s2, s1)
                        assert all(s[x] == p[x] for x in a)
                        assert all(s[x] == x for x in set(range(n)) - (a | w | image(p, a)))
                        counts['two_swap_restrictions'] += 1
        for part in partitions(n):
            normalizer = [p for p in perms if {image(p, a) for a in part} == set(part)]
            kernel = [p for p in normalizer if all(image(p, a) == a for a in part)]
            # Product decomposition: arbitrary separate permutations of blocks.
            expected = 1
            for a in part:
                f = 1
                for j in range(1, len(a) + 1):
                    f *= j
                expected *= f
            assert len(kernel) == expected
            quotient_images = {tuple(part.index(image(p, a)) for a in part) for p in normalizer}
            assert len(normalizer) == len(kernel) * len(quotient_images)
            counts['partition_normalizers'] += 1
        for u in sets[1:]:
            # Include the distinguished corner as the first atom; partition its
            # complement into blocks small enough to inject into u.
            order = sorted(u)
            complement = sorted(set(range(n)) - u)
            blocks = [tuple(order)] + [tuple(complement[i:i+len(u)]) for i in range(0, len(complement), len(u))]
            m = len(blocks)
            ambient = [(y, i) for i in range(m) for y in order]
            where = {pair: j for j, pair in enumerate(ambient)}
            phi = {}
            for i, block in enumerate(blocks):
                for j, x in enumerate(block):
                    phi[x] = where[(order[j], i)]
            assert len(set(phi.values())) == n
            used = set(phi.values())
            def lift(p):
                out = list(range(len(ambient)))
                for x in range(n):
                    out[phi[x]] = phi[p[x]]
                assert sorted(out) == list(range(len(ambient)))
                assert all(out[z] == z for z in set(range(len(ambient))) - used)
                return tuple(out)
            lifts = {p: lift(p) for p in perms}
            assert len(set(lifts.values())) == len(perms)
            counts['matrix_embedding_elements'] += len(perms)
            for p in perms:
                for q in perms:
                    assert lifts[compose(p,q)] == compose(lifts[p], lifts[q])
                    counts['matrix_embedding_products'] += 1
            # Uniform invariant probability on u extends to weight 1/|u| per x.
            weights = {x: Fraction(1, len(u)) for block in blocks for x in block}
            for x in range(n):
                assert weights[x] / sum(weights.values()) == Fraction(1,n)
                counts['measure_atom_equalities'] += 1
            assert sum(weights[x] for x in u) == 1
            assert Fraction(1,1) <= sum(weights.values()) <= m
            for e in sets:
                val = sum((weights[x] for x in e), Fraction())
                for p in perms:
                    assert val == sum((weights[x] for x in image(p,e)), Fraction())
                    counts['measure_invariance_equalities'] += 1
    for a in range(1, 8):
        for b in range(1, 8):
            flat = {(i,j): i*b+j for i in range(a) for j in range(b)}
            assert set(flat.values()) == set(range(a*b))
            for src in flat:
                for dst in flat:
                    assert divmod(flat[src], b) == src
                    assert divmod(flat[dst], b) == dst
                    counts['layer_flattening_pairs'] += 1
    inv = {1:-1, -1:1, 2:-2, -2:2}
    alphabet = (1, -1, 2, -2)
    def prepend(s, w):
        return w[1:] if w and w[0] == inv[s] else (s,)+w
    free_records = []
    for length in range(1, 7):
        words = [()]
        last = [()]
        for _ in range(length):
            last = [(s,)+w for w in last for s in alphabet if not w or s != inv[w[0]]]
            words.extend(last)
        words.sort(key=lambda w: (len(w), w))
        index = {w:i for i,w in enumerate(words)}
        assert len(words) == 1 + 2 * (3**length - 1)
        gen = {}
        for s in (1,2):
            partial = {index[w]:index[prepend(s,w)] for w in words if prepend(s,w) in index}
            unused_domain = sorted(set(range(len(words))) - set(partial))
            unused_range = sorted(set(range(len(words))) - set(partial.values()))
            partial.update(zip(unused_domain, unused_range))
            p = tuple(partial[i] for i in range(len(words)))
            assert sorted(p) == list(range(len(words)))
            gen[s], gen[-s] = p, inverse(p)
        for w in words[1:]:
            point = index[()]
            for s in reversed(w):
                point = gen[s][point]
            assert point == index[w] and point != index[()]
            counts['free_word_separations'] += 1
        free_records.append({'radius':length, 'ball_size':len(words), 'nonidentity_words':len(words)-1})
    return {
        'problem_id':20001587,
        'all_checks_passed':True,
        'arithmetic':'exact integer permutations and fractions; Python standard library only',
        'counts':counts,
        'total_checks':sum(counts.values()),
        'free_group_models':free_records,
        'scope':'Finite algebraic controls only. No infinite amenability claim is certified by these tests.',
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
