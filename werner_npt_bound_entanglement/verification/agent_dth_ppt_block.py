#!/usr/bin/env python3
"""Exact corrected mixed-support audit in the cloud obstruction block.

The block is the real binary carrier of the local
[4,1] x [4,1] x [3,2] S_5 type.  After pair antisymmetry, pair exchange,
and the first Pluecker equation, it is seven dimensional and lies in both
Omega kernels.

For an operator rho supported on this block, this verifier constructs the
linear map

    rho -> C_supp (rho ** Gamma_first_bivector)

exactly.  It proves injectivity by full modular column rank 49.  Hence the
mixed support equation alone forces rho=0 in this block; positivity and PPT
are not needed for this local exclusion.

Only the Python standard library is used.  Full rank modulo a prime is an
exact certificate of full rank over Q.
"""

from fractions import Fraction as F
from itertools import combinations
import sys

import agent_dth_five_block as fb


PRIME = 1_000_003


def source_project(v):
    """Project to Sym^2(Lambda^2 H), then remove Lambda^4 H."""
    t12 = fb.apply_global_perm(v, fb.transposition(0, 1))
    out = fb.scale(F(1, 2), fb.add(v, fb.scale(-1, t12)))
    t34 = fb.apply_global_perm(out, fb.transposition(2, 3))
    out = fb.scale(F(1, 2), fb.add(out, fb.scale(-1, t34)))
    pair_swap = fb.apply_global_perm(out, (2, 3, 0, 1, 4))
    out = fb.scale(F(1, 2), fb.add(out, pair_swap))
    return fb.add(out, fb.scale(-1, fb.global_A4(out)))


def physical_index(bits):
    k = 0
    for bit in bits:
        k = 2 * k + bit
    return k


def wedge_coordinates(v):
    """Coordinates in Lambda^2(H)_12 x Lambda^2(H)_34 x H_5.

    The input is already antisymmetric in pairs 12 and 34.  We retain the
    coefficient at the canonically ordered representative.  Omitting the
    common normalization factors does not affect any kernel or rank claim.
    """
    out = {}
    for key, x in v.items():
        st = tuple(physical_index(fb.replica_state(key, r)) for r in range(5))
        a, b, c, d, z = st
        if a < b and c < d:
            k = ((a, b), (c, d), z)
            out[k] = out.get(k, F(0)) + x
    return {k: x for k, x in out.items() if x}


def frac_mod(x, p=PRIME):
    return (x.numerator % p) * pow(x.denominator % p, -1, p) % p


def reduce_sparse_column(column, pivots, p=PRIME):
    """Reduce a rational sparse column modulo p against normalized pivots."""
    v = {k: frac_mod(x, p) for k, x in column.items() if frac_mod(x, p)}
    while v:
        pivot = min(v)
        if pivot not in pivots:
            inv = pow(v[pivot], -1, p)
            v = {k: (x * inv) % p for k, x in v.items() if (x * inv) % p}
            return pivot, v
        c = v[pivot]
        old = pivots[pivot]
        for k, x in old.items():
            y = (v.get(k, 0) - c * x) % p
            if y:
                v[k] = y
            elif k in v:
                del v[k]
    return None, {}


def select_independent(columns, target=None, p=PRIME):
    pivots = {}
    selected = []
    for j, column in enumerate(columns):
        pivot, reduced = reduce_sparse_column(column, pivots, p)
        if pivot is not None:
            pivots[pivot] = reduced
            selected.append(j)
            if target is not None and len(selected) == target:
                break
    return selected, pivots


def solve_square(a, b):
    """Solve a x=b over Q by Gauss--Jordan; a is copied."""
    n = len(a)
    aug = [list(map(F, a[i])) + [F(b[i])] for i in range(n)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if aug[i][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        c = aug[col][col]
        aug[col] = [x / c for x in aug[col]]
        for i in range(n):
            if i == col or not aug[i][col]:
                continue
            c = aug[i][col]
            aug[i] = [x - c * y for x, y in zip(aug[i], aug[col])]
    return [aug[i][-1] for i in range(n)]


def prove_span(columns, selected):
    """Prove exactly that all columns lie in the selected-column span."""
    basis = [columns[j] for j in selected]
    all_rows = sorted(set().union(*(set(v) for v in basis)))
    row_columns = []
    for row in all_rows:
        row_columns.append({j: basis[j].get(row, F(0)) for j in range(len(basis))
                            if basis[j].get(row, F(0))})
    selected_rows, _ = select_independent(row_columns, target=len(basis))
    assert len(selected_rows) == len(basis)
    pivot_rows = [all_rows[i] for i in selected_rows]
    square = [[basis[j].get(row, F(0)) for j in range(len(basis))]
              for row in pivot_rows]
    for v in columns:
        coeff = solve_square(square, [v.get(row, F(0)) for row in pivot_rows])
        reconstruction = {}
        for c, q in zip(coeff, basis):
            for row, x in q.items():
                reconstruction[row] = reconstruction.get(row, F(0)) + c * x
        reconstruction = {row: x for row, x in reconstruction.items() if x}
        assert reconstruction == v
    return pivot_rows


def support_pt_column(vi, vj):
    """C_supp applied to PT_A(|vi><vj|), as a sparse output operator.

    An input ket coordinate is (a=(p,q), b=((c,d),z)).  The mixed support
    contraction sends it to ((c,d),q) when z=p and to -((c,d),p) when z=q.
    Partial transpose on the first bivector gives

      PT_A(|vi><vj|)[(a,b),(a',b')]
        = vi[(a',b)] vj[(a,b')]

    in this real rational carrier.
    """
    out = {}
    for (a_prime, pair_b, z), x in vi.items():
        for (a, pair_bprime, zprime), y in vj.items():
            p, q = a
            if z == p:
                row = (pair_b, q, a_prime, pair_bprime, zprime)
                out[row] = out.get(row, F(0)) + x * y
            if z == q:
                row = (pair_b, p, a_prime, pair_bprime, zprime)
                out[row] = out.get(row, F(0)) - x * y
    return {k: x for k, x in out.items() if x}


def physical_monomial(u, v, z):
    """Unnormalized (u wedge v)^2 tensor z in wedge coordinates."""
    support = sorted(set(u) | set(v))
    w = {}
    for i, j in combinations(support, 2):
        x = u.get(i, F(0)) * v.get(j, F(0)) - u.get(j, F(0)) * v.get(i, F(0))
        if x:
            w[(i, j)] = x
    return {(a, b, k): x * y * t
            for a, x in w.items() for b, y in w.items() for k, t in z.items()
            if x * y * t}


def build_block():
    rlabels = (
        (0, 1, 2, 3),
        (0, 1, 2, 4),
        (0, 2, 1, 3),
        (0, 2, 1, 4),
        (0, 3, 1, 4),
    )
    rbasis = [fb.r(*x) for x in rlabels]
    raw = [fb.tensor3(fb.f(i), fb.f(j), r)
           for i in range(4) for j in range(4) for r in rbasis]
    projected_raw = [source_project(v) for v in raw]
    projected = [wedge_coordinates(v) for v in projected_raw]
    selected, _ = select_independent(projected, target=7)
    assert len(selected) == 7
    prove_span(projected, selected)
    block_raw = [projected_raw[j] for j in selected]
    block = [projected[j] for j in selected]
    return raw, projected_raw, block_raw, block, selected


def main():
    # Direct convention audit on a nontrivial supported decomposable monomial.
    # u=(e0+e2), v=(e1+e3), z=e0-e2 has z perpendicular to span{u,v}.
    u = {0: F(1), 2: F(1)}
    v = {1: F(1), 3: F(1)}
    z_supported = {0: F(1), 2: F(-1)}
    eta_supported = physical_monomial(u, v, z_supported)
    assert not support_pt_column(eta_supported, eta_supported)
    z_unsupported = {0: F(1), 2: F(1)}
    eta_unsupported = physical_monomial(u, v, z_unsupported)
    assert support_pt_column(eta_unsupported, eta_unsupported)

    raw, projected_raw, block_raw, block, selected = build_block()

    # Exact source and Omega audit for the selected block basis.
    for i, v in enumerate(block_raw):
        assert not fb.add(fb.apply_global_perm(v, fb.transposition(0, 1)), v)
        assert not fb.add(fb.apply_global_perm(v, fb.transposition(2, 3)), v)
        assert not fb.add(fb.apply_global_perm(v, (2, 3, 0, 1, 4)), fb.scale(-1, v))
        assert not fb.global_A4(v)
        assert not fb.product_triple_antisym(v, (0, 1, 4))
        assert not fb.product_triple_antisym(v, (2, 3, 4))

    # There are 7^2 operator matrix units.  Full modular rank proves that the
    # mixed support map after partial transpose is injective on End(block).
    operator_columns = [support_pt_column(block[i], block[j])
                        for i in range(7) for j in range(7)]
    independent, pivots = select_independent(operator_columns)
    assert len(independent) == 49
    assert len(pivots) == 49

    print("exact corrected mixed-PPT obstruction-block audit")
    print("mixed contraction convention passes supported/unsupported monomial audit")
    print(f"raw local carrier dimension = {len(raw)}")
    print(f"first-Pluecker source dimension = {len(block)}")
    print(f"selected projected columns = {selected}")
    print("both lifted Omega contractions vanish on the block")
    print(f"rank_mod_{PRIME}(rho -> C_supp rho^Gamma) = {len(independent)} / 49")
    print("therefore C_supp rho^Gamma=0 forces rho=0 in this block")
    print("PPT and rho>=0 are not needed for this block exclusion")


if __name__ == "__main__":
    main()
