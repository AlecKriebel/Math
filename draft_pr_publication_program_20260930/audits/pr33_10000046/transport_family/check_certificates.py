#!/usr/bin/env python3
"""Read-only independent certificate verifier. Imports no solver or old code.

Lower certificates: literal permutations / rational full couplings.
Upper certificates: literal Hall subsets whose neighborhoods are rederived.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
from math import factorial, prod
from pathlib import Path
import json

count = 0


def check(ok, label):
    global count
    if not ok:
        raise AssertionError(label)
    count += 1


def decode_path(label, d, n, start):
    digits = [0]*n
    for i in range(n-1, -1, -1):
        digits[i] = label % (2*d)
        label //= 2*d
    z = list(start)
    points = [tuple(z)]
    for letter in digits:
        z[letter//2] += (-1 if letter % 2 == 0 else 1)
        points.append(tuple(z))
    return tuple(points)


def finite(record):
    d, n, L = record['d'], record['N'], record['L']
    check(L == (2*d)**n, 'number of complete marginal words')
    left = [decode_path(i, d, n, (0,)*d) for i in range(L)]
    right = [decode_path(j, d, n, record['displacement']) for j in range(L)]
    check(record['event'] in ('synchronous', 'drop_zero', 'full'), 'recognized event')

    def safe(a, b):
        if record['event'] == 'synchronous':
            return all(a[k] != b[k] for k in range(n+1))
        if record['event'] == 'drop_zero':
            return not set(a[1:]).intersection(b[1:])
        return not set(a).intersection(b)

    perm = record['permutation']
    check(len(perm) == L and sorted(perm) == list(range(L)), 'both complete finite marginal laws')
    lower = sum(safe(left[i], right[j]) for i, j in enumerate(perm))
    A = record['Hall_A']
    check(len(set(A)) == len(A) and all(0 <= i < L for i in A), 'literal Hall set valid')
    neighbors = {j for i in A for j in range(L) if safe(left[i], right[j])}
    upper = L-len(A)+len(neighbors)
    check(lower == upper == record['safe_count'], 'permutation and Hall bound certify optimum')
    check(Fraction(lower, L) == Fraction(record['optimum']), 'recorded rational objective')


def weighted(record):
    p, q = list(map(Fraction, record['p'])), list(map(Fraction, record['q']))
    C = [list(map(Fraction, row)) for row in record['full_coupling']]
    check(sum(p) == sum(q) == 1 and all(a >= 0 for a in p+q), 'valid fixed finite marginal laws')
    check(len(C) == len(p) and all(len(row) == len(q) for row in C), 'coupling dimensions')
    check(all(a >= 0 for row in C for a in row), 'coupling nonnegative')
    check([sum(row) for row in C] == p, 'all weighted row masses exact')
    check([sum(row[j] for row in C) for j in range(len(q))] == q, 'all weighted column masses exact')
    E = {tuple(edge) for edge in record['E']}
    A = record['Hall_A']
    check(len(set(A)) == len(A) and all(0 <= i < len(p) for i in A), 'weighted Hall set valid')
    neighborhood = {j for i, j in E if i in A}
    upper = 1-sum(p[i] for i in A)+sum(q[j] for j in neighborhood)
    lower = sum(C[i][j] for i, j in E)
    check(lower == upper == Fraction(record['optimum']), 'rational primal and Hall dual equal')


def main():
    certificate = Path(__file__).with_name('certificates.json')
    data = json.loads(certificate.read_text())
    for record in data['finite']:
        finite(record)
    for record in data['weighted']+data['vanishing']:
        weighted(record)
    for record in data['first_hits']:
        absolute = [abs(a) for a in record['displacement']]
        check(len(absolute) == record['d'] and sum(absolute) == 10, 'actual graph distance ten')
        check(record['words'] == factorial(10)//prod(factorial(a) for a in absolute), 'shortest-word count')
    fake = [(Fraction(row['mass']), tuple(row['word'])) for row in data['fake_path_law']]
    check(len(fake) == 8 and sum(mass for mass, word in fake) == 1, 'fake law is normalized')
    for t in range(4):
        marginal = Counter()
        true = Counter()
        for mass, word in fake:
            marginal[sum(word[:t])] += mass
        for word in product((-1, 1), repeat=3):
            true[sum(word[:t])] += Fraction(1, 8)
        check(marginal == true, 'fake process has correct one-time law')
    check(any(mass != Fraction(1, 8) for mass, word in fake), 'fake process fails complete path law')
    print(json.dumps({'pass': True, 'checks': count,
                      'finite_certificates': len(data['finite']),
                      'rational_certificates': len(data['weighted'])+len(data['vanishing']),
                      'scope': 'Independent primal/Hall-dual and marginal certificate verification only'}, indent=2))


if __name__ == '__main__':
    main()
