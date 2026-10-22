#!/usr/bin/env python3
"""Independent exact audit controls; analytic/source checks remain in AUDIT.md.
Requires SymPy. Does not modify the frozen public packet.
"""
from pathlib import Path
from fractions import Fraction
from math import factorial
import hashlib
import json
import platform
import sympy as s

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / 'public'
checks = []
def check(name, condition):
    if not bool(condition):
        raise AssertionError(name)
    checks.append(name)
def zero(name, expression):
    check(name, s.simplify(expression) == 0)

expected_manifest = 'f25cf28a767af988aa7ccfbef005a6c515ddf5a1ddfd0393d25b0c8f393225b7'
expected_proof = 'da2c5ebc59a77683059958c4a736499dffee6bc72c563e1f74595b09beec5f9a'
check('frozen manifest digest', hashlib.sha256((PUBLIC / 'SHA256SUMS.json').read_bytes()).hexdigest() == expected_manifest)
check('frozen proof digest', hashlib.sha256((PUBLIC / 'proof.md').read_bytes()).hexdigest() == expected_proof)
manifest = json.loads((PUBLIC / 'SHA256SUMS.json').read_text())
actual = {p.relative_to(PUBLIC).as_posix() for p in PUBLIC.rglob('*') if p.is_file()}
check('exact frozen file inventory', actual == set(manifest) | {'SHA256SUMS.json'})
for name, record in sorted(manifest.items()):
    data = (PUBLIC / name).read_bytes()
    check('public bytes and digest: ' + name,
          len(data) == record['bytes'] and hashlib.sha256(data).hexdigest() == record['sha256'])

z, w, q, xi, T, t, x, y = s.symbols('z w q xi T t x y')
p = (1-w**2)/(1+2*q*w+w**2)
herglotz = ((1+xi*w)/(1-xi*w)+(1+w/xi)/(1-w/xi))/2
zero('Herglotz averaging identity', p.subs(q,-(xi+1/xi)/2)-herglotz)
zero('endpoint cancellation', p.subs(q,1)-(1-w)/(1+w))
pexpand = s.series(p,w,0,3).removeO()
zero('rational vector-field Taylor expansion', pexpand-(1-2*q*w+(4*q**2-2)*w**2))

# Derive the raw coefficient equations instead of trusting normalized A,B.
v1 = s.exp(-t)
v2 = 2*t*s.exp(-T-t)
v3 = (4*t**2-4*t)*s.exp(-2*T-t)+s.exp(-t)-s.exp(-3*t)
wseries = v1*z+v2*z**2+v3*z**3
rhs = s.expand(-wseries+2*s.exp(t-T)*wseries**2-(4*s.exp(2*t-2*T)-2)*wseries**3)
for n,vn in enumerate((v1,v2,v3),1):
    zero(f'raw ODE coefficient {n}', s.diff(vn,t)-rhs.coeff(z,n))
    zero(f'raw initial coefficient {n}', vn.subs(t,0)-(1 if n == 1 else 0))
terminal = wseries.subs(t,T)
fseries = s.expand(s.exp(T)*(terminal+2*terminal**2+3*terminal**3))
a1 = s.simplify(fseries.coeff(z,1))
a2 = s.simplify(fseries.coeff(z,2))
a3 = s.simplify(fseries.coeff(z,3))
zero('Koebe normalized first coefficient', a1-1)
zero('Koebe second coefficient', a2-2*(T+1)*s.exp(-T))
zero('Koebe third coefficient', a3-(1+(4*T**2+4*T+2)*s.exp(-2*T)))
zero('T=0 Koebe second coefficient', a2.subs(T,0)-2)
zero('T=0 Koebe third coefficient', a3.subs(T,0)-3)
a2half = s.simplify(a2.subs(T,s.Rational(1,2)))
a3half = s.simplify(a3.subs(T,s.Rational(1,2)))
zero('T=1/2 input second coefficient', a2half-3/s.sqrt(s.E))
zero('T=1/2 input third coefficient', a3half-1-5/s.E)
# Independent consistency check: this input saturates FS at lambda=1/3.
zero('input extremal consistency at lambda=1/3', a3half-a2half**2/3-(1+2/s.E))

# Rational-polynomial check with x playing the role of e, no float conversion.
c2 = s.Rational(9,2)/x
c3 = (1+5/x)**2/3
obstruction = s.factor(c3-c2**2/2-(1+2/x**2))
zero('weighted margin factorization', obstruction + 2*(x-s.Rational(7,4))*(x-s.Rational(13,4))/(3*x**2))
zero('Koebe injectivity algebra', s.expand(x*(1-y)**2-y*(1-x)**2)-(x-y)*(1-x*y))
# Mutation checks exercise the required factors and signs as wrong formulae.
check('missing 1/2 coefficient weight is rejected', s.simplify(c3-(9/x)**2/2-(1+2/x**2)-obstruction) != 0)
check('missing 1/3 coefficient weight is rejected', s.simplify((1+5/x)**2-c2**2/2-(1+2/x**2)-obstruction) != 0)
check('margin sign reversal is rejected', s.simplify(obstruction+obstruction) != 0)
check('lost Koebe quadratic term is rejected', s.simplify(s.exp(T)*terminal.coeff(z,2)-a2) != 0)
check('wrong vector field numerator is rejected', s.simplify((1-w)/(1+2*q*w+w**2)-p) != 0)

# New rational enclosure, independent truncation N=14, with an explicit tail.
N = 14
lo = sum((Fraction(1,factorial(n)) for n in range(N+1)),Fraction(0))
hi = lo + Fraction(N+2,(N+1)*factorial(N+1))
check('strict e enclosure and sign brackets', Fraction(7,4) < 2 < lo < hi < 3 < Fraction(13,4))
dlo = Fraction(2,3)*(lo-Fraction(7,4))*(Fraction(13,4)-hi)/(hi*hi)
dhi = Fraction(2,3)*(hi-Fraction(7,4))*(Fraction(13,4)-lo)/(lo*lo)
check('strict independent positive margin', 0 < dlo < dhi)
check('margin exceeds 0.04645', dlo > Fraction(4645,100000))
check('margin below 0.04646', dhi < Fraction(4646,100000))

replay = json.loads((ROOT/'audit/author_controls_replay.json').read_text())
stored = json.loads((PUBLIC/'controls/verification_results.json').read_text())
check('author replay matches frozen result', replay == stored)
check('author assertion accounting', replay['exact_and_sample_assertions']==114 and len(replay['checks'])==114)
check('17 nonfloating plus 97 supplementary checks', sum(n.startswith('flow radius sample ') or n.startswith('conjugation sample ') or n=='sample mesh agreement' for n in replay['checks'])==97)

result = {
 'problem_id':2306044,
 'passed':True,
 'independent_checks':len(checks),
 'checks':checks,
 'input_hashes':{'manifest':expected_manifest,'proof':expected_proof},
 'e_enclosure':{'lower':str(lo),'upper':str(hi),'truncation':N},
 'margin_enclosure':{'lower':str(dlo),'upper':str(dhi)},
 'margin_decimal_illustration':[float(dlo),float(dhi)],
 'author_controls':{'passed':True,'total':114,'nonfloating':17,'supplementary_floating':97,'identical_replay':True},
 'versions':{'python':platform.python_version(),'sympy':s.__version__},
 'limits':['Symbolic identities and interval checks are not a formal verification of the analytic flow or Fekete-Szego theorem.','The source and analytic audit is in AUDIT.md.','Bshouty original full text remains unread.','No external or remote state was changed.']
}
print(json.dumps(result,indent=2))
