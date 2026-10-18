#!/usr/bin/env python3
"""Independent read-only controls for the frozen GPZ applicability candidate.
The projective-line reference evaluator below does not use the author's reduction.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import importlib.util
import hashlib
import itertools
import json
import random
import time
import sympy as s

ROOT = Path(__file__).resolve().parent.parent / 'author'
OUT = Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location('candidate', ROOT / 'orbitwise_evaluator.py')
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)
checks=[]

def check(name,actual,expected,category):
    ok=s.cancel(actual-expected)==0
    checks.append({'name':name,'category':category,'actual':str(actual),'expected':str(expected),'passed':bool(ok)})
    if not ok:
        raise AssertionError(checks[-1])

def check_true(name,value,category):
    checks.append({'name':name,'category':category,'passed':bool(value)})
    if not value:
        raise AssertionError(checks[-1])

def projective_reference(P, bs, Q, xy):
    """E_Q of a homogeneous degree-zero fraction in dimension two.

    Dehomogenize at y=1. Univariate rational division and derivative-defined
    partial-fraction coefficients reduce to x^k/y^k and y^k/(x-r*y)^k.
    For one pole L_u, E_Q(L_v^k/L_u^k)=(Q(v,u)/Q(u,u))^k.
    This route has no dependence-elimination or numerator-cancellation tree.
    """
    x,y=xy
    t=s.Symbol('projective_t')
    assert s.Poly(P,x,y).total_degree()==len(bs) or P==0
    R=s.cancel(P.subs({x:t,y:1})/s.prod(b[0]*t+b[1] for b in bs))
    num,den=s.fraction(R)
    poly=s.div(num,den,t)[0]
    result=poly.subs(t,Q[0,1]/Q[1,1])
    multiplicities={}
    for b in bs:
        if b[0]:
            r=-s.Rational(b[1],b[0])
            multiplicities[r]=multiplicities.get(r,0)+1
    reconstruction=poly
    for r,m in multiplicities.items():
        regular=s.cancel((t-r)**m*R)
        alpha=(Q[0,1]-r*Q[1,1])/(Q[0,0]-2*r*Q[0,1]+r*r*Q[1,1])
        for k in range(1,m+1):
            coefficient=s.diff(regular,t,m-k).subs(t,r)/s.factorial(m-k)
            result += coefficient*alpha**k
            reconstruction += coefficient/(t-r)**k
    assert s.cancel(reconstruction-R)==0
    return s.factor(result)

start=time.monotonic()
manifest=json.loads((ROOT/'PUBLIC_AUTHOR_MANIFEST.json').read_text())
check_true('public_author_subset_manifest_sha256',hashlib.sha256((ROOT/'PUBLIC_AUTHOR_MANIFEST.json').read_bytes()).hexdigest()=='de82bc21d4e00203fa2c7c89048f7190b3540739dacd0b09feedcef779d443ad','integrity')
for rel,data in manifest['files'].items():
    raw=(ROOT/rel).read_bytes()
    check_true('source_integrity_'+rel,len(raw)==data['bytes'] and hashlib.sha256(raw).hexdigest()==data['sha256'],'integrity')
author=json.loads((OUT/'AUTHOR_TEST_RERUN.json').read_text())
check_true('author_rerun_equals_frozen_tests',author==json.loads((ROOT/'AUTHOR_TESTS.json').read_text()),'author_reproduction')

rng=random.Random(30001568)
matrices=[s.eye(2),s.Matrix([[2,1],[1,2]]),s.Matrix([[5,-2],[-2,3]]),s.Matrix([[s.Rational(3,2),s.Rational(1,3)],[s.Rational(1,3),s.Rational(4,3)]])]
cases=[[(1,0)],[(0,-3),(0,2)],[(1,0),(0,1)],[(1,0),(0,1),(1,1)],[(1,0),(1,0),(0,1),(1,1)],[(1,2),(-2,-4),(0,3),(2,-1)],[(1,0),(0,1),(1,1),(1,-1),(2,1)],[(1,2),(2,-1),(3,1),(1,2),(0,1)]]
for qi,Q in enumerate(matrices):
    E=candidate.Evaluator(2,Q)
    x,y=E.x
    for ci,bs in enumerate(cases):
        m=len(bs)
        P=sum(rng.randint(-5,5)*x**j*y**(m-j) for j in range(m+1))
        expected=projective_reference(P,bs,Q,E.x)
        check(f'projective_Q{qi}_case{ci}',E.degree_zero(P,bs),expected,'independent_projective_reference')
        check(f'permuted_Q{qi}_case{ci}',E.degree_zero(P,list(reversed(bs))),expected,'denominator_order')

# Rank-deficient dependent poles in 3D, with a transverse numerator direction.
Q3=s.Matrix([[4,1,1],[1,3,-1],[1,-1,3]])
E3=candidate.Evaluator(3,Q3)
x,y,z=E3.x
v=s.Matrix([1,2,-1]);u=s.Matrix([2,-1,3]);alpha=(v.T*Q3*u)[0]/(u.T*Q3*u)[0]
check('rank_one_3d_high_multiplicity',E3.degree_zero(E3.linear(v)**5,[list(u)]*5),alpha**5,'rank_deficient')
w=(s.Matrix.hstack(s.Matrix([1,0,0]),s.Matrix([0,1,0])).T*Q3).nullspace()[0]
bs3=[[1,0,0],[0,1,0],[1,1,0],[1,0,0]]
check('transverse_polar_numerator_3d',E3.degree_zero(E3.linear(w)**4,bs3),0,'rank_deficient')
check('dependent_polynomial_cancellation_3d',E3.degree_zero(s.prod(E3.linear(b) for b in bs3),bs3),1,'rank_deficient')

# Full binomial identities cancel to finite Laurent polynomials, including
# linearly dependent, repeated, opposite, and scaled pole vectors.
for i,(bs,Ns,center) in enumerate([
    ([(1,0),(0,1),(1,1)], [2,3,2], [s.Rational(2,3),s.Rational(-3,5)]),
    ([(1,2),(1,2),(-2,-4),(0,1)], [2,1,2,3], [s.Rational(7,3),s.Rational(1,4)]),
]):
    E=candidate.Evaluator(2,matrices[2])
    a=s.Matrix([-2,3]);total=0
    for mask in itertools.product([0,1],repeat=len(bs)):
        exponent=a+sum((bit*N*s.Matrix(b) for bit,N,b in zip(mask,Ns,bs)),s.zeros(2,1))
        total+=(-1)**sum(mask)*E.term(list(exponent),bs,center)
    check(f'finite_geometric_product_{i}',total,s.prod(Ns),'finite_total_cancellation')

# Independently construct all six affine S3 triangle actions by permuting
# barycentric coordinates. N=5 makes the fixed center genuinely fractional.
N=5
c=s.Matrix([s.Rational(N,3)]*2)
bary_constants=[N,0,0]
bary_rows=[s.Matrix([[-1,-1]]),s.Matrix([[1,0]]),s.Matrix([[0,1]])]
group=[]
for permutation in itertools.permutations(range(3)):
    A=s.Matrix.vstack(bary_rows[permutation[1]],bary_rows[permutation[2]])
    t=s.Matrix([bary_constants[permutation[1]],bary_constants[permutation[2]]])
    group.append((A,t))
Q=sum((A.T*A for A,t in group),s.zeros(2))
check_true('affine_group_size_and_nonorthogonality',len(group)==6 and any(A.T*A!=s.eye(2) for A,t in group),'affine_group')
for i,(A,t) in enumerate(group):
    check_true(f'fixed_center_and_metric_{i}',A*c+t==c and A.T*Q*A==Q,'affine_group')
E=candidate.Evaluator(2,Q)
a=s.Matrix([2,-3]);bs=[s.Matrix(b) for b in [(1,0),(0,1),(1,1),(1,0)]]
reference=E.term(list(a),[list(b) for b in bs],list(c))
for i,(A,t) in enumerate(group):
    check(f'affine_dependent_seed_member_{i}',E.term(list(A*a+t),[list(A*b) for b in bs],list(c)),reference,'affine_equivariance')

# Rational-function stabilizers, including denominator permutations, determine
# orbit weights. Verify equalities in z, not merely equal scalar evaluations.
z0,z1=s.symbols('z0 z1')
def monomial(v): return z0**v[0]*z1**v[1]
def rational_term(a,bs): return monomial(a)/s.prod(1-monomial(b) for b in bs)
seed=rational_term([0,0],[[1,0],[0,1]])
members=[s.cancel(rational_term(t,[A*s.Matrix([1,0]),A*s.Matrix([0,1])])) for A,t in group]
stabilizer=[i for i,m in enumerate(members) if s.cancel(m-seed)==0]
unique=[]
for member in members:
    if all(s.cancel(member-old)!=0 for old in unique): unique.append(member)
check('triangle_stabilizer_order',len(stabilizer),2,'orbit_multiplicity')
check('triangle_distinct_orbit_size',len(unique),3,'orbit_multiplicity')
finite=sum(z0**i*z1**j for i in range(N+1) for j in range(N+1-i))
check('triangle_rational_identity',s.cancel(sum(unique)-finite),0,'finite_total_cancellation')
seed_value=E.term([0,0],[[1,0],[0,1]],list(c))
check('triangle_one_seed_distinct_weight',3*seed_value,(N+1)*(N+2)//2,'orbit_multiplicity')
check('proper_stabilizer_subgroup_repetitions',6*seed_value,2*((N+1)*(N+2)//2),'orbit_multiplicity')
check('weighted_repetition_compensation',s.Rational(1,2)*6*seed_value,(N+1)*(N+2)//2,'orbit_multiplicity')

# Negative controls must actually detect the tempting incorrect replacements.
bad=candidate.Evaluator(2,s.eye(2))
bad_values=[bad.term(list(t),[list(A*s.Matrix([1,0])),list(A*s.Matrix([0,1]))],list(c)) for A,t in group]
check_true('negative_noninvariant_metric_breaks_orbit_equality',len(set(bad_values))>1,'negative_control')
unfixed=[E.term(list(t),[list(A*s.Matrix([1,0])),list(A*s.Matrix([0,1]))],[0,0]) for A,t in group]
check_true('negative_omitted_center_breaks_affine_orbit_equality',len(set(unfixed))>1,'negative_control')
check_true('negative_group_size_overcounts_distinct_orbit',6*seed_value!=(N+1)*(N+2)//2,'negative_control')
tau=s.Symbol('tau', real=True)
check_true('negative_genuine_pole_has_no_ordinary_value',s.limit(1/(1-s.exp(tau)),tau,0,dir='+')==-s.oo and candidate.Evaluator(1,[[1]]).term([0],[[1]])==s.Rational(1,2),'negative_control')

# Input contract controls.
for name,thunk in [
    ('nonsymmetric_Q',lambda:candidate.Evaluator(2,[[1,2],[0,1]])),
    ('indefinite_Q',lambda:candidate.Evaluator(2,[[1,2],[2,1]])),
    ('irrational_Q',lambda:candidate.Evaluator(1,[[s.sqrt(2)]])),
    ('zero_binomial_vector',lambda:E.term([0,0],[[0,0]],list(c))),
    ('wrong_vector_dimension',lambda:E.term([0,0],[[1]],list(c))),
    ('inhomogeneous_degree_zero_input',lambda:E.degree_zero(E.x[0]+1,[[1,0]])),
]:
    try: thunk()
    except ValueError: passed=True
    else: passed=False
    check_true('reject_'+name,passed,'input_validation')

# Verify the frozen author files again after all execution.
for rel,data in manifest['files'].items():
    raw=(ROOT/rel).read_bytes()
    check_true('postrun_integrity_'+rel,hashlib.sha256(raw).hexdigest()==data['sha256'],'integrity')
result={'review_target':'30001568 / OWR-4426-005','public_author_subset_manifest_sha256':hashlib.sha256((ROOT/'PUBLIC_AUTHOR_MANIFEST.json').read_bytes()).hexdigest(),'sympy_version':s.__version__,'passed':len(checks),'failed':0,'author_tests_reproduced':author['passed'],'elapsed_seconds':round(time.monotonic()-start,3),'negative_control_evidence':{'noninvariant_metric_values':list(map(str,bad_values)),'omitted_center_values':list(map(str,unfixed)),'correct_triangle_seed_value':str(seed_value),'dependent_affine_seed_value':str(reference)},'checks':checks}
(OUT/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
