#!/usr/bin/env python3
"""Supplementary independent identities and normalizations, not an existence proof."""
from pathlib import Path
import json
import sympy as s

A, C, theta = s.symbols('A C theta', positive=True)
V, B, q, gamma = s.symbols('V B q gamma', real=True)
x = s.symbols('x0:3', real=True)
r2 = sum(z*z for z in x)
rho = C*A**-3*s.exp(-r2/(2*A**2))
u = [V*z/A for z in x]
p = theta*A**(-q)*rho
e = theta*A**(-q)/(gamma-1)
E = rho*(e + sum(z*z for z in u)/2)
partial_t = lambda z: s.diff(z,A)*V + s.diff(z,V)*B
material = lambda z: partial_t(z)+sum(u[i]*s.diff(z,x[i]) for i in range(3))
results = []

def check(name, z):
    z = s.simplify(z)
    if z != 0:
        raise AssertionError((name,z))
    results.append({'name':name,'result':'exact zero'})

def ode(z):
    return z.subs(B,theta*A**(-q-1)).subs(q,3*(gamma-1))

check('arbitrary gamma, 3D: conservative mass',
      (partial_t(rho)+sum(s.diff(rho*u[i],x[i]) for i in range(3)))/rho)
for i in range(3):
    check(f'arbitrary gamma, 3D: conservative momentum {i}',
          ode((partial_t(rho*u[i])+sum(s.diff(rho*u[i]*u[j],x[j]) for j in range(3))+s.diff(p,x[i]))/rho))
check('arbitrary gamma, 3D: conservative energy',
      ode((partial_t(E)+sum(s.diff((E+p)*u[i],x[i]) for i in range(3)))/rho))
check('arbitrary gamma, 3D: equation of state',p-(gamma-1)*rho*e)
S = s.log(theta)+(1-gamma)*s.log(C)+(gamma-1)*r2/(2*A**2)
check('arbitrary gamma, 3D: entropy advection',material(S))
check('arbitrary gamma, 3D: entropy equation of state derivative',
      s.diff(p,x[0])/p-gamma*s.diff(rho,x[0])/rho-s.diff(S,x[0]))
check('arbitrary gamma, 3D: first integral',
      ode(partial_t(V**2/2+theta*A**(-q)/q)))

z=s.symbols('z',real=True)
I0=s.integrate(s.exp(-z*z/2),(z,-s.oo,s.oo))
I2=s.integrate(z*z*s.exp(-z*z/2),(z,-s.oo,s.oo))
check('1D Gaussian normalization',I0-s.sqrt(2*s.pi))
check('1D Gaussian second moment',I2-I0)
M=C*I0**3
check('3D mass normalization',M-C*(2*s.pi)**s.Rational(3,2))
check('3D total second moment normalization',3*C*A*A*I2*I0**2-3*A*A*M)
check('3D energy is three times scalar ODE energy',
      (3*M*V*V/2+M*theta*A**(-q)/(gamma-1)-3*M*(V*V/2+theta*A**(-q)/q)).subs(q,3*(gamma-1)))
check('3D entropy integral, C=1 and gamma=5/3',
      ((1-gamma)*s.log(C)*M+(gamma-1)*3*M/2-M).subs({C:1,gamma:s.Rational(5,3)}))

r=s.symbols('r',nonnegative=True)
xi=s.symbols('xi',positive=True)
source_M = 2*s.pi*s.sqrt(2)*C*s.integrate(s.exp(-xi)/s.sqrt(xi),(xi,0,s.oo))
source_E = 6*s.pi*s.sqrt(2)*C*s.integrate(s.exp(-xi)*s.sqrt(xi),(xi,0,s.oo))
check('published lambda=0 mass normalization',source_M-M)
check('published lambda=0 energy normalization',source_E-3*M/2)

t=s.symbols('t',real=True)
a=s.sqrt(1+t*t)
check('explicit monatomic scale equation',s.diff(a,t,2)-a**-3)
check('explicit monatomic scalar first integral',s.diff(a,t)**2+a**-2-1)
# The isentropic pressure-gradient acceleration is proportional to rho^(gamma-1),
# whereas the Gaussian full-Euler acceleration is linear with constant coefficient.
# This exact nonzero witness prevents accidental relabeling as an isentropic solution.
negative=s.simplify(1-s.Rational(5,3)*s.exp(-r*r/3))
witness=s.simplify(negative.subs(r,s.sqrt(3*s.log(2))))
assert witness == s.Rational(1,6)
results.append({'name':'negative control: isentropic substitution at t=0, radius squared=3 log 2','result':'nonzero: 1/6'})

report={'result':'PASS','exact_checks':len(results),'sympy_version':s.__version__,
        'checks':results,'limitations':['Analytic continuation, complete flow, positivity and Gaussian tails require the written audit.','These identities certify no bounded-entropy or isentropic existence claim.']}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:report[k] for k in ['result','exact_checks','sympy_version']}))
