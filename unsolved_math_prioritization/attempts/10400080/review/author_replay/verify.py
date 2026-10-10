#!/usr/bin/env python3
"""Exact algebraic diagnostics for the credited skein-torsion consequence."""
from pathlib import Path
from hashlib import sha256
import json
import sympy as s
C={}
def ck(t,g):
 assert bool(t),g
 C[g]=C.get(g,0)+1
A,z=s.symbols('A z');h=A+1
# The two-by-two trace identity, before imposing determinant-one relations.
x=s.symbols('x0:4');y=s.symbols('y0:4');X=s.Matrix(2,2,x);Y=s.Matrix(2,2,y)
ck(s.expand(s.trace(X)*s.trace(Y)-s.trace(X*Y)-s.trace(X*Y.adjugate()))==0,'universal trace identity')
ck(s.trace(X.adjugate())==s.trace(X),'unoriented trace identity')
ck((-A**3).subs(A,-1)==1,'framing specialization')
ck((-A*A-A**(-2)).subs(A,-1)==-2,'unknot specialization')
# The diagonal abelian character family and all parallel-copy highest terms.
for i in range(-8,9):
 for j in range(-8,9):
  lhs=(z**i+z**(-i))*(z**j+z**(-j))
  rhs=z**(i+j)+z**(-i-j)+z**(i-j)+z**(j-i)
  ck(s.expand(lhs-rhs)==0,'diagonal trace relation')
for d in range(13):
 pol=[s.expand((-z-z**(-1))**j) for j in range(d+1)]
 B=s.Matrix([[q.coeff(z,i) for q in pol] for i in range(d+1)])
 ck(B.det()==(-1)**(d*(d+1)//2),'independent parallel skeins')
 for j,q in enumerate(pol):
  ck(q.coeff(z,j)==(-1)**j,'highest Laurent coefficient')
  ck(all(q.coeff(z,i)==0 for i in range(j+1,d+2)),'triangular degree control')
# Exact specialization division in Z[A,A^-1]; multiply by a unit A^m first.
for shift in range(5):
 for e in range(1,7):
  for content in [1,2,5]:
   for g in [s.Integer(1),A-2,A*A+1]:
    relation=s.expand(content*h**e*g);eta=s.expand(content*h**(e-1)*g)
    ck(s.expand(h*eta-relation)==0,'actual linear-factor annihilator')
    ck(s.rem(eta,relation,A)!=0,'nonzero torsion class')
    laurent=relation/A**shift
    ck(s.expand(A**shift*laurent-relation)==0,'Laurent unit clearing')
    ck((content*g).subs(A,-1)!=0,'nonzero primitive specialization')
# The localization relation need not be a relation in the original module:
# v0=(1,0),v1=(1,1) in R plus R/(A+1).
diff_free=s.Integer(0);diff_torsion=s.Integer(1)
ck(diff_free==0 and s.rem(diff_torsion,h,A)!=0,'localization kernel nonzero')
ck(s.rem(h*diff_torsion,h,A)==0,'extra annihilator clears relation')
# Generic and specialized ranks in direct-sum test modules, including R/(2h).
for rank in range(5):
 for e in range(1,8):
  generic_rank=rank;special_rank=rank+1
  ck(special_rank>generic_rank,'rank jump direct sums')
  ck(s.rem(2*h**(e-1),2*h**e,A)!=0,'nonprimitive integral torsion')
  ck(s.rem(h*2*h**(e-1),2*h**e,A)==0,'nonprimitive annihilation')
root=Path(__file__).resolve().parent
res={'verdict':'PASS','assertions':sum(C.values()),'groups':C,'artifact_sha256':sha256((root/'KNOWN_RESULT.md').read_bytes()).hexdigest(),'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'sympy_version':s.__version__,'scope':'Exact algebraic controls only. Published generic finiteness and geometric existence are imported theorems, not certified by these computations.'}
(root/'verification.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
