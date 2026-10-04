#!/usr/bin/env python3
"""Independent dense-matrix checks and deliberate negative controls."""
import json, random, unittest
import controls as c

class Controls(unittest.TestCase):
 def test_collection(self):
  self.assertEqual([c.collect(w) for w in c.WORDS],[(0,0,6),(-4,4,0),(4,8,26)])
  self.assertEqual(c.collect([('y',1),('x',1)]),(1,1,1))
  self.assertEqual(c.collect([('x',1),('y',1)]),(1,1,0))
 def test_exact_polynomial_representation(self):
  for P in (c.X,c.Y):
   self.assertEqual(c.pmul(P,c.pinv(P)),(c.I,))
   self.assertEqual(c.pmul(c.pinv(P),P),(c.I,))
  for w in c.WORDS:self.assertEqual(c.evalword(w,{'x':c.X,'y':c.Y},(c.I,),c.pmul,c.pinv),(c.I,))
 def test_wrong_relator_rejected(self):
  wrong=c.WORDS[0]+[('x',1)]
  self.assertNotEqual(c.evalword(wrong,{'x':c.X,'y':c.Y},(c.I,),c.pmul,c.pinv),(c.I,))
 def test_three_state_cycle(self):
  o=c.leading_orbit()
  self.assertEqual([x['rank'] for x in o['ranks']],[1,2,3,3])
  self.assertEqual((o['cycle_start_gamma_index'],o['cycle_repeat_gamma_index'],o['cycle_period']),(2,5,3))
  # Negative indexing control: a one-step shift changes the claimed first target rank.
  self.assertNotEqual(o['ranks'][1]['rank'],o['ranks'][2]['rank'])
 def test_magnus_initial_forms(self):
  m=[c.magnus(w) for w in c.WORDS]
  self.assertEqual([a['degree'] for a in m],[4,4,4])
  vs=[sum(1<<int(t.replace('x','0').replace('y','1'),2) for t in a['initial_terms']) for a in m]
  self.assertEqual(len(c.basis(vs)),3)
  # Negative control: appending x creates degree one, so the truncation detects it.
  self.assertEqual(c.magnus(c.WORDS[0]+[('x',1)])['degree'],1)
 def test_independent_dense_matrix_multiplication(self):
  def dense(P):
   m=len(P); blocks=m+3; n=3*blocks; rows=[1<<i for i in range(n)]
   for r in range(blocks):
    for d,a in enumerate(P,1):
     if r+d>=blocks:continue
     a=a[r%3]
     for i in range(3):
      for j in range(3):
       if a>>(3*i+j)&1:rows[3*r+i]^=1<<(3*(r+d)+j)
   return tuple(rows)
  def extract(A,m):
   return tuple(tuple(sum(((A[3*r+i]>>(3*(r+d)+j))&1)<<(3*i+j) for i in range(3) for j in range(3)) for r in range(3)) for d in range(1,m+1))
  rng=random.Random(61030001033)
  for m in range(1,6):
   E=((0,0,0),)*m
   for _ in range(12):
    P=tuple(tuple(rng.randrange(512) for _ in range(3)) for _ in range(m))
    Q=tuple(tuple(rng.randrange(512) for _ in range(3)) for _ in range(m))
    self.assertEqual(c.tmul(P,Q),extract(c.mm(dense(P),dense(Q),3*(m+3)),m))
    self.assertEqual(c.tmul(P,c.tinv(P)),E)
    self.assertEqual(c.tmul(c.tinv(P),P),E)
 def test_finite_group_sequences(self):
  expected=[(4,[4]),(32,[16,2]),(128,[16,2,4]),(1024,[16,2,4,8]),(8192,[16,2,4,8,8])]
  for m,(order,indices) in enumerate(expected,1):
   q=c.finite_control(m)
   self.assertEqual((q['order'],q['lower_central_indices']),(order,indices))
   self.assertFalse(q['limits']['full_abstract_quotient'])
 def test_noncommutative_negative_control(self):
  x=tuple(c.diag(c.X,d) for d in [1,2]); y=tuple(c.diag(c.Y,d) for d in [1,2])
  self.assertNotEqual(c.tmul(x,y),c.tmul(y,x))
if __name__=='__main__':unittest.main(verbosity=2)
