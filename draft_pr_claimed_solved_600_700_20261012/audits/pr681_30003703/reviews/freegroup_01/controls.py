#!/usr/bin/env python3
"""Fresh PR681 controls via exact integral unitriangular path representations.

No author/audit code imports or execution. No writes, subprocesses or network.
The full integer matrix products are untruncated. Runtime assertions are avoided.
"""
from itertools import product
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
NATIVE = HERE.parent.parent / 'native/unsolved_math_prioritization/attempts/30003703'


def need(value, text):
    if not value:
        raise RuntimeError(text)


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def multiply(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n))
             for j in range(n)] for i in range(n)]


def plus(a, b, sign=1):
    return [[x + sign * y for x, y in zip(r, s)] for r, s in zip(a, b)]


def matrix_inverse(a):
    """I+N inverse, N strictly upper triangular; entire finite geometric sum."""
    n = len(a)
    ident = eye(n)
    delta = plus(a, ident, -1)
    need(all(delta[i][j] == 0 for i in range(n) for j in range(i+1)),
         'not upper unipotent')
    answer, power = eye(n), eye(n)
    for exponent in range(1, n):
        power = multiply(power, delta)
        answer = plus(answer, power, -1 if exponent % 2 else 1)
    need(multiply(power, delta) == [[0]*n for _ in range(n)], 'nilpotence')
    need(multiply(answer, a) == multiply(a, answer) == ident, 'two-sided matrix inverse')
    return answer


def reverse(word):
    return tuple(-v for v in reversed(word))


def freely_reduce(word):
    # Deliberately use repeated adjacent-cancellation passes, not author's stack.
    word = tuple(word)
    while True:
        cut = next((i for i in range(len(word)-1) if word[i] == -word[i+1]), None)
        if cut is None:
            return word
        word = word[:cut] + word[cut+2:]


def commutator(a, b):
    # Keep unreduced words here, so inverse and cancellation are checked later.
    return tuple(a) + tuple(b) + reverse(a) + reverse(b)


def examples():
    a, b, c = (1,), (2,), (3,)
    ab = commutator(a, b)
    w = commutator(commutator(ab, commutator(a, c)), a)
    v = commutator(commutator(ab, commutator(a, ab)), a)
    return w, v


def path_matrices(target, rank):
    """Edge j -> j+1 has the color target[j]; X_i sums edges of color i."""
    out = [eye(len(target)+1) for _ in range(rank)]
    for j, letter in enumerate(target):
        out[letter-1][j][j+1] = 1
    return out


def evaluate(word, matrices):
    inverse = [matrix_inverse(m) for m in matrices]
    out = eye(len(matrices[0]))
    for letter in word:
        out = multiply(out, matrices[letter-1] if letter > 0 else inverse[-letter-1])
    return out


def coefficient_from_paths(word, target, rank):
    return evaluate(word, path_matrices(target, rank))[0][-1]


def full_paths(word, rank, degree):
    """All coefficients of all positive-degree monomials through this degree."""
    out, count = {}, 0
    for d in range(1, degree+1):
        for target in product(range(1, rank+1), repeat=d):
            count += 1
            coefficient = coefficient_from_paths(word, target, rank)
            if coefficient:
                out[target] = coefficient
    return out, count


def replace(word, images):
    out = ()
    for letter in word:
        out += images[letter] if letter > 0 else reverse(images[-letter])
    return freely_reduce(out)


def inverse_check(word, moving, rank):
    a = {j:(j,) for j in range(1, rank+1)}
    b = dict(a)
    a[moving] = (moving,) + word
    b[moving] = (moving,) + reverse(word)
    return all(replace(a[j], b) == replace(b[j], a) == (j,)
               for j in range(1, rank+1))


def show_poly(poly):
    return [{'word': list(m), 'coefficient': c} for m, c in sorted(poly.items())]


def run():
    w, v = examples()
    records = []
    checks = []
    for name, word, rank, degree, target, expected, moving in [
        ('w', w, 3, 5, (1,1,2,1,3), -1, 4),
        ('v', v, 2, 6, (1,1,1,2,1,2), 1, 3),
    ]:
        poly, evaluated = full_paths(word, rank, degree)
        need(poly.get(target) == expected, name + ' decisive coefficient')
        need({len(m) for m in poly} == {degree}, name + ' first nonzero degree')
        need(len(poly) == (12 if name == 'w' else 10), name + ' term count')
        retained = json.loads((NATIVE/'release/verification.json').read_text())
        field = 'p5_free_associative_terms' if name == 'w' else 'q6_free_associative_terms'
        need(show_poly(poly) == retained[field], name + ' frozen coefficient transcription')
        need(list(freely_reduce(word)) == retained[name+'5_reduced_word' if name == 'w' else 'v6_reduced_word'],
             name + ' frozen reduced-word transcription')
        witness = evaluate(word, path_matrices(target, rank))
        exact = eye(degree+1)
        exact[0][degree] = expected
        need(witness == exact, name + ' entire unitriangular witness')
        inverse_target = evaluate(reverse(word), path_matrices(target, rank))
        inverse_exact = eye(degree+1)
        inverse_exact[0][degree] = -expected
        need(inverse_target == inverse_exact, name + ' word inverse coefficient')
        need(evaluate(word + reverse(word), path_matrices(target, rank)) == eye(degree+1),
             name + ' unreduced group inverse')
        for n in [moving, moving+1, 8, 17]:
            need(inverse_check(word, moving, n), name + ' two-sided inverse rank ' + str(n))
        need(not inverse_check(word, 1, rank), name + ' invalid spare generator rejected')
        # In UT_degree, the last coefficient cannot be represented. Record this
        # as a deliberately insufficient witness, not a proof of nonmembership.
        need(evaluate(word, path_matrices(target[:-1], rank)) == eye(degree),
             name + ' too-small matrix negative control')
        need(coefficient_from_paths(word + word, target, rank) == 2*expected,
             name + ' integral doubled word')
        # Doubling all generator edges scales degree-d coefficient by 2^d.
        doubled = path_matrices(target, rank)
        for m in doubled:
            for i in range(len(m)):
                for j in range(i+1,len(m)):
                    m[i][j] *= 2
        need(evaluate(word, doubled)[0][-1] == expected*2**degree,
             name + ' weighted coefficient homogeneity')
        checks.extend([name+': full monomial inventory', name+': exact full UT witness',
                       name+': inverse sign', name+': unreduced cancellation',
                       name+': both compositions at four ranks', name+': invalid moving generator',
                       name+': insufficient dimension', name+': integral doubled word',
                       name+': weighted homogeneous coefficient'])
        records.append({'name': name, 'rank_of_word': rank, 'degree': degree,
                        'unreduced_word_length': len(word),
                        'reduced_word_length': len(freely_reduce(word)),
                        'path_matrix_evaluations': evaluated,
                        'target': list(target), 'coefficient': expected,
                        'full_witness': witness, 'full_nonzero_polynomial': show_poly(poly),
                        'automorphism_ranks_tested': [moving,moving+1,8,17]})
    # A convention change reversing only the outer commutator reverses its
    # leading class. This catches a sign error hidden by nonzero-only testing.
    a,b,c=(1,),(2,),(3,)
    wrong = commutator(a, commutator(commutator(a,b),commutator(a,c)))
    need(coefficient_from_paths(wrong,(1,1,2,1,3),3) == 1, 'outer swap')
    # Ordinary commutator is nonzero in degree two; commuting variables would
    # incorrectly annihilate it. Matrix path evaluation keeps order explicit.
    simple = commutator(a,b)
    need(coefficient_from_paths(simple,(1,2),2) == 1 and
         coefficient_from_paths(simple,(2,1),2) == -1, 'noncommuting letters')
    checks.extend(['outer commutator sign error', 'commuting-variable error'])
    return {'result':'PASS', 'arithmetic':'untruncated exact integer matrix products',
            'method':'colored paths in integral unitriangular matrices; no Magnus code import',
            'cases':records, 'check_families':checks, 'check_family_count':len(checks),
            'coefficient_path_matrix_evaluations':sum(x['path_matrix_evaluations'] for x in records),
            'author_code_imported_or_executed':False,
            'role':'finite exact checks supplement the written universal derivation'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
