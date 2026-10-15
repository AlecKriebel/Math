"""Finite exhaustive checks of the specific P-tableau/rank-law bridge.

These checks support an elementary proof, not an infinite-limit theorem.
No third-party source text is embedded.
"""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import permutations
from math import factorial
from pathlib import Path
import datetime
import json


def insert(word):
    rows = []
    for value in word:
        row_index = 0
        while True:
            if row_index == len(rows):
                rows.append([value])
                break
            row = rows[row_index]
            pos = next((j for j, old in enumerate(row) if old > value), len(row))
            if pos == len(row):
                row.append(value)
                break
            row[pos], value = value, row[pos]
            row_index += 1
    return tuple(tuple(row) for row in rows)


def shape(tableau):
    return tuple(map(len, tableau))


def pile_tops(word):
    tops = []
    for value in word:
        pos = next((i for i, old in enumerate(tops) if old > value), len(tops))
        if pos == len(tops):
            tops.append(value)
        else:
            tops[pos] = value
    return tuple(tops)


@lru_cache(None)
def skew_count(lam, mu):
    """Count saturated Young-lattice paths by removable-box recursion."""
    if lam == mu:
        return 1
    if len(mu) > len(lam) or any(a > b for a, b in zip(mu, lam)):
        return 0
    result = 0
    for row, size in enumerate(lam):
        if row + 1 < len(lam) and lam[row + 1] == size:
            continue
        if row < len(mu) and size == mu[row]:
            continue
        smaller = list(lam)
        smaller[row] -= 1
        result += skew_count(tuple(x for x in smaller if x), mu)
    return result


def run():
    checked_permutations = 0
    checked_restrictions = 0
    checked_shape_chains = 0
    for n in range(1, 8):
        counts_p = Counter()
        chains = Counter()
        cuts = tuple(sorted({0, 1, n // 2, n - 1, n}))
        for word in permutations(range(1, n + 1)):
            tableau = insert(word)
            assert tableau[0] == pile_tops(word)
            counts_p[tableau] += 1
            chain = tuple(shape(insert(word[:cut])) for cut in cuts)
            chains[chain] += 1
            for k in range(n + 1):
                restricted = tuple(tuple(x for x in row if x <= k) for row in tableau)
                restricted = tuple(row for row in restricted if row)
                assert restricted == insert(tuple(x for x in word if x <= k))
                checked_restrictions += 1
            checked_permutations += 1
        for tableau, count in counts_p.items():
            assert count == skew_count(shape(tableau), ())
        for chain, count in chains.items():
            expected = skew_count(chain[-1], ())
            for mu, lam in zip(chain, chain[1:]):
                expected *= skew_count(lam, mu)
            assert count == expected, (n, cuts, chain, count, expected)
            checked_shape_chains += 1
    return {
        'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'maximum_permutation_size': 7,
        'permutations_checked': checked_permutations,
        'all_small_label_restrictions_checked': checked_restrictions,
        'prescribed_shape_chains_checked': checked_shape_chains,
        'assertions': [
            'P top row equals all patience pile tops',
            'P restricted to labels at most k equals P of the filtered permutation',
            'each P tableau has f(shape) uniform-permutation preimages',
            'prefix shape-chain count equals f(terminal) times product f(skew increments)',
        ],
        'result': 'pass',
        'limitation': 'Finite verification only; general argument is in FINAL_REPORT.md.',
    }


if __name__ == '__main__':
    result = run()
    Path(__file__).with_name('RANK_BRIDGE_CHECKS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
