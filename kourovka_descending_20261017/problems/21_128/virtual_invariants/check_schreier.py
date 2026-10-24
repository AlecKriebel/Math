#!/usr/bin/env python3
"""Exact finite checks for the proved cyclic-cover free basis.

No Artin word problem is solved or assumed. Arguments for arbitrary m/word
length are in FREE_RETRACT_FILTER.md; this independently checkable computation
exercises the explicit rewriting formulas, including inverse letters and m=1.
"""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import itertools
import json


def reduce_word(word):
    result = []
    for letter in word:
        if result and result[-1] == -letter:
            result.pop()
        else:
            result.append(letter)
    return tuple(result)


def expand_basis(letter, m):
    # Basis 1 is a^m; basis j+2 is a^j b a^-j.
    positive = abs(letter)
    if positive == 1:
        word = (1,) * m
    else:
        j = positive - 2
        assert 0 <= j < m
        word = (1,) * j + (2,) + (-1,) * j
    return word if letter > 0 else tuple(-x for x in reversed(word))


def rewrite(word, m):
    vertex = 0
    result = []
    for x in word:
        if x == 1:
            if vertex == m - 1:
                result.append(1)
            vertex = (vertex + 1) % m
        elif x == -1:
            if vertex == 0:
                result.append(-1)
            vertex = (vertex - 1) % m
        elif x == 2:
            result.append(vertex + 2)
        elif x == -2:
            result.append(-(vertex + 2))
        else:
            raise ValueError(x)
    return reduce_word(result), vertex


def reduced_words(max_length):
    yield ()
    frontier = [()]
    for _ in range(max_length):
        following = []
        for word in frontier:
            for x in (1, -1, 2, -2):
                if not word or word[-1] != -x:
                    following.append(word + (x,))
        yield from following
        frontier = following


def main():
    rows = []
    words = list(reduced_words(8))
    assert len(words) == 1 + sum(4 * 3 ** (n - 1) for n in range(1, 9))
    for m in range(1, 65):
        basis_checks = 0
        for j in range(1, m + 2):
            for sign in (1, -1):
                rewritten, endpoint = rewrite(expand_basis(sign * j, m), m)
                assert endpoint == 0
                assert rewritten == (sign * j,)
                basis_checks += 1
        kernel_words = 0
        for word in words:
            abstract, endpoint = rewrite(word, m)
            lifted = reduce_word(itertools.chain.from_iterable(
                expand_basis(x, m) for x in abstract))
            # The spanning-tree identity is w = rewritten(w) * a^endpoint.
            assert reduce_word(lifted + (1,) * endpoint) == word
            assert endpoint == sum(1 if x == 1 else -1 if x == -1 else 0
                                   for x in word) % m
            if endpoint == 0:
                kernel_words += 1
                assert lifted == word
        rows.append(dict(index=m, vertices=m, oriented_positive_edges=2*m,
                         covering_free_rank=2*m-m+1,
                         basis_count=m+1, basis_inverse_checks=basis_checks,
                         reduced_words_tested=len(words),
                         kernel_words_checked=kernel_words))
    report = dict(
        generated_utc=datetime.now(timezone.utc).isoformat(),
        scope="Finite exact checks; universal proof is the spanning-tree argument.",
        max_reduced_word_length=8,
        checks=sum(row['reduced_words_tested'] for row in rows),
        rows=rows,
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        status="PASS")
    destination = Path(__file__).with_name('schreier_checks.json')
    destination.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in
                      ('status', 'checks', 'max_reduced_word_length',
                       'source_sha256')}, indent=2))


if __name__ == '__main__':
    main()
