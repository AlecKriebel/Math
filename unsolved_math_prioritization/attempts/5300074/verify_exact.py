#!/usr/bin/env python3
"""Read-only exact arithmetic checks for the partial-results packet.

These finite checks are not a verifier for the analytic dynamical arguments.
Run with Python normally, -O, or -OO. No files or network resources are written.
"""

from fractions import Fraction as Q
from math import gcd
import unittest


def fractional_part(x):
    return x - x.numerator // x.denominator


def sigma(d, x):
    return fractional_part(d * x)


class FiniteRotationLift:
    """Affine-gap degree-one lift of a finite cyclic-order-preserving set."""

    def __init__(self, d, angles):
        if d < 2:
            raise ValueError("Degree must be at least two")
        self.d = d
        a = sorted(set(Q(t) for t in angles))
        if not a or a[0] < 0 or a[-1] >= 1:
            raise ValueError("Angles must be a nonempty subset of [0,1)")
        image = [sigma(d, x) for x in a]
        if set(image) != set(a):
            raise ValueError("This finite set is not invariant and surjective")
        m = len(a)
        order = [a.index(y) for y in image]
        shift = order[0]
        if any(order[i] != (i + shift) % m for i in range(m)):
            raise ValueError("The cyclic order is not preserved")
        values = [image[0]]
        for y in image[1:]:
            while y < values[-1]:
                y += 1
            values.append(y)
        a.append(a[0] + 1)
        values.append(values[0] + 1)
        slopes = [(values[i + 1] - values[i]) / (a[i + 1] - a[i])
                  for i in range(m)]
        if any(s < 0 or s > d for s in slopes):
            raise ValueError("The bounded-slope conclusion failed")
        self.x = a
        self.y = values
        self.slopes = slopes
        self.rotation = Q(shift, m)

    def __call__(self, t):
        t = Q(t)
        shift = (t - self.x[0]).numerator // (t - self.x[0]).denominator
        u = t - shift
        for j in range(len(self.slopes)):
            if self.x[j] <= u <= self.x[j + 1]:
                return self.y[j] + self.slopes[j] * (u - self.x[j]) + shift
        raise RuntimeError("A degree-one fundamental interval was missed")

    def iterate(self, t, n):
        for _ in range(n):
            t = self(t)
        return t


class ExactChecks(unittest.TestCase):
    def test_named_rotation_sets(self):
        cases = [
            (2, [Q(0)], Q(0)),
            (2, [Q(1, 3), Q(2, 3)], Q(1, 2)),
            (2, [Q(1, 7), Q(2, 7), Q(4, 7)], Q(1, 3)),
            (2, [Q(3, 7), Q(5, 7), Q(6, 7)], Q(2, 3)),
            (3, [Q(0), Q(1, 2)], Q(0)),
            (3, [Q(1, 8), Q(1, 4), Q(3, 8), Q(3, 4)], Q(1, 2)),
        ]
        for d, angles, rotation in cases:
            f = FiniteRotationLift(d, angles)
            self.assertEqual(f.rotation, rotation)
            for x in angles:
                self.assertEqual(fractional_part(f(x)), sigma(d, x))
            q = rotation.denominator
            p = rotation.numerator
            x = min(angles)
            self.assertEqual(f.iterate(x, q) - x, p)
            for k in range(-20, 21):
                x = Q(k, 7)
                self.assertEqual(f(x + 1), f(x) + 1)

    def test_small_periodic_orbits(self):
        checked = 0
        for d in range(2, 7):
            for denominator in range(2, 71):
                if gcd(d, denominator) != 1:
                    continue
                unseen = {Q(k, denominator) for k in range(denominator)}
                while unseen:
                    start = min(unseen)
                    orbit = []
                    x = start
                    while x not in orbit:
                        orbit.append(x)
                        x = sigma(d, x)
                    self.assertEqual(x, start)
                    unseen.difference_update(orbit)
                    a = sorted(orbit)
                    indices = [a.index(sigma(d, t)) for t in a]
                    if any(indices[i] != (i + indices[0]) % len(a)
                           for i in range(len(a))):
                        continue
                    f = FiniteRotationLift(d, a)
                    q = f.rotation.denominator
                    p = f.rotation.numerator
                    self.assertEqual(f.iterate(a[0], q) - a[0], p)
                    self.assertTrue(all(0 <= s <= d for s in f.slopes))
                    checked += 1
        self.assertGreater(checked, 100)
        print("Exact finite rotation orbits checked:", checked)

    def test_non_rotation_orbit_rejected(self):
        with self.assertRaises(ValueError):
            FiniteRotationLift(2, [Q(1, 5), Q(2, 5), Q(3, 5), Q(4, 5)])

    def test_quadratic_coefficients_exactly(self):
        # A complex number is an exact pair of rational real/imaginary parts.
        lam = (Q(2), Q(1, 2))
        square = (lam[0] ** 2 - lam[1] ** 2, 2 * lam[0] * lam[1])
        c = (lam[0] / 2 - square[0] / 4,
             lam[1] / 2 - square[1] / 4)
        other_multiplier = (2 - lam[0], -lam[1])
        self.assertEqual(c, (Q(1, 16), Q(-1, 4)))
        self.assertEqual(other_multiplier, (Q(0), Q(-1, 2)))
        self.assertEqual(sum(x*x for x in lam), Q(17, 4))
        self.assertEqual(sum(x*x for x in other_multiplier), Q(1, 4))
        self.assertGreater(lam[1], 0)

    def test_disk_expansion_identity(self):
        # Exact algebraic samples only; log(d) and pi are not approximated.
        for x in [Q(0), Q(1, 8), Q(3, 2), Q(7)]:
            for y in [Q(-7), Q(-1, 3), Q(0), Q(5, 2)]:
                for radius in [Q(1, 9), Q(1), Q(11, 3)]:
                    self.assertEqual(
                        radius**2 - ((x-radius)**2 + y*y),
                        2*radius*x-x*x-y*y)


if __name__ == "__main__":
    unittest.main(verbosity=2)
