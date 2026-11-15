#!/usr/bin/env python3
"""Independent bounded exact controls, written before native/foreign exposure."""
from collections import defaultdict
from fractions import Fraction
import json

checks = 0

def need(ok, label):
    global checks
    checks += 1
    if not ok:
        raise ValueError(label)

def reduce_word(word):
    out = []
    for letter in word:
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return tuple(out)

def inverse(word):
    return tuple(-x for x in reversed(word))

def substitute(word, images):
    out = ()
    for x in word:
        image = images[abs(x)]
        out = reduce_word(out + (image if x > 0 else inverse(image)))
    return out

def fox(word, variable):
    result = defaultdict(int)
    prefix = ()
    for letter in word:
        if letter == variable:
            result[prefix] += 1
        prefix = reduce_word(prefix + (letter,))
        if letter == -variable:
            result[prefix] -= 1
    return {word: value for word, value in result.items() if value}

def ring_add(*terms):
    out = defaultdict(int)
    for term in terms:
        for word, coefficient in term.items():
            out[word] += coefficient
    return {word: value for word, value in out.items() if value}

def ring_multiply(left, right):
    out = defaultdict(int)
    for u, a in left.items():
        for v, b in right.items():
            out[reduce_word(u + v)] += a * b
    return {word: value for word, value in out.items() if value}

def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]

def ma(*matrices):
    return [[sum(a[i][j] for a in matrices) for j in range(3)] for i in range(3)]

def scale(a, c):
    return [[c * x for x in row] for row in a]

I = [[int(i == j) for j in range(3)] for i in range(3)]
ZERO = [[0] * 3 for _ in range(3)]

def perm(values):
    return [[int(values[i] == j) for j in range(3)] for i in range(3)]

def transpose(a):
    return list(map(list, zip(*a)))

def evaluate(word, images):
    out = I
    for letter in word:
        a = images[abs(letter)]
        out = mm(out, a if letter > 0 else transpose(a))
    return out

def evaluate_ring(ring, images):
    return ma(ZERO, *(scale(evaluate(word, images), c) for word, c in ring.items()))

def algebra_controls(rank):
    # a=1, b_i=i+1. A second free alphabet has a=1 and U_i=i+1.
    u = [()]
    for i in range(1, rank):
        u.append(u[-1] + (1, i + 1))
    w = u[-1] + (1,)
    forward = {1: (1,), **{i + 1: u[i] for i in range(1, rank)}}
    backward = {1: (1,), **{i + 1: (-1,) + (() if i == 1 else (-i,)) + (i + 1,) for i in range(1, rank)}}
    for generator in range(1, rank + 1):
        need(substitute(substitute((generator,), forward), backward) == (generator,), 'basis inverse U to b')
        need(substitute(substitute((generator,), backward), forward) == (generator,), 'basis inverse b to U')
    S = {word: 1 for word in u}
    need(fox(w, 1) == S, 'a Fox prefixes')
    for i in range(1, rank):
        need(fox(w, i + 1) == {u[i - 1] + (1,): 1}, 'b Fox prefix')
    telescope = {}
    for generator in range(1, rank + 1):
        telescope = ring_add(telescope, ring_multiply(fox(w, generator), {(generator,): 1, (): -1}))
    need(telescope == {w: 1, (): -1}, 'noncommutative fundamental Fox identity')
    return {'rank': rank, 'word_length': len(w), 'a_derivative_terms': len(S), 'both_basis_substitution_composites_identity': True, 'full_free_ring_Fox_identity': True}

def noncommuting_quotient():
    # This is a genuine quotient of the rank100 presentation, but finite:
    # all b_i=1, a=(01), t=(012), hence w=a^100=1 and all relators hold.
    rank = 100
    A = perm([1, 0, 2])
    T = perm([1, 2, 0])
    images = {1: A, **{i + 1: I for i in range(1, rank)}, rank + 1: T}
    u = [()]
    for i in range(1, rank):
        u.append(u[-1] + (1, i + 1))
    w = u[-1] + (1,)
    relator = (rank + 1,) + w + (-(rank + 1),) + inverse(w)
    need(evaluate(w, images) == I and evaluate(relator, images) == I, 'finite quotient relators')
    S = evaluate_ring(fox(w, 1), images)
    actual_a = evaluate_ring(fox(relator, 1), images)
    tm1 = ma(T, scale(I, -1))
    need(actual_a == mm(tm1, S), 'correct ordered Fox derivative')
    swapped = mm(S, tm1)
    need(swapped != actual_a, 'swap order actually differs')
    need(mm(actual_a, ma(A, scale(I, -1))) == ZERO, 'correct a part complex identity')
    need(mm(swapped, ma(A, scale(I, -1))) != ZERO, 'wrong order fails complex identity')
    need(mm(S, ma(A, scale(I, -1))) == ZERO and A != I, 'finite quotient singularity is not Gamma-l2 injectivity')
    return {'a_fox_matrix': actual_a, 'swapped_matrix': swapped, 'wrong_order_d1d2': mm(swapped, ma(A, scale(I, -1))), 'all_relators_hold': True, 'finite_quotient_kernel_not_l2_counterexample': True}

def height_control(rank, M):
    known = set(range(rank - 1))
    need(M > rank and max(known) < M, 'height-control scope')
    trace = []
    for start in range(M - rank + 1):
        required = set(range(start, start + rank - 1))
        need(required <= known, 'all preceding a edges available')
        final_source = start + rank - 1
        need(final_source < M, 'valid source height')
        known.add(final_source)
        trace.append((start, final_source, (final_source + 1) % M))
    need(known == set(range(M)), 'all a source heights generated')
    need(trace[-1][1:] == (M - 1, 0), 'last edge wraps to zero')
    need(set(range(rank - 1)) != set(range(M)), 'without supplied w propagation initial graphing is insufficient')
    return {'rank': rank, 'M': M, 'initial_height_count': rank - 1, 'propagated_height_count': len(trace), 'last_source_and_target': list(trace[-1][1:]), 'a_map_cost': str(Fraction(rank - 1, M))}

def main():
    algebra = [algebra_controls(r) for r in [2, 3, 7, 100]]
    quotient = noncommuting_quotient()
    heights = [height_control(r, M) for r, Ms in [(2, [3, 5]), (3, [4, 7]), (100, [101, 102, 199, 200, 257])] for M in Ms]
    lhs = 2 * 3 ** 97 * 96 ** 4
    rhs = 2 ** 183
    need(lhs < rhs and 2 ** 61 > 200, 'exact sufficient alpha certificate')
    need(Fraction(1, 2 ** 61) < Fraction(1, 200), 'alpha upper bound')
    need(Fraction(1, 2) >= Fraction(1, 200), 'inadmissible alpha negative control')
    finite_cost = Fraction(1, 2)
    beta0 = Fraction(1, 2)
    need(finite_cost - 1 == -beta0, 'finite group comparison includes beta0')
    need(finite_cost < 1, 'omitting beta0 produces a false finite-group lower bound')
    print(json.dumps({'status': 'PASS_BOUNDED_INDEPENDENT_EXACT_CONTROLS', 'checks': checks, 'free_word_and_Fox': algebra, 'noncommutative_quotient_control': quotient, 'height_propagation_controls': heights, 'integer_certificate': {'left': lhs, 'right': rhs, 'positive_integer_slack': rhs - lhs, 'eta': str(Fraction(1, 100 * 2 ** 61))}, 'finite_group_boundary': {'q': 2, 'cost': '1/2', 'beta0': '1/2', 'beta1': 0}, 'limitations': ['No finite computation proves infinite-tree l2 injectivity or the upstream positive cost bound.', 'No native code/results/archive opinions/current peers/foreign primary bodies read.', 'All independent analytic deductions are in INDEPENDENT_DERIVATION.md.'], 'project_imports_network_subprocess_writes': False}, indent=2))

if __name__ == '__main__':
    main()
