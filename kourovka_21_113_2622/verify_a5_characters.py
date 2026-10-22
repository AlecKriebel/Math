#!/usr/bin/env python3
"""Exact A5 checks in Q(a), a^2+a=1. Classical tables are credited in notes."""
from fractions import Fraction as F
from dataclasses import dataclass
import json
from pathlib import Path

@dataclass(frozen=True)
class Q:
 u:F=F(0)
 v:F=F(0)
 def __add__(self,b):
  b=q(b);return Q(self.u+b.u,self.v+b.v)
 __radd__=__add__
 def __neg__(self):return Q(-self.u,-self.v)
 def __sub__(self,b):return self+-q(b)
 def __rsub__(self,b):return q(b)+-self
 def __mul__(self,b):
  b=q(b);return Q(self.u*b.u+self.v*b.v,self.u*b.v+self.v*b.u-self.v*b.v)
 __rmul__=__mul__
 def __truediv__(self,b):
  assert isinstance(b,int) and b!=0
  return Q(self.u/b,self.v/b)
 def integer(self):
  assert self.v==0 and self.u.denominator==1
  return self.u.numerator

def q(x):return x if isinstance(x,Q) else Q(F(x))
def dot(x,y,sizes):return sum((q(a)*q(b)*s for a,b,s in zip(x,y,sizes)),Q())/60

def main():
 a=Q(F(0),F(1));b=-1-a
 sizes=[1,15,20,12,12]
 ordinary=[[1,1,1,1,1],[3,-1,0,1+a,1+b],[3,-1,0,1+b,1+a],[4,0,1,-1,-1],[5,1,-1,0,0]]
 for i,row in enumerate(ordinary):
  for j,col in enumerate(ordinary):assert dot(row,col,sizes)==q(int(i==j))
 assert sum(row[0]**2 for row in ordinary)==60
 brauer=[[1,1,1,1],[2,-1,a,b],[2,-1,b,a],[4,1,-1,-1]]
 D=[[1,0,0,0],[1,1,0,0],[1,0,1,0],[0,0,0,1],[1,1,1,0]]
 for row,ds in zip(ordinary,D):
  reg=[row[i] for i in [0,2,3,4]]
  assert [q(x) for x in reg]==[sum((d*q(phi[j]) for d,phi in zip(ds,brauer)),Q()) for j in range(4)]
 psi=[16,0,1,1,1]
 ordinary_coeff=[dot(psi,row,sizes).integer() for row in ordinary]
 projective_coeff=[dot([16,1,1,1],row,[1,20,12,12]).integer() for row in brauer]
 assert ordinary_coeff==[1,1,1,1,1]
 assert projective_coeff==[1,0,0,1]
 alpha=[q(1)+q(x) for x in ordinary[1]]
 alpha_coeff=[dot([alpha[i] for i in [0,2,3,4]],row,[1,20,12,12]).integer() for row in brauer]
 assert alpha[1]==q(0) and alpha_coeff==[1,0,-1,0]
 # The induced-centralizer subtraction formula, using nonidentity p-regular classes.
 rowsums=[sum((q(x) for x in row),Q()).integer() for row in brauer]
 c3=[((q(row[0])+2*q(row[1]))/3).integer() for row in brauer]
 c5=[((q(row[0])+2*q(row[2])+2*q(row[3]))/5).integer() for row in brauer]
 local=[x+2*y for x,y in zip(c3,c5)]
 assert rowsums==[4,0,0,3] and local==[3,0,0,2]
 assert [x-y for x,y in zip(rowsums,local)]==projective_coeff
 result={'field':'Q(a), a^2+a=1','ordinary_orthonormality_checks':25,'decomposition_identities':20,'psi_2_A5_ordinary_coefficients':ordinary_coeff,'psi_2_A5_projective_coefficients':projective_coeff,'alpha_ordinary_character':'1 + chi_3','alpha_projective_coefficients':alpha_coeff,'alpha_negative_Brauer_pairing':-1,'truncated_conjugation_projective_coefficients':rowsums,'proper_centralizer_contribution':local}
 return result

if __name__=='__main__':
 result=main();Path(__file__).with_name('a5_verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
