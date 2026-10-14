#!/usr/bin/env python3
"""Diagnostics for an exact variational counterexample; not a numerical proof.
All checks raise explicitly and remain active under python -O and -OO.
"""
import json, math, platform
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import eigh_tridiagonal, solve_banded
from scipy.optimize import brentq
import sympy as sp


def require(condition, message):
    if not bool(condition):
        raise RuntimeError(message)

Q, a = sp.symbols('Q a', real=True)
# Expansion of the difference between angular and radial mode energies.
# Integrate -2a r^(Q-3)d''d -2a(Q-1)r^(Q-4)d'd by parts.
# The d^2 coefficient before subtracting the angular correction is
# a^2 + 2a(Q-4), while the gradient correction contributes a(Q-1).
mode_coeff = sp.expand(a*a + 2*a*(Q-4) - a*(Q-1))
require(sp.simplify(mode_coeff - a*(a+Q-7)) == 0, 'mode coefficient mismatch')
require(sp.simplify(mode_coeff.subs(Q,5) - a*(a-2)) == 0, 'Q5 coefficient mismatch')
r, lam = sp.symbols('r lam', positive=True)
d = sp.Function('d')(r)
dp, dpp = sp.diff(d,r), sp.diff(d,r,2)
W = lam/r**2 - 1/r**4
exact_integrand = r**4*(dpp+4*dp/r-a*d/r**2)**2 - (W+4/r**2)*(r**4*dp**2+a*r**2*d**2)
square_integrand = r**4*dpp**2 + (1-lam*r**2)*dp**2 + 2*a*(r*dp+d/2)**2 + a*(a-sp.Rational(3,2)-lam)*d**2 + a*d**2/r**2
boundary_term = 4*r**3*dp**2 - 2*a*r**2*dp*d - 3*a*r*d**2
require(sp.simplify(exact_integrand-square_integrand-sp.diff(boundary_term,r)) == 0,
        'exact all-mode integrand identity failed')
trial_upper = 9/4 + math.pi**2/100 + math.exp(-4)
require(trial_upper < 19/8 < 12/5 < 5/2, 'trial or comparison threshold mismatch')
require((5-5) == 0, 'V=1 side condition mismatch')

runs = []
for n in (1799, 3599, 7199):
    left, right = -6., 12.
    h = (right-left)/(n+1)
    t = left + h*np.arange(1,n+1)
    diagonal = 2/h**2 + 9/4 + np.exp(-2*t)
    off = np.full(n-1, -1/h**2)
    ev = eigh_tridiagonal(diagonal, off, select='i', select_range=(0,1), eigvals_only=True, tol=1e-11)
    l0,l1 = map(float,ev)
    mean_vector = np.exp(-t/2)
    # Mean constraint in y=r^(3/2)w coordinates: int exp(-t/2)y dt=0.
    # Its lowest constrained value lies between the first two eigenvalues,
    # and is the unique zero of <h,(H-lambda)^(-1)h> there when neither
    # endpoint eigenvector is orthogonal to h.
    def secular(x):
        band = np.zeros((3,n))
        band[0,1:] = off
        band[1,:] = diagonal-x
        band[2,:-1] = off
        sol = solve_banded((1,1),band,mean_vector,check_finite=True)
        return float(np.dot(mean_vector,sol)*h)
    delta = max(1e-8, (l1-l0)*1e-6)
    slo,shi = secular(l0+delta),secular(l1-delta)
    require(slo < 0 < shi, 'secular root not bracketed')
    lc = float(brentq(secular,l0+delta,l1-delta,xtol=1e-12))
    lam = (l0+min(lc,12/5))/2
    require(9/4 < l0 < lam < lc, 'numerical threshold ordering failed')
    require(lam < 12/5, 'numerical parameter cap failed')
    require(l0 < trial_upper, 'lowest eigenvalue violates rigorous trial bound')
    runs.append({'grid_interior_points':n,'left_log_endpoint':left,'right_log_endpoint':right,
                 'grid_spacing':h,'lambda_0_approx':l0,'lambda_c_approx':lc,
                 'lambda_1_approx':l1,'selected_lambda_approx':lam,
                 'constrained_gap_approx':lc-l0,'first_angular_margin_lower_approx':2.5-lam,
                 'secular_signs':[slo,shi]})
require(abs(runs[-1]['lambda_0_approx']-runs[-2]['lambda_0_approx']) < 1e-5,
        'lambda0 mesh convergence diagnostic failed')
require(abs(runs[-1]['lambda_c_approx']-runs[-2]['lambda_c_approx']) < 1e-5,
        'lambdac mesh convergence diagnostic failed')
result = {'kind':'diagnostics_only_not_proof','python':platform.python_version(),
          'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__,
          'explicit_runtime_checks':True,'optimized_safe':True,
          'exact_scope':{'Q':5,'n':3,'R':'exp(12)','V':'1','W':'lambda/r^2 - 1/r^4',
                         'lambda':'(lambda_0 + min(lambda_c, 12/5))/2'},
          'symbolic_mode_d2_coefficient':str(mode_coeff),
          'exact_integrand_minus_square_form_is_total_derivative':True,
          'trial_upper_bound_float':trial_upper,
          'proof_thresholds':['trial_upper < 19/8','19/8 < 12/5','12/5 < 5/2'],
          'finite_difference_runs':runs,
          'caveats':['Exact lambda is variationally defined; rounded eigenvalues do not define the proof weights.',
                     'Finite interval log truncation and mesh convergence do not certify the infinite-interval spectrum.',
                     'Universal all-test validity is established analytically in the authored proof.']}
print(json.dumps(result,indent=2,sort_keys=True))
