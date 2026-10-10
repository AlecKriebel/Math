import csv,tempfile,unittest
from pathlib import Path
import compute,verify

class Tests(unittest.TestCase):
    def test_negative_controls(self):
        r=verify.controls();self.assertEqual(r['axis_only_restriction']['maximum_squared_side'],5)
        self.assertEqual(r['axis_only_restriction']['axis_aligned_square_count'],0)
    def test_rectangle_exact(self):
        c={(x,y) for x in range(3) for y in range(2)}
        self.assertTrue(compute.valid(c));self.assertTrue(verify.admissible(c))
        self.assertEqual(compute.analyze(c)[:2],(2,4));self.assertEqual(verify.params(c)[:2],(2,4))
    def test_quarter_turn_cross(self):
        c={(1,0),(0,1),(1,1),(2,1),(1,2)}
        self.assertTrue(compute.valid(c));s,m,*_=compute.analyze(c)
        self.assertGreaterEqual(m,s*s)
    def test_squared_side_not_diagonal(self):
        c={(0,0)};self.assertEqual(compute.analyze(c)[:2],(1,1));self.assertEqual(verify.params(c)[:2],(1,1))
    def damaged(self,kind):
        p=Path(__file__).resolve().parent/'computation/certificate.csv'
        with p.open() as f:r=list(csv.DictReader(f))
        names=list(r[0]);q=r.copy()
        if kind=='parameter':q[0]=q[0].copy();q[0]['max_side_squared']='2'
        if kind=='missing':q=q[1:]
        if kind=='duplicate':q=[q[0]]+q
        with tempfile.TemporaryDirectory() as d:
            z=Path(d)/'certificate.csv'
            with z.open('w') as f:w=csv.DictWriter(f,fieldnames=names);w.writeheader();w.writerows(q)
            with self.assertRaises(AssertionError):verify.check_certificate(z)
    def test_reject_changed_parameter(self):self.damaged('parameter')
    def test_reject_missing_mask(self):self.damaged('missing')
    def test_reject_duplicate_mask(self):self.damaged('duplicate')

if __name__=='__main__':unittest.main()
