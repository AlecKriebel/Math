#!/usr/bin/env python3
"""Exact, standard-library-only checks for AMR-084-0009. No exhaustive search."""
from fractions import Fraction as Q
from math import isqrt
import json
import sys
import unittest

ALMOST = tuple(map(Q, ('140/51', '2223/30464', '278817/33856', '3182740/17661')))
TRIPLE = tuple(map(Q, ('1976/5607', '3780/1691', '14596/1197')))
ZERO_EDGE = tuple(map(Q, ('37620/26299', '195/28', '-28/195')))

def root(q):
    q = Q(q)
    if q < 0:
        return None
    n, d = isqrt(q.numerator), isqrt(q.denominator)
    return Q(n, d) if n*n == q.numerator and d*d == q.denominator else None

def conditions(values):
    values = tuple(map(Q, values))
    out = []
    for i in range(len(values)):
        for j in range(i, len(values)):
            q = values[i]*values[j]+1
            r = root(q)
            out.append({'pair': [i+1, j+1], 'value': str(q),
                        'root': None if r is None else str(r)})
    return out

def strong(values):
    values = tuple(map(Q, values))
    if not values or any(x == 0 for x in values):
        return False
    if len(set(values)) != len(values):
        return False
    return all(row['root'] is not None for row in conditions(values))

def d_of_t(t):
    t = Q(t)
    if not t:
        raise ValueError('t must be nonzero')
    return (t*t-1)/(2*t)

def f(a, t):
    a, t = Q(a), Q(t)
    return 2*t*(a*t*t+2*t-a)

def extension(base, t):
    base = tuple(map(Q, base))
    d = d_of_t(t)
    return (strong(base) and d != 0 and d not in base
            and all(root(f(a, t)) is not None for a in base))

def genus(k):
    if not isinstance(k, int) or k < 1:
        raise ValueError('k must be a positive integer')
    degree, branch_points = 2**k, 2*k+2
    return 1 + Q(-2*degree + branch_points*(degree//2), 2)

def positive_normalization(values):
    values = tuple(map(Q, values))
    if not strong(values):
        raise ValueError('input must be a strong tuple')
    if any(values[i]*values[j]+1 == 0 for i in range(len(values))
           for j in range(i+1, len(values))):
        raise ValueError('zero cross-products excluded from this normalization')
    if max(values) < 0:
        values = tuple(-x for x in values)
    pivot = max(values)
    return (pivot,) + tuple((pivot-b)/(pivot*b+1) for b in values if b != pivot)

def regular_extensions(triple):
    a, b, c = map(Q, triple)
    r, s, t = root(a*b+1), root(a*c+1), root(b*c+1)
    if None in (r, s, t):
        raise ValueError('not an ordinary Diophantine triple')
    return tuple(a+b+c+2*a*b*c+sign*2*r*s*t for sign in (-1, 1))

def certificate():
    regular = []
    for d in regular_extensions(TRIPLE):
        regular.append({'d': str(d), 'cross_roots': [str(root(a*d+1)) for a in TRIPLE],
                        'diagonal': str(d*d+1), 'diagonal_root': root(d*d+1)})
    return {'problem_id': 8500009, 'outcome': 'PARTIAL; existence unresolved',
            'almost_conditions': conditions(ALMOST),
            'published_positive_triple': conditions(TRIPLE),
            'published_zero_edge_triple': conditions(ZERO_EDGE),
            'regular_extensions': regular,
            'genus_by_fixed_base_size': {str(k): str(genus(k)) for k in (1, 2, 3)},
            'nonlifting_quotient_witness': {'base': ['3/4', '-4/3'], 't': '3/4',
                'd': '-7/24', 'cross_values': ['25/32', '25/18'],
                'product': '625/576', 'product_root': '25/24',
                'individual_values_are_squares': False},
            'scope': 'Exact fixtures and identities only; no rational-point enumeration or completeness claim.'}

class ExactTests(unittest.TestCase):
    def test_square_predicate(self):
        for q, expected in [(Q(0), Q(0)), (Q(25,36), Q(5,6)), (Q(2), None),
                            (Q(-1), None), (Q(10**40+1), None)]:
            self.assertEqual(root(q), expected)

    def test_almost_all_ten(self):
        rows = conditions(ALMOST)
        self.assertEqual(len(rows), 10)
        self.assertEqual([r['pair'] for r in rows if r['root'] is None], [[3,4]])
        self.assertEqual(rows[8]['value'], '459627303/309488')
        self.assertFalse(strong(ALMOST))
        for r in rows:
            if r['root'] is not None:
                self.assertEqual(Q(r['root'])**2, Q(r['value']))
        q = Q(rows[8]['value'])
        self.assertTrue(21438**2 < q.numerator < 21439**2)
        self.assertTrue(556**2 < q.denominator < 557**2)

    def test_invalid_tuples_and_printed_typo(self):
        self.assertFalse(strong([1,3,8,120]))
        self.assertFalse(strong(TRIPLE + (Q(0),)))
        self.assertFalse(strong((TRIPLE[0],)*4))
        typo = (ALMOST[0], Q(2223,3046), ALMOST[2], ALMOST[3])
        self.assertFalse(strong(typo))
        self.assertIsNone(root(typo[1]**2+1))

    def test_known_triples(self):
        self.assertTrue(strong(TRIPLE))
        self.assertTrue(strong(ALMOST[:3]))
        self.assertTrue(strong((ALMOST[0],ALMOST[1],ALMOST[3])))
        self.assertTrue(strong(ZERO_EDGE))
        self.assertEqual(ZERO_EDGE[1]*ZERO_EDGE[2]+1, 0)

    def test_diagonal_and_cover_identities(self):
        for n in range(-9,10):
            for m in range(1,8):
                if not n:
                    continue
                t = Q(n,m)
                d = d_of_t(t)
                self.assertEqual(d*d+1, ((t*t+1)/(2*t))**2)
                for a in ALMOST + ZERO_EDGE:
                    self.assertEqual(f(a,t), (2*t)**2*(a*d+1))
        with self.assertRaises(ValueError):
            d_of_t(0)

    def test_extension_lifting(self):
        base = ALMOST[:2]
        for d in ALMOST[2:]:
            s = root(d*d+1)
            for t in (d+s, d-s):
                self.assertTrue(extension(base,t))
                self.assertEqual(d_of_t(t),d)
        for t in (Q(1),Q(-1)):
            self.assertFalse(extension(base,t))
        for d in base:
            self.assertFalse(extension(base, d+root(d*d+1)))
        # Zero value in one cross-condition is allowed, not automatically discarded.
        b = ZERO_EDGE[:2]
        d = ZERO_EDGE[2]
        self.assertTrue(extension(b, d+root(d*d+1)))
        # Nonzero product-square witness that fails both individual square tests.
        base = (Q(3,4),Q(-4,3))
        t, d = Q(3,4), Q(-7,24)
        self.assertTrue(strong(base))
        self.assertEqual(d_of_t(t),d)
        u,v = (a*d+1 for a in base)
        self.assertEqual((u,v),(Q(25,32),Q(25,18)))
        self.assertEqual(root(u*v),Q(25,24))
        self.assertIsNone(root(u)); self.assertIsNone(root(v))
        self.assertFalse(extension(base,t))

    def test_branch_roots_and_genus(self):
        for base in (ALMOST[:2],TRIPLE,ZERO_EDGE):
            roots = []
            for a in base:
                s = root(a*a+1)
                for r in ((-1+s)/a,(-1-s)/a):
                    self.assertNotEqual(r,0)
                    self.assertEqual(a*r*r+2*r-a,0)
                    self.assertNotIn(r,roots)
                    roots.append(r)
        self.assertEqual([genus(k) for k in (1,2,3)], [1,3,9])

    def test_sign_normalization_and_zero_guard(self):
        signed = (Q(140,51),Q(187,84),Q(-427,1836))
        for values in (TRIPLE,signed,tuple(-x for x in signed)):
            normalized = positive_normalization(values)
            self.assertTrue(strong(normalized))
            self.assertTrue(all(x>0 for x in normalized))
            a = max(values) if max(values)>0 else max(-x for x in values)
            vals = values if max(values)>0 else tuple(-x for x in values)
            for b in vals:
                if b == a: continue
                e = (a-b)/(a*b+1)
                self.assertEqual(a*e+1,(a*a+1)/(a*b+1))
                self.assertEqual(e*e+1,(a*a+1)*(b*b+1)/(a*b+1)**2)
                for c in vals:
                    if c == a: continue
                    h = (a-c)/(a*c+1)
                    self.assertEqual(e*h+1,(a*a+1)*(b*c+1)/((a*b+1)*(a*c+1)))
        with self.assertRaises(ValueError):
            positive_normalization(ZERO_EDGE)

    def test_regular_extensions_do_not_solve(self):
        ds = regular_extensions(TRIPLE)
        self.assertEqual(ds,(Q(135938,106533),Q(789662,11837)))
        for d in ds:
            self.assertTrue(all(root(a*d+1) is not None for a in TRIPLE))
            self.assertIsNone(root(d*d+1))
            self.assertFalse(strong(TRIPLE+(d,)))

if __name__ == '__main__':
    if '--test' in sys.argv:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
    else:
        print(json.dumps(certificate(), indent=2, sort_keys=True))
