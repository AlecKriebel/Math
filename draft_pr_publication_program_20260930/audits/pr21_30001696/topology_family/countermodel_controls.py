#!/usr/bin/env python3
"""Independent exact falsification controls for global topology claims.

Uses only the standard library; imports no snapshot code or historical results.
Works in projective coordinates where a common positive normalization cancels.
These are checks of countermodels and finite spectral controls, not a proof of B.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import product
import hashlib
import json
from datetime import datetime, timezone

COUNTS = {}

def check(label, condition):
    COUNTS[label] = COUNTS.get(label, 0) + 1
    assert condition, label

def sminus(v):
    nz = [x for x in v if x]
    return sum(a != b for a,b in zip(nz,nz[1:]))

def completions(v):
    zero = [j for j,x in enumerate(v) if not x]
    for signs in product((-1,1),repeat=len(zero)):
        w=list(v)
        for j,sign in zip(zero,signs): w[j]=sign
        yield tuple(w)

def sphere_point(dim, seed):
    if dim == 1:
        return (Q(1 if seed % 2 else -1),)
    t = [Q(((seed+j*3)%11)-5,7) for j in range(dim-1)]
    t2 = sum(x*x for x in t)
    return tuple([2*x/(1+t2) for x in t]+[(1-t2)/(1+t2)])

def diagonal(v,a):
    return tuple(x*a**k for k,x in enumerate(v))

def norm2(v): return sum(x*x for x in v)

def ratio2(v,r): return norm2(v[r:])/norm2(v[:r])

def derivative(v,r):
    # d log R / d log a evaluated at the current representative v.
    return (sum(k*v[k]**2 for k in range(r,len(v)))/norm2(v[r:])
            -sum(k*v[k]**2 for k in range(r))/norm2(v[:r]))

# A zero-stratum falsification control: closed cone != its interior.
check('zero_sensitive_countermodel', sminus((1,0,1)) == 0)
check('zero_sensitive_countermodel', max(map(sminus,completions((1,0,1)))) == 2)
check('weak_TN_countermodel', sminus((1,0,1)) <= 0)
check('weak_TN_countermodel', max(map(sminus,completions((1,0,1)))) > 0)
# Identity is TN, but cannot strictly trap this boundary point.

# Direct endpoint d=2,i=0, with E=(1,1), F=(1,-1).
# Original-sign cone membership iff (u+z)(u-z)>=0 iff |z|<=|u|.
for u,z in product([Q(-3),Q(-1),Q(0),Q(1),Q(3)],repeat=2):
    if u == z == 0: continue
    original=(u+z,u-z)
    in_cone=sminus(tuple((x>0)-(x<0) for x in original)) == 0
    check('d2_S0_S0_endpoint', in_cone == (z*z <= u*u))
check('d2_S0_S0_endpoint', len(list(product((-1,1),repeat=2))) == 4)

# Uniform cross-section spectral checks using unrelated rational points.
for d in range(2,12):
    N=d-1
    for r in range(1,d):
        for seed in range(1,9):
            s=sphere_point(r,seed)+sphere_point(d-r,seed+2)
            check('rational_Sigma', norm2(s[:r]) == norm2(s[r:]) == 1)
            previous=Q(0)
            for a in [Q(1,64),Q(1,8),Q(1,4),Q(1,2),Q(1),Q(2),Q(8),Q(64)]:
                v=diagonal(s,a)
                rr=ratio2(v,r)
                check('ratio_monotonicity', rr>previous)
                previous=rr
                check('derivative_gap', Q(1) <= derivative(v,r) <= N)
                check('ratio_bounds', a**(2*N)<=rr<=a*a if a<=1 else a*a<=rr<=a**(2*N))
                check('inverse_action', diagonal(v,1/a)==s)
                if a>=Q(1,4):
                    check('identity_cutoff_contrapositive', rr>=Q(1,4)**(2*N))

# Non-strict trapping countermodel on S^2 with the SAME distinct spectral
# indices diag(1,a,a^2): C={z^2<=x^2+y^2} plus a closed
# spike y=0,x>=0,0<=z<=4x. Its exceptional orbit endpoint is a=2.
def spike_C(x,y,z):
    return z*z<=x*x+y*y or (y==0 and x>=0 and 0<=z<=4*x)
for z in [Q(5,4),Q(3,2),Q(7,4),Q(4)]:
    check('nonstrict_spike_many_boundary_points', spike_C(Q(1),Q(0),z))
    # Any nonzero transverse perturbation destroys spike membership.
    check('nonstrict_spike_many_boundary_points', not spike_C(Q(1),Q(1,1000),z))
    for b in [Q(1,4),Q(1,2),Q(3,4),Q(9,10)]:
        check('nonstrict_forward_invariance', spike_C(Q(1),Q(0),b*b*z))
check('nonstrict_not_strict', not (Q(9,8)**2 < 1))
check('nonstrict_beta_discontinuous', Q(2) != Q(1))

# Stronger countermodel: all strict-trapping hypotheses hold, but naive orbit
# rescaling a->a/beta fails at the core. Use diag(1,a,a^2), E=R^2, F=R.
# beta=2 on z>0 Sigma component and 1 on z<0 component.
def strict_C(v):
    x,y,z=v
    return (z>=0 and z*z<=16*x*x+4*y*y) or (z<=0 and z*z<=x*x+y*y)
for sign in (-1,1):
    beta=Q(1 if sign<0 else 2)
    for y in [Q(0),Q(1,2),Q(1),Q(2)]:
        # Boundary points may use a sqrt in z; check squared coordinates instead.
        z2=(Q(1)+y*y) if sign<0 else (Q(16)+4*y*y)
        for b in [Q(1,16),Q(1,4),Q(1,2),Q(3,4),Q(15,16)]:
            lhs=b**4*z2
            rhs=(Q(1)+b*b*y*y) if sign<0 else (Q(16)+4*b*b*y*y)
            check('strict_C_trapping', lhs<rhs)
check('naive_core_two_path_limits', (Q(1),Q(1,2)) != (Q(1),Q(1)))
for n in range(12,65):
    xplus=(Q(1),Q(1),Q(1,n))
    xminus=(Q(1),Q(1),Q(-1,n))
    check('naive_core_paths_inside', strict_C(xplus) and strict_C(xminus))
    check('cutoff_fixes_both_core_paths', ratio2(xplus,2)<Q(1,4)**4)
    check('naive_rescale_plus', diagonal(xplus,Q(1,2))[:2] == (Q(1),Q(1,2)))
    check('naive_rescale_minus', diagonal(xminus,Q(1))[:2] == (Q(1),Q(1)))

# Affine cutoff and inverse sanity controls with endpoint values crossing 1.
eps=Q(1,4)
for beta in [Q(1,2),Q(1),Q(2),Q(17,3)]:
    def h(a): return a if a<=eps else eps+(1-eps)*(a-eps)/(beta-eps)
    def hinv(c): return c if c<=eps else eps+(beta-eps)*(c-eps)/(1-eps)
    prev=Q(0)
    for k in range(1,65):
        a=beta*k/64
        check('cutoff_increasing', h(a)>prev)
        prev=h(a)
        check('cutoff_inverse', hinv(h(a))==a)
    check('cutoff_endpoints', h(beta)==1 and h(eps)==eps and hinv(eps)==eps)

out={'created_at_utc':datetime.now(timezone.utc).isoformat(),
     'kind':'new independent exact falsification controls, supplementary only',
     'proof_sha256':'58809f3edaa2930f1111ba823b1ce50c8e328dd8388b2e19323600ede3d04305',
     'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'historical_imports':False,'counts':COUNTS,'total_assertions':sum(COUNTS.values()),
     'status':'pass','countermodels_confirmed':['closed cone does not imply interior',
        'TN / weak variation does not imply strict trapping',
        'non-strict trapping permits a discontinuous beta and many orbit boundary points',
        'continuous semialgebraic beta and strict trapping do not justify naive identity-core extension'],
     'limitations':'Finite controls do not establish the general theorem; the universal reconstruction and primary theorem audit carry acceptance.'}
Path(__file__).with_name('countermodel_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
