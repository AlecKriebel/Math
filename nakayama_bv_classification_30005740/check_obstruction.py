import sympy as s
x = s.symbols('x')
cases = [x ** 2, x ** 3, x ** 6, (x - 1) ** 2 * (x + 2), (x * x + 1) ** 3 * (x - 2) ** 2, 7 * (x * x + 1) ** 2]
rows = []
for h in cases:
    d = s.gcd(h, s.diff(h, x)).monic() if isinstance(s.gcd(h, s.diff(h, x)), s.Poly) else s.Poly(s.gcd(h, s.diff(h, x)), x).monic().as_expr()
    pi = s.cancel(h / d)
    for u, m in s.factor_list(d)[1]:
        g = s.cancel(d / u)
        L = s.cancel(pi * s.diff(h, x) / h - s.diff(pi, x))
        q = s.cancel(L * g - pi * s.diff(g, x))
        relation = s.expand(L * h + h * s.diff(pi, x) - s.diff(h, x) * pi)
        if not relation == 0:
            raise RuntimeError('check_obstruction.py:13: relation==0')
        if not s.rem(s.Poly(pi * g, x), s.Poly(d, x)).is_zero:
            raise RuntimeError('check_obstruction.py:14: s.rem(s.Poly(pi*g,x),s.Poly(d,x)).is_zero')
        if not s.cancel(q - h * s.diff(u, x) / u ** 2) == 0:
            raise RuntimeError('check_obstruction.py:15: s.cancel(q-h*s.diff(u,x)/u**2)==0')
        if not not s.rem(s.Poly(q, x), s.Poly(h, x)).is_zero:
            raise RuntimeError('check_obstruction.py:16: not s.rem(s.Poly(q,x),s.Poly(h,x)).is_zero')
        rows.append({'h': str(h), 'u': str(u), 'd': str(d), 'b_Y_coefficient': str(L), 'bracket_q': str(q), 'relation_check': True, 'cup_zero': True, 'bracket_nonzero': True})
import json
print(json.dumps(rows, indent=2))
