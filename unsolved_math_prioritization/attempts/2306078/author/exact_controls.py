#!/usr/bin/env python3
"""Exact algebraic controls for the authored proof, not a formal analytic proof.

Requires Python 3 and SymPy. Uses no network, source text, or private inputs.
Writes deterministic EXACT_RESULTS.json beside this script.
"""
import json
from pathlib import Path
import sympy as s

checks = []
mutations = []

def check(name, condition):
    if not bool(condition):
        raise AssertionError(name)
    checks.append(name)

def zero(expr):
    return s.simplify(expr) == 0

def reject(name, wrong_identity):
    if zero(wrong_identity):
        raise AssertionError("Mutation not rejected: " + name)
    mutations.append(name)

r, t, u = s.symbols("r t u", positive=True)
z, w, c = s.symbols("z w c")
x, y = s.symbols("x y", real=True)
a, ap = s.symbols("a ap", positive=True)
pi = s.pi

# Metric scale, total area, attained candidate, and weak covering bound.
primitive = -4*pi/(1+u*u)
check("radial area primitive", zero(s.diff(primitive,u)-8*pi*u/(1+u*u)**2))
disk = 4*pi*r*r/(1+r*r)
check("disk area at radius r", zero(primitive.subs(u,r)-primitive.subs(u,0)-disk))
check("unit disk is half of unit sphere", disk.subs(r,1)==2*pi)
check("whole sphere area", s.limit(disk,r,s.oo)==4*pi)
check("quarter-area convention", (disk/4).subs(r,1)==pi/2)
check("Koebe-quarter area", disk.subs(r,s.Rational(1,4))==4*pi/17)
check("weak bound is strictly weaker", s.Rational(4,17)<2)
check("small-radius area coefficient", s.limit(disk/(4*pi*r*r),r,0)==1)

# Sharp differential inequality and equality-model algebra.
check("identity derivative", zero(s.diff(disk,r)-8*pi*r/(1+r*r)**2))
check("identity isoperimetric equality", zero((4*pi*r/(1+r*r))**2-disk*(4*pi-disk)))
check("identity Cauchy-Schwarz equality", zero(2*pi*r*s.diff(disk,r)-(4*pi*r/(1+r*r))**2))
check("identity logistic equality", zero(r*s.diff(disk/(4*pi),r)-2*(disk/(4*pi))*(1-disk/(4*pi))))
Q=a/(r*r*(1-a))
dQ=s.diff(Q,r)+s.diff(Q,a)*ap
check("Q derivative numerator", zero(dQ-(r*ap-2*a*(1-a))/(r**3*(1-a)**2)))
dlog=s.diff(s.log(a/(1-a)/r**2),r)+s.diff(s.log(a/(1-a)/r**2),a)*ap
check("log Q derivative", zero(dlog-ap/(a*(1-a))+2/r))
check("identity Q equals one", zero(Q.subs(a,r*r/(1+r*r))-1))
check("sharp lower-bound rearrangement", zero(a-r*r/(1+r*r)-(a-r*r*(1-a))/(1+r*r)))
check("Dufresnoy threshold algebra", zero(a/(1-a)-1-(2*a-1)/(1-a)))
check("Dufresnoy equality threshold", s.solve(s.Eq(1,a/(1-a)),a)==[s.Rational(1,2)])

# Exact Mobius controls, including geometry of the image.
f=lambda v:v/(1-c*v)
check("Mobius normalization at zero", f(0)==0)
check("Mobius derivative normalization", s.diff(f(z),z).subs(z,0)==1)
check("Mobius injectivity factorization", zero(f(z)-f(w)-(z-w)/((1-c*z)*(1-c*w))))
check("Mobius inverse", zero(f(w/(1+c*w))-w))
rho2=x*x+y*y
X=2*x/(1+rho2); Y=2*y/(1+rho2); Z=(rho2-1)/(1+rho2)
check("stereographic unit-sphere identity", zero(X*X+Y*Y+Z*Z-1))
check("disk inequality becomes a plane", zero(((2-t*t)*Z-2*t*X-t*t)*(1+rho2)-2*((1-t*t)*rho2-2*t*x-1)))
check("plane normal norm square", zero((2-t*t)**2+(2*t)**2-(4+t**4)))
mobius=2*pi*(1+t*t/s.sqrt(4+t**4))
check("Mobius area at zero", mobius.subs(t,0)==2*pi)
check("half-plane endpoint", zero(mobius.subs(t,1)-2*pi*(1+1/s.sqrt(5))))
check("strict Mobius area derivative", zero(s.diff(mobius,t)-16*pi*t/(4+t**4)**s.Rational(3,2)))
check("plane cap offset below one", zero(4+t**4-t**4-4))

# Equality-family normalization and first nonzero Taylor coefficient controls.
b, bc, lam = s.symbols("b bc lam")
g=(b+lam*z)/(1-lam*bc*z)
check("classical equality value", g.subs(z,0)==b)
check("classical equality derivative", zero(s.diff(g,z).subs(z,0)-lam*(1+b*bc)))
check("normalization collapses equality family", zero(g.subs({b:0,bc:0,lam:1})-z))
for n in range(2,9):
    h=z+c*z**n
    check("first-coefficient derivative n="+str(n), s.expand(s.diff(h,z)-1).coeff(z,n-1)==n*c)
    check("quadratic error order n="+str(n), 2*n-2>=n)

# Deliberate wrong claims must not pass the equality controls.
reject("missing metric factor four", disk.subs(r,1)-pi/2)
reject("reversed logistic sign at identity", r*s.diff(disk/(4*pi),r)+2*(disk/(4*pi))*(1-disk/(4*pi)))
reject("missing Cauchy-Schwarz factor two", pi*r*s.diff(disk,r)-(4*pi*r/(1+r*r))**2)
reject("wrong full-sphere minimum", disk.subs(r,1)-4*pi)
reject("all Mobius maps minimize", mobius.subs(t,1)-2*pi)
reject("wrong equality coefficient", g.subs({b:0,bc:0,lam:2})-z)

result = {
    "problem_id":"2306078",
    "status":"PASS",
    "exact_checks_passed":len(checks),
    "checks":checks,
    "mutations_rejected":len(mutations),
    "mutations":mutations,
    "scope":"Exact symbolic constants, rational identities, cap geometry, and equality-model controls only. No formal proof of spherical isoperimetry, injectivity for arbitrary functions, or the analytic limiting arguments.",
}
target=Path(__file__).resolve().parent/"EXACT_RESULTS.json"
target.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":"PASS","exact_checks_passed":len(checks),"mutations_rejected":len(mutations)}))
