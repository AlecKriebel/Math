#!/usr/bin/env python3
"""New exact free-word and compact-action cocycle controls; not a full-target proof."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import json
import random
import sys
import sympy as s
from sympy.combinatorics.free_groups import free_group

assert __debug__ and sys.flags.optimize == 0
counts = Counter()
negatives = Counter()
mode = sys.argv[1] if len(sys.argv) > 1 else 'baseline'
assert mode in ['baseline', 'reverse_commutator', 'prefix_suffix_mutation']
Free, u, v, w = free_group('u,v,w')
e = Free.identity


def check(condition, name):
    assert bool(condition), name
    counts[name] += 1


def multiply(g, h):
    coordinates, shift = g
    values, step = h
    result = dict(coordinates)
    for index, word in values.items():
        at = index + shift
        value = result.get(at, e) * word
        if value == e:
            result.pop(at, None)
        else:
            result[at] = value
    return result, shift + step


def inverse(g):
    coordinates, shift = g
    return {index - shift: word ** -1 for index, word in coordinates.items()}, -shift


def product(sequence):
    result = ({}, 0)
    for value in sequence:
        result = multiply(result, value)
    return result


def commutator(g, h):
    return product([g, h, inverse(g), inverse(h)])


def base(word):
    return ({0: word} if word != e else {}), 0


def translate(g, offset):
    return {index + offset: word for index, word in g[0].items()}, g[1]


F = ({}, 1)
one = ({}, 0)


def compression(pairs):
    aa, bb = [base(a) for a, _ in pairs], [base(b) for _, b in pairs]
    cc = [commutator(a, b) for a, b in zip(aa, bb)]
    h = product(cc)
    A = product(translate(a, i + 1) for i, a in enumerate(aa))
    B = product(translate(b, i + 1) for i, b in enumerate(bb))
    C = product(translate(product(cc[i:]), i) for i in range(len(cc)))
    K = product(translate(c, i + 1) for i, c in enumerate(cc))
    check(commutator(A, B) == K, 'parallel_free_group_commutators')
    check(commutator(C, F) == multiply(h, inverse(K)), 'ordered_suffix_cancellation')
    left = commutator(F, C) if mode == 'reverse_commutator' else commutator(C, F)
    if mode == 'prefix_suffix_mutation':
        bad = product(translate(product(cc[:i + 1]), i) for i in range(len(cc)))
        left = commutator(bad, F)
    check(multiply(left, commutator(A, B)) == h, 'two_commutator_identity')
    if h != one and multiply(commutator(F, C), K) != h:
        negatives['reverse_commutator_rejected'] += 1
    if len(cc) >= 2:
        bad = product(translate(product(cc[:i + 1]), i) for i in range(len(cc)))
        if multiply(commutator(bad, F), K) != h:
            negatives['prefix_suffix_mutation_rejected'] += 1
    return h


# Certify a noncommuting infinite-group control before randomized words.
check(commutator(base(u), base(v)) != one, 'nontrivial_free_commutator')
cc1, cc2 = commutator(base(u), base(v)), commutator(base(u), base(w))
check(multiply(cc1, cc2) != multiply(cc2, cc1), 'noncommuting_input_commutators')
compression([(u, v), (u, w)])
compression([])
compression([(e, e)])
compression([(u, v)])
rng = random.Random(4850103)
letters = [u, u ** -1, v, v ** -1, w, w ** -1]


def random_word():
    out = e
    for _ in range(rng.randrange(0, 9)):
        out *= rng.choice(letters)
    return out


for m in range(0, 13):
    for _ in range(20):
        compression([(random_word(), random_word()) for _ in range(m)])
compression([(u ** (i + 1) * v, w * u ** (1 - i)) for i in range(64)])
for _ in range(100):
    g = ({-2: random_word(), 3: random_word()}, rng.randrange(-5, 6))
    h = ({0: random_word(), 1: random_word()}, rng.randrange(-5, 6))
    k = ({-4: random_word()}, rng.randrange(-5, 6))
    # Inputs may contain explicit identity entries; normalize through multiplication.
    g, h, k = multiply(one, g), multiply(one, h), multiply(one, k)
    check(multiply(g, inverse(g)) == one, 'wreath_inverse_right')
    check(multiply(inverse(g), g) == one, 'wreath_inverse_left')
    check(multiply(multiply(g, h), k) == multiply(g, multiply(h, k)), 'wreath_associativity')
    check(product([F, g, inverse(F)]) == translate(g, 1), 'actual_conjugation_shift')
check(negatives['reverse_commutator_rejected'] > 0, 'negative_reversed_word_nonvacuous')
check(negatives['prefix_suffix_mutation_rejected'] > 0, 'negative_prefix_word_nonvacuous')

# An independent closed-four-manifold negative cutoff: rotate S1 in S1 x S3.
theta = s.symbols('theta', real=True)
tau = (1 + s.sin(2 * theta)) / 2
derivative = s.diff(theta + tau, theta)
check(s.simplify(derivative - 1 - s.cos(2 * theta)) == 0, 'circle_cutoff_exact_derivative')
check(tau.subs(theta, s.pi / 2) == s.Rational(1, 2), 'circle_cutoff_interior_time')
check(derivative.subs(theta, s.pi / 2) == 0, 'circle_cutoff_singular')
J = s.diag(derivative.subs(theta, s.pi / 2), 1, 1, 1)
check(J.rank() == 3, 'closed_four_manifold_cutoff_rank_three')

# Exact additive coboundary on S1 rotations, extended to S1 x S3.
# H(t)=1/t for representatives 0<t<1, H(0)=0 is finite Borel everywhere.
# The fixed measure is Dirac at 0. Every displayed integral is finite.
def H(angle):
    angle %= 1
    return Fraction(0) if angle == 0 else 1 / angle


g = Fraction(1, 4)
compact_defects = []
for n in range(5, 105):
    f = Fraction(1, n)
    actual = H(f + g) - H(f) - H(g) + H(Fraction(0))
    extra = (H(f + g) - H(g)) - (H(f) - H(Fraction(0)))
    check(actual == extra, 'compact_action_signed_pushforward')
    check(actual == -n - Fraction(16, n + 4), 'compact_action_unbounded_defect_formula')
    check(abs(actual) >= n, 'compact_action_unbounded_defect_lower_bound')
    compact_defects.append({'n': n, 'defect_numerator': actual.numerator, 'defect_denominator': actual.denominator})
mu = {Fraction(0): Fraction(2, 3), Fraction(1, 3): Fraction(1, 3)}
for _ in range(200):
    f, g = Fraction(rng.randrange(30), 30), Fraction(rng.randrange(30), 30)
    def Q(a):
        return sum((weight * (H(x + a) - H(x)) for x, weight in mu.items()), Fraction(0))
    push = {}
    for x, weight in mu.items():
        target = (x + g) % 1
        push[target] = push.get(target, Fraction(0)) + weight
    extra = sum((weight * (H(x + f) - H(x)) for x, weight in push.items()), Fraction(0)) - Q(f)
    actual = Q(f + g) - Q(f) - Q(g)
    check(actual == extra, 'rational_circle_weighted_defect_identity')
    check(sum(push.values()) == 1, 'pushforward_probability_preserved')
    if actual != 0:
        negatives['wrong_signed_pushforward_rejected'] += int(actual != -extra)
check(negatives['wrong_signed_pushforward_rejected'] > 0, 'wrong_pushforward_sign_nonvacuous')

# A bounded height supplies a contrasting positive example without invariance.
def bounded_H(angle):
    angle %= 1
    return angle


for n in range(5, 105):
    f, g = Fraction(1, n), Fraction(1, 4)
    defect = bounded_H(f + g) - bounded_H(f) - bounded_H(g) + bounded_H(0)
    check(abs(defect) <= 2, 'noninvariant_bounded_coboundary_bound')

result = {'schema': 'pr48-algebra-family-new-independent-controls/v1', 'status': 'PASS',
          'assertions': sum(counts.values()), 'checks': dict(counts), 'negative_predicates': dict(negatives),
          'sympy_version': s.__version__, 'free_group_cases': 265, 'maximum_input_commutators': 64,
          'infinite_group_normal_forms': 'SymPy free group on three generators, restricted wreath with integer shifts',
          'compact_action_unbounded_defect_sample': compact_defects,
          'unbounded_defect_analytic_formula': '-n-16/(n+4), n>=5',
          'new_substantive_research_turns': 0, 'audit_turns': 0, 'full_target_resolved': False,
          'scope': 'Finite exact controls plus the written universal derivation; Borel cocycle example diagnoses the stated averaging axioms, not a full Diff0 quasimorphism or a solution.'}
print(json.dumps(result, indent=2) + '\n', end='')
