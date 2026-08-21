"""Exact audit of the four-copy local-effect Hessian on a sparse code.

The calculation uses SymPy only for exact Gaussian-rational arithmetic.
It reconstructs the Hessian from the two codewords, rather than trusting
the displayed matrices in the accompanying note.
"""

from itertools import combinations

import sympy as sp


R = sp.Rational
I = sp.I

U = {
    (1, 2, 2, 1): -1 / sp.sqrt(3),
    (2, 0, 2, 2): 1 / sp.sqrt(3),
    (1, 2, 0, 2): 1 / sp.sqrt(3),
}
V = {
    (1, 1, 2, 2): 1 / sp.sqrt(3),
    (1, 0, 2, 2): -1 / sp.sqrt(3),
    (0, 2, 0, 2): 1 / sp.sqrt(3),
}
CODE = (U, V)


def hermitian_basis():
    """Rational coordinate basis for Herm(3).

    The order is
      d0,d1,d2, Re01,Im01, Re02,Im02, Re12,Im12.
    Off-diagonal basis vectors are intentionally not HS-normalized;
    this does not affect inertia.
    """

    out = []
    for a in range(3):
        matrix = sp.zeros(3)
        matrix[a, a] = 1
        out.append(matrix)
    for a, b in ((0, 1), (0, 2), (1, 2)):
        matrix = sp.zeros(3)
        matrix[a, b] = matrix[b, a] = 1
        out.append(matrix)
        matrix = sp.zeros(3)
        matrix[a, b] = I
        matrix[b, a] = -I
        out.append(matrix)
    return out


BASIS = hermitian_basis()


def pair_state(r, s):
    """Sparse state u_r tensor u_s, including its exact normalization."""

    return {
        x + y: ax * ay
        for x, ax in CODE[r].items()
        for y, ay in CODE[s].items()
    }


PAIRS = {(r, s): pair_state(r, s) for r in range(2) for s in range(2)}


def inserted_swap_expectation(a, b, swapped_sites, r, s):
    """<u_r u_s|(a tensor b)_site0 F_S|u_r u_s> exactly."""

    state = PAIRS[r, s]
    value = 0
    for ket, ket_amplitude in state.items():
        swapped = list(ket)
        for site in swapped_sites:
            swapped[site], swapped[4 + site] = (
                swapped[4 + site],
                swapped[site],
            )
        left_input = swapped[0]
        right_input = swapped[4]
        for left_output in range(3):
            a_entry = a[left_output, left_input]
            if a_entry == 0:
                continue
            for right_output in range(3):
                b_entry = b[right_output, right_input]
                if b_entry == 0:
                    continue
                bra = tuple(
                    [left_output]
                    + swapped[1:4]
                    + [right_output]
                    + swapped[5:8]
                )
                bra_amplitude = state.get(bra)
                if bra_amplitude is not None:
                    value += (
                        sp.conjugate(bra_amplitude)
                        * ket_amplitude
                        * a_entry
                        * b_entry
                    )
    return sp.simplify(value)


def hessian_bilinear(a, b):
    """Polarization of N(A)=Tr[(P⊗P)(A⊗A)_1 K_4]."""

    value = 0
    for size in range(5):
        for swapped_sites in combinations(range(4), size):
            coefficient = R(-1, 2) ** (4 - size)
            for r in range(2):
                for s in range(2):
                    value += coefficient * (
                        inserted_swap_expectation(
                            a, b, swapped_sites, r, s
                        )
                        + inserted_swap_expectation(
                            b, a, swapped_sites, r, s
                        )
                    ) / 2
    return sp.simplify(value)


N = sp.Matrix(
    9, 9, lambda row, col: hessian_bilinear(BASIS[row], BASIS[col])
)

EXPECTED_N = sp.Matrix(
    [
        [R(1, 144), R(1, 12), -R(1, 144), 0, 0, 0, 0, 0, 0],
        [R(1, 12), R(1, 6), R(7, 72), 0, 0, 0, 0, 0, 0],
        [-R(1, 144), R(7, 72), R(1, 144), 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, -R(1, 18), 0],
        [0, 0, 0, 0, 0, 0, 0, 0, -R(1, 18)],
        [0, 0, 0, 0, 0, R(1, 36), 0, 0, 0],
        [0, 0, 0, 0, 0, 0, R(1, 36), 0, 0],
        [0, 0, 0, -R(1, 18), 0, 0, 0, -R(1, 18), 0],
        [0, 0, 0, 0, -R(1, 18), 0, 0, 0, -R(1, 18)],
    ]
)
assert N == EXPECTED_N


def compression_matrix():
    """Matrix of A -> U^*(A tensor I)U in Hermitian coordinates."""

    out = sp.zeros(4, 9)
    for column, a in enumerate(BASIS):
        logical = sp.zeros(2)
        for r in range(2):
            for s in range(2):
                entry = 0
                for x, ax in CODE[r].items():
                    for y, ay in CODE[s].items():
                        if x[1:] == y[1:]:
                            entry += (
                                sp.conjugate(ax) * ay * a[x[0], y[0]]
                            )
                logical[r, s] = sp.simplify(entry)
        out[0, column] = logical[0, 0]
        out[1, column] = logical[1, 1]
        out[2, column] = (logical[0, 1] + logical[1, 0]) / 2
        out[3, column] = (logical[0, 1] - logical[1, 0]) / (2 * I)
    return out


C = compression_matrix()
assert C.rank() == 4

KERNEL_BASIS = sp.Matrix(
    [
        [1, 0, 0, 0, 0],
        [-R(1, 2), 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1],
    ]
)
assert C * KERNEL_BASIS == sp.zeros(4, 5)

RESTRICTED = sp.simplify(KERNEL_BASIS.T * N * KERNEL_BASIS)
assert RESTRICTED == sp.diag(
    -R(5, 36), R(1, 36), R(1, 36), -R(1, 6), -R(1, 6)
)

identity = sp.Matrix([1, 1, 1, 0, 0, 0, 0, 0, 0])
assert (identity.T * N * identity)[0] == R(19, 36)
assert N.det() == -R(169, 101559956668416)

# The three diagonal/off-diagonal blocks give the full inertia directly.
diagonal_block = N[:3, :3]
assert diagonal_block[0, 0] > 0
assert diagonal_block[:2, :2].det() < 0
assert diagonal_block.det() < 0
# Thus its LDL signs are +,-,+: inertia (2+,1-).
# Each [[0,-1/18],[-1/18,-1/18]] block has negative determinant:
# inertia (1+,1-).  The two remaining entries 1/36 are positive.
# Total inertia(N)=(6+,3-).

print("verified: rank(C)=4, inertia(N)=(6+,3-), inertia(N|ker C)=(2+,3-)")


def rebuild(code):
    """Rebuild N and C after replacing the sparse normalized code."""

    global CODE, PAIRS
    CODE = code
    PAIRS = {
        (r, s): pair_state(r, s) for r in range(2) for s in range(2)
    }
    hessian = sp.Matrix(
        9,
        9,
        lambda row, col: hessian_bilinear(BASIS[row], BASIS[col]),
    )
    return hessian, compression_matrix()


HS_METRIC = sp.diag(1, 1, 1, 2, 2, 2, 2, 2, 2)
z = sp.symbols("z", real=True)

# Exact counterexample to tr(N|ker C) <= F/8.
trace_code = (
    {
        (1, 0, 0, 1): 1 / sp.sqrt(6),
        (1, 0, 2, 2): 1 / sp.sqrt(6),
        (2, 2, 0, 2): 2 / sp.sqrt(6),
    },
    {
        (0, 0, 2, 2): 2 / sp.sqrt(5),
        (0, 2, 2, 0): 1 / sp.sqrt(5),
    },
)
N_TRACE, C_TRACE = rebuild(trace_code)
assert C_TRACE.rank() == 4
K_TRACE = sp.Matrix.hstack(*C_TRACE.nullspace())
R_TRACE = sp.simplify(K_TRACE.T * N_TRACE * K_TRACE)
G_TRACE = sp.simplify(K_TRACE.T * HS_METRIC * K_TRACE)
assert sp.simplify(sp.factor((R_TRACE - z * G_TRACE).det()) - (
    -R(5, 209952)
    * (12 * z - 1) ** 2
    * (18 * z + 1)
    * (36 * z + 1) ** 2
)) == 0
trace_restriction = sp.factor(sp.trace(G_TRACE.inv() * R_TRACE))
identity = sp.Matrix([1, 1, 1, 0, 0, 0, 0, 0, 0])
endpoint = sp.factor((identity.T * N_TRACE * identity)[0])
assert trace_restriction == R(1, 18)
assert endpoint == R(121, 450)
assert trace_restriction - endpoint / 8 == R(79, 3600)

# Exact counterexample to det(N|ker C) <= 0.
determinant_code = (
    {
        (1, 2, 1, 2): -I / sp.sqrt(2),
        (0, 0, 1, 0): 1 / sp.sqrt(2),
    },
    {
        (2, 2, 1, 2): I / sp.sqrt(5),
        (0, 1, 1, 1): (-1 + I) / sp.sqrt(5),
        (1, 1, 1, 1): (1 - I) / sp.sqrt(5),
    },
)
N_DET, C_DET = rebuild(determinant_code)
assert C_DET.rank() == 4
K_DET = sp.Matrix.hstack(*C_DET.nullspace())
R_DET = sp.simplify(K_DET.T * N_DET * K_DET)
G_DET = sp.simplify(K_DET.T * HS_METRIC * K_DET)
assert sp.simplify(sp.factor((R_DET - z * G_DET).det()) - (
    -R(3, 102400000000)
    * (160 * z - 3)
    * (160 * z + 7)
    * (400 * z - 1) ** 2
    * (2400 * z + 59)
)) == 0
assert R_DET.det() > 0
assert (identity.T * N_DET * identity)[0] == R(163, 400)

print("verified: the crossed-kernel trace and determinant sign shortcuts fail")
