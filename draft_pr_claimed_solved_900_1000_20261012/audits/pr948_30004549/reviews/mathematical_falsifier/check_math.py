"""Independent exact algebra; does not import candidate or other audit code."""
import json
import sys
from itertools import combinations
import sympy as s


def add(*terms):
    out = {}
    for form in terms:
        for inds, coeff in form.items():
            out[inds] = out.get(inds, 0) + coeff
    return {inds: s.simplify(c) for inds, c in out.items() if s.simplify(c) != 0}


def scale(c, form):
    return add({inds: c * coeff for inds, coeff in form.items()})


def wedge(left, right):
    out = {}
    for a, ca in left.items():
        for b, cb in right.items():
            inds = a + b
            if len(set(inds)) != len(inds):
                continue
            sign = (-1) ** sum(inds[i] > inds[j] for i in range(len(inds)) for j in range(i + 1, len(inds)))
            key = tuple(sorted(inds))
            out[key] = out.get(key, 0) + sign * ca * cb
    return add(out)


def equal(actual, expected, label):
    if add(actual, scale(-1, expected)):
        raise RuntimeError(label + ': ' + repr(actual) + ' != ' + repr(expected))


def matrix(form):
    out = s.zeros(4)
    for (i, j), c in form.items():
        out[i, j], out[j, i] = c, -c
    return out


du, dv, dx, dt = [{(i,): s.Integer(1)} for i in range(4)]
vol = {(0, 1, 2, 3): s.Integer(1)}
ru, rv, rx, rt = s.symbols('R_u R_v R_x R_t', real=True)
alpha = add(wedge(du, dx), scale(-1, wedge(dv, dt)))
beta = add(wedge(du, dt), wedge(dv, dx))
delta = wedge(add(scale(ru, du), scale(rv, dv), scale(rx, dx), scale(rt, dt)), dv)
beta_e = add(beta, delta)
equal(wedge(alpha, alpha), scale(2, vol), 'alpha square')
equal(wedge(alpha, beta_e), scale(rt, vol), 'mixed wedge including all cutoff derivatives')
equal(wedge(beta_e, beta_e), scale(2 * (1 - rx), vol), 'beta square')
equal(wedge(du, alpha), wedge(dv, beta_e), 'third-form closure')
D = 1 - rx - rt ** 2 / 4
unnormalized_B = add(beta_e, scale(-rt / 2, alpha))
equal(wedge(alpha, unnormalized_B), {}, 'orthogonality')
equal(wedge(unnormalized_B, unnormalized_B), scale(2 * D, vol), 'normalization')
A = matrix(alpha)
Q = -A.inv() * matrix(unnormalized_B)
if (Q * Q + D * s.eye(4)).applyfunc(s.simplify) != s.zeros(4):
    raise RuntimeError('general cutoff real J square failed')
if (Q.T * A * Q + D * A).applyfunc(s.simplify) != s.zeros(4):
    raise RuntimeError('general alpha anti-invariance failed')
Be = matrix(beta_e)
if (Q.T * Be * Q + D * Be).applyfunc(s.simplify) != s.zeros(4):
    raise RuntimeError('general beta anti-invariance failed')

# Adversarial controls: three values cannot belong to a rank-two plane.
delta_control = scale(-s.Rational(1, 4), wedge(dv, dx))
beta_control = add(beta, delta_control)
wrong_gamma = add(alpha, scale(-1, beta), delta_control)
correct_gamma = add(alpha, scale(-1, beta_control))
keys = list(combinations(range(4), 2))
columns = lambda forms: s.Matrix([[f.get(key, 0) for f in forms] for key in keys])
if columns([alpha, beta_control, wrong_gamma]).rank() != 3:
    raise RuntimeError('wrong gamma sign was not rejected')
if columns([alpha, beta_control, correct_gamma]).rank() != 2:
    raise RuntimeError('correct gamma relation control failed')
# Replacing d(epsilon*rho*x^2*dv/2) by epsilon*rho*x*dx*dv
# drops cutoff derivatives; rho=u already makes its d nonzero.
equal(wedge(wedge(du, dx), dv), {(0, 1, 2): -1}, 'nonclosed omitted-cutoff control')

k = s.symbols('k', positive=True)
kp = s.symbols('k_prime', real=True)
phi1 = add(du, scale(s.I * s.sqrt(k), dv))
phi2 = add(dx, scale(s.I / s.sqrt(k), dt))
dphi1 = scale(s.I * kp / (2 * s.sqrt(k)), wedge(dx, dv))
equal(wedge(wedge(dphi1, phi1), phi2), scale(kp / (2 * k), vol), 'coframe obstruction sign')
equal(wedge(phi1, phi2), add(alpha, scale(s.I / s.sqrt(k), add(wedge(du, dt), scale(k, wedge(dv, dx))))), 'core factorization')

u, v, x, t, eps = s.symbols('u v x t epsilon', real=True)
coords = (u, v, x, t)
core_k = 1 - eps * x
J = s.zeros(4)
J[1, 0], J[0, 1] = core_k ** s.Rational(-1, 2), -s.sqrt(core_k)
J[3, 2], J[2, 3] = s.sqrt(core_k), -core_k ** s.Rational(-1, 2)


def bracket(X, Y):
    return s.Matrix([sum(X[j] * s.diff(Y[i], coords[j]) - Y[j] * s.diff(X[i], coords[j]) for j in range(4)) for i in range(4)])


basis = [s.eye(4)[:, i] for i in range(4)]
nonzero = {}
for i, j in combinations(range(4), 2):
    X, Y = basis[i], basis[j]
    N = bracket(J * X, J * Y) - J * bracket(J * X, Y) - J * bracket(X, J * Y) - bracket(X, Y)
    N = N.applyfunc(s.simplify)
    if N != s.zeros(4, 1):
        nonzero[str((i, j))] = [str(c) for c in N]
    expected = s.Matrix([-eps / (2 * core_k), 0, 0, 0])
    if (i, j) == (0, 2) and (N - expected).applyfunc(s.simplify) != s.zeros(4, 1):
        raise RuntimeError('Nijenhuis convention mismatch')

print(json.dumps({'status': 'PASS', 'python_optimized': not __debug__, 'sympy_version': s.__version__, 'general_cutoff_wedge_identities': True, 'general_real_J_square_and_two_anti_invariances': True, 'wrong_gamma_sign_rejected_by_rank_three': True, 'omitted_cutoff_derivative_rejected_by_nonclosure': True, 'coframe_sign': 'k_prime/(2*k)', 'Nijenhuis_all_six_pairs': nonzero, 'symbolic_support_limit': 'Finite exact algebra only; global geometric arguments are in INDEPENDENT_DERIVATION.md.'}, indent=2))
