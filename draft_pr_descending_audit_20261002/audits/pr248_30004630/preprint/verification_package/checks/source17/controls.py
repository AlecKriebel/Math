"""Independent exact controls: they do not replace the analytic PDE derivation."""
from pathlib import Path
from datetime import datetime, timezone
import json
import sympy as sp

assertions = []
def check(name, proposition):
    assert bool(proposition), name
    assertions.append(name)

r, h, a, c, t, epsilon = sp.symbols('r h a c t epsilon', positive=True, real=True)
pi = sp.pi
e = sp.sin(pi*r)/(sp.sqrt(2*pi)*r)
check('radial PDE identity', sp.simplify(sp.diff(e,r,2)+2*sp.diff(e,r)/r+pi**2*e)==0)
check('normalization in actual ball volume', sp.simplify(4*pi*sp.integrate(e**2*r**2,(r,0,1)))==1)
check('origin finite value', sp.limit(e,r,0)==pi/sp.sqrt(2*pi))
check('boundary Dirichlet value', sp.simplify(e.subs(r,1))==0)
check('spatial interpolation identity', sp.Rational(1,10)==sp.Rational(4,5)/12+sp.Rational(1,5)/6)
check('temporal interpolation identity', sp.Rational(1,5)==sp.Rational(4,5)/4)

# Derive the kernel before choosing center; do not import the author's checker.
b = sp.simplify(a/pi*sp.integrate(sp.sin(pi*(1-t)),(t,c-h,c+h)))
d = sp.simplify(a*sp.integrate(sp.cos(pi*(1-t)),(t,c-h,c+h)))
check('general centered terminal displacement', sp.simplify(b-2*a*sp.sin(pi*c)*sp.sin(pi*h)/pi**2)==0)
check('general centered terminal velocity', sp.simplify(d+2*a*sp.cos(pi*c)*sp.sin(pi*h)/pi)==0)
b = sp.simplify(b.subs(c,sp.Rational(1,2)))
d = sp.simplify(d.subs(c,sp.Rational(1,2)))
check('velocity symmetry cancellation', d==0)
gap = sp.simplify(2*a*h-pi*b)
linear_growth = sp.expand((gap+b**2/2).subs(a,h))
coefficient = pi**2/3+2/pi**2
check('full linear baseline leading coefficient', sp.simplify(sp.limit(linear_growth/h**4,h,0)-coefficient)==0)
check('normalized growth leading coefficient', sp.simplify(sp.limit(linear_growth/(2*h**4),h,0)-coefficient/2)==0)
check('normalized growth ratio zero', sp.limit(linear_growth/(2*h**3),h,0)==0)
trial = sp.simplify((gap+b**2/2-epsilon*b).subs(h,pi*epsilon/(2*a)))
check('perturbed trial leading improvement', sp.limit(trial/epsilon**2,epsilon,0)==-sp.Rational(1,2))
check('fixed amplitude comparison cubic term', sp.simplify(sp.limit((trial+epsilon**2/2)/epsilon**3,epsilon,0)-pi**5/(24*a**2))==0)

# A sharper enclosing parabolic cap confirms that the submitted simpler bound is safe.
delta,s=sp.symbols('delta s',positive=True,real=True)
cap_squared=sp.simplify(sp.integrate((delta-2*s**2)**2,(s,-sp.sqrt(delta/2),sp.sqrt(delta/2))))
check('enclosing parabolic cap squared integral', sp.simplify(cap_squared-8*sp.sqrt(2)*delta**sp.Rational(5,2)/15)==0)
check('submitted positive part constant dominates', sp.simplify(cap_squared/(sp.sqrt(2)*delta**sp.Rational(5,2)))<1)
check('stability contradiction exponent', sp.Rational(9,4)>2)

receipt = {
 'status':'PASS', 'utc':datetime.now(timezone.utc).isoformat(),
 'assertions':len(assertions),'checks':assertions,'sympy_version':sp.__version__,
 'exact_linear_pulse_leading_coefficient':str(coefficient),
 'boundaries':'Finite exact identities only. No nonlinear PDE simulation, numerical Strichartz constant, novelty assertion, or substitute for INDEPENDENT_DERIVATION.md.'
}
Path(__file__).with_name('INDEPENDENT_CONTROLS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
