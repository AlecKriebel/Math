#!/usr/bin/env python3
"""Exact algebra diagnostics for the historical Q3 proof; no spectral numerics.
Checks are explicit runtime exceptions and survive -O and -OO.
"""
import hashlib, json, platform
from pathlib import Path
import sympy as s


def require(condition, message):
    if not bool(condition):
        raise RuntimeError(message)

r=s.symbols('r', positive=True)
a,lam=s.symbols('a lam', real=True)
b=s.Rational(3,4)
d=s.Function('d')(r); dp=s.diff(d,r); dpp=s.diff(d,r,2)
V=r**b; W=lam*V; p=r**(2+b)
side=-2*V/r**2+3*s.diff(V,r)/r-s.diff(V,r,2)
require(s.simplify(side-s.Rational(7,16)*r**(-s.Rational(5,4)))==0,'side condition identity')
correction=2*(V/r**2-s.diff(V,r)/r)
require(s.simplify(correction-s.Rational(1,2)*r**(-s.Rational(5,4)))==0,'V prime correction')
exact=p*(dpp+2*dp/r-a*d/r**2)**2-(W+correction)*(r**2*dp**2+a*d**2)
reduced=p*(dpp**2-lam*dp**2)+a*(2*r**b*dp**2+(a-s.Rational(13,16))*r**(b-2)*d**2-lam*r**b*d**2)
boundary=2*r**(b+1)*dp**2-2*a*r**b*dp*d+a*(b-2)*r**(b-1)*d**2
require(s.simplify(exact-reduced-s.diff(boundary,r))==0,'full mode identity')
y=s.Function('y')(r); dy=s.diff(y,r)
dsub=r**(-b/2)*y
bracket=2*r**b*s.diff(dsub,r)**2+(a-s.Rational(13,16))*r**(b-2)*dsub**2-lam*r**b*dsub**2
transformed=2*dy**2+(a-s.Rational(41,32))*y**2/r**2-lam*y**2
require(s.simplify(bracket-transformed-s.diff(-b*y**2/r,r))==0,'angular transformation')
require(2-s.Rational(41,32)==s.Rational(23,32),'first angular potential')
num=s.integrate(4*r**s.Rational(19,4),(r,0,1))
den=s.integrate(p*(1-r**2)**2,(r,0,1))
quotient=s.simplify(num/den)
require(quotient==s.Rational(465,32),'trial quotient')
require(quotient<16<18,'exact parameter cap')
require(s.integrate(r**s.Rational(-3,4),(r,0,1))==4,'mean continuity constant')

# Verify the polynomial eigenbasis, including explicit ambient harmonicity.
x,t,z=s.symbols('x t z', real=True)
records=[]
for m in range(9):
    for odd in (False,True):
        gamma=s.Rational(1,4) if odd else -s.Rational(1,4)
        gegenbauer_parameter=gamma+s.Rational(1,2)
        P=s.Poly(s.gegenbauer(m,gegenbauer_parameter,z),z)
        pe=P.as_expr()
        J=(1-z*z)*s.diff(pe,z,2)-(2*gamma+2)*z*s.diff(pe,z)
        require(s.expand(J+m*(m+2*gamma+1)*pe)==0,'polynomial eigenvalue')
        harmonic=0
        for (j,),coef in P.terms():
            require((m-j)%2==0,'polynomial parity')
            harmonic += coef*(2*t)**j*(x**4+4*t**2)**((m-j)//2)
        if odd: harmonic *=x
        harmonic=s.expand(harmonic)
        require(s.expand(s.diff(harmonic,x,2)+x*x*s.diff(harmonic,t,2))==0,'ambient harmonic polynomial')
        k=2*m+int(odd)
        records.append({'m':m,'odd':odd,'k':k,'a_k':k*(k+1),'polynomial_degree_checked':True,'harmonicity':True})

# Verify the two angular sectors' conjugation exactly.
P=s.Function('P')(z); g=(1-z*z)**s.Rational(1,4)
Jminus=lambda f:(1-z*z)*s.diff(f,z,2)-s.Rational(3,2)*z*s.diff(f,z)
Jplus=lambda f:(1-z*z)*s.diff(f,z,2)-s.Rational(5,2)*z*s.diff(f,z)
require(s.simplify(Jminus(g*P)-g*(Jplus(P)-P/2))==0,'odd-sector conjugation')

# Direct coordinate/operator check off the axis; axis extension is proved by ambient IBP.
phi=s.symbols('phi', positive=True)
sn,cs=s.sin(phi),s.cos(phi)
xpolar=r*s.sqrt(sn); tpolar=r*r*cs/2
jac=s.det(s.Matrix([[s.diff(xpolar,r),s.diff(xpolar,phi)],[s.diff(tpolar,r),s.diff(tpolar,phi)]]))
require(s.trigsimp(jac+r*r/(2*s.sqrt(sn)))==0,'polar Jacobian')
rx=sn**s.Rational(3,2); phix=2*cs*s.sqrt(sn)/r
rt=cs/r; phit=-2*sn/r**2
Dx=lambda f:rx*s.diff(f,r)+phix*s.diff(f,phi)
Dt=lambda f:rt*s.diff(f,r)+phit*s.diff(f,phi)
checks={'rr':rx**2+xpolar**2*rt**2-sn,
        'r_phi':rx*phix+xpolar**2*rt*phit,
        'phi_phi':phix**2+xpolar**2*phit**2-4*sn/r**2,
        'r_first':Dx(rx)+xpolar**2*Dt(rt)-2*sn/r,
        'phi_first':Dx(phix)+xpolar**2*Dt(phit)-2*cs/r**2}
for name,expr in checks.items():
    require(s.trigsimp(s.simplify(expr))==0,'coordinate operator '+name)

result={'kind':'exact_symbolic_diagnostics_not_a_substitute_for_proof',
        'python':platform.python_version(),'sympy':s.__version__,'checks_survive_optimization':True,
        'scope':{'Q':3,'n':1,'R':1,'V':'r^(3/4)','W':'lambda r^(3/4)',
                 'lambda':'(alpha + min(beta,16))/2'},
        'side_condition':'(7/16) r^(-5/4)','gradient_correction':'(1/2) r^(-5/4)',
        'trial_quotient':str(quotient),'mean_functional_squared_bound':4,
        'angular_first_inverse_square_coefficient':'23/32',
        'mode_identity_exact':True,'angular_transformation_exact':True,
        'even_odd_angular_conjugation_exact':True,'polar_coordinate_operator_exact':True,
        'basis_diagnostics':records,
        'limitations':['Finite polynomial checks supplement the all-degree proof, not establish completeness.',
                       'Compactness, spectral-gap attainment, infinite-energy convention, and all-test convergence are proved analytically.']}
print(json.dumps(result,indent=2,sort_keys=True))
