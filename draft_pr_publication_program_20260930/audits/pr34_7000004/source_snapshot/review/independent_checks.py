#!/usr/bin/env python3
"""Independent exact local controls; no global linking certificate is asserted."""
from pathlib import Path
import json
import sympy as s
checks={}
def check(name, statement):
    assert bool(statement),name
    checks[name]='PASS'
def zero(expr):
    if isinstance(expr,s.MatrixBase):return all(s.simplify(z)==0 for z in expr)
    return s.simplify(expr)==0
k,tau,tp,theta,thetap=s.symbols('k tau tp theta thetap',real=True)
T=s.Matrix([1,0,0]);N=s.Matrix([0,1,0]);B=s.Matrix([0,0,1])
Tp=k*N;Np=-k*T+tau*B;Bp=-tau*N
D=s.Matrix.hstack(Tp,Np,Bp)
check('frame_derivative_skew',zero(D+D.T))
check('binormal_twist_density',zero(T.dot(B.cross(Bp))-tau))
check('normal_twist_density',zero(T.dot(N.cross(Np))-tau))
V=s.cos(theta)*N+s.sin(theta)*B
Vp=s.cos(theta)*Np+s.sin(theta)*Bp+thetap*(-s.sin(theta)*N+s.cos(theta)*B)
check('rotating_normal_twist',zero(T.dot(V.cross(Vp))-(tau+thetap)))
Bpp=-tp*N-tau*Np
check('spherical_geodesic_curvature_numerator',zero(Bpp.dot(B.cross(Bp))-tau**2*k))
check('binormal_speed_squared',zero(Bp.dot(Bp)-tau**2))
# Both torsion signs must give the same pullback curvature integral, with the
# outward-sphere convention: kg_B = k/|tau| and ds_B = |tau| ds.
for a in [-3,-1,1,3]:
    for b in [-2,0,2]:
        check(f'curvature_pullback_tau{a}_k{b}',s.Rational(a*a*b,abs(a)**3)*abs(a)==b)
# Fixed spatial u has moving components (a,b,c) in the Darboux frame.
a,b,c=s.symbols('a b c',real=True)
ap=k*b;bp=-k*a+tau*c;cp=-tau*b
# cos(theta_u)=c/h, sin(theta_u)=-b/h; atan2 derivative cancels h.
angle_prime=s.cancel((c*(-bp)-(-b)*cp)/(b*b+c*c))
check('angle_derivative_formula',zero(angle_prime-(-tau+k*a*c/(b*b+c*c))))
check('angle_zero_crossing_sign',zero(angle_prime.subs(c,0)+tau))
check('great_circle_transversality',zero(cp+tau*b))
# Ruled strip F(s,r)=gamma(s)+r N(s) has fundamental coefficients at r=0:
# I=identity, II=[[0,tau],[tau,0]], so K=-tau^2, independently of k.
II=s.Matrix([[Tp.dot(B),Np.dot(B)],[Np.dot(B),0]])
check('strip_gaussian_curvature',zero(II.det()+tau**2))
# The source's printed Example 4.2 has missing /6 factors, confirmed by
# reading (not executing) its author-hosted Mathematica notebook.
t=s.symbols('t',real=True)
r=3+s.sin(t);angle=s.Rational(5,2)*s.cos(t)
x=r*s.cos(angle);y=r*s.sin(angle)
check('printed_example_radicand',zero((1-x*x-y*y)-(1-r*r)))
check('printed_example_invalid_at_zero',s.simplify((1-x*x-y*y).subs(t,0))==-8)
check('printed_example_negative_all_parameters_upper_bound',1-2**2==-3)
r6=r/6
check('notebook_radicand_identity',zero(1-r6*r6-(53+s.cos(2*t)-12*s.sin(t))/72))
check('notebook_radicand_lower_bound',1-s.Rational(4,6)**2==s.Rational(5,9))
planar_speed_squared=s.diff(r6,t)**2+r6**2*s.diff(angle,t)**2
check('polar_speed_squared',zero(planar_speed_squared-(s.cos(t)**2/s.Integer(36)+s.Rational(25,144)*(3+s.sin(t))**2*s.sin(t)**2)))
check('speed_at_sin_zero',planar_speed_squared.subs(t,0)==s.Rational(1,36))
check('angle_range_less_full_turn',s.Rational(5)<2*s.pi)
# Gauss-Bonnet range controls for genuine Jordan regions 0<A<4pi.
for numerator in range(1,8):
    area=s.Rational(numerator,2)*s.pi
    check(f'gauss_bonnet_area_{numerator}',abs(2*s.pi-area)<2*s.pi)
# A unit circle's Frenet binormal is constant, so it cannot be injective.
gamma=s.Matrix([s.cos(t),s.sin(t),0])
check('circle_binormal_constant',zero(gamma.diff(t).cross(gamma.diff(t,2))-B))
out={'passed':len(checks),'failed':0,'sympy_version':s.__version__,'checks':checks,'scope':'Exact local frame, sign, curvature, and source-typo controls. No full-target theorem, global linking value, or numerical example certification.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
