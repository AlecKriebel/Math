#!/usr/bin/env python3
"""Source-free exact checks for the authored KP-2.28 partial report.
Python 3 standard library only. This is a finite check, not the general proof.
"""
import hashlib
import itertools
import json
from collections import deque
from fractions import Fraction as F
from pathlib import Path


def connected(mask, adj):
    if not mask:
        return False
    reached = mask & -mask
    while True:
        nxt = reached
        for v in range(len(adj)):
            if reached >> v & 1:
                nxt |= adj[v] & mask
        if nxt == reached:
            return reached == mask
        reached = nxt


def cds(mask, adj):
    if not connected(mask, adj):
        return False
    covered = mask
    for v in range(len(adj)):
        if mask >> v & 1:
            covered |= adj[v]
    return covered == (1 << len(adj)) - 1


def contained_in_join_masks(gamma):
    """Independent brute force: enumerate every disjoint nonempty join pair."""
    n = len(gamma)
    joins = set()
    full = (1 << n) - 1
    for left in range(1, full + 1):
        available = full ^ left
        right = available
        while right:
            if all((gamma[v] & right) == right
                   for v in range(n) if left >> v & 1):
                sub = left | right
                while sub:
                    joins.add(sub)
                    sub = (sub - 1) & (left | right)
            right = (right - 1) & available
    return joins


def graph_check():
    graphs = subsets = 0
    for n in range(1, 6):
        pairs = list(itertools.combinations(range(n), 2))
        for bits in range(1 << len(pairs)):
            gamma = [0] * n
            for k, (a, b) in enumerate(pairs):
                if bits >> k & 1:
                    gamma[a] |= 1 << b
                    gamma[b] |= 1 << a
            lam = [((1 << n) - 1) ^ (1 << v) ^ gamma[v]
                   for v in range(n)]
            in_join = contained_in_join_masks(gamma)
            for mask in range(1, 1 << n):
                assert cds(mask, lam) == (mask not in in_join)
                subsets += 1
            graphs += 1
    return {"labelled_graphs": graphs, "nonempty_supports": subsets,
            "mismatches": 0, "maximum_vertices": 5}


def cycle_checks():
    cases = 0
    examples = []
    for n in range(5, 21):
        lam = [(1 << ((i - 1) % n)) | (1 << ((i + 1) % n))
               for i in range(n)]
        support = ((1 << n) - 1) ^ (1 << 1) ^ (1 << 2)
        assert cds(support, lam)
        for m in range(n, 4*n + 1):
            tree = [(1 << (i-1) if i else 0) |
                    (1 << (i+1) if i+1 < m else 0) for i in range(m)]
            lifted = sum(1 << i for i in range(m) if i % n not in {1, 2})
            assert lifted & 1 and lifted & (1 << 3)
            assert not connected(lifted, tree)
            cases += 1
        if n == 5:
            examples.append({"cycle_order": n, "path_vertices": n,
                             "source_support": [0, 3, 4],
                             "lifted_support_components": [[0], [3, 4]]})
    return {"cases": cases, "all_source_supports_loxodromic": True,
            "all_lifted_supports_disconnected": True, "examples": examples}


def commutes(x, y):
    return frozenset((x.lower(), y.lower())) in {
        frozenset('ab'), frozenset('bc'), frozenset('cd')}


def cyclic_reduction_check():
    start = 'acACbdBDcaCAdbDB'
    target = 'AdBDaCAdbDac'
    seen = {start}
    q = deque([start])
    minimum = len(start)
    while q:
        word = q.popleft()
        minimum = min(minimum, len(word))
        next_words = []
        for i in range(len(word)-1):
            if word[i].swapcase() == word[i+1]:
                next_words.append(word[:i] + word[i+2:])
            elif commutes(word[i], word[i+1]):
                next_words.append(word[:i] + word[i+1] + word[i] + word[i+2:])
        if word:
            next_words.append(word[1:] + word[:1])
        for other in next_words:
            if other not in seen:
                seen.add(other)
                q.append(other)
    assert target in seen and minimum == 12
    blockers = []
    for i, letter in enumerate(target):
        for distance in range(1, len(target)):
            j = (i + distance) % len(target)
            if target[j] == letter.swapcase():
                between = ''.join(target[(i+k) % len(target)]
                                  for k in range(1, distance))
                # RAAG inverse-pair cancellation requires every intervening
                # letter to commute; equal generators do not commute as moves.
                assert any(x.lower() != letter.lower() and not commutes(letter, x) for x in between)
                blockers.append([i, j, between])
    assert set(target.lower()) == set('abcd')
    return {"commutation_cancellation_rotation_states": len(seen),
            "minimum_cyclic_length": minimum,
            "cyclically_reduced_word": target,
            "support": list('abcd'), "blocked_inverse_arcs": blockers}


def mm(a, b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def inv(a):
    return ((a[1][1], -a[0][1]), (-a[1][0], a[0][0]))


def mob(a, x):
    return (a[0][0]*x + a[0][1]) / (a[1][0]*x + a[1][1])


def schottky_check():
    base = ((34, 21), (21, 13))
    ainv = inv(base)
    assert base[0][0]*base[1][1] - base[0][1]*base[1][0] == 1
    plus = [F(3, 2), F(7, 4)]
    minus = [-F(3, 4), -F(1, 2)]
    plus_image = sorted(mob(base, x) for x in minus)
    minus_image = sorted(mob(ainv, x) for x in plus)
    assert plus[0] < plus_image[0] < plus_image[1] < plus[1]
    assert minus[0] < minus_image[0] < minus_image[1] < minus[1]
    # The pole of each map lies in its excluded interval, justifying
    # the entire complementary projective-interval image calculation.
    assert minus[0] < -F(13, 21) < minus[1]
    assert plus[0] < F(34, 21) < plus[1]
    generators = []
    for i in range(3):
        l = 10*i
        generators.append(mm(mm(((1, l), (0, 1)), base), ((1, -l), (0, 1))))
    mats = generators + [inv(a) for a in generators]
    tested = 0
    min_abs_trace = None
    def rec(word, product):
        nonlocal tested, min_abs_trace
        if word and (len(word) == 1 or (word[-1]+3) % 6 != word[0]):
            trace = abs(product[0][0] + product[1][1])
            assert trace > 2
            min_abs_trace = trace if min_abs_trace is None else min(min_abs_trace, trace)
            tested += 1
        if len(word) == 5:
            return
        for i, matrix in enumerate(mats):
            if not word or i != (word[-1]+3) % 6:
                rec(word+[i], mm(product, matrix))
    rec([], ((1, 0), (0, 1)))
    return {"base_matrix": base, "forward_interval_image": list(map(str, plus_image)),
            "inverse_interval_image": list(map(str, minus_image)),
            "sample_free_rank": 3, "max_cyclic_word_length": 5,
            "sample_words_checked": tested, "minimum_absolute_trace": min_abs_trace,
            "warning": "Finite sampling supplements, and does not replace, the all-word ping-pong proof."}


def c5_transversal_check():
    n = 5
    lam = [(1 << ((i-1) % n)) | (1 << ((i+1) % n)) for i in range(n)]
    supports = [m for m in range(1, 1 << n) if cds(m, lam)]
    minimal = [m for m in supports if not any(s != m and s & m == s for s in supports)]
    cliques = [m for m in range(1, 1 << n)
               if all(((m ^ (1 << i)) & ~lam[i]) == 0
                      for i in range(n) if m >> i & 1)]
    assert len(minimal) == 5 and all(m.bit_count() == 3 for m in minimal)
    for k in cliques:
        assert any(not k & m for m in minimal)
    return {"minimal_supports": [[i for i in range(n) if m >> i & 1] for m in minimal],
            "nonempty_cliques": len(cliques), "clique_transversals": 0}


def main():
    results = {"problem_id": 2776, "all_checks_passed": True,
               "graph_criterion": graph_check(), "cycle_cover_obstruction": cycle_checks(),
               "free_quotient_obstruction": cyclic_reduction_check(),
               "explicit_free_embedding": schottky_check(),
               "c5_local_gadget_obstruction": c5_transversal_check(),
               "finite_cover_obstruction": "Proved in the report; not computationally tested."}
    output = Path(__file__).with_name('VERIFICATION_RESULTS.json')
    output.write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps({k: v for k, v in results.items() if k not in {'free_quotient_obstruction'}}, indent=2))


if __name__ == '__main__':
    main()
