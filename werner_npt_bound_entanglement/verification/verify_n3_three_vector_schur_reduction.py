#!/usr/bin/env python3
"""Exact checks for the three-vector Schur reduction.

The proof in the accompanying note is dimension-independent.  This
small checker verifies the contraction identities and the sharp
product-anchor equality on an exact three-qubit instance.
"""

from __future__ import annotations

import itertools

import sympy as sp


HALF = sp.Rational(1, 2)


def words(dims):
    return list(itertools.product(*(range(d) for d in dims)))


def partial_trace(matrix, dims, traced):
    traced = tuple(sorted(traced))
    kept = tuple(i for i in range(len(dims)) if i not in traced)
    full_words = words(dims)
    positions = {word: i for i, word in enumerate(full_words)}
    kept_words = words([dims[i] for i in kept])
    traced_words = words([dims[i] for i in traced])
    out = sp.zeros(len(kept_words), len(kept_words))
    for ir, row_kept in enumerate(kept_words):
        for ic, col_kept in enumerate(kept_words):
            value = 0
            for common in traced_words:
                row = [0] * len(dims)
                col = [0] * len(dims)
                for p, site in enumerate(kept):
                    row[site] = row_kept[p]
                    col[site] = col_kept[p]
                for p, site in enumerate(traced):
                    row[site] = common[p]
                    col[site] = common[p]
                value += matrix[positions[tuple(row)], positions[tuple(col)]]
            out[ir, ic] = sp.simplify(value)
    return out


def embed(reduced, dims, kept):
    kept = tuple(kept)
    full_words = words(dims)
    kept_dims = [dims[i] for i in kept]
    kept_words = words(kept_dims)
    kept_pos = {word: i for i, word in enumerate(kept_words)}
    out = sp.zeros(len(full_words), len(full_words))
    complement = tuple(i for i in range(len(dims)) if i not in kept)
    for ir, row in enumerate(full_words):
        for ic, col in enumerate(full_words):
            if any(row[i] != col[i] for i in complement):
                continue
            rr = tuple(row[i] for i in kept)
            cc = tuple(col[i] for i in kept)
            out[ir, ic] = reduced[kept_pos[rr], kept_pos[cc]]
    return out


def hs(first, second):
    return sp.simplify(
        sum(
            sp.conjugate(first[i, j]) * second[i, j]
            for i in range(first.rows)
            for j in range(first.cols)
        )
    )


def endpoint_bilinear(first, second, dims):
    answer = 0
    sites = range(len(dims))
    for size in range(len(dims) + 1):
        for traced in itertools.combinations(sites, size):
            answer += (-HALF) ** size * hs(
                partial_trace(first, dims, traced),
                partial_trace(second, dims, traced),
            )
    return sp.simplify(answer)


def outer(x, y):
    return x * y.conjugate().T


def A_of(x, dims):
    projection = outer(x, x)
    answer = sp.zeros(projection.rows)
    sites = tuple(range(len(dims)))
    for size in range(len(dims) + 1):
        for traced in itertools.combinations(sites, size):
            kept = tuple(i for i in sites if i not in traced)
            reduced = partial_trace(projection, dims, traced)
            answer += (-HALF) ** size * embed(reduced, dims, kept)
    return sp.simplify(answer)


def K_of(x, dims):
    projection = outer(x, x)
    answer = sp.zeros(projection.rows)
    sites = tuple(range(len(dims)))
    for size in range(len(dims) + 1):
        for kept in itertools.combinations(sites, size):
            traced = tuple(i for i in sites if i not in kept)
            reduced = partial_trace(projection, dims, traced)
            answer += (-HALF) ** size * embed(reduced, dims, kept)
    return sp.simplify(answer)


def main():
    dims = (2, 2, 2)
    dimension = 8
    basis = [sp.eye(dimension)[:, i] for i in range(dimension)]

    # Exact unit vectors with nontrivial rational superpositions.
    w = basis[0]
    u = sp.Rational(3, 5) * basis[1] + sp.Rational(4, 5) * basis[6]
    v = sp.Rational(5, 13) * basis[2] + sp.Rational(12, 13) * basis[7]
    assert (u.conjugate().T * u)[0] == 1
    assert (v.conjugate().T * v)[0] == 1

    Pw = outer(w, w)
    D = outer(u, v)
    Aw = A_of(w, dims)
    Ku = K_of(u, dims)

    a = endpoint_bilinear(Pw, Pw, dims)
    b = endpoint_bilinear(D, D, dims)
    z = endpoint_bilinear(Pw, D, dims)
    assert sp.simplify(a - (w.conjugate().T * Aw * w)[0]) == 0
    assert sp.simplify(b - (v.conjugate().T * Ku * v)[0]) == 0
    assert sp.simplify(z - (v.conjugate().T * Aw * u)[0]) == 0

    # Product-anchor identity A_w=2^{-3} U and its sharp equality.
    local_u = sp.diag(1, -1)
    reflection = sp.kronecker_product(local_u, local_u, local_u)
    assert Aw == sp.Rational(1, 8) * reflection
    assert a == sp.Rational(1, 8)

    sharp = basis[7]
    Psharp = outer(sharp, sharp)
    sharp_b = endpoint_bilinear(Psharp, Psharp, dims)
    sharp_z = endpoint_bilinear(Pw, Psharp, dims)
    assert sharp_b == sp.Rational(1, 8)
    assert sharp_z == -sp.Rational(1, 8)
    assert sp.simplify(a * sharp_b - sharp_z**2) == 0

    # Exact separable compression used in the one-site Schur boundary.
    phi = sp.Matrix([1, 0, 0, 1])
    local_compression = sp.eye(4) - HALF * phi * phi.T
    separable = sp.zeros(4)
    for phase in (1, sp.I, -1, -sp.I):
        first = sp.Matrix([1, phase])
        second = sp.Matrix([1, -sp.conjugate(phase)])
        product = sp.kronecker_product(first, second) / 2
        separable += HALF * product * product.conjugate().T
    e01 = sp.Matrix([0, 1, 0, 0])
    e10 = sp.Matrix([0, 0, 1, 0])
    separable += HALF * (e01 * e01.T + e10 * e10.T)
    assert sp.simplify(local_compression - separable) == sp.zeros(4)

    print(
        "verified: A/K contraction identities, exact Schur data, "
        "sharp product-anchor equality, and one-site separable compression"
    )


if __name__ == "__main__":
    main()
