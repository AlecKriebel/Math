"""Independent direct-pair graph and full-subset audit of bounded instances."""
import json, hashlib
from pathlib import Path
P = Path(__file__).parent
rows = json.loads((P / 'exact_results.json').read_text()) + json.loads((P / 'sampled_t2_results.json').read_text())
checks = []
for row in rows:
    n, t = (row['N'], row['t'])
    A = row['witness']
    if not (len(A) == row['maximum'] and len(set(A)) == len(A) and all((1 <= a <= n for a in A))):
        raise RuntimeError('verification guard failed')
    edges = [(a, b) for a in range(1, n + 1) for b in range(a + 1, n + 1) if b - a >= t and b % (b - a) == 0]
    if not not any((a in A and b in A for a, b in edges)):
        raise RuntimeError('verification guard failed')
    adj = [0] * n
    for a, b in edges:
        adj[a - 1] |= 1 << b - 1
        adj[b - 1] |= 1 << a - 1
    if n <= 18:
        ok = bytearray(1 << n)
        ok[0] = 1
        best = 0
        count = 0
        for mask in range(1, 1 << n):
            low = mask & -mask
            rest = mask ^ low
            if ok[rest] and (not adj[low.bit_length() - 1] & rest):
                ok[mask] = 1
                best = max(best, mask.bit_count())
                count += 1
        if not best == row['maximum']:
            raise RuntimeError((n, t, best, row))
        checks.append({'N': n, 't': t, 'maximum': best, 'nonempty_independent_subsets': count})
    for x in range(2, n + 1, 2):
        actual = {y for y in range(1, n + 1, 2) if abs(x - y) >= t and max(x, y) % abs(x - y) == 0}
        predicted = {y for d in range(1, x + 1, 2) if x % d == 0 and d >= t for y in [x - d, x + d] if 1 <= y <= n}
        if not actual == predicted:
            raise RuntimeError('verification guard failed')
        u = x
        while u % 2 == 0:
            u //= 2
        if not (not actual) == (u < t):
            raise RuntimeError('verification guard failed')
    if t >= 2:
        L = n.bit_length() - 1
        q = max(1, (t - 1).bit_length())
        formula = min(L, q - 1) + (max(0, L - q + 1) + 1) // 2
        powers = [1 << k for k in range(1, L + 1)]
        best = max((mask.bit_count() for mask in range(1 << L) if all((not (mask >> i & 1 and mask >> j & 1) or (b - a < t or b % (b - a) != 0) for i, a in enumerate(powers) for j, b in enumerate(powers) if i < j))), default=0)
        if not best == formula:
            raise RuntimeError('verification guard failed')
out = {'all_recorded_witnesses_verified': len(rows), 'direct_subset_exhaustive_instances': checks, 'odd_neighbor_checks': 'All even x for every recorded (N,t)', 'restricted_power_formula_checks': 'Every recorded (N,t) with t>=2', 'scope': 'Independent exhaustive optimality verification only for N<=18. Larger supplied values have verified witnesses and a source-code recurrence audit, not independent exhaustive reruns.'}
(P / 'INDEPENDENT_CHECKS.json').write_text(json.dumps(out, indent=2) + '\n')
print('Verified', len(rows), 'witnesses;', len(checks), 'independent exhaustive optima.')
construction_rows = json.loads((P / 'construction_checks.json').read_text())
for row in construction_rows:
    n, t = (row['N'], row['t'])
    mstar = 2 * (t // 2) - 1
    Q = (2 * mstar).bit_length()
    even = []
    for m in range(1, t, 2):
        k = 1
        while (1 << k) * m <= n:
            even.append((1 << k) * m)
            k += Q
    A = sorted(list(range(1, n + 1, 2)) + even)
    if not (len(even) == row['added_evens'] and Q == row['Q'] and (row['passed'] is True)):
        raise RuntimeError('verification guard failed')
    if not len(A) == len(set(A)):
        raise RuntimeError('verification guard failed')
    if not all((b - a < t or b % (b - a) != 0 for i, a in enumerate(A) for b in A[i + 1:])):
        raise RuntimeError('verification guard failed')
out['reconstructed_spaced_valuation_constructions'] = len(construction_rows)
(P / 'INDEPENDENT_CHECKS.json').write_text(json.dumps(out, indent=2) + '\n')
print('Verified', len(construction_rows), 'spaced-valuation constructions.')
