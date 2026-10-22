#!/usr/bin/env python3
"""Exact finite controls for the authored universal midpoint proof; no dependencies."""
from fractions import Fraction as Q
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def reduce_word(word):
    out = []
    inverse = {'a': 'A', 'A': 'a', 'b': 'B', 'B': 'b'}
    for letter in word:
        require(letter in inverse, 'unknown generator')
        if out and out[-1] == inverse[letter]:
            out.pop()
        else:
            out.append(letter)
    return ''.join(out)


def weighted_length(word, a=1, b=2):
    return sum(a if letter.lower() == 'a' else b for letter in reduce_word(word))


def reduced_words(maximum):
    inverse = {'a': 'A', 'A': 'a', 'b': 'B', 'B': 'b'}
    level = ['']
    answer = ['']
    for _ in range(maximum):
        level = [w+c for w in level for c in 'aAbB' if not w or c != inverse[w[-1]]]
        answer.extend(level)
    return answer


def prefix_at_distance(word, distance, a=1, b=1):
    """Return (vertex prefix, next edge, edge fraction), exact metric interpolation."""
    require(distance >= 0, 'negative distance')
    prefix = ''
    for letter in word:
        length = a if letter.lower() == 'a' else b
        if distance == 0:
            return (prefix, '', Q(0))
        if distance < length:
            return (prefix, letter, Q(distance, length))
        prefix += letter
        distance -= length
    require(distance == 0, 'distance exceeds geodesic')
    return (prefix, '', Q(0))


def main():
    counts = {'midpoint_controls': 0, 'quadratic_identity_controls': 0,
              'nearest_integer_controls': 0, 'off_segment_word_controls': 0,
              'enumerated_minimum_controls': 0, 'homothety_controls': 0,
              'nonproportional_length_controls': 0}
    exact_minima = []
    for n in range(1, 81):
        word = 'a'*(4*n)+'b'*(4*n)
        require(weighted_length(word, 1, 1) == 8*n, 'T1 length')
        require(weighted_length(word, 1, 2) == 12*n, 'T2 length')
        require(prefix_at_distance(word, 4*n, 1, 1) == ('a'*(4*n), '', Q(0)), 'first midpoint')
        require(prefix_at_distance(word, 6*n, 1, 2) == ('a'*(4*n)+'b'*n, '', Q(0)), 'second midpoint')
        counts['midpoint_controls'] += 4
        values = []
        for k in range(n+1):
            value = k*k+4*(n-k)**2
            require(value == Q(4*n*n, 5)+5*(Q(k)-Q(4*n, 5))**2, 'quadratic identity')
            require(2*value >= n*n, 'coarse lower bound')
            values.append(value)
            counts['quadratic_identity_controls'] += 2
        floor = (4*n)//5
        nearest = min(abs(Q(4*n, 5)-floor), abs(Q(4*n, 5)-(floor+1)))
        minimum = Q(4*n*n, 5)+5*nearest**2
        require(min(values) == minimum, 'exact minimum')
        counts['nearest_integer_controls'] += 1
        exact_minima.append([n, int(minimum)])
    words = reduced_words(7)
    require(len(words) == 4373, 'word enumeration cardinality')
    for n in range(1, 9):
        expected = min(k*k+4*(n-k)**2 for k in range(n+1))
        values = []
        for h in words:
            first = len(h)
            second = weighted_length('B'*n+h)
            value = first*first+second*second
            require(value >= expected, 'off-segment vertex beats segment minimum')
            require(2*value >= n*n, 'off-segment coarse bound')
            values.append(value)
            counts['off_segment_word_controls'] += 2
        require(min(values) == expected, 'bounded enumeration misses known minimizer')
        counts['enumerated_minimum_controls'] += 1
    # Positive controls: proportional edge lengths preserve fractional path parameters.
    control_words = ['ab', 'aabbb', 'baBA', 'AAAbabBB', 'abABaabb']
    for raw in control_words:
        word = reduce_word(raw)
        for c in (Q(1, 3), Q(1, 2), Q(1), Q(2), Q(7, 2)):
            for fraction in (Q(0), Q(1, 7), Q(1, 2), Q(6, 7), Q(1)):
                one = prefix_at_distance(word, Q(len(word))*fraction)
                two = prefix_at_distance(word, Q(len(word))*fraction*c, c, c)
                require(one == two, 'homothety fractional parameter mismatch')
                counts['homothety_controls'] += 1
    lengths = {'a': [weighted_length('a',1,1), weighted_length('a',1,2)],
               'b': [weighted_length('b',1,1), weighted_length('b',1,2)]}
    require(Q(*lengths['a']) != Q(*lengths['b']), 'length ratios unexpectedly proportional')
    counts['nonproportional_length_controls'] += 1
    result = {'problem_id': '6200022', 'status': 'pass', 'arithmetic': 'exact integer and Fraction',
              'counts': counts, 'total_checks': sum(counts.values()),
              'enumerated_reduced_words': len(words), 'word_length_bound': 7,
              'midpoint_n_range': [1,80], 'off_segment_n_range': [1,8],
              'exact_minima_sha256': hashlib.sha256(json.dumps(exact_minima,sort_keys=True).encode()).hexdigest(),
              'minimum_examples': exact_minima[:10], 'generator_marked_lengths': lengths,
              'scope': 'Finite auxiliary controls only; universal proofs are in RESULT.md.'}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
