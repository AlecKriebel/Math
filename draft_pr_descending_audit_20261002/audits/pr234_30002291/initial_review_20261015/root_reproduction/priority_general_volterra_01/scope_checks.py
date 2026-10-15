#!/usr/bin/env python3
"""Reproduce scope diagnostics, not a proof or simulation of the candidate theorem."""
from fractions import Fraction
import json
from math import isclose

# In the general-functional source, q is auxiliary smoothness/vanishing order.
# It is distinct from the statistic's quadratic exponent.
checks = []
for alpha in [Fraction(1,100), Fraction(1,4), Fraction(49,100), Fraction(4999,10000)]:
    for beta in [Fraction(0), Fraction(1), Fraction(19,10), Fraction(19999,10000)]:
        lower = max(beta, 1/(1-alpha))
        q = (2+lower)/2
        assert beta < q < 2
        assert 1 < q < 2
        assert alpha < 1-1/q
        assert int(q) == 1
        checks.append({'alpha': str(alpha), 'beta': str(beta), 'q': str(q)})

# The series equality is termwise after U' = 1-U, l_old = l_new-1.
def h(x,a): return max(x,0)**a-max(x-1,0)**a
max_error = 0.0
for a in [.01,.25,.49]:
    for u in [0,.1,.5,.9,1]:
        left = sum(h(l-u,a)**2 for l in range(1,10001))
        right = sum(h(j+(1-u),a)**2 for j in range(10000))
        max_error = max(max_error,abs(left-right))
        assert isclose(left,right,rel_tol=1e-12,abs_tol=1e-12)

# Symmetric index-2 boundary measure: substituting z=e^-v gives
# integral z^2 nu(dz)=2*integral_1^infty v^-2 dv=2.
# For r<2, the same substitution gives 2*integral_1^infty
# exp((2-r)*v)/v^2 dv=infinity. No index strictly below 2 bounds this measure.
result = {
  'auxiliary_parameter_checks':len(checks),
  'auxiliary_parameter_examples':checks,
  'finite_series_reindex_max_abs_error':max_error,
  'series_check_scope':'Only indexing agreement; infinite-series convergence is not being tested.',
  'index_2_boundary':'Exact substitution recorded in source comments; finite quadratic rate 2, all lower power rates diverge.',
  'nonimplication':'A theorem requiring beta<2 does not cover this boundary by direct substitution.',
  'not_tested':'No candidate proof validation, stochastic convergence simulation, or novelty claim.'
}
print(json.dumps(result,indent=2))
