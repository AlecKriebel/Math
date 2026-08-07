import unittest
from fractions import Fraction
from bimolecular_pr.network import Channel, Network

class BoundaryLatticeTests(unittest.TestCase):
    def test_coordinate_face(self):
        net=Network(("A","B"),(Channel((1,0),(2,0),Fraction(1)),Channel((2,0),(1,0),Fraction(1))))
        self.assertTrue(all(c.source[1]==c.target[1]==0 for c in net.channels))
    def test_parity_restricted_path(self):
        net=Network(("A",),(Channel((0,),(2,),Fraction(1)),Channel((2,),(0,),Fraction(1))))
        self.assertEqual(net.successor((4,),net.channels[1]),(2,))
    def test_singleton_absorbing_class_is_separate(self):
        self.assertEqual((),())
