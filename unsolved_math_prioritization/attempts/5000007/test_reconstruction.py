#!/usr/bin/env python3
"""Local tests added after the frozen checker; no downloaded software is run."""
import unittest
from fractions import Fraction as F
from check_certificate import K, Z, R, det, polygon, FACES, reconstruct, check, interior_angle

class Arithmetic(unittest.TestCase):
    def test_field_signs(self):
        for a in range(-8,9):
            for b in range(-8,9):
                x=K(a,b)
                self.assertEqual(x.sign(),(float(x)>0)-(float(x)<0))
                if x.sign():self.assertEqual(x/x,K(1))
    def test_rotation(self):
        self.assertEqual(R*R*R*R*R,Z(1))
        self.assertEqual(R.norm(),K(1))
        self.assertEqual(R*R.conj(),Z(1))
    def test_face_links(self):
        for v in range(20):
            pairs=[]
            for face in FACES:
                if v in face:
                    i=face.index(v);pairs.append((face[(i-1)%5],face[(i+1)%5]))
            self.assertEqual(len(pairs),3)
            self.assertEqual(sorted(a for a,b in pairs),sorted(b for a,b in pairs))
            self.assertEqual(len({a for a,b in pairs}),3)
    def test_direct_diagonal_source_calibration(self):
        # The source labels X0,X1,... clockwise, with X4=(1,0).
        p=polygon([0,1,2,3,4],0,1,Z(),Z(1))
        expected={1:(0,72,0),2:(36,108,2),3:(72,144,1),4:(108,180,0)}
        for j,(alpha,beta,source_type) in expected.items():
            v=p[j]-p[0];out=p[(j+1)%5]-p[j]
            aa=interior_angle(p[1]-p[0],v);bb=180-interior_angle(out,-v)
            self.assertAlmostEqual(aa,alpha,places=10)
            self.assertAlmostEqual(bb,beta,places=10)
            # N=1 is odd: use sum branches in Definition2.1, n=5.
            k=int(round(5-(aa+bb)/72-1)) % 3
            self.assertEqual(k,source_type)
    def test_external_witness(self):
        result=check()
        self.assertEqual(result['graph_distance'],2)
        self.assertEqual(len(result['crossings']),15)
        self.assertAlmostEqual(result['fuchs_beta_minus_alpha'],144,places=10)

if __name__=='__main__':unittest.main()
