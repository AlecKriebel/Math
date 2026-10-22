"""Exact rational local computations. No numerical fitting or external data imports."""
import sympy as S
import json
from pathlib import Path
v, w = S.symbols('v w')
N = 4
tr = lambda f: S.series(f, v, 0, N + 1).removeO().expand()

def period(k):
    a = S.Integer(1)
    coeff = [a]
    for n in range(1, N + 1):
        a *= (n - 1 + S.Rational(k, 5)) ** 4 / S.prod((n + S.Rational(k - j, 5) for j in range(1, 5)))
        coeff.append(a)
    return sum((a * v ** n for n, a in enumerate(coeff)))
A = {k: period(k) for k in range(1, 5)}
for k in A:
    for n in range(1, N + 1):
        if not S.expand(A[k]).coeff(v, n) * S.prod((n + S.Rational(k - j, 5) for j in range(1, 5))) == S.expand(A[k]).coeff(v, n - 1) * (n - 1 + S.Rational(k, 5)) ** 4:
            raise AssertionError('exact mathematical guard failed')
H = tr(A[2] / A[1])
J = tr(H + 5 * v * S.diff(H, v))
K = S.Integer(1)
for n in range(1, N + 1):
    c = S.Symbol('c')
    trial = K + c * w ** n
    expr = S.series(trial * H.subs(v, w * trial ** 5), w, 0, n + 1).removeO().expand().coeff(w, n)
    K += S.solve(expr, c)[0] * w ** n
if not S.series(K * H.subs(v, w * K ** 5), w, 0, N + 1).removeO().expand() == 1:
    raise AssertionError('exact mathematical guard failed')

def compose(f):
    return S.series(f.subs(v, w * K ** 5), w, 0, N + 1).removeO().expand()
Y = compose(tr(5 / A[1] ** 2 / (1 - v) / J ** 3))
F0 = {5 * n + 3: S.factor(Y.coeff(w, n) / ((5 * n + 1) * (5 * n + 2) * (5 * n + 3))) for n in range(N + 1)}
F1u = tr(-S.Rational(31, 3) * S.log(A[1]) - S.Rational(1, 12) * S.log(1 - v) - S.Rational(1, 2) * S.log(J))
F1s = compose(F1u)
F1 = {5 * n: F1s.coeff(w, n) for n in range(1, N + 1)}
expected0 = {3: S.Rational(5, 6), 8: S.Rational(5, 1008), 13: S.Rational(5975, 10378368), 18: S.Rational(34521785, 266765571072)}
expected1 = {5: -S.Rational(1, 9), 10: -S.Rational(163, 18144), 15: -S.Rational(85031, 46702656), 20: -S.Rational(6909032915, 20274183401472)}
if not all((F0[n] == c for n, c in expected0.items())):
    raise AssertionError('exact mathematical guard failed')
if not F1 == expected1:
    raise AssertionError('exact mathematical guard failed')
hkq = {0: expected0, 1: expected1, 2: {2: S.Rational(155, 18), 7: -S.Rational(5, 864), 12: S.Rational(585295, 14370048), 17: S.Rational(1710167735, 177843714048)}, 3: {4: S.Rational(488305, 9072), 9: -S.Rational(3634345, 979776), 14: -S.Rational(1612981445, 7846046208), 19: -S.Rational(2426211933305, 116115777662976)}, 4: {1: S.Rational(48550, 567), 6: S.Rational(36705385, 163296), 11: S.Rational(16986429665, 603542016), 16: S.Rational(341329887875, 70614415872)}, 5: {3: S.Rational(1237460905, 224532), 8: S.Rational(108607458385, 28740096), 13: -S.Rational(2079654832074515, 1553517149184), 18: -S.Rational(50102421421803185, 438808843984896)}}
if not all(((n - (2 * g - 2)) % 5 == 0 for g, cs in hkq.items() for n in cs)):
    raise AssertionError('exact mathematical guard failed')
counts = {g: max(0, g - 1 - int(S.ceiling(S.Rational(3 * g - 3, 5)))) for g in range(2, 54)}
if not all((c == (2 * g - 2) // 5 for g, c in counts.items())):
    raise AssertionError('exact mathematical guard failed')
witness = []
for g in range(4, 101):
    m = int(S.ceiling(S.Rational(3 * (g - 1), 5)))
    r = 5 * m - 3 * (g - 1)
    if not (m + 1 <= g - 1 and 0 <= r <= 4 and ((r - 2 * g + 2) % 5 == 0)):
        raise AssertionError('exact mathematical guard failed')
    if not g - m - 2 >= 0:
        raise AssertionError('exact mathematical guard failed')
    witness.append({'g': g, 'm': m, 'leading_power': r, 'leading_coefficient_shift': str(5 ** (2 * g - 2))})
out = {'explicit_ambiguity_witness_checks': witness, 'period_A_polynomials': {str(k): str(a) for k, a in A.items()}, 'flat_s_over_u': str(H), 'inverse_u_over_s': str(K), 'Yukawa_in_w_s5': str(Y), 'F0_independent': {str(n): str(c) for n, c in F0.items()}, 'F1_independent': {str(n): str(c) for n, c in F1.items()}, 'HKQ_transcription': {str(g): {str(n): str(c) for n, c in cs.items()} for g, cs in hkq.items()}, 'ambiguity_counts_per_Liu_Ruan': counts, 'assertions': 'PASS: 16 PF coefficient equations, inverse mirror map to w^4, four genus-zero and four genus-one HKQ coefficients, 24 support residues, remaining-index count genera 2-53; explicit ambiguity exponents genera 4-100.'}
Path(__file__).with_name('exact_checks.json').write_text(json.dumps(out, indent=2) + '\n')
print(out['assertions'])
print('F0:', F0)
print('F1:', F1)
