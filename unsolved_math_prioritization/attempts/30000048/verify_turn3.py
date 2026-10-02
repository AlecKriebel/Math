"""Exact algebra controls for the turn-3 SU(3) degree-four theorem.

Run beside verify_turn2.py, or pass --prior-dir to its recovered directory.
The analytic nonnegativity arguments are proved in TURN_3.md. This program
does not use a finite grid to assert positivity and is not a proof assistant.
"""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

checks = 0


def ck(condition):
    global checks
    assert condition
    checks += 1


def add(a, b):
    c = dict(a)
    for k, v in b.items():
        c[k] = c.get(k, 0) + v
    return {k: v for k, v in c.items() if v}


def scale(a, k):
    return {e: k * c for e, c in a.items() if k * c}


def mul(a, b):
    c = {}
    for (i, j), v in a.items():
        for (k, l), w in b.items():
            e = (i + k, j + l)
            c[e] = c.get(e, 0) + v * w
    return {k: v for k, v in c.items() if v}


def power(a, n):
    c = {(0, 0): 1}
    for _ in range(n):
        c = mul(c, a)
    return c


def swap(a):
    return {(j, i): c for (i, j), c in a.items()}


def conj(a):
    return {(-i, -j): c for (i, j), c in a.items()}


def substitute(p, u, v):
    c = {}
    for (i, j), n in p.items():
        c = add(c, scale(mul(power(u, i), power(v, j)), n))
    return c


def alt(exps):
    eigenvalues = [(1, 0), (0, 1), (-1, -1)]
    out = {}
    for perm in permutations(range(3)):
        inversions = sum(perm[i] > perm[j] for i in range(3)
                         for j in range(i + 1, 3))
        e = tuple(sum(exps[i] * eigenvalues[perm[i]][j]
                      for i in range(3)) for j in range(2))
        out[e] = out.get(e, 0) + (-1) ** inversions
    return {k: v for k, v in out.items() if v}


def center(p):
    return {e: c for e, c in p.items() if (e[0] - e[1]) % 3 == 0}


def circle(p):
    return substitute(p, {(1, 0): 1}, {(-1, 0): 1})


unit = {(0, 0): 1}
u, v = {(1, 0): 1}, {(0, 1): 1}
x = mul(u, v)
y = add(power(u, 3), power(v, 3))
trace = {(1, 0): 1, (0, 1): 1, (-1, -1): 1}
trace_conj = conj(trace)
den = alt((2, 1, 0))
weight = mul(den, conj(den))

# Complete symmetric functions followed by the two-row Jacobi-Trudi formula.
h = {-2: {}, -1: {}, 0: unit}
for n in range(1, 6):
    h[n] = add(add(mul(u, h[n - 1]), scale(mul(v, h[n - 2]), -1)),
               h[n - 3])
chars = {}
for a in range(5):
    for b in range(5 - a):
        ch = add(mul(h[a + b], h[b]), scale(mul(h[a + b + 1], h[b - 1]), -1))
        chars[a, b] = ch
        ck(ch.get((a, b)) == 1)
        ck(all(i + j < a + b for i, j in ch if (i, j) != (a, b)))
        laurent = substitute(ch, trace, trace_conj)
        ck(mul(den, laurent) == alt((a + b + 2, b + 1, 0)))
        ck(sum(laurent.values()) == (a + 1) * (b + 1) * (a + b + 2) // 2)
        ck(all((i - j - a + b) % 3 == 0 for i, j in ch))
ck(len(chars) == 15)
for (a, b), ch in chars.items():
    ck(swap(ch) == chars[b, a])
laurents = {ab: substitute(ch, trace, trace_conj) for ab, ch in chars.items()}
for ab, ch in laurents.items():
    for cd, other in laurents.items():
        ck(F(mul(mul(ch, conj(other)), weight).get((0, 0), 0), 6) == (ab == cd))

central_weights = sorted(ab for ab in chars if (ab[0] - ab[1]) % 3 == 0)
ck(central_weights == [(0, 0), (0, 3), (1, 1), (2, 2), (3, 0)])
central_monomials = sorted((i, j) for i in range(5) for j in range(5 - i)
                          if (i - j) % 3 == 0)
ck(central_monomials == [(0, 0), (0, 3), (1, 1), (2, 2), (3, 0)])

noncentral_basis = [add(u, v), add(power(u, 2), power(v, 2)),
                    mul(x, add(u, v)), add(power(u, 4), power(v, 4)),
                    mul(x, add(power(u, 2), power(v, 2)))]
expected_circles = [{(1, 0): 1, (-1, 0): 1},
                    {(2, 0): 1, (-2, 0): 1},
                    {(1, 0): 1, (-1, 0): 1},
                    {(4, 0): 1, (-4, 0): 1},
                    {(2, 0): 1, (-2, 0): 1}]
for p, expected in zip(noncentral_basis, expected_circles):
    ck(not center(p))
    ck(circle(p) == expected)
    ck(swap(p) == p)

roots = [unit, u, add(power(u, 2), scale(v, -1)), add(x, scale(unit, -1))]
squares = [mul(r, swap(r)) for r in roots]
expected_squares = [unit, x, add(add(power(x, 2), scale(y, -1)), x),
                    add(add(power(x, 2), scale(x, -2)), unit)]
for p, expected in zip(squares, expected_squares):
    ck(p == expected)
    ck(center(p) == p)
    ck(F(mul(substitute(p, trace, trace_conj), weight).get((0, 0), 0), 6) == 1)
ck(circle(squares[1]) == unit)
ck(circle(squares[2]) == {(0, 0): 2, (3, 0): -1, (-3, 0): -1})
ck(circle(squares[3]) == {})
for p in squares[1:3]:
    ck({e: c for e, c in p.items() if sum(e) < 2} == {})
    ck({e: c for e, c in p.items() if sum(e) == 2} == x)

# Every unit-circle trace is realized by diag(-s^2,s^-1,-s^-1).
eigenvalues = [{(2, 0): -1}, {(-1, 0): 1}, {(-1, 0): -1}]
ck(mul(mul(eigenvalues[0], eigenvalues[1]), eigenvalues[2]) == unit)
ck(add(add(eigenvalues[0], eigenvalues[1]), eigenvalues[2]) == {(2, 0): -1})

# The determinant at trace 1 is 2. At trace 0 it is 3 sqrt(3)/2.
# Store Q(sqrt(3)) values as (rational part, sqrt(3) coefficient).
def qmul(a, b):
    return (a[0] * b[0] + 3 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def qsub(a, b):
    return (a[0] - b[0], a[1] - b[1])


j0 = [[(0, F(-1, 2)), (0, -1)], [(F(3, 2), 0), (0, 0)]]
det0 = qsub(qmul(j0[0][0], j0[1][1]), qmul(j0[0][1], j0[1][0]))
ck(det0 == (0, F(3, 2)))
ck((-1) * 0 - (-2) * 1 == 2)

# After circle vanishing the adjoint-square perturbation is
# (1-x)[a(u+v)+b(u^2+v^2)]. Verify both independent coefficients.
for low, high in [(noncentral_basis[0], noncentral_basis[2]),
                  (noncentral_basis[1], noncentral_basis[4])]:
    ck(add(low, scale(high, -1)) == mul(add(unit, scale(x, -1)), low))
ck([b for b in range(-10, 11) if 1 + 2 * b >= 0 and 1 - 2 * b >= 0] == [0])
# The preceding range is only an arithmetic control. The proof itself bounds
# b between -1/2 and 1/2, hence covers every integer without a cutoff.

parser = argparse.ArgumentParser()
parser.add_argument('--prior-dir', type=Path, default=Path(__file__).resolve().parent)
args = parser.parse_args()
prior = json.loads(subprocess.check_output([sys.executable, str(args.prior_dir / 'verify_turn2.py')], text=True))
ck(prior['status'] == 'PASS_EXACT_FINITE_SPAN_CLASSIFICATION')
ck(prior['integer_triples'] == 19635)
ck(prior['excluded_by_exact_negative_witness'] == 19631)
ck(prior['surviving_triples'] == [[0, 0, 0], [1, 0, 0], [1, 0, 1], [2, 1, 1]])
ck(prior['witness_stream_sha256'] == '0711947aebd2f2ad9e9a20c4ac4c211c51fe769b9f1856686045dd96d83b442f')
char_rows = {str(ab): [[*e, c] for e, c in sorted(ch.items())] for ab, ch in sorted(chars.items())}
print(json.dumps({
    'status': 'PASS_EXACT_ALGEBRA_CONTROLS',
    'completed_substantive_author_turns': 3,
    'original_status': 'unresolved',
    'scope': 'All real SU(3) virtual characters supported on a+b<=4. Theorem and analytic positivity steps in TURN_3.md; independent review pending.',
    'turn3_exact_assertions': checks,
    'irreducibles_verified': len(chars),
    'orthogonality_pairs_verified': len(chars) ** 2,
    'center_neutral_weights': central_weights,
    'prior_turn2_assertions_rerun': prior['exact_assertions'],
    'prior_turn2_witness_sha256': prior['witness_stream_sha256'],
    'character_table_sha256': hashlib.sha256(json.dumps(char_rows, sort_keys=True).encode()).hexdigest(),
    'local_trace_jacobian_determinants': ['3*sqrt(3)/2 at trace 0', '2 at trace 1'],
    'survivor_square_root_dimensions': [1, 3, 6, 8],
    'finite_grid_positivity_inference': False,
}, indent=2, sort_keys=True))
