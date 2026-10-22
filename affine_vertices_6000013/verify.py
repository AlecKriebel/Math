"""Exact algebraic sanity checks; not numerical evidence of global theorems.
Guards: graph vertex tests apply only where q=f'' !=0; counts exclude
inflections. Quotient examples do not assert completeness/equiaffinity.
"""
import sympy as s
x, a, t, n, eps = s.symbols('x a t n eps', real=True)

def numerator(f, z):
    q = s.diff(f, z, 2)
    return s.expand(9 * q * q * s.diff(q, z, 3) - 45 * q * s.diff(q, z) * s.diff(q, z, 2) + 40 * s.diff(q, z) ** 3)
f = x ** a
expected = 2 * a ** 3 * (a - 1) ** 3 * (a - 2) * (a + 1) * (2 * a - 1) * x ** (3 * a - 9)
if not s.simplify(numerator(f, x) - expected) == 0:
    raise RuntimeError('Exact mathematical check failed')
if not numerator(x ** 3, x) == 8640:
    raise RuntimeError('Exact mathematical check failed')
if not s.simplify(numerator(eps * s.sin(n * t), t) + eps ** 3 * n ** 9 * s.cos(n * t) * (36 * s.sin(n * t) ** 2 + 40 * s.cos(n * t) ** 2)) == 0:
    raise RuntimeError('Exact mathematical check failed')
if not s.factor(s.wronskian([1, x, x ** 3, x ** 2, x ** 4, x ** 6], x)) == -207360 * x:
    raise RuntimeError('Exact mathematical check failed')
q = s.Function('q')(x)
k = (3 * q * s.diff(q, x, 2) - 5 * s.diff(q, x) ** 2) / (9 * q ** s.Rational(8, 3))
if not s.simplify(k + s.diff(q ** s.Rational(-2, 3), x, 2) / 2) == 0:
    raise RuntimeError('Exact mathematical check failed')
if not s.simplify(s.diff(k, x) * 27 * q ** s.Rational(11, 3) - (9 * q * q * s.diff(q, x, 3) - 45 * q * s.diff(q, x) * s.diff(q, x, 2) + 40 * s.diff(q, x) ** 3)) == 0:
    raise RuntimeError('Exact mathematical check failed')
a2, a3, a4, a5 = s.symbols('a2 a3 a4 a5', nonzero=True)
f = a2 * x * x + a3 * x ** 3 + a4 * x ** 4 + a5 * x ** 5
conic = f - a2 * x * x - a3 / a2 * x * f + (a3 * a3 / a2 ** 3 - a4 / a2 ** 2) * f * f
if not s.expand(conic).coeff(x, 5) == a5 - 3 * a3 * a4 / a2 + 2 * a3 ** 3 / a2 ** 2:
    raise RuntimeError('Exact mathematical check failed')
if not s.expand(numerator(f, x).subs(x, 0) - 4320 * (a2 * a2 * a5 - 3 * a2 * a3 * a4 + 2 * a3 ** 3)) == 0:
    raise RuntimeError('Exact mathematical check failed')
print('PASS: exact power graph, cubic nonvertex, periodic sine count factor, conic Wronskian, curvature/contact identities.')
rho = 1 + (1 - n * n) * eps * s.cos(n * t)
k = rho ** s.Rational(-4, 3) - s.diff(rho, t, 2) * rho ** s.Rational(-7, 3) / 3 + 4 * s.diff(rho, t) ** 2 * rho ** s.Rational(-10, 3) / 9
if not s.simplify(s.diff(k, t, eps).subs(eps, 0) - n * (n * n - 1) * (n * n - 4) * s.sin(n * t) / 3) == 0:
    raise RuntimeError('Exact mathematical check failed')
r = s.Matrix([s.exp(t) * s.cos(t), s.exp(t) * s.sin(t)])
if not s.simplify(s.det(s.Matrix.hstack(s.diff(r, t), s.diff(r, t, 2))) - 2 * s.exp(2 * t)) == 0:
    raise RuntimeError('Exact mathematical check failed')
exponents = [0, 1 + s.I, 1 - s.I, 2, 2 + 2 * s.I, 2 - 2 * s.I]
if not len(set(exponents)) == 6:
    raise RuntimeError('Exact mathematical check failed')
vandermonde = s.prod((exponents[j] - exponents[i] for j in range(6) for i in range(j)))
if not s.simplify(vandermonde) != 0:
    raise RuntimeError('Exact mathematical check failed')
print('PASS: support-function first variation and spiral noninflection/Vandermonde checks.')
