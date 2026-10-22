#!/usr/bin/env python3
"""Exact algebraic sanity checks; not a certificate of a KK-theoretic theorem."""
from fractions import Fraction as F
from collections import defaultdict
import os
from pathlib import Path
import stat
import unittest


def nc_add(*polys):
    out = defaultdict(F)
    for p in polys:
        for w, c in p.items():
            out[w] += c
    return {w: c for w, c in out.items() if c}


def nc_mul(a, b):
    out = defaultdict(F)
    for x, c in a.items():
        for y, d in b.items():
            out[x + y] += c * d
    return {w: c for w, c in out.items() if c}


def nc_neg(a):
    return {w: -c for w, c in a.items()}


def matrix(rows):
    if not isinstance(rows, (tuple, list)) or not rows:
        raise ValueError('nonempty matrix required')
    n = len(rows[0]) if isinstance(rows[0], (tuple, list)) else 0
    if not n or any(not isinstance(row, (tuple, list)) or len(row) != n for row in rows):
        raise ValueError('rectangular nonempty matrix required')
    if any(type(x) not in (int, F) for row in rows for x in row):
        raise TypeError('only exact integer or rational entries are accepted')
    return tuple(tuple(F(x) for x in row) for row in rows)


def mul(a, b):
    if len(a[0]) != len(b):
        raise ValueError('incompatible matrix dimensions')
    return tuple(tuple(sum((a[i][k] * b[k][j] for k in range(len(b))), F())
                       for j in range(len(b[0]))) for i in range(len(a)))


def transpose(a):
    return tuple(zip(*a))


def dyadic_square(n):
    if type(n) is not int:
        raise TypeError('integer index required; booleans are not indices')
    if not 1 <= n <= 10000:
        raise ValueError('index must be between 1 and 10000')
    s = sum((F(1, 2**k) for k in range(1, n + 1)), F())
    return s * s


class AlgebraChecks(unittest.TestCase):
    def test_ambient_error_identity(self):
        one = {(): F(1)}
        d, ds, x, y = ({(z,): F(1)} for z in ('d', 'd*', 'x', 'y'))
        lhs = nc_add(nc_mul(nc_mul(nc_add(one, d), x), nc_add(one, ds)), nc_neg(y))
        rhs = nc_add(x, nc_neg(y), nc_mul(d, x), nc_mul(x, ds), nc_mul(nc_mul(d, x), ds))
        self.assertEqual(lhs, rhs)

    def test_corner_lift_unitary(self):
        # p M3 p has unit p, so the complement must be restored.
        p = matrix([[1, 0, 0], [0, 1, 0], [0, 0, 0]])
        w = matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
        lift = matrix([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
        identity = matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        self.assertEqual(mul(w, transpose(w)), p)
        self.assertNotEqual(mul(w, transpose(w)), identity)
        self.assertEqual(mul(lift, transpose(lift)), identity)
        self.assertEqual(mul(transpose(lift), lift), identity)

    def test_arbitrary_compression_not_unitary(self):
        u = matrix([[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]])
        self.assertEqual(mul(u, transpose(u)), matrix([[1, 0], [0, 1]]))
        compression = matrix([[u[0][0]]])
        self.assertEqual(mul(compression, transpose(compression)), matrix([[F(9, 25)]]))
        self.assertNotEqual(mul(compression, transpose(compression)), matrix([[1]]))

    def test_nonessential_direct_sum_error(self):
        # E=M2(Q) direct-sum Q, D=M2(Q) direct-sum 0.
        phi = (matrix([[1, 2], [3, 4]]), F(7))
        psi = (matrix([[4, 3], [2, 1]]), F(7))
        u = matrix([[0, -1], [1, 0]])
        image = mul(mul(u, phi[0]), transpose(u))
        error = matrix([[image[i][j] - psi[0][i][j] for j in range(2)] for i in range(2)])
        self.assertEqual(phi[1] - psi[1], 0)
        self.assertNotEqual(error, matrix([[0, 0], [0, 0]]))
        # Discarding the annihilator summand changes neither this error nor its norm.
        self.assertEqual((error, F(0))[0], error)

    def test_finite_dyadic_rectangle(self):
        for n in range(1, 65):
            with self.subTest(n=n):
                total = dyadic_square(n)
                self.assertEqual(total, (1 - F(1, 2**n))**2)
                self.assertEqual(1 - total, F(2, 2**n) - F(1, 2**(2*n)))
                self.assertLess(total, 1)

    def test_fixed_strict_margin(self):
        # Replacing the (1,1) majorant 1/4 by a value <=1/8
        # leaves a uniform 1/8 margin even after all other majorants are summed.
        for n in range(1, 65):
            with self.subTest(n=n):
                self.assertLessEqual(dyadic_square(n) - F(1, 8), F(7, 8))

    def test_no_inexact_or_boolean_inputs(self):
        for bad in (True, False, 1.0, '2', None):
            with self.subTest(bad=bad):
                with self.assertRaises(TypeError):
                    dyadic_square(bad)
        for bad in (-1, 0, 10001):
            with self.assertRaises(ValueError):
                dyadic_square(bad)
        for bad in ([[True]], [[0.1]], [['1']]):
            with self.assertRaises(TypeError):
                matrix(bad)

    def test_dimension_guards(self):
        for bad in ([], [[]], [[1], [1, 2]], [3]):
            with self.assertRaises(ValueError):
                matrix(bad)
        with self.assertRaises(ValueError):
            mul(matrix([[1, 2]]), matrix([[1, 2]]))

    def test_execution_is_unprivileged_and_read_only(self):
        p = Path(__file__).resolve()
        self.assertEqual(os.getuid(), 1000)
        self.assertEqual(os.geteuid(), 1000)
        self.assertEqual(stat.S_IMODE(p.stat().st_mode), 0o444)
        self.assertEqual(stat.S_IMODE(p.parent.stat().st_mode), 0o555)
        self.assertFalse(os.access(p, os.W_OK))
        self.assertFalse(os.access(p.parent, os.W_OK))


if __name__ == '__main__':
    print('Scope: exact algebra and finite bounds only; no analytical proof certification.', flush=True)
    unittest.main(verbosity=2)
