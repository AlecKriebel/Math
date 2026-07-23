#!/usr/bin/env python3
"""Exact triple-incidence barrier for the weighted-residual inequality."""

from fractions import Fraction as Q
from itertools import combinations, permutations

try:
    from verifiers.verify_fixed41_bv_degree5 import (
        add_scaled,
        determinant,
        zero_matrix,
        z_matrix,
    )
    from verifiers.verify_local_hybrid_barrier import (
        load_certificate,
    )
except ModuleNotFoundError:  # Direct execution from the repository root.
    from verify_fixed41_bv_degree5 import (
        add_scaled,
        determinant,
        zero_matrix,
        z_matrix,
    )
    from verify_local_hybrid_barrier import (
        load_certificate,
    )


N = 41

# The first integral pseudo-incidence used to test Phi_f.  It passes the
# named scalar tests but fails two full degree-two matrices.  It is retained
# so that the exact negative polynomial directions remain reproducible.
REJECTED_TRIPLE_COUNTS = {
    (0, 0, 4): 270,
    (0, 1, 4): 24,
    (0, 2, 4): 201,
    (0, 3, 3): 2550,
    (1, 2, 4): 93,
    (2, 3, 3): 546,
    (2, 4, 4): 4269,
    (3, 3, 3): 2174,
    (4, 4, 4): 533,
}

# A stronger integral pseudo-incidence passing every total-degree-two BV
# block as well as Phi_f.  No edge-colored graph realizing all counts is
# asserted to exist.
TRIPLE_COUNTS = {
    (0, 0, 4): 275,
    (0, 1, 4): 30,
    (0, 2, 4): 508,
    (0, 3, 4): 2227,
    (1, 1, 4): 3,
    (1, 3, 4): 81,
    (2, 2, 2): 7,
    (2, 2, 3): 2066,
    (2, 2, 4): 224,
    (3, 3, 3): 227,
    (3, 3, 4): 3313,
    (3, 4, 4): 1033,
    (4, 4, 4): 666,
}


def center_count(triple, allowed_types):
    """Number of triangle vertices incident with two allowed edge types."""

    a, b, c = triple
    return sum(
        (
            a in allowed_types and b in allowed_types,
            a in allowed_types and c in allowed_types,
            b in allowed_types and c in allowed_types,
        )
    )


def harmonic_matrix(
    total_degree,
    harmonic_degree,
    nodes,
    ordered_counts,
    triple_counts=TRIPLE_COUNTS,
):
    radial_degree = total_degree - harmonic_degree
    matrix = zero_matrix(radial_degree + 1)
    add_scaled(
        matrix,
        z_matrix(
            harmonic_degree, radial_degree, Q(1), Q(1), Q(1)
        ),
    )
    alpha = [Q(count, N) for count in ordered_counts]
    for node, weight in zip(nodes, alpha):
        add_scaled(
            matrix,
            z_matrix(harmonic_degree, radial_degree, Q(1), node, node),
            weight,
        )
        add_scaled(
            matrix,
            z_matrix(harmonic_degree, radial_degree, node, Q(1), node),
            weight,
        )
        add_scaled(
            matrix,
            z_matrix(harmonic_degree, radial_degree, node, node, Q(1)),
            weight,
        )
    for triple, count in triple_counts.items():
        values = tuple(nodes[index] for index in triple)
        orbit = sorted(set(permutations(values)))
        weight = Q(6 * count, N)
        for u, v, t in orbit:
            add_scaled(
                matrix,
                z_matrix(harmonic_degree, radial_degree, u, v, t),
                weight / len(orbit),
            )
    return matrix


def verify():
    size, nodes, ordered_counts, _, _ = load_certificate()
    assert size == N
    unordered_counts = [count // 2 for count in ordered_counts]

    assert sum(TRIPLE_COUNTS.values()) == N * (N - 1) * (N - 2) // 6
    for edge_type, edge_count in enumerate(unordered_counts):
        incidence = sum(
            count * triple.count(edge_type)
            for triple, count in TRIPLE_COUNTS.items()
        )
        assert incidence == (N - 2) * edge_count

    gram_determinants = {}
    for triple in TRIPLE_COUNTS:
        u, v, t = (nodes[index] for index in triple)
        value = 1 + 2 * u * v * t - u * u - v * v - t * t
        assert value > 0
        gram_determinants[triple] = value
    assert min(
        (value, triple) for triple, value in gram_determinants.items()
    ) == (Q(392283, 2500000), (0, 0, 4))

    # The exact integer-envelope wedge counts are attained.  Type 0 is the
    # -77/100 class; types 0 and 1 together are the two deepest classes.
    deep_0_wedges = sum(
        center_count(triple, {0}) * count
        for triple, count in TRIPLE_COUNTS.items()
    )
    deep_01_wedges = sum(
        center_count(triple, {0, 1}) * count
        for triple, count in TRIPLE_COUNTS.items()
    )
    assert deep_0_wedges == 275
    assert deep_01_wedges == 308
    assert deep_0_wedges <= unordered_counts[4]  # multiplicity one
    assert deep_01_wedges <= 3 * unordered_counts[4]

    # These wedge counts are compatible with the Pfender degree cap.  The
    # type-0 degrees may be 3^5,4^25,5^11:
    # sum d=170 and sum binom(d,2)=275.
    assert 5 * 3 + 25 * 4 + 11 * 5 == ordered_counts[0]
    assert 5 * 3 + 25 * 6 + 11 * 10 == deep_0_wedges
    # The three type-1 edges may form a 3-star on four type-0 degree-five
    # vertices.  It then creates 30 mixed wedges and 3 type-1 wedges.
    assert unordered_counts[1] == 3
    assert TRIPLE_COUNTS[(0, 1, 4)] == 5 * (3 + 1 + 1 + 1)
    assert TRIPLE_COUNTS[(1, 1, 4)] == 3

    # Exact audit of the first, rejected integer pseudo-incidence.  For the
    # k=0 polynomial p(u)=1/5+u-u^2 and the k=1 radial polynomial
    # q(u)=1/5+u, the corresponding scalar-square inequalities are negative.
    rejected_k0 = harmonic_matrix(
        2, 0, nodes, ordered_counts, REJECTED_TRIPLE_COUNTS
    )
    rejected_k1 = harmonic_matrix(
        2, 1, nodes, ordered_counts, REJECTED_TRIPLE_COUNTS
    )
    p_vector = (Q(1, 5), Q(1), Q(-1))
    q_vector = (Q(1, 5), Q(1))
    rejected_k0_direction = sum(
        p_vector[i] * rejected_k0[i][j] * p_vector[j]
        for i in range(3)
        for j in range(3)
    )
    rejected_k1_direction = sum(
        q_vector[i] * rejected_k1[i][j] * q_vector[j]
        for i in range(2)
        for j in range(2)
    )
    assert rejected_k0_direction == Q(
        -804424208380157, 20500000000000
    )
    assert rejected_k1_direction == Q(
        -2007505237299643, 20500000000000
    )

    # The stronger pseudo-incidence passes every fixed-N BV block of total
    # degree at most two.  Exact positivity of all principal minors is
    # checked rather than inferred from floating-point eigenvalues.
    degree_two_minima = {}
    for harmonic_degree in range(3):
        matrix = harmonic_matrix(
            2, harmonic_degree, nodes, ordered_counts
        )
        principal_minors = []
        for size_minor in range(1, len(matrix) + 1):
            for indices in combinations(range(len(matrix)), size_minor):
                minor = determinant(
                    [[matrix[i][j] for j in indices] for i in indices]
                )
                assert minor > 0
                principal_minors.append((minor, indices))
        degree_two_minima[harmonic_degree] = min(principal_minors)
    assert degree_two_minima == {
        0: (Q(3259537, 2562500), (1,)),
        1: (Q(3760571867797, 10250000000000), (1,)),
        2: (Q(3791123972203, 10250000000000), (0,)),
    }
    degree_2_k2 = harmonic_matrix(
        2, 2, nodes, ordered_counts
    )[0][0]

    # For f(u)=u-(8/3)u^2, Phi_f is the quadratic form of the total-degree
    # three k=1 block at (0,1,-8/3).
    degree_3_k1 = harmonic_matrix(3, 1, nodes, ordered_counts)
    vector = (Q(0), Q(1), Q(-8, 3))
    phi = sum(
        vector[i] * degree_3_k1[i][j] * vector[j]
        for i in range(3)
        for j in range(3)
    )
    assert phi == Q(
        35272233739927717, 90087890625000000
    ) > 0

    # The first failure is the total-degree-three k=0 block.  A short exact
    # direction is p(u)=1/5+u-u^2+u^3.
    degree_3_k0 = harmonic_matrix(3, 0, nodes, ordered_counts)
    first_failure_vector = (Q(1, 5), Q(1), Q(-1), Q(1))
    first_failure = sum(
        first_failure_vector[i]
        * degree_3_k0[i][j]
        * first_failure_vector[j]
        for i in range(4)
        for j in range(4)
    )
    assert first_failure == Q(
        -94089968136590201847, 10250000000000000000
    )

    return {
        "triple_type_count": len(TRIPLE_COUNTS),
        "minimum_3_by_3_determinant": min(gram_determinants.values()),
        "deep_0_wedges": deep_0_wedges,
        "deep_01_wedges": deep_01_wedges,
        "rejected_k0_direction": rejected_k0_direction,
        "rejected_k1_direction": rejected_k1_direction,
        "degree_2_minimum_principal_minors": degree_two_minima,
        "degree_2_k2_scalar": degree_2_k2,
        "weighted_residual_scalar": phi,
        "first_degree_3_failure": first_failure,
        "status": "PASS",
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
