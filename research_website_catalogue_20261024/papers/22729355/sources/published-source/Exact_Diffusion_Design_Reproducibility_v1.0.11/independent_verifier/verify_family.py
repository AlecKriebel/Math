#!/usr/bin/env python3
"""Verify reaction family, conservation, flux cone, and Jacobian independently."""
from __future__ import annotations

if not __debug__:
    raise SystemExit(
        "Exact verifier requires assertions; unset PYTHONOPTIMIZE and do not use python -O"
    )

import argparse
import sympy as sp
from stable_core import reactions, gamma_y, conservation, flux, A_matrix


def expected_A(m: int, a: sp.Expr, b: sp.Expr) -> sp.Matrix:
    A = sp.zeros(m + 1)
    A[0, 0] = -(a + b)
    A[0, m - 2] = -a
    A[0, m - 1] = -b
    A[0, m] = 2 * b
    A[1, 0] = -a
    A[1, 1] = -a
    A[1, m - 1] = 2 * a
    for i in range(2, m - 1):
        A[i, i - 1] = a
        A[i, i] = -a
    A[m - 1, 0] = 2 * a - b
    A[m - 1, m - 2] = 2 * a
    A[m - 1, m - 1] = -(4 * a + b)
    A[m - 1, m] = 2 * b
    A[m, 0] = 2 * b
    A[m, m - 1] = 2 * b
    A[m, m] = -4 * b
    return A


def selected_stoichiometric_minor(m: int, G: sp.Matrix | None = None) -> sp.Matrix:
    """Return the all-dimensional nonzero maximal minor printed in the proof.

    Rows are ``X_1,X_3,...,X_m,Z`` and columns are
    ``R_2,...,R_{m-2},R_a,R_b,R_+``.  The chain range is empty for ``m=3``.
    """

    if G is None:
        G, _ = gamma_y(m)
    labels = [reaction.label for reaction in reactions(m)]
    selected_labels = [f"R{i}" for i in range(2, m - 1)] + ["Ra", "Rb", "R+"]
    rows = [0] + list(range(2, m + 1))
    cols = [labels.index(label) for label in selected_labels]
    assert len(rows) == len(cols) == m
    return G.extract(rows, cols)


def verify_selected_minor(m: int, G: sp.Matrix | None = None) -> None:
    """Verify the exact determinant and its transparent two-step expansion."""

    M = selected_stoichiometric_minor(m, G)
    assert sp.factor(M.det()) == 4 * (-1) ** m

    # The Z row has only the R_+ entry -2.  After expanding it, the R_b
    # column likewise has only the X_m entry -2.  What remains has first row
    # (0,...,0,-1) and a unit lower-bidiagonal chain, with determinant
    # (-1)^m.  These structural checks make the finite exact calculation
    # mirror the all-m proof rather than merely recording a numerical value.
    assert M[-1, :-1] == sp.zeros(1, m - 1)
    assert M[-1, -1] == -2
    after_Z = M[:-1, :-1]
    assert after_Z[:-1, -1] == sp.zeros(m - 2, 1)
    assert after_Z[-1, -1] == -2
    residual = after_Z[:-1, :-1]
    expected = sp.zeros(m - 2)
    expected[0, m - 3] = -1
    for i in range(1, m - 2):
        expected[i, i - 1] = 1
        expected[i, i] = -1
    assert residual == expected
    assert residual.det() == (-1) ** m


def verify(m: int) -> None:
    rs = reactions(m)
    assert len(rs) == m + 2
    assert all(sum(r.y) <= 2 and sum(r.yp) <= 2 and r.y != r.yp for r in rs)
    G, Y = gamma_y(m)
    c = conservation(m)
    assert c.T * G == sp.zeros(1, m + 2)
    verify_selected_minor(m, G)
    assert G.rank() == m
    assert len(G.columnspace()) == m
    left_null = G.T.nullspace()
    assert len(left_null) == 1
    assert sp.Matrix.hstack(left_null[0], c).rank() == 1
    # Exact kernel basis: long circuit and reversible pair.
    e_long = sp.Matrix([1] * m + [0, 0])
    e_pair = sp.Matrix([0] * m + [1, 1])
    assert G * e_long == sp.zeros(m + 1, 1)
    assert G * e_pair == sp.zeros(m + 1, 1)
    assert sp.Matrix.hstack(e_long, e_pair).rank() == 2
    assert len(G.nullspace()) == 2
    # Check each computed null vector lies in the advertised span and conversely.
    E = sp.Matrix.hstack(e_long, e_pair)
    assert all(E.gauss_jordan_solve(v)[1].rows == 0 for v in G.nullspace())
    a, b = sp.symbols("a b", positive=True)
    assert G * flux(m, a, b) == sp.zeros(m + 1, 1)
    A = A_matrix(m, a, b)
    assert sp.simplify(A - expected_A(m, a, b)) == sp.zeros(m + 1)
    # The complete positive-realization family is A(a,b)H; reconstruction uses
    # x*=H^{-1}, k_r=v_r/(x*)^{y_r}.  Check the Jacobian directly symbolically
    # for one generic diagonal per finite m.
    hs = sp.symbols(f"h1:{m+2}", positive=True)
    H = sp.diag(*hs)
    xstar = [1 / h for h in hs]
    rates = []
    v = flux(m, a, b)
    for j in range(Y.cols):
        mon = sp.prod(xstar[i] ** int(Y[i, j]) for i in range(m + 1))
        rates.append(sp.factor(v[j] / mon))
    xs = sp.symbols(f"x1:{m+1}") + (sp.Symbol("z"),)
    mon_rates = []
    for j in range(Y.cols):
        mon_rates.append(rates[j] * sp.prod(xs[i] ** int(Y[i, j]) for i in range(m + 1)))
    f = G * sp.Matrix(mon_rates)
    J = sp.Matrix(f).jacobian(xs).subs({xs[i]: xstar[i] for i in range(m + 1)})
    assert sp.simplify(J - A * H) == sp.zeros(m + 1)
    print(
        f"FAMILY_PASS m={m} reactions={len(rs)} rank={G.rank()} kernel=2 "
        f"selected_minor={4 * (-1) ** m}"
    )


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("m", nargs="*", type=int, default=[3, 4, 5, 6, 8, 10])
    args = p.parse_args()
    for m in args.m:
        verify(m)


if __name__ == "__main__":
    main()
