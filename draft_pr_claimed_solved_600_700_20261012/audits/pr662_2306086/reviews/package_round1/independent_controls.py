#!/usr/bin/env python3
"""Fresh adversarial exact controls; uses no supplied mathematical modules."""
import json
import sympy as s
C=[]
def need(ok,label):
 if not ok:raise ValueError(label)
 C.append(label)
def zero(e,label):need(s.cancel(e)==0,label)
z,w=s.symbols('z w'); u=s.symbols('u',real=True)
# Independently parameterize the entire real Koepf extreme-point family.
F=z/(1-2*u*z+z*z)
Fw=w/(1-2*u*w+w*w)
zero(F-Fw-(z-w)*(1-z*w)/((1-2*u*z+z*z)*(1-2*u*w+w*w)), 'two_boundary_pole_family_injective_factorization')
P=s.diff(F,z,2)/s.diff(F,z)
A=s.cancel(s.Rational(3,4)*P.subs(z,s.I/2)+s.I)
A2=s.cancel(A*s.conjugate(A))
zero(A2-s.Rational(16,25)*(289*u*u+36)/(16*u*u+9),'entire_extreme_family_exact_value_at_i_over_2')
zero(s.Rational(208,25)-A2-s.Rational(1296,25)*(1-u*u)/(16*u*u+9),'family_upper_bound_208_over25_for_minus1_le_u_le_1')
need(s.Rational(256,25)>s.Rational(208,25),'admissible_two_slit_h_exceeds_entire_linear_extreme_family_here')
h=z/(1-z*z)
Ah=s.cancel(s.Rational(3,4)*(s.diff(h,z,2)/s.diff(h,z)).subs(z,s.I/2)+s.I)
need(Ah==s.Rational(16,5)*s.I,'h_value_i_over_2')
# A distinct inverse-transform equality example: complex a and lambda, not a Koebe rotation.
a=(1+s.I)/4; ac=s.conjugate(a); lam=s.I
k=z/(1-lam*z)**2
psi=(z-a)/(1-ac*z)
kprime=s.diff(k,z)
f=s.cancel((k.subs(z,psi)-k.subs(z,-a))/((1-a*ac)*kprime.subs(z,-a)))
need(s.simplify(f.subs(z,0))==0 and s.simplify(s.diff(f,z).subs(z,0))==1,'inverse_transform_normalized')
AA=s.cancel((1-a*ac)*(s.diff(f,z,2)/s.diff(f,z)).subs(z,a)-2*ac)
need(s.simplify(AA-4*lam)==0,'inverse_transform_equality_at_complex_point')
a2=s.diff(f,z,2).subs(z,0)/2; a3=s.diff(f,z,3).subs(z,0)/6
need(s.simplify(4*a3-3*a2*a2)!=0,'original_equality_map_not_koebe_rotation')
need(s.im(s.expand_complex(a2))!=0,'equality_example_outside_real_class')
# Affine normalization works even with a negative real derivative.
g=7-3*h
zero(s.diff(g,z,2)/s.diff(g,z)-s.diff(h,z,2)/s.diff(h,z),'negative_real_affine_normalization_invariant')
# Real-axis endpoint pair obstructs even recentering the disk.
x=s.symbols('x',real=True)
for sign in (-1,1):
 k=z/(1-sign*z)**2
 ax=s.cancel((1-x*x)*(s.diff(k,z,2)/s.diff(k,z)).subs(z,x)-2*x)
 need(ax==4*sign,'real_axis_endpoint_'+str(sign))
r=s.Rational(3,5)
endpoints=[4*r/(1-r*r),-4*r/(1-r*r)]
need((endpoints[0]-endpoints[1])/2==s.Rational(15,4),'recentered_source_disk_radius_at_real_three_fifths')
# Im z -> 0 does not by itself give a Koebe limiting obstruction at disk endpoints.
e=s.symbols('e',positive=True); zz=1-e+s.I*e; zc=s.conjugate(zz)
delta2=-(zz-zc)**2/(4*(1-zz*zz)*(1-zc*zc))
need(s.limit(s.cancel(delta2),e,0)==s.Rational(1,8),'endpoint_path_delta_squared_limit_one_eighth')
# Both global-gap obstructions are exact, without numerical optimization.
t=s.symbols('t',positive=True)
need(s.limit(8*t/(1+t*t),t,1,dir='-')==4,'boundary_approach_to_i_saturates_lower_bound')
need(s.limit(16-48*t*t/(1+t*t)**2,t,0,dir='+')==16,'interior_real_approach_saturates_koebe_squared')
# Naive derivative of an argument envelope needs a real argument about derivatives.
# The Rodemich addendum's rational lower margin is exact, independently recomputed.
need(4*((s.Rational(99,10000)*500/s.Rational(11,4))**2+s.Rational(9,10)**2)==s.Rational(81,5),'rodemich_countermodel_margin_exact')
need(s.Rational(81,5)>16,'rodemich_countermodel_outside_globally_univalent_class')
print(json.dumps({'status':'PASS','checks':len(C),'labels':C,'new_extreme_family_bound_squared':'208/25','admissible_h_squared':'256/25','scope':'Exact controls supplement the written proof; no sharp-radius or novelty certificate.'},indent=2,sort_keys=True))
