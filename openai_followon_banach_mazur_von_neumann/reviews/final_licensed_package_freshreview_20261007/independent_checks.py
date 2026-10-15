"""Original finite checks for the fresh cohomology support review.

These calculations check identities and combinatorics, not infinite-dimensional
vanishing. Only Python's standard library is needed. Exact rational arithmetic
is used for matrix calculations.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import product
from math import comb, factorial
import json


def central_d(f, n):
    result = {}
    for a in product(range(2), repeat=n + 1):
        value = (a[0] == 0) * f[a[1:]]
        for j in range(1, n + 1):
            if a[j - 1] == a[j]:
                value += (-1) ** j * f[a[:j - 1] + (a[j],) + a[j + 1:]]
        value += (-1) ** (n + 1) * f[a[:-1]] * (a[-1] == 0)
        result[a] = value
    return result


def central_j(f, n):
    if n <= 1:
        return {(): 0}
    result = {}
    for a in product(range(2), repeat=n - 1):
        value = 0
        for i in range(1, n):
            if all(x == 0 for x in a[:i - 1]) and a[i - 1] == 1:
                value += (-1) ** i * f[a[:i - 1] + (1, 1) + a[i:]]
        result[a] = value
    return result


central_counts = {}
for n in range(1, 7):
    keys = list(product(range(2), repeat=n))
    checked = 0
    for basis in keys:
        f = {key: int(key == basis) for key in keys}
        dj = central_d(central_j(f, n), n - 1)
        jd = central_j(central_d(f, n), n + 1)
        for a in keys:
            cut = f[a] if all(x == 0 for x in a) else 0
            assert dj[a] + jd[a] == f[a] - cut, (n, basis, a)
            checked += 1
    central_counts[n] = checked


ZERO = (Q(0),) * 4
ONE = (Q(1), Q(0), Q(0), Q(1))
BASIS = tuple(tuple(Q(int(i == j)) for i in range(4)) for j in range(4))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(c, a):
    return tuple(c * x for x in a)


def mul(a, b):
    return tuple(sum(a[2*i + k] * b[2*k + j] for k in range(2))
                 for i in range(2) for j in range(2))


def transpose(a):
    return (a[0], a[2], a[1], a[3])


def h(a):
    return scale(Q(1, 11), transpose(a))


def g(a):
    return add(a, h(a))


def inverse_g(a):
    return scale(Q(121, 120), sub(a, h(a)))


def delta(a, b):
    return scale(Q(1, 7), add(mul(a, b), mul(b, a)))


def dh(a, b):
    return sub(add(mul(a, h(b)), mul(h(a), b)), h(mul(a, b)))


transport_pairs = 0
for x, y in product(BASIS, repeat=2):
    bx, by = inverse_g(x), inverse_g(y)
    actual = sub(g(add(mul(bx, by), delta(bx, by))), mul(x, y))
    expected = sub(add(sub(delta(bx, by), dh(bx, by)), h(delta(bx, by))),
                   mul(h(bx), h(by)))
    assert actual == expected
    transport_pairs += 1


def k(a):
    return add(a, scale(Q(1, 5), transpose(a)))


def inverse_k(a):
    return scale(Q(25, 24), sub(a, scale(Q(1, 5), transpose(a))))


def associative_mu(a, b):
    return inverse_k(mul(k(a), k(b)))


def associative_delta(a, b):
    return sub(associative_mu(a, b), mul(a, b))


associativity_triples = 0
for a, b, c in product(BASIS, repeat=3):
    D = associative_delta
    differential = sub(add(mul(a, D(b, c)), D(a, mul(b, c))),
                       add(D(mul(a, b), c), mul(D(a, b), c)))
    quadratic = sub(D(D(a, b), c), D(a, D(b, c)))
    assert differential == quadratic
    assert associative_mu(associative_mu(a, b), c) == associative_mu(a, associative_mu(b, c))
    associativity_triples += 1


def reduce_word(letters):
    stack = []
    for label, sign in letters:
        if stack and stack[-1] == (label, -sign):
            stack.pop()
        else:
            stack.append((label, sign))
    return stack


catalan_results = []
for d in range(1, 5):
    signs = tuple((-1) ** (i + 1) for i in range(2*d))
    for r in range(1, 6):
        leading = 0
        total = 0
        for labels in product(range(r), repeat=2*d):
            if not reduce_word(zip(labels, signs)):
                total += 1
                leading += len(set(labels)) == d
        falling = factorial(r) // factorial(r-d) if r >= d else 0
        catalan = comb(2*d, d) // (d + 1)
        assert leading == catalan * falling
        catalan_results.append({"d": d, "r": r, "total_identity_words": total,
                                "leading_exactly_d_labels": leading})


block_configurations = 0
for count in range(1, 4):
    for degrees in product(range(3), repeat=count):
        signs = tuple(s for d in degrees for s in (1, -1)*d + (1,))
        if len(signs) > 7:
            continue
        for labels in product(range(3), repeat=len(signs)):
            word = reduce_word(zip(labels, signs))
            assert word and word[0][1] == 1 and word[-1][1] == 1
            block_configurations += 1


result = {
    "status": "all_assertions_passed",
    "central_homotopy_exhaustive_basis_checks_C2_zC2": central_counts,
    "M2_transport_exact_rational_basis_pairs": transport_pairs,
    "M2_associativity_defect_exact_rational_basis_triples": associativity_triples,
    "Catalan_label_count_results": catalan_results,
    "ordered_block_exhaustive_three_label_configurations": block_configurations,
    "scope": "finite identities/combinatorics only; no verification of infinite-dimensional vanishing",
}
print(json.dumps(result, indent=2))
