"""Exact controls for the dominant-mode criterion, not actual scattering data."""
from fractions import Fraction as F
from collections import Counter
import json
C=Counter()
def ck(g,b):
 if not b:raise AssertionError(g)
 C[g]+=1
for dn in range(1,21):
 Delta=F(dn,20);theta=1-Delta
 for an in range(1,21):
  a=F(an,20)
  for en in range(1,11):
   eps=a*Delta*F(en,320)
   q=eps/(Delta-3*eps);beta=theta+2*eps
   ck('smallness',eps<=Delta/16 and q<=F(1,13) and q<=a/2)
   ck('Schur_disc_invariance',eps+eps*q<2*eps)
   ck('Schur_contraction',q*q<1)
   ck('power_decomposition_constant',(1+q)*(1+q/(1-q*q))<2)
   ck('projection_difference_constant',2*q/(1-q*q)<=3*q)
   ck('uniform_gap',beta/(1-2*eps)<=1-3*Delta/4<1)
   ck('excited_mode_lower_bound',(a-q)*(1-q)/(1+q*q)>=a/8)
   ck('quotient_numerator_bound',2*(beta+1+2*eps)<=6)
# Exact rational matrices with a known perturbed leading eigenvalue.
for theta in (F(1,4),F(1,2),F(3,4)):
 for n in (100,200,1000):
  eps=F(1,n);zeta=1+eps
  # Upper-triangular perturbation: the leading root and left eigenvector
  # exactly solve the same block equations; include a nonzero coupling b.
  b=eps;D=theta;R=1/(zeta-D)
  phi=(F(1),b*R);u=(F(1),F(0))
  ck('left_eigenfunctional',phi[0]*b+phi[1]*D==zeta*phi[1])
  ck('projection_normalization',phi[0]*u[0]+phi[1]*u[1]==1)
  for j in range(1,31):
   off=b*(zeta**j-D**j)/(zeta-D)
   # First coordinate of S^j(1,1) and its spectral decomposition.
   val=zeta**j+off;lead=zeta**j*(1+b*R);rem=-b*R*D**j
   ck('exact_power_decomposition',val==lead+rem)
print(json.dumps({'status':'PASS_EXACT_OPERATOR_CRITERION_CONTROLS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),'scope':'Rational constants and finite block identities supplement the Banach-space proof; strong-norm PDE approximation and initial excitation remain unproved.'},indent=2,sort_keys=True))
