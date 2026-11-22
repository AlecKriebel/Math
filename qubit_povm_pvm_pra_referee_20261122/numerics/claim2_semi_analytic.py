#!/usr/bin/env python3
"""Independent semi-analytic cross-check of the qubit PVM optimum of the 3x2 functional for support {0,2}:
maximise  10*(|R(b0+b1)| + |R(b0-b1)|) + F_eta  over eta in [0,1] and unit vectors b0,b1, using the paper's
closed form 20 F_eta = 7 + eta(3x+4y) + sqrt((-1+eta(3x-4y))^2 + 24(1-eta^2)(1-r))."""
import numpy as np
from scipy.optimize import minimize
rng = np.random.default_rng(5)
def unit(th, ph): return np.array([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)])
def f(p):
    eta = 0.5 * (1 + np.sin(p[0]))  # in [0,1]
    b0 = unit(p[1], p[2]); b1 = unit(p[3], p[4])
    s = np.sqrt(max(1 - eta * eta, 0)); R = np.diag([s, -s, 1.0])
    S = np.linalg.norm(R @ (b0 + b1)) + np.linalg.norm(R @ (b0 - b1))
    x, y, r = b0[2], b1[2], b0 @ b1
    F = (7 + eta * (3 * x + 4 * y) + np.sqrt((-1 + eta * (3 * x - 4 * y)) ** 2 + 24 * (1 - eta * eta) * (1 - r))) / 20
    return -(10 * S + F), eta, S, F, x, y, r
best = None
for i in range(300):
    p0 = np.concatenate([[rng.uniform(-np.pi / 2, np.pi / 2)], rng.uniform(0, np.pi, 1), rng.uniform(0, 2 * np.pi, 1), rng.uniform(0, np.pi, 1), rng.uniform(0, 2 * np.pi, 1)])
    r = minimize(lambda p: f(p)[0], p0, method='BFGS', options=dict(gtol=1e-12))
    r = minimize(lambda p: f(p)[0], r.x, method='Nelder-Mead', options=dict(xatol=1e-12, fatol=1e-15, maxiter=5000))
    if best is None or r.fun < best.fun: best = r
v, eta, S, F, x, y, rr = f(best.x)
print(f"semi-analytic PVM optimum (support {{0,2}}): {-v:.12f}   eta={eta:.8f}  S={S:.10f} (2sqrt2-S={2*np.sqrt(2)-S:.3e})  T=F_eta={F:.10f}  x={x:.6f} y={y:.6f} r=b0.b1={rr:.6f}")
print(f"   compare with see-saw / pattern / direct searches: 28.887740069934;  289/10 - value = {28.9+v:.9f}")
