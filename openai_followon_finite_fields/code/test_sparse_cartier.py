"""Falsifiable checks of the candidate reduction, not a novelty certificate."""

import itertools
import unittest

import finite_fields as ff
import sparse_cartier as sc


class SparseCartierTests(unittest.TestCase):
    def test_dense_comparisons_all_small_monic(self):
        total = 0
        for p, h, cap in [(2, (0, 1), 7), (3, (0, 1), 5), (2, (1, 1, 1), 4)]:
            K = ff.FiniteField(p, h)
            elements = list(K.elements_for_testing())
            for degree in range(cap + 1):
                for prefix in itertools.product(elements, repeat=degree):
                    f = prefix + (K.one,)
                    terms = [(n, a) for n, a in enumerate(f) if a != K.zero]
                    got, audit = sc.factor_sparse(K, terms)
                    want = ff.factor(K, f, ff.exhaustive_prime_split_oracle)
                    self.assertEqual(got, want, (p, h, f, audit))
                    total += 1
        self.assertEqual(total, 960)

    def test_huge_binary_exponents_and_multiplicities(self):
        K = ff.FiniteField(2, (0, 1))
        for k, odd in [(257, False), (257, True), (1025, False)]:
            pk = 1 << k
            terms = [(0, 1), (pk, 1)] if not odd else [(0, 1), (1, 1), (pk, 1), (pk + 1, 1)]
            result, audit = sc.factor_sparse(K, terms)
            self.assertEqual(result.factors, ((K.poly((1, 1)), pk + int(odd)),))
            self.assertLessEqual(len(audit["levels"]), k + 1)
            self.assertLessEqual(max(level["new_denominator_degree"] for level in audit["levels"]), 1)

    def test_denominator_artifact_cancels(self):
        K = ff.FiniteField(2, (0, 1))
        f = K.poly((1, 0, 1, 1))
        result, audit = sc.factor_sparse(K, enumerate(f))
        self.assertEqual(result.factors, ((f, 1),))
        self.assertTrue(any(level["new_denominator_degree"] == 1 for level in audit["levels"]))

    def test_negative_signed_residues_and_large_carry(self):
        K = ff.FiniteField(3, (0, 1))
        for k in (1, 17, 127):
            s = 3 ** (k + 1)
            # (X-1)^(7+s)*(X+1)^2: a huge binomial times a degree-nine base.
            huge = {0: K.element(2), s: K.one}
            small = ff.mul(K, sc.dense_power(K, K.poly((2, 1)), 7), K.poly((1, 2, 1)))
            terms = sc.sparse_dense_product(K, huge, small)
            result, audit = sc.factor_sparse(K, terms.items())
            self.assertEqual(dict(result.factors), {K.poly((2, 1)): 7 + s,
                                                    K.poly((1, 1)): 2})
            self.assertTrue(any(level["denominator_degree"] > 0 for level in audit["levels"]))
            self.assertTrue(any(level["negative_signed_residues"] for level in audit["levels"]))

    def test_extension_scalar_units_and_shift(self):
        K = ff.FiniteField(2, (1, 1, 0, 1))
        a = K.basis()[1]
        pk = 2 ** 51
        ak = K.pow(a, pk)
        scalar = K.add(K.one, a)
        f = [(7, K.mul(scalar, K.mul(a, ak))),
             (8, K.mul(scalar, ak)), (7 + pk, K.mul(scalar, a)),
             (8 + pk, scalar)]
        result, _ = sc.factor_sparse(K, f)
        self.assertEqual(result.unit, scalar)
        self.assertEqual(dict(result.factors), {K.poly((0, 1)): 7,
                                                (a, K.one): pk + 1})

    def test_rejects_false_pade_prefix(self):
        K = ff.FiniteField(2, (0, 1))
        U = sc.normalized_sparse(K, [(0, 1), (8, 1), (9, 1)])
        audit = []
        G = sc.logarithmic_denominator(K, U, audit)
        dense = K.poly((1, 0, 0, 0, 0, 0, 0, 0, 1, 1))
        want = ff.monic(K, ff.exact_div(K, dense, ff.gcd(K, dense, ff.derivative(K, dense))))
        self.assertEqual(G, want)
        self.assertFalse(audit[0]["accepted"])

    def test_constant_zero_and_encoding(self):
        K = ff.FiniteField(3, (0, 1))
        self.assertEqual(sc.factor_sparse(K, [(0, 2)])[0], ff.Factorization(K.element(2), ()))
        self.assertEqual(sc.factor_sparse(K, [(100000000000000000000, 2)])[0].factors,
                         ((K.poly((0, 1)), 100000000000000000000),))
        with self.assertRaises(ValueError):
            sc.factor_sparse(K, [])
        with self.assertRaises(ValueError):
            sc.factor_sparse(K, [(-1, 1)])


if __name__ == "__main__":
    unittest.main()
