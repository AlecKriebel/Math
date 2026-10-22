import sympy as s
import json
x, y, e = s.symbols('x y e', real=True)
h = (x * y + 1) * (x - y) ** 2
p = 1 + x - y
r = (1 + x + y) ** 3 * p

def component(f, degree):
    return s.Add(*(coef * x ** a * y ** b for (a, b), coef in s.Poly(f, x, y).terms() if a + b == degree))

def at_axis(f):
    return f.subs({x: 0, y: 1})
checks = {'source_counterexample_identity': s.expand(p + h - ((y - x - s.Rational(1, 2)) ** 2 + s.Rational(3, 4) + x * y * (y - x) ** 2)) == 0, 'h_degree': s.Poly(h, x, y).total_degree(), 'p_degree': s.Poly(p, x, y).total_degree(), 'p_actual_leading_at_axis': at_axis(component(p, s.Poly(p, x, y).total_degree())), 'p_ambient_degree4_at_axis': at_axis(component(p, 4)), 'h_leading_at_axis': at_axis(component(h, 4)), 'separator_r_degree': s.Poly(r, x, y).total_degree(), 'separator_r_degree4_at_axis': s.Poly(r, x, y).coeff_monomial(y ** 4), 'separator_r_on_diagonal': str(s.factor(r.subs(y, x))), 'nonexact_epsilon_quadratic_determinant_M_1_over_4e': str(s.simplify(e * (e + 1 / (4 * e)) - (2 * e - 1) ** 2 / 4)), 'empty_Z_example_completion_identity': s.simplify((s.Symbol('A') + s.Symbol('M')) * x ** 2 + s.Symbol('B') * x + s.Symbol('C') + s.Symbol('M') - ((s.Symbol('A') + s.Symbol('M')) * (x + s.Symbol('B') / (2 * (s.Symbol('A') + s.Symbol('M')))) ** 2 + s.Symbol('C') + s.Symbol('M') - s.Symbol('B') ** 2 / (4 * (s.Symbol('A') + s.Symbol('M'))))) == 0}
if not checks['h_degree'] == 4:
    raise RuntimeError("check_exact.py:24: checks['h_degree']==4")
if not checks['p_degree'] == 1:
    raise RuntimeError("check_exact.py:25: checks['p_degree']==1")
if not checks['p_actual_leading_at_axis'] == -1:
    raise RuntimeError("check_exact.py:26: checks['p_actual_leading_at_axis']==-1")
if not checks['p_ambient_degree4_at_axis'] == 0:
    raise RuntimeError("check_exact.py:27: checks['p_ambient_degree4_at_axis']==0")
if not checks['h_leading_at_axis'] == 0:
    raise RuntimeError("check_exact.py:28: checks['h_leading_at_axis']==0")
if not checks['separator_r_degree'] == 4:
    raise RuntimeError("check_exact.py:29: checks['separator_r_degree']==4")
if not s.expand(r.subs(y, x) - (1 + 2 * x) ** 3) == 0:
    raise RuntimeError('check_exact.py:30: s.expand(r.subs(y,x)-(1+2*x)**3)==0')
if not checks['source_counterexample_identity']:
    raise RuntimeError("check_exact.py:31: checks['source_counterexample_identity']")
if not checks['separator_r_degree4_at_axis'] == -1:
    raise RuntimeError("check_exact.py:32: checks['separator_r_degree4_at_axis']==-1")
if not checks['nonexact_epsilon_quadratic_determinant_M_1_over_4e'] == 'e':
    raise RuntimeError("check_exact.py:33: checks['nonexact_epsilon_quadratic_determinant_M_1_over_4e']=='e'")
if not checks['empty_Z_example_completion_identity']:
    raise RuntimeError("check_exact.py:34: checks['empty_Z_example_completion_identity']")
print(json.dumps(checks, indent=2, default=str))
