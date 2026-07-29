#!/usr/bin/env python3
"""Exact audit of the quadratic-product symmetrizer identity.

No third-party packages are used.  All calculations are over
fractions.  The checker verifies the six-coset collapse coefficientwise
on an integer basis of Sym^2(C^3), checks the dimension conversion
giving 2/5, and checks the sharp monomial example.
"""

from fractions import Fraction as F
from itertools import permutations


def sym2_basis():
    out = []
    for i in range(3):
        for j in range(i, 3):
            matrix = [[F(0) for _ in range(3)] for _ in range(3)]
            matrix[i][j] = F(1)
            matrix[j][i] = F(1)
            out.append(matrix)
    return out


def tensor4(first, second):
    return {
        (i, j, k, ell): first[i][j] * second[k][ell]
        for i in range(3)
        for j in range(3)
        for k in range(3)
        for ell in range(3)
    }


def permute(tensor, permutation):
    # U_pi sends an input tensor to the tensor with output coordinate r
    # read from input coordinate pi[r].  Summing over all permutations
    # makes the inverse convention immaterial.
    return {
        index: tensor[tuple(index[permutation[r]] for r in range(4))]
        for index in tensor
    }


def inner(first, second):
    return sum(first[index] * second[index] for index in first)


def symmetrize(tensor):
    output = {index: F(0) for index in tensor}
    all_permutations = tuple(permutations(range(4)))
    for permutation in all_permutations:
        moved = permute(tensor, permutation)
        for index, value in moved.items():
            output[index] += value / 24
    return output


basis = sym2_basis()

# Verify coefficientwise that the full S4 symmetrizer equals the average
# over the six placements of the first two tensor positions.  Testing the
# four basis slots independently audits the universal sesquilinear
# identity, rather than a numerical sample.
coset_representatives = (
    (0, 1, 2, 3),
    (2, 3, 0, 1),
    (0, 2, 1, 3),
    (0, 3, 1, 2),
    (1, 2, 0, 3),
    (1, 3, 0, 2),
)

for first_bra in basis:
    for first_ket in basis:
        for second_bra in basis:
            for second_ket in basis:
                bra = tensor4(first_bra, second_bra)
                ket = tensor4(first_ket, second_ket)
                full = inner(bra, symmetrize(ket))
                six = sum(
                    inner(bra, permute(ket, permutation))
                    for permutation in coset_representatives
                ) / 6
                assert full == six

# Haar conversion:
#   (1/15)(1/6) / ((1/6)(1/6)) = 2/5.
dim_sym2 = 6
dim_sym4 = 15
constant = F(dim_sym2 * dim_sym2, 6 * dim_sym4)
assert constant == F(2, 5)

# Sharp example f=z_0^2, g=z_1^2.  Their two nontrivial positive
# contractions vanish, so ||Sym(f tensor g)||^2=1/6.
f = [[F(0) for _ in range(3)] for _ in range(3)]
g = [[F(0) for _ in range(3)] for _ in range(3)]
f[0][0] = F(1)
g[1][1] = F(1)
fg = tensor4(f, g)
sym_fg = symmetrize(fg)
assert inner(sym_fg, sym_fg) == F(1, 6)
haar_product = inner(sym_fg, sym_fg) / dim_sym4
haar_f = F(1, dim_sym2)
haar_g = F(1, dim_sym2)
assert haar_product == F(2, 5) * haar_f * haar_g

print("verified: sharp quadratic product gap with constant 2/5")
