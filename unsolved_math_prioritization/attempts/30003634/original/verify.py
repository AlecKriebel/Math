#!/usr/bin/env python3
"""Exact, standard-library certificate replay. No assert statements or writes."""
from fractions import Fraction
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import sys

class VerificationError(Exception):
    pass

def require(condition, message):
    if not condition:
        raise VerificationError(message)

def integer(x):
    return type(x) is int

def reduce_word(word):
    result = []
    for x in word:
        require(integer(x) and x in (-2, -1, 1, 2), 'invalid Artin letter')
        if result and result[-1] == -x:
            result.pop()
        else:
            result.append(x)
    return tuple(result)

def inverse(word):
    return tuple(-x for x in word[::-1])

def commutator(u, v):
    return reduce_word(u + v + inverse(u) + inverse(v))

def candidate():
    a, b = (1, 1), (2, 2)
    c = commutator(a, b)
    d = reduce_word(inverse(a) + c + a)
    e = reduce_word(inverse(b) + c + b)
    u, v = commutator(c, d), commutator(d, e)
    return commutator(u, v)

def linking(word):
    labels = [0, 1, 2]
    counts = {(0, 1): 0, (0, 2): 0, (1, 2): 0}
    for s in word:
        i = abs(s) - 1
        pair = tuple(sorted((labels[i], labels[i + 1])))
        counts[pair] += 1 if s > 0 else -1
        labels[i], labels[i + 1] = labels[i + 1], labels[i]
    require(labels == [0, 1, 2], 'word is not pure')
    require(all(x % 2 == 0 for x in counts.values()), 'odd linking crossing sum')
    return [counts[k] // 2 for k in sorted(counts)]

def cyclic_runs(word):
    word = reduce_word(word)
    while word and word[0] == -word[-1]:
        word = word[1:-1]
    require(word and {abs(x) for x in word} == {1, 2}, 'two generators required')
    start = next(i for i in range(len(word)) if abs(word[i]) == 1 and abs(word[i-1]) == 2)
    word = word[start:] + word[:start]
    runs = []
    for s in word:
        if runs and runs[-1][0] == abs(s):
            runs[-1][1] += 1 if s > 0 else -1
        else:
            runs.append([abs(s), 1 if s > 0 else -1])
    require(len(runs) >= 4 and len(runs) % 2 == 0, 'at least two alternating pairs required')
    require(all(g == i % 2 + 1 and e != 0 for i, (g, e) in enumerate(runs)), 'invalid cyclic syllables')
    return [e for g, e in runs]

def goeritz(word):
    runs = cyclic_runs(word)
    size = sum(abs(x) for x in runs[1::2])
    require(size >= 3, 'cycle must have at least three vertices')
    matrix = [[0] * size for _ in range(size)]
    start = 0
    for a, b in zip(runs[0::2], runs[1::2]):
        matrix[start][start] += a
        sign = 1 if b > 0 else -1
        for k in range(abs(b)):
            i, j = (start + k) % size, (start + k + 1) % size
            matrix[i][i] -= sign
            matrix[j][j] -= sign
            matrix[i][j] += sign
            matrix[j][i] += sign
        start += abs(b)
    return matrix, sum(runs[0::2]), runs

def inertia(matrix):
    require(all(len(row) == len(matrix) for row in matrix), 'nonsquare matrix')
    require(all(matrix[i][j] == matrix[j][i] for i in range(len(matrix)) for j in range(len(matrix))), 'nonsymmetric matrix')
    a = [[Fraction(x) for x in row] for row in matrix]
    positive = negative = zero = 0
    pivots = []
    while a:
        n = len(a)
        i = next((i for i in range(n) if a[i][i]), None)
        if i is not None:
            a[0], a[i] = a[i], a[0]
            for row in a:
                row[0], row[i] = row[i], row[0]
            pivot = a[0][0]
            positive += pivot > 0
            negative += pivot < 0
            pivots.append(str(pivot))
            a = [[a[j][k] - a[j][0] * a[0][k] / pivot for k in range(1, n)] for j in range(1, n)]
        else:
            pair = next(((i, j) for i in range(n) for j in range(i+1, n) if a[i][j]), None)
            if pair is None:
                zero += n
                break
            order = list(pair) + [k for k in range(n) if k not in pair]
            a = [[a[i][j] for j in order] for i in order]
            pivot = a[0][1]
            positive += 1
            negative += 1
            pivots.append(['0', str(pivot), '0'])
            a = [[a[j][k] - (a[j][0] * a[1][k] + a[j][1] * a[0][k]) / pivot for k in range(2, n)] for j in range(2, n)]
    return [positive, negative, zero], pivots

def determinant(matrix):
    a = [row[:] for row in matrix]
    n = len(a)
    if n == 0:
        return 1
    prev = sign = 1
    for k in range(n-1):
        if a[k][k] == 0:
            i = next((i for i in range(k+1, n) if a[i][k]), None)
            if i is None:
                return 0
            a[k], a[i] = a[i], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k+1, n):
            for j in range(k+1, n):
                value = a[i][j] * pivot - a[i][k] * a[k][j]
                require(value % prev == 0, 'Bareiss nonintegral division')
                a[i][j] = value // prev
        for i in range(k+1, n):
            a[i][k] = 0
        prev = pivot
    return sign * a[-1][-1]

def multiply(a, b):
    x, y, z, t = a
    u, v, w, s = b
    return (x*u+y*w, x*v+y*s, z*u+t*w, z*v+t*s)

def meyer_generator(a, letter):
    # e = (A^{-1}-I)v1 = (I-B)v2; q(e)=det(v1+v2,e).
    eps = 1 if letter > 0 else -1
    x, y, z, t = a
    aa, bb, cc, dd = t-1, -y, -z, x-1
    ex, ey = (0, 1) if abs(letter) == 1 else (1, 0)
    det = aa*dd - bb*cc
    if det:
        vx = Fraction(dd*ex-bb*ey, det)
        vy = Fraction(aa*ey-cc*ex, det)
    else:
        if aa == bb == cc == dd == 0:
            return 0
        if aa*ey-cc*ex or bb*ey-dd*ex:
            return 0
        if aa:
            vx, vy = Fraction(ex, aa), Fraction(0)
        elif bb:
            vx, vy = Fraction(0), Fraction(ex, bb)
        elif cc:
            vx, vy = Fraction(ey, cc), Fraction(0)
        else:
            vx, vy = Fraction(0), Fraction(ey, dd)
    value = vx + eps if abs(letter) == 1 else eps - vy
    return (value > 0) - (value < 0)

def meyer_signature(word):
    a = (1, 0, 0, 1)
    terms = []
    for letter in word:
        terms.append(meyer_generator(a, letter))
        eps = 1 if letter > 0 else -1
        b = (1, 0, -eps, 1) if abs(letter) == 1 else (1, eps, 0, 1)
        a = multiply(a, b)
    return -sum(terms), list(a), terms

def no_duplicate_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result

def load_certificate(path):
    raw = path.read_bytes()
    require(len(raw) <= 250000, 'oversized certificate')
    value = json.loads(raw, object_pairs_hook=no_duplicate_pairs,
                       parse_constant=lambda x: (_ for _ in ()).throw(VerificationError('nonfinite JSON constant')))
    def strict_types(x):
        require(type(x) in (dict, list, str, int), 'unsupported JSON value type')
        if type(x) is dict:
            for k, v in x.items():
                require(type(k) is str, 'invalid JSON key')
                strict_types(v)
        elif type(x) is list:
            for v in x:
                strict_types(v)
    strict_types(value)
    return value

def verify_certificate(cert):
    fields = {'schema', 'problem_id', 'n', 'm', 'derived_level', 'word', 'syllables',
              'pairwise_linking', 'goeritz', 'goeritz_inertia', 'goeritz_pivots',
              'goeritz_determinant', 'goeritz_correction', 'signature', 'burau_matrix', 'meyer_terms'}
    require(type(cert) is dict and set(cert) == fields, 'certificate fields mismatch')
    require(cert['schema'] == 'derived-pure-braid-counterexample-v1', 'wrong schema')
    for key, expected in [('problem_id', 30003634), ('n', 1), ('m', 3), ('derived_level', 3), ('signature', -2), ('goeritz_correction', 0), ('goeritz_determinant', -7154819319988224)]:
        require(integer(cert[key]) and cert[key] == expected, 'false claim: ' + key)
    require(type(cert['word']) is list and all(integer(x) for x in cert['word']), 'bad word type')
    word = candidate()
    require(len(word) == 104 and cert['word'] == list(word), 'word does not match nested commutator certificate')
    require(cert['pairwise_linking'] == linking(word) == [0, 0, 0], 'nonzero linking')
    matrix, correction, runs = goeritz(word)
    require(all(type(row) is list and all(integer(x) for x in row) for row in cert['goeritz']), 'bad matrix entry type')
    require(cert['goeritz'] == matrix and len(matrix) == 48, 'Goeritz matrix mismatch')
    require(cert['syllables'] == runs and all(integer(x) for x in cert['syllables']), 'syllable mismatch')
    it, pivots = inertia(matrix)
    require(cert['goeritz_inertia'] == it == [23, 25, 0], 'false inertia')
    require(cert['goeritz_pivots'] == pivots, 'congruence pivot mismatch')
    require(correction == 0 and it[0]-it[1]-correction == -2, 'signature correction failure')
    require(determinant(matrix) == cert['goeritz_determinant'], 'determinant mismatch')
    sig, burau, terms = meyer_signature(word)
    require(sig == -2 and cert['burau_matrix'] == burau and cert['meyer_terms'] == terms, 'Meyer cross-check mismatch')
    require(burau[0]*burau[3]-burau[1]*burau[2] == 1, 'Burau determinant failure')
    return word

def controls(word):
    count = 0
    for matrix, expected in [([], [0,0,0]), ([[0]], [0,0,1]), ([[0,1],[1,0]], [1,1,0]), ([[2,0],[0,-3]], [1,1,0]), ([[0,0],[0,0]], [0,0,2]), ([[1,1],[1,1]], [1,0,1])]:
        require(inertia(matrix)[0] == expected, 'inertia control failure')
        count += 1
    for w, expected in [((2,2,2),-2), ((1,2)*6,-8), ((2,2,2,-1,2,-1),-2), ((1,2,1),-1), (word,-2), (inverse(word),2), (word*2,-4)]:
        require(meyer_signature(w)[0] == expected, 'Meyer normalization failure')
        count += 1
    # Independent Goeritz/Meyer comparisons on all 256 four-syllable words.
    for powers in itertools.product((-4,-2,2,4), repeat=4):
        w = tuple(s for i,p in enumerate(powers) for s in [(i%2+1)*(1 if p>0 else -1)]*abs(p))
        matrix, correction, _ = goeritz(w)
        it, _ = inertia(matrix)
        require(it[0]-it[1]-correction == meyer_signature(w)[0], 'two-signature control mismatch')
        count += 1
    for u in [word, inverse(word), word*2, (1,2)*6, (1,1,2,2,-1,-1,-2,-2)]:
        g, mu, _ = goeritz(u)
        it, _ = inertia(g)
        require(it[0]-it[1]-mu == meyer_signature(u)[0], 'large signature control mismatch')
        count += 1
    for prefix in [(), (1,), (-2,1), (1,2,-1,-2)]:
        for suffix in [(), (-1,), (2,1)]:
            left = prefix + (1,2,1) + suffix
            right = prefix + (2,1,2) + suffix
            require(meyer_signature(left)[0] == meyer_signature(right)[0], 'braid relation signature mismatch')
            require(meyer_signature(left)[1] == meyer_signature(right)[1], 'braid relation matrix mismatch')
            count += 1
    return count

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate', nargs='?', default=str(Path(__file__).resolve().with_name('certificate.json')))
    args = parser.parse_args()
    cert = load_certificate(Path(args.certificate))
    word = verify_certificate(cert)
    count = controls(word)
    result = {'status': 'PASS_EXACT_CERTIFICATE', 'problem_id':30003634, 'n':1, 'm':3,
              'derived_level':3, 'word_length':104, 'goeritz_dimension':48,
              'goeritz_inertia':[23,25,0], 'signature':-2, 'additional_controls':count,
              'scope':'Finite certificate replay; topology theorem and source hypotheses require mathematical review.'}
    print(json.dumps(result, sort_keys=True, separators=(',', ':')))

if __name__ == '__main__':
    try:
        main()
    except (VerificationError, ValueError, TypeError, KeyError, IndexError, OSError, StopIteration) as error:
        print('REJECT: ' + str(error), file=sys.stderr)
        sys.exit(1)
