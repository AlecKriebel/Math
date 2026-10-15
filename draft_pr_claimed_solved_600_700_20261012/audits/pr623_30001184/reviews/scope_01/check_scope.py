"""Independent finite-matrix sanity checks. Analytic proofs are in DEDUCTIONS.md.

No dependencies, no network, no candidate imports. Run: python3 check_scope.py.
"""
from math import acos, cos, exp, log, sin, sqrt
from decimal import Decimal, localcontext
import json

def matmul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))

def adjoint(a):
    return tuple(tuple(a[j][i].conjugate() if isinstance(a[j][i], complex)
                       else a[j][i] for j in range(2)) for i in range(2))

def sub(a, b):
    return tuple(tuple(a[i][j] - b[i][j] for j in range(2)) for i in range(2))

def scale(a, r):
    return tuple(tuple(r * a[i][j] for j in range(2)) for i in range(2))

def error(a, b):
    return max(abs(a[i][j] - b[i][j]) for i in range(2) for j in range(2))

def rotation(z):
    return ((cos(z), -sin(z)), (sin(z), cos(z)))

def g(x):
    return 0.0 if x <= 0 else acos(exp(-x)) / 2

def cocycle(t, x):
    return matmul(adjoint(rotation(g(x))), rotation(g(x + t)))

q = ((1., 0.), (0., 0.))

def shifted_q(t, x):
    u = cocycle(t, x)
    return matmul(matmul(u, q), adjoint(u))

def transition(t):
    return (((1 + exp(-t))/2, (1 - exp(-t))/2),
            ((1 - exp(-t))/2, (1 + exp(-t))/2))

s = log(2)
Q = ((3/4, sqrt(3)/4), (sqrt(3)/4, 1/4))
d = 3*(sqrt(5) - 1)/16

def witness(x):
    return sub(matmul(matmul(q, shifted_q(s, x)), q), scale(q, 3/4))

u = cocycle(s, 0)
evolved = matmul(matmul(u, witness(s)), adjoint(u))
time_values = (0., 1e-6, 0.01, 0.3, s, 2., 20.)
space_values = (-20., -1., 0., 0.01, s, 2., 20.)
cocycle_error = max(error(matmul(cocycle(t, x), cocycle(r, x+t)),
                         cocycle(t+r, x))
                     for x in space_values for t in time_values for r in time_values)
markov_error = max(error(matmul(transition(t), transition(r)), transition(t+r))
                   for t in time_values for r in time_values)
compression_error = max(abs(shifted_q(t, 0)[i][i] - transition(t)[i][0])
                        for t in time_values for i in range(2))

# Keep the base-flow sums exact in 50-digit decimal arithmetic, then evaluate
# the same real rotations. This separates input associativity from the
# matrix cocycle identity and independently confirms the source of the error.
def cocycle_exact_inputs(t, x):
    return matmul(adjoint(rotation(g(float(x)))), rotation(g(float(x+t))))

with localcontext() as ctx:
    ctx.prec = 50
    exact_times = tuple(Decimal(repr(t)) for t in time_values)
    exact_spaces = tuple(Decimal(repr(x)) for x in space_values)
    stable_cocycle_error = max(
        error(matmul(cocycle_exact_inputs(t, x), cocycle_exact_inputs(r, x+t)),
              cocycle_exact_inputs(t+r, x))
        for x in exact_spaces for t in exact_times for r in exact_times)
assert error(shifted_q(s, 0), Q) < 1e-14
assert error(witness(0), ((0., 0.), (0., 0.))) < 1e-14
assert error(witness(s), scale(q, d)) < 1e-14
assert error(evolved, scale(Q, d)) < 1e-14
# Input sums near x+t=0 lose a few ulps through cancellation. g has a
# square-root cusp there, so an ulp in an input can amplify to ~1e-13 in
# the angle. The conservative 1e-11 cocycle bound records that sensitivity;
# the exact algebraic telescoping proof does not have this limitation.
assert cocycle_error < 1e-11 and markov_error < 1e-13 and compression_error < 1e-13
assert stable_cocycle_error < 1e-14
assert d > 0.23

# Infinitesimal projection identity for an independent Hermitian matrix.
# A derivation q -> i[H,q] has exactly zero diagonal, but T'_0(q) does not.
H = ((1., 2.+3.j), (2.-3.j, -4.))
commutator = sub(matmul(H, q), matmul(q, H))
delta_q = scale(commutator, 1.j)
assert delta_q[0][0] == delta_q[1][1] == 0

result = {
    'kind': 'numerical sanity checks supplementing exact independent deductions',
    'sampled_cocycle_max_error': cocycle_error,
    'sampled_cocycle_exact_decimal_input_sums_max_error': stable_cocycle_error,
    'sampled_markov_semigroup_max_error': markov_error,
    'sampled_compression_max_error': compression_error,
    'exact_witness_positive_coefficient_formula': '3*(sqrt(5)-1)/16',
    'witness_positive_coefficient_numeric': d,
    'evolved_witness_at_zero': evolved,
    'evolved_gns_squared_norm_diagonal': [3*d*d/4, d*d/4],
    'projection_derivation_diagonal': [0, 0],
    'target_markov_derivative_diagonal': [-0.5, 0.5],
    'status': 'all_assertions_passed',
    'cocycle_tolerance': 1e-11,
    'rounding_note': 'Associative input sums differ in floating arithmetic near the square-root cusp at zero; angle sensitivity amplifies cancellation.',
    'limitations': 'Finite numerical samples do not prove continuum identities; proofs do.'
}
print(json.dumps(result, indent=2))
