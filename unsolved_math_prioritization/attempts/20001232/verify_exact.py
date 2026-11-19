import json, hashlib
from pathlib import Path
from fractions import Fraction
src = Path(__file__).parent
u0 = [[2, 1, 2, 0, 2, 0], [1, 0, 2, 0, 0, 2], [1, 0, 0, 2, 2, 0], [0, 1, 0, 2, 0, 2]]
v0 = [[2, 1, 2, 3, 0, 0], [2, 1, 0, 0, 2, 1], [0, 0, 2, 1, 2, 3]]
w0 = [[2, 3, 2], [2, 1, 2], [2, 1, 2], [2, 1, 2]]
I, J, K = (6, 4, 3)
cells = [(i, j, k) for i in range(I) for j in range(J) for k in range(K)]
rows = [[int(a == i and b == j) for a, b, c in cells] for i in range(I) for j in range(J)] + [[int(a == i and c == k) for a, b, c in cells] for i in range(I) for k in range(K)] + [[int(b == j and c == k) for a, b, c in cells] for j in range(J) for k in range(K)]
b = [u0[j][i] for i in range(I) for j in range(J)] + [v0[k][i] for i in range(I) for k in range(K)] + sum(w0, [])
records = json.loads((src / 'probe_results.json').read_text())['results']
checked = 0
positive = 0
if not {(r['scale'], r['offset']) for r in records} == {(s, t) for s in [1, 2, 3, 5, 10] for t in [0, 1, 2]}:
    raise RuntimeError('exact mathematical check failed at original line 13')
for r in records:
    s, t = (r['scale'], r['offset'])
    rhs = [s * v + t * sum(row) for v, row in zip(b, rows)]
    if not r['min_margin'] == min(rhs):
        raise RuntimeError('exact mathematical check failed at original line 16')
    if not sorted(map(int, r['witnesses'])) == r['spectrum']:
        raise RuntimeError('exact mathematical check failed at original line 17')
    if t:
        if not min(rhs) > 0:
            raise RuntimeError('exact mathematical check failed at original line 19')
        if not r['spectrum'] == list(range(2 * s + 3 * t + 1)):
            raise RuntimeError('exact mathematical check failed at original line 20')
        positive += 1
    for z, x in r['witnesses'].items():
        if not (len(x) == I and all((len(a) == J and all((len(q) == K for q in a)) for a in x))):
            raise RuntimeError('exact mathematical check failed at original line 22')
        flat = [x[i][j][k] for i, j, k in cells]
        if not all((type(a) is int and a >= 0 for a in flat)):
            raise RuntimeError('exact mathematical check failed at original line 24')
        if not all((sum((a * y for a, y in zip(row, flat))) == v for row, v in zip(rows, rhs))):
            raise RuntimeError('exact mathematical check failed at original line 25')
        if not flat[0] == int(z):
            raise RuntimeError('exact mathematical check failed at original line 26')
        checked += 1
cert = json.loads((src / 'exact_zero_fiber.json').read_text())
active = [n for n in range(72) if all((not row[n] or v != 0 for row, v in zip(rows, b)))]
if not active == cert['active_flat_indices']:
    raise RuntimeError('exact mathematical check failed at original line 28')
c, d = (cert['constant'], cert['direction'])
if not len(c) == len(d) == len(active) == 26:
    raise RuntimeError('exact mathematical check failed at original line 29')
M = [[row[n] for n in active] for row in rows]
if not all((sum((a * y for a, y in zip(row, c))) == v and sum((a * y for a, y in zip(row, d))) == 0 for row, v in zip(M, b))):
    raise RuntimeError('exact mathematical check failed at original line 31')
R = [[Fraction(a) for a in row] for row in M]
rank = 0
for col in range(26):
    pivot = next((j for j in range(rank, len(R)) if R[j][col]), None)
    if pivot is None:
        continue
    R[rank], R[pivot] = (R[pivot], R[rank])
    f = R[rank][col]
    R[rank] = [v / f for v in R[rank]]
    for j in range(rank + 1, len(R)):
        f = R[j][col]
        if f:
            R[j] = [a - f * v for a, v in zip(R[j], R[rank])]
    rank += 1
if not rank == 25 == cert['rank']:
    raise RuntimeError('exact mathematical check failed at original line 41')
if not (c[active.index(0)] == 4 and d[active.index(0)] == -2):
    raise RuntimeError('exact mathematical check failed at original line 42')
if not any((a == 0 and v == 1 for a, v in zip(c, d))):
    raise RuntimeError('exact mathematical check failed at original line 43')
if not (any((a == -1 and v == 1 for a, v in zip(c, d))) and any((a == 2 and v == -1 for a, v in zip(c, d)))):
    raise RuntimeError('exact mathematical check failed at original line 44')
if not all((a + v >= 0 and a + 2 * v >= 0 for a, v in zip(c, d))):
    raise RuntimeError('exact mathematical check failed at original line 45')
print(json.dumps({'exact_integer_witnesses_checked': checked, 'positive_offset_complete_spectra': positive, 'zero_offset_exact_rank': rank, 'zero_offset_complete_spectrum_for_every_positive_integer_scale': '{0,2,...,2s}'}))
padding = json.loads((src / 'padding_family.json').read_text())['ones_margin_witnesses']
if not len(padding) == 4:
    raise RuntimeError('exact mathematical check failed at original line 48')
for z, x in enumerate(padding):
    if not (len(x) == I and all((len(a) == J and all((len(q) == K for q in a)) for a in x))):
        raise RuntimeError('exact mathematical check failed at original line 50')
    flat = [x[i][j][k] for i, j, k in cells]
    if not all((type(a) is int and a >= 0 for a in flat)):
        raise RuntimeError('exact mathematical check failed at original line 52')
    if not (flat[0] == z and all((sum((a * y for a, y in zip(row, flat))) == sum(row) for row in rows))):
        raise RuntimeError('exact mathematical check failed at original line 53')
print('PASS four all-ones-margin witnesses; total 169 witnesses')
