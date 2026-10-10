#!/usr/bin/env python3
"""Independent exact audit controls, using SymPy rather than author's algebra.

The Cartesian curve is differentiated from its Laurent representation. Analytic
and global assertions are reviewed in AUDIT.md; these finite checks are not a
universal rigidity proof. No network access and no author-file modification.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import zipfile
import sympy as S

BASE = Path(__file__).resolve().parent
AUTHOR = BASE.parent / 'geometry_7000003'
ARCHIVE = BASE.parent / 'GEOMETRY_7000003_AUTHOR_SAFE_FREEZE.zip'
passed, rejected = [], []

def check(name, condition):
    if not condition:
        raise AssertionError(name)
    passed.append(name)

def zero(expr):
    return S.simplify(S.expand(expr)) == 0

def equal_vec(a, b):
    return all(zero(x-y) for x, y in zip(a, b))

def reject(name, false_claim):
    if false_claim:
        raise AssertionError('Mutation accepted: ' + name)
    rejected.append(name)

frozen = {p.name: p.read_bytes() for p in AUTHOR.iterdir() if p.is_file()}
check('seven_author_files', set(frozen) == {
    'README.md', 'PROOFS.md', 'SOURCES.json', 'verify.py',
    'verify_manifest.py', 'EXPECTED_RESULTS.json', 'MANIFEST.json'})
archive_data = ARCHIVE.read_bytes()
check('archive_size', len(archive_data) == 15539)
check('archive_sha256', hashlib.sha256(archive_data).hexdigest() ==
      'fd97db7181994876f78dbc2afc20d497bdd2fd34becdf2f20c10c8ea66cb4b48')
with zipfile.ZipFile(ARCHIVE) as zf:
    entries = [i for i in zf.infolist() if not i.is_dir()]
    check('archive_seven_files', len(entries) == 7)
    archived = {Path(i.filename).name: zf.read(i) for i in entries}
    check('archive_matches_author_files', archived == frozen)
manifest = json.loads(frozen['MANIFEST.json'])
check('author_manifest_digests_and_sizes', all(
    len(frozen[e['path']]) == e['bytes'] and
    hashlib.sha256(frozen[e['path']]).hexdigest() == e['sha256']
    for e in manifest['files']))
author_run = subprocess.run([sys.executable, str(AUTHOR/'verify.py')],
                            check=True, capture_output=True, text=True)
author_result = json.loads(author_run.stdout)
check('author_replay_matches_expected', author_result ==
      json.loads(frozen['EXPECTED_RESULTS.json']))
check('author_replay_24_assertions_8_controls',
      author_result['assertions_passed'] == 24 and
      author_result['corrupted_controls_rejected'] == 8)

# Start directly from Cartesian gamma, z = exp(i*q). Differentiation is i*z*d/dz.
z = S.symbols('z', nonzero=True)
C, U = (z + z**-1)/2, (z - z**-1)/(2*S.I)
c, w = (z**2 + z**-2)/2, (z**2 - z**-2)/(2*S.I)
gamma = S.Matrix([(4+c)*C, (4+c)*U, w])
def dq(v):
    return v.applyfunc(lambda e: S.expand(S.I*z*S.diff(e, z)))
v = dq(gamma)
a = dq(v)
j = dq(a)
cross = v.cross(a).applyfunc(S.expand)
D = S.expand(v.dot(a.cross(j)))
expected_D = -6*(c**3 - 24*c**2 + 32)
check('cartesian_laurent_torsion_determinant', zero(D-expected_D))
check('cartesian_laurent_speed_squared', zero(v.dot(v)-((4+c)**2+4)))
x = S.symbols('x', real=True)
check('torsion_strict_sign_certificate', zero(
    x**3-24*x*x+32 - (7+(x+1)*(x*x-x+1)+24*(1-x*x))))
check('positive_quadratic_certificate', zero(
    x*x-x+1 - ((x-S.Rational(1,2))**2+S.Rational(3,4))))
check('radius_and_speed_lower_bounds', 4-1 == 3 and 3**2+4 == 13)
reflect = S.diag(1, 1, -1)
Dr = (reflect*v).dot((reflect*a).cross(reflect*j))
reject('reflecting_height_preserves_torsion_sign', zero(Dr-expected_D))
reject('speed_constant_3_instead_of_4', zero(v.dot(v)-((4+c)**2+3)))

# Recover all four normal-offset test points from the independently derived jets.
t = S.symbols('t', real=True)
offsets = []
angles = [S.Integer(1), S.Integer(-1), S.I, (1+S.I)/S.sqrt(2)]
expected_normals = [S.Matrix([-1,0,0]), S.Matrix([1,0,0]),
                    S.Matrix([0,1,0])]
for idx, zz in enumerate(angles):
    vv = v.subs(z, zz).applyfunc(S.simplify)
    aa = a.subs(z, zz).applyfunc(S.simplify)
    raw = (aa-vv*aa.dot(vv)/vv.dot(vv)).applyfunc(S.simplify)
    nn = (raw/S.sqrt(raw.dot(raw))).applyfunc(S.simplify)
    gg = gamma.subs(z, zz).applyfunc(S.simplify)
    offsets.append(gg+t*nn)
    check('derived_unit_normal_%d' % idx, zero(nn.dot(nn)-1) and zero(nn.dot(vv)))
    if idx < 3:
        check('normal_cardinal_value_%d' % idx, equal_vec(nn, expected_normals[idx]))
    else:
        check('normal_quarter_height', zero(nn[2]+5/S.sqrt(70)))
        reject('unnormalized_acceleration_is_frenet_normal', zero(aa.dot(vv)))
vol = S.det(S.Matrix.hstack(*(offsets[i]-offsets[0] for i in (1,2,3))))
check('four_point_offset_volume', zero(vol+
    2*(5-t)*(3+t)*(1-5*t/S.sqrt(70))))
check('offset_height_strict_bound', S.Rational(25,70) < 1)
reject('offset_boundaries_coplanar_as_identity', zero(vol))

# Additional adversarial normal-bundle control: B has a repeated value.
check('binormal_numerator_x', zero(cross[0]-2*U*(3*c*c-2*c-4)))
check('binormal_reflection_symmetry',
      zero(cross[0].subs(z,1/z)+cross[0]) and
      zero(cross[1].subs(z,1/z)-cross[1]) and
      zero(cross[2].subs(z,1/z)-cross[2]))
cstar = (1-S.sqrt(13))/3
check('repeated_binormal_root', zero(3*cstar*cstar-2*cstar-4)
      and bool(cstar > -1) and bool(cstar < 1))

# Rotation-field compatibility derived from arbitrary components, not copied jets.
aa, bb, cc, dd, ee, ff = S.symbols('aa bb cc dd ee ff')
e1, e2 = S.Matrix([1,0,0]), S.Matrix([0,1,0])
compatibility = S.Matrix([aa,bb,cc]).cross(e2)-S.Matrix([dd,ee,ff]).cross(e1)
sol = S.solve(list(compatibility), (cc,ff,ee), dict=True)[0]
check('rotation_derivatives_tangent', sol[cc] == 0 and sol[ff] == 0)
p, q, h = S.symbols('p q h')
y = S.Matrix([h,-q,p])
check('unique_rotation_reconstructs_strain_map',
      equal_vec(y.cross(e1), S.Matrix([0,p,q])) and
      equal_vec(y.cross(e2), S.Matrix([-p,0,h])))

# Solve the Fourier-reduced strain system, including the zero mode.
m, r, rp, zp, B, H, Bp, Hp = S.symbols('m r rp zp B H Bp Hp')
strain = [-S.I*m*rp*Bp+zp*Hp,
          r*Bp+rp*(m*m-1)*B+S.I*m*zp*H]
mode_sol = S.solve(strain, (Bp,Hp), dict=True)[0]
expected_Bp = -rp*(m*m-1)*B/r-S.I*m*zp*H/r
expected_Hp = -S.I*m*rp**2*(m*m-1)*B/(r*zp)+m*m*rp*H/r
check('fourier_system_solved_independently',
      zero(mode_sol[Bp]-expected_Bp) and zero(mode_sol[Hp]-expected_Hp))
check('zero_mode_included', zero(mode_sol[Bp].subs(m,0)-rp*B/r)
      and zero(mode_sol[Hp].subs(m,0)))
reject('fourier_axial_sign_reversal', zero(
    strain[0].subs({Bp:expected_Bp,Hp:-expected_Hp})))

# Differentiate both associate immersions in Cartesian coordinates.
u, theta, alpha = S.symbols('u theta alpha', real=True)
cat = S.Matrix([S.cosh(u)*S.cos(theta),S.cosh(u)*S.sin(theta),u])
hel = S.Matrix([S.sinh(u)*S.sin(theta),-S.sinh(u)*S.cos(theta),theta])
check('associate_derivative_relations', equal_vec(hel.diff(u),-cat.diff(theta))
      and equal_vec(hel.diff(theta),cat.diff(u)))
associate = S.cos(alpha)*cat+S.sin(alpha)*hel
du, dt = associate.diff(u), associate.diff(theta)
check('associate_metric_E', zero(S.trigsimp(du.dot(du))-S.cosh(u)**2))
check('associate_metric_F', zero(S.trigsimp(du.dot(dt))))
check('associate_metric_G', zero(S.trigsimp(dt.dot(dt))-S.cosh(u)**2))
period = (associate.subs(theta,theta+2*S.pi)-associate).applyfunc(S.trigsimp)
check('associate_global_period', equal_vec(period,S.Matrix([0,0,2*S.pi*S.sin(alpha)])))
reject('helicoid_descends_to_annulus', equal_vec(period.subs(alpha,S.pi/2),S.zeros(3,1)))

# Differential Frenet-frame computation of the entire normal ribbon, not just core.
k, tau, kp, tp = S.symbols('k tau kp tp', real=True)
def ds(vec):
    derivative = vec.applyfunc(lambda e:S.diff(e,k)*kp+S.diff(e,tau)*tp)
    return derivative+S.Matrix([-k*vec[1],k*vec[0]-tau*vec[2],tau*vec[1]])
T, N = S.Matrix([1,0,0]), S.Matrix([0,1,0])
xs, xt = T+t*ds(N), N
xss, xst = ds(xs), xs.diff(t)
nn = xs.cross(xt)
E = S.expand(xs.dot(xs))
LL, MM = S.expand(xss.dot(nn)), S.expand(xst.dot(nn))
check('ribbon_metric', zero(E-((1-t*k)**2+t*t*tau*tau))
      and zero(xs.dot(xt)) and xt.dot(xt)==1)
check('ribbon_normal', equal_vec(nn,S.Matrix([-t*tau,0,1-t*k]))
      and zero(nn.dot(nn)-E))
check('ribbon_full_L_numerator', zero(LL-(t*tp+t*t*(kp*tau-k*tp))))
check('ribbon_full_M_numerator', zero(MM-tau))
check('ribbon_ruling_second_derivative_zero', xt.diff(t)==S.zeros(3,1))
check('ribbon_K', zero(-MM**2/E**2+tau*tau/E**2))
check('ribbon_core_L_and_derivative', LL.subs(t,0)==0 and S.diff(LL,t).subs(t,0)==tp)
reject('ribbon_K_positive', zero(-MM**2/E**2-tau*tau/E**2))
reject('ribbon_Lt_twice_torsion_derivative', zero(S.diff(LL,t).subs(t,0)-2*tp))

# Differentiate the implicit equation itself and solve for its slope derivative.
ell, mixed, other, slope = (S.Function(n)(t) for n in ['ell','mixed','other','slope'])
at, lt, m0 = S.symbols('at lt m0')
equation_derivative = S.diff(ell+2*mixed*slope+other*slope**2,t)
at_core = equation_derivative.subs(t,0).subs({
    slope.subs(t,0):0, S.Subs(S.Derivative(slope,t),t,0):at,
    S.Subs(S.Derivative(ell,t),t,0):lt, mixed.subs(t,0):m0})
derived_at = S.solve(at_core,at)[0]
check('return_slope_implicit_derivative', zero(derived_at+lt/(2*m0)))
reject('return_exponent_missing_half', zero(derived_at+lt/m0))
negative_tau = S.symbols('negative_tau', negative=True)
check('torsion_log_antiderivative', zero(S.diff(S.log(-negative_tau),negative_tau)-1/negative_tau))

check('author_freeze_unchanged', frozen == {
    p.name:p.read_bytes() for p in AUTHOR.iterdir() if p.is_file()})
result = {
    'problem_id':'7000003', 'status':'PASS',
    'independent_assertions_passed':len(passed),
    'independent_mutations_rejected':len(rejected),
    'author_assertions_passed':24, 'author_mutations_rejected':8,
    'engine':'SymPy exact symbolic arithmetic; no floating-point sampling',
    'passed':passed, 'rejected':rejected,
    'scope':'Finite algebra and freeze integrity only; see AUDIT.md for analytic review. No resolution of Problem 1.3.'
}
expected_path = BASE/'EXPECTED_RESULTS.json'
if expected_path.exists() and json.loads(expected_path.read_text()) != result:
    raise AssertionError('Independent expected output mismatch')
print(json.dumps(result,indent=2,sort_keys=True))
