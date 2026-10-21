"""Exact authored algebra checks; does not reproduce external source text."""
import sympy as s
x, y, e = s.symbols('x y e')
h = (x * y + 1) * (x - y) ** 2
p = 1 + x - y
if not s.expand(p + h - ((y - x - s.Rational(1, 2)) ** 2 + s.Rational(3, 4) + x * y * (y - x) ** 2)) == 0:
    raise RuntimeError('check_examples.py:6: s.expand(p+h-((y-x-s.Rational(1,2))**2+s.Rational(3,4)+x*y*(y-x)**2))==0')
if not s.Poly(p, x, y).total_degree() == 1:
    raise RuntimeError('check_examples.py:7: s.Poly(p,x,y).total_degree()==1')
if not s.Poly(h, x, y).total_degree() == 4:
    raise RuntimeError('check_examples.py:8: s.Poly(h,x,y).total_degree()==4')
if not s.Poly(h, x, y).coeff_monomial(y ** 4) == 0:
    raise RuntimeError('check_examples.py:9: s.Poly(h,x,y).coeff_monomial(y**4)==0')
r = (1 + x + y) ** 3 * (1 + x - y)
if not s.Poly(r, x, y).coeff_monomial(y ** 4) == -1:
    raise RuntimeError('check_examples.py:11: s.Poly(r,x,y).coeff_monomial(y**4)==-1')
if not s.expand(r.subs(y, x) - (1 + 2 * x) ** 3) == 0:
    raise RuntimeError('check_examples.py:12: s.expand(r.subs(y,x)-(1+2*x)**3)==0')
if not s.factor(4 * e * (e + 1 / (4 * e)) - (2 * e - 1) ** 2) == 4 * e:
    raise RuntimeError('check_examples.py:13: s.factor(4*e*(e+1/(4*e))-(2*e-1)**2)==4*e')
cubic = 1 + x ** 3 - (y - x) ** 3
if not s.expand(cubic.subs(y, x)) == 1 + x ** 3:
    raise RuntimeError('check_examples.py:15: s.expand(cubic.subs(y,x))==1+x**3')
if not s.Poly(cubic, x, y).coeff_monomial(y ** 3) == -1:
    raise RuntimeError('check_examples.py:16: s.Poly(cubic,x,y).coeff_monomial(y**3)==-1')
u = s.symbols('u')
F = (1 + x) ** 2 + (u - x) ** 2
if not s.expand(F.subs(u, x) - (1 + x) * (1 + x)) == 0:
    raise RuntimeError('check_examples.py:19: s.expand(F.subs(u,x)-(1+x)*(1+x))==0')
if not s.Poly(F, x, u).total_degree() == 2:
    raise RuntimeError('check_examples.py:20: s.Poly(F,x,u).total_degree()==2')
print('PASS: all exact identities, degree checks, and horizon assertions; explicit boundary perturbation determinant is 4ε>0.')
