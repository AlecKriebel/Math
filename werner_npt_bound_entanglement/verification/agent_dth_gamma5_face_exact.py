#!/usr/bin/env python3
"""Exact Gamma_5 pair/Pluecker plus crossed-support face theorem.

Let ``K5`` be the final-slot mixed support obtained by imposing the two
global bivector antisymmetries, exchange symmetry of the two bivectors, and
the first Pluecker equation.  These constraints involve replicas 1--4 only
and therefore commute with final-slot partial transpose.

On ``V^tensor4 tensor conjugate(V)`` define two delta contractions.  The
first contracts replicas 2 and 5 and retains replicas (1,3,4); the second
contracts replicas 4 and 5 and, after pair identification, retains
(3,1,2).  Across the three physical qutrit sites put

    D5 = d0^tensor3 + d2^tensor3.

This verifier constructs rational highest-weight vectors and performs exact
sparse elimination.  In the symmetry-reduced invariant block algebra it
proves

    reduced_dim K5 = 772,        reduced_rank(D5|K5) = 21,
    reduced_dim(K5 intersect ker D5) = 751.

After restoring the local irrep carrier dimensions, the corresponding full
vector-space dimensions/rank are 1194102, 6552, and 1187550.

The rank 21 occurs in exactly nineteen ordered Schur blocks: rank one on the
eighteen permutations of five displayed type multisets and rank three on
``(11,11,11)``.  The difference ``d0^tensor3-d2^tensor3`` vanishes exactly
on K5.  No floating-point arithmetic or external package is used.
"""

from fractions import Fraction as F
from itertools import combinations, permutations, product
import hashlib
import sys

sys.path.insert(0, "verification")
import agent_dth_block_census as census
import agent_dth_gamma5_000_chart as dense_000
import agent_dth_last_crossing_exact as last
import agent_dth_local_crossing_exact as bridge


EXPECTED_TOTAL_SUPPORT = 772
EXPECTED_TOTAL_DELTA_RANK = 21
EXPECTED_TOTAL_FACE = 751
EXPECTED_ACTIVE_BLOCKS = 188
EXPECTED_DELTA_BLOCKS = 19
EXPECTED_FULL_SUPPORT = 1_194_102
EXPECTED_FULL_DELTA_RANK = 6_552
EXPECTED_FULL_FACE = 1_187_550


def localizer_normalization_audit():
    """Coefficientwise audit of the crossed-support factor ``1/4``.

    This is the universal one-particle index calculation, instantiated on
    ``V=C^3``.  The basis of ``Lambda^2 V`` is orthonormal, so contraction of
    one leg of ``e_p wedge e_q`` has squared coefficient ``1/2``.  We form
    both Gram operators on ``A tensor A tensor conjugate(V)`` and compare
    them after the exact pair-symmetry projector.

    The same Kronecker-delta formula is used at dimension 27 in the DTH
    problem; dimension three keeps this convention check small and readable.
    """
    wedges = tuple(combinations(range(3), 2))
    states = tuple(product(range(3), range(3), range(3)))
    index = {state: position for position, state in enumerate(states)}
    size = len(states)

    def contraction_inner(wedge, z, other_wedge, other_z):
        # If W is the coefficient matrix of the normalized wedge, return
        # <W e_z, W' e_z'>.  Store coefficients after multiplication by
        # sqrt(2); the final factor is therefore 1/2.
        def column(pair, column):
            p, q = pair
            if column == q:
                return {p: 1}
            if column == p:
                return {q: -1}
            return {}

        left = column(wedge, z)
        right = column(other_wedge, other_z)
        return F(sum(left.get(row, 0) * right.get(row, 0)
                     for row in range(3)), 2)

    # K_supp=C_supp^* C_supp on the mixed module, crossed in the first
    # bivector and final vector slots.  Dgram is D5^*D5, with the two
    # contractions identified in the common output V tensor A.
    crossed = [[F(0) for _ in range(size)] for _ in range(size)]
    dgram = [[F(0) for _ in range(size)] for _ in range(size)]
    for row_state in states:
        a, b, z = row_state
        row = index[row_state]
        for column_state in states:
            ap, bp, zp = column_state
            column_index = index[column_state]
            # K^{Gamma_A Gamma_C}_{a b z; a' b' z'}
            # = K_{a' b z'; a b' z}.
            if b == bp:
                crossed[row][column_index] = contraction_inner(
                    wedges[ap], zp, wedges[a], z
                )

            value = F(0)
            # <d0,d0>, <d0,d2>, <d2,d0>, and <d2,d2>.
            if b == bp:
                value += contraction_inner(wedges[a], z, wedges[ap], zp)
            if b == ap:
                value += contraction_inner(wedges[a], z, wedges[bp], zp)
            if a == bp:
                value += contraction_inner(wedges[b], z, wedges[ap], zp)
            if a == ap:
                value += contraction_inner(wedges[b], z, wedges[bp], zp)
            dgram[row][column_index] = value

    def pair_swap(state):
        a, b, z = state
        return index[(b, a, z)]

    # Compare P_sym Kcross P_sym and (1/4) P_sym D^*D P_sym without
    # constructing a floating or algebraic-number basis of Sym^2(A).
    for row_state in states:
        row = index[row_state]
        row_swap = pair_swap(row_state)
        for column_state in states:
            column = index[column_state]
            column_swap = pair_swap(column_state)
            left = F(1, 4) * (
                crossed[row][column]
                + crossed[row_swap][column]
                + crossed[row][column_swap]
                + crossed[row_swap][column_swap]
            )
            right = F(1, 16) * (
                dgram[row][column]
                + dgram[row_swap][column]
                + dgram[row][column_swap]
                + dgram[row_swap][column_swap]
            )
            assert left == right

    # A transparent diagonal normalization test.  For the normalized wedge
    # w=e0 wedge e1 and z=e0, Kcross has value 1/2 whereas D^*D has value 2.
    unsupported = index[(0, 0, 0)]
    supported = index[(0, 0, 2)]
    assert crossed[unsupported][unsupported] == F(1, 2)
    assert dgram[unsupported][unsupported] == F(2)
    assert crossed[supported][supported] == dgram[supported][supported] == 0


def target_word_bases():
    return [
        [
            {bridge.WORDS[index]: coefficient
             for index, coefficient in vector.items()}
            for vector in basis
        ]
        for basis in last.last_highest_weight_bases()
    ]


def delta_half(vector, first):
    """Contract the final contravariant state into one bivector copy."""
    output = {}
    if first == 0:
        contracted = 1
        retained = (0, 2, 3)
    elif first == 2:
        contracted = 3
        # Identify both outputs as (remaining single vector, other bivector).
        retained = (2, 0, 1)
    else:
        raise ValueError(first)
    for key, coefficient in vector.items():
        if any(word[contracted] != word[4] for word in key):
            continue
        row = tuple(census.state_index(census.state_at(key, replica))
                    for replica in retained)
        output[row] = output.get(row, F(0)) + coefficient
    return {key: value for key, value in output.items() if value}


def combined_delta(vector, sign=1):
    return census.add(delta_half(vector, 0),
                      census.scale(sign, delta_half(vector, 2)))


def orbit_size(shapes):
    return len(set(permutations(shapes)))


def block_data(shapes, bases):
    # The 00 local basis has eighteen raw words per vector.  Its tensor cube
    # is checked independently in a 27-dimensional exact dense chart by
    # verify_dth_gamma5_000_dense.py.
    if shapes == (5, 5, 5):
        return (dense_000.RAW_RANK, dense_000.SUPPORT_RANK,
                dense_000.DELTA_RANK, dense_000.FACE_RANK)
    raw = [census.tensor3(left, middle, right)
           for left in bases[shapes[0]]
           for middle in bases[shapes[1]]
           for right in bases[shapes[2]]]
    projected = [census.source_project(vector) for vector in raw]
    independent, _ = census.exact_column_echelon(projected)
    support = [projected[index] for index in independent]
    plus_columns = [combined_delta(vector, 1) for vector in support]
    minus_columns = [combined_delta(vector, -1) for vector in support]
    assert all(not column for column in minus_columns)
    delta_independent, delta_kernel = census.exact_column_echelon(plus_columns)
    support_rank = len(support)
    delta_rank = len(delta_independent)
    face_rank = len(delta_kernel)
    assert face_rank == support_rank - delta_rank
    return len(raw), support_rank, delta_rank, face_rank


def unordered_triples(number):
    for first in range(number):
        for second in range(first, number):
            for third in range(second, number):
                yield first, second, third


def main():
    localizer_normalization_audit()
    bases = target_word_bases()
    rows = []
    total_support = total_delta = total_face = active = delta_blocks = 0
    full_support = full_delta = full_face = 0
    for shapes in unordered_triples(len(bases)):
        raw, support, delta, face = block_data(shapes, bases)
        multiplicity = orbit_size(shapes)
        total_support += multiplicity * support
        total_delta += multiplicity * delta
        total_face += multiplicity * face
        carrier = 1
        for shape in shapes:
            carrier *= last.LAST_IRREP_DIMS[shape]
        full_support += multiplicity * carrier * support
        full_delta += multiplicity * carrier * delta
        full_face += multiplicity * carrier * face
        active += multiplicity * bool(support)
        delta_blocks += multiplicity * bool(delta)
        rows.append((shapes, raw, support, delta, face, multiplicity))
        print("/".join(last.LAST_NAMES[index] for index in shapes),
              "raw/support/delta/face", raw, support, delta, face,
              "orbit", multiplicity, flush=True)

    assert total_support == EXPECTED_TOTAL_SUPPORT
    assert total_delta == EXPECTED_TOTAL_DELTA_RANK
    assert total_face == EXPECTED_TOTAL_FACE
    assert active == EXPECTED_ACTIVE_BLOCKS
    assert delta_blocks == EXPECTED_DELTA_BLOCKS
    assert full_support == EXPECTED_FULL_SUPPORT
    assert full_delta == EXPECTED_FULL_DELTA_RANK
    assert full_face == EXPECTED_FULL_FACE

    nonzero_delta = {
        tuple(last.LAST_NAMES[index] for index in shapes): delta
        for shapes, _, _, delta, _, _ in rows if delta
    }
    assert nonzero_delta == {
        ("30", "30", "11"): 1,
        ("30", "11", "11"): 1,
        ("30", "11", "00"): 1,
        ("11", "11", "11"): 3,
        ("11", "11", "00"): 1,
        ("11", "00", "00"): 1,
    }

    census_text = "\n".join(
        f"{','.join(last.LAST_NAMES[index] for index in shapes)}:"
        f"{raw},{support},{delta},{face},{multiplicity}"
        for shapes, raw, support, delta, face, multiplicity in rows
    ).encode("ascii")
    digest = hashlib.sha256(census_text).hexdigest()

    print("exact Gamma5 DTH face theorem passed")
    print("reduced support/delta/face rank sums:",
          total_support, total_delta, total_face)
    print("full support/delta/face dimensions:",
          full_support, full_delta, full_face)
    print("active support / delta blocks:", active, delta_blocks)
    print("unordered census sha256:", digest)


if __name__ == "__main__":
    main()
