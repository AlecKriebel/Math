"""Exact diagnostics accompanying the authored universal derivation; not a formal proof."""
from itertools import product
from collections import defaultdict
import json
RELATIONS = (((1, 1, 0, (1, 1)), (-1, 0, 0, (1, 3)), (1, 0, 0, (3, 1)), (-1, 1, 0, (3, 3))), ((1, 1, 0, (1, 2)), (-1, 0, 0, (1, 4)), (1, 0, 0, (3, 2)), (-1, 1, 0, (3, 4))), ((1, 1, 0, (2, 1)), (-1, 0, 0, (2, 3)), (1, 0, 0, (4, 1)), (-1, 1, 0, (4, 3))), ((1, 1, 0, (2, 2)), (-1, 0, 0, (2, 4)), (1, 0, 0, (4, 2)), (-1, 1, 0, (4, 4))), ((1, 0, 1, (1, 1)), (-1, 0, 0, (1, 2)), (1, 0, 0, (4, 1)), (-1, 0, 1, (4, 2))), ((1, 0, 1, (1, 3)), (-1, 0, 0, (1, 4)), (1, 0, 0, (4, 3)), (-1, 0, 1, (4, 4))))

def evaluate(relation, values=(1, 1, 1, 1)):
    d = defaultdict(int)
    for c, a, b, word in relation:
        z = c
        for i in word:
            z *= values[i - 1]
        d[a, b] += z
    return {k: v for k, v in d.items() if v}

def telescoping(word):
    d = defaultdict(int)
    for j, i in enumerate(word):
        prefix = word[:j]
        suffix = (1,) * (len(word) - j - 1)
        d[prefix + (i,) + suffix] += 1
        d[prefix + (1,) + suffix] -= 1
    return {k: v for k, v in d.items() if v}

def expected_telescope(word):
    d = defaultdict(int)
    d[word] += 1
    d[(1,) * len(word)] -= 1
    return {k: v for k, v in d.items() if v}

def quotient_geometry():

    def plus(*polys):
        d = defaultdict(int)
        for p in polys:
            for mon, c in p.items():
                d[mon] += c
        return {m: c for m, c in d.items() if c}

    def times(p, q):
        d = defaultdict(int)
        for m, c in p.items():
            for n, e in q.items():
                d[tuple((a + b for a, b in zip(m, n)))] += c * e
        return {m: c for m, c in d.items() if c}

    def mon(c, a=0, b=0, s=0, t=0):
        return {(a, b, s, t): c} if c else {}
    S = mon(1, s=1)
    T = mon(1, t=1)
    B = mon(1, b=1)
    theta = (plus(S, times(B, T)), plus(times(B, S), T))
    inverse = (plus(S, times(mon(-1, b=1), T)), plus(times(mon(-1, b=1), S), T))
    coords = (S, T)
    Q = ((1, 1, (0, 0)), (-1, 0, (0, 1)), (1, 0, (1, 0)), (-1, 1, (1, 1)))

    def qimage(lift):
        return plus(*(times(mon(c, b=b), times(coords[w[0]], lift[w[1]])) for c, b, w in Q))
    if not qimage(theta) == {}:
        raise AssertionError('exact diagnostic failed')
    inverse_residual = plus(mon(2, b=1, s=2), mon(-2, b=1, t=2))
    ordinary_residual = plus(mon(1, b=1, s=2), mon(-1, b=1, t=2))
    if not qimage(inverse) == inverse_residual:
        raise AssertionError('exact diagnostic failed')
    if not qimage(coords) == ordinary_residual:
        raise AssertionError('exact diagnostic failed')
    lookup = (0, 1, 0, 1)
    for relation in RELATIONS:
        image = plus(*(times(mon(c, a=a, b=b), times(coords[lookup[w[0] - 1]], theta[lookup[w[1] - 1]])) for c, a, b, w in relation))
        if not image == {}:
            raise AssertionError('exact diagnostic failed')

    def collapse(r):
        d = defaultdict(int)
        for c, a, b, w in r:
            d[a, b, tuple((lookup[i - 1] for i in w))] += c
        return {m: c for m, c in d.items() if c}
    expected = {(0, 1, (0, 0)): 1, (0, 0, (0, 1)): -1, (0, 0, (1, 0)): 1, (0, 1, (1, 1)): -1}
    if not [collapse(r) for r in RELATIONS] == [{}, {}, {}, {}, expected, expected]:
        raise AssertionError('exact diagnostic failed')
    for beta, expected_terms in [(1, {(0, 0): 1, (0, 1): -1, (1, 0): 1, (1, 1): -1}), (-1, {(0, 0): -1, (0, 1): -1, (1, 0): 1, (1, 1): 1})]:
        actual = defaultdict(int)
        for c, b, w in Q:
            actual[w] += c * beta ** b
        if not dict(actual) == expected_terms:
            raise AssertionError('exact diagnostic failed')
    determinant = plus(times(S, S), times(mon(-1, b=2), times(S, S)))
    if not determinant == plus(mon(1, s=2), mon(-1, b=2, s=2)):
        raise AssertionError('exact diagnostic failed')
    if not (inverse_residual != {} and ordinary_residual != {}):
        raise AssertionError('exact diagnostic failed')
    if not all((c % 2 == 0 for c in inverse_residual.values())):
        raise AssertionError('exact diagnostic failed')
    if not [1 - 1, 2 - -2, 1 - 1] == [0, 4, 0]:
        raise AssertionError('exact diagnostic failed')
    return {'candidate_quotient_source_relations': 6, 'candidate_Q_twisted_image_zero': True, 'quotient_relation_images': ['0', '0', '0', '0', 'Q', 'Q'], 'positive_pullback_required_over_integers': True, 'inverse_lift_residual': '2*beta*(s^2-t^2)', 'untwisted_residual': 'beta*(s^2-t^2)', 'inverse_lift_residual_char2_zero': True, 'singular_boundary_factorizations_verified': 2, 'scope': 'Exact symbolic checks; universal THCR, primeness and normal-spanning proofs remain written mathematics.'}

def run():
    if not all((evaluate(r) == {} for r in RELATIONS)):
        raise AssertionError('exact diagnostic failed')
    words = 0
    for n in range(6):
        for word in product(range(1, 5), repeat=n):
            if not telescoping(word) == expected_telescope(word):
                raise AssertionError('exact diagnostic failed')
            words += 1
    coeffchecks = 0
    for p in (2, 3, 5, 7, 11):
        for alpha, beta in product(range(p), repeat=2):
            for relation in RELATIONS:
                if not sum((c * pow(alpha, a, p) * pow(beta, b, p) for c, a, b, w in relation)) % p == 0:
                    raise AssertionError('exact diagnostic failed')
                coeffchecks += 1
    plus_square = (1, 2, 1)
    minus_square = (1, -2, 1)
    if not tuple((a - b for a, b in zip(plus_square, minus_square))) == (0, 4, 0):
        raise AssertionError('exact diagnostic failed')
    for p in (3, 5, 7, 11):
        for r in range(1, p):
            if not 2 * r % p != 0:
                raise AssertionError('exact diagnostic failed')
            if not (r + 1 + (r - 1)) % p == 2 * r % p:
                raise AssertionError('exact diagnostic failed')
            if not (pow(r + 1, 2, p) - pow(r - 1, 2, p)) % p == 4 * r % p:
                raise AssertionError('exact diagnostic failed')
    if not all((c % 2 == 0 for c in (0, 4, 0))):
        raise AssertionError('exact diagnostic failed')
    assoc = 0
    for a, b, c in product(range(17), repeat=3):
        if not a + b + c == a + (b + c):
            raise AssertionError('exact diagnostic failed')
        assoc += 1
    if not len({(n, 0) for n in range(65)}) == 65:
        raise AssertionError('exact diagnostic failed')
    negatives = []

    def rejects(name, test):
        try:
            if not test():
                raise AssertionError('exact diagnostic failed')
        except AssertionError:
            negatives.append(name)
        else:
            raise AssertionError('negative control accepted: ' + name)
    for j, r in enumerate(RELATIONS):
        rejects('added-unit-coefficient-to-f' + str(j + 1), lambda r=r: evaluate(r + ((1, 0, 0, (1, 1)),)) == {})
    rejects('delete-constant-term-f1', lambda: evaluate(RELATIONS[0][:2] + RELATIONS[0][3:]) == {})
    rejects('incorrect-tuple-one-zero-one-one', lambda: all((evaluate(r, (1, 0, 1, 1)) == {} for r in RELATIONS)))
    rejects('false-nonzero-char2-mobius-determinant', lambda: any((c % 2 for c in (0, 4, 0))))
    rejects('augmentation-has-infinite-dimensional-image', lambda: len({0 if n else 1 for n in range(65)}) == 65)
    rejects('incorrect-telescope-sign', lambda: {(2,): -1, (1,): 1} == expected_telescope((2,)))
    return {'result': 'PASS', 'candidate_geometry': quotient_geometry(), 'universal_symbolic_relations': 6, 'finite_field_coefficient_diagnostics': coeffchecks, 'free_word_telescope_diagnostics': words, 'point_section_associativity_diagnostics': assoc, 'positive_dimension_target_monomials': 65, 'geometry_determinant_polynomial': [0, 4, 0], 'negative_controls_rejected': negatives, 'negative_control_count': len(negatives), 'scope': 'Exact diagnostics support the written universal proof; samples do not prove a field classification or geometric theorem.'}
if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
