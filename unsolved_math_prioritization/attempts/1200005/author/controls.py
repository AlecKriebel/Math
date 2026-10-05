#!/usr/bin/env python3
"""Exact, standard-library controls for binary-tree automorphism laws.

Words are tuples of signed, nonzero integers. Tree portraits use root bit first,
then the left and right depth-(n-1) portraits. Permutations act on the right.
No random test is used to certify a law. Witness searches return exact portraits.
"""
import argparse
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path


def reduce_word(w):
    stack = []
    for x in w:
        if stack and stack[-1] == -x:
            stack.pop()
        else:
            stack.append(x)
    return tuple(stack)


def canonical(w):
    """Signed generator renaming only; preserve free length and lawhood."""
    names = {}
    out = []
    for x in w:
        i = abs(x)
        if i not in names:
            names[i] = (len(names) + 1) * (1 if x > 0 else -1)
        out.append(names[i] * (1 if x > 0 else -1))
    return tuple(out), names


def section(w, eps, start):
    b = start
    out = []
    for x in w:
        i = abs(x) - 1
        if x < 0:
            b ^= eps[i]
        out.append((2 * i + b + 1) * (1 if x > 0 else -1))
        if x > 0:
            b ^= eps[i]
    return b, reduce_word(out)


def pack(n, eps, a, b):
    s = (1 << (n - 1)) - 1
    return eps | (a << 1) | (b << (1 + s))


def unpack(n, g):
    s = (1 << (n - 1)) - 1
    return g & 1, (g >> 1) & ((1 << s) - 1), g >> (1 + s)


@lru_cache(maxsize=None)
def inverse(n, g):
    if n == 0:
        return 0
    eps, a, b = unpack(n, g)
    children = (a, b)
    return pack(n, eps, inverse(n - 1, children[eps]),
                inverse(n - 1, children[1 ^ eps]))


@lru_cache(maxsize=None)
def permutation(n, g):
    if n == 0:
        return (0,)
    eps, a, b = unpack(n, g)
    half = 1 << (n - 1)
    pa, pb = permutation(n - 1, a), permutation(n - 1, b)
    return tuple(eps * half + x for x in pa) + tuple((1 ^ eps) * half + x for x in pb)


def evaluate(n, w, values):
    perms = {i: permutation(n, g) for i, g in values.items()}
    perms.update({-i: permutation(n, inverse(n, g)) for i, g in values.items()})
    p = tuple(range(1 << n))
    for x in w:
        p = tuple(perms[x][v] for v in p)
    return p


@lru_cache(maxsize=None)
def law(n, w):
    if not w or n == 0:
        return True
    w = reduce_word(w)
    cw, _ = canonical(w)
    if cw != w:
        return law(n, cw)
    k = max(map(abs, w), default=0)
    for eps in itertools.product((0, 1), repeat=k):
        for b in (0, 1):
            end, s = section(w, eps, b)
            if end != b or not law(n - 1, s):
                return False
    return True


def witness(n, w):
    """Return an exact nonlaw evaluation, or None if the word is a law."""
    w = reduce_word(w)
    if not w or n == 0:
        return None
    cw, names = canonical(w)
    if cw != w:
        v = witness(n, cw)
        if v is None:
            return None
        return {old: v[abs(new)] if new > 0 else inverse(n, v[-new])
                for old, new in names.items()}
    k = max(map(abs, w))
    for eps in itertools.product((0, 1), repeat=k):
        for b in (0, 1):
            end, s = section(w, eps, b)
            if end != b:
                return {i + 1: pack(n, eps[i], 0, 0) for i in range(k)}
            if law(n - 1, s):
                continue
            v = witness(n - 1, s)
            assert v is not None
            return {i + 1: pack(n, eps[i], v.get(2 * i + 1, 0),
                                v.get(2 * i + 2, 0)) for i in range(k)}
    return None


def exponent_sums(w):
    out = {}
    for x in w:
        out[abs(x)] = out.get(abs(x), 0) + (1 if x > 0 else -1)
    return out


def balanced_cyclic_words(length, max_rank):
    """All signed-renaming canonical, cyclically reduced, balanced words."""
    if length == 0:
        return
    word = [1]
    sums = [1]

    def rec():
        left = length - len(word)
        if sum(map(abs, sums)) > left:
            return
        if left == 0:
            if word[-1] != -1 and all(x == 0 for x in sums):
                yield tuple(word)
            return
        for i in range(len(sums)):
            for sign in (1, -1):
                x = (i + 1) * sign
                if x == -word[-1]:
                    continue
                word.append(x)
                sums[i] += sign
                yield from rec()
                sums[i] -= sign
                word.pop()
        if len(sums) < max_rank and left >= 2:
            sums.append(1)
            word.append(len(sums))
            yield from rec()
            word.pop()
            sums.pop()

    yield from rec()


def all_reduced(k, length):
    letters = tuple(range(1, k + 1)) + tuple(range(-1, -k - 1, -1))
    def rec(w):
        if len(w) == length:
            yield w
            return
        for x in letters:
            if not w or x != -w[-1]:
                yield from rec(w + (x,))
    yield from rec(())


def prefix_witness(w):
    """Bradford-style separated-prefix construction, depth exactly len(w)."""
    if not w:
        return {}
    n = len(w)
    if n == 1:
        return {abs(w[0]): 1}
    old = prefix_witness(w[:-1])
    # Extend each permutation by preserving its new last binary digit.
    old_perms = {i: permutation(n - 1, g) for i, g in old.items()}
    lifted = {i: tuple(2 * p[v // 2] + v % 2 for v in range(1 << n))
              for i, p in old_perms.items()}
    for x in w:
        lifted.setdefault(abs(x), tuple(range(1 << n)))
    def invp(p):
        q = [0] * len(p)
        for i, v in enumerate(p):
            q[v] = i
        return tuple(q)
    def trace(values):
        p, path = 0, [0]
        for x in w:
            q = values[abs(x)] if x > 0 else invp(values[-x])
            p = q[p]
            path.append(p)
        return path
    path = trace(lifted)
    if len(set(path)) != len(path):
        j = abs(w[-1])
        p = list(lifted[j])
        if w[-1] > 0:
            a = path[-2]
            p[a], p[a ^ 1] = p[a ^ 1], p[a]
        else:
            # Swap the output siblings at the starting point of the inverse edge.
            a = path[-2]
            p = [v ^ 1 if v // 2 == a // 2 else v for v in p]
        lifted[j] = tuple(p)
    assert len(set(trace(lifted))) == len(w) + 1
    return {i: from_permutation(n, p) for i, p in lifted.items()}


def from_permutation(n, p):
    if n == 0:
        assert p == (0,)
        return 0
    h = 1 << (n - 1)
    eps = p[0] // h
    assert all(v // h == eps for v in p[:h])
    assert all(v // h == 1 ^ eps for v in p[h:])
    a = from_permutation(n - 1, tuple(v % h for v in p[:h]))
    b = from_permutation(n - 1, tuple(v % h for v in p[h:]))
    return pack(n, eps, a, b)


def run():
    result = {"format": 1, "claims": {}, "checks": {}}
    # Independent permutation arithmetic checks the portrait/section routines.
    arithmetic = 0
    for n in range(1, 4):
        size = 1 << ((1 << n) - 1)
        for g in range(size):
            p = permutation(n, g)
            assert sorted(p) == list(range(1 << n))
            assert from_permutation(n, p) == g
            q = permutation(n, inverse(n, g))
            assert all(q[p[i]] == i for i in range(1 << n))
            assert evaluate(n, (1,) * (1 << n), {1: g}) == tuple(range(1 << n))
            arithmetic += 1
    result["checks"]["all_portraits_depths_1_through_3"] = arithmetic
    # Exhaustive direct assignments for reduced words in F_2 through length 6
    # in W_2; compare with the exact recursive law criterion.
    direct = 0
    for length in range(1, 7):
        for w in all_reduced(2, length):
            brute = all(evaluate(2, w, {1: a, 2: b}) == (0, 1, 2, 3)
                        for a in range(8) for b in range(8))
            assert brute == law(2, w)
            direct += 1
    result["checks"]["recursive_vs_direct_W2_words"] = direct
    # The full arbitrary-rank depth-3 claim reduces to balanced even lengths 4,6.
    low_counts = {}
    stream = hashlib.sha256()
    for length in (4, 6):
        independently_enumerated = {
            canonical(w)[0] for w in all_reduced(3, length)
            if w[-1] != -w[0] and all(e == 0 for e in exponent_sums(w).values())
        }
        assert set(balanced_cyclic_words(length, length // 2)) == independently_enumerated
        count = 0
        for w in balanced_cyclic_words(length, length // 2):
            v = witness(3, w)
            assert v is not None
            p = evaluate(3, w, v)
            assert p != tuple(range(8))
            stream.update(json.dumps([w, sorted(v.items()), p], separators=(",", ":")).encode()+b"\n")
            count += 1
        low_counts[str(length)] = count
    result["claims"]["L1_L2_L3"] = [2, 4, 8]
    result["checks"]["depth3_arbitrary_rank_balanced_cyclic_words"] = low_counts
    result["checks"]["depth3_witness_stream_sha256"] = stream.hexdigest()
    # Restricted rank-two depth-4 claim. This is not an arbitrary-rank claim.
    counts = {}
    stream = hashlib.sha256()
    for length in range(4, 16, 2):
        count = 0
        for w in balanced_cyclic_words(length, 2):
            v = witness(4, w)
            assert v is not None, ("unexpected law", w)
            p = evaluate(4, w, v)
            assert p != tuple(range(16))
            stream.update(json.dumps([w, sorted(v.items()), p], separators=(",", ":")).encode()+b"\n")
            count += 1
        counts[str(length)] = count
        # Independent fixed-alphabet dynamic-programming count. All nonempty
        # reduced balanced two-variable words use both variables, so signed
        # permutations act freely, with orbit size 8. Fixing the first letter
        # to +x accounts for four of those possibilities, leaving a factor 2.
        @lru_cache(maxsize=None)
        def count_suffix(left, last, ex, ey):
            if left == 0:
                return int(last != -1 and ex == 0 and ey == 0)
            return sum(count_suffix(left - 1, a,
                                    ex + (1 if a == 1 else -1 if a == -1 else 0),
                                    ey + (1 if a == 2 else -1 if a == -2 else 0))
                       for a in (1, -1, 2, -2) if a != -last)
        assert count_suffix(length - 1, 1, 1, 0) == 2 * count
        count_suffix.cache_clear()
    result["claims"]["L4_rank_two"] = 16
    result["checks"]["depth4_rank_two_balanced_cyclic_words"] = counts
    result["checks"]["depth4_witness_stream_sha256"] = stream.hexdigest()
    result["checks"]["independent_candidate_enumeration_checks"] = 8
    # Independently replay the separated-prefix construction on every reduced
    # F_2 word up to length 6, checking membership and all prefix positions.
    prefix_count = 0
    for length in range(1, 7):
        for w in all_reduced(2, length):
            v = prefix_witness(w)
            path = [evaluate(length, w[:j], v)[0] for j in range(length + 1)]
            assert len(set(path)) == length + 1
            prefix_count += 1
    result["checks"]["prefix_separation_words"] = prefix_count
    # Central half-powers, exhaustive n <= 4, checked by leaf permutations.
    central_counts = {}
    for n in range(1, 5):
        ident = tuple(range(1 << n))
        z = tuple(i ^ 1 for i in ident)
        count = 0
        for g in range(1 << ((1 << n) - 1)):
            h = evaluate(n, (1,) * (1 << (n - 1)), {1: g})
            assert h in (ident, z)
            count += 1
        central_counts[str(n)] = count
    result["checks"]["central_halfpower_all_portraits"] = central_counts
    # Literal root-section shortening by 1/2 is false even for [x,y].
    w = (1, 2, -1, -2)
    section_rows = []
    for eps in itertools.product((0, 1), repeat=2):
        row = [section(w, eps, b)[1] for b in (0, 1)]
        assert all(len(s) == 4 for s in row)
        section_rows.append({"root_bits": eps, "sections": row})
    result["checks"]["unshortened_commutator_sections"] = section_rows
    # Power-law positive controls and a nontrivial commutator positive control.
    assert law(1, (1, 1))
    assert law(2, (1,) * 4)
    assert law(3, (1,) * 8)
    assert law(4, (1,) * 16)
    for n in range(1, 5):
        m = 1 << (n - 1)
        central_word = (1,) * m + (2,) + (-1,) * m + (-2,)
        assert len(central_word) == (1 << n) + 2
        assert law(n, central_word)
    result["checks"]["power_and_central_commutator_positive_controls"] = 8
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(data)
    else:
        print(data, end="")
