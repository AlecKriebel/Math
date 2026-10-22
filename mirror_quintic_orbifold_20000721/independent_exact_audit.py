import sympy as S
from fractions import Fraction
u, s = S.symbols('u s')
A = {}
for k in range(1, 5):
    c = S.Rational(1)
    a = 1
    for n in range(1, 4):
        c *= (n - 1 + S.Rational(k, 5)) ** 4 / S.prod((n + S.Rational(k - j, 5) for j in range(1, 5)))
        a += c * u ** (5 * n)
    A[k] = a
N = 16
tr = lambda a: S.series(a, u, 0, N).removeO().expand()
sm = tr(u * A[2] / A[1])
ds = S.diff(sm, u)
y = tr(5 / A[1] ** 2 / (1 - u ** 5) / ds ** 3)
f1 = tr(-S.Rational(31, 3) * S.log(A[1]) - S.Rational(1, 12) * S.log(1 - u ** 5) - S.Rational(1, 2) * S.log(ds))
b, c = S.symbols('b c')
inv = s + b * s ** 6 + c * s ** 11
comp = S.series(sm.subs(u, inv), s, 0, 12).removeO().expand()
sol = S.solve([comp.coeff(s, 6), comp.coeff(s, 11)], [b, c])
inv = inv.subs(sol)
ys = S.series(y.subs(u, inv), s, 0, 11).removeO().expand()
fs = S.series(f1.subs(u, inv), s, 0, 11).removeO().expand()
print('A1=', A[1])
print('s=', sm)
print('u=', inv)
print('C_sss=', ys)
print('F1=', fs)
if not ys == 5 + S.Rational(5, 3) * s ** 5 + S.Rational(5975, 6048) * s ** 10:
    raise AssertionError('exact mathematical guard failed')
if not fs == -s ** 5 / 9 - S.Rational(163, 18144) * s ** 10:
    raise AssertionError('exact mathematical guard failed')
print('PASS independent exact low-genus check')
