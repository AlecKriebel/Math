import sympy as s
from collections import defaultdict
import json
x = s.symbols('x')

def add(d, k, v):
    if k[1]:
        d[k] += v
for n in range(2, 21):
    actual = defaultdict(int)
    for i in range(1, n):
        add(actual, (i, 1, n - 1 - i), 1)
        add(actual, (0, i + 1, n - 1 - i), -1)
        add(actual, (0, i, n - i), 1)
    expected = defaultdict(int)
    for i in range(n):
        add(expected, (i, 1, n - 1 - i), 1)
    add(expected, (0, n, 0), -1)
    if not {k: v for k, v in actual.items() if v} == {k: v for k, v in expected.items() if v}:
        raise RuntimeError('checks.py:17: {k:v for k,v in actual.items() if v}=={k:v for k,v in expected.items() if v}')
examples = [(x ** 2, x), (x ** 3, x), (x ** 7, x), ((x * x + 1) ** 2, x * x + 1), ((x * x + 1) ** 4 * (x - 2) ** 3 * (x + 1), x * x + 1), ((x * x + 1) ** 4 * (x - 2) ** 3 * (x + 1), x - 2), (7 * (x * x + 1) ** 2 * (x - 3), x * x + 1)]
results = []
for h, u in examples:
    h = s.expand(h)
    d = s.Poly(s.gcd(h, s.diff(h, x)), x).monic().as_expr()
    pi = s.cancel(h / d)
    g = s.cancel(d / u)
    L = s.cancel(pi * s.diff(d, x) / d)
    q = s.cancel(L * g - pi * s.diff(g, x))
    if not (s.denom(L) == 1 and s.denom(q) == 1):
        raise RuntimeError('checks.py:23: s.denom(L)==1 and s.denom(q)==1')
    if not s.expand(L * h + h * s.diff(pi, x) - s.diff(h, x) * pi) == 0:
        raise RuntimeError('checks.py:24: s.expand(L*h+h*s.diff(pi,x)-s.diff(h,x)*pi)==0')
    if not s.cancel(q - h * s.diff(u, x) / u ** 2) == 0:
        raise RuntimeError('checks.py:25: s.cancel(q-h*s.diff(u,x)/u**2)==0')
    if not s.rem(s.expand(g * pi), d, x) == 0:
        raise RuntimeError('checks.py:26: s.rem(s.expand(g*pi),d,x)==0')
    if not s.rem(q, h, x) != 0:
        raise RuntimeError('checks.py:27: s.rem(q,h,x)!=0')
    results.append(dict(h=str(h), u=str(u), d=str(d), pi=str(pi), g=str(g), L=str(L), q=str(q), cup_mod_d='0', bracket_mod_h=str(s.rem(q, h, x))))
print(json.dumps({'normalized_bar_telescope_degrees': list(range(2, 21)), 'examples': results}, indent=2))
