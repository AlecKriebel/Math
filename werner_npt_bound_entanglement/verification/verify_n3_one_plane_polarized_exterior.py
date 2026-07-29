#!/usr/bin/env python3
"""Exact checks for the polarized one-plane exterior reduction.

All amplitudes are handled with rational common normalization factors,
so no floating-point or third-party package is used.
"""

from fractions import Fraction as F
from itertools import combinations


def swap_string(left, right, sites):
    left = list(left)
    right = list(right)
    for site in sites:
        left[site], right[site] = right[site], left[site]
    return tuple(left), tuple(right)


def inner_sparse(left, right):
    return sum(
        left.get(key, F(0)) * right.get(key, F(0))
        for key in set(left) | set(right)
    )


def swap_matrix_element(bra_left, bra_right, ket_left, ket_right, sites):
    """<bra_left,bra_right| F_sites |ket_left,ket_right>."""

    value = F(0)
    for left_string, left_amplitude in ket_left.items():
        for right_string, right_amplitude in ket_right.items():
            swapped_left, swapped_right = swap_string(
                left_string,
                right_string,
                sites,
            )
            value += (
                bra_left.get(swapped_left, F(0))
                * bra_right.get(swapped_right, F(0))
                * left_amplitude
                * right_amplitude
            )
    return value


all_sites = (0, 1, 2)
pairs = tuple(combinations(all_sites, 2))


def e2_element(bra_left, bra_right, ket_left, ket_right):
    value = F(0)
    for first, second in pairs:
        value += swap_matrix_element(
            bra_left, bra_right, ket_left, ket_right, ()
        )
        value -= swap_matrix_element(
            bra_left, bra_right, ket_left, ket_right, (first,)
        )
        value -= swap_matrix_element(
            bra_left, bra_right, ket_left, ket_right, (second,)
        )
        value += swap_matrix_element(
            bra_left, bra_right, ket_left, ket_right, (first, second)
        )
    return value


def e3_element(bra_left, bra_right, ket_left, ket_right):
    value = F(0)
    for size in range(4):
        coefficient = F(-1 if size % 2 else 1)
        for sites in combinations(all_sites, size):
            value += coefficient * swap_matrix_element(
                bra_left,
                bra_right,
                ket_left,
                ket_right,
                sites,
            )
    return value


def e_element(bra_left, bra_right, ket_left, ket_right):
    return e2_element(
        bra_left, bra_right, ket_left, ket_right
    ) + e3_element(
        bra_left, bra_right, ket_left, ket_right
    )


def basis(string):
    return {tuple(string): F(1)}


# ---------------------------------------------------------------------------
# Layerwise obstruction
# ---------------------------------------------------------------------------

# Unnormalized psi_r have three unit amplitudes and squared norm 3.
psi0 = {
    (0, 0, 0): F(1),
    (0, 1, 1): F(1),
    (0, 2, 2): F(1),
}
psi1 = {
    (1, 0, 0): F(1),
    (1, 1, 1): F(1),
    (1, 2, 2): F(1),
}

# x_r carries normalization 1/sqrt(6), v_r normalization 1/sqrt(3).
# A diagonal expectation therefore has scale 1/18.  The minus sign in
# x_1 gives cross scale -1/18 in this raw convention.  We report c
# after the harmless adversarial phase flip, hence its positive modulus.
a2 = F(1, 18) * (
    e2_element(psi0, psi0, psi0, psi0)
    + e2_element(psi1, psi1, psi1, psi1)
)
a3 = F(1, 18) * (
    e3_element(psi0, psi0, psi0, psi0)
    + e3_element(psi1, psi1, psi1, psi1)
)
c2_raw = F(-1, 18) * e2_element(psi0, psi1, psi1, psi0)
c3_raw = F(-1, 18) * e3_element(psi0, psi1, psi1, psi0)
c2 = abs(c2_raw)
c3 = abs(c3_raw)

assert a2 == F(4, 3)
assert a3 == 0
assert c2 == F(2, 3)
assert c3 == F(2, 3)
assert c3 > F(1, 2) + a3 / 2
assert c2 + c3 - (a2 + a3) / 2 == F(2, 3)
assert F(2, 3) < 1


# ---------------------------------------------------------------------------
# Crossed-Cauchy obstruction and coherent equality
# ---------------------------------------------------------------------------

u = basis((0, 0, 0))
w = basis((0, 0, 1))
v0 = basis((1, 1, 0))
v1 = basis((1, 1, 1))

matched_0 = e_element(u, v0, u, v0)
matched_1 = e_element(w, v1, w, v1)
crossed_0 = e_element(u, v1, u, v1)
crossed_1 = e_element(w, v0, w, v0)
transition = e_element(u, v1, w, v0)

assert matched_0 == matched_1 == 1
assert crossed_0 == crossed_1 == 4
assert transition == -3

# Ordinary Cauchy gives 4, while the lossless matched bound is 3.
assert crossed_0 * crossed_1 == 16
assert (2 + matched_0) * (2 + matched_1) == 9
assert transition * transition == 9


# Swap-sector eigenvalues of H=2I+E.
def h_eigenvalue(antisymmetric_count):
    signs = [-1] * antisymmetric_count + [1] * (
        3 - antisymmetric_count
    )
    one = sum(signs)
    two = sum(
        signs[first] * signs[second] for first, second in pairs
    )
    three = signs[0] * signs[1] * signs[2]
    return 6 - 3 * one + 2 * two - three


assert [h_eigenvalue(count) for count in range(4)] == [2, 2, 6, 22]


# ---------------------------------------------------------------------------
# Five-versus-five Möbius identity
# ---------------------------------------------------------------------------

# A monomial is the commuting trace-replacement product e_S, encoded by
# the bit mask S on (K,1,2,3).  Expand
#
#   M_T = (prod_{j in T}(e_j-I)) (prod_{j not in T} e_j)
#
# exactly in this basis.
def mobius_term(mask):
    complement = 15 ^ mask
    out = {}
    submask = mask
    while True:
        monomial = complement | submask
        mask_size = bin(mask).count("1")
        submask_size = bin(submask).count("1")
        coefficient = F(-1 if (mask_size - submask_size) % 2 else 1)
        out[monomial] = out.get(monomial, F(0)) + coefficient
        if submask == 0:
            break
        submask = (submask - 1) & mask
    return out


def add_polynomial(target, source, scale=F(1)):
    for monomial, coefficient in source.items():
        target[monomial] = target.get(monomial, F(0)) + scale * coefficient
        if target[monomial] == 0:
            del target[monomial]


K = 1
physical = (2, 4, 8)
pair_masks = tuple(
    physical[first] | physical[second]
    for first, second in combinations(range(3), 2)
)
physical_mask = 2 | 4 | 8

five_by_five = {}
add_polynomial(five_by_five, mobius_term(K), F(4))
for mask in pair_masks:
    add_polynomial(five_by_five, mobius_term(mask))
add_polynomial(five_by_five, mobius_term(physical_mask))
add_polynomial(five_by_five, mobius_term(0), F(-1))
for mask in pair_masks:
    add_polynomial(five_by_five, mobius_term(K | mask), F(-1))
add_polynomial(five_by_five, mobius_term(K | physical_mask), F(-1))

# The marginal form of 3(2I-S_V), before using Tr_phys R=I_K, is
#
#   3 e_all + 2 sum_i e_i - 3 sum_{i<j} e_i e_j - I.
expected_defect = {15: F(3), 0: F(-1)}
for mask in physical:
    expected_defect[mask] = F(2)
for mask in pair_masks:
    expected_defect[mask] = F(-3)

assert five_by_five == expected_defect

print("verified: H has swap-sector eigenvalues 2,2,6,22")
print("verified: five-versus-five Möbius expansion is exact")
print("verified: triple-layer bound fails exactly by 1/6")
print("verified: pair matched mass repairs the layer obstruction")
print("verified: crossed Cauchy gives 4 while the sharp coherent value is 3")
print("verified: canonical fixed-factor vectors saturate the lossless bound")
