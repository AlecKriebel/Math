"""Ancillary exact coefficient checks; the all-m analytic proof is in ROOT_MATH_REVIEW.md."""
from fractions import Fraction as Q
from math import comb
import json

def require(ok, label):
    if not ok:
        raise ValueError(label)

def integral(p):
    return sum((c / Q(j + 1) for j, c in enumerate(p)), Q(0))

def mul(p, q):
    r = [Q(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            r[i + j] += x * y
    return r

def value(p, x):
    r = Q(0)
    for c in reversed(p):
        r = r * x + c
    return r

checks = 0
for m in range(1, 129):
    h = sum((Q(1, k) for k in range(1, m + 1)), Q(0))
    # Direct binomial expansion of 1-(1-t)^m.
    a = [Q(0)] + [Q((-1)**(j+1) * comb(m, j)) for j in range(1, m+1)]
    p = a[1:]
    # Independently sum the finite geometric series for P_m.
    p_geom = [sum(Q((-1)**j * comb(k, j)) for k in range(j, m)) for j in range(m)]
    require(p == p_geom, 'binomial versus geometric'); checks += 1
    require(integral(p) == h, 'direct origin integral'); checks += 1
    f = [-h] + [a[j] / j for j in range(1, m+1)]
    require(sum(f) == 0, 'zero boundary trace'); checks += 1
    require([j*f[j] for j in range(1,m+1)] == p, 'bar partial primitive'); checks += 1
    g = [f[0]] + [f[j]+a[j] for j in range(1,m+1)]
    dg = [j*g[j] for j in range(1,m+1)]
    require(dg == [p[k]+Q(m*(-1)**k*comb(m-1,k)) for k in range(m)], 'monotonicity identity'); checks += 1
    require(g[0] == -h and sum(g) == 1, 'both endpoint values'); checks += 1
    require(integral(mul(g,g)) == integral(mul(a,a)) == 1-Q(2,m+1)+Q(1,2*m+1), 'full-plane L2 isometry check'); checks += 1
    for t in (Q(1,7), Q(1,2), Q(6,7)):
        g_direct = 1-(1-t)**m-sum(((1-t)**k/Q(k) for k in range(1,m+1)), Q(0))
        require(value(g,t) == g_direct, 'independent point evaluation'); checks += 1

rejections = []
for label, bad in [('wrong origin sign', lambda: require(Q(1) == -Q(1), 'origin sign')),
                   ('wrong m=1 normalization', lambda: require(Q(2) == Q(1), 'normalization'))]:
    try:
        bad()
    except ValueError:
        rejections.append(label)
    else:
        raise RuntimeError('guard failed: ' + label)
print(json.dumps(dict(status='PASS', m_min=1, m_max=128, exact_checks=checks,
    guard_controls_rejected=rejections,
    limitation='Finite coefficient/integral checks do not prove analytic convergence, principal values, all-m identities, or priority.'), indent=2))
