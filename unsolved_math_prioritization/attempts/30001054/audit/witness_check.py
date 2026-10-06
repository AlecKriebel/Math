#!/usr/bin/env python3
"""Finite check of a literal four-axiom gap; no imported theorem is proved here."""
import argparse
import collections
import json
import math
import pathlib
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_json(path):
    def reject(value):
        raise ValueError('Nonfinite JSON constant: ' + value)
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique,
                      parse_constant=reject)


def reverse_toggle(term):
    return tuple(-x for x in reversed(term))


def analyze(data):
    require(type(data) is dict and set(data) == {'schema', 'n', 'sequence'}, 'Invalid fields')
    require(type(data['schema']) is int and data['schema'] == 1, 'Invalid schema')
    n = data['n']
    require(type(n) is int and 2 <= n <= 8, 'Invalid n')
    sequence = data['sequence']
    require(type(sequence) is list and len(sequence) == 8 * math.comb(n, 2), 'Invalid period length')
    symbols = set(range(1, n + 1)) | set(range(-n, 0))
    for term in sequence:
        require(type(term) is list and len(term) == 2 * n, 'Invalid term length')
        require(all(type(x) is int for x in term) and set(term) == symbols, 'Invalid symbols')
        require(all(term.index(i) < term.index(-i) for i in range(1, n + 1)), 'Endpoint order')
    sequence = [tuple(term) for term in sequence]
    length = len(sequence)
    require(all(sequence[(i + length // 2) % length] == reverse_toggle(sequence[i])
                for i in range(length)), 'Half-period reversal')
    switches = []
    for i, before in enumerate(sequence):
        after = sequence[(i + 1) % length]
        changed = [j for j in range(2 * n) if before[j] != after[j]]
        require(len(changed) == 2 and changed[1] == changed[0] + 1, 'Not one adjacent swap')
        j, k = changed
        require(before[j] == after[k] and before[k] == after[j], 'Not a transposition')
        require(abs(before[j]) != abs(before[k]), 'Same-body swap')
        switches.append((after[j], after[k]))
    least = next(d for d in range(1, length + 1)
                 if all(sequence[i] == sequence[(i + d) % length] for i in range(length)))
    require(least == length, 'Not the stipulated least period')
    counts = collections.Counter(switches)
    expected = {(a, b) for a in symbols for b in symbols if abs(a) != abs(b)}
    separating = sum(a * b < 0 for a, b in switches)
    return {
        'literal_four_axioms': True,
        'least_period': least,
        'single_nontrivial_adjacent_swap_at_every_step': True,
        'half_period_identity_at_every_phase': True,
        'switch_convention': 'post-switch ordered pair; negative means primed',
        'switches': [list(s) for s in switches],
        'switch_multiplicities': [{'switch': list(s), 'count': counts[s]} for s in sorted(counts)],
        'missing_directed_switches': [list(s) for s in sorted(expected - set(counts))],
        'separating_switch_count': separating,
        'supporting_switch_count': length - separating,
        'switch_once_condition': set(counts) == expected and all(v == 1 for v in counts.values()),
        'all_terms_overlap': all(max(t.index(i) for i in range(1, n + 1)) <
                                 min(t.index(-i) for i in range(1, n + 1)) for t in sequence),
    }


def verify_witness(path):
    data = read_json(path)
    require(type(data) is dict and data.get('n') == 2, 'Certificate is for n=2')
    result = analyze(data)
    require(result['separating_switch_count'] == 0, 'Missing-internal-switch obstruction absent')
    require(result['supporting_switch_count'] == 8, 'Wrong supporting count')
    require(len(result['missing_directed_switches']) == 4, 'Wrong missing switch count')
    require(result['switch_once_condition'] is False, 'Not an axiom-gap witness')
    require(result['all_terms_overlap'] is True, 'Overlap cross-check failed')
    return {'result': 'PASS_LITERAL_AXIOM_GAP',
            'imported_representation_theorem_proved_by_code': False, **result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('witness', nargs='?', type=pathlib.Path,
                        default=pathlib.Path(__file__).resolve().parent / 'WITNESS.json')
    args = parser.parse_args()
    try:
        result = verify_witness(args.witness)
    except Exception as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
