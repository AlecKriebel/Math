"""Independent small-field checks of the CONDITIONAL reference reduction.

The comparator enumerates monic trial divisors; it does not use Berlekamp,
Frobenius kernels, trace coordinates, or the injected root oracle.  Both comparator
and toy root oracle have exponential dependence on binary characteristic/field
size and are used only for finite regression examples.
"""

import itertools
import unittest

from finite_fields import (FiniteField, divmod_poly, factor,
                           exhaustive_prime_split_oracle, irreducible, monic, mul,
                           polynomial_pth_root, prime_polynomial_irreducible)


def monic_polynomials(K, degree):
    elements = list(K.elements_for_testing())
    for coefficients in itertools.product(elements, repeat=degree):
        yield tuple(coefficients) + (K.one,)


def trial_irreducible(K, f):
    degree = len(f) - 1
    if degree < 1:
        return False
    for d in range(1, degree // 2 + 1):
        for candidate in monic_polynomials(K, d):
            if not divmod_poly(K, f, candidate)[1]:
                return False
    return True


def trial_factor(K, original):
    residual = monic(K, original)
    result = []
    for degree in range(1, len(original)):
        if len(residual) <= 1:
            break
        for candidate in monic_polynomials(K, degree):
            if len(candidate) > len(residual):
                break
            multiplicity = 0
            while len(candidate) <= len(residual):
                quotient, remainder = divmod_poly(K, residual, candidate)
                if remainder:
                    break
                residual = quotient
                multiplicity += 1
            if multiplicity:
                result.append((candidate, multiplicity))
    if residual != (K.one,):
        raise AssertionError("trial divisor comparator did not exhaust the input")
    return tuple(sorted(result))


class ConditionalReductionTests(unittest.TestCase):
    def compare(self, K, f):
        answer = factor(K, f, exhaustive_prime_split_oracle)
        self.assertEqual(answer.factors, trial_factor(K, f))
        self.assertEqual(answer.reconstruct(K), f)
        self.assertTrue(answer.verify(K, f))
        for g, multiplicity in answer.factors:
            self.assertGreaterEqual(multiplicity, 1)
            self.assertTrue(trial_irreducible(K, g))
            self.assertTrue(irreducible(K, g))
        for run in K.stats.squarefree_runs:
            self.assertLessEqual(run["fixed_algebra_dimension"], run["degree"])
        for coordinate in K.stats.trace_coordinates:
            self.assertLessEqual(coordinate["minimal_degree"], coordinate["input_degree"])
        return answer

    def test_all_monic_small_polynomials(self):
        # Every monic input within the listed ranges, including repeated factors.
        cases = [(2, [0, 1], 5), (3, [0, 1], 3), (5, [0, 1], 2),
                 (2, [1, 1, 1], 3), (2, [1, 1, 0, 1], 2),
                 (3, [1, 0, 1], 2)]
        checked = 0
        for p, h, maximum_degree in cases:
            K = FiniteField(p, h)
            for degree in range(1, maximum_degree + 1):
                for f in monic_polynomials(K, degree):
                    with self.subTest(p=p, h=h, f=f):
                        self.compare(K, f)
                    checked += 1
        self.assertEqual(checked, 377)

    def test_extension_characteristic_two_and_inseparability(self):
        K = FiniteField(2, [1, 1, 1])
        alpha = K.element((0, 1))
        linear = K.poly([alpha, 1])
        other = K.poly([K.add(alpha, K.one), 1])
        f = (K.one,)
        for _ in range(4):
            f = mul(K, f, linear)
        for _ in range(3):
            f = mul(K, f, other)
        answer = self.compare(K, f)
        self.assertEqual(sorted(e for _, e in answer.factors), [3, 4])
        square = mul(K, linear, linear)
        self.assertEqual(polynomial_pth_root(K, square), linear)
        # Coefficient root is nontrivial here: alpha^2 has root alpha in F_4.
        self.assertNotEqual(square[0], linear[0])

    def test_nonmonic_constants_zero_and_degree_one(self):
        K = FiniteField(3, [2, 1])  # F_3 with a nonzero root for its linear h.
        f = K.poly([2, 1, 2])
        self.compare(K, f)
        answer = factor(K, K.poly([2]), exhaustive_prime_split_oracle)
        self.assertEqual(answer.unit, K.element(2))
        self.assertEqual(answer.factors, ())
        self.assertTrue(answer.verify(K, K.poly([2])))
        answer = self.compare(K, K.poly([1, 1]))
        self.assertEqual(answer.factors, ((K.poly([1, 1]), 1),))
        with self.assertRaisesRegex(ValueError, "zero polynomial"):
            factor(K, (), exhaustive_prime_split_oracle)

    def test_modulus_checks_without_integer_factorization(self):
        self.assertTrue(prime_polynomial_irreducible(2, [1, 1, 1]))
        self.assertFalse(prime_polynomial_irreducible(2, [1, 0, 1]))
        self.assertTrue(prime_polynomial_irreducible(3, [1, 0, 1]))
        with self.assertRaisesRegex(ValueError, "reducible"):
            FiniteField(2, [1, 0, 1])
        with self.assertRaisesRegex(ValueError, "monic"):
            FiniteField(3, [1, 2])
        with self.assertRaises(ValueError):
            polynomial_pth_root(FiniteField(2, [1, 1, 1]),
                                FiniteField(2, [1, 1, 1]).poly([1, 1]))

    def test_field_laws_exhaustively(self):
        for p, h in [(2, [0, 1]), (3, [2, 1]), (2, [1, 1, 1]),
                     (2, [1, 1, 0, 1]), (3, [1, 0, 1])]:
            K = FiniteField(p, h)
            values = list(K.elements_for_testing())
            for a in values:
                self.assertEqual(K.pow(a, K.q), a)
                self.assertEqual(K.mul(a, K.one), a)
                if a != K.zero:
                    self.assertEqual(K.mul(a, K.inv(a)), K.one)
                for b in values:
                    self.assertEqual(K.add(a, b), K.add(b, a))
                    self.assertEqual(K.mul(a, b), K.mul(b, a))
                    for c in values:
                        self.assertEqual(K.mul(K.mul(a, b), c), K.mul(a, K.mul(b, c)))
                        self.assertEqual(K.mul(a, K.add(b, c)),
                                         K.add(K.mul(a, b), K.mul(a, c)))

    def test_corrupt_oracle_is_rejected(self):
        K = FiniteField(3, [0, 1])
        f = K.poly([0, 2, 1])  # x(x-1).
        with self.assertRaisesRegex(ArithmeticError, "completely factor"):
            factor(K, f, lambda p, g: [])
        with self.assertRaisesRegex(ArithmeticError, "duplicate"):
            factor(K, f, lambda p, g: [0, 0])
        with self.assertRaisesRegex(ValueError, "toy oracle"):
            exhaustive_prime_split_oracle(5003, (0, 1))

    def test_all_distinct_component_values_are_separated(self):
        K = FiniteField(2, [1, 1, 0, 1])
        f = (K.one,)
        for value in K.elements_for_testing():
            f = mul(K, f, K.poly([value, 1]))
        answer = self.compare(K, f)
        self.assertEqual(len(answer.factors), 8)
        run = K.stats.squarefree_runs[-1]
        self.assertEqual(run["fixed_algebra_dimension"], 8)
        self.assertLessEqual(K.stats.counters["prime_oracle_calls"], 3 * 8)
        self.assertTrue(all(query["degree"] <= 8 for query in K.stats.oracle_queries))


if __name__ == "__main__":
    unittest.main(verbosity=2)
