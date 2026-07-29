#!/usr/bin/env python3
"""Exact checks of the anchored CP and crossing certificates.

The proof is dimension-independent within qubit tensor powers.  This
small verifier checks the matrix identities and the GHZ equality case.
It also checks the arbitrary-dimensional crossing and alternating
identities on a nontrivial exact qutrit example.
"""

import itertools

import sympy as sp


def kron_all(items):
    out = sp.ones(1, 1)
    for item in items:
        out = sp.kronecker_product(out, item)
    return out


# Local Hilbert--Schmidt/Choi projector.
phi = sp.Matrix([1, 0, 0, 1])
pi = sp.eye(4) - sp.Rational(1, 2) * phi * phi.T
assert pi.T == pi
assert pi * pi == pi

# Three local qubit factors.  This ordering is the regrouped local
# operator ordering; it is unitarily equivalent to ordinary vec order.
Pi = kron_all([pi, pi, pi])
assert Pi.T == Pi
assert Pi * Pi == Pi

# Unnormalized GHZ projector in the local operator basis
# (00, 01, 10, 11) at each site.
e0 = sp.Matrix([1, 0])
e1 = sp.Matrix([0, 1])
w_plus = kron_all([e0, e0, e0]) + kron_all([e1, e1, e1])
w_minus = kron_all([e0, e0, e0]) - kron_all([e1, e1, e1])
P = w_plus * w_plus.T


def local_operator_vec(matrix):
    """Vectorize and regroup (row sites, column sites) into local pairs."""

    out = sp.zeros(64, 1)
    for row in range(8):
        rb = ((row >> 2) & 1, (row >> 1) & 1, row & 1)
        for col in range(8):
            cb = ((col >> 2) & 1, (col >> 1) & 1, col & 1)
            local = tuple(2 * rb[i] + cb[i] for i in range(3))
            index = 16 * local[0] + 4 * local[1] + local[2]
            out[index] = matrix[row, col]
    return out


def local_operator_unvec(vector):
    out = sp.zeros(8, 8)
    for row in range(8):
        rb = ((row >> 2) & 1, (row >> 1) & 1, row & 1)
        for col in range(8):
            cb = ((col >> 2) & 1, (col >> 1) & 1, col & 1)
            local = tuple(2 * rb[i] + cb[i] for i in range(3))
            index = 16 * local[0] + 4 * local[1] + local[2]
            out[row, col] = vector[index]
    return out


p = local_operator_vec(P)
x = Pi * p
A = local_operator_unvec(x)
a = (p.T * x)[0]

assert Pi * x == x
assert (x.T * x)[0] == a

# The normalized Choi residual is itself an orthogonal projection.
residual_projection = Pi - x * x.T / a
assert residual_projection.T == residual_projection
assert residual_projection * residual_projection == residual_projection

# Exact even/odd copositive splitting after Choi partial transpose.
swap = sp.Matrix(
    [
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
    ]
)
sym = (sp.eye(4) + swap) / 2
antisym = (sp.eye(4) - swap) / 2
k_pt = kron_all([sp.eye(4) - swap / 2] * 3)
a_pt = kron_all([swap - sp.eye(4) / 2] * 3)
odd_sector_sum = sp.zeros(64, 64)
for mask in range(8):
    if bin(mask).count("1") % 2 == 0:
        continue
    factors = [
        antisym if (mask >> party) & 1 else sym
        for party in range(3)
    ]
    odd_sector_sum += (
        sp.Rational(1, 4)
        * 3 ** bin(mask).count("1")
        * kron_all(factors)
    )
assert k_pt - a_pt == odd_sector_sum

# The vectors are unnormalized, so P scales by two relative to the
# normalized convention.  The equality remains homogeneous.
assert A * w_minus == -w_minus
q_minus = sp.Rational(2)  # 4 times Q_3(P_{w_-}/2) = 4*(1/2)
cross_squared = (w_minus.T * A * w_minus)[0] ** 2
assert a == 2
assert cross_squared == a * q_minus

print("verified: exact three-qubit anchored CP projection and GHZ equality")


def digits(number, local, copies):
    answer = [0] * copies
    for position in range(copies - 1, -1, -1):
        answer[position] = number % local
        number //= local
    return tuple(answer)


def index(word, local):
    answer = 0
    for letter in word:
        answer = local * answer + letter
    return answer


def trace_and_replace(matrix, local, copies, traced):
    """Apply Tr_traced(.) tensor I_traced, preserving party order."""

    traced = tuple(sorted(traced))
    remaining = tuple(i for i in range(copies) if i not in traced)
    dimension = local**copies
    words = [digits(i, local, copies) for i in range(dimension)]
    out = sp.zeros(dimension, dimension)
    traced_words = tuple(
        itertools.product(range(local), repeat=len(traced))
    )
    for row_index, row_word in enumerate(words):
        for column_index, column_word in enumerate(words):
            if any(row_word[i] != column_word[i] for i in traced):
                continue
            value = 0
            for traced_word in traced_words:
                source_row = list(row_word)
                source_column = list(column_word)
                for party, letter in zip(traced, traced_word):
                    source_row[party] = letter
                    source_column[party] = letter
                value += matrix[
                    index(source_row, local), index(source_column, local)
                ]
            out[row_index, column_index] = value
    return out


def map_a(matrix, local, copies):
    out = sp.zeros(matrix.rows, matrix.cols)
    parties = tuple(range(copies))
    for size in range(copies + 1):
        for traced in itertools.combinations(parties, size):
            out += (
                sp.Rational(-1, 2) ** size
                * trace_and_replace(matrix, local, copies, traced)
            )
    return out


def map_k(matrix, local, copies):
    out = sp.zeros(matrix.rows, matrix.cols)
    parties = tuple(range(copies))
    for size in range(copies + 1):
        for retained in itertools.combinations(parties, size):
            traced = tuple(i for i in parties if i not in retained)
            out += (
                sp.Rational(-1, 2) ** size
                * trace_and_replace(matrix, local, copies, traced)
            )
    return out


def sparse_vector(local, copies, terms):
    out = sp.zeros(local**copies, 1)
    for word, coefficient in terms.items():
        out[index(word, local)] = coefficient
    return out


# A genuinely qutrit exact check of the crossing identity
# <t,A_xy z> = <y,K_xt z> and the alternating identity
# (A_xy-K_xy)z = -(A_zy-K_zy)x.
local = 3
copies = 3
x3 = sparse_vector(local, copies, {(0, 0, 0): 1, (1, 1, 1): 2})
y3 = sparse_vector(local, copies, {(0, 1, 2): 1, (1, 2, 0): -1})
z3 = sparse_vector(local, copies, {(2, 0, 1): 1, (0, 2, 1): 3})
t3 = sparse_vector(local, copies, {(1, 0, 2): 2, (2, 1, 0): -1})

Axy = map_a(x3 * y3.T, local, copies)
Kxt = map_k(x3 * t3.T, local, copies)
assert (t3.T * Axy * z3)[0] == (y3.T * Kxt * z3)[0]

Kxy = map_k(x3 * y3.T, local, copies)
Azy = map_a(z3 * y3.T, local, copies)
Kzy = map_k(z3 * y3.T, local, copies)
assert (Axy - Kxy) * z3 == -(Azy - Kzy) * x3

P3 = x3 * x3.T
assert map_a(P3, local, copies) * x3 == map_k(P3, local, copies) * x3

print("verified: exact qutrit crossing, diagonal, and exterior alternation")
