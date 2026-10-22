"""Fresh controls supporting, never replacing, the analytic reconstruction."""
from pathlib import Path
import json
from datetime import datetime, timezone
from fractions import Fraction as F
import sympy as s
r,k,t=s.symbols('r k t',positive=True)
n=s.symbols('n',integer=True,positive=True)
g=s.exp(s.I*k*r)/(4*s.pi*r)
ci=s.factor(-s.diff(g,r)/r-k*k*g)
ce=s.factor(-s.diff(g,r,2)+s.diff(g,r)/r)
assert s.simplify(ci-s.exp(s.I*k*r)*(1-s.I*k*r-k*k*r*r)/(4*s.pi*r**3))==0
assert s.simplify(ce-s.exp(s.I*k*r)*(k*k*r*r+3*s.I*k*r-3)/(4*s.pi*r**3))==0
assert s.simplify(s.series(ci-1/(4*s.pi*r**3),k,0,4).removeO()+k*k/(8*s.pi*r)+s.I*k**3/(6*s.pi))==0
assert s.simplify(s.series(ce+3/(4*s.pi*r**3),k,0,4).removeO()+k*k/(8*s.pi*r))==0
# Coefficient algebra for every n >= 2, after dividing by i^n/n!.
assert s.simplify(1-n+n*(n-1)-(n-1)**2)==0
assert s.simplify(-n*(n-1)+3*n-3+(n-1)*(n-3))==0
# Exact pair-distance integrals from intersection volume of two unit balls.
overlap=s.pi*(4+r)*(2-r)**2/12
moments={p:s.integrate(4*s.pi*r**(2+p)*overlap,(r,0,2)) for p in [-2,-1,2]}
assert s.simplify(moments[-2]-4*s.pi**2)==0
assert s.simplify(moments[-1]-32*s.pi**2/15)==0
assert s.simplify(moments[2]-32*s.pi**2/15)==0
c2_hs_sq=s.simplify(6*moments[-2]/(64*s.pi**2))
remainder_hs_sq=s.simplify(9*moments[2]/(16*s.pi**2))
quadratic=s.simplify(-s.Rational(1,8)/s.pi*s.Rational(4,3)*moments[-1]/(4*s.pi/3))
assert c2_hs_sq==s.Rational(3,8) and remainder_hs_sq==s.Rational(6,5) and quadratic==-s.Rational(4,15)
# Closed-form monotonic gap, not a finite list of spherical degrees.
a=n/(2*n+1)-s.Rational(1,3)
assert s.factor(a-(n-1)/(3*(2*n+1)))==0
assert s.factor((n+1)/(2*n+3)-n/(2*n+1))==1/((2*n+1)*(2*n+3))
k0=F(1,10000);eps=2*k0*k0;eta=120*k0*k0
assert eps<F(1,60) and eta<F(1,2)
margin=F(2,3)-1446*k0
assert margin==F(7831,15000)>0
trace_bound=-margin*k0**3
# All-n removal series coefficient, after factoring 2^(-3j-12).
assert s.summation(s.Rational(1,8)**n,(n,1,s.oo))==s.Rational(1,7)
result={'utc':datetime.now(timezone.utc).isoformat(),'all_passed':True,
 'symbolic_radial_derivative_and_cubic_terms':True,'all_n_coefficient_algebra':True,
 'ball_pair_distance_moments':{str(p):str(v) for p,v in moments.items()},
 'stronger_C2_HS_squared':str(c2_hs_sq),'stronger_remainder_HS_squared_coefficient':str(remainder_hs_sq),
 'PC2_constant_compression':str(quadratic),'all_degree_monotonic_gap_identity':True,
 'kappa':str(k0),'epsilon_bound':str(eps),'projection_distance_bound':str(eta),
 'graph_norm_bound':str(240*k0*k0),'trace_upper':str(trace_bound),'negative_trace_coefficient':str(-margin),
 'all_n_rational_hole_volume_factor':'1/7',
 'limitation':'These algebraic controls do not prove strong/HS limits, Hodge completeness, Fredholm continuation, source exclusion or priority.'}
(Path(__file__).absolute().parent/'INDEPENDENT_CONTROLS_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
