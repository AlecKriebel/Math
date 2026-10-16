#!/usr/bin/env python3
"""Exact finite checks for an analytic bridge; not a PDE or priority certificate."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sympy as s

checks = []
def check(name, expression):
    reduced = s.simplify(expression)
    assert reduced == 0, (name, reduced)
    checks.append({"name": name, "residual": "0"})

pi = s.pi
r = s.symbols("r", positive=True)
radial = s.sin(pi*r)/(s.sqrt(2*pi)*r)
check("normalized radial eigenfunction", 4*pi*s.integrate(radial**2*r**2, (r, 0, 1))-1)
check("radial Laplacian eigenvalue", s.diff(radial,r,2)+2*s.diff(radial,r)/r+pi**2*radial)
check("regular center value", s.limit(radial,r,0)-pi/s.sqrt(2*pi))
check("Dirichlet trace", radial.subs(r,1))

h,t = s.symbols("h t", positive=True)
endpoint = s.integrate(h*s.sin(pi*(1-t))/pi, (t,s.Rational(1,2)-h,s.Rational(1,2)+h))
velocity = s.integrate(h*s.cos(pi*(1-t)), (t,s.Rational(1,2)-h,s.Rational(1,2)+h))
check("pulse linear endpoint", endpoint-2*h*s.sin(pi*h)/pi**2)
check("pulse terminal velocity", velocity)
mass, l2sq = 2*h**2, 2*h**3
loss = mass-pi*endpoint
terminal = endpoint**2/2
check("tracking plus sparsity exact gap", loss+terminal-(2*h**2-2*h*s.sin(pi*h)/pi+2*h**2*s.sin(pi*h)**2/pi**4))
check("first loss leading coefficient", s.limit(loss/h**4,h,0)-pi**2/3)
check("terminal square leading coefficient", s.limit(terminal/h**4,h,0)-2/pi**2)
check("L2 growth quotient vanishes", s.limit((loss+terminal)/l2sq,h,0))
check("normalized Hessian", endpoint**2/l2sq-2*s.sin(pi*h)**2/(pi**4*h))
ndc = loss/l2sq + endpoint**2/(2*l2sq)
check("NDC exact expression", ndc-(1/h-s.sin(pi*h)/(pi*h**2)+s.sin(pi*h)**2/(pi**4*h)))
check("NDC leading coefficient", s.limit(ndc/h,h,0)-(pi**2/6+1/pi**2))
check("NDC vanishes", s.limit(ndc,h,0))

A,d = s.symbols("A d", nonnegative=True)
b=A/pi+d*A**2
composite=A-pi*b+b**2/2
check("local composite expansion", composite-(A**2/(2*pi**2)-pi*d*A**2+d*A**3/pi+d**2*A**4/2))
check("worst admissible remainder coefficient", (A**2/(2*pi**2)-pi*d*A**2).subs(d,1/(4*pi**3))-A**2/(4*pi**2))
x=s.symbols("x", real=True)
check("composite derivative", s.diff(A-pi*x+x*x/2,x)-(x-pi))
eta=s.symbols("eta", positive=True)
check("linear Taylor first order", s.diff(-pi*eta*endpoint+eta**2*endpoint**2/2,eta).subs(eta,0)+pi*endpoint)
check("linear Taylor second order", s.diff(-pi*eta*endpoint+eta**2*endpoint**2/2,eta,2)-endpoint**2)
check("normalized pulse has unit L2 norm", (h/s.sqrt(l2sq))**2*(2*h)-1)

payload={"schema":"pr248-independent-bridge-exact-checks-v1", "sympy":s.__version__,
         "exact_checks":len(checks),"checks":checks,
         "limitations":["Finite identities do not establish the analytic state-space estimates.",
                        "Finite identities do not certify historical priority."]}
target=Path(__file__).with_name("INDEPENDENT_CHECK_RECEIPT.json")
target.write_text(json.dumps(payload,indent=2)+"\n")
print(json.dumps({"exact_checks":len(checks),"receipt":str(target),
                  "sha256":hashlib.sha256(target.read_bytes()).hexdigest()}))
