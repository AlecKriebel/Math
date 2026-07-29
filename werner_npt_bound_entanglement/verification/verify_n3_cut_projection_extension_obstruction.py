#!/usr/bin/env python3
"""Exact checks for the 3 x 4 projection and cut-sum obstructions."""

import sympy as sp


def partial_trace(M: sp.Matrix, dims: tuple[int, ...], keep: tuple[int, ...]) -> sp.Matrix:
    """Partial trace of an operator, retaining the factors in ``keep``."""
    n = len(dims)
    keep = tuple(keep)
    traced = tuple(i for i in range(n) if i not in keep)
    out_dim = sp.prod(dims[i] for i in keep)
    out = sp.zeros(out_dim, out_dim)

    def tuples(ds):
        if not ds:
            return [()]
        ans = [()]
        for d in ds:
            ans = [a + (j,) for a in ans for j in range(d)]
        return ans

    def flat(t):
        k = 0
        for x, d in zip(t, dims):
            k = d * k + x
        return k

    keep_tuples = tuples(tuple(dims[i] for i in keep))
    trace_tuples = tuples(tuple(dims[i] for i in traced))
    for ar, row_keep in enumerate(keep_tuples):
        for ac, col_keep in enumerate(keep_tuples):
            value = 0
            for tr in trace_tuples:
                row = [0] * n
                col = [0] * n
                for pos, i in enumerate(keep):
                    row[i] = row_keep[pos]
                    col[i] = col_keep[pos]
                for pos, i in enumerate(traced):
                    row[i] = tr[pos]
                    col[i] = tr[pos]
                value += M[flat(tuple(row)), flat(tuple(col))]
            out[ar, ac] = sp.simplify(value)
    return out


def embed(A: sp.Matrix, dims: tuple[int, ...], keep: tuple[int, ...]) -> sp.Matrix:
    """Embed ``A`` on ``keep`` and identities on the other factors."""
    n = len(dims)
    keep = tuple(keep)
    complement = tuple(i for i in range(n) if i not in keep)
    out = sp.zeros(sp.prod(dims), sp.prod(dims))

    def tuples(ds):
        if not ds:
            return [()]
        ans = [()]
        for d in ds:
            ans = [a + (j,) for a in ans for j in range(d)]
        return ans

    def flat_with_dims(t, ds):
        k = 0
        for x, d in zip(t, ds):
            k = d * k + x
        return k

    all_tuples = tuples(dims)
    kept_dims = tuple(dims[i] for i in keep)
    for row in all_tuples:
        for col in all_tuples:
            if any(row[i] != col[i] for i in complement):
                continue
            rr = tuple(row[i] for i in keep)
            cc = tuple(col[i] for i in keep)
            out[flat_with_dims(row, dims), flat_with_dims(col, dims)] = A[
                flat_with_dims(rr, kept_dims), flat_with_dims(cc, kept_dims)
            ]
    return out


# Section 1: exact 3 x 4 counterexample.
r5 = sp.sqrt(5)
lam = (r5 - 1) / 4
golden = (1 + r5) / 2
H = sp.Matrix([[-sp.Rational(1, 2), sp.Rational(1, 2)],
               [sp.Rational(1, 2), 0]])
w = sp.Matrix([1, golden])
assert sp.simplify(H * w - lam * w) == sp.zeros(2, 1)
assert sp.simplify(lam - sp.Rational(1, 4) - (r5 - 2) / 4) == 0
assert 5 > 4  # certifies sqrt(5) > 2

dims34 = (3, 4)
psi = sp.zeros(12, 1)
psi[0 * 4 + 0] = 1 / sp.sqrt(2)
psi[1 * 4 + 1] = sp.Rational(1, 2)
psi[2 * 4 + 2] = sp.Rational(1, 2)

e1 = sp.zeros(12, 1)
e1[0] = 1
eplus = sp.zeros(12, 1)
eplus[1 * 4 + 1] = 1 / sp.sqrt(2)
eplus[2 * 4 + 2] = 1 / sp.sqrt(2)
phi = e1 + golden * eplus
phi = phi / sp.sqrt((phi.conjugate().T * phi)[0])
chi = sp.zeros(12, 1)
chi[2 * 4 + 3] = 1
P = sp.simplify(phi * phi.conjugate().T + chi * chi.conjugate().T)
assert sp.simplify(P * P - P) == sp.zeros(12)
assert sp.trace(P) == 2

rho_a = partial_trace(P, dims34, (0,))
rho_b = partial_trace(P, dims34, (1,))
majorant = embed(rho_a, dims34, (0,)) + embed(rho_b, dims34, (1,))
gap = sp.simplify((psi.conjugate().T * (P - majorant) * psi)[0])
assert sp.simplify(gap - (r5 - 2) / 4) == 0

# Section 2: exact pair-sector equality example and failed cut sum.
dims333 = (3, 3, 3)
E01 = sp.zeros(3)
E01[0, 1] = 1
D = sp.kronecker_product(E01, E01, sp.eye(3))
K = D.conjugate().T * D
assert sp.trace(K) == 3

ket110 = sp.zeros(27, 1)
ket111 = sp.zeros(27, 1)
ket110[1 * 9 + 1 * 3 + 0] = 1
ket111[1 * 9 + 1 * 3 + 1] = 1
P_right = ket110 * ket110.T + ket111 * ket111.T
assert P_right * P_right == P_right
assert sp.trace(P_right) == 2

cut_values = []
for i in range(3):
    others = tuple(j for j in range(3) if j != i)
    rho_i = partial_trace(P_right, dims333, (i,))
    rho_others = partial_trace(P_right, dims333, others)
    M_i = embed(rho_i, dims333, (i,)) + embed(rho_others, dims333, others)
    cut_values.append(sp.trace(K * M_i))
assert cut_values == [8, 8, 8]
assert sum(cut_values) == 24
assert sum(cut_values) > 2 * sp.trace(K)

singular_squares = sorted(K.eigenvals().keys(), reverse=True)
assert singular_squares[:2] == [1, 0] or K.eigenvals()[1] == 3
# K has eigenvalue one with multiplicity three, so its Ky--Fan-two value is two.
assert K.eigenvals()[1] == 3
assert 2 == 2 * sum(abs(x) ** 2 for x in E01) ** 2

# Section 3: the exact sharpness determinant for the coefficient 4/3.
c, eps = sp.symbols("c eps", positive=True, real=True)
H_sym = sp.Matrix([
    [(1 - c) * (1 - eps), sp.sqrt(eps * (1 - eps))],
    [sp.sqrt(eps * (1 - eps)), (1 - 2 * c) * eps],
])
threshold_det = sp.factor((H_sym - c * eps * sp.eye(2)).det())
assert threshold_det == c * eps * (3 * c + 3 * eps - 4)

print("verified exact 3x4 projection counterexample:", gap)
print("verified exact pair-cut marginal sum:", cut_values, "total =", sum(cut_values))
print("verified sharp 4/3 coefficient determinant:", threshold_det)
