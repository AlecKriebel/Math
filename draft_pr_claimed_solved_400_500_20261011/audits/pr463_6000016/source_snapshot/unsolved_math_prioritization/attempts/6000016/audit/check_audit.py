#!/usr/bin/env python3
"""Read-only independent algebraic controls. Python 3 + SymPy; no network.

Usage: python check_audit.py [--author-dir /path/to/frozen/files]
The default is the sibling public/ directory, or this directory when collocated.
Analytic global nonexistence is audited in AUDIT_REPORT.md, not by this script.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import sympy as s

PINNED = {
    'FROZEN_AUTHOR_MANIFEST.json': '376b54e387e261f5dfdde1058ecf6c2fc889823a54fead31350584716848c896',
    'PROOF.md': '783f927e0e1bcc309547ad58371a64aeb4428553bfc329df22c980a2b8f0bdb0',
    'README.md': 'd6d4f98ffe015cc1fb89abd1c2773e771aaf4420ea47f6925985165516651a80',
    'SOURCE_GATE.md': '3a95531688ff58804096d8823463ee07f1145e7d3a1bc1d6d0887244f2ccd67a',
    'RESEARCH_LOG.md': '92dc4d89044678627044a45a29856a0ed6ee08cb87d495ca4ec51913e432a6d7',
    'check_exact.py': '76839bdc7a403d3552f6d1bfbe717d903524455a86b6a8f9ea0ade43b58c122a',
    'exact_results.json': 'f5ef9ddfd0786fde75c53bb338d7d759162aa44f6f86d9f91af41789fb818d25',
}
checks = []
def confirm(name, ok):
    if not ok:
        raise AssertionError(name)
    checks.append(name)

def identity(name, expression):
    entries = list(expression) if isinstance(expression, s.MatrixBase) else [expression]
    confirm(name, all(s.simplify(v) == 0 for v in entries))

here = Path(__file__).resolve().parent
p = argparse.ArgumentParser()
p.add_argument('--author-dir', type=Path, default=here.parent / 'public' if (here.parent / 'public').is_dir() else here)
args = p.parse_args()
author = args.author_dir.resolve()
for filename, digest in PINNED.items():
    confirm('frozen_sha256_' + filename, hashlib.sha256((author / filename).read_bytes()).hexdigest() == digest)
manifest = json.loads((author / 'FROZEN_AUTHOR_MANIFEST.json').read_text())
confirm('manifest_exact_six_author_entries', {e['path'] for e in manifest['files']} == set(PINNED) - {'FROZEN_AUTHOR_MANIFEST.json'})
for entry in manifest['files']:
    confirm('manifest_size_' + entry['path'], len((author / entry['path']).read_bytes()) == entry['bytes'])
    confirm('manifest_hash_' + entry['path'], PINNED[entry['path']] == entry['sha256'])
author_run = subprocess.run([sys.executable, str(author / 'check_exact.py')], check=True, capture_output=True)
confirm('author_rerun_byte_identical', author_run.stdout == (author / 'exact_results.json').read_bytes())
parsed = json.loads(author_run.stdout)
confirm('author_all_41_pass', parsed['status'] == 'PASS' and parsed['exact_identity_count'] == 41 and len(parsed['checks']) == 41)

x, y, t, u, v, r = s.symbols('x y t u v r', real=True)
m, n, a, b = s.symbols('m n a b', integer=True)
coords = (x, y)
zero = s.zeros(2)
K = [s.Matrix([[0, 0], [t, 0]]), zero]
e = [s.eye(2)[:, i] for i in range(2)]
for i in range(2):
    for j in range(2):
        identity('matrix_torsion_%d%d' % (i,j), K[i]*e[j]-K[j]*e[i])
        identity('matrix_curvature_%d%d' % (i,j), K[j].diff(coords[i])-K[i].diff(coords[j])+K[i]*K[j]-K[j]*K[i])
        identity('connection_operator_product_%d%d' % (i,j), K[i]*K[j])
    identity('parallel_volume_trace_%d' % i, s.trace(K[i]))

F = s.Matrix([x, y+t*x*x/2])
Finv = s.Matrix([u, v-t*u*u/2])
J = F.jacobian(coords)
identity('global_inverse_left', F.subs({x:Finv[0], y:Finv[1]}, simultaneous=True)-s.Matrix([u,v]))
identity('global_inverse_right', Finv.subs({u:F[0], v:F[1]}, simultaneous=True)-s.Matrix(coords))
identity('developing_jacobian_det_one', J.det()-1)
for i in range(2):
    identity('frame_change_connection_%d' % i, J.inv()*J.diff(coords[i])-K[i])

def H(aa,bb,vec):
    uu,vv = vec
    return s.Matrix([uu+aa, vv+bb+t*aa*uu+t*aa*aa/2])
q = s.Matrix([u,v])
identity('deck_action_conjugacy', F.subs({x:x+m,y:y+n}, simultaneous=True)-H(m,n,F))
identity('deck_group_law', H(m,n,H(a,b,q))-H(m+a,n+b,q))
identity('deck_group_inverse', H(-m,-n,H(m,n,q))-q)
identity('deck_linear_determinant', H(m,n,q).jacobian((u,v)).det()-1)
identity('central_developing_identity', F.subs(t,0)-s.Matrix(coords))
identity('polynomial_parameter_second_derivative', F.diff(t,2))

A, B, C = [s.Function(nm)(x,y) for nm in ('A','B','C')]
G = s.Matrix([[A,B],[B,C]])
def dg(metric):
    return [metric.diff(coords[i])-K[i].T*metric-metric*K[i] for i in range(2)]
def codazzi(metric):
    d = dg(metric)
    return s.Matrix([d[0][1,k]-d[1][0,k] for k in range(2)])
expected = s.Matrix([B.diff(x)-A.diff(y)-t*C,C.diff(x)-B.diff(y)])
identity('all_function_Codazzi_components', codazzi(G)-expected)
identity('obstruction_exterior_derivative_sign', expected[0]-(s.diff(B,x)-s.diff(A,y)-t*C))
identity('central_Euclidean_metric_Codazzi', codazzi(s.eye(2)).subs(t,0))
identity('noncentral_Euclidean_metric_obstruction', codazzi(s.eye(2))-s.Matrix([-t,0]))
identity('central_metric_Hessian', s.hessian((x*x+y*y)/2,coords)-s.eye(2))

# Boundary controls: local positive Hessian metrics exist, and indefinite metrics
# can descend. These tests would reject overclaims that omit compactness/positivity.
local_metric = J.T*J
identity('noncompact_pullback_metric_Codazzi', codazzi(local_metric))
identity('noncompact_pullback_metric_det_one', local_metric.det()-1)
identity('noncompact_pullback_B_not_periodic', local_metric[0,1].subs(x,x+1)-local_metric[0,1]-t)
indefinite = s.Matrix([[0,1],[1,0]])
identity('indefinite_periodic_metric_Codazzi', codazzi(indefinite))
identity('indefinite_metric_negative_determinant', indefinite.det()+1)
phi = u*v-t*u**3/3
hess = s.hessian(phi,(u,v)).subs({u:F[0],v:F[1]}, simultaneous=True)
identity('indefinite_metric_local_potential', J.T*hess*J-indefinite)

x0,y0,velx,vely = s.symbols('x0 y0 velx vely',real=True)
gamma = s.Matrix([x0+velx*r,y0+vely*r-t*velx**2*r**2/2])
velocity = gamma.diff(r)
identity('all_initial_data_geodesic_equation', gamma.diff(r,2)+sum((K[i]*velocity*velocity[i] for i in range(2)),s.zeros(2,1)))
identity('all_initial_positions', gamma.subs(r,0)-s.Matrix([x0,y0]))
identity('all_initial_velocities', velocity.subs(r,0)-s.Matrix([velx,vely]))

print(json.dumps({
    'status':'PASS',
    'author_exact_identity_count':41,
    'audit_control_count':len(checks),
    'checks':checks,
    'analytic_scope':'Universal nonexistence uses the reviewed periodicity, strict positivity, and Stokes argument; no symbolic count certifies those hypotheses.',
    'source_scope':'Original item 5(b), p. 126, and Baues-Goldman v2 pp. 8 and 20 were visually reviewed separately; source interpretation is not automated.',
},indent=2,sort_keys=True))
