"""Floating-point diagnostics, explicitly separate from the exact/proof checks.

Evaluates the ideal-model mean via the exact Beta marginal formula. Requires
pre-existing NumPy/SciPy; no package is installed by this script.
"""
import json
import numpy as np
import scipy
from scipy.special import zeta, betainc

N = 12000
j = np.arange(1, N+1, dtype=float)
a = zeta(2*j, 1)/(2*j)
h = np.ones(N+1)
for n in range(1, N+1):
    h[n] = np.dot(j[:n]*a[:n], h[n-1::-1])/n
rows = []
for n in (300, 3000, 12000):
    g = n//3 + 1
    jj = j[:n-1]
    low, high = 1/np.sqrt(g), 2/np.sqrt(g)
    probs = betainc(2*jj, 2*n-2*jj, high)-betainc(2*jj, 2*n-2*jj, low)
    mean = np.dot(a[:n-1]*h[n-1:0:-1]/h[n], probs)
    rows.append({'n':n, 'g':g, 'ideal_window_mean':float(mean), 'h_n_sqrt_n':float(h[n]*np.sqrt(n))})
print(json.dumps({'scope':'Non-rigorous finite ideal-model diagnostics, not geometric data or asymptotic certification.', 'numpy':np.__version__, 'scipy':scipy.__version__, 'predicted_mean':float(np.log(2)/2), 'predicted_h_n_sqrt_n':float(np.sqrt(2/np.pi)), 'rows':rows}, indent=2, sort_keys=True))
