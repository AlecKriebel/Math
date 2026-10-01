"""Finite symbolic controls for the analytic partial package.

These check signs, half shifts and finite-dimensional algebra. They do not
prove theta estimates, local Langlands theory or an automorphic L-function FE.
"""
import sympy as S
from collections import Counter
import json
C=Counter()
def ck(x,key):
 assert x,key
 C[key]+=1
def eq(x,y,key):ck(S.simplify(x-y)==0,key)
z,s,t,c=S.symbols('z s t c');I=S.I
for lam in [S.Rational(-7,3),S.Integer(0),S.Rational(11,5),I,2+3*I]:
 for m in range(13):
  J=(-1)**m*S.factorial(m)/(z+lam)**(m+1)
  eq(S.diff(1/(z+lam),z,m),J,'lower_mellin_derivative')
  reverse_coefficient=-(-1)**m
  reverse_J=reverse_coefficient*(-1)**m*S.factorial(m)/(-z-lam)**(m+1)
  eq(reverse_J,J,'reverse_defect_same_polar_part')
  eq((z+lam).subs(z,s-S.Rational(1,2)),s-(S.Rational(1,2)-lam),'half_shift_pole_location')
  eq((-z).subs(z,s-S.Rational(1,2)),(1-s)-S.Rational(1,2),'dual_half_shift')
  # Pointwise involution B -> -B(1/r), with r=exp(t), including logarithm parity.
  f=S.exp(lam*t)*t**m
  g=-f.subs(t,-t)
  eq(-g.subs(t,-t),f,'reverse_boundary_involution')
# Exact covariance and nonzero symmetrized functional on a two-character model.
for r in [S.Rational(2),S.Rational(3,2),S.Rational(1,5)]:
 for a in range(1,8):
  R=S.diag(r**(-a),r**a);Ri=S.diag(r**a,r**(-a));F=S.Matrix([[0,1],[1,0]])
  ck(F*R==Ri*F,'Fourier_dilation_covariance')
  ell=S.Matrix([[1,0]]);E=ell+ell*F
  ck(E*F==E and E!=S.zeros(1,2),'single_self_dual_symmetrization')
  ck(S.Matrix.vstack(ell,ell*F).det()!=0,'distinct_character_independence')
# A negative square forbids a nonzero fixed linear functional.
Fm=S.Matrix([[0,1],[-1,0]])
ck(Fm*Fm==-S.eye(2),'negative_Fourier_square')
ck((Fm-S.eye(2)).det()!=0,'negative_square_no_fixed_functional')
# Finite boundary translation modules: Jordan block entries and differential law.
for n in range(1,8):
 N=S.zeros(n)
 for j in range(n-1):N[j,j+1]=1
 E=S.zeros(n)
 for j in range(n):E+=t**j/S.factorial(j)*(N**j)
 ck(E.diff(t)==N*E,'nilpotent_translation_differential_equation')
 ck(E.subs(t,0)==S.eye(n),'nilpotent_translation_initial_value')
 u=S.symbols('u')
 ck((E.subs(t,t+u)-E*E.subs(t,u)).applyfunc(S.simplify)==S.zeros(n),'Jordan_translation_group_law')
 for i in range(n):
  for j in range(n):eq(E[i,j],t**(j-i)/S.factorial(j-i) if j>=i else 0,'Jordan_power_log_terms')
# Abstract local multipliers give the global epsilon formula algebraically.
p,L,Ld,eps=S.symbols('p L Ld eps',nonzero=True)
Zd=eps*p*Ld;Z=p*L
eq((Z-Zd)/p,L-eps*Ld,'meromorphic_multiplier_cancellation')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),'sympy_version':S.__version__,'scope':'Finite sign, half-shift, covariance, Fourier-square and boundary-module algebra only; no analytic theorem or arithmetic conclusion follows from these tests alone.'},indent=2,sort_keys=True))
