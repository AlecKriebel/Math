#!/usr/bin/env python3
"""Small exact checks; no external dependencies, source downloads or network.

The general proofs are in PROOF.md. This program checks the actual bijection,
its inverse, the cancellation involution, and independent finite identities.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import permutations, product
from math import comb, factorial
from functools import lru_cache
import json


COUNTS = Counter()


def check(value, category):
    assert value, category
    COUNTS[category] += 1


def arrangement_value(n, k):
    value = 1
    for j in range(1, n + 1):
        value = j * value + (k - 1) ** j
    return value


def derangements(n):
    a, b = 1, 0
    if n == 0:
        return a
    for j in range(2, n + 1):
        a, b = b, (j - 1) * (a + b)
    return b


def forward(sigma, colors):
    """Permutation is zero-based; colors are a tuple at increasing fixed points."""
    n = len(sigma)
    inverse = [0] * n
    for i, j in enumerate(sigma):
        inverse[j] = i
    color_it = iter(colors)
    upper, lower, raw = [], [], []
    for i in range(n):
        a, b = inverse[i], sigma[i]
        h = len(upper)
        assert h == len(lower)
        if a == i:
            assert b == i
            raw.append((h, 3, next(color_it)))
        elif a > i and b > i:
            upper.append(i)
            lower.append(i)
            raw.append((h + 1, 0, 0))
        elif a < i and b < i:
            p, q = upper.index(a) + 1, lower.index(b) + 1
            upper.remove(a)
            lower.remove(b)
            raw.append((h - 1, 0, (p, q)))
        elif a < i < b:
            p = upper.index(a) + 1
            upper.remove(a)
            upper.append(i)
            raw.append((h, 1, p))
        elif b < i < a:
            q = lower.index(b) + 1
            lower.remove(b)
            lower.append(i)
            raw.append((h, 2, q))
        else:
            raise AssertionError("missing case")
    assert not upper and not lower
    # Move the first down-label to its stack-matched upstep.
    out = list(raw)
    stack, height = [], 0
    for i, (nxt, typ, label) in enumerate(raw):
        if nxt == height + 1:
            stack.append(i)
        elif nxt == height - 1:
            j = stack.pop()
            p, q = label
            out[j] = (raw[j][0], 0, p)
            out[i] = (nxt, 0, q)
        height = nxt
    assert not stack
    return tuple(out)


def backward(history):
    """Inverse symmetrization followed by inverse arc scan."""
    raw = list(history)
    stack, height = [], 0
    for i, (nxt, typ, label) in enumerate(history):
        if nxt == height + 1:
            stack.append(i)
        elif nxt == height - 1:
            j = stack.pop()
            raw[i] = (nxt, 0, (history[j][2], label))
        height = nxt
    assert height == 0 and not stack
    upper, lower, colors = [], [], []
    sigma = [None] * len(history)
    height = 0
    for i, (nxt, typ, label) in enumerate(raw):
        if typ == 3:
            sigma[i] = i
            colors.append(label)
        elif nxt == height + 1:
            upper.append(i)
            lower.append(i)
        elif nxt == height - 1:
            p, q = label
            a, b = upper.pop(p - 1), lower.pop(q - 1)
            sigma[a] = i
            sigma[i] = b
        elif typ == 1:
            a = upper.pop(label - 1)
            sigma[a] = i
            upper.append(i)
        elif typ == 2:
            b = lower.pop(label - 1)
            sigma[i] = b
            lower.append(i)
        else:
            raise AssertionError("invalid history")
        height = nxt
    assert not upper and not lower
    assert sorted(sigma) == list(range(len(history)))
    return tuple(sigma), tuple(colors)


def sign(history, k):
    if k >= 0:
        return 1
    return -1 if sum(step[1] == 3 for step in history) % 2 else 1


def steps(height, k):
    if height:
        for lab in range(1, height + 1):
            yield height - 1, 0, lab
    for lab in range(1, height + 2):
        yield height + 1, 0, lab
    for typ in (1, 2):
        for lab in range(1, height + 1):
            yield height, typ, lab
    for lab in range(1, abs(k) + 1):
        yield height, 3, lab


def all_prefixes(n, k):
    paths = {(): 0}
    for _ in range(n):
        nxt = {}
        for p, h in paths.items():
            for step in steps(h, k):
                nxt[p + (step,)] = step[0]
        paths = nxt
    buckets = defaultdict(list)
    for p, h in paths.items():
        buckets[h].append(p)
    return {h: sorted(v) for h, v in buckets.items()}


def prefix_matching(paths, k):
    stack, matching = [], {}
    for p in paths:
        if stack and sign(stack[-1], k) != sign(p, k):
            q = stack.pop()
            matching[p] = q
            matching[q] = p
        else:
            stack.append(p)
    return matching, set(stack)


def reverse_segment(segment, initial_height):
    heights = [initial_height] + [s[0] for s in segment]
    return tuple((heights[i], segment[i][1], segment[i][2])
                 for i in range(len(segment) - 1, -1, -1))


def phi(history, matches):
    n = len(history) // 2
    p = history[:n]
    h = p[-1][0] if p else 0
    q = reverse_segment(history[n:], h)
    matching = matches.get(h, {})
    if p in matching:
        p = matching[p]
    elif q in matching:
        q = matching[q]
    return p + reverse_segment(q, 0)


def jacobi_row(n, k):
    row = [1]
    for _ in range(n):
        nxt = [0] * (len(row) + 1)
        for h, value in enumerate(row):
            nxt[h] += (2 * h + k) * value
            nxt[h + 1] += (h + 1) * value
            if h:
                nxt[h - 1] += h * value
        row = nxt
    return row


def jacobi_from(start, n, k):
    row = {start: 1}
    for _ in range(n):
        nxt = defaultdict(int)
        for h, value in row.items():
            nxt[h] += (2 * h + k) * value
            nxt[h + 1] += (h + 1) * value
            if h:
                nxt[h - 1] += h * value
        row = nxt
    return row


@lru_cache(None)
def linearization(i, j, h):
    total = 0
    for d in range(min(i, j, h) + 1):
        twice = [i + j - h - d, i + h - j - d, j + h - i - d]
        if min(twice) < 0 or any(x % 2 for x in twice):
            continue
        a, b, c = [x // 2 for x in twice]
        total += factorial(a + b + c + d) * 2 ** d // (
            factorial(a) * factorial(b) * factorial(c) * factorial(d))
    return total


def laguerre_q(h):
    return [Fraction((-1) ** (h + j) * comb(h, j), factorial(j))
            for j in range(h + 1)]


def multiply_poly(a, b):
    result = [Fraction()] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i + j] += x * y
    return result


def factorial_integral(poly):
    return sum((v * factorial(j) for j, v in enumerate(poly)), Fraction())


def square_entry(h, j, k):
    lo, hi = sorted((h, j))
    if lo == hi:
        return lo * lo + (2 * lo + k) ** 2 + (lo + 1) ** 2
    if hi == lo + 1:
        return 2 * (lo + 1) * (2 * lo + k + 1)
    if hi == lo + 2:
        return (lo + 1) * (lo + 2)
    return 0


def local_walks(n, k=-1):
    row = {0: 1}
    for _ in range(n):
        nxt = defaultdict(int)
        for h, count in row.items():
            for j in range(max(0, h - 2), h + 3):
                weight = square_entry(h, j, k)
                assert weight >= 0
                nxt[j] += count * weight
        row = nxt
    return row.get(0, 0)


def main():
    # 1. Three independent arithmetic definitions and exact square identities.
    for k in range(-12, 13):
        for n in range(0, 33):
            a = arrangement_value(n, k)
            egf = factorial(n) * sum((Fraction((k - 1) ** j, factorial(j))
                                      for j in range(n + 1)), Fraction())
            rencontres = sum(comb(n, f) * derangements(n - f) * k ** f
                             for f in range(n + 1))
            check(a == egf == rencontres, "recurrence_egf_rencontres")
            row = jacobi_row(n, k)
            check(row[0] == a, "jacobi_moments")
            for h, value in enumerate(row):
                explicit = factorial(n) * sum((Fraction(comb(n - j, h) *
                    (k - 1) ** j, factorial(j)) for j in range(n - h + 1)),
                    Fraction())
                check(value == explicit, "prefix_closed_formula")
            check(sum(v * v for v in row) == arrangement_value(2 * n, k),
                  "integer_sum_of_squares")

    # 2. The actual permutation/history bijection; full small finite classes.
    for n in range(0, 7):
        for m in range(0, 4):
            histories = set()
            signed_total = 0
            for sigma in permutations(range(n)):
                fixed = sum(i == j for i, j in enumerate(sigma))
                for colors in product(range(1, m + 1), repeat=fixed):
                    history = forward(sigma, colors)
                    check(backward(history) == (sigma, colors), "bijection_roundtrip")
                    check(history not in histories, "bijection_injective")
                    histories.add(history)
                    check(sign(history, -m) == (-1) ** fixed if m else fixed == 0,
                          "bijection_sign")
                    signed_total += (-1) ** fixed
            check(len(histories) == arrangement_value(n, m), "unsigned_full_class")
            check(signed_total == arrangement_value(n, -m), "signed_full_class")
            # Independently generated closed histories certify surjectivity too.
            generated = set(all_prefixes(n, -m).get(0, []))
            check(histories == generated, "bijection_surjective")

    # 3. Prefix stack matching and full path involutions.
    samples = []
    for k in range(-3, 4):
        for n in range(0, 4):
            buckets = all_prefixes(n, k)
            matches, survivors = {}, {}
            for h, paths in buckets.items():
                matching, remain = prefix_matching(paths, k)
                matches[h], survivors[h] = matching, remain
                check(len({sign(p, k) for p in remain}) <= 1,
                      "prefix_survivor_sign")
                check(len(remain) == abs(jacobi_row(n, k)[h]),
                      "prefix_survivor_count")
                for p, q in matching.items():
                    check(matching[q] == p and sign(p, k) == -sign(q, k),
                          "prefix_pairing_involution")
            closed = all_prefixes(2 * n, k).get(0, [])
            fixed_count = 0
            images = set()
            for history in closed:
                image = phi(history, matches)
                check(phi(image, matches) == history, "full_involution")
                check(image in closed, "full_involution_domain")
                # Check after transporting the map back to permutations.
                perm, col = backward(image)
                check(forward(perm, col) == image, "transported_involution")
                images.add(image)
                if image == history:
                    check(sign(history, k) == 1, "positive_fixed_points")
                    fixed_count += 1
                else:
                    check(sign(image, k) == -sign(history, k), "sign_reversal")
            check(len(images) == len(closed), "full_map_bijective")
            check(fixed_count == sum(len(s) ** 2 for s in survivors.values())
                  == arrangement_value(2 * n, k), "residual_pair_cardinality")
            samples.append({"k": k, "n": n, "fixed_points": fixed_count})

    # 4. Local model and all-parameter gauge obstruction.
    for n in range(0, 41):
        check(local_walks(n) == arrangement_value(2 * n, -1), "local_walk_model")
        row = jacobi_from(0, 2 * n, -1)
        terminal = [8, 120, 320, 480, 360, 120]
        check(sum(row.get(h, 0) * v for h, v in enumerate(terminal))
              == arrangement_value(2 * n + 5, -1), "local_odd_walk_model")
    check(jacobi_row(5, -1) == terminal, "local_odd_terminal_vector")
    for k in range(-2, -101, -1):
        if (-k) % 2 == 0:
            s = (-k) // 2
            cycle = [s - 1, s, s + 1, s - 1]
        else:
            s = (-k - 1) // 2
            cycle = [s - 1, s, s + 2, s + 1, s - 1]
        edge_product = 1
        for h, j in zip(cycle, cycle[1:]):
            edge_product *= square_entry(h, j, k)
        check(edge_product < 0, "negative_cycle_obstruction")
    # Entrywise matrix multiplication checks (10), including h=0 boundary.
    for k in range(-12, 13):
        def entry(h, j):
            if h == j:
                return 2 * h + k
            if abs(h - j) == 1:
                return max(h, j)
            return 0
        for h in range(16):
            for j in range(18):
                expected = sum(entry(h, ell) * entry(ell, j)
                               for ell in range(20))
                check(expected == square_entry(h, j, k), "jacobi_square_entries")

    # 5. Odd-size identities and the concrete remaining sign obstruction.
    check([x * y for x, y in zip(jacobi_row(2, -1), jacobi_row(3, -1))]
          == [-4, 0, 12], "odd_mixed_sign_example")
    for k in range(-20, 1):
        r = 1 - k
        for n in range(2, 50):
            check(arrangement_value(n, k) == (n - r) * arrangement_value(n - 1, k)
                  + r * (n - 1) * arrangement_value(n - 2, k), "second_order")
        for n in range(1, 50, 2):
            diff = (Fraction(arrangement_value(n + 2, k), factorial(n + 2))
                    - Fraction(arrangement_value(n, k), factorial(n)))
            formula = Fraction(r ** (n + 1), factorial(n + 1)) * (
                1 - Fraction(r, n + 2))
            check(diff == formula, "odd_increment")
    # Verify derivative coefficients directly from the rencontres polynomial.
    for n in range(1, 41):
        for f in range(n):
            check((f + 1) * comb(n, f + 1) * derangements(n - f - 1)
                  == n * comb(n - 1, f) * derangements(n - 1 - f),
                  "derivative_identity")

    # 6. Positive Laguerre linearization, verified against polynomial integrals.
    for i in range(7):
        for j in range(7):
            pair = multiply_poly(laguerre_q(i), laguerre_q(j))
            check(factorial_integral(pair) == int(i == j), "laguerre_orthogonality")
            for h in range(i + j + 2):
                triple = factorial_integral(multiply_poly(pair, laguerre_q(h)))
                check(triple == linearization(i, j, h), "laguerre_linearization")
    for r in range(2, 13):
        k = 1 - r
        for n in range(4 * r - 1, 4 * r + 9):
            check(all(v > 0 for v in jacobi_row(n, k)), "uniform_positive_prefixes")
        s = 4 * r
        c = jacobi_row(s, k)
        for i in range(7):
            row = jacobi_from(i, s, k)
            check(all(v >= 0 for v in row.values()), "eventual_nonnegative_rows")
            for j in range(7):
                expected = sum(linearization(i, j, h) * c[h]
                               for h in range(min(s, i + j) + 1))
                check(expected == row.get(j, 0), "eventual_transfer_formula")
    # Evaluate the terminal-colored block graph with its nonnegative T weights.
    for r in range(2, 5):
        k, s = 1 - r, 4 * r
        c = jacobi_row(s, k)
        graph_row = {0: 1}
        for q in range(1, 4):
            for t in range(s):
                terminal = jacobi_row(s + t, k)
                count = sum(v * terminal[h] for h, v in graph_row.items()
                            if h < len(terminal))
                check(count == arrangement_value(q * s + t, k), "eventual_graph_model")
            if q < 3:
                nxt = defaultdict(int)
                for i, value in graph_row.items():
                    for j in range(max(0, i - s), i + s + 1):
                        weight = sum(linearization(i, j, h) * c[h]
                                     for h in range(s + 1))
                        assert weight >= 0
                        nxt[j] += value * weight
                graph_row = nxt

    result = {
        "status": "PASS",
        "checks": dict(sorted(COUNTS.items())),
        "total_assertions": sum(COUNTS.values()),
        "small_even_models": samples,
        "k_minus_one_first_values": [arrangement_value(n, -1) for n in range(11)],
        "limits": "Finite checks support but do not replace the universal proofs. No odd-size structural resolution or novelty claim."
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
