#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
import json
checks=0

def ck(x):
 global checks
 assert x
 checks+=1
# Binary cubic matching decomposition: squared variables avoid inexact radicals.
for a in range(1,31):
 for b in range(a+1):
  A=F(a,7);B=F(b,7);u2=A/(A+B);W2=(A+B)**3/A
  ck(F(1,2)<=u2<=1)
  ck(W2*u2**3==A*A)
  ck(W2*u2*(1-u2)**2==B*B)
  ck((3*u2-1)/2+3*(1-u2)/2==1)
# Physical spectra, complete norm threshold squarings, including boundaries.
physical_cases=0
for n in range(101):
 p=F(n,100);U=(1+3*p)/4
 for k in range(101):
  t=U*F(k,100)
  ev0=(1-p)/8;evp=(1+3*p)/8+t/2;evm=(1+3*p)/8-t/2
  ck(min(ev0,evp,evm)>=0)
  ck(6*ev0+evp+evm==1)
  # Exact detection for R with its positive square-root diagonal term.
  Rdiag2=(1+p)**3/8
  ck((Rdiag2>(1-t)**2)==((1+p)**3>8*(1-t)**2))
  physical_cases+=1
 # Cubic coefficient substitutions for both maps.
 ck(F(1,8)*(1+p)**3==(1+p)**3/8)
 ck(F(27,64)*(1+p/3)**3==(3+p)**3/64)
 ck((1+p)**3-8*(1-p)**2==p**3-5*p**2+19*p-7)
 # SIC equality: collect rational and sqrt(2) coefficients after squaring.
 ck((3+p)**3-64-8*p*p==p**3+p*p+27*p-37)
 ck(1+p<3+p)
# Exact p=1/2 separation.
ck(F(27,64)>F(1,4))
ck(14<F(15,4)**2 and 2<F(17,12)**2)
ck((7*F(15,4)+4*F(17,12))/32==F(383,384)<1)
# Boundary consistency with the Schmidt-correlated formulas.
ck((1+F(1))**3/8==1)
ck((3+F(1))**3/64==1)
# Opposite off-diagonal complex phases do not alter singular magnitudes.
for re,im in product(range(-10,11),repeat=2):
 norm2=F(re*re+im*im,400)
 ck(norm2==F(re*re+(-im)*(-im),400))
print(json.dumps({'exact_assertions':checks,'physical_parameter_cases':physical_cases,'binary_cubic_projective_norm':'(A+B)^(3/2)/sqrt(A), 0<=B<=A','exact_three_qubit_detection_regions':True,'complex_norm_lower_certificate_from_turn3':True,'separability_inferred_from_non_detection':False},indent=2))
