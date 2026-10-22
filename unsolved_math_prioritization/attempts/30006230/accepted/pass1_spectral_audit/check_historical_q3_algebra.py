#!/usr/bin/env python3
"""Exact algebra diagnostics for the historical n=1 candidate; analytic audit is separate."""
import json, platform, sys
from datetime import datetime,timezone
from pathlib import Path
import sympy as S

def require(ok,label):
    if not bool(ok): raise RuntimeError(label)
    return {'check':label,'passed':True}

r=S.symbols('r',positive=True)
z=S.symbols('z',real=True)
a,lam,m=S.symbols('a lam m',real=True)
s=S.Rational(3,4)
d=S.Function('d')(r); dp=S.diff(d,r); dpp=S.diff(d,r,2)
raw=r**(s+2)*(dpp+2*dp/r-a*d/r**2)**2-(lam*r**s+2*(1-s)*r**(s-2))*(r**2*dp**2+a*d**2)
reduced=r**(s+2)*(dpp**2-lam*dp**2)+a*(2*r**s*dp**2+(a-S.Rational(13,16))*r**(s-2)*d**2-lam*r**s*d**2)
boundary=2*r**(s+1)*dp**2-2*a*r**s*d*dp+a*(s-2)*r**(s-1)*d**2
checks=[require(S.simplify(raw-reduced-S.diff(boundary,r))==0,'Q3 mode identity modulo exact total derivative')]
y=S.Function('y')(r); transformed=2*r**s*S.diff(r**(-s/2)*y,r)**2+(a-S.Rational(13,16))*r**(s-2)*(r**(-s/2)*y)**2
positive=2*S.diff(y,r)**2+(a-S.Rational(41,32))*y**2/r**2
checks.append(require(S.simplify(transformed-positive+s*S.diff(y**2/r,r))==0,'elementary Dirichlet-Poincare transformation'))
checks.append(require(2-S.Rational(41,32)==S.Rational(23,32),'first nonradial inverse-square potential is positive'))
g=S.Function('g')(z)
def L(f):return (1-z*z)*S.diff(f,z,2)-S.Rational(3,2)*z*S.diff(f,z)
h=(1-z*z)**S.Rational(1,4)
odd=(1-z*z)*S.diff(g,z,2)-S.Rational(5,2)*z*S.diff(g,z)-g/2
checks.append(require(S.simplify(L(h*g)-h*odd)==0,'odd-sheet conjugated angular differential operator'))
checks.append(require(S.expand(4*m*(m+S.Rational(1,2))-(2*m)*(2*m+1))==0,'even eigenvalue k(k+1)'))
checks.append(require(S.expand(4*(m*(m+S.Rational(3,2))+S.Rational(1,2))-(2*m+1)*(2*m+2))==0,'odd eigenvalue k(k+1)'))
trial=1-r*r;p=r**S.Rational(11,4)
E=S.integrate(p*S.diff(trial,r)**2,(r,0,1));N=S.integrate(p*trial**2,(r,0,1))
checks.append(require(S.simplify(E/N)==S.Rational(465,32),'exact trial Rayleigh quotient 465/32'))
checks.append(require(S.Rational(465,32)<16,'strict admissible trial cap'))
checks.append(require(S.integrate(r*r/p,(r,0,1))==4,'ordinary-mean energy continuity constant squared'))
checks.append(require(-2+4*s-s*s==S.Rational(7,16),'historical source side-condition coefficient'))
result={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),'sympy':S.__version__,'optimization_flag':sys.flags.optimize,'checks':checks,'status':'PASS','scope':'Symbolic and rational identities only. Completeness, compactness, strict gap, full-test convergence, and nonexistence of a positive solution are established analytically in HISTORICAL_Q3_SPECTRAL_AUDIT.md.'}
Path(__file__).with_name('HISTORICAL_Q3_DIAGNOSTICS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
