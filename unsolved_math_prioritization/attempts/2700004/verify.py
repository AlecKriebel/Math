#!/usr/bin/env python3
"""Exact algebraic checks for the Gaussian full-Euler reconstruction.

These checks supplement the analytic smoothness, Gaussian integrability, and
ODE-continuation arguments in PROOF.md; they are not a PDE-existence proof.
No network, numerical search, or external data is used.
"""
import json
from pathlib import Path
import sympy as s

checks = []

def zero(name, expr):
    residual = s.simplify(expr)
    if residual != 0:
        raise AssertionError(f"{name}: {residual}")
    checks.append({"name": name, "result": "exact zero"})

t = s.symbols("t", real=True)
alpha = 1 + t**2
for d in (1, 2, 3, 5):
    x = s.symbols(f"x0:{d}", real=True)
    r2 = sum(z*z for z in x)
    gamma = 1 + s.Rational(2, d)
    rho = alpha**(-s.Rational(d, 2))*s.exp(-r2/(2*alpha))
    u = [t*z/alpha for z in x]
    p = rho/alpha
    e = s.Rational(d, 2)/alpha
    energy = rho*(e+sum(v*v for v in u)/2)
    entropy = s.log(p/rho**gamma)

    zero(f"d={d}: equation of state", p-(gamma-1)*rho*e)
    zero(f"d={d}: conservative continuity",
         (s.diff(rho,t)+sum(s.diff(rho*u[j],x[j]) for j in range(d)))/rho)
    for i in range(d):
        zero(f"d={d}: conservative momentum component {i}",
             (s.diff(rho*u[i],t)+
              sum(s.diff(rho*u[i]*u[j],x[j]) for j in range(d))+
              s.diff(p,x[i]))/rho)
    zero(f"d={d}: conservative total energy",
         (s.diff(energy,t)+
          sum(s.diff((energy+p)*u[j],x[j]) for j in range(d)))/rho)
    S = (gamma-1)*r2/(2*alpha)
    zero(f"d={d}: entropy advected",
         s.diff(S,t)+sum(u[j]*s.diff(S,x[j]) for j in range(d)))
    # Check the logarithm of the equation-of-state ratio without branch rewrites.
    zero(f"d={d}: entropy spatial derivative",
         s.diff(p,x[0])/p-gamma*s.diff(rho,x[0])/rho-s.diff(S,x[0]))
    zero(f"d={d}: entropy temporal derivative",
         s.diff(p,t)/p-gamma*s.diff(rho,t)/rho-s.diff(S,t))
    zero(f"d={d}: mass-energy formula",
         s.Rational(d,2)*t*t/alpha+s.Rational(d,2)/alpha-s.Rational(d,2))

    v = s.symbols(f"v0:{d}", real=True)
    kinetic_q = sum((x[i]-t*v[i])**2+v[i]**2 for i in range(d))
    completed_q = alpha*sum((v[i]-u[i])**2 for i in range(d))+r2/alpha
    zero(f"d={d}: kinetic completion of square", kinetic_q-completed_q)
    zero(f"d={d}: free-transport quadratic invariant",
         s.diff(kinetic_q,t)+sum(v[j]*s.diff(kinetic_q,x[j]) for j in range(d)))

# Exact all-d radial identities.
d, R = s.symbols("d R", positive=True)
h = t/alpha
logrho = -d*s.log(alpha)/2-R/(2*alpha)
D = lambda F: s.diff(F,t)+2*h*R*s.diff(F,R)
zero("symbolic d: continuity", D(logrho)+d*h)
zero("symbolic d: momentum coefficient", s.diff(h,t)+h*h-alpha**-2)
zero("symbolic d: conserved material radius", D(R/alpha))

# Arbitrary gamma ODE ansatz; represent a, a', a'' by independent symbols.
A, V, B, theta, q, gamma = s.symbols(
    "A V B theta q gamma", positive=True)
H = V/A
DT = lambda F: s.diff(F,A)*V+s.diff(F,V)*B+2*H*R*s.diff(F,R)
lr = -d*s.log(A)-R/(2*A*A)
e = theta*A**(-q)/(gamma-1)
zero("arbitrary gamma: continuity", DT(lr)+d*H)
zero("arbitrary gamma: momentum after ODE",
     (B/A-theta*A**(-q-2)).subs(B,theta*A**(-q-1)))
zero("arbitrary gamma: internal energy",
     (DT(e)+(gamma-1)*e*d*H).subs(q,d*(gamma-1)))
zero("arbitrary gamma: entropy transport",
     DT((gamma-1)*R/(2*A*A)))
zero("arbitrary gamma: ODE first integral derivative",
     DT(V*V/2+theta*A**(-q)/q).subs(B,theta*A**(-q-1)))
zero("arbitrary gamma: energy equals d times ODE energy",
     (d*V*V/2+theta*A**(-q)/(gamma-1)-
      d*(V*V/2+theta*A**(-q)/q)).subs(q,d*(gamma-1)))
zero("monatomic ODE explicit solution",
     s.diff(s.sqrt(alpha),t,2)-alpha**(-s.Rational(3,2)))

# Flow equation and composition.
b, c = s.symbols("b c", real=True)
scale = s.sqrt(alpha)/s.sqrt(1+b*b)
zero("flow equation", s.diff(scale,t)-t*scale/alpha)
zero("flow composition",
     s.sqrt(alpha)/s.sqrt(1+b*b)*s.sqrt(1+b*b)/s.sqrt(1+c*c)-
     s.sqrt(alpha)/s.sqrt(1+c*c))

# A negative control: replacing the full pressure by the isentropic rho^gamma
# must NOT be reported as solving the same momentum equation.
rho3 = (1+t*t)**(-s.Rational(3,2))*s.exp(-R/(2*(1+t*t)))
isentropic_force_coeff = -s.Rational(5,3)*rho3**s.Rational(2,3)/(1+t*t)
bad_momentum_coeff = (1+t*t)**-2+isentropic_force_coeff
bad_at_positive_radius = s.simplify(bad_momentum_coeff.subs({t:0,R:3*s.log(2)}))
assert bad_at_positive_radius == s.Rational(1,6)
checks.append({
    "name": "negative control: isentropic coefficient mismatch at t=0, R=3 log 2",
    "result": "nonzero: 1/6"
})

report = {
    "problem_id": 2700004,
    "result": "PASS",
    "sympy_version": s.__version__,
    "exact_checks": len(checks),
    "dimensions_checked_directly": [1, 2, 3, 5],
    "limitations": [
        "Analytic integrability and global ODE continuation use the written proof.",
        "No bounded-entropy or isentropic existence theorem is certified.",
        "No novelty or literature-completeness claim is made."
    ],
    "checks": checks
}
out = Path(__file__).with_name("checks.json")
out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
print(json.dumps({k: report[k] for k in ("result","exact_checks","sympy_version")}))

