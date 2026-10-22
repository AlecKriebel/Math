"""Exact rational symbolic checks; not a numerical proof or novelty claim."""
import json
from pathlib import Path
import sympy as s
N, r, c, t, a, b, z = s.symbols('N r c t a b z')
D = a * (1 - a) * b * (1 - b)
checks = {}

def record(name, condition):
    if not condition:
        raise RuntimeError(name)
    checks[name] = 'PASS'
q = s.Matrix([[t, r - t], [c - t, N - r - c + t]])
record('expected determinant Nt-rc', s.expand(q.det() - (N * t - r * c)) == 0)
u11, u12, u21, u22 = s.symbols('u11 u12 u21 u22')
u = [u11, u12, u21, u22]
p = [a * b, a * (1 - b), (1 - a) * b, (1 - a) * (1 - b)]
for v, stat in [(a, u11 + u12), (b, u11 + u21)]:
    diff = sum((ui * s.diff(pi, v) / pi for ui, pi in zip(u, p)))
    record('score_' + str(v), s.simplify(diff - (stat - sum(u) * v) / (v * (1 - v))) == 0)
record('checkerboard likelihood constant', s.cancel(p[0] * p[3] / p[1] / p[2]) == 1)
K = s.QQ.frac_field(N, r, c)
g = s.groebner([r - N * a, c - N * b, z * D - 1], a, b, z, domain=K)
for name, f in [('a', a - r / N), ('b', b - c / N), ('z', z - N ** 4 / (r * (N - r) * c * (N - c)))]:
    record('generic_solution_' + name, g.reduce(f)[1] == 0)
record('generic fiber not empty', not any((f.as_expr() == 1 for f in g.polys)))
for name, eqs, K in [('N0_r_nonzero', [r, c, z * D - 1], s.QQ.frac_field(r, c)), ('N0_r0_c_nonzero', [c, z * D - 1], s.QQ.frac_field(c)), ('N_nonzero_r0', [-N * a, c - N * b, z * D - 1], s.QQ.frac_field(N, c)), ('N_nonzero_rN', [N - N * a, c - N * b, z * D - 1], s.QQ.frac_field(N, c)), ('N_nonzero_c0', [r - N * a, -N * b, z * D - 1], s.QQ.frac_field(N, r)), ('N_nonzero_cN', [r - N * a, N - N * b, z * D - 1], s.QQ.frac_field(N, r))]:
    G = s.groebner(eqs, a, b, z, domain=K)
    record(name + '_empty', list(G) == [1])
G = s.groebner([z * D - 1], a, b, z, domain=s.QQ)
record('allzero not empty', list(G) != [1])
record('allzero not zero-dimensional', not G.is_zero_dimensional)
G = s.groebner([a, b - s.Rational(1, 2), z * D - 1], z, a, b, domain=s.QQ)
record('specialize_then_saturate_is_unit', list(G) == [1])
record('saturate_then_specialize_keeps_boundary', D.subs({a: 0, b: s.Rational(1, 2)}) == 0)
x = s.Matrix([1, 2, -3])
y = s.Matrix([1, 2, 3, -6])
Q = x * y.T
record('3x4 zero-margin cell-torus example', all((v != 0 for v in Q)) and Q * s.ones(4, 1) == s.zeros(3, 1) and (s.ones(1, 3) * Q == s.zeros(1, 4)) and (Q.rank() == 1))
record('nonzero-row zero-column family', s.Matrix([1, 2, -3]) * s.Matrix([[1, 2, -2]]) * s.ones(3, 1) == s.Matrix([1, 2, -3]))
x0, x1 = s.symbols('x0 x1')
boundary = [x0, -x0, x1, -x1]
record('projective boundary ruling sumzero', sum(boundary) == 0)
record('projective boundary ruling determinantzero', s.expand(boundary[0] * boundary[3] - boundary[1] * boundary[2]) == 0)
out = {'arithmetic': 'SymPy ' + s.__version__ + ' over QQ and rational-function fields', 'checks': checks, 'count': len(checks), 'limitations': 'Symbolic branch checks support the proofs in report.md; matrix dimensions and closure completeness are proved there, not inferred from samples.'}
Path(__file__).with_name('exact_check_results.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
