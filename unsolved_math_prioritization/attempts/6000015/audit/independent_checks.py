#!/usr/bin/env python3
"""Frozen-packet replay and independently formulated finite controls.

Usage: python independent_checks.py [path/to/public]
These computations supplement, and do not prove, the analytic assertions.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import sympy as s

packet = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'public'
checks = []
def test(name, assertion):
    if not bool(assertion):
        raise AssertionError(name)
    checks.append(name)
def zero(expression):
    return s.simplify(s.trigsimp(expression)) == 0

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

expected_manifest = '9e6d6a08ddef9005d5bacf9995a3221692e1daf2ed689a52c16597bf6b3733c9'
expected_proof = 'd00dc75d1a734bbfb257403eeac82b9b86341003f93ae90f78f5b4df1bc3defb'
assert digest(packet / 'FROZEN_MANIFEST.json') == expected_manifest
assert digest(packet / 'PROOF.md') == expected_proof
manifest = json.loads((packet / 'FROZEN_MANIFEST.json').read_text())
for filename, expected in manifest['files'].items():
    data = (packet / filename).read_bytes()
    assert len(data) == expected['bytes']
    assert hashlib.sha256(data).hexdigest() == expected['sha256']
replay = subprocess.run([sys.executable, str(packet / 'verify.py')], check=True, text=True, capture_output=True)
expected_text = (packet / 'verification_results.json').read_text()
assert replay.stdout == expected_text
record = json.loads(replay.stdout)
assert record['status'] == 'PASS' and record['check_count'] == 60

# Direct Wirtinger operators, separately formed from the verification program.
x1,x2,y1,y2,t = s.symbols('x1 x2 y1 y2 t', real=True)
x,y = (x1,x2),(y1,y2)
def dz(f,i): return (s.diff(f,x[i])-s.I*s.diff(f,y[i]))/2
def dzbar(f,i): return (s.diff(f,x[i])+s.I*s.diff(f,y[i]))/2
phi=(x1**2+x2**2)/2-s.cos(x1)*s.cos(x2)/4
metric=s.hessian(phi,x)
fiber=s.Matrix(y)
norm=(fiber.T*metric*fiber)[0]
levi=s.Matrix(2,2,lambda i,j:dz(dzbar(norm,j),i))
point={x1:0,x2:0,y1:4,y2:0}
test('full_torus_levi_bad_point',levi.subs(point)==-s.Rational(3,8)*s.eye(2))
test('full_torus_gradient_bad_point',s.Matrix([dz(norm,i) for i in range(2)]).subs(point)==s.Matrix([-5*s.I,0]))
test('rho_bad_point',norm.subs(point)==20)
test('transverse_gradient_all_t',zero(dz(norm,1).subs({x1:0,x2:0,y1:t,y2:0})))
test('transverse_levi_all_t',zero(levi[1,1].subs({x1:0,x2:0,y1:t,y2:0})-(s.Rational(5,8)-t**2/16)))
alpha,beta=s.symbols('alpha beta',real=True)
composition=alpha*levi[1,1]+beta*dz(norm,1)*dzbar(norm,1)
test('scalar_reparametrization_at_bad_point',zero(composition.subs(point)+3*alpha/8))

# A non-coordinate rank-one lattice in R^2; the quotient base is noncompact.
B=s.Matrix([1,1]);P=s.eye(2)-B*(B.T*B).inv()*B.T
u1,u2,v1,v2=s.symbols('u1 u2 v1 v2',real=True)
u=s.Matrix([u1,u2]);v=s.Matrix([v1,v2])
F=(u.T*P*u)[0]-s.log(s.cos(v1))-s.log(s.cos(v2))
LF=(s.hessian(F,(u1,u2))+s.hessian(F,(v1,v2)))/4
expected=P/2+s.diag(1/s.cos(v1)**2,1/s.cos(v2)**2)/4
test('strip_levi_direct_hessians',all(zero(e) for e in LF-expected))
test('projection_exact',P==s.Matrix([[s.Rational(1,2),-s.Rational(1,2)],[-s.Rational(1,2),s.Rational(1,2)]]))
test('strip_uniform_lower_bound_at_center',set((LF.subs({v1:0,v2:0})).eigenvals())=={s.Rational(1,4),s.Rational(3,4)})
test('projection_kills_lattice',P*B==s.zeros(2,1))

# gamma(x1,x2)=(2*x2,2*x1) preserves the positive quadrant.
# Its square is 4I; on logarithms it is swap + log(2)*(1,1).
S=s.Matrix([[0,1],[1,0]])
G=2*S
ell=s.log(2)
test('facet_permutation_order_two',S*S==s.eye(2))
test('scaling_kernel_square',G*G==4*s.eye(2))
test('affine_action_has_no_nonzero_fixed_vector',(G-s.eye(2)).det()!=0)
test('log_action_square',S*(S*u+ell*B)+ell*B==u+2*ell*B)
shifted=(S*u+ell*B).T*P*(S*u+ell*B)
test('real_exhaustion_invariant_under_swap_scale',zero(shifted[0]-(u.T*P*u)[0]))
test('barrier_invariant_under_swap',zero((-s.log(s.cos(v2))-s.log(s.cos(v1)))-(-s.log(s.cos(v1))-s.log(s.cos(v2)))))
test('noncompact_base_direction_control',zero((u.T*P*u)[0]-(u1-u2)**2/2))

# A bounded, nonconical interval: its two facet forms have an affine relation.
A=s.Matrix([[1],[-1]])
test('interval_facets_separate_points',A.rank()==1)
test('interval_affine_relation',s.expand(x1+(1-x1))==1)

# Verify genuine local degeneracy, rather than only a pointwise null value.
active=s.log(x1*x1+y1*y1)/2-s.log(x1)
test('active_support_branch_transverse_gradient',dz(active,1)==0)
test('active_support_branch_transverse_levi',dz(dzbar(active,1),1)==0)
test('active_support_branch_positive_levi',zero(dz(dzbar(active,0),0)-1/(4*x1*x1)))

print(json.dumps({
    'status':'PASS',
    'frozen_manifest_sha256':expected_manifest,
    'frozen_proof_sha256':expected_proof,
    'frozen_files_verified':len(manifest['files']),
    'author_replay_check_count':record['check_count'],
    'author_replay_byte_identical':True,
    'independent_control_count':len(checks),
    'independent_controls':checks,
    'sympy_version':s.__version__,
    'scope':'Finite algebraic controls and integrity checks only. Analytic arguments are reviewed separately; the original question remains unresolved.'
},indent=2,sort_keys=True))
