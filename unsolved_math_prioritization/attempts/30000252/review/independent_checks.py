#!/usr/bin/env python3
"""Independent symbolic application checks, not a PDE existence computation."""
import sympy as s
from collections import Counter
from pathlib import Path
import hashlib,json

checks=Counter()
def check(ok,name):
    assert bool(ok),name
    checks[name]+=1

n,m=s.symbols('n m',positive=True)
p=(n+2*m)/(n-2*m)
q=2*n/(n-2*m)
a=(n-2*m)/(4*m)
check(s.simplify(q-p-1)==0,'critical_power_conversion')
check(s.simplify(a*(p-1)-1)==0,'inverse_scaling_exponent')
check(s.simplify(a+1-a*p)==0,'nonlinear_coefficient_normalization')
check(s.simplify(a+1-(n+2*m)/(4*m))==0,'forcing_exponent')
check(s.simplify((p-1)/p-4*m/(n+2*m))==0,'smallness_threshold_exponent')
check(p.subs({m:3,n:7})==13,'odd_order_example_power')
check(q.subs({m:3,n:7})==14,'Sobolev_exponent_example')
check(a.subs({m:3,n:7})==s.Rational(1,12),'example_rescaling')

# Remove fractional powers entirely by setting lambda=t^12 and v=t*u.
t,u=s.symbols('t u',positive=True)
check(s.expand(t**13*(1+u**13)-(t**13+(t*u)**13))==0,
      'polynomial_scaling_forward')
check(s.expand((t**13+u**13)/t-t**12*(1+(u/t)**13))==0,
      'polynomial_scaling_backward')
check((-1)**3==-1,'literal_and_standard_odd_operators')

x=s.symbols('x0:7',real=True)
xi=s.Matrix([-v for v in x]);D=xi.jacobian(x)
check(D+D.T==-2*s.eye(7),'conformal_field')
check(s.trace(D)==-7,'strict_negative_divergence')
h=s.symbols('h',positive=True)
check(s.simplify(sum((s.exp(-h)*v)**2 for v in x)
                 -s.exp(-2*h)*sum(v*v for v in x))==0,'contracting_flow_norm')

# Boundary-data diagnostic: (1-|x|^2)^3 has zero full jet through order two
# on the unit sphere, but it does not satisfy the third Navier condition.
radius2=sum(v*v for v in x);test=(1-radius2)**3
check(s.factor(test).has((radius2-1)**3) or s.expand(test+(radius2-1)**3)==0,
      'test_function_zero_trace')
for v in x:
    derivative=s.diff(test,v)
    check(s.rem(derivative,s.Poly(1-radius2,x[-1]).as_expr(),x[-1])==0,
          'zero_first_boundary_jet')
for i in range(7):
    for j in range(i,7):
        derivative=s.diff(test,x[i],x[j])
        check(s.rem(derivative,s.Poly(1-radius2,x[-1]).as_expr(),x[-1])==0,
              'zero_second_boundary_jet')
z=s.symbols('z',real=True)
radial_lap=lambda f:s.expand(4*z*s.diff(f,z,2)+14*s.diff(f,z))
v=(1-z)**3
check(radial_lap(v).subs(z,1)==0,'first_Navier_trace_diagnostic')
check(radial_lap(radial_lap(v)).subs(z,1)==-864,'Dirichlet_not_Navier_diagnostic')

here=Path(__file__).resolve().parent
digest=hashlib.sha256((here/'author_replay/KNOWN_RESULT.md').read_bytes()).hexdigest()
check(digest=='401cf0b937e23c22f8da09a4b26890cdd64f1a27aae7a3cadffebbcb123ef888','frozen_artifact_hash')
print(json.dumps({'status':'PASS','exact_assertions':sum(checks.values()),
 'checks':dict(sorted(checks.items())),'artifact_sha256':digest,
 'limitation':'Symbolic scaling, geometry and boundary-data controls only. The published analytic multiplicity and regularity theorem is used as an input, not reconstructed or numerically certified.'},indent=2,sort_keys=True))
