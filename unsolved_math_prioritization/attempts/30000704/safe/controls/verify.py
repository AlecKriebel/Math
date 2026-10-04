#!/usr/bin/env python3
"""Exact symbolic controls only; not an analytic/topological proof checker."""
import json
import sys
import sympy as s

r, a, b, R, m, ell, K = s.symbols('r a b R m ell K', positive=True)
def radial_laplacian(expr):
    return s.diff(expr, r, 2) + s.diff(expr, r)/r

def zero(expr):
    return s.factor(expr) == 0 or s.simplify(s.powsimp(s.together(expr), force=True)) == 0 or s.simplify(s.expand_power_base(expr, force=True)) == 0

checks = []
def check(name, passed, kind='exact_identity'):
    checks.append({'name': name, 'passed': bool(passed), 'kind': kind})
    if not passed:
        raise AssertionError(name)

cone = a*r**(a-1)/(1-r**(2*a))
u_cone_prime = (a-1)/r + 2*a*r**(2*a-1)/(1-r**(2*a))
delta_cone = s.diff(r*u_cone_prime,r)/r
check('cone logarithmic derivative', zero(s.diff(cone,r)/cone-u_cone_prime))
check('cone Gauss curvature is minus four', zero(delta_cone-4*cone**2))
check('cone radial length primitive', zero(s.diff(s.atanh(r**a),r)-cone))
check('flat power curvature vanishes', zero(radial_laplacian(-b*s.log(r))))
check('flat power length primitive', zero(s.diff(r**(1-b)/(1-b),r)-r**(-b)))

singleton = a*2**(-a)*r**(a-1)/(1-2**(-2*a)*r**(2*a))
check('singleton radial length primitive',
      zero(s.diff(s.atanh((r/2)**a),r)-singleton))
check('singleton radial curvature is minus four',
      zero((s.diff(r*s.diff(singleton,r)/singleton,r)/r)-4*singleton**2))

cusp = 1/(2*r*s.log(R/r))
u_cusp_prime = -1/r + 1/(r*s.log(R/r))
check('punctured disk metric curvature is minus four',
      zero(s.diff(r*u_cusp_prime,r)/r-4*cusp**2))
check('log-log barrier differential',
      zero(s.diff(s.log(s.log(R/r)),r)+1/(r*s.log(R/r))))
check('circular cutoff Laplacian',
      zero(radial_laplacian(-s.log(R**2-r**2))-4*R**2/(R**2-r**2)**2))

# The two factors on the right are nonnegative under 0<r<R and ell>=m.
d = R**2-r**2
Kcut = 4*R**4+4*R**2/m**2
rho_sq = ell**2/d**2
residual = Kcut*rho_sq-4*ell**2-4*R**2/d**2
certificate = 4*(ell**2*r**2*(2*R**2-r**2)
                 + R**2*(ell**2/m**2-1))/d**2
check('cutoff curvature inequality exact nonnegative-factor certificate',
      zero(residual-certificate))
check('curvature normalization scaling', zero(K/(s.sqrt(K)/2)**2-4))
check('local barrier coefficient at r=R/2',
      zero((R**2-r**2).subs(r,R/2)-3*R**2/4))

wrong = (1-r**2)**(-a)
wrong_curvature = -radial_laplacian(-a*s.log(1-r**2))/wrong**2
check('subcritical disk power has unbounded negative curvature',
      zero(wrong_curvature+4*a*(1-r**2)**(2*a-2)))

# Negative controls: these mutations must fail, not pass.
check('reversed cone curvature sign is rejected',
      not zero(delta_cone+4*cone**2), 'negative_control')
check('reversed normalization factor is rejected',
      not zero(K/(2/s.sqrt(K))**2-4), 'negative_control')
check('missing factor two in punctured metric is rejected',
      not zero(s.diff(r*u_cusp_prime,r)/r-4*(2*cusp)**2), 'negative_control')

# Exact checks for a=1/2 at rational square radii supplement the symbolic ones.
from fractions import Fraction as F
for t in [F(1,10),F(1,4),F(1,2),F(3,4),F(9,10)]:
    rr=t*t
    density=1/(2*t*(1-rr))
    delta=1/(rr*(1-rr)**2)
    check('rational cone control t='+str(t), delta==4*density*density,
          'exact_rational')

out = {'problem_id':30000704, 'status':'PASS', 'sympy_version':s.__version__,
       'checks':checks, 'count':len(checks),
       'limits':['Symbolic identities do not prove boundary topology or kernel convergence.',
                 'No numerical experiment is used as proof.',
                 'The disk local-completeness theorem remains an explicit literature dependency.',
                 'The full minimum-regularity problem remains unresolved.']}
print(json.dumps(out,indent=2,sort_keys=True))
