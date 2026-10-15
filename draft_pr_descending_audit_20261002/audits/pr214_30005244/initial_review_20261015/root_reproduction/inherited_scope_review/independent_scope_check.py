"""Separate exact controls for the ball-mode and compact-support argument.
No author checker is imported; no numerical eigenvalue computation is used.
"""
from fractions import Fraction as F
import sympy as s
import json
count=0
# The potential of unit density in the unit ball for G=1/(4*pi*r).
x,y,z,r=s.symbols('x y z r',real=True)
V=4*s.pi/3
potential=s.Rational(1,2)-(x*x+y*y+z*z)/6
H=-s.hessian(potential,(x,y,z))
assert H==s.eye(3)/3;count+=9
assert -sum(s.diff(potential,t,2) for t in (x,y,z))==1;count+=1
# It matches the exterior 1/(3r), including the radial derivative.
pin=s.Rational(1,2)-r*r/6;pout=1/(3*r)
assert pin.subs(r,1)==pout.subs(r,1);count+=1
assert s.diff(pin,r).subs(r,1)==s.diff(pout,r).subs(r,1);count+=1
# Average C2 on the constant modes gives -4/15 I (extra independent control).
energy=s.integrate(4*s.pi*r*r*pin,(r,0,1))*4*s.pi
assert s.simplify(-energy/(6*s.pi*V))==-s.Rational(4,15);count+=1
# Interior/exterior matching for each spherical harmonic and jump normalization.
for ell in range(1,151):
    a=F(1,2*ell+1)
    assert a*ell-a*(-ell-1)==1;count+=1
    shifted=F(ell,2*ell+1)-F(1,3)
    assert shifted==F(ell-1,3*(2*ell+1));count+=1
    if ell==1:assert shifted==0 and 2*ell+1==3
    else:assert shifted>=F(1,15)
    count+=1
ell=s.symbols('ell',integer=True,positive=True)
lam=ell/(2*ell+1)
assert s.simplify(lam.subs(ell,ell+1)-lam-1/((2*ell+1)*(2*ell+3)))==0;count+=1
# Scalar coefficients obtained by multiplying the exponential series directly.
for n in range(2,60):
    fact=s.factorial
    cf=s.I**n/fact(n)-s.I*s.I**(n-1)/fact(n-1)-s.I**(n-2)/fact(n-2)
    cg=-3*s.I**n/fact(n)+3*s.I*s.I**(n-1)/fact(n-1)+s.I**(n-2)/fact(n-2)
    assert s.simplify(cf-s.I**n*(n-1)**2/fact(n))==0;count+=1
    assert s.simplify(cg+s.I**n*(n-1)*(n-3)/fact(n))==0;count+=1
    if n>=4:
        assert (n-1)**2<=n*n and abs((n-1)*(n-3))<=n*n;count+=1
# Certified elementary series upper bound for e, independent of floating point.
e_upper=sum((F(1,int(s.factorial(n))) for n in range(5)),F(0))+F(1,100)
assert e_upper<F(11,4);count+=1
assert 2*e_upper-F(9,2)<1;count+=1
# Hilbert-Schmidt constants with all factors of pi canceled.
assert F(6,64)*F(32,3)==1;count+=1
assert F(3,4)*2*F(4,3)==2;count+=1
assert F(4,3)/6==F(2,9);count+=1
assert 1+F(2,9)*F(1,2)+2*F(1,2)**2<2;count+=1
# Resolvent and graph estimates at the explicit frequency.
k=F(1,10000);eps=2*k*k;eta=120*k*k
assert 30*eps<F(1,2);count+=1
assert F(1,30)*60*30==60;count+=1
assert 60*eps==eta<F(1,2);count+=1
assert eta/(1-eta)<=240*k*k;count+=1
assert 2+2*240==482;count+=1
trace_bound=-F(2,3)*k**3+3*482*k**4
assert trace_bound<0;count+=1
# Geometric removal: the radii have summable cubes, and shrink with j.
for j in range(1,51):
    ratio=F(1,2**(3*j+12))*F(1,7)
    assert F(0)<ratio<1;count+=1
    assert ratio/8==F(1,7*2**(3*(j+1)+12));count+=1
print(json.dumps({'status':'PASS','exact_assertions':count,'frequency':'1/10000','ball_constant_mode_dimension':3,'static_gap':'1/15','average_quadratic_mode_coefficient':'-4/15','imaginary_trace_upper_bound':str(trace_bound),'author_scope':'Arbitrary compact positive-volume empty-interior support; not a regular-particle counterexample','limitations':'Exact finite controls of formulas and constants. Completeness of the Helmholtz/spherical-harmonic decomposition, compact-mask convergence and Riesz persistence are verified in the written review, not certified by these checks.'},indent=2))
