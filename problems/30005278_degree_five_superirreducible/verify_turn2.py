#!/usr/bin/env python3
"""Symbolic exact elimination and bounded diagnostics. Requires SymPy."""
import sympy as S,json
from itertools import product
from fractions import Fraction as F
from collections import Counter
C=Counter()
def ck(t,k):assert t,k;C[k]+=1
x=S.symbols('x');A=S.symbols('A0:5');a,b,c,d,e=A
f=x**5+2*x+1;remainder=S.rem(sum(A[i]*x**i for i in range(5))**2,f,x).expand()
forms=[a*a-2*b*e-2*c*d,2*a*b-4*b*e-4*c*d-2*c*e-d*d,2*a*c+b*b-4*c*e-2*d*d-2*d*e,2*a*d+2*b*c-4*d*e-e*e,2*a*e+2*b*d+c*c-2*e*e]
for i in range(5):ck(S.expand(remainder.coeff(x,i)-forms[i])==0,'power_basis_reduction')
s,t=S.symbols('s t');D=t-s*s;v={a:(-t**3+2*t-4*s*s-s)/(2*D),b:(s*t*t+2*s+1)/(2*D),c:t,d:s,e:1}
R=-8*s**6-8*s**5+16*s**4*t+20*s**3*t+5*s*s*t**4+4*s*s*t*t+4*s*s-10*s*t*t+4*s-4*t**5-8*t**3+1
ck(S.cancel(4*D*D*forms[2].subs(v)-R)==0,'plane_equation_identity')
for i in (3,4):ck(S.cancel(forms[i].subs(v))==0,'eliminated_quadric_identity')
ck(S.expand(R.subs(t,s*s)-(s**5+2*s+1)**2)==0,'denominator_exception_identity')
ck(S.expand(forms[2].subs({e:0,d:1,c:t,b:-t*t/2,a:t**3/2})-(5*t**4-8)/4)==0,'zero_quartic_coordinate')
zero3=4*t**5+8*t**3-1;zero2=-8*s**6-8*s**5+4*s*s+4*s+1;zero1=t*(t*t+2)**3-2*(t*t+1)
ck(S.expand(R.subs(s,0)+zero3)==0,'zero_cubic_eliminant')
ck(S.expand(R.subs(t,0)-zero2)==0,'zero_quadratic_eliminant')
sub={a:1-t*t/2,b:0,c:t,d:-1/(t*t+2),e:1}
ck(S.cancel((t*t+2)**2*forms[2].subs(sub)+zero1)==0,'zero_linear_eliminant')
for i in (3,4):ck(S.cancel(forms[i].subs(sub))==0,'zero_linear_auxiliary_equations')
candidates=[]
for poly,var,ds in [(zero3,t,(1,2,4)),(zero2,s,(1,2,4,8)),(zero1,t,(1,))]:
 nums=(1,2) if poly==zero1 else (1,)
 for n in nums:
  for q in ds:
   for sign in (-1,1):
    z=S.Rational(sign*n,q);value=poly.subs(var,z);ck(value!=0,'complete_rational_root_candidates');candidates.append({'polynomial':str(poly),'candidate':str(z),'value':str(value)})
# Modest projective-vector box, not a complete rational-point computation.
def coeff(v):
 a,b,c,d,e=v
 return [a*a-2*b*e-2*c*d,2*a*b-4*b*e-4*c*d-2*c*e-d*d,2*a*c+b*b-4*c*e-2*d*d-2*d*e,2*a*d+2*b*c-4*d*e-e*e,2*a*e+2*b*d+c*c-2*e*e]
box=0;witnesses=[];scalar_vectors=0
for v in product(range(-5,6),repeat=5):
 if not any(v):continue
 box+=1;r=coeff(v)
 if r[2:]==[0,0,0]:
  if r[1]:witnesses.append(v)
  else:scalar_vectors+=1;ck(not any(v[1:]),'bounded_scalar_only_vectors')
ck(not witnesses,'bounded_nonconstant_witness_scan')
print(json.dumps({'status':'PASS','arithmetic':'exact symbolic rational algebra and integers; requires SymPy','assertions':sum(C.values()),'by_scope':dict(C),'rational_root_candidates':candidates,'diagnostic_vector_box':{'bound':5,'nonzero_vectors':box,'nonconstant_witnesses':witnesses,'scalar_vectors':scalar_vectors},'plane_curve':str(R),'scope':'The sparsity exclusions are proved universally. The coefficient box is only a finite diagnostic and does not exhaust rational points of the remaining curve.'},indent=2,sort_keys=True))
