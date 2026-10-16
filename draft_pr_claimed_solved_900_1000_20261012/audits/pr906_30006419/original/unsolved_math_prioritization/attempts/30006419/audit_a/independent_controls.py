#!/usr/bin/env python3
"""Independent finite controls; not a formal verification of analytic claims."""
from pathlib import Path
import hashlib, json, math
import numpy as np
import sympy as sp
from scipy.integrate import quad
out = {'scope': 'Independent algebraic and numerical controls; analytic proof audited separately.', 'controls': {}}
C = out['controls']

def B(x):
    return 0.0 if x <= 0 else math.exp(-1.0 / x)

def H(x):
    return B(x) / (B(x) + B(1 - x))

def eta(t):
    return 1 - H((16 * t * t - 1) / 3)

def a(t):
    return eta(t) * t * t + 1 - eta(t)

def rho(s):
    r = abs(s)
    return math.exp(-r * H(r - 2))
c = quad(lambda t: 1 - a(t), 0, 0.5, points=[0.25], epsabs=1e-13, epsrel=1e-13)[0]

def h(t):
    if t < 0:
        return -h(-t)
    if t >= 0.5:
        return t - c
    return quad(a, 0, t, points=[0.25] if t > 0.25 else None, epsabs=1e-13)[0]
mesh = np.linspace(-4, 4, 16001)
if not all((0 <= a(float(t)) <= 1 for t in mesh)):
    raise RuntimeError('Independent control failed at original line 29')
if not all((abs(a(float(t)) - float(t * t)) < 1e-14 for t in mesh if abs(t) <= 0.25)):
    raise RuntimeError('Independent control failed at original line 30')
if not all((a(float(t)) == 1 for t in mesh if abs(t) >= 0.5)):
    raise RuntimeError('Independent control failed at original line 31')
if not 0 < c < 0.5:
    raise RuntimeError('Independent control failed at original line 32')
area = 4 * math.pi * (quad(lambda s: rho(s) ** 2, 0, 3, points=[2], epsabs=1e-11)[0] + math.exp(-6) / 2)
energy = 4 * math.pi * (quad(lambda t: rho(h(t)) ** 2, 0, 3 + c, points=[0.5, 2 + c], epsabs=1e-10)[0] + math.exp(-6) / 2)
if not abs(energy - area - 4 * math.pi * c) < 1e-08:
    raise RuntimeError('Independent control failed at original line 35')
C['global_geometry'] = {'c': c, 'target_area': area, 'map_E_plus': energy, 'energy_excess': energy - area, 'expected_excess': 4 * math.pi * c, 'sampled_cutoff_points': len(mesh)}
A, m = sp.symbols('A m', positive=True)
b = m / (A - m)
if not sp.simplify((1 + b) * m - b * A) == 0:
    raise RuntimeError('Independent control failed at original line 41')
C['exact_calibration_zero_integral'] = True
bands = []
for Q in [1, 10, 1000.0, 1000000.0, 1000000000000.0]:
    d = min(0.25, 0.5 / math.sqrt(Q))
    if not (1 / d ** 2 > Q and 4 * math.pi * math.tanh(d) > 0):
        raise RuntimeError('Independent control failed at original line 46')
    bands.append({'Q': Q, 'half_width': d, 'round_area': 4 * math.pi * math.tanh(d), 'ratio_lower_bound': 1 / d ** 2})
C['positive_area_distortion_bands'] = bands
t, x = sp.symbols('t x', real=True)
l, r, w = (sp.Rational(1, 8), sp.Rational(3, 16), sp.Rational(1, 5))
psi = (t - l) ** 2 * (r - t) ** 2 * (w * w - x * x) ** 2
integ = lambda expr: sp.integrate(expr, (t, l, r), (x, -w, w))
d1 = sp.factor(integ(2 * t * t * sp.diff(psi, t)))
d1_parts = sp.factor(integ(-4 * t * psi))
d2 = sp.factor(integ(sp.diff(psi, t) ** 2 + sp.diff(psi, x) ** 2))
if not (d1 == d1_parts and d1 < 0 and (d2 > 0)):
    raise RuntimeError('Independent control failed at original line 58')
epsilon = -d1 / (2 * d2)
delta = sp.factor(epsilon * d1 + epsilon ** 2 * d2)
variation_image_bound = r ** 3 / 3 + epsilon * (r - l) ** 4 * w ** 4 / 16
if not variation_image_bound < 2:
    raise RuntimeError('KS test variation leaves flat belt')
if not delta < 0:
    raise RuntimeError('Independent control failed at original line 61')
C['KS_lowering_variation'] = {'first_derivative_exact': str(d1), 'second_order_coefficient_exact': str(d2), 'epsilon': float(epsilon), 'energy_change_exact': str(delta), 'energy_change': float(delta), 'same_trace': True, 'first_coordinate_upper_bound': float(variation_image_bound)}
nodes, weights = np.polynomial.legendre.leggauss(90)
tt = (nodes + 1) * (float(r - l) / 2) + float(l)
xx = nodes * float(w)
T, X = np.meshgrid(tt, xx, indexing='ij')
WT, WX = np.meshgrid(weights * float(r - l) / 2, weights * float(w), indexing='ij')
p = (t - l) * (r - t) / (r - l) ** 2 * (1 - x * x / (w * w))
p_t = sp.lambdify((t, x), sp.diff(p, t), 'numpy')
p_x = sp.lambdify((t, x), sp.diff(p, x), 'numpy')
P_t, P_x = (p_t(T, X), p_x(T, X))
base = float((r - l) * 2 * w)
perturbations = []
for amp1, amp2 in [(0, 0), (0.001, 0), (0, 0.001), (0.005, -0.002), (-0.004, 0.003), (0.02, 0.02)]:
    aa = T * T + amp1 * P_t
    bb = amp1 * P_x
    cc = amp2 * P_t
    dd = 1 + amp2 * P_x
    tr = aa * aa + bb * bb + cc * cc + dd * dd
    det = (aa * dd - bb * cc) ** 2
    norm2 = 0.5 * (tr + np.sqrt(np.maximum(0, tr * tr - 4 * det)))
    e = float(np.sum(norm2 * WT * WX))
    scalar = float(np.sum((cc * cc + dd * dd) * WT * WX))
    if not (e >= scalar - 1e-12 and scalar >= base - 1e-12):
        raise RuntimeError('Independent control failed at original line 84')
    perturbations.append({'amplitudes': [amp1, amp2], 'E_plus': e, 'scalar_energy': scalar, 'baseline_area': base})
C['flat_belt_scalar_controls'] = perturbations
phi = np.arange(262144) * (2 * math.pi / 262144)
V = np.stack((np.cos(phi), np.sin(phi)), axis=1)
Bmat = np.array([[0.31, 0.22], [-0.17, -0.12]])
Amat = np.array([[1.3, 0.2], [-0.1, 0.9]])
if not np.linalg.det(Amat) > 0:
    raise RuntimeError('Independent control failed at original line 93')
norms = {'euclidean': lambda z: np.linalg.norm(z, axis=1), 'linfty': lambda z: np.max(abs(z), axis=1), 'l1': lambda z: np.sum(abs(z), axis=1), 'rank_one': lambda z: abs(z[:, 0]), 'anisotropic': lambda z: np.linalg.norm(z * np.array([1, 0.1]), axis=1)}

def energy(norm, mat):
    return 2 * np.mean(norm(V @ mat.T) ** 2) / np.linalg.det(mat)

def stress(norm):
    sq = norm(V) ** 2
    return 2 * np.mean(sq[:, None, None] * (4 * V[:, :, None] * V[:, None, :] - 2 * np.eye(2)), axis=0)
ks = {}
for name, norm in norms.items():
    sv = norm(V) ** 2
    transformed = 2 * np.mean(sv / np.linalg.norm(V @ np.linalg.inv(Amat).T, axis=1) ** 4) / np.linalg.det(Amat) ** 2
    direct = energy(norm, Amat)
    S = stress(norm)
    eps = 1e-05
    fd = (energy(norm, np.eye(2) + eps * Bmat) - energy(norm, np.eye(2) - eps * Bmat)) / (2 * eps)
    deriv = float(np.sum(S * Bmat))
    if not abs(transformed - direct) < 2e-08:
        raise RuntimeError('Independent control failed at original line 109')
    if not abs(fd - deriv) < 2e-05:
        raise RuntimeError('Independent control failed at original line 110')
    ks[name] = {'angular_formula_abs_error': abs(transformed - direct), 'variation_abs_error': abs(fd - deriv), 'stress': S.tolist()}
if not np.max(abs(stress(norms['rank_one']) - np.diag([1.0, -1.0]))) < 1e-10:
    raise RuntimeError('Independent control failed at original line 112')
if not np.max(abs(stress(norms['linfty']))) < 1e-10:
    raise RuntimeError('Independent control failed at original line 113')
if not np.max(abs(stress(norms['l1']))) < 1e-10:
    raise RuntimeError('Independent control failed at original line 114')
if not abs((4 + math.sqrt(17)) * (math.sqrt(17) - 4) - 1) < 1e-13:
    raise RuntimeError('Independent control failed at original line 115')
C['KS_angular_and_stress_controls'] = ks
C['KS_nonround_balanced_negative_control'] = 'Both l1 and linfty stress vanish; zero stress cannot imply roundness.'
C['KS_nonzero_rank_one_negative_control'] = 'Rank-one stress is diag(1,-1); degeneracy is excluded by balance.'
out['result'] = 'PASS'
path = Path(__file__).with_name('INDEPENDENT_CONTROL_RESULTS.json')
path.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
