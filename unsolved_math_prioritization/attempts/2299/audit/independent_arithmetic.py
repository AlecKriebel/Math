"""Independently authored exact-integer cross-check; does not import claim code."""
from math import comb
import json

def shadow(m, k):
    total = 0
    ceiling = None
    while m and k:
        low = k - 1
        high = ceiling if ceiling is not None else k
        if ceiling is None:
            while comb(high, k) <= m:
                high *= 2
        while high - low > 1:
            mid = (low + high) // 2
            if comb(mid, k) <= m:
                low = mid
            else:
                high = mid
        if not low >= k:
            raise RuntimeError('Arithmetic check failed: low >= k')
        total += comb(low, k - 1)
        m -= comb(low, k)
        ceiling = low
        k -= 1
    if not m == 0:
        raise RuntimeError('Arithmetic check failed: m == 0')
    return total

def chain(r, hi, top=None):
    v = {hi: r if top is None else top}
    for i in range(hi - 1, 1, -1):
        v[i] = r + shadow(v[i + 1], i + 1)
    return v

def fits(v, n):
    return all((m <= comb(n, i) for i, m in v.items()))
out = {'small': [], 'uniform_finite': [], 'lower_window': {}, 'seams': []}
for r in range(4, 11):
    n = 2 * r + 4
    bad = chain(r, n - 2)
    good = chain(r, n - 1)
    core = chain(r, r + 2)
    if not (bad[2] > comb(n, 2) and all((bad[i] <= comb(n, i) for i in bad if i >= 3))):
        raise RuntimeError('Arithmetic check failed: bad[2] > comb(n, 2) and all((bad[i] <= comb(n, i) for i in bad if i >= 3))')
    if not (fits(good, n + 1) and fits(core, r + 5)):
        raise RuntimeError('Arithmetic check failed: fits(good, n + 1) and fits(core, r + 5)')
    out['small'].append({'r': r, 'last_failure': n, 'overflow': bad[2] - comb(n, 2), 'first_success_slack2': comb(n + 1, 2) - good[2]})
for r in range(11, 29):
    a = chain(r, r + 2)
    e = a[3] - comb(r + 4, 3)
    bad = chain(r, 2 * r + 3)
    if not (all((a[i] <= comb(r + 4, i) for i in a if i >= 4)) and 1 <= e <= 6):
        raise RuntimeError('Arithmetic check failed: all((a[i] <= comb(r + 4, i) for i in a if i >= 4)) and 1 <= e <= 6')
    if not (fits(a, r + 5) and bad[2] > comb(2 * r + 5, 2)):
        raise RuntimeError('Arithmetic check failed: fits(a, r + 5) and bad[2] > comb(2 * r + 5, 2)')
    if not all((bad[i] <= comb(2 * r + 5, i) for i in bad if i >= 3)):
        raise RuntimeError('Arithmetic check failed: all((bad[i] <= comb(2 * r + 5, i) for i in bad if i >= 3))')
    out['uniform_finite'].append({'r': r, 'carry': e, 'overflow': bad[2] - comb(2 * r + 5, 2)})
slacks = []
for r in range(11, 380):
    a = chain(r, r + 1, r - 6)
    if not fits(a, r + 4):
        raise RuntimeError('Arithmetic check failed: fits(a, r + 4)')
    slack = min((comb(r + 4, i) - m for i, m in a.items()))
    slacks.append((slack, r))
    if r in (377, 378, 379):
        out['seams'].append({'r': r, 'minimum_slack': slack})
out['lower_window'] = {'range': [11, 377], 'count': 367, 'failures': 0, 'minimum_slack': min((x[0] for x in slacks[:367])), 'first_minimum_r': min(slacks[:367])[1]}
print(json.dumps(out, indent=2))
