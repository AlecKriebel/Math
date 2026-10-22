#!/usr/bin/env python3
"""Independent algebra and integrity controls for the frozen partial report.

Runs entirely locally and leaves the frozen inputs untouched. Exact assertions,
high-precision numerical checks, and deliberate invalid-model controls are
separated. None is a continuum approximation certificate.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import mpmath as mp
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED_MANIFEST = '19cf0e95e43fd4fb82ce6debdc99e98aeb7ff288b4e26decd8f955bce9e43004'
exact, numerical, negative = [], [], []


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def check(name, truth):
    assert bool(truth), name
    exact.append(name)


def reject(name, truth):
    assert bool(truth), name
    negative.append(name)


def integrity():
    manifest_path = ROOT / 'audit/FROZEN_INPUTS.json'
    assert sha(manifest_path) == EXPECTED_MANIFEST, 'Manifest mismatch'
    manifest = json.loads(manifest_path.read_text())
    rows = []
    for entry in manifest['files']:
        p = ROOT / entry['path']
        assert p.stat().st_size == entry['bytes'], entry['path']
        assert sha(p) == entry['sha256'], entry['path']
        rows.append({'path': entry['path'], 'sha256': sha(p), 'matched': True})
    return rows


integrity_before = integrity()
# Replay the reviewed author program from an isolated temporary copy: its
# __file__-relative results output cannot overwrite the frozen results.
with tempfile.TemporaryDirectory(prefix='modular-audit-replay-') as tmp:
    copy = Path(tmp) / 'verify_exact.py'
    shutil.copyfile(ROOT / 'verification/verify_exact.py', copy)
    process = subprocess.run([sys.executable, str(copy)], capture_output=True, text=True)
    assert process.returncode == 0, process.stderr
    replay = json.loads((Path(tmp) / 'results.json').read_text())
    frozen_replay = json.loads((ROOT / 'verification/results.json').read_text())
    assert replay == frozen_replay, 'Author replay differs from frozen output'
    author_replay = {
        'verdict': replay['verdict'],
        'exact_check_count': replay['exact_check_count'],
        'numerical_replay_count': len(replay['numerical_replays']),
        'negative_control_count': len(replay['negative_controls']),
        'output_matches_frozen_result': True,
        'script_sha256': replay['script_sha256'],
    }

# 1. Independent operator-level Fourier test, including the differential side.
# q=R^2-|x|^2 transforms to R^2+Delta_p. General unnamed test functions ensure
# that no special Gaussian or polynomial test can hide an omitted derivative.
m, R = s.symbols('m R', positive=True)
for dim in (1, 2, 3):
    p = s.symbols(f'p0:{dim}', real=True)
    rr = sum(z*z for z in p)
    w = s.sqrt(rr+m*m)
    f = s.Function('f')(*p)
    def Q(g):
        return R*R*g + sum(s.diff(g, z, 2) for z in p)
    full = w*Q(w*f)
    local = sum(z*Q(z*f) for z in p)+m*m*Q(f)
    residual = s.simplify(s.expand(full-local))
    expected = (dim-1+m*m/(rr+m*m))*f
    check(f'full_fourier_operator_identity_n{dim}', s.simplify(residual-expected) == 0)
    reject(f'wrong_yukawa_sign_n{dim}', s.simplify(residual-(dim-1-m*m/(rr+m*m))*f) != 0)
    if dim > 1:
        reject(f'missing_constant_n{dim}', s.simplify(residual-m*m*f/(rr+m*m)) != 0)

# A dimension-symbolic double-commutator derivation gives the general n proof:
# 1/2{A,q} = -div(q grad)+m^2 q+n and
# [w,[w,q]] = 2|grad_p w|^2 = 2r^2/(r^2+m^2).
n, rho = s.symbols('n rho', positive=True)
check('dimension_symbolic_double_commutator_residual',
      s.simplify(n-rho/(rho+m*m)-(n-1+m*m/(rho+m*m))) == 0)
# Wrong Fourier sign for x^2 must already fail the n=1 constant test.
p = s.symbols('p', real=True)
w = s.sqrt(p*p+m*m)
reject('wrong_fourier_x_squared_sign', s.simplify(w*(w-s.diff(w,p,2))-(w*(w+s.diff(w,p,2)))) != 0)

# 2. Exact finite standardness and modular operator, derived from Tomita's
# defining real-linear involution instead of assuming the arcoth formula.
a, b = s.symbols('a b', positive=True)
T = s.Matrix([[a+b,a-b],[a-b,a+b]])/2
E = T.inv()
chi = s.diag(1,0)
J = s.zeros(4)
J[:2,2:] = s.eye(2)
J[2:,:2] = -s.eye(2)
W = s.zeros(4,2)
W[:2,0] = T[:,0]
W[2:,1] = E[:,0]
V = W.row_join(J*W)
check('tomita_decomposition_determinant', s.factor(V.det()-(a*a-b*b)**2/(4*a*a*b*b)) == 0)
check('factorial_symplectic_restriction', s.simplify(W.T*J*W) == s.Matrix([[0,1],[-1,0]]))
S = s.simplify(V*s.diag(1,1,-1,-1)*V.inv())
check('tomita_involution', s.simplify(S*S) == s.eye(4))
check('tomita_antilinearity', s.simplify(S*J+J*S) == s.zeros(4))
check('tomita_fixes_local_real_subspace', s.simplify(S*W-W) == s.zeros(4,2))
Delta = s.simplify(S.T*S)
d = (a-b)**2/(a+b)**2
check('modular_operator_from_tomita', s.simplify(Delta-s.diag(d,1/d,d,1/d)) == s.zeros(4))
B = s.simplify(T*chi*E+E*chi*T-s.eye(2))
Bexpected = (a*a+b*b)/(2*a*b)*s.diag(1,-1)
check('arcoth_argument_general_parameters', s.simplify(B-Bexpected) == s.zeros(2))
check('delta_arcoth_log_relation', s.simplify((B[0,0]-1)/(B[0,0]+1)-d) == 0)
L = s.symbols('L', real=True)  # L=log((b+a)/(b-a)) for 0<a<b
logDelta = s.diag(-2*L,2*L,-2*L,2*L)
U = s.diag(T,E)
K = s.simplify(U.inv()*(-J*logDelta)*U)
Mminus = 2*L/(a*b)*s.diag(1,-1)
check('tomita_Mminus_normalization_and_sign', s.simplify(K[:2,2:]-Mminus) == s.zeros(2))
check('tomita_Mplus_conjugation', s.simplify(-K[2:,:2]-T*T*Mminus*T*T) == s.zeros(2))
check('time_zero_complex_linearity', s.simplify(K*(U.inv()*J*U)-(U.inv()*J*U)*K) == s.zeros(4))
reject('degenerate_equal_eigenvalues_not_standard', s.factor(V.det()).subs(b,a) == 0)
reject('degenerate_arcoth_endpoint_rejected', B[0,0].subs(b,a) == 1)
reject('wrong_modular_generator_sign', s.simplify((-K[:2,2:])-Mminus) != s.zeros(2))

# Four-coordinate position algebra, checked by a commutator rather than only
# reading the nonzero off-diagonal entry.
c1,c2 = s.log(3),s.log(7)/6
inside = s.Matrix([[c1+c2,c1-c2],[c1-c2,c1+c2]])/2
coordinate_projection = s.diag(1,0)
comm = inside*coordinate_projection-coordinate_projection*inside
check('four_point_nondiagonal_commutator', comm[0,1] == -(c1-c2)/2)
check('strict_log_inequality_integer_certificate', 3**6 > 7)
# alpha/beta asymptotics imply a nonconstant positive coefficient.
x = s.symbols('x',positive=True)
check('mass_shift_asymptotic_decay', s.limit(s.log(x)/s.sqrt(x),x,s.oo) == 0)
check('dimensionless_mass_radius_scaling', s.simplify(((R**-2)**s.Rational(-1,4))**2-R) == 0)

# 3. Endpoint, noncommuting spectral calculus, and heat-kernel controls.
mp.mp.dps = 70

def mm(X):
    return mp.matrix([[mp.mpf(str(s.N(X[i,j],80))) for j in range(X.cols)] for i in range(X.rows)])

def spectral(X,fn):
    vals,Q = mp.eigsy(X)
    return Q*mp.diag([fn(v) for v in vals])*Q.T

def maxentry(X):
    return max(abs(X[i,j]) for i in range(X.rows) for j in range(X.cols))

def arcoth(v):
    assert abs(v)>1
    return mp.log((v+1)/(v-1))/2

def numcheck(name,error,threshold,**metadata):
    assert error < mp.mpf(threshold), (name, str(error))
    numerical.append({'name':name,'error':mp.nstr(error,15),'threshold':threshold,**metadata})

# Non-special rational orthogonal mixing; this is independent of the report's
# two 45-degree blocks and tests functional calculus on non-diagonal B.
Z = s.Matrix([[0,1,2,0],[-1,0,1,1],[-2,-1,0,2],[0,-1,-2,0]])
O = (s.eye(4)-Z)*(s.eye(4)+Z).inv()
check('independent_rational_mixing_orthogonal', O.T*O == s.eye(4))
A0 = mm(O*s.diag(1,4,9,16)*O.T)
Ch = mp.diag([1,1,0,0])
Jn = mp.zeros(8)
for k in range(4):
    Jn[k,k+4]=1
    Jn[k+4,k]=-1

def finite(lam):
    A=A0+lam*mp.eye(4)
    T=spectral(A,lambda v:v**mp.mpf('.25'))
    E=T**-1
    C=T*Ch*E
    B=C+C.T-mp.eye(4)
    F=spectral(B,arcoth)
    M=2*E*F*E
    return A,T,E,C,B,F,M

for lam in (mp.mpf('.5'),mp.mpf('2')):
    A,T,E,C,B,F,M=finite(lam)
    Wn=mp.zeros(8,4)
    for row in range(4):
        for col in range(2):
            Wn[row,col]=T[row,col]
            Wn[row+4,col+2]=E[row,col]
    JW=Jn*Wn
    Vn=mp.zeros(8)
    for row in range(8):
        for col in range(4):
            Vn[row,col]=Wn[row,col]
            Vn[row,col+4]=JW[row,col]
    Sn=Vn*mp.diag([1]*4+[-1]*4)*(Vn**-1)
    Dn=Sn.T*Sn
    logDn=spectral(Dn,mp.log)
    target=mp.zeros(8)
    for row in range(4):
        for col in range(4):
            target[row,col]=-2*F[row,col]
            target[row+4,col+4]=-2*F[row,col]
    numcheck('non_special_tomita_vs_arcoth',maxentry(logDn-target),'1e-60',scalar_shift=str(lam))

# Integral Frechet derivative with the correct outside factors, independently
# evaluated and compared with mpmath's numerical differentiation of the matrix.
lam=mp.mpf('.5')
A,T,E,C,B,F,M=finite(lam)
Ai=A**-1
Bp=(Ai*(C-C.T)-(C-C.T)*Ai)/4

def derivative_integrand(t):
    Rm=(B-t*mp.eye(4))**-1
    Rp=(B+t*mp.eye(4))**-1
    return -(Rm*Bp*Rm+Rp*Bp*Rp)/2
DF=mp.matrix([[mp.quad(lambda t:derivative_integrand(t)[i,j],[0,1]) for j in range(4)] for i in range(4)])
expected_derivative=-(Ai*M+M*Ai)/4+2*E*DF*E
actual_derivative=mp.matrix([[mp.diff(lambda t:finite(t)[-1][i,j],lam) for j in range(4)] for i in range(4)])
numcheck('resolvent_integral_mass_derivative',maxentry(expected_derivative-actual_derivative),'1e-55')
reject('outside_derivative_factors_cannot_be_omitted',maxentry(2*E*DF*E-actual_derivative)>mp.mpf('1e-4'))

for dim,z in ((1,mp.mpf('2.4')),(3,mp.mpf('.7'))):
    mass=mp.mpf('1.3')
    kernel=mp.quad(lambda t:mp.exp(-mass*mass*t-z*z/(4*t))/(4*mp.pi*t)**(mp.mpf(dim)/2),[0,1,mp.inf])
    known=mp.exp(-mass*z)/(2*mass) if dim==1 else mp.exp(-mass*z)/(4*mp.pi*z)
    numcheck(f'heat_kernel_normalization_n{dim}',abs(kernel-known),'1e-60')
    assert kernel>0

# A genuinely too-small Lipschitz constant fails even in a scalar model.
# The valid sharper 1/(a^2-1) bound follows separately from the inverse-power
# series; it is not falsely labeled an invalid two-sided-spectrum estimate.
a_gap=mp.mpf('2')
h=mp.mpf('1e-8')
ratio=abs(arcoth(a_gap+h)-arcoth(a_gap))/h
reject('undersized_gap_lipschitz_constant',ratio>mp.mpf(1)/4)
z=s.symbols('z',positive=True)
check('inverse_power_series_sharp_gap_constant',s.simplify(z**-2/(1-z**-2)-1/(z*z-1))==0)

eps, gap=s.symbols('eps gap',positive=True)
endpoint=s.log(2*(2+eps)/(2+2*eps))/2
check('endpoint_difference_has_nonzero_limit',s.limit(endpoint,eps,0)==s.log(2)/2)
check('gap_resolvent_integral',s.simplify(1/(gap-1)-1/gap-1/(gap*(gap-1)))==0)

integrity_after=integrity()
assert integrity_after==integrity_before
result={
    'verdict':'PASS_PARTIAL',
    'scope':'Independent exact algebra, finite-model tests, and analytical audit only. Neither continuum source question is solved.',
    'frozen_manifest_sha256':EXPECTED_MANIFEST,
    'frozen_files_unchanged':True,
    'frozen_file_count':len(integrity_before),
    'author_replay':author_replay,
    'independent_exact_checks':exact,
    'independent_exact_count':len(exact),
    'independent_numerical_checks':numerical,
    'independent_negative_controls':negative,
    'independent_negative_count':len(negative),
    'versions':{'python':sys.version.split()[0],'sympy':s.__version__,'mpmath':mp.__version__,'mpmath_digits':mp.mp.dps},
    'audit_script_sha256':sha(Path(__file__)),
}
(HERE/'control_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
