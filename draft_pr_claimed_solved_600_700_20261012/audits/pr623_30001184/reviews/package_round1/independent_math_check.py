#!/usr/bin/env python3
"""Independent symbolic diagnostics; continuum claims remain analytic proofs."""
from pathlib import Path
import json
import sympy as s

checks = []


def verify(condition, name):
    if not condition:
        raise ValueError(name)
    checks.append(name)


r = s.symbols('r', positive=True)
x = s.symbols('x', positive=True)
q = s.diag(1, 0)
Q = s.Matrix([[(1+r)/2, s.sqrt(1-r*r)/2], [s.sqrt(1-r*r)/2, (1-r)/2]])
verify(s.simplify(Q*Q-Q) == s.zeros(2), 'symbolic evaluated projection')
verify(s.simplify(q*Q*q-(1+r)*q/2) == s.zeros(2), 'all-time initial kernel equality')
double_angle = r**3 + s.sqrt(1-r*r)*s.sqrt(1-r**4)
factorized = r**3 + (1-r*r)*s.sqrt(1+r*r)
# The radical equality uses 0<r<1, recorded explicitly rather than a blind simplify.
verify(s.expand((1-r*r)*(1-r**4) - ((1-r*r)*s.sqrt(1+r*r))**2) == 0,
       'radical magnitudes equal with both signs positive for 0<r<1')
d = (1-r*r)*(s.sqrt(1+r*r)-r)/2
verify(s.simplify((factorized-r)/2-d) == 0, 'witness factorization')
verify(s.simplify(d - (1-r*r)/(2*(s.sqrt(1+r*r)+r))) == 0, 'positive rationalized coefficient')
verify(s.simplify(d.subs(r,s.Rational(1,2))-3*(s.sqrt(5)-1)/16) == 0, 'exact log-two witness')
verify(s.limit(d,r,1,dir='-') == 0, 'zero-time limiting coefficient')
verify(s.limit(d,r,0,dir='+') == s.Rational(1,2), 'infinite-time limiting coefficient')
verify(s.limit(d/(1-r),r,1,dir='-') == s.sqrt(2)-1, 'zero-time first-order scale')
g = s.acos(s.exp(-x))/2
verify(s.simplify(s.diff(g,x)-1/(2*s.sqrt(s.exp(2*x)-1))) == 0, 'positive-side angle derivative')
verify(s.simplify(s.diff(1/(2*s.sqrt(s.exp(2*x)-1)),x)+s.exp(2*x)/(2*(s.exp(2*x)-1)**s.Rational(3,2))) == 0,
       'strictly decreasing positive-side derivative')
J = s.ones(2)/2
K = s.eye(2)-J
u,v = s.symbols('u v')
verify(s.expand((J+u*K)*(J+v*K) - (J+u*v*K)) == s.zeros(2), 'parametric Markov semigroup identity')
U = s.eye(4)
c,z = s.symbols('c z', real=True)
U[1,1] = U[2,2] = c
U[1,2] = U[2,1] = -s.I*z
verify((U.conjugate().T*s.kronecker_product(s.eye(2),q)*U)[2:4,2:4] == c*c*q,
       'literal BFH finite-bath decaying projection compression')
Lq = s.diag(-s.Rational(1,2),s.Rational(1,2))
verify(q*Lq*q == -q/2 and q*(-q)*q == -q,
       'both compressed generators violate derivation projection corner identity')
out = {'result':'PASS', 'independent_symbolic_checks':len(checks), 'checks':checks,
       'coefficient_positive_for_all_positive_times':'0<r<1; 1-r^2>0 and sqrt(1+r^2)>r',
       'continuous_quantifiers':'proved analytically in INDEPENDENT_DEDUCTIONS.md, not inferred from diagnostics',
       'sympy_version':s.__version__}
Path(__file__).with_name('INDEPENDENT_MATH_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
