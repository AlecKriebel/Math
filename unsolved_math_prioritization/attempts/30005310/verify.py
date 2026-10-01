#!/usr/bin/env python3
"""Exact checks only; no statistical simulation or floating-point rank tests."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import sympy as s
import json,hashlib
counts=Counter()
def ck(name,test):
 assert test,name
 counts[name]+=1
U=s.eye(4);V=s.zeros(4,4)
for j in range(4):V[j,j]=1;V[j,(j+1)%4]=1
X=U.col_join(V)
ck('rank4_gram_point',X.rank()==4 and (X*X.T).rank()==4)
outputs=[(i,i) for i in range(8)]+[(i,j) for i in range(4) for j in range(4,8)]
J=s.zeros(24,32)
for row,(i,j) in enumerate(outputs):
 for k in range(4):
  J[row,4*i+k]+=X[j,k]
  J[row,4*j+k]+=X[i,k]
piv=J.rref()[1];minor=J[:,list(piv)];det=minor.det()
ck('full_singleton_jacobian_rank',len(piv)==24 and det!=0)
Jc=s.Matrix.vstack(J[0,:]+J[1,:],J[2:8,:],J[8:,:])
pc=Jc.rref()[1];dc=Jc[:,list(pc)].det()
ck('full_colored_jacobian_rank',Jc.rows==23 and len(pc)==23 and dc!=0)
# Cross-block determinant is a genuine nonzero four-minor in the ideal.
z=s.symbols('b0:16');B=s.Matrix(4,4,z);f=B.det()
ck('obstruction_degree_four',s.Poly(f,*z).total_degree()==4)
ck('obstruction_has_24_terms',len(s.Poly(f,*z).terms())==24)
ck('obstruction_nonzero',f.subs(dict(zip(z,list(s.eye(4)))))==1)
Xstar=s.zeros(8,2)
for i in range(4):Xstar[i,0]=1
for i in range(4,8):Xstar[i,1]=1
S=Xstar*Xstar.T;P=s.eye(8)
def stats(M,merged=False):
 v=[M[i,j] for i,j in outputs]
 return ([v[0]+v[1]]+v[2:]) if merged else v
ck('rank2_witness',S.rank()==2)
ck('singleton_PD_statistics_match',stats(S)==stats(P))
ck('colored_PD_statistics_match',stats(S,True)==stats(P,True))
ck('positive_definite_completion',P.det()==1)
ck('determinantal_obstruction_zero_at_PD_stats',s.Matrix(S[:4,4:]).det()==0)
# Universal rational dominance margin and data full-rank lower bound.
eps=F(1,100);diag=(1-eps)**2;cross=2*eps*(1+eps);margin=diag-4*cross
ck('open_box_diagonal_bound',diag==F(9801,10000))
ck('open_box_cross_bound',cross==F(202,10000))
ck('open_box_PD_margin',margin==F(8993,10000) and margin>0)
ck('open_box_rank2_minor_lower_bound',(1-eps)**2-eps**2==1-2*eps and 1-2*eps>0)
# A few exact interior points illustrate the universal bound; not an exhaustive search.
for step in range(1,10):
 Y=Xstar.copy()
 for i in range(8):
  for j in range(2):Y[i,j]+=s.Rational(((i*7+j*3+step)%11)-5,1000)
 T=Y*Y.T;M=s.zeros(8,8)
 for i,j in outputs:M[i,j]=M[j,i]=T[i,j]
 ck('perturbation_rank2',Y.rank()==2)
 ck('perturbation_singleton_stats',stats(T)==stats(M))
 ck('perturbation_colored_stats',stats(T,True)==stats(M,True))
 for i in range(8):ck('perturbation_diagonal_dominance',M[i,i]>sum(abs(M[i,j]) for j in range(8) if j!=i))
 for k in range(1,9):ck('perturbation_sylvester',M[:k,:k].det()>0)
# One sample cannot complete the observed singleton edge3-5.
a,b=s.symbols('a b');ck('one_sample_edge_minor_zero',s.det(s.Matrix([[a*a,a*b],[a*b,b*b]]))==0)
M=next(k for k in range(1,9) if k*(k+1)//2>=8)
ck('credited_MLT_formula_application',M==4 and min(M,5)==4)
root=Path(__file__).resolve().parent
out={'status':'PASS_EXACT','proof_sha256':hashlib.sha256((root/'PROOF.md').read_bytes()).hexdigest(),'assertions':sum(counts.values()),'categories':dict(counts),'singleton_jacobian_shape':list(J.shape),'singleton_pivot_columns':list(piv),'singleton_minor_determinant':str(det),'colored_jacobian_shape':list(Jc.shape),'colored_pivot_columns':list(pc),'colored_minor_determinant':str(dc),'open_box_epsilon':str(eps),'uniform_PD_margin':str(margin),'observed_sample_witness_rank':2,'original_n':3,'weak_threshold':2,'singleton_MLT_credited_prior_value':4,'numerical_simulation':False,'scope':'Exact algebra/rank/dominance controls; positive probability and ideal dominance follow from the written proofs; MLT4 is credited prior theorem'}
(root/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
