#!/usr/bin/env python3
"""New exact finite audit from syllable sequences, independent of package checkers."""
from collections import Counter
from itertools import product
import json
import sys


def need(ok, why):
    if not ok:
        raise RuntimeError(why)


def matrix_power(a, t):
    k = len(a)
    r = [[int(i == j) for j in range(k)] for i in range(k)]
    for _ in range(t):
        r = [[sum(r[i][h] * a[h][j] for h in range(k)) for j in range(k)] for i in range(k)]
    return r


rows = []
mutations = Counter()
total_words = total_pairs = suffixes = 0
profiles = [([0, 1, 2], [0, 1, 2], range(6, 10)),
            ([0, 0, 1, 2], [1, 0, 2, 3], range(6, 9)),
            ([0, 1, 1, 2, 2, 2], [0, 2, 1, 3, 5, 4], range(6, 9))]
for colors, inv, lengths in profiles:
    k = len(colors)
    a = [[int(colors[i] != colors[j]) for j in range(k)] for i in range(k)]

    def inverse(w):
        return tuple(inv[x] for x in reversed(w))

    def words(t, prefix=()):
        if len(prefix) == t:
            yield prefix
        else:
            for x in range(k):
                if not prefix or colors[prefix[-1]] != colors[x]:
                    yield from words(t, prefix + (x,))

    reduced = {t: list(words(t)) for t in range(1, 6)}
    v = {t: [w for w in ws if w != inverse(w)] for t, ws in reduced.items()}
    for t, ws in reduced.items():
        endpoint = Counter((w[0], w[-1]) for w in ws)
        power = matrix_power(a, t - 1)
        need(all(endpoint[i, j] == power[i][j] for i in range(k) for j in range(k)), "endpoint exponent")
        removed = [w for w in ws if w == inverse(w)]
        if t % 2 == 0:
            need(not removed, "even inverse fixed")
        elif t > 1:
            need(len(removed) <= k * len(reduced[(t - 1) // 2]), "odd deletion bound")
    for ell in lengths:
        l, e = divmod(ell, 3)
        pattern = ([l, l, l], [l, l, l + 1], [l, l + 1, l + 1])[e]
        types = sorted(set(pattern))
        corners = Counter()
        for i in range(3):
            t, u = pattern[i], pattern[(i + 1) % 3]
            corners[t, u] += 1; corners[u, t] += 1
        expected_c = ([[6]], [[2, 2], [2, 0]], [[0, 2], [2, 2]])[e]
        need([[corners[t, u] for u in types] for t in types] == expected_c, "type counts")
        observed = Counter()
        z = kept = maxdegree = 0
        for w in words(ell):
            if colors[w[0]] == colors[w[-1]]:
                continue
            z += 1
            b0 = w[:pattern[0]]; b1 = w[pattern[0]:pattern[0] + pattern[1]]; b2 = w[pattern[0] + pattern[1]:]
            blocks = [b0, b1, b2]
            if any(b == inverse(b) for b in blocks):
                continue
            kept += 1
            degree = Counter()
            for i in range(3):
                x = inverse(blocks[i]); y = blocks[(i + 1) % 3]
                need(x != y, "loop")
                observed[x, y] += 1; observed[y, x] += 1
                degree[x] += 1; degree[y] += 1
            maxdegree = max(maxdegree, max(degree.values()))
            need(max(degree.values()) <= 3, "per relator degree")
        need(z == sum(matrix_power(a, ell)[i][i] for i in range(k)), "cyclic trace exponent")
        vertices = [w for t in types for w in v[t]]
        pairs = 0
        for x, y in product(vertices, repeat=2):
            t, u = len(x), len(y)
            h = ell - t - u
            c = corners[t, u]
            completion = sum(a[x[-1]][w[0]] * a[w[-1]][y[-1]] for w in v[h]) if c else 0
            kernel = c * a[x[0]][y[0]] * completion
            need(observed[x, y] == kernel, "corner kernel")
            pairs += 1
            if kernel:
                mutations["half-oriented-multiplicity"] += (kernel // 2 != observed[x, y])
            if c:
                undeleted = sum(a[x[-1]][w[0]] * a[w[-1]][y[-1]] for w in reduced[h])
                mutations["omit-completion-deletion"] += (c * a[x[0]][y[0]] * undeleted != observed[x, y])
        need(sum(observed.values()) == 6 * kept, "retention normalization")
        total_words += z; total_pairs += pairs
        rows.append({"parts": [colors.count(c) for c in sorted(set(colors))], "length": ell,
                     "cyclic": z, "retained": kept, "ordered_pairs": pairs, "max_degree_per_sample": maxdegree})
    # Construct the paper's suffix witnesses from factor colors, without enumerating exponential alphabets.
    representatives = {c: colors.index(c) for c in set(colors)}
    for length in range(4, 18):
        for x, y in product(range(k), repeat=2):
            third = next(c for c in representatives if c not in {colors[x], colors[y]})
            others = [c for c in representatives if c != third]
            if length % 2:
                seq = [third, others[0], others[1], third] + [others[0], third] * ((length - 5) // 2)
            else:
                seq = ([third, others[0]] * length)[:length - 1]
            suffix = tuple(representatives[c] for c in seq)
            left = (x,) + suffix; right = (inv[y],) + suffix
            need(len(left) == len(right) == length, "suffix length")
            need(all(colors[w[i]] != colors[w[i + 1]] for w in (left, right) for i in range(length - 1)), "suffix reduction")
            need(left != inverse(left) and right != inverse(right), "suffix survives")
            # Common suffix cancellation in the free product leaves precisely the product x*y.
            need(inverse(right) == inverse(suffix) + (y,), "suffix cancellation")
            suffixes += 1
need(all(mutations.values()) and len(mutations) == 2, "mutation witnesses")
print(json.dumps({"status": "PASS", "mode": "optimized" if sys.flags.optimize else "normal",
                  "cases": rows, "cyclic_words": total_words, "ordered_pairs": total_pairs,
                  "suffix_witnesses": suffixes, "mutation_mismatch_counts": dict(mutations),
                  "scope": "Exact finite diagnostics only; analytical proof and external established inputs remain necessary."}, sort_keys=True, indent=2))
