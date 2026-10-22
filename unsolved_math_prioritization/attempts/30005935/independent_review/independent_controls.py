#!/usr/bin/env python3
"""Independent review controls. Imports no author scripts and does not simulate rare events."""
from fractions import Fraction as Q
from collections import Counter
import json
import sympy as s
C=Counter()
def ck(name,truth):
 assert truth,name
 C[name]+=1
# Symbolic Ito calculation in the original variable and in the BES radius.
y,r=s.symbols('y r',positive=True)
R=4*y**(-s.Rational(1,4))
ck('ito_forward_diffusion',s.simplify(s.diff(R,y)*y**s.Rational(5,4)+1)==0)
ck('ito_forward_drift',s.simplify(s.diff(R,y,2)*y**s.Rational(5,2)/2-s.Rational(5,2)/R)==0)
Y=256/r**4
ck('ito_reverse_drift',s.simplify(s.diff(Y,r)*s.Rational(5,2)/r+s.diff(Y,r,2)/2)==0)
ck('ito_reverse_diffusion',s.simplify(-s.diff(Y,r)-Y**s.Rational(5,4))==0)
# Reconstruct the tilted-normal second derivative using the MGF, not the author's brackets.
a,b,f,h,t,q=s.symbols('a b f h t q',real=True)
mgf=s.exp(t*q*q/2)
expr=s.exp(-t*f*f)*((a-b*t*f)**2*mgf+2*b*(a-b*t*f)*s.diff(mgf,q)+b*b*s.diff(mgf,q,2))
expr=s.simplify(expr.subs(q,2*f)/s.exp(t*f*f))
ck('mgf_general_identity',s.expand(expr-((a+t*f*b)**2+t*b*b))==0)
ck('mgf_N_identity',s.expand(expr.subs({a:1,b:h})-((1+t*f*h)**2+t*h*h))==0)
gp=s.symbols('gp',real=True)
ck('mgf_J_identity',s.expand(expr.subs({a:gp,b:f*h})-((gp+t*f*f*h)**2+t*f*f*h*h))==0)
# Independent Laplace substitution and antiderivative.
q,h,t,r=s.symbols('q h t r',positive=True)
qsub=h/(1-2*t*h)
ck('laplace_jacobian',s.simplify(qsub*(1+2*t*qsub)**(-3)*s.diff(qsub,h)-h)==0)
ck('laplace_exponent',s.simplify(qsub/(1+2*t*qsub)-h)==0)
primitive=-(1+r*r*h)*s.exp(-r*r*h)/r**4
ck('laplace_primitive',s.simplify(s.diff(primitive,h)-h*s.exp(-r*r*h))==0)
# Different noninteger p and eta values; positivity follows after squaring positive roots.
for den in range(3,34):
 for num in range(den+1,4*den+1):
  p=Q(num,den);eta=(p*p-1)/(3*(p*p+1))
  ck('jensen_margin',0<eta<1 and p*p*(1-eta)>1+eta)
  ck('jensen_squared_margin',p*p*(1-eta)-(1+eta)==Q(2,3)*(p*p-1))
# Gaussian bracket bounds with genuinely negative and mixed f,h,g' values.
for L in (Q(1,5),Q(4,3),Q(7,2)):
 for dt in (Q(1,101),Q(2,17),Q(9,5)):
  x=L*L*dt; bound=1+8*x+4*x*x
  for fi in range(-5,6):
   fv=L*Q(fi,5)
   for hi in range(-7,8):
    hv=2*L*Q(hi,7)
    ck('N_bracket_bound',(1+dt*fv*hv)**2+dt*hv*hv<=bound)
    for gi in (-3,-1,0,2,3):
     gv=L*Q(gi,3)
     ck('J_bracket_bound',(gv+dt*fv*fv*hv)**2+dt*fv*fv*hv*hv<=L*L*bound)
  # Finite Taylor lower bound already dominates the bracket; exponent has positive coefficients.
  ck('exponential_majorant',1+8*x+(8*x)**2/2>=bound)
# Laplace scale relation and strict positive CEV mean deficit, via exp(b)>1+b.
for num in range(1,80):
 for den in range(1,20):
  b=Q(num,den)
  ck('strict_deficit',1+b+b*b/2>1+b>0)
# Radial moment integrability and a p strictly between 1 and min(r,3/2).
for den in range(2,50):
 for num in range(den+1,3*den):
  target=Q(num,den);p=(1+min(target,Q(3,2)))/2
  ck('error_moment_choice',1<p<min(target,Q(3,2)))
  ck('radial_integrability',5-4*p>-1)
print(json.dumps({'status':'PASS_INDEPENDENT_CONTROLS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),'scope':'Independent symbolic and rational verification only. Kernel tails, SPDE comparison, time-change and Hilbert-space estimates are checked analytically in the review.'},indent=2,sort_keys=True))
