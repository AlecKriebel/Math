#!/usr/bin/env python3
"""Independent integer/rational checks; read-only and optimization-safe.

Usage: python3 [-O|-OO] -B independent_exact_checks.py /path/to/verify_exact.py
This is not a verifier for the analytic dynamical proofs.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import gcd
import runpy
import sys
import unittest

TARGET=Path(sys.argv.pop(1)).resolve() if len(sys.argv)>1 else Path(__file__).with_name('verify_exact.py')
D=runpy.run_path(str(TARGET),run_name='external_ray_packet_under_test')
Lift=D['FiniteRotationLift']

class IndependentChecks(unittest.TestCase):
 def test_integer_oracle_616_cases(self):
  total=0; distinct=set()
  for degree in range(2,7):
   for denominator in range(2,71):
    if gcd(degree,denominator)!=1:continue
    unseen=set(range(denominator))
    while unseen:
     first=min(unseen); cycle=[]; x=first
     while x not in cycle:
      cycle.append(x);x=degree*x%denominator
     self.assertEqual(x,first)
     unseen.difference_update(cycle)
     a=sorted(cycle);perm=[a.index(degree*k%denominator) for k in a]
     offsets={(j-i)%len(a) for i,j in enumerate(perm)}
     if len(offsets)!=1:continue
     total+=1;angles=tuple(Q(k,denominator) for k in a)
     distinct.add((degree,angles))
     expected=Q(next(iter(offsets)),len(a));f=Lift(degree,angles)
     self.assertEqual(f.rotation,expected)
     self.assertEqual(f.iterate(angles[0],expected.denominator)-angles[0],expected.numerator)
  self.assertEqual(total,616)
  print('INDEPENDENT_ORBIT_COUNT',total,'DISTINCT_DEGREE_AND_SET_PAIRS',len(distinct))

 def test_all_small_invariant_subsets(self):
  accepted=rejected=0
  for degree in range(2,7):
   for denominator in range(2,13):
    for mask in range(1,1<<denominator):
     a=[k for k in range(denominator) if (mask>>k)&1]
     images=[degree*k%denominator for k in a]
     if set(images)!=set(a):continue
     perm=[a.index(k) for k in images]
     offsets={(j-i)%len(a) for i,j in enumerate(perm)}
     angles=[Q(k,denominator) for k in a]
     if len(offsets)!=1:
      with self.assertRaises(ValueError):Lift(degree,angles)
      rejected+=1;continue
     f=Lift(degree,angles);expected=Q(next(iter(offsets)),len(a));accepted+=1
     self.assertEqual(f.rotation,expected)
     # Values checked independently against integer multiplication modulo m.
     for x,numerator in zip(angles,images):self.assertEqual(f(x)%1,Q(numerator,denominator))
     for i,slope in enumerate(f.slopes):
      self.assertGreaterEqual(slope,0);self.assertLessEqual(slope,degree)
      left,right=f.x[i:i+2];mid=(left+right)/2
      self.assertEqual(f(mid),(f(left)+f(right))/2)
      for k in [-7,-1,0,2,9]:self.assertEqual(f(mid+k),f(mid)+k)
     for x in angles:self.assertEqual(f.iterate(x,expected.denominator)-x,expected.numerator)
  print('SMALL_INVARIANT_SUBSETS_ACCEPTED',accepted,'REJECTED_NON_ROTATION',rejected)

 def test_wringing_beltrami_algebra(self):
  # For L_s(z) = (1+i*s/2)z + (i*s/2)conj(z), |mu|^2=s^2/(4+s^2).
  for s in [Q(-100),Q(-1),Q(-1,17),Q(0),Q(3,11),Q(1),Q(100)]:
   a_norm=1+s*s/4;b_norm=s*s/4
   self.assertEqual(b_norm/a_norm,s*s/(4+s*s))
   self.assertLess(b_norm/a_norm,1)
   for x,y in [(Q(1,2),Q(-3,7)),(Q(17),Q(2,5))]:
    for degree in [2,3,6]:
     self.assertEqual((degree*x,degree*y+s*degree*x),(degree*x,degree*(y+s*x)))

 def test_quadratic_conjugacy_polynomial_identity(self):
  def add(a,b):return (a[0]+b[0],a[1]+b[1])
  def mul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
  lam=(Q(2),Q(1,2));half=(Q(1),Q(1,4));c=(Q(1,16),Q(-1,4))
  for z in [(Q(0),Q(0)),(Q(1),Q(2)),(Q(-1,3),Q(7,5))]:
   left=add(add(mul(z,z),mul(lam,z)),half)
   w=add(z,half);right=add(mul(w,w),c)
   self.assertEqual(left,right)

if __name__=='__main__':unittest.main(verbosity=2)
