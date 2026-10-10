#!/usr/bin/env python3
"""Local regression tests for the authored obstruction certificate."""
import copy,itertools,json,unittest
from pathlib import Path
import verify_faces as g
import check_certificate as c
ROOT=Path(__file__).parent
class TestFaces(unittest.TestCase):
    def test_all_small_classes(self):
        expect={2:[],3:[],4:[(2,4,1,3),(3,4,1,2),(4,2,3,1)]}
        for n in (2,3,4): self.assertEqual(g.run(n)['nonrepresentable'],expect[n])
    def test_independent_edge_directions(self):
        for n in (2,3,4):
            for p in itertools.permutations(range(1,n+1)):
                expected={tuple((a,b)):r for a,b,r in g.diagram(p)}
                self.assertEqual(dict(c.active(p)),expected)
    def test_certificate(self):
        z=json.loads((ROOT/'certificate.json').read_text());self.assertEqual(c.check(z)['borels_covered'],24)
    def test_reject_missing_borel(self):
        z=json.loads((ROOT/'certificate.json').read_text());z.pop()
        with self.assertRaises(AssertionError):c.check(z)
    def test_reject_wrong_values(self):
        z=json.loads((ROOT/'certificate.json').read_text());z[0]['top_labels_at_predecessor']=[1,1]
        with self.assertRaises(AssertionError):c.check(z)
    def test_reject_nonpredecessor(self):
        z=json.loads((ROOT/'certificate.json').read_text());z[0]['predecessor']=[2,4,1,3];z[0]['sigma_predecessor']=[2,4,1,3]
        with self.assertRaises(AssertionError):c.check(z)
if __name__=='__main__':unittest.main(verbosity=2)
