import unittest
from fractions import Fraction
from bimolecular_pr.top_complex_dichotomy import classify_top_complexes

class TopComplexTests(unittest.TestCase):
    def test_all_top_nonnegative_invariant(self):
        r=classify_top_complexes([(1,0),(0,1)],(Fraction(1,2),Fraction(1,2)),frozenset({0,1}))
        self.assertEqual(r.case,"all_top_invariant")
    def test_two_divergent_particles(self):
        r=classify_top_complexes([(1,1),(1,0),(0,0)],(Fraction(1,2),Fraction(1,2)),frozenset({0,1}))
        self.assertEqual(r.case,"two_divergent_availability")
    def test_unary_top(self):
        r=classify_top_complexes([(1,0),(0,1),(0,0)],(Fraction(1),Fraction(0)),frozenset({0}))
        self.assertEqual(r.case,"unary_top_availability")
    def test_service_availability(self):
        r=classify_top_complexes([(1,1,0),(0,1,0),(0,0,0)],(Fraction(1),Fraction(0),Fraction(0)),frozenset({0}))
        self.assertEqual(r.case,"service_availability")
    def test_shared_service_species(self):
        r=classify_top_complexes([(1,0,1),(0,1,1),(0,0,0)],(Fraction(1,2),Fraction(1,2),Fraction(0)),frozenset({0,1}))
        self.assertEqual(r.case,"signed_invariant")
    def test_slower_divergent_weight_zero_is_retained(self):
        r=classify_top_complexes([(1,0),(0,1),(0,0)],(Fraction(1),Fraction(0)),frozenset({0,1}))
        self.assertEqual(r.case,"unary_top_availability")
    def test_species_absent_from_complexes(self):
        r=classify_top_complexes([(1,0,0),(0,1,0)],(Fraction(1,2),Fraction(1,2),Fraction(0)),frozenset({0,1,2}))
        self.assertEqual(r.case,"all_top_invariant")
