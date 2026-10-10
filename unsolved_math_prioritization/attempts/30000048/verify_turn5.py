"""Exact algebra controls for unrestricted Hermitian-SOS rigidity on SU(3).

The geometric positivity gap is expressly not settled by these finite checks.
Place beside verify_turn4.py or supply --prior-dir.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse
import contextlib
import hashlib
import io
import json
import runpy

parser = argparse.ArgumentParser()
parser.add_argument('--prior-dir', type=Path, default=Path(__file__).resolve().parent)
args = parser.parse_args()
captured = io.StringIO()
with contextlib.redirect_stdout(captured):
    old = runpy.run_path(str(args.prior_dir / 'verify_turn4.py'))
prior_receipt = json.loads(captured.getvalue())
assert prior_receipt['status'] == 'PASS_EXACT_ALGEBRA_CONTROLS'
mul, add, power = old['mul'], old['add'], old['power']
decompose, substitute, alt = old['decompose'], old['substitute'], old['alt']
counts = Counter()


def ck(x, label):
    assert x, label
    counts[label] += 1


BOUND = 16
cs = old['character_table'](2 * BOUND)
records = []
for N in range(1, BOUND + 1):
    for a in range(N + 1):
        for c in range(N + 1):
            dec = decompose(mul(cs[a, N - a], cs[N - c, c]), cs)
            ck(all(v >= 0 for v in dec.values()), 'cross_tensor_nonnegative_coefficients')
            for k in range(1, N // 2 + 1):
                if min(a, N - a, c, N - c) < k - 1:
                    continue
                delta = a - c
                if delta == 0:
                    expected = k + int(min(a, N - a) >= k)
                elif delta % 3:
                    expected = 0
                else:
                    expected = max(0, k - 2 * abs(delta // 3) + 1)
                actual = dec.get((k, k), 0)
                ck(actual == expected, 'stable_strip_cross_multiplicity')
                toeplitz = k + 1 if delta == 0 else (
                    max(0, k - 2 * abs(delta // 3) + 1) if delta % 3 == 0 else 0)
                boundary = int(delta == 0 and min(a, N - a) == k - 1)
                ck(actual == toeplitz - boundary, 'boundary_mass_matrix_identity')
                records.append([N, a, c, k, actual])

# A positive definite non-diagonal Gram matrix can have zero off-diagonal
# band sums. The proof must use the subsequent integral boundary moments.
M = [[F(1, 3), F(1, 10), F(0)],
     [F(1, 10), F(1, 3), F(-1, 10)],
     [F(0), F(-1, 10), F(1, 3)]]
ck(sum(M[i][i] for i in range(3)) == 1, 'non_diagonal_control_trace')
ck(M[0][0] > 0 and M[0][0] * M[1][1] - M[0][1] ** 2 > 0,
   'non_diagonal_control_first_two_sylvester_minors')
det = M[0][0] * M[1][1] * M[2][2] - M[0][0] * M[1][2] ** 2 - M[2][2] * M[0][1] ** 2
ck(det == F(41, 1350) > 0, 'non_diagonal_control_determinant')
for delta in (1, 2):
    ck(sum(M[a + delta][a] for a in range(3 - delta)) == 0,
       'non_diagonal_control_zero_band_sum')
f = {}
for a in range(3):
    for c in range(3):
        f = add(f, mul(cs[a, 2 - a], cs[2 - c, c]), M[a][c])
fd = decompose(f, cs)
ck(fd.get((1, 1)) == F(4, 3), 'boundary_moment_detects_nonintegrality')
ck(any(x.denominator > 1 for x in fd.values()), 'non_diagonal_control_not_virtual_integral')

# Explicit positive virtual character outside the Hermitian polynomial-SOS
# cone: the Weyl discriminant has Haar mean 15, not 1.
unit = {(0, 0): 1}
u, v = {(1, 0): 1}, {(0, 1): 1}
x, y = mul(u, v), add(power(u, 3), power(v, 3))
discriminant = add(add(add({}, unit, 27), x, -18), y, 4)
discriminant = add(discriminant, power(x, 2), -1)
expected = {(0, 0): 15, (1, 1): -6, (3, 0): 3, (0, 3): 3, (2, 2): -1}
ck(decompose(discriminant, cs) == expected, 'discriminant_irreducible_expansion')
trace = {(1, 0): 1, (0, 1): 1, (-1, -1): 1}
tracebar = {(-i, -j): c for (i, j), c in trace.items()}
up = [power(trace, n) for n in range(5)]
vp = [power(tracebar, n) for n in range(5)]
den = alt((2, 1, 0))
denbar = {(-i, -j): c for (i, j), c in den.items()}
ck(substitute(discriminant, up, vp) == mul(den, denbar), 'discriminant_global_torus_square')
ck(sum(c * 4 ** (i + j) for (i, j), c in discriminant.items()) == -5,
   'discriminant_negative_outside_trace_domain')
ck(expected[(0, 0)] == 15, 'discriminant_haar_mean_not_one')

print(json.dumps({
    'status': 'PASS_EXACT_HERMITIAN_SOS_CONTROLS',
    'completed_substantive_author_turns': 5,
    'original_status': 'exhausted_unresolved',
    'new_assertions': sum(counts.values()),
    'counts': dict(sorted(counts.items())),
    'prior_turn4_assertions_rerun': prior_receipt['assertions'],
    'cross_tensor_height_bound': BOUND,
    'cross_tensor_products_checked': sum((N + 1) ** 2 for N in range(1, BOUND + 1)),
    'stable_strip_entries_checked': len(records),
    'stable_strip_record_sha256': hashlib.sha256(json.dumps(records, separators=(',', ':')).encode()).hexdigest(),
    'scope': 'All-weight Hermitian-SOS theorem is proved in TURN_5.md. These finite controls verify algebra and a genuine non-SOS obstruction of Haar mean 15; they do not classify all pointwise nonnegative mean-one virtual characters.',
}, indent=2, sort_keys=True))
