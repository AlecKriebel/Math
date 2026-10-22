#!/usr/bin/env python3
"""Independent algebra checks and a nonmutating replay of the reviewed packet.

Run from any directory with Python 3.11+ and SymPy 1.14.0 installed.
The adjacent public directory is read only. This script writes audit_results.json
beside itself. No network access, source documents, or mathematical corpus needed.
These checks are algebraic controls, not certification of analytic arguments.
"""

import hashlib
import itertools
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import sympy as s

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent / "public"
EXPECTED_MANIFEST = "3cea69df13cb1c9605b22cdbda7d9b0a454f8e3fc92b20ea759099557643e3ff"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

before = {p.name: sha(p) for p in sorted(PACKET.iterdir()) if p.is_file()}
assert before["SHA256SUMS"] == EXPECTED_MANIFEST
for line in (PACKET / "SHA256SUMS").read_text().splitlines():
    expected, name = line.split(maxsplit=1)
    assert before[name] == expected, name
assert s.__version__ == "1.14.0"

# Replay in temporary storage because the submitted verifier writes its result.
with tempfile.TemporaryDirectory() as td:
    replay_script = Path(td) / "verify.py"
    shutil.copyfile(PACKET / "verify.py", replay_script)
    replay = subprocess.run([sys.executable, str(replay_script)], capture_output=True, text=True)
    assert replay.returncode == 0, replay.stderr
    replay_result = json.loads((Path(td) / "verification.json").read_text())
    assert replay_result == json.loads((PACKET / "verification.json").read_text())
    assert replay_result["number_of_checks"] == 38

# Re-derive the examples with exterior-form components rather than the packet's
# curl helper. Two-forms are stored in the order (dx^dy, dx^dz, dy^dz).
x, y, z, t = s.symbols("x y z t", real=True)
xyz = (x, y, z)
n = s.symbols("n", integer=True, positive=True)
k = s.symbols("k", integer=True, positive=True)
q = 2 * s.pi
checks = {}
additional = {}

def same(name, left, right, collection=checks):
    delta = left - right
    if isinstance(delta, s.MatrixBase):
        ok = all(s.simplify(v) == 0 for v in delta)
    else:
        ok = s.simplify(delta) == 0
    assert ok, (name, delta)
    collection[name] = True

def d1(a):
    return s.Matrix([s.diff(a[j], xyz[i]) - s.diff(a[i], xyz[j])
                     for i, j in ((0, 1), (0, 2), (1, 2))])

def i_volume(v):
    return s.Matrix([v[2], -v[1], v[0]])

def d2(w):
    return s.diff(w[2], x) - s.diff(w[1], y) + s.diff(w[0], z)

def wedge(a, w):
    return a[0]*w[2] - a[1]*w[1] + a[2]*w[0]

def integral(expr):
    return s.simplify(s.integrate(expr, (x, 0, 1), (y, 0, 1), (z, 0, 1)))

B = s.Matrix([s.sin(q*z), s.cos(q*z), 0])
C = s.Matrix([-s.sin(q*z), s.cos(q*z), 0])
reflection = s.Matrix([-x, y, z])
same("reflection_determinant", reflection.jacobian(xyz).det(), -1)
same("positive_beltrami_curl", d1(B), q*i_volume(B))
same("negative_beltrami_curl", d1(C), -q*i_volume(C))
same("positive_helicity", integral(wedge(B/q, d1(B/q))), 1/q)
same("negative_helicity", integral(wedge(-C/q, d1(-C/q))), -1/q)

h = s.Matrix([x, y+s.sin(q*n*x)/n, z])
U = s.Matrix([s.sin(q*z), 0, 0])
Un = s.Matrix([s.sin(q*z), q*s.cos(q*n*x)*s.sin(q*z), 0])
AU = s.Matrix([0, s.cos(q*z)/q, 0])
AUn = s.Matrix([-s.cos(q*z)*s.cos(q*n*x), s.cos(q*z)/q, 0])
same("shear_jacobian", h.jacobian(xyz).det(), 1)
same("shear_pushforward", h.jacobian(xyz)*U, Un)
same("original_shear_primitive", d1(AU), i_volume(U))
same("pushed_shear_primitive", d1(AUn), i_volume(Un))
same("shear_divergence", d2(i_volume(Un)), 0)
same("shear_squared_L2_error", integral(sum(v*v for v in (Un-U))), s.pi**2)
same("shear_helicity_density", wedge(AUn, d1(AUn)), 0)

X = s.Matrix([s.sin(q*y), s.sin(q*z), s.sin(q*x)])
A = s.Matrix([-s.cos(q*z)/q, -s.cos(q*x)/q, -s.cos(q*y)/q])
same("indexed_field_divergence", d2(i_volume(X)), 0)
same("indexed_field_primitive", d1(A), i_volume(X))
same("indexed_field_helicity", integral(wedge(A, d1(A))), 0)
all_indices = []
for i, j, ell in itertools.product((0, 1), repeat=3):
    point = dict(zip(xyz, (s.Rational(i,2), s.Rational(j,2), s.Rational(ell,2))))
    suffix = f"{i}{j}{ell}"
    same("zero_"+suffix, X.subs(point), s.zeros(3, 1))
    index = (-1)**(i+j+ell)
    same("index_"+suffix, X.jacobian(xyz).det().subs(point), q**3*index)
    all_indices.append(index)
same("total_index", sum(all_indices), 0)
same("boundary_radius_lower_bound", 4*s.Rational(1,8), s.Rational(1,2))

V = s.Matrix([0, s.sin(q*z), 0])
AV = s.Matrix([-s.cos(q*z)/q, 0, 0])
same("rough_shear_field_primitive", d1(AV), i_volume(V))
same("rough_shear_field_divergence", d2(i_volume(V)), 0)
same("rough_shear_field_helicity", integral(wedge(AV, d1(AV))), 0)
same("oscillatory_extremal_values", s.sin(s.pi/2+k*s.pi), (-1)**k)
N, K = s.symbols("N K", positive=True)
lower = 2*(N-K)/s.sqrt(s.pi/2+N*s.pi)
assert s.limit(lower, N, s.oo) == s.oo
checks["variation_lower_bound_diverges"] = True
assert len(checks) == 38
assert set(checks) == set(replay_result["checks"])

# Additional independent controls for exact primitives, same-time flows,
# local radial gauge, wedge signs, and endpoint growth distinctions.
hi = s.Matrix([x, y-s.sin(q*n*x)/n, z])
same("shear_inverse_left", hi.subs(dict(zip(xyz,h)), simultaneous=True), s.Matrix(xyz), additional)
same("shear_inverse_right", h.subs(dict(zip(xyz,hi)), simultaneous=True), s.Matrix(xyz), additional)
same("pushed_primitive_pullback", h.jacobian(xyz).T*AUn.subs(dict(zip(xyz,h)), simultaneous=True), AU, additional)
psi = s.Matrix([x+t*s.sin(q*z), y+(s.sin(q*n*(x+t*s.sin(q*z)))-s.sin(q*n*x))/n, z])
same("flow_initial_condition", psi.subs(t,0), s.Matrix(xyz), additional)
same("flow_generator_for_all_t", psi.diff(t), Un.subs(dict(zip(xyz,psi)), simultaneous=True), additional)
phi = s.Matrix([x+t*s.sin(q*z), y, z])
same("same_time_flow_conjugacy", h.subs(dict(zip(xyz,phi)), simultaneous=True), psi.subs(dict(zip(xyz,h)), simultaneous=True), additional)
F = s.Function("F")
g = s.Matrix([x, y+F(x), z])
phiV = s.Matrix([x,y+t*s.sin(q*z),z])
same("arbitrary_shear_commutes_with_V", g.subs(dict(zip(xyz,phiV)), simultaneous=True), phiV.subs(dict(zip(xyz,g)), simultaneous=True), additional)
linearX = s.Matrix([y,z,x])
rho = s.Matrix([(-x*y+z*z)/3, (x*x-y*z)/3, (-x*z+y*y)/3])
same("radial_primitive_linear_model", d1(rho), i_volume(linearX), additional)
lambda_ = s.symbols("lambda", positive=True)
same("radial_primitive_quadratic_order", rho.subs({x:lambda_*x,y:lambda_*y,z:lambda_*z}, simultaneous=True), lambda_**2*rho, additional)
r,a,b = s.symbols("r a b", positive=True)
same("boundary_growth_exponent", r**2*r**2*r**(-a)*r**(2*b), r**(4+2*b-a), additional)
same("cutoff_L2_exponent", s.sqrt(r**2*r**3), r**s.Rational(5,2), additional)
a1 = s.Matrix([x*y,z*x,y*z])
gamma = s.Matrix([y,x,0])  # d(xy), a closed one-form
cross = gamma.cross(a1)
same("closed_form_stokes_sign", sum(s.diff(cross[i],xyz[i]) for i in range(3)), -wedge(gamma,d1(a1)), additional)

assert before == {p.name: sha(p) for p in sorted(PACKET.iterdir()) if p.is_file()}
result = {
    "problem_id": 30006363,
    "date_utc": "2026-10-04",
    "packet_manifest_sha256": EXPECTED_MANIFEST,
    "packet_hashes_verified_and_unchanged": True,
    "sympy_version": s.__version__,
    "submitted_verifier_replayed": {"checks": 38, "all_passed": True, "output_identical": True},
    "independent_controls": {"checks": len(checks), "all_passed": True, "results": checks},
    "additional_controls": {"checks": len(additional), "all_passed": True, "results": additional},
    "scope": "Exact algebra and examples only; not a proof of the analytic propositions or the unrestricted conjecture.",
}
(HERE / "audit_results.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps({key:result[key] for key in ("problem_id","packet_hashes_verified_and_unchanged","submitted_verifier_replayed")},indent=2))
print(f"Independent controls: {len(checks)}/38. Additional controls: {len(additional)}/12.")
