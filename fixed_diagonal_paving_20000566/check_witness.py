import sympy as s, json
from pathlib import Path
J = s.ones(3)
I = s.eye(3)
B = s.diag(J / 3, I - J / 3)
G = (I / 3).row_join(s.sqrt(2) * I / 3).col_join((s.sqrt(2) * I / 3).row_join(2 * I / 3))
for Q in [B, G]:
    if not (Q.T == Q and Q * Q == Q and (Q.rank() == 3)):
        raise RuntimeError('Exact check failed at original line 7')
    if not list(Q.diagonal()) == [s.Rational(1, 3)] * 3 + [s.Rational(2, 3)] * 3:
        raise RuntimeError('Exact check failed at original line 8')
if not B[:3, :3].rank() == 1:
    raise RuntimeError('Exact check failed at original line 9')
if not (s.eye(6) - G)[:3, :3] == 2 * I / 3:
    raise RuntimeError('Exact check failed at original line 10')
if not (s.eye(6) - G)[3:, 3:] == I / 3:
    raise RuntimeError('Exact check failed at original line 11')
out = {'real_same_diagonal_strict_separation': True, 'bad_value': '1', 'good_value': '2/3'}
Path(__file__).with_name('WITNESS_CHECK.json').write_text(json.dumps(out, indent=2) + '\n')
print(out)
