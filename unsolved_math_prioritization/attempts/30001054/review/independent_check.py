#!/usr/bin/env python3
"""Independent exhaustive n=2 audit. Imports no code from the reviewed packet."""
from collections import Counter
from itertools import permutations, product
import json


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


# p and q designate the primed endpoints of 1 and 2, respectively.
ALPHABET = '12pq'
BODY = {'1': 1, 'p': 1, '2': 2, 'q': 2}
TOGGLE = str.maketrans('12pq', 'pq12')
STATES = tuple(''.join(p) for p in permutations(ALPHABET)
               if p.index('1') < p.index('p') and p.index('2') < p.index('q'))


def dual(term):
    return term[::-1].translate(TOGGLE)


def switch(before, after):
    for k in range(3):
        if before[:k] + before[k + 1] + before[k] + before[k + 2:] == after:
            if BODY[before[k]] != BODY[before[k + 1]]:
                return after[k:k + 2]
    return None


def inspect(word):
    if len(word) != 8 or any(t not in STATES for t in word):
        return None
    if any(word[(k + 4) % 8] != dual(word[k]) for k in range(8)):
        return None
    switches = tuple(switch(word[k], word[(k + 1) % 8]) for k in range(8))
    if None in switches:
        return None
    period = next(d for d in range(1, 9)
                  if all(word[k] == word[(k + d) % 8] for k in range(8)))
    if period != 8:
        return None
    expected = {a + b for a in ALPHABET for b in ALPHABET if BODY[a] != BODY[b]}
    return {'least_period': period, 'switches': switches,
            'multiplicities': dict(sorted(Counter(switches).items())),
            'missing_switches': sorted(expected - set(switches)),
            'switch_once': len(set(switches)) == 8,
            'separating_events': sum((s[0] in 'pq') != (s[1] in 'pq') for s in switches)}


def main():
    witness = ('12pq', '12qp', '12pq', '12qp', '21qp', '12qp', '21qp', '12qp')
    report = inspect(witness)
    check(report is not None, 'Witness violates a weak axiom or least-period requirement')
    check(report['separating_events'] == 0, 'Internal-tangent obstruction failed')
    check(report['multiplicities'] == {'12': 2, '21': 2, 'pq': 2, 'qp': 2},
          'Unexpected switch multiplicities')
    check(report['missing_switches'] == ['1q', '2p', 'p2', 'q1'], 'Wrong omitted switches')
    # Cartesian-product enumeration, rather than the packet's graph-walk routine.
    # The half-period identity fixes the remaining four terms, so 6**4 inputs are exhaustive.
    counts = Counter()
    roots = set()
    for half in product(STATES, repeat=4):
        word = half + tuple(dual(t) for t in half)
        result = inspect(word)
        if result is None:
            continue
        roots.add(word)
        counts['primitive_weak_words'] += 1
        counts['switch_once_words' if result['switch_once'] else 'non_switch_once_words'] += 1
        if result['separating_events'] == 0:
            counts['zero_separating_words'] += 1
        if '1p2q' in word or '2q1p' in word:
            counts['words_with_fully_separated_term'] += 1
            if not result['switch_once']:
                counts['non_switch_once_with_fully_separated_term'] += 1
    counts.setdefault('non_switch_once_with_fully_separated_term', 0)
    check(witness in roots, 'Witness absent from exhaustive enumeration')
    check(counts['primitive_weak_words'] == 48, 'Weak-word count differs')
    check(counts['switch_once_words'] == 16, 'Switch-once count differs')
    check(counts['non_switch_once_words'] == counts['zero_separating_words'] == 32,
          'Counterexample-class count differs')
    check(counts['non_switch_once_with_fully_separated_term'] == 0,
          'Fully-separated-start boundary failed')
    # Every phase, traversal direction, and renaming of the two bodies remains a witness.
    symmetry_controls = 0
    for word in (witness, tuple(reversed(witness))):
        for relabel in (False, True):
            renamed = tuple(t.translate(str.maketrans('12pq', '21qp')) if relabel else t for t in word)
            for k in range(8):
                transformed = renamed[k:] + renamed[:k]
                checked = inspect(transformed)
                check(checked is not None and checked['separating_events'] == 0, 'Symmetry failure')
                symmetry_controls += 1
    # A genuine n=2 supporting/separating cycle is a positive comparison, not a gap witness.
    good = ('1p2q', '12pq', '21pq', '21qp', '2q1p', '21qp', '21pq', '12pq')
    positive = inspect(good)
    check(positive is not None and positive['switch_once'] and positive['separating_events'] == 4,
          'Positive control failed')
    check(inspect(tuple('12pq' for _ in range(8))) is None, 'Stationary negative control failed')
    check(inspect(witness[:4] * 2) is None, 'Wrong-half-period negative control failed')
    print(json.dumps({'result': 'PASS', 'symbol_key': {'p': "1'", 'q': "2'"},
                      'witness': witness, 'witness_analysis': report,
                      'enumerated_half_words': len(STATES) ** 4,
                      'rooted_word_counts': dict(counts), 'symmetry_controls': symmetry_controls,
                      'positive_control': 'PASS', 'negative_controls': 2,
                      'scope': 'Finite weak-axiom witness; not a proof of the representation theorem.'},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
