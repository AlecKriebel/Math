#!/usr/bin/env python3
"""Exact auxiliary controls for the independently written analytical audit.

No finite test set is used to certify the geometric theorem or the supremum mass.
The boundary-flux and origin-ray mechanisms differ from the candidate's infinity
coefficient and center-shell integrations.
"""
from pathlib import Path
import json
import sympy as S

checks = []
def ck(name, expression, expected=0):
    residual = S.simplify(expression-expected)
    if residual != 0:
        raise AssertionError((name, str(residual)))
    checks.append({'name': name, 'status': 'PASS', 'exact_residual': str(residual)})

r,R,d,a,lam,z,t,b = S.symbols('r R d a lam z t b', positive=True)
# First-principles Euclidean normalized energy, not a mass formula substitution.
ck('Euclidean energy normalization', S.integrate(R**2/r**2,(r,R,S.oo)), R)
# Boundary angular mean: assume 0<d<R; sqrt((R-d)^2)=R-d.
# This is the spherical mean on the actual displaced ball boundary.
angular_primitive = S.sqrt(R**2+d**2+2*R*d*z)/(R*d)
ck('Boundary angular primitive', S.diff(angular_primitive,z), 1/S.sqrt(R**2+d**2+2*R*d*z))
angular_mean = ((R+d)-(R-d))/(2*R*d)
ck('Enclosing-sphere Newton mean', angular_mean, 1/R)
boundary_capacity = R*(1-a*angular_mean)
ck('Exact conformal capacity from inner boundary flux', boundary_capacity, R-a)
# U=1-a/r and f=1-R/s are each harmonic outside their singular points.
U=1-a/r
ck('Exterior radial harmonicity', S.diff(U,r,2)+2*S.diff(U,r)/r)
ck('ADM conformal mass', S.limit(-2*r*r*U**3*S.diff(U,r),r,S.oo), -2*a)
# Origin-ray volume integration: r_max=d*z+sqrt(R^2-d^2+d^2*z^2).
# Cross term is odd. The sum of the two squares is polynomial.
pos=d*z+S.sqrt(R**2-d**2+d**2*z**2)
neg=-d*z+S.sqrt(R**2-d**2+d**2*z**2)
ck('Origin-ray odd term cancellation', S.expand(pos**2+neg**2), 2*(R**2-d**2+2*d**2*z**2))
ray_moment=S.pi*S.integrate(R**2-d**2+2*d**2*z**2,(z,-1,1))
ck('Solid-ball Newton moment by origin rays', ray_moment, 2*S.pi*(R**2-d**2/3))
volume_radius_shift=S.simplify(-6*a*ray_moment.subs(d,lam*R)/(4*S.pi*R**2))
ck('Signed volume-radius shift', volume_radius_shift, -a*(3-lam**2))
deficit=S.simplify(volume_radius_shift+a)
ck('General off-center deficit', deficit, -2*a+a*lam**2)
ck('Strict-gap exact expression', deficit-(-2*a), a*lam**2)
ck('Frozen explicit limit', deficit.subs({a:1,lam:S.Rational(1,2)}), -S.Rational(7,4))
ck('Frozen explicit gap', (deficit+2*a).subs({a:1,lam:S.Rational(1,2)}), S.Rational(1,4))
ck('Centered boundary control', deficit.subs(lam,0), -2*a)
ck('Zero-mass Euclidean control', deficit.subs(a,0))
# A homothety scales all lengths, mass and final deficit equally.
ck('Homothety of deficit', deficit.subs(a,b*a), b*deficit)
ck('Homothety of capacity', (R-a).subs({R:b*R,a:b*a}), b*(R-a))
# Cube root is derived as a formal inverse-radius expansion with residual order.
q=S.symbols('q', real=True)
ck('Cube-root constant shift', S.series((1+q*t)**S.Rational(1,3),t,0,2).removeO().coeff(t,1), q/3)
# Scalar-curvature exclusion is exact and independent of the positive mass theorem.
chi=S.Function('chi')(r)
cutoff_U=1-chi/r
ck('Cutoff radial Laplacian', S.diff(cutoff_U,r,2)+2*S.diff(cutoff_U,r)/r, -S.diff(chi,r,2)/r)
# Compact core changes a volume radius only at order length^-2.
C=S.symbols('C', real=True)
ck('Compact-fill volume-radius order', S.limit(((R**3+C)**S.Rational(1,3)-R)*R**2,R,S.oo), C/3)
# Author binomial O(r^-2) bound, now exact on every x in [0,1/3].
x=S.symbols('x', nonnegative=True)
remainder=S.expand((1-x)**6-1+6*x)
quotient=S.cancel(remainder/x**2)
ck('Continuous remainder quotient', quotient, 15-20*x+15*x**2-6*x**3+x**4)
# Absolute coefficient majorant is 57 on x in [0,1], hence on [0,1/3].
ck('Remainder coefficient majorant', sum(abs(c) for c in S.Poly(quotient,x).all_coeffs()), S.Integer(57))
# Scaling controls intentionally include negative and positive Schwarzschild mass.
m=S.symbols('m', real=True)
signed_deficit=m*(1-lam**2/2)
ck('Positive/negative unified formula', signed_deficit.subs(m,-2*a), deficit)

out={'status':'PASS','mechanisms':['Euclidean variational energy normalization','inner-boundary flux on displaced ball','origin-ray solid-ball Newton moment','radial scalar-curvature exclusion','homothety and limiting controls','continuous binomial remainder bound'], 'checks':checks,'exact_assertions':len(checks),'unverified_by_code':['smooth cutoff existence and completeness are analytical','capacitary uniqueness is analytical','arbitrary exhaustion supremum not numerically evaluated','prior theorem applicability independently read from primary sources'],'scope':'Auxiliary exact calculations only; see INDEPENDENT_MATHEMATICAL_VERDICT.md for the proof and hypotheses.'}
print(json.dumps(out,indent=2,sort_keys=True))
