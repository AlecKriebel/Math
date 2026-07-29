#!/usr/bin/env python3
"""Exact replay for the OSR-four Clifford-frame parity audit.

This verifier uses only integer/Fraction arithmetic and finite Pauli-word
algebra.  It does not construct floating-point matrices.
"""

from collections import Counter
from fractions import Fraction as Q
from itertools import product


EDGES = tuple((i, j) for i in range(4) for j in range(i + 1, 4))


def gf2_rank(rows, ncols=4):
    rows = list(rows)
    rank = 0
    for col in range(ncols):
        pivot = next(
            (idx for idx in range(rank, len(rows)) if (rows[idx] >> col) & 1),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for idx in range(len(rows)):
            if idx != rank and ((rows[idx] >> col) & 1):
                rows[idx] ^= rows[rank]
        rank += 1
    return rank


def graph_rows(bits):
    rows = [0] * 4
    for bit, (i, j) in zip(bits, EDGES):
        if bit:
            rows[i] |= 1 << j
            rows[j] |= 1 << i
    return tuple(rows)


def isolated(rows):
    return any(row == 0 for row in rows)


def verify_complement_lemma():
    cases = 0
    for bits in product((0, 1), repeat=6):
        complement = tuple(1 - bit for bit in bits)
        rows_a = graph_rows(bits)
        rows_b = graph_rows(complement)
        if gf2_rank(rows_a) == gf2_rank(rows_b) == 2:
            cases += 1
            assert isolated(rows_a) or isolated(rows_b)
    assert cases == 20
    complete_rows = graph_rows((1,) * 6)
    assert gf2_rank(complete_rows) == 4
    return cases


# A Pauli word is represented by (x,z) binary masks.  The Hermitian phase is
# irrelevant for commutation, linear independence, and generated-algebra
# dimension.
def pauli_vec(word):
    x = 0
    z = 0
    for idx, letter in enumerate(word):
        if letter in "XY":
            x |= 1 << idx
        if letter in "YZ":
            z |= 1 << idx
    return x | (z << len(word))


def symplectic(a, b, nqubits=2):
    mask = (1 << nqubits) - 1
    ax, az = a & mask, (a >> nqubits) & mask
    bx, bz = b & mask, (b >> nqubits) & mask
    return (bin(ax & bz).count("1") + bin(az & bx).count("1")) & 1


def commutation_bits(words):
    vecs = [pauli_vec(word) for word in words]
    return tuple(symplectic(vecs[i], vecs[j]) for i, j in EDGES)


# Gaussian-rational arithmetic for exact Pauli coefficients.
def gadd(a, b):
    return a[0] + b[0], a[1] + b[1]


def gmul(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def gscale(a, scalar):
    return a[0] * scalar, a[1] * scalar


ONE = (Q(1), Q(0))
ZERO = (Q(0), Q(0))
PHASE = {1: ONE, -1: (Q(-1), Q(0)), 1j: (Q(0), Q(1)), -1j: (Q(0), Q(-1))}
MUL = {
    ("I", "I"): (1, "I"),
    ("I", "X"): (1, "X"),
    ("I", "Y"): (1, "Y"),
    ("I", "Z"): (1, "Z"),
    ("X", "I"): (1, "X"),
    ("X", "X"): (1, "I"),
    ("X", "Y"): (1j, "Z"),
    ("X", "Z"): (-1j, "Y"),
    ("Y", "I"): (1, "Y"),
    ("Y", "X"): (-1j, "Z"),
    ("Y", "Y"): (1, "I"),
    ("Y", "Z"): (1j, "X"),
    ("Z", "I"): (1, "Z"),
    ("Z", "X"): (1j, "Y"),
    ("Z", "Y"): (-1j, "X"),
    ("Z", "Z"): (1, "I"),
}


def word_multiply(left, right):
    coefficient = ONE
    letters = []
    for a, b in zip(left, right):
        phase, letter = MUL[a, b]
        coefficient = gmul(coefficient, PHASE[phase])
        letters.append(letter)
    return coefficient, "".join(letters)


def dict_add(left, right, scale=Q(1)):
    out = dict(left)
    for word, coefficient in right.items():
        out[word] = gadd(out.get(word, ZERO), gscale(coefficient, scale))
    return {word: coefficient for word, coefficient in out.items() if coefficient != ZERO}


def dict_multiply(left, right):
    out = {}
    for word_a, coefficient_a in left.items():
        for word_b, coefficient_b in right.items():
            phase, word = word_multiply(word_a, word_b)
            coefficient = gmul(gmul(coefficient_a, coefficient_b), phase)
            out[word] = gadd(out.get(word, ZERO), coefficient)
    return {word: coefficient for word, coefficient in out.items() if coefficient != ZERO}


def verify_d4_calibration():
    a_words = ("XI", "IX", "ZI", "XZ")
    b_words = ("XI", "ZI", "XZ", "ZY")
    bits_a = commutation_bits(a_words)
    bits_b = commutation_bits(b_words)
    assert all((a ^ b) == 1 for a, b in zip(bits_a, bits_b))

    # Both local Pauli families span all four binary Pauli directions and
    # therefore generate M_4; their commutants are scalar.
    assert gf2_rank([pauli_vec(word) for word in a_words], ncols=4) == 4
    assert gf2_rank([pauli_vec(word) for word in b_words], ncols=4) == 4

    h = {
        a_word + b_word: (Q(1, 2), Q(0))
        for a_word, b_word in zip(a_words, b_words)
    }
    identity_4q = {"IIII": ONE}
    assert dict_multiply(h, h) == identity_4q

    # Every local word is nonidentity, so both partial traces vanish.  The
    # four words on each side are distinct/orthogonal, proving OSR = 4.
    assert all(word[:2] != "II" and word[2:] != "II" for word in h)
    assert len(set(a_words)) == len(set(b_words)) == 4

    h12 = {word + "II": coefficient for word, coefficient in h.items()}
    h23 = {"II" + word: coefficient for word, coefficient in h.items()}
    residual = dict_add(
        dict_add(
            dict_multiply(dict_multiply(h12, h23), h12),
            dict_multiply(dict_multiply(h23, h12), h23),
            Q(-1),
        ),
        dict_add(h12, h23, Q(-1)),
        Q(-1, 3),
    )
    norm_squared = Q(64) * sum(
        re * re + im * im for re, im in residual.values()
    )
    assert len(residual) == 38
    assert norm_squared == Q(1376, 9)
    coefficient_counts = Counter(residual.values())
    assert coefficient_counts == Counter(
        {
            (Q(1, 4), Q(0)): 21,
            (Q(-1, 4), Q(0)): 9,
            (Q(1, 6), Q(0)): 3,
            (Q(-1, 6), Q(0)): 3,
            (Q(5, 12), Q(0)): 1,
            (Q(-5, 12), Q(0)): 1,
        }
    )
    return norm_squared


def main():
    cases = verify_complement_lemma()
    norm_squared = verify_d4_calibration()
    print("PASS four-vertex complement lemma: 64 graphs exhausted")
    print(f"PASS rank-two/rank-two cases checked: {cases}")
    print("PASS d=4 Clifford calibration: H*=H, H^2=I, trace and partial traces zero")
    print("PASS d=4 calibration: OSR 4 and both leg commutants scalar")
    print(f"PASS d=4 cubic residual: 38 words, squared norm {norm_squared}")
    print("SCOPE arbitrary OSR-4 exceptional solutions remain open")


if __name__ == "__main__":
    main()
