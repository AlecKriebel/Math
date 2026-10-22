#!/usr/bin/env python3
"""Exact algebra diagnostics. Not a spectral computation or a proof of compactness."""
import json
import platform
from datetime import datetime, timezone
from pathlib import Path
import sympy as s


def require(condition, label):
    if not bool(condition):
        raise RuntimeError(label)
    return {"check": label, "passed": True}

r=s.symbols('r', positive=True)
mu,lam=s.symbols('mu lam', real=True)
d=s.Function('d')(r)
dp=s.diff(d,r)
dpp=s.diff(d,r,2)
raw=r**4*(dpp+4*dp/r-mu*d/r**2)**2-((lam+4)*r**2-1)*(dp**2+mu*d**2/r**2)
reduced=r**4*dpp**2+(2*mu-lam)*r**2*dp**2+dp**2+mu*(mu-lam-2)*d**2+mu*d**2/r**2
boundary=4*r**3*dp**2-2*mu*r**2*d*dp-2*mu*r*d**2
checks=[require(s.simplify(raw-reduced-s.diff(boundary,r))==0,'exact mode defect modulo an explicit total derivative')]
qpart=r**4*dpp**2+dp**2-lam*r**2*dp**2
checks.append(require(s.simplify(reduced-qpart-mu*(2*r**2*dp**2+(mu-2-lam)*d**2+d**2/r**2))==0,'constrained quadratic form plus angular bracket'))
square=2*(r*dp+d/2)**2+(mu-s.Rational(3,2)-lam)*d**2+d**2/r**2
bracket=2*r**2*dp**2+(mu-2-lam)*d**2+d**2/r**2
checks.append(require(s.simplify(bracket-square+s.diff(r*d**2,r))==0,'angular bracket square completion modulo total derivative'))
checks.append(require(s.Rational(9,4)+s.Rational(1,10)+s.Rational(1,50)==s.Rational(237,100),'rational trial upper bound'))
checks.append(require(s.Rational(237,100)<s.Rational(19,8)<s.Rational(12,5)<s.Rational(169,68)<s.Rational(5,2),'exact ordering of all conservative caps'))
checks.append(require(4-s.Rational(3,2)-s.Rational(12,5)==s.Rational(1,10),'first angular mode has a strict one-tenth square-completion margin'))
scale_coeff=s.Rational(9,16)+mu**2-s.Rational(3,2)*mu-lam*(mu+s.Rational(1,4))
checks.append(require(s.solve(scale_coeff.subs(mu,4),lam)==[s.Rational(169,68)],'weaker pure-scale first-mode cap, not an obstruction'))
result={"checked_at_utc":datetime.now(timezone.utc).isoformat(),"python":platform.python_version(),"sympy":s.__version__,"optimization_flag":__import__('sys').flags.optimize,"checks":checks,"status":"PASS","scope":"Exact symbolic and rational algebra only. Compactness, strict constrained gap, source test density, and positive-solution obstruction are analytic arguments in the audit; no numerical eigenvalue is asserted."}
out=Path(__file__).with_name('SPECTRAL_ALGEBRA_DIAGNOSTICS.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
