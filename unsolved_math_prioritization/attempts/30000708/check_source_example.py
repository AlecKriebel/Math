"""Exact algebraic checks of a published Boman–Lindskog counterexample.

This validates source transcription; it is not original proof research and
does not numerically certify the published uniqueness theorems.
"""
import sympy as s
import json
from collections import Counter
counts=Counter()
def ck(expr,label):
    assert expr,label
    counts[label]+=1
def zero(expr,label):ck(s.simplify(s.cancel(expr))==0,label)
x,y,p,t,r=s.symbols('x y p t r',real=True)
rho=s.symbols('rho',positive=True)
f=(x**3-3*x*y*y)/(x*x+y*y)**3
zero(s.re((x+s.I*y)**(-3))-f,'real_density_transcription')
zero((x*x+y*y)**3-(x**3-3*x*y*y)**2-y*y*(3*x*x-y*y)**2,'absolute_density_bound')
zero(f.subs({x:rho*x,y:rho*y})-rho**(-3)*f,'density_homogeneity_minus3')
primitive=s.I/(2*(p+s.I*t)**2)
zero(s.diff(primitive,t)-(p+s.I*t)**(-3),'complex_line_primitive')
for pp in [s.Rational(j,7) for j in range(-20,21) if j]:
    P=primitive.subs(p,pp)
    zero(s.limit(P,t,s.oo),'primitive_at_positive_infinity')
    zero(s.limit(P,t,-s.oo),'primitive_at_negative_infinity')
    zero(s.diff(P,t)-(pp+s.I*t)**(-3),'rational_offset_derivative')
zero(f.subs({x:1,y:0})-1,'nonzero_positive_density')
zero(f.subs({x:-1,y:0})+1,'nonzero_negative_density')
# Polar density: r^-3 cos(3theta); angular absolute integral is 4.
theta=s.symbols('theta',real=True)
zero(s.trigsimp(f.subs({x:rho*s.cos(theta),y:rho*s.sin(theta)})-rho**(-3)*s.cos(3*theta)),'polar_density')
zero(12*s.integrate(s.cos(3*theta),(theta,0,s.pi/6))-4,'angular_absolute_integral')
eps=s.symbols('eps',positive=True)
zero(s.integrate(4*rho**(-2),(rho,eps,s.oo))-4/eps,'finite_exterior_total_variation')
ck(s.integrate(4*rho**(-2),(rho,0,eps))==s.oo,'infinite_origin_total_variation')
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'families':dict(sorted(counts.items())),'sympy_version':s.__version__,'scope':'Source-example transcription controls only. All uniqueness results and the counterexample family are credited to the cited literature; no original proof turn.'},indent=2,sort_keys=True))
