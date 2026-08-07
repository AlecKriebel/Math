import unittest
from fractions import Fraction
from bimolecular_pr.network import Channel, Network, falling_factorial
from bimolecular_pr.target_augmented import direct_exp_increment, exp_potential_increment, marked_successor

class NetworkTests(unittest.TestCase):
    def test_residual_identity(self):
        x=(5,3); t=(1,1); ch=Channel((2,0),(0,1),Fraction(2),"r")
        self.assertEqual(direct_exp_increment(x,t,ch), exp_potential_increment(x,t,ch.source))
    def test_zero_complex_and_two_a(self):
        self.assertEqual(falling_factorial((3,), (0,)), 1)
        self.assertEqual(falling_factorial((3,), (2,)), 6)
    def test_mixed_complex(self):
        self.assertEqual(falling_factorial((3,4),(1,1)),12)
    def test_parallel_and_same_displacement_channels(self):
        net=Network(("A","B"),(
            Channel((0,0),(1,0),Fraction(2),"a"), Channel((0,0),(1,0),Fraction(3),"b"),
            Channel((1,0),(0,1),Fraction(1),"c"), Channel((2,0),(1,1),Fraction(1),"d")))
        combined=net.combined_parallel()
        self.assertEqual(len(combined.channels),3)
        self.assertTrue(any(c.rate==5 and c.source==(0,0) for c in combined.channels))
    def test_mark_actual_channel_not_displacement(self):
        c1=Channel((1,0),(0,1),Fraction(1),"c1")
        c2=Channel((2,0),(1,1),Fraction(1),"c2")
        self.assertEqual(c1.displacement,c2.displacement)
        self.assertNotEqual(marked_successor((2,0),c1)[1],marked_successor((2,0),c2)[1])
    def test_strong_connectivity(self):
        net=Network(("A",),(Channel((0,),(1,),Fraction(1)),Channel((1,),(0,),Fraction(1))))
        self.assertTrue(net.strongly_connected())
