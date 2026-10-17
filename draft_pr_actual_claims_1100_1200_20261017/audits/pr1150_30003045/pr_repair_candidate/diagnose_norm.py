#!/usr/bin/env python3
"""Exact characteristic-two diagnostics. The universal argument is in COUNTEREXAMPLE.md.

Sparse Laurent polynomials over F2. No finite-field specialization: variables
remain formal. Ordinary exceptions remain operative with Python -O.
"""
import json
from itertools import product


def require(test, message):
    if not test:
        raise ValueError(message)


def add(a, b):
    return a ^ b


def mul(a, b):
    out = set()
    for x in a:
        for y in b:
            z = tuple(u + v for u, v in zip(x, y))
            if z in out:
                out.remove(z)
            else:
                out.add(z)
    return out


def var(n, i):
    return {tuple(int(j == i) for j in range(n))}


def one(n):
    return {(0,) * n}


def power(a, n):
    out = one(len(next(iter(a))))
    for _ in range(n):
        out = mul(out, a)
    return out


def pair_mul(p, q, s):
    # pi^2 = s*pi+s. A+B*pi times C+D*pi.
    a, b = p
    c, d = q
    bd = mul(b, d)
    return add(mul(a, c), mul(s, bd)), add(add(mul(a, d), mul(b, c)), mul(s, bd))


def norm(p, s):
    a, b = p
    return add(add(mul(a, a), mul(s, mul(a, b))), mul(s, mul(b, b)))


def valuation(p):
    return min(m[0] for m in p) if p else None


def main():
    n = 5
    s, a, b, c, d = [var(n, i) for i in range(n)]
    zero = set()
    conjugate = (add(a, mul(s, b)), b)
    actual = pair_mul((a, b), conjugate, s)
    require(actual == (norm((a, b), s), zero), 'formal conjugate norm identity')
    require(norm(pair_mul((a, b), (c, d), s), s) == mul(norm((a, b), s), norm((c, d), s)), 'formal norm multiplicativity')
    require(norm((zero, one(n)), s) == s, 'uniformizer has norm s')

    # k(s) representation formula with z^2=y, coefficients formal and independent.
    # Pair representation U+V*z; multiplication uses z^2=y.
    y, p0, p1, q0, q1 = [var(5, i) for i in range(5)]
    def z_mul(p, q):
        aa, bb = p
        cc, dd = q
        return add(mul(aa, cc), mul(y, mul(bb, dd))), add(mul(aa, dd), mul(bb, cc))
    numerator = z_mul((p0, p1), (q0, q1))
    denominator = add(mul(q0, q0), mul(y, mul(q1, q1)))
    require(z_mul((q0, q1), (q0, q1)) == (denominator, zero), 'formal denominator rationalization')
    require(z_mul(numerator, (q0, q1)) == (mul(denominator, p0), mul(denominator, p1)), 'universal rational decomposition identity')

    # Formal F2[x,y]-valued Laurent polynomials in s, all leading valuations -15..15.
    # Nonzero coefficient choices include nonconstant and repeated terms.
    s3 = var(3, 0)
    all_vals = 0
    unit_cases = 0
    nonunit_cases = 0
    for va, vb in product(range(-15, 16), repeat=2):
        aa = {(va, 1, 0), (va + 1, 0, 1), (va + 3, 2, 1)}
        bb = {(vb, 0, 1), (vb + 2, 1, 0), (vb + 3, 1, 1)}
        nn = norm((aa, bb), s3)
        expected = min(2 * va, 1 + 2 * vb)
        require(valuation(nn) == expected, 'norm valuation parity failed')
        if expected == 0:
            require(va == 0 and vb >= 0, 'unit norm coefficient conditions')
            residues = {m for m in nn if m[0] == 0}
            square_residue = mul({m for m in aa if m[0] == 0}, {m for m in aa if m[0] == 0})
            require(residues == square_residue, 'unit norm square residue')
            unit_cases += 1
        else:
            nonunit_cases += 1
        all_vals += 1
    for vv in range(-15, 16):
        aa = {(vv, 1, 0)}
        require(valuation(norm((aa, zero), s3)) == 2 * vv, 'B=0 valuation')
        require(valuation(norm((zero, aa), s3)) == 1 + 2 * vv, 'A=0 valuation')

    # Adversarial sign/normalization sanity: omitting the odd exponent term,
    # or reversing uniformizer norm, changes actual formal polynomials.
    require(norm((zero, one(3)), s3) != one(3), 'uniformizer is not a norm-unit')
    require(norm((zero, one(3)), s3) != {(2, 0, 0)}, 'uniformizer norm exponent not two')
    require(norm((zero, one(3)), s3) != {(-1, 0, 0)}, 'uniformizer norm not inverse s')
    print(json.dumps({'status':'PASS','formal_norm_identities':3,'formal_rational_decomposition_identities':2,'valuation_pairs':all_vals,'unit_cases':unit_cases,'nonunit_cases':nonunit_cases,'zero_coefficient_cases':62,'computed_normalization_sanity_checks':3,'meaning':'Exact diagnostics only; universal proofs do not follow by sample count.'},sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
