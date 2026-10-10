"""Independent exact algebra controls. No PDE simulation or numerical PDE constants."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
import sympy as s
import json
C=Counter()
def ck(q,k):assert bool(q),k;C[k]+=1
pi=s.pi;t,h,q,tau,eps,a,b,r=s.symbols('t h q tau eps a b r',positive=True)
# Start from the general-center Duhamel kernel, not the centered endpoint formula.
k=s.sin(pi*(1-t))/pi
Z=s.simplify(q*s.integrate(k,(t,tau-h,tau+h)))
V=s.simplify(q*s.integrate(s.cos(pi*(1-t)),(t,tau-h,tau+h)))
ck(s.trigsimp(Z-2*q*s.sin(pi*h)*s.sin(pi*tau)/pi**2)==0,'general_center_endpoint')
ck(s.trigsimp(V+2*q*s.sin(pi*h)*s.cos(pi*tau)/pi)==0,'general_center_velocity')
z=s.simplify(Z.subs(tau,s.Rational(1,2)));v=s.simplify(V.subs(tau,s.Rational(1,2)))
ck(v==0,'centered_velocity_zero')
gap=2*q*h-pi*z
lin=gap+z*z/2
ck(s.simplify(s.limit(lin.subs(q,h)/h**4,h,0)-(pi**2/3+2/pi**2))==0,'exact_growth_gap_leading_coefficient')
ck(s.simplify(s.limit(lin.subs(q,h)/(2*h**4),h,0)-(pi**2/6+1/pi**2))==0,'growth_ratio_divided_by_h')
trial=s.simplify((lin-eps*z).subs({q:a,h:pi*eps/(2*a)}))
ck(s.limit(trial/eps**2,eps,0)==-s.Rational(1,2),'perturbed_negative_quadratic_leading_term')
ck(s.simplify(s.limit((trial+eps**2/2)/eps**3,eps,0)-pi**5/(24*a**2))==0,'perturbed_cubic_coefficient')
ck(s.trigsimp(-pi*k+s.sin(pi*t))==0,'adjoint_and_subgradient_cancel')
# Radial eigenmode via the transformed radial unknown r*e(r).
w=s.sin(pi*r)/s.sqrt(2*pi)
ck(s.simplify(s.diff(w,r,2)+pi**2*w)==0,'radial_eigenmode_ode')
ck(s.simplify(4*pi*s.integrate(w*w,(r,0,1)))==1,'radial_normalization')
ck(s.limit(w/r,r,0)==pi/s.sqrt(2*pi),'regular_origin')
# Interpolation identities underlying the Banach-space contraction.
ck(F(1,10)==F(4,5)*F(1,12)+F(1,5)*F(1,6),'space_interpolation')
ck(F(1,5)==F(4,5)*F(1,4),'time_interpolation')
ck(5*F(1,10)==F(1,2) and 5*F(1,5)==1,'quintic_forcing_exponents')
# Exhaustive small rational densities, distinct from author's random tests.
for n in range(1,7):
 for levels in product((F(0),F(1,2),F(1)),repeat=n):
  A=sum(levels,F(0))/n;moment=F(0)
  for j,f in enumerate(levels):
   l=F(j,n)-F(1,2);u=F(j+1,n)-F(1,2);moment+=f*(u**3-l**3)/3
  ck(moment>=A**3/12,'exhaustive_rational_bathtub')
# Dimensionless global positivity with k=C0*rho^4 <=1/12 and x=A/rho<=1.
for i in range(13):
 for j in range(21):ck(F(1,6)-F(i,144)*F(j,20)**2>=F(1,12),'uniform_global_gap_constant')
# Exact norm of the enclosing parabolic cap; the author's simpler bound is larger.
radius=s.sqrt(b/2)
capnorm2=s.simplify(s.integrate((b-2*t*t)**2,(t,-radius,radius)))
ck(s.simplify(capnorm2-8*s.sqrt(2)*b**s.Rational(5,2)/15)==0,'exact_positive_part_cap_norm')
ck(F(8,15)<1,'published_bound_dominates_sharper_cap')
ck(F(5,4)+1>2 and 5>2,'target_stability_exponents')
for power,expected in [(4,5),(5,7),(10,17)]:ck(2*power-3==expected>0,'growth_remainder_ratios')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'symbolic_growth_leading_coefficient':'pi^2/3+2/pi^2','symbolic_target_trial_leading_term':'-epsilon^2/2','scope':'Exact eigenmode, contraction exponents, pulse expansions and finite bathtub controls. Infinite-dimensional estimates, compactness and critical-cone/source scope are verified analytically in the review; no certified numerical PDE constant is claimed.'},indent=2))
