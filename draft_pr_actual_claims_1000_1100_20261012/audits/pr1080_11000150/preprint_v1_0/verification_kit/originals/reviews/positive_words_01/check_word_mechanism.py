#!/usr/bin/env python3
"""Fresh finite symbolic fault checks; these are not the universal proof."""
import hashlib
import itertools
import json
from pathlib import Path


def reduced(word):
    stack = []
    for letter in word:
        if stack and stack[-1] == -letter:
            stack.pop()
        else:
            stack.append(letter)
    return tuple(stack)


def inverse(word):
    return tuple(-x for x in reversed(word))


def decomposition(v, retained):
    u, blocks, block = [], [], []
    for i, letter in enumerate(v):
        if i in retained:
            blocks.append(tuple(block))
            block = []
            u.append(letter)
        else:
            block.append(letter)
    blocks.append(tuple(block))
    return tuple(u), blocks


def correct_rhs(u, blocks):
    prefix, result = (), ()
    for j, block in enumerate(blocks):
        if j:
            prefix += (u[j - 1],)
        result += prefix + block + inverse(prefix)
    return reduced(result)


def faulty_rhs(v, blocks):
    result = ()
    for j, block in enumerate(blocks):
        prefix = v[:j]  # Deliberate fault: prefixes of v, not retained u.
        result += prefix + block + inverse(prefix)
    return reduced(result)


def subgroup_product(left, right):
    # Z semidirect Z, where the second factor acts by parity on the first.
    r, k = left
    s, ell = right
    return r + (-1) ** k * s, k + ell


def evaluate_semidirect(word):
    value = (0, 0)
    for letter in word:
        value = subgroup_product(value, {'a': (0, 1), 'b': (1, 0)}[letter])
    return value


def subsequence(u, v):
    i = 0
    for x in v:
        if i < len(u) and x == u[i]:
            i += 1
    return i == len(u)


def main():
    cases, proper, empty, repeated, first_fault = 0, 0, 0, 0, None
    for n in range(7):
        for v in itertools.product((1, 2), repeat=n):
            for mask in range(1 << n):
                retained = {i for i in range(n) if mask & (1 << i)}
                u, blocks = decomposition(v, retained)
                lhs = reduced(v + inverse(u))
                assert lhs == correct_rhs(u, blocks), (u, v, mask)
                assert subsequence(u, v)
                if len(u) < len(v):
                    assert lhs, (u, v, mask)  # Free-group positive identity control.
                    proper += 1
                if not u:
                    empty += 1
                if len(set(v)) < len(v):
                    repeated += 1
                if first_fault is None and lhs != faulty_rhs(v, blocks):
                    first_fault = {'u': u, 'v': v, 'mask': mask,
                                   'correct_reduced_lhs': lhs,
                                   'faulty_reduced_rhs': faulty_rhs(v, blocks)}
                cases += 1
    assert first_fault is not None

    # Without conjugation invariance, no-positive-identity alone is insufficient:
    # bab=a, and a is a proper scattered subword of bab. Every nonempty positive
    # a,b-word has k=#a>0, or k=0 and r=#b>0, so cannot equal the group identity.
    assert evaluate_semidirect('a') == evaluate_semidirect('bab') == (0, 1)
    assert subsequence('a', 'bab')
    # Without no-positive-identity, a has the same value as aaa in C2.
    assert 1 % 2 == 3 % 2 and subsequence('a', 'aaa')
    # Without finite alphabet, infinitely many distinct symbols all mapped to 1
    # in Z give an infinite fiber of one-letter words, which are incomparable.
    # Finite proxy checks distinct equal-length words are incomparable.
    assert all(not subsequence((i,), (j,)) for i in range(50) for j in range(50) if i != j)
    # There is no length bound from alphabet size alone across arbitrary targets.
    assert [len('a' * target) for target in (1, 10, 100)] == [1, 10, 100]

    result = {
        'scope': 'fresh finite symbolic controls; universal proof is the written derivation',
        'insertion_cases': cases,
        'proper_subsequence_cases': proper,
        'empty_retained_word_cases': empty,
        'repeated_letter_cases': repeated,
        'all_correct_formula_cases_passed': True,
        'wrong_prefix_formula_detected': first_fault,
        'missing_conjugation_invariance_control': {'group': 'Z semidirect Z, parity action',
                                                   'P': ['a=(0,1)', 'b=(1,0)'],
                                                   'same_value': ['a', 'bab'],
                                                   'no_positive_identity': 'k=#a; if k=0 then r=#b>0'},
        'missing_no_positive_identity_control': 'a and aaa have equal value in C2',
        'missing_finite_alphabet_control': 'countably many distinct symbols evaluating to 1 in Z',
        'alphabet_size_only_bound_control': 'one letter evaluating to +1 in Z has target-dependent lengths 1,10,100',
        'historical_computation_replayed': False,
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }
    destination = Path(__file__).with_name('WORD_CONTROL_RESULTS.json')
    destination.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
