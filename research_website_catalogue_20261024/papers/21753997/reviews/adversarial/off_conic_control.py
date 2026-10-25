"""Exact positivity of the isolated residual real point, using fresh ideals only.

This is a boundary/wording control, not a counterexample to the main theorems.
No numerical root finding is used to certify signs or zero-set membership.
"""
from pathlib import Path
from datetime import datetime, timezone
import json
import sympy as S

ROOT = Path(__file__).resolve().parent
x, y, z = S.symbols('x y z')

def mul(a, b):
    p = [a[i] * b[j] for i in (0, 1) for j in (0, 1)]
    return min(p), max(p)

def horner(poly, interval):
    result = (S.Integer(0), S.Integer(0))
    for c in S.Poly(poly, z, domain=S.QQ).all_coeffs():
        lo, hi = mul(result, interval)
        result = lo + c, hi + c
    return result

out = {'created_utc': datetime.now(timezone.utc).isoformat(), 'cases': {}}
for case in ('clean', 'frozen'):
    polys = [S.sympify(line, locals={'x': x, 'y': y, 'z': z})
             for line in (ROOT / (case + '-fresh-maximal-ideal.txt')).read_text().splitlines()]
    X = S.expand(x-polys[0]); Y = S.expand(y-polys[1])
    assert X.free_symbols <= {z} and Y.free_symbols <= {z}
    R = S.Poly(polys[2], z, domain=S.QQ)
    intervals = R.intervals(eps=S.Rational(1, 10**30))
    assert len(intervals) == 1 and intervals[0][1] == 1
    interval = intervals[0][0]
    xb, yb = horner(X, interval), horner(Y, interval)
    assert interval[0] > 0 and xb[0] > 0 and yb[0] > 0
    assert R.count_roots(*interval) == 1
    # The fresh radical control already proved this maximal ideal disjoint
    # from the conic ideal. Also record a direct interval exclusion L != 0.
    lb = (interval[0]-xb[1]-yb[1]+1, interval[1]-xb[0]-yb[0]+1)
    assert lb[1] < 0 or lb[0] > 0
    middle = sum(interval)/2
    out['cases'][case] = {
        'z_interval': list(map(str, interval)),
        'x_interval': list(map(str, xb)), 'y_interval': list(map(str, yb)),
        'L_interval': list(map(str, lb)),
        'approx_xyz': [float(X.subs(z, middle)), float(Y.subs(z, middle)), float(middle)],
        'one_real_residual_root': True,
        'positivity_certified_by_rational_interval_horner': True,
        'off_conic_by_nonzero_L_interval': True
    }
out['interpretation'] = ('The v2 Section 8 phrase cannot mean nowhere zero outside '
    'the conic. The main radical theorems already explicitly allow isolated residual '
    'points; this is a clarification, not a main-theorem counterexample.')
out['completed_utc'] = datetime.now(timezone.utc).isoformat()
(ROOT / 'off-conic-reproduced.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps({case: out['cases'][case]['approx_xyz'] for case in out['cases']}))
