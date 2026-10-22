import sympy as S
from fractions import Fraction as Q
import json
r,s,t=S.symbols('r s t',real=True);count=0;rows=[]
def ck(x):
 global count;count+=1;assert x
J=lambda x:S.Rational(315,256)*(1-x*x)**4
for k in [2,3,4]:
 P=lambda x:(1-x*x)**k
 same=S.integrate(J(r-s)*P(s),(s,0,1))
 cross=S.integrate(J(r+s)*P(s),(s,0,1-r))
 left=S.integrate(-S.diff(P(r),r)*(same+cross),(r,0,1))
 peak=2*S.integrate(J(s)*P(s),(s,0,1))
 stress=S.integrate(S.integrate(-S.diff(J(t),t).subs(t,r+s)*P(r)*P(s),(s,0,1-r)),(r,0,1))
 ck(S.simplify(left-peak+stress)==0);ck(stress>0);ck(stress<peak/2)
 rows.append({'profile_power':k,'integral_pprime_Jp':str(left),'peak_convolution':str(peak),'boundary_stress':str(stress)})
# A'' without the positive beta factor.
f=lambda x:2*x/(1-x*x)**2
for a in range(-9,10):
 for b in range(a+1,10):
  m,u=Q(a,10),Q(b,10);c=(m+u)/2;rad=(u-m)/2
  for j in range(1,20):
   z=rad*Q(j,20);v=f(c+z)+f(c-z)
   ck((v>0)-(v<0)==(c>0)-(c<0))
ck(S.simplify(S.diff(2*t/(1-t*t)**2,t)-2*(1+3*t*t)/(1-t*t)**3)==0)
print(json.dumps({'assertions':count,'exact_polynomial_models':rows,'scope':'IBP identity and error-sign controls only; test profiles are not solutions.'},indent=2))
