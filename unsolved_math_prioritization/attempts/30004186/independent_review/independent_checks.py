#!/usr/bin/env python3
"""Independent exact diagnostics for the scoped Ostrovsky proof.
Uses SymPy for polynomial/rational identities; no PDE simulation.
"""
import sympy as s
import json, hashlib
from collections import Counter
from pathlib import Path
c=Counter()
def check(ok,name):
    assert bool(ok), name
    c[name]+=1

def zero(expr,name): check(s.cancel(s.expand(expr))==0,name)

x,P,R=s.symbols('x P R',positive=True)
L=2*P;k=P/3; speed=k*k
phi=(x-P)**2/6-P*P/18
primitive=s.integrate(phi,x)
primitive-=s.integrate(primitive,(x,0,L))/L
zero(s.integrate(phi,(x,0,L)),'profile_mean')
zero((phi-speed)*s.diff(phi,x)-primitive,'traveling_profile_equation')
zero(phi.subs(x,0)-speed,'crest_value')
zero(s.diff(phi,x).subs(x,0)+k,'right_crest_slope')
zero(s.diff(phi,x).subs(x,L)-k,'left_crest_slope')
zero(s.integrate(primitive,(x,0,L)),'primitive_mean')
zero(s.integrate(s.Rational(1,2)-x/L,(x,0,L/2))-
     s.integrate(s.Rational(1,2)-x/L,(x,L/2,L))-L/4,'primitive_kernel_L1')

# Exact nonlinear characteristic lift of the unperturbed wave, with R=e^(k*t).
z=L*x/(x+(L-x)*R)
zt=s.diff(z,R)*k*R
zero(zt-(phi-speed).subs(x,z),'background_characteristic')
zero(s.diff(phi.subs(x,z),R)*k*R-primitive.subs(x,z),'background_acceleration')
zero(s.diff(z,x).subs(x,0)-1/R,'background_right_jacobian')
zero(s.diff(z,x).subs(x,L)-R,'background_left_jacobian')

# Generic finite polynomial coordinates. L=2; |a|<=1/4 ensures X'>=1/2.
xx=s.symbols('xx',real=True)
for a in [s.Rational(-1,4),s.Rational(0),s.Rational(1,4)]:
    X=xx+a*xx*(2-xx);Xp=s.diff(X,xx)
    for b,d in [(s.Rational(1,3),s.Rational(2,5)),(s.Rational(-2,3),s.Rational(1,7)),(0,s.Rational(-1,2))]:
        V=1+b*xx*(2-xx)+d*xx*(2-xx)*(xx-1)
        V-=s.integrate(V*Xp,(xx,0,2))/2
        K=s.integrate(V*Xp,(xx,0,xx))
        H=K-s.integrate(K*Xp,(xx,0,2))/2
        zero(V.subs(xx,0)-V.subs(xx,2),'coordinate_endpoint_values')
        zero(s.integrate(V*Xp,(xx,0,2)),'coordinate_physical_mean')
        zero(H.subs(xx,0)-H.subs(xx,2),'primitive_endpoint_values')
        zero(s.diff(H,xx)-V*Xp,'coordinate_primitive_derivative')
        zero(s.integrate(H*Xp,(xx,0,2)),'coordinate_primitive_mean')
        zero(s.integrate(H*Xp+V*s.diff(V,xx),(xx,0,2)),'physical_mean_conservation')
        w=s.diff(V,xx)/Xp
        wt=(s.diff(H,xx)*Xp-s.diff(V,xx)**2)/Xp**2
        zero(wt-(V-w*w),'characteristic_Riccati_identity')

wm,wp,v=s.symbols('wm wp v')
zero((v-wm**2)-(v-wp**2)+(wm+wp)*(wm-wp),'corner_jump_equation')
A=s.Rational(5,2);kap=s.Rational(1);eps=s.Rational(1,10)
check(A-2*kap==s.Rational(1,2),'growth_rate_difference')
check(A/(A-kap)==s.Rational(5,3),'crest_forcing_constant')
check(3-(A-2*kap)/(2*kap)==s.Rational(11,4),'error_power')
q=s.symbols('q',positive=True)
delta=2*eps*q**4
C0=s.symbols('C0',positive=True)
error_ratio=s.Rational(10,3)*C0*delta**2*(1/q-1)
zero(error_ratio-s.Rational(2,15)*C0*q**7*(1-q),'log_time_error_ratio')
for C in [1,10,100]:
    for n in range(4,21):
        val=error_ratio.subs({q:s.Rational(1,2**n),C0:C})
        check(0<val<s.Rational(1,2),'finite_small_delta_error_controls')

# C1 polynomial cutoff control: only a scaling diagnostic, not the C-infinity
# cutoff asserted in the theorem. The candidate uses a standard smooth cutoff.
y,dd=s.symbols('y dd',positive=True)
rho=1-3*y*y+2*y**3
zero(s.diff(rho,y)+6*y*(1-y),'cutoff_derivative_factorization')
check(s.integrate(y*rho,(y,0,1))==s.Rational(3,20),'cutoff_integral')
raw=-dd*x*rho.subs(y,x/dd**2)
zero(raw.subs(x,0),'cutoff_crest_value')
zero(s.diff(raw,x).subs(x,0)+dd,'cutoff_crest_slope')
zero(s.integrate(raw,(x,0,dd**2))+s.Rational(3,20)*dd**5,'cutoff_mass_scaling')

receipt={'status':'PASS','sympy_version':s.__version__,'checks':dict(c),
         'assertions':sum(c.values()),
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'scope':'Exact finite algebra/coordinate/scale diagnostics; general PDE and norm conclusions rest on the written review'}
print(json.dumps(receipt,indent=2))
