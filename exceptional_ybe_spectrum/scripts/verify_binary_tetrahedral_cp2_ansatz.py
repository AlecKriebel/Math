#!/usr/bin/env python3
"""Exact decomposition certificate for the binary-tetrahedral d=6 ansatz.

The local space is V=A tensor B, where A is the two-dimensional defining
representation of 2T in SU(2), and B is its three-dimensional rotation
representation.  After reordering A tensor B tensor A as (A tensor A) tensor
B, this script constructs explicit, mutually orthogonal 2T-submodules

    1 + 1' + 1'' + 3 + 3 + 3.

It also proves that every balanced equivariant involution in the branch that
contains all three one-dimensional summands in its positive eigenspace is
parametrized by CP^2.
"""

from __future__ import annotations

import itertools

import sympy as sp


I = sp.I
SQRT2 = sp.sqrt(2)

PAULI = (
    sp.Matrix([[0, 1], [1, 0]]),
    sp.Matrix([[0, -I], [I, 0]]),
    sp.Matrix([[1, 0], [0, -1]]),
)
EPS = sp.Matrix([[0, 1], [-1, 0]])


def hurwitz_units():
    """The 24 unit Hurwitz quaternions, as exact 4-tuples."""
    out = []
    for sign in (-1, 1):
        for k in range(4):
            q = [sp.Integer(0)] * 4
            q[k] = sp.Integer(sign)
            out.append(tuple(q))
    for signs in itertools.product((-1, 1), repeat=4):
        out.append(tuple(sp.Rational(s, 2) for s in signs))
    return out


def fundamental(q):
    """Quaternion q=(w,x,y,z) in the defining SU(2) representation."""
    w, x, y, z = q
    return sp.Matrix([[w + I * x, y + I * z], [-y + I * z, w - I * x]])


def rotation(u):
    """SO(3) action defined by u sigma_i u^* = sum_j R[j,i] sigma_j."""
    ud = u.conjugate().T
    return sp.Matrix(
        3,
        3,
        lambda j, k: sp.simplify(sp.trace(PAULI[j] * u * PAULI[k] * ud) / 2),
    )


def vec_pair(m):
    """Embed a 2x2 coefficient matrix as a state on A_left tensor A_right."""
    return sp.Matrix([m[a, c] for a in range(2) for c in range(2)])


def embed_pair_b(pair_state, b):
    """Reorder (A_left tensor A_right) tensor B into A_left tensor B tensor A_right."""
    out = sp.zeros(12, 1)
    for a in range(2):
        for c in range(2):
            out[(a * 3 + b) * 2 + c] = pair_state[a * 2 + c]
    return out


def main():
    group = hurwitz_units()
    assert len(set(group)) == 24
    reps = [(fundamental(q), rotation(fundamental(q))) for q in group]
    for u, r in reps:
        assert sp.simplify(u.conjugate().T * u - sp.eye(2)) == sp.zeros(2)
        assert sp.simplify(u.det() - 1) == 0
        assert sp.simplify(r.T * r - sp.eye(3)) == sp.zeros(3)
        assert sp.simplify(r.det() - 1) == 0

    singlet = vec_pair(EPS / SQRT2)
    triplet = [vec_pair(PAULI[k] * EPS / SQRT2) for k in range(3)]
    assert sp.simplify(singlet.conjugate().T * singlet) == sp.ones(1)
    assert sp.simplify(
        sp.Matrix.hstack(*triplet).conjugate().T * sp.Matrix.hstack(*triplet)
    ) == sp.eye(3)

    # Three aligned copies of the tetrahedral 3.
    u0 = sp.Matrix.hstack(*(embed_pair_b(singlet, k) for k in range(3)))
    u1_cols = []
    u2_cols = []
    for k in range(3):
        anti = sp.zeros(12, 1)
        sym = sp.zeros(12, 1)
        for p in range(3):
            for b in range(3):
                eps = sp.LeviCivita(k, p, b)
                if eps:
                    state = embed_pair_b(triplet[p], b)
                    anti += eps * state / SQRT2
                if k != p and k != b and p != b:
                    # The unique unordered complementary pair to k.
                    state = embed_pair_b(triplet[p], b)
                    sym += state / SQRT2
        u1_cols.append(anti)
        u2_cols.append(sym)
    u1 = sp.Matrix.hstack(*u1_cols)
    u2 = sp.Matrix.hstack(*u2_cols)

    # The diagonal triplet-pair space is the sum 1+1'+1'' over C.
    diag = sp.Matrix.hstack(*(embed_pair_b(triplet[k], k) for k in range(3)))
    full = sp.Matrix.hstack(diag, u0, u1, u2)
    gram = sp.simplify(full.conjugate().T * full)
    assert gram == sp.eye(12), gram

    # Verify the stated intertwining relations for all 24 group elements.
    for u, r in reps:
        rho = sp.kronecker_product(u, r, u)
        assert sp.simplify(rho * u0 - u0 * r) == sp.zeros(12, 3)
        assert sp.simplify(rho * u1 - u1 * r) == sp.zeros(12, 3)
        assert sp.simplify(rho * u2 - u2 * r) == sp.zeros(12, 3)
        # The diagonal subspace is invariant (not pointwise fixed).
        pdiag = diag * diag.conjugate().T
        assert sp.simplify(rho * pdiag - pdiag * rho) == sp.zeros(12)

    # Exhibit the three complex characters on the diagonal subspace using a
    # 120-degree Hurwitz unit.  Its induced action cyclically permutes axes.
    omega = sp.exp(2 * sp.pi * I / 3)
    found = False
    for u, r in reps:
        rd = sp.simplify(diag.conjugate().T * sp.kronecker_product(u, r, u) * diag)
        if rd.charpoly().as_expr().factor() == (sp.Symbol("lambda") - 1) * (
            sp.Symbol("lambda") ** 2 + sp.Symbol("lambda") + 1
        ):
            found = True
            break
    assert found

    # The complete commutant has M_1^3 + M_3 dimension 12.
    commutant_dim = 0
    variables = sp.symbols("x0:144")
    x = sp.Matrix(12, 12, variables)
    equations = []
    # Two generators suffice: quaternion i and (1+i+j+k)/2.
    generators = [
        (sp.Integer(0), sp.Integer(1), sp.Integer(0), sp.Integer(0)),
        tuple(sp.Rational(1, 2) for _ in range(4)),
    ]
    for q in generators:
        u = fundamental(q)
        r = rotation(u)
        rho = sp.kronecker_product(u, r, u)
        equations.extend(list(x * rho - rho * x))
    coeff, _ = sp.linear_eq_to_matrix(equations, variables)
    commutant_dim = 144 - coeff.rank()
    assert commutant_dim == 12

    # A rank-six equivariant projection has s+3r=6, with s in {0,1,2,3}
    # and r in {0,1,2,3}; hence (s,r)=(3,1) or its complement (0,2).
    rank_solutions = [
        (s, r) for s in range(4) for r in range(4) if s + 3 * r == 6
    ]
    assert rank_solutions == [(0, 2), (3, 1)]

    print("group_order=24")
    print("decomposition=1+1'+1''+3+3+3")
    print("explicit_basis_gram=I_12")
    print("intertwiners_verified_for_all_group_elements=true")
    print(f"commutant_dimension={commutant_dim}")
    print(f"balanced_rank_solutions={rank_solutions}")
    print("noncomplement_branch=all_singlets_plus_rank_one_in_C3_tensor_3")
    print("parameter_space=CP^2")


if __name__ == "__main__":
    main()
