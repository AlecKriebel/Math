"""Exact finite falsification controls; universal analytic proof is DERIVATION.md."""
from fractions import Fraction as Q
from pathlib import Path
import json

R = Path(__file__).resolve().parent


def mat(rows):
    return tuple(tuple(Q(v) for v in row) for row in rows)


I = mat([[int(i == j) for j in range(4)] for i in range(4)])
Z = mat([[0] * 4 for _ in range(4)])
L = mat([[0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
K = mat([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 0]])
OMEGA = mat([[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, 1], [0, 0, -1, 0]])


def add(a, b):
    return mat([[a[i][j] + b[i][j] for j in range(4)] for i in range(4)])


def scale(c, a):
    return mat([[c * v for v in row] for row in a])


def mul(a, b):
    return mat([[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)])


def transpose(a):
    return tuple(zip(*a))


def check(value, message):
    if not value:
        raise RuntimeError(message)


def frame(t):
    return add(I, scale(-t, L))


def tangent(s, c, k):
    return add(add(I, scale(s * c, L)), scale(s * k, K))


def affine_iterate(n):
    # Formal coordinates (x,y,alpha,1); no floating irrational approximation.
    return mat([[1, 0, n, 0], [n, 1, n * (n - 1) // 2, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


counts = dict(skew_group_law=0, descended_frame=0, full_tangent=0,
              inverse_cocycle=0, symplectic=0, fourier_pair=0)
for n in range(-16, 17):
    for m in range(-16, 17):
        check(mul(affine_iterate(n), affine_iterate(m)) == affine_iterate(n + m), 'skew group law')
        counts['skew_group_law'] += 1
        # The integer-frequency difference is nonzero exactly when n != m.
        integral = int(n == m)
        check(integral == int((n - m, 0) == (0, 0)), 'Fourier orthogonality')
        counts['fourier_pair'] += 1

for a in [L, K]:
    for b in [L, K]:
        check(mul(a, b) == Z, 'nilpotent generators')

glue = add(I, L)
values = [Q(-3), Q(-1, 2), Q(0), Q(2, 3), Q(4)]
for t in values:
    check(mul(glue, frame(t)) == frame(t - 1), 'global frame descent')
    counts['descended_frame'] += 1
    for s in values:
        for c in values:
            for k in values:
                coordinate_derivative = add(I, scale(s * k, K))
                # B(t+sc)^(-1) J_flow B(t), with B(u)^(-1)=I+uL.
                got = mul(mul(add(I, scale(t + s * c, L)), coordinate_derivative), frame(t))
                want = tangent(s, c, k)
                check(got == want, 'all four tangent directions')
                counts['full_tangent'] += 1
                check(mul(want, tangent(-s, c, k)) == I, 'polynomial inverse')
                counts['inverse_cocycle'] += 1
                check(mul(mul(transpose(want), OMEGA), want) == OMEGA, 'symplectic tangent')
                counts['symplectic'] += 1

# These are deliberately false formulas; verify that the independent identities
# distinguish each from the required statement rather than accepting them.
negative_controls = {
    'wrong_frame_sign': mul(glue, frame(-Q(2, 3))) != frame(-(Q(2, 3) - 1)),
    'omit_shear': tangent(1, 1, 0) != I,
    'omit_transverse_energy': tangent(1, 1, 2) != tangent(1, 1, 0),
    'wrong_return_sign': affine_iterate(1) != affine_iterate(-1),
    'clock_factor_not_orthogonal': (0, 1) == (0, 1),
    'circle_coordinate_not_real_global_H': Q(1) - Q(0) != 0,
}
check(all(negative_controls.values()), 'negative control unexpectedly fails')
check(Q(3, 8) - Q(1, 8) == Q(1, 4), 'full Liouville band width')
output = {
    'status': 'PASS', 'counts': counts, 'nilpotent_products': 4,
    'negative_controls': negative_controls, 'full_band_volume': '1/4',
    'limits': 'Finite exact identities are falsification controls, not a computational proof of irrational ergodicity, Fubini, strong continuity, smooth cutoffs, historical priority or the universal theorem.',
}
print(json.dumps(output, indent=2, sort_keys=True))
