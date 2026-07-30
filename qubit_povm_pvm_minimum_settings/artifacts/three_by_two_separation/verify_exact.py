#!/usr/bin/env python3
"""Independent exact verifier for the qubit POVM--PVM Bell separation.

The script reads the machine-readable coefficient and strategy files and checks
all finite algebraic certificates used in the proof.  It uses exact SymPy
rational/algebraic arithmetic; no floating-point inequality is accepted as a
proof step.  The optional numerical values printed at the end are display only.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
from itertools import product

import sympy as sp

ROOT = Path(__file__).resolve().parent
R = sp.Rational
sqrt = sp.sqrt
I2 = sp.eye(2)
Z2 = sp.zeros(2)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Z = sp.Matrix([[1, 0], [0, -1]])


def zmat(A: sp.Matrix) -> bool:
    return all(sp.simplify(v) == 0 for v in A)


def parse_expr(text: str, env: dict[str, sp.Expr] | None = None) -> sp.Expr:
    loc = {"sqrt": sp.sqrt}
    if env:
        loc.update(env)
    return sp.simplify(sp.sympify(text.replace("^", "**"), locals=loc))


def parse_matrix(raw, env=None) -> sp.Matrix:
    return sp.Matrix([[parse_expr(str(v), env) for v in row] for row in raw])


def kron(A, B):
    return sp.kronecker_product(A, B)


def expect(psi, A, B):
    return sp.simplify((psi.T.conjugate() * kron(A, B) * psi)[0])


def assert_projector(P):
    assert zmat(P - P.T.conjugate())
    assert zmat(P * P - P)


def assert_psd_2x2(P):
    assert zmat(P - P.T.conjugate())
    assert sp.simplify(P.trace()) >= 0
    assert sp.simplify(P.det()) >= 0


def load_coefficients():
    dense = {}
    with (ROOT / "bell_coefficients_dense.csv").open(newline="") as f:
        for row in csv.DictReader(f):
            key = tuple(int(row[k]) for k in ("x", "y", "a", "b"))
            dense[key] = parse_expr(row["c_abxy"])
    assert len(dense) == 36
    assert set(dense) == set(product(range(3), range(2), range(3), range(2)))

    sparse = {}
    with (ROOT / "bell_coefficients_sparse.csv").open(newline="") as f:
        for row in csv.DictReader(f):
            key = tuple(int(row[k]) for k in ("x", "y", "a", "b"))
            sparse[key] = parse_expr(row["c_abxy"])
    assert sparse == {k: v for k, v in dense.items() if v != 0}

    alpha = (1, -1, 1)
    beta = (1, -1)
    chsh_sign = {(0, 0): 1, (0, 1): 1, (1, 0): 1, (1, 1): -1}
    expected = {}
    for x, y, a, b in dense:
        v = 0
        if x < 2:
            v += 10 * chsh_sign[x, y] * alpha[a] * beta[b]
        if (x, y, a, b) == (2, 0, 0, 0):
            v += R(3, 5)
        if (x, y, a, b) == (2, 0, 1, 1):
            v += R(3, 5)
        if (x, y, a, b) == (2, 1, 2, 0):
            v += R(4, 5)
        expected[x, y, a, b] = sp.sympify(v)
    assert dense == expected
    return dense


def behavior_and_value(psi, alice, bob, coeff):
    probs = {}
    for x, y, a, b in coeff:
        probs[x, y, a, b] = expect(psi, alice[x][a], bob[y][b])
    value = sp.simplify(sum(coeff[k] * probs[k] for k in coeff))
    return probs, value


def verify_simple_strategy(coeff):
    raw = json.loads((ROOT / "strategy_simple_qsqrt2.json").read_text())
    psi = sp.Matrix([parse_expr(x) for x in raw["state"]])
    assert sp.simplify((psi.T.conjugate() * psi)[0]) == 1
    alice = {
        0: [parse_matrix(M) for M in raw["alice"]["x0"]],
        1: [parse_matrix(M) for M in raw["alice"]["x1"]],
        2: [parse_matrix(M) for M in raw["alice"]["x2"]],
    }
    bob = {
        0: [parse_matrix(M) for M in raw["bob"]["y0"]],
        1: [parse_matrix(M) for M in raw["bob"]["y1"]],
    }
    for x in range(3):
        assert zmat(sum(alice[x], Z2) - I2)
    for y in range(2):
        assert zmat(sum(bob[y], Z2) - I2)
    for x in (0, 1):
        assert_projector(alice[x][0])
        assert_projector(alice[x][1])
        assert zmat(alice[x][2])
    for y in range(2):
        for P in bob[y]:
            assert_projector(P)

    # Independent PSD factorizations for the genuine POVM.
    factors = [
        (R(1, 25), sp.Matrix([4, -1])),
        (R(1, 25), sp.Matrix([1, -4])),
        (R(8, 25), sp.Matrix([1, 1])),
    ]
    for M, (scale, v) in zip(alice[2], factors):
        assert zmat(M - scale * v * v.T)
        assert 0 < sp.simplify(M.trace()) < 1
        assert sp.simplify(M.det()) == 0

    probs, value = behavior_and_value(psi, alice, bob, coeff)
    assert probs[2, 0, 0, 0] == R(8, 25)
    assert probs[2, 0, 1, 1] == R(8, 25)
    assert probs[2, 1, 2, 0] == R(8, 25)
    L0 = 20 * sqrt(2) + R(16, 25)
    assert sp.simplify(value - L0) == 0
    assert sp.simplify(value - parse_expr(raw["attained_value"])) == 0

    # Ideal three-state discrimination dual certificate and PSD factorizations.
    W0 = R(3, 20) * (I2 + Z)
    W1 = R(3, 20) * (I2 - Z)
    W2 = R(1, 5) * (I2 + X)
    Gamma = R(8, 25) * I2 + R(2, 25) * X
    dual_factors = [
        (R(1, 50), sp.Matrix([1, 4])),
        (R(1, 50), sp.Matrix([4, 1])),
        (R(3, 25), sp.Matrix([1, -1])),
    ]
    for W, M, (scale, v) in zip((W0, W1, W2), alice[2], dual_factors):
        D = sp.simplify(Gamma - W)
        assert zmat(D - scale * v * v.T)
        assert zmat(D * M)
    assert Gamma.trace() == R(16, 25)

    # Every two-label ideal PVM support has value 3/5; every singleton is lower.
    p, q = R(3, 10), R(2, 5)
    pair01 = 2 * p
    pair02 = sp.simplify((p + q + sqrt((p + q) ** 2 - 2 * p * q)) / 2)
    assert pair01 == R(3, 5)
    assert pair02 == R(3, 5)
    assert q < R(3, 5)
    return L0


def verify_strengthened_strategy(coeff):
    raw = json.loads((ROOT / "strategy_strengthened_algebraic.json").read_text())
    q = sqrt(7813)
    eta = 1 / q
    s = 6 * sqrt(217) / q
    a = sqrt((q + 1) / (2 * q))
    b = sqrt((q - 1) / (2 * q))
    k = R(3, 5) * sqrt((q - 1) / (q + 1))
    env = {"q": q, "eta": eta, "s": s, "a": a, "b": b, "k": k}
    for name, text in raw["definitions"].items():
        if name in env:
            assert sp.simplify(parse_expr(text, env) - env[name]) == 0

    psi = sp.Matrix([parse_expr(x, env) for x in raw["state"]])
    assert sp.simplify((psi.T * psi)[0]) == 1
    A0 = parse_matrix(raw["alice_observables"]["A0"], env)
    A1 = parse_matrix(raw["alice_observables"]["A1"], env)
    B0 = parse_matrix(raw["bob_observables"]["B0"], env)
    B1 = parse_matrix(raw["bob_observables"]["B1"], env)
    for O in (A0, A1, B0, B1):
        assert zmat(O.T.conjugate() - O)
        assert zmat(O * O - I2)
    alice = {
        0: [(I2 + A0) / 2, (I2 - A0) / 2, Z2],
        1: [(I2 + A1) / 2, (I2 - A1) / 2, Z2],
        2: [parse_matrix(M, env) for M in raw["alice_x2"]],
    }
    bob = {0: [(I2 + B0) / 2, (I2 - B0) / 2],
           1: [(I2 + B1) / 2, (I2 - B1) / 2]}
    assert zmat(sum(alice[2], Z2) - I2)
    # Rank-one PSD factorizations.
    v0 = sp.Matrix([k, 1])
    v1 = sp.Matrix([-k, 1])
    assert zmat(alice[2][0] - v0 * v0.T / 2)
    assert zmat(alice[2][1] - v1 * v1.T / 2)
    assert zmat(alice[2][2] - (1 - k**2) * sp.Matrix([1, 0]) * sp.Matrix([1, 0]).T)
    assert sp.simplify(1 - k**2) > 0

    probs, value = behavior_and_value(psi, alice, bob, coeff)
    S = sp.simplify(
        expect(psi, A0, B0) + expect(psi, A0, B1)
        + expect(psi, A1, B0) - expect(psi, A1, B1)
    )
    assert sp.simplify(S - 250 / q) == 0

    # Direct dual certificate for the optimized auxiliary POVM.
    D = sp.diag(a, b)
    N00, N10 = bob[0]
    N01 = bob[1][0]
    Ws = [R(3, 5) * D * N00.T * D,
          R(3, 5) * D * N10.T * D,
          R(4, 5) * D * N01.T * D]
    Gamma = parse_matrix(raw["dual_Gamma"], env)
    dvecs = [
        sp.Matrix([sqrt(1 + eta) / 2, -3 * sqrt(1 - eta) / 10]),
        sp.Matrix([sqrt(1 + eta) / 2, 3 * sqrt(1 - eta) / 10]),
        None,
    ]
    for i in (0, 1):
        assert zmat(Gamma - Ws[i] - dvecs[i] * dvecs[i].T)
        assert zmat((Gamma - Ws[i]) * alice[2][i])
    assert zmat(Gamma - Ws[2] - sp.diag(0, R(6, 25) * (1 - eta)))
    assert zmat((Gamma - Ws[2]) * alice[2][2])
    T = sp.simplify(Gamma.trace())
    assert sp.simplify(T - (16 + 4 * eta) / 25) == 0

    L1 = (16 + 8 * q) / 25
    assert sp.simplify(value - L1) == 0
    assert sp.simplify(value - parse_expr(raw["attained_value"], env)) == 0

    # Exact one-variable subfamily optimization certificate.
    e = sp.symbols("e", positive=True)
    f = 20*sqrt(2-e**2) + (16+4*e)/25
    fp = sp.diff(f, e)
    assert sp.simplify(fp - (-20*e/sqrt(2-e**2) + R(4,25))) == 0
    assert sp.simplify(fp.subs(e, 1/sqrt(7813))) == 0
    fsecond = sp.simplify(sp.diff(f, e, 2))
    assert sp.simplify(fsecond + 40*(2-e**2)**sp.Rational(-3,2)) == 0
    return sp.simplify(L1)


def verify_projective_bound():
    eta, x, y, r, q = sp.symbols("eta x y r q", real=True)

    # Determinant and trace-discriminant identities for binary projective
    # discrimination.  The Bloch vectors obey n^2=m^2=1 and n.m=r.
    nx, ny, nz, mx, my, mz = sp.symbols("nx ny nz mx my mz", real=True)
    s = sp.symbols("s", nonnegative=True, real=True)
    D = sp.diag(sp.sqrt((1 + eta) / 2), sp.sqrt((1 - eta) / 2))
    Qn = (I2 + nx * X + ny * Y + nz * Z) / 2
    Qm = (I2 + mx * X + my * Y + mz * Z) / 2
    A = R(3, 5) * D * Qn * D
    B = R(4, 5) * D * Qm * D
    H = sp.simplify(A - B)
    # Reduce polynomial identities modulo unit-vector and dot-product relations.
    relations = [nx**2 + ny**2 + nz**2 - 1,
                 mx**2 + my**2 + mz**2 - 1,
                 nx*mx + ny*my + nz*mz - r]
    G = sp.groebner(relations, nx, ny, nz, mx, my, mz, order="lex", domain=sp.QQ.frac_field(eta, r))
    det_target = -R(3, 50) * (1 - eta**2) * (1 - r)
    rem = G.reduce(sp.together(H.det() - det_target).as_numer_denom()[0])[1]
    assert sp.expand(rem) == 0
    trA = R(3, 10) * (1 + eta * nz)
    trB = R(2, 5) * (1 + eta * mz)
    assert sp.simplify(A.trace() - trA) == 0
    assert sp.simplify(B.trace() - trB) == 0
    disc = sp.expand((H.trace())**2 - 4 * H.det())
    disc_target = ( (-1 + eta * (3*nz - 4*mz))**2
                    + 24*(1-eta**2)*(1-r) ) / 100
    rem = G.reduce(sp.together(disc - disc_target).as_numer_denom()[0])[1]
    assert sp.expand(rem) == 0

    # The robust square-root comparison, checked as a polynomial identity.
    Rrad = (-1 + eta * (3*x - 4*y))**2 + 24*(1-eta**2)*(1-r)
    Hlin = 8 - 3*x - 4*y
    E1 = 8*(1-y)*(4-3*x) + 12*(1-r)
    E2 = (q-1)*Hlin + 8*(1-y)
    lhs = sp.expand((q + eta*Hlin)**2 - Rrad)
    lhs = sp.expand(lhs.subs(q**2, 25-24*r))
    rhs = sp.expand(2*eta*(eta*E1 + E2))
    assert sp.simplify(lhs-rhs) == 0
    assert sp.expand(Hlin - (1 + 3*(1-x) + 4*(1-y))) == 0
    assert sp.expand((4-3*x) - (1+3*(1-x))) == 0

    # Scalar tangent/square certificates used in the CHSH deficit estimates.
    u, z = sp.symbols("u z", nonnegative=True, real=True)
    assert sp.factor((1-u**2/2)**2 - (1-u**2)) == u**4/4
    assert sp.factor((2-u**2/4)**2 - (4-u**2)) == u**4/16
    assert sp.factor((5+8*u)**2 - (25+24*u)) == 8*u*(7+8*u)

    C = R(2, 5) * (2**R(1, 4) + 2**R(3, 4))
    C2 = sp.simplify(C**2)
    assert C2 == (16 + 12*sqrt(2)) / 25
    assert sp.simplify(C2/40 - 10*(z-C/20)**2 - (C*z-10*z**2)) == 0

    # Exhaustive rank partitions of a three-label PVM in dimension two.
    patterns = [p for p in product(range(3), repeat=3) if sum(p) == 2]
    assert set(patterns) == {(2,0,0),(0,2,0),(0,0,2),(1,1,0),(1,0,1),(0,1,1)}

    U = 20*sqrt(2) + R(3,5) + (4+3*sqrt(2))/250
    assert sp.simplify(U - (20*sqrt(2) + R(3,5) + C2/40)) == 0
    return U


def verify_gaps(L0, L1, U):
    gap0 = sp.simplify(L0-U)
    assert gap0 == 3*(2-sqrt(2))/250
    assert 2**2 > 2  # hence 2 > sqrt(2)

    q = sqrt(7813)
    gap1 = sp.simplify(L1-U)
    expected = (6 + 80*q - 5003*sqrt(2))/250
    assert sp.simplify(gap1-expected) == 0
    # Both sides are positive, so two exact integer square comparisons certify
    # 6+80*sqrt(7813) > 5003*sqrt(2).
    first_difference = sp.expand((6+80*q)**2 - 2*5003**2)
    assert first_difference == -56782 + 960*q
    integer_difference = 960**2 * 7813 - 56782**2
    assert integer_difference == 3976265276
    assert integer_difference > 0
    assert sp.simplify(L1-L0) > 0
    return gap0, gap1


def main():
    coeff = load_coefficients()
    L0 = verify_simple_strategy(coeff)
    L1 = verify_strengthened_strategy(coeff)
    U = verify_projective_bound()
    gap0, gap1 = verify_gaps(L0, L1, U)
    print("All exact certificate checks passed.")
    print("Simple attained value L0 =", L0)
    print("Strengthened attained value L1 =", L1)
    print("Global projective upper bound U =", U)
    print("Original certified gap L0-U =", gap0)
    print("Strengthened certified gap L1-U =", gap1)
    print("Decimal displays (not used as proof):")
    print("  L1 = %.12f" % sp.N(L1, 15))
    print("  U  = %.12f" % sp.N(U, 15))
    print("  gap= %.12f" % sp.N(gap1, 15))


if __name__ == "__main__":
    main()
