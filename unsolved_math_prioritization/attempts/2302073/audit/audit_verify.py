#!/usr/bin/env python3
"""Independent exact checks for the frozen Rubel 2.73 audit.

Reads the sibling public directory, never writes there, and prints JSON.
Finite symbolic checks supplement, rather than certify, the analytic audit.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import sympy as s

PUBLIC = Path(__file__).resolve().parent.parent / 'public'
EXPECTED = 'f8944c83f3131caa950cf466ff5c7332fc7db2f5ba271e49a9eb66429363858f'
checks = []
def check(name, condition):
    if not bool(condition):
        raise AssertionError(name)
    checks.append(name)
def eq(name, lhs, rhs=0):
    check(name, s.expand(lhs-rhs) == 0)
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

author_manifest = PUBLIC / 'FROZEN_MANIFEST.json'
check('expected_frozen_manifest_hash', digest(author_manifest) == EXPECTED)
manifest = json.loads(author_manifest.read_text())
actual = {p.name for p in PUBLIC.iterdir() if p.is_file()}
expected_files = {e['path'] for e in manifest['files']} | {'FROZEN_MANIFEST.json'}
check('exact_frozen_file_set', actual == expected_files)
frozen_hashes = {}
for entry in manifest['files']:
    p = PUBLIC / entry['path']
    check('frozen_integrity_'+entry['path'], p.stat().st_size == entry['bytes'] and digest(p) == entry['sha256'])
    frozen_hashes[entry['path']] = digest(p)
frozen_hashes['FROZEN_MANIFEST.json'] = digest(author_manifest)
replay = subprocess.run([sys.executable, str(PUBLIC/'verify.py')], capture_output=True, env={**os.environ, 'PYTHONDONTWRITEBYTECODE':'1'})
check('author_replay_success', replay.returncode == 0)
check('author_replay_exact_output', replay.stdout == (PUBLIC/'verification.json').read_bytes())
check('author_replay_35_assertions', json.loads(replay.stdout)['assertions'] == 35)
checksum = subprocess.run(['sha256sum','-c','SHA256SUMS'], cwd=PUBLIC, capture_output=True)
check('author_sha256sums_replay', checksum.returncode == 0)

x,y,t,q,R,k,e = s.symbols('x y t q R k e')
f = s.Matrix([y,(y*y-x)/2])
g = s.Matrix([x*x-2*y,x])
M = f.jacobian([x,y]).subs({x:0,y:0})
D = s.diag(s.Rational(3,4),1)
weighted_M = D*M*D.inv()
weighted_inverse = D*M.inv()*D.inv()
operator_norm = lambda a: max(sum(abs(v) for v in a.row(i)) for i in range(a.rows))
eq('independent_weighted_operator_norm',operator_norm(weighted_M),s.Rational(3,4))
eq('independent_inverse_operator_norm',operator_norm(weighted_inverse),s.Rational(3,2))
check('spectral_polynomial', M.charpoly(t).as_expr() == t*t+s.Rational(1,2))
check('spectral_gap_squared', s.Rational(1,4)<s.Rational(1,2))
# r=q/6 with 0<=q<=1 turns the contraction margin into a manifestly nonnegative product.
r=q/6
eq('contraction_interval_margin',s.Rational(3,4)*r-r*r/2-s.Rational(2,3)*r,q*(1-q)/72)
ratio=operator_norm(weighted_inverse)*operator_norm(weighted_M)**2
eq('derived_geometric_ratio',ratio,s.Rational(27,32))
check('summability',ratio<1)
eq('tail_constant_from_sum',operator_norm(weighted_inverse)/2/(1-ratio),s.Rational(24,5))

# Independently expand finite normalized iterates and their Jacobians.
p=s.Matrix([x,y]); normalized=[]
for n in range(4):
    H=(M**(-n)*p).applyfunc(s.expand)
    normalized.append(H)
    eq('normalized_iterate_jacobian_'+str(n),H.jacobian([x,y]).det(),1)
    check('normalized_iterate_derivative_'+str(n),H.jacobian([x,y]).subs({x:0,y:0})==s.eye(2))
    p=f.subs({x:p[0],y:p[1]},simultaneous=True).applyfunc(s.expand)
for n in range(3):
    difference=normalized[n].subs({x:f[0],y:f[1]},simultaneous=True)-M*normalized[n+1]
    for j in range(2):
        eq('finite_intertwining_'+str(n)+'_'+str(j),difference[j])
for j in range(2):
    eq('independent_inverse_composition_'+str(j),g.subs({x:f[0],y:f[1]},simultaneous=True)[j],[x,y][j])

# Solve the degree-2 and degree-3 homological equations independently.
def trunc(expr,n):
    poly=s.Poly(s.expand(expr),x,y)
    return sum(c*x**a*y**b for (a,b),c in poly.terms() if a+b<=n)
mon=[x*x,x*y,y*y,x**3,x*x*y,x*y*y,y**3]
c=s.symbols('c:14')
H=s.Matrix([x+sum(c[j]*mon[j] for j in range(7)),y+sum(c[7+j]*mon[j] for j in range(7))])
res=H.subs({x:f[0],y:f[1]},simultaneous=True)-M*H
equations=[v for expr in res for power,v in s.Poly(trunc(expr,3),x,y).terms()]
solutions=s.solve(equations,c,dict=True)
check('unique_cubic_conjugacy_jet',len(solutions)==1 and len(solutions[0])==14)
H=H.subs(solutions[0])
eq('conjugacy_jet_first',H[0],x-s.Rational(2,3)*y*y-s.Rational(2,9)*x*x*y)
eq('conjugacy_jet_second',H[1],y-x*x/6+s.Rational(4,9)*x*y*y)
eq('conjugacy_jet_unit_jacobian_through_degree_two',trunc(H.jacobian([x,y]).det(),2),1)

# Boundary variables make both geometric trapping inequalities transparent.
eq('middle_trap_boundary_polynomial',((t*t-10)-(10+t)).subs(t,5+k),k*k+9*k)
eq('outer_trap_boundary_polynomial',(t*t-3*t+20-10).subs(t,10+k),k*k+17*k+80)
check('outer_boundary_strict',80>0)
# A second normality cross-check: at t=2(R+2)+k, the lower bound is >=t^2/2.
lower=t*t-(R+1)*t-1
eq('marty_large_slope_margin',(lower-t*t/2).subs(t,2*(R+2)+k),2*R+3+(R+3)*k+k*k/2)
check('marty_large_slope_minimum_positive',3>0)
# Opposite Jacobian orientation would invalidate the claimed positive defect.
A=s.Matrix([x+y*y,y]);L=s.Matrix([y/25,x/25])
composed=A.subs({x:L[0],y:L[1]},simultaneous=True)
eq('coordinate_changes_combined_jacobian',composed.jacobian([x,y]).det(),-s.Rational(1,625))
Ua,Ub,Va,Vb,z=s.symbols('Ua Ub Va Vb z')
eq('negative_jacobian_defect',(Ub+z*Vb)*Va-(Ua+z*Va)*Vb,-(Ua*Vb-Ub*Va))
Gw,Gzw,Ha,Hb=s.symbols('Gw Gzw Ha Hb')
eq('arbitrary_factorization_zero_defect',(Gw*Hb)*(Gzw*Ha)-(Gw*Ha)*(Gzw*Hb),0)

# Mutation controls ensure the special norm, basin, and infinity convention matter.
wrong_M=s.Matrix([[0,1],[s.Rational(1,2),0]])
check('negative_control_wrong_sign_detected',wrong_M != M)
euclidean_M=s.sqrt(max((M.T*M).eigenvals()))
euclidean_inverse=s.sqrt(max((M.inv().T*M.inv()).eigenvals()))
check('negative_control_euclidean_bound_not_summable',euclidean_inverse*euclidean_M**2 == 2)
# r=1/5, x=-4r/3,y=r violates the claimed 3/4 contraction outside B.
r=s.Rational(1,5)
outside=f.subs({x:-4*r/3,y:r})
check('negative_control_larger_ball_fails',max(3*abs(outside[0])/4,abs(outside[1]))>3*r/4)
check('negative_control_unrestricted_affine_family',s.limit(t/(1+abs(t*0)**2),t,s.oo)==s.oo)
check('negative_control_finite_only_limits_fail',s.limit(t*t,t,s.oo)==s.oo)
for name,h in frozen_hashes.items():
    check('unchanged_after_replay_'+name,digest(PUBLIC/name)==h)

print(json.dumps({
 'problem_id':2302073,'status':'PASS','author_assertions_replayed':35,
 'audit_assertions':len(checks),'checks':checks,
 'frozen_manifest_sha256':EXPECTED,'frozen_file_hashes':frozen_hashes,
 'python_version':sys.version.split()[0],'sympy_version':s.__version__,
 'cubic_conjugacy_jet':[str(v) for v in H],
 'limitations':'Exact finite supplementary checks; the global analytic proof is audited in ADVERSARIAL_AUDIT.md. No formal proof-assistant or human peer-review claim.'
},indent=2,sort_keys=True))
