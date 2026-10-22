import json
from itertools import combinations
import sympy as s
I = s.eye(3)
J = s.ones(3)
Qb = s.diag(J / 3, I - J / 3)
Qg = (I / 3).row_join(s.sqrt(2) * I / 3).col_join((s.sqrt(2) * I / 3).row_join(2 * I / 3))
for Q in [Qb, Qg]:
    if not (Q == Q.T and Q * Q == Q):
        raise RuntimeError('Exact check failed at original line 8')
    if not list(Q.diagonal()) == [s.Rational(1, 3)] * 3 + [s.Rational(2, 3)] * 3:
        raise RuntimeError('Exact check failed at original line 9')
    if not Q.rank() == 3:
        raise RuntimeError('Exact check failed at original line 10')
Pb = s.eye(6) - Qb
Pg = s.eye(6) - Qg
parts = []
for mask in range(1, 2 ** 5):
    S = [0] + [i for i in range(1, 6) if not mask >> i - 1 & 1]
    T = [i for i in range(1, 6) if mask >> i - 1 & 1]
    vals = []
    for P in [Pb, Pg]:
        ev = list(P.extract(S, S).eigenvals()) + list(P.extract(T, T).eigenvals())
        vals.append(max(ev))
    if not vals[0] == 1:
        raise RuntimeError('Exact check failed at original line 20')
    parts.append({'S': S, 'T': T, 'bad_norm': str(vals[0]), 'good_norm': str(vals[1])})
if not min((s.sympify(p['good_norm']) for p in parts)) == s.Rational(2, 3):
    raise RuntimeError('Exact check failed at original line 22')
t = s.symbols('theta', positive=True)
C = s.Matrix([[t, s.sqrt(t * (1 - t))], [s.sqrt(t * (1 - t)), 1 - t]])
if not s.simplify(C * C - C) == s.zeros(2):
    raise RuntimeError('Exact check failed at original line 25')
print(json.dumps({'status': 'PASS', 'sympy': s.__version__, 'fractional_coupling_projection_identity': True, 'same_diagonal_real_projection_witness': True, 'bad_optimum': '1', 'good_optimum': '2/3', 'all_31_unordered_nonempty_partitions': parts}, indent=2))
