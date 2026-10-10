#!/usr/bin/env python3
"""Independent finite rational controls; they do not certify analytic statements."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
GROUPS = {}

def check(group, condition):
    assert condition, group
    GROUPS[group] = GROUPS.get(group, 0) + 1

def add(z,w): return z[0]+w[0],z[1]+w[1]
def neg(z): return -z[0],-z[1]
def sub(z,w): return add(z,neg(w))
def mul(z,w): return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]
def norm(z): return z[0]*z[0]+z[1]*z[1]
def reflect(z): return -z[0],z[1]
def div(z,w):
    den=norm(w)
    assert den>0
    return (z[0]*w[0]+z[1]*w[1])/den,(z[1]*w[0]-z[0]*w[1])/den

def poisson(w,xi): return (1-norm(w))/norm(sub(xi,w))

# All points use exact fractions; repeat input values are removed.
xis=sorted(set([(-Q(1),Q(0))]+[((1-t*t)/(1+t*t),2*t/(1+t*t)) for t in (Q(j,7) for j in range(-21,22))]))
ws=[(Q(j,9),Q(k,9)) for j in range(-8,9) for k in range(-8,9) if j*j+k*k<81]
eta=(Q(3,5),Q(4,5))
for xi in xis:
    check('unit_circle_parameterization', norm(xi)==1)
    for w in ws:
        p=poisson(w,xi)
        check('poisson_positive_inside', p>0)
        check('two_sheet_poisson_composition',
              poisson(mul(w,w),mul(xi,xi))==(p+poisson(w,neg(xi)))/2)
        check('reflection_covariance',poisson(reflect(w),reflect(xi))==p)
        check('rotation_covariance',poisson(mul(eta,w),mul(eta,xi))==p)
        if w[0]>0 and xi[0]>0:
            check('slit_reflection_denominator_gap',
                  norm(sub(reflect(xi),w))-norm(sub(xi,w))==4*w[0]*xi[0]>0)
            check('slit_kernel_strict_positivity',p-poisson(w,reflect(xi))>0)

# Möbius formula behind Re arctan w: its argument lies between 0 and pi/2
# in the right half disk; boundary checks exclude the two corner points.
one=(Q(1),Q(0)); imag=(Q(0),Q(1))
for w in ws:
    if w[0]<=0: continue
    iw=mul(imag,w)
    t=div(add(one,iw),sub(one,iw))
    d=(1+w[1])**2+w[0]**2
    check('arctan_mobius_interior_real', t[0]==(1-norm(w))/d>0)
    check('arctan_mobius_interior_imaginary',t[1]==2*w[0]/d>0)
for w in xis:
    if w[0]<=0: continue
    t=div(add(one,mul(imag,w)),sub(one,mul(imag,w)))
    check('arctan_semicircle_boundary_argument',t[0]==0 and t[1]>0)
for j in range(-20,21):
    y=Q(j,21); w=(Q(0),y)
    t=div(add(one,mul(imag,w)),sub(one,mul(imag,w)))
    check('arctan_diameter_boundary_argument',t==((1-y)/(1+y),Q(0)) and t[0]>0)
    check('slit_normal_derivative_sign',1/(1-y*y)>0)

# Independent dipole rotation check, including preservation of the zero center.
for j in range(1,100):
    r=Q(j,100)
    positive=mul((r,Q(0)),eta); negative=neg(positive)
    check('dipole_rotated_positive_axis',poisson(positive,eta)-poisson(positive,neg(eta))==4*r/(1-r*r)>0)
    check('dipole_rotated_negative_axis',poisson(negative,eta)-poisson(negative,neg(eta))==-4*r/(1-r*r)<0)
check('dipole_zero_center',poisson((Q(0),Q(0)),eta)-poisson((Q(0),Q(0)),neg(eta))==0)

# Deliberately incorrect candidate formulas must be detected by these witnesses.
w=(Q(0),Q(0)); xi=(Q(1),Q(0))
check('negative_control_missing_composition_half',poisson(mul(w,w),mul(xi,xi)) != poisson(w,xi)+poisson(w,neg(xi)))
w=(Q(1,10),-Q(4,5)); xi=(Q(3,5),Q(4,5))
check('negative_control_antipode_not_reflection',poisson(w,xi)-poisson(w,neg(xi))<0)
r=Q(1,2)
check('negative_control_reversed_dipole', (1-r*r)/(1+r)**2-(1-r*r)/(1-r)**2 != 4*r/(1-r*r))

a=Q(3,4)
def q(r):return (r*r-a*a)/(1-a*a)
for r in (Q(1,4),Q(1,2),Q(3,4)):
    check('finite_sampling_explicit_witness_samples',q(r)<=0)
check('finite_sampling_explicit_witness_missed',q(Q(7,8))==Q(13,28)>0)
check('finite_sampling_explicit_witness_boundary',q(Q(1))==1)
check('finite_sampling_explicit_witness_laplacian',4/(1-a*a)==Q(64,7)>0)

out={
    'schema':'independent-rational-audit-controls-v1',
    'problem_id':2303014,
    'status':'PASS',
    'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'exact_checks':sum(GROUPS.values()),
    'groups':{k:{'checks':v,'status':'PASS','arithmetic':'exact rational'} for k,v in GROUPS.items()},
    'grid':{'distinct_unit_circle_points':len(xis),'distinct_interior_points':len(ws)},
    'limits':['Finite rational identity and sign checks only.','No numerical certification of arbitrary L1 traces, subharmonicity, optional stopping, or the projection theorem.','Negative controls reject specified wrong algebra; passing does not establish the infinite-dimensional extremal claim.','The separate reconstructed checker replay is not included in this independent check count.']
}
(HERE/'AUDIT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
