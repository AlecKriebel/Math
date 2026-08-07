import unittest
from fractions import Fraction
from bimolecular_pr.episode_bounds import episode_continuation_probability, scalar_envelope_branch

class EpisodeTests(unittest.TestCase):
    def test_scalar_envelope_all_branches(self):
        self.assertEqual(scalar_envelope_branch(Fraction(1,2),Fraction(-2)).branch,"endpoint")
        b=scalar_envelope_branch(Fraction(1,2),Fraction(-3))
        self.assertEqual(b.branch,"interior"); self.assertEqual(b.maximizer,Fraction(2,3))
    def test_path_length_zero(self):
        self.assertEqual(episode_continuation_probability(Fraction(1),Fraction(1)),1)
    def test_entropy_identity_with_zero_source(self):
        self.assertEqual(episode_continuation_probability(Fraction(1,3),Fraction(1,2)),Fraction(1,6))
