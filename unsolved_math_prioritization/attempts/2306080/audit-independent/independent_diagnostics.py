#!/usr/bin/env python3
"""Independent finite diagnostics, not a proof of univalence or nonnormality.
Run with Python 3 and mpmath. All analytic conclusions require AUDIT.md.
"""
import json
from fractions import Fraction as Q
import mpmath as mp

bq, cq = Q(1, 100), Q(1, 10)
q = Q(11, 100) + cq * Q(1, 8) / (1 - Q(1, 8))
assert q == Q(87, 700)
# For |B-1| <= q, Re(1/B) >= 1/(1+q). Thus every nonzero
# exponential collision would have |Im(w2-w1)| / pi >= 2/(1+q) > 1.
reciprocal_real_lower = 1 / (1 + q)
collision_height_ratio = 2 * reciprocal_real_lower
assert collision_height_ratio == Q(1400, 787) > 1
# Exact normalization coefficient, calculated without complex floats.
dr = bq + bq*bq - cq*cq - bq*(1+bq)
di = cq + 2*bq*cq
assert (dr, di) == (Q(-1, 100), Q(51, 500))

with mp.workdps(1000):
    b, c = mp.mpf(1)/100, mp.mpf(1)/10
    a = b + mp.j*c
    d = a*(1+a)-b*(1+b)
    rows = []
    for n in (1, 2, 5, 10, 20):
        t = mp.exp(-20*mp.pi*n)
        z = 1-t
        assert 0 < z < 1
        # Direct formulas from the original z plane, deliberately not
        # replacing F(z) with its exact known zero or using just a t formula.
        ell = mp.log(1-z)
        F = mp.exp(-a*ell)-mp.exp(-b*ell)
        f = a*mp.exp(-(1+a)*ell)-b*mp.exp(-(1+b)*ell)
        weighted = (1-z*z)*abs(f)/(1+abs(F)**2)
        expected = c*(2-t)*mp.exp(mp.pi*n/5)
        rel = abs(weighted/expected-1)
        H = (F-mp.j*c*z)/d
        Hp = (f-mp.j*c)/d
        weighted_H = (1-z*z)*abs(Hp)/(1+abs(H)**2)
        assert abs(F) < mp.mpf('1e-400')
        assert rel < mp.mpf('1e-400')
        rows.append({'n': n,
                     'direct_F_absolute_residual': mp.nstr(abs(F), 12),
                     'direct_normality_quantity': mp.nstr(weighted, 15),
                     'closed_form_relative_error': mp.nstr(rel, 12),
                     'normalized_H_normality_quantity': mp.nstr(weighted_H, 15)})
    print(json.dumps({'certification': 'Exact rational identities plus 1000-decimal finite diagnostics; not interval-certified or universal proof.',
                      'mpmath_version': mp.__version__,
                      'exact_collision_height_ratio_lower_bound': str(collision_height_ratio),
                      'exact_normalization_d': [str(dr), str(di)],
                      'direct_radial_samples': rows,
                      'all_tests_pass': True}, indent=2))
