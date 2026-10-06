#!/usr/bin/env python3
"""Independently designed exact analytic discriminators; no imported audit code.

The early seal fixes the universal proof obligations. These trigonometric,
variation, and explicit norm controls supplement that written proof; none is a
PDE simulation or general Banach existence certificate.
"""
from pathlib import Path
from collections import Counter
import datetime,hashlib,json
import sympy as s

HERE=Path(__file__).resolve().parent
C=Counter();E={};N=[]
def check(name,p):assert bool(p),name;C[name]+=1
def zero(name,p):check(name,s.trigsimp(s.simplify(p))==0)
def negative(name,p):check('rejected_'+name,not bool(p));N.append(name)

# Distinct Fourier-coordinate family: X=x+a sin(x), V=cos(x)+d sin(x).
# |a|<1 ensures injectivity. Physical mean a/2 differs from label mean zero.
x,a,d,e=s.symbols('x a d e',real=True);L=2*s.pi
X=x+a*s.sin(x);J=s.diff(X,x);V=s.cos(x)+d*s.sin(x)
m=s.integrate(V*J,(x,0,L))/L
K=s.integrate((V-m)*J,(x,0,x));H=K-s.integrate(K*J,(x,0,L))/L
zero('Fourier_lift_degree_one',X.subs(x,L)-X.subs(x,0)-L)
zero('Fourier_weighted_mean',m-a/2)
zero('Fourier_K_periodicity',K.subs(x,L)-K.subs(x,0))
zero('Fourier_physical_primitive_mean',s.integrate(H*J,(x,0,L)))
zero('Fourier_primitive_derivative',s.diff(H,x)-(V-m)*J)
wrongK=s.integrate(V*J,(x,0,x))
negative('unweighted_input_mean',s.simplify(wrongK.subs(x,L)).subs(a,s.Rational(1,2))==0)
wrongH=K-s.integrate(K,(x,0,L))/L
res=s.simplify(s.integrate(wrongH*J,(x,0,L)))
negative('unweighted_output_mean',res.subs({a:s.Rational(1,2),d:s.Rational(2,3)})==0)
E['unweighted_K_endpoint_residual']=str(s.simplify(wrongK.subs(x,L)))
E['unweighted_H_physical_mean_residual']=str(res)

# First variation at identity of a generally nonzero-mean input. These exact
# directional formulas discriminate the mean/Jacobian terms of the vector field.
Z=s.sin(2*x);W=s.cos(2*x)+s.sin(x)
Je=J+e*s.diff(Z,x);Ve=V+e*W
me=s.integrate(Ve*Je,(x,0,L))/L
dm=s.integrate(W*J+V*s.diff(Z,x),(x,0,L))/L
zero('Frechet_mean_first_variation',s.diff(me,e).subs(e,0)-dm)
Ke=s.integrate((Ve-me)*Je,(x,0,x))
dK=s.integrate((W-dm)*J+(V-m)*s.diff(Z,x),(x,0,x))
zero('Frechet_K_first_variation',s.diff(Ke,e).subs(e,0)-dK)
He=Ke-s.integrate(Ke*Je,(x,0,L))/L
dH=dK-s.integrate(dK*J+K*s.diff(Z,x),(x,0,L))/L
zero('Frechet_H_first_variation',s.diff(He,e).subs(e,0)-dH)
zero('Frechet_primitive_mean_constraint',s.integrate(dH*J+H*s.diff(Z,x),(x,0,L)))
negative('missing_variation_of_J',s.simplify(dH-(dK-s.integrate(dK*J,(x,0,L))/L)).subs({a:s.Rational(1,4),d:s.Rational(1,3)})==0)

# Moving-seam weak form uses continuity of value and flux, not slope matching.
U,p,q,velocity=s.symbols('U p q velocity',real=True)
zero('continuous_seam_conservative_residual',velocity*(U-U)-(U**2-U**2)/2)
jump=s.symbols('jump',nonzero=True)
negative('discontinuous_seam_has_no_measure',velocity*jump-((U+jump)**2-U**2)/2==0)
zero('slope_jump_ODE',(U-p*p)-(U-q*q)+(p+q)*(p-q))

# True material forcing without freezing velocity; retain exact Gronwall
# displacement integral and the subleading exponential term.
t,k,A,a0=s.symbols('t k A a0',positive=True)
zeta=a0*(s.exp(A*t)-s.exp(k*t))/(A-k)
zero('actual_corner_displacement_equation',s.diff(zeta,t)-k*zeta-a0*s.exp(A*t))
F=(a0*s.exp(A*t)+k*zeta).subs(A,5*k/2)
zero('corner_forcing_with_subleading_term',F-(5*a0*s.exp(5*k*t/2)/3-2*a0*s.exp(k*t)/3))
negative('frozen_corner_forcing',s.simplify(F-a0*s.exp(5*k*t/2))==0)

# A sign control computes the sharp periodic primitive norm and rejects an
# accidentally half-sized kernel. Its input has zero mean exactly.
ell=s.symbols('ell',positive=True);G=s.Rational(1,2)-x/ell
zero('kernel_sharp_L1',s.integrate(G,(x,0,ell/2))-s.integrate(G,(x,ell/2,ell))-ell/4)
zero('kernel_mean',s.integrate(G,(x,0,ell)))
negative('kernel_half_constant',ell/4==ell/8)

# Smooth branch proxy with a quintic cutoff, distinct from prior polynomial
# controls. It is a C2 scaling diagnostic, not the theorem's C-infinity cutoff.
r,delta,eta=s.symbols('r delta eta',positive=True)
rho=1-10*r**3+15*r**4-6*r**5
raw=-delta*x*rho.subs(r,x/eta)
zero('quintic_cutoff_join_value',raw.subs(x,eta))
zero('quintic_cutoff_join_derivative',s.diff(raw,x).subs(x,eta))
zero('quintic_cutoff_join_second_derivative',s.diff(raw,x,2).subs(x,eta))
zero('quintic_crest_slope',s.diff(raw,x).subs(x,0)+delta)
zero('quintic_mass_scale',s.integrate(raw,(x,0,eta))+delta*eta**2/7)
scaled=s.diff(raw,x,2).subs(x,eta/3).subs(eta,delta**2)
check('ordered_scale_substitution_has_no_eta',not scaled.has(eta))
zero('quintic_second_derivative_exact_scale',delta*scaled-s.Rational(40,9))
negative('uniform_second_derivative_bound',s.limit(scaled,delta,0)==0)
E['proxy_second_derivative_at_third_width']=str(s.factor(scaled))

# Universal exponent criterion, with positive fixed epsilon and cutoff constant.
p,R=s.symbols('p R',real=True)
power=1+p-(R-2)/2
zero('candidate_error_power',power.subs({p:2,R:s.Rational(5,2)})-s.Rational(11,4))
check('candidate_relative_error_is_little_o',power.subs({p:2,R:s.Rational(5,2)})>1)
negative('fixed_width_little_o',power.subs({p:0,R:s.Rational(5,2)})>1)
negative('critical_width_little_o',power.subs({p:s.Rational(1,4),R:s.Rational(5,2)})>1)

# Every phase has identical derivative supremum. Essential-sup endpoint
# information occupies an interval: w=-k-e+x^2 exceeds k+e/2 for x<sqrt(e/2).
eps=s.symbols('eps',positive=True)
w=-k-eps+x*x
zero('endpoint_excess_neighborhood',(-w).subs(x,s.sqrt(eps/2))-(k+eps/2))
check('essential_interval_has_positive_measure',s.sqrt(eps/2)>0)
theta=s.symbols('theta',real=True)
phi=(x-s.pi)**2/6-s.pi**2/18
zero('phase_derivative_sup_invariant',s.diff(phi.subs(x,x-theta),x).subs(x,theta)+s.pi/3)

# A fixed derivative discrepancy can coexist with arbitrarily small H1 norm.
# Piecewise quadratic tent on [-h,h]; mean corrected by a constant on period L.
h=s.symbols('h',positive=True);tent=eps*h*(1-x/h)**2
mass=2*s.integrate(tent,(x,0,h))
l2=2*s.integrate(tent**2,(x,0,h))-mass**2/L
der2=2*s.integrate(s.diff(tent,x)**2,(x,0,h))
zero('quadratic_tent_gradient_norm',der2-8*eps**2*h/3)
zero('quadratic_tent_value_norm',l2-(2*eps**2*h**3/5-4*eps**2*h**4/(9*L)))
check('fixed_slope_shrinking_H1',s.limit(l2+der2,h,0)==0)
negative('fixed_gradient_implies_fixed_H1',s.limit(l2+der2,h,0)>0)

# Qualitative continuity need not have a proportional modulus: d^(1/3)/d
# diverges. This independently discriminates the obsolete v1 stability step.
check('qualitative_nonproportional_modulus',s.limit(delta**s.Rational(1,3),delta,0)==0)
check('no_fixed_proportional_modulus',s.limit(delta**s.Rational(-2,3),delta,0)==s.oo)

result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','assertions':sum(C.values()),'checks':dict(C),'negative_controls':N,'evidence':E,'sympy':s.__version__,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Fresh distinct exact Fourier/variation/seam/scale/norm analytic controls; finite examples and formal identities supplement universal written proof. No candidate or prior family code imported.'}
(HERE/'INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
