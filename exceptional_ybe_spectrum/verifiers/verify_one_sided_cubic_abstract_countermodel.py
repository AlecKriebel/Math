#!/usr/bin/env python3
"""Exact abstract H_3 countermodel for the one-sided color compression.

This is deliberately *not* a local Yang--Baxter matrix P on (C^6)^2.
It is an exact representation of the two-projection cubic on C^216
with:

* the d=6, eta=1/2 H_3 multiplicities;
* a reducing d=4 tensor-tower summand of dimension 4^3;
* two rank-32 boundary-color projections with all scalar traces forced
  for WWU and UWW;
* nonzero leakage across both boundary projections.

It certifies that the abstract cubic, H_3 multiplicities, inherited
d=4 subrepresentation, and scalar boundary trace identities do not by
themselves force the missing color projections to reduce the opposite
generator.
"""

from __future__ import annotations

import sympy as sp


SQRT2 = sp.sqrt(2)


def hs2(x: sp.MatrixBase) -> sp.Expr:
    return sp.simplify(sp.trace(x.conjugate().T * x))


def projection(indices: list[int], n: int) -> sp.SparseMatrix:
    return sp.SparseMatrix(n, n, {(i, i): 1 for i in indices})


def put_block(
    target: sp.SparseMatrix, rows: tuple[int, int], block: sp.MatrixBase
) -> None:
    for i in range(2):
        for j in range(2):
            value = sp.simplify(block[i, j])
            if value != 0:
                target[rows[i], rows[j]] = value


def main() -> None:
    # Balanced H_3 multiplicities at local dimension six:
    # common-one 27, common-zero 27, and 81 copies of the standard
    # two-dimensional module.
    common = 27
    standard = 81
    n = 2 * common + 2 * standard
    assert n == 216

    c1 = range(0, common)
    c0 = range(common, 2 * common)
    top0 = 2 * common
    bot0 = top0 + standard

    a = sp.SparseMatrix(n, n, {})
    b = sp.SparseMatrix(n, n, {})
    for i in c1:
        a[i, i] = 1
        b[i, i] = 1
    for m in range(standard):
        t = top0 + m
        z = bot0 + m
        a[t, t] = 1
        b[t, t] = sp.Rational(1, 3)
        b[t, z] = SQRT2 / 3
        b[z, t] = SQRT2 / 3
        b[z, z] = sp.Rational(2, 3)

    cubic = (
        a * b * a
        - b * a * b
        - sp.Rational(1, 3) * (a - b)
    )
    assert cubic == sp.zeros(n)
    assert a * a == a and b * b == b
    assert a.T == a and b.T == b
    assert sp.trace(a) == 108
    assert sp.trace(b) == 108
    assert sp.trace(a * b) == 54

    # The inherited d=4 H_3 representation has multiplicities
    # 8 common-one, 8 common-zero, and 24 standard modules.
    w_indices = (
        list(range(0, 8))
        + list(range(common, common + 8))
        + [top0 + m for m in range(24)]
        + [bot0 + m for m in range(24)]
    )
    w3 = projection(w_indices, n)
    assert sp.trace(w3) == 64
    assert a * w3 == w3 * a
    assert b * w3 == w3 * b
    assert sp.trace(w3 * a) == 32
    assert sp.trace(w3 * b) == 32
    assert sp.trace(w3 * a * b) == 16

    # Abstract WWU boundary projection G_L.  It commutes with A.
    # Four dimensions in each common sector and two disjoint rank-12
    # multiplicity projections in the standard A=1 and A=0 rows make
    # all genuine scalar WWU traces exact while retaining B-leakage.
    gl_indices = (
        list(range(8, 12))
        + list(range(common + 8, common + 12))
        + [top0 + m for m in range(24, 36)]
        + [bot0 + m for m in range(36, 48)]
    )
    gl = projection(gl_indices, n)

    assert sp.trace(gl) == 32
    assert gl * a == a * gl
    assert sp.trace(gl * a) == 16
    assert sp.trace(gl * b) == 16
    assert sp.trace(gl * a * b) == 8
    assert hs2(gl * b * a) == 8
    leak_l = sp.simplify(hs2(b * gl - gl * b) / 2)
    assert leak_l == sp.Rational(16, 3)

    # Abstract UWW boundary projection G_R on disjoint multiplicity
    # coordinates.  It is diagonal in the B-eigenbasis and commutes
    # with B, while leaking across A.
    gr = sp.SparseMatrix(n, n, {})
    for i in range(12, 16):
        gr[i, i] = 1
    for i in range(common + 12, common + 16):
        gr[i, i] = 1

    # Twelve B=1 vectors (1,sqrt(2))/sqrt(3).
    for m in range(48, 60):
        t = top0 + m
        z = bot0 + m
        gr[t, t] = sp.Rational(1, 3)
        gr[t, z] = SQRT2 / 3
        gr[z, t] = SQRT2 / 3
        gr[z, z] = sp.Rational(2, 3)

    # Twelve B=0 vectors (-sqrt(2),1)/sqrt(3).
    for m in range(60, 72):
        t = top0 + m
        z = bot0 + m
        gr[t, t] = sp.Rational(2, 3)
        gr[t, z] = -SQRT2 / 3
        gr[z, t] = -SQRT2 / 3
        gr[z, z] = sp.Rational(1, 3)

    assert gr * gr == gr
    assert gr.T == gr
    assert sp.trace(gr) == 32
    assert gr * b == b * gr
    assert sp.trace(gr * a) == 16
    assert sp.trace(gr * b) == 16
    assert sp.trace(gr * b * a) == 8
    assert hs2(gr * a * b) == 8
    leak_r = sp.simplify(hs2(a * gr - gr * a) / 2)
    assert leak_r == sp.Rational(16, 3)

    # The two boundary sectors and the inherited W^3 sector are
    # mutually orthogonal, as genuine color sectors would be.
    assert w3 * gl == sp.zeros(n)
    assert w3 * gr == sp.zeros(n)
    assert gl * gr == sp.zeros(n)

    # A stronger color-level limitation model.  The three commuting
    # projections p1,p2,p3 have exactly the dimensions of the one-site
    # W colors in (W+U)^3 for r=4,u=2.  They satisfy every color
    # commutation forced by A=P12 and B=P23:
    #
    #   [A,p3]=[B,p1]=[A,p1 p2]=[B,p2 p3]=0.
    #
    # Nevertheless the complementary pair-color projections f1 f2 and
    # f2 f3 do not reduce A and B.
    ident = projection(list(range(n)), n)
    p1 = sp.SparseMatrix(n, n, {})
    p2 = sp.SparseMatrix(n, n, {})
    p3 = sp.SparseMatrix(n, n, {})

    def put_common(start: int) -> None:
        assignments = [
            (range(start + 0, start + 8), "WWW"),
            (range(start + 8, start + 12), "WWU"),
            (range(start + 12, start + 16), "UWW"),
            (range(start + 16, start + 19), "WUU"),
            (range(start + 19, start + 27), "UWU"),
        ]
        for indices, word in assignments:
            for i in indices:
                if word[0] == "W":
                    p1[i, i] = 1
                if word[1] == "W":
                    p2[i, i] = 1
                if word[2] == "W":
                    p3[i, i] = 1

    put_common(0)
    put_common(common)

    scalar_assignments = [
        (range(0, 24), "WWW"),
        (range(24, 36), "WWU"),
        (range(36, 48), "WUW"),
        (range(48, 60), "UWW"),
        (range(60, 65), "WUU"),
    ]
    for multiplicities, word in scalar_assignments:
        for m in multiplicities:
            rows = (top0 + m, bot0 + m)
            for leg, target in enumerate((p1, p2, p3)):
                if word[leg] == "W":
                    target[rows[0], rows[0]] = 1
                    target[rows[1], rows[1]] = 1

    a0 = sp.Matrix([[1, 0], [0, 0]])
    b0 = sp.Matrix(
        [[sp.Rational(1, 3), SQRT2 / 3],
         [SQRT2 / 3, sp.Rational(2, 3)]]
    )
    i2 = sp.eye(2)

    # Eight L-type blocks: p2=U, p3=W, and p1 alternates between
    # B0 and I-B0.  Each contributes one WUW and one UUW dimension.
    for m in range(65, 73):
        rows = (top0 + m, bot0 + m)
        put_block(p1, rows, b0 if m < 69 else i2 - b0)
        put_block(p3, rows, i2)

    # Eight R-type blocks: p1=p2=U, and p3 alternates between A0 and
    # I-A0.  Each contributes one UUW and one UUU dimension.
    for m in range(73, 81):
        rows = (top0 + m, bot0 + m)
        put_block(p3, rows, a0 if m < 77 else i2 - a0)

    for p in (p1, p2, p3):
        assert p * p == p
        assert p.T == p
        assert sp.trace(p) == 144
    assert p1 * p2 == p2 * p1
    assert p1 * p3 == p3 * p1
    assert p2 * p3 == p3 * p2

    assert a * p3 == p3 * a
    assert b * p1 == p1 * b
    assert a * (p1 * p2) == (p1 * p2) * a
    assert b * (p2 * p3) == (p2 * p3) * b

    # Scalar one-color traces inherited from standardness.
    for p in (p1, p2, p3):
        assert sp.trace(p * a) == 72
        assert sp.trace(p * b) == 72

    sectors: dict[str, sp.MatrixBase] = {}
    expected = {
        "WWW": 64,
        "WWU": 32,
        "WUW": 32,
        "UWW": 32,
        "WUU": 16,
        "UWU": 16,
        "UUW": 16,
        "UUU": 8,
    }
    for word in expected:
        factors = [
            p if bit == "W" else ident - p
            for bit, p in zip(word, (p1, p2, p3))
        ]
        sector = factors[0] * factors[1] * factors[2]
        assert sector * sector == sector
        assert sector.T == sector
        assert sp.trace(sector) == expected[word]
        sectors[word] = sector

    assert sectors["WWW"] == w3
    assert sum(sectors.values(), sp.zeros(n)) == ident

    e12 = p1 * p2
    e23 = p2 * p3
    f12 = (ident - p1) * (ident - p2)
    f23 = (ident - p2) * (ident - p3)
    assert sp.trace(e12) == 96 and sp.trace(e23) == 96
    assert sp.trace(f12) == 24 and sp.trace(f23) == 24
    assert a * e12 == e12 * a
    assert b * e23 == e23 * b

    color_leak_l = sp.simplify(hs2(a * f12 - f12 * a) / 2)
    color_leak_r = sp.simplify(hs2(b * f23 - f23 * b) / 2)
    assert color_leak_l == sp.Rational(16, 9)
    assert color_leak_r == sp.Rational(16, 9)

    # The actual WWU and UWW sectors obey the exact boundary traces and
    # the full-cubic norm identities.
    color_gl = sectors["WWU"]
    color_gr = sectors["UWW"]
    assert color_gl * a == a * color_gl
    assert color_gr * b == b * color_gr
    assert sp.trace(color_gl * a) == 16
    assert sp.trace(color_gl * b) == 16
    assert sp.trace(color_gl * a * b) == 8
    assert hs2(color_gl * b * a) == 8
    assert sp.trace(color_gr * a) == 16
    assert sp.trace(color_gr * b) == 16
    assert sp.trace(color_gr * b * a) == 8
    assert hs2(color_gr * a * b) == 8

    print("PASS exact abstract H_3 cubic on dimension 216")
    print("PASS balanced d=6 H_3 ranks: 27, 27, 81 standard copies")
    print("PASS inherited d=4 summand: 8, 8, 24 standard copies")
    print("PASS WWU boundary traces: rank 32, A=B=16, AB=8")
    print("PASS UWW boundary traces: rank 32, A=B=16, BA=8")
    print(f"PASS nonzero left boundary leakage = {leak_l}")
    print(f"PASS nonzero right boundary leakage = {leak_r}")
    print("PASS eight commuting color sectors have dimensions 64,32,32,32,16,16,16,8")
    print("PASS all one-color A/B traces equal 72")
    print("PASS color locality [A,p3]=[B,p1]=[A,p1p2]=[B,p2p3]=0")
    print(f"PASS nonzero complementary-pair A leakage = {color_leak_l}")
    print(f"PASS nonzero complementary-pair B leakage = {color_leak_r}")
    print("SCOPE abstract three-strand model only; no local two-site P claimed")


if __name__ == "__main__":
    main()
