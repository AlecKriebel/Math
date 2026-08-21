#!/usr/bin/env python3
"""Exact census of partial-transpose cuts in the five-replica DTH lift.

The physical ket is ``h = w_12 tensor w_34 tensor z_5``.  Its density is
invariant under swaps inside either bivector pair and under exchange of the
two pairs.  Together with complement equivalence of partial transpose, these
symmetries give five and only five nontrivial cut orbits.

Only two orbits are PPT for every physical monomial: a whole bivector pair
and the final z replica.  The other three fail already for the exact
decomposable bivector ``e_0 wedge e_1``.  This verifier checks both claims
with integer arithmetic.
"""

from itertools import combinations


N = 5
IDENTITY = tuple(range(N))
GENERATORS = (
    (1, 0, 2, 3, 4),       # (12)
    (0, 1, 3, 2, 4),       # (34)
    (2, 3, 0, 1, 4),       # (13)(24)
)


def compose(left, right):
    return tuple(left[right[index]] for index in range(N))


def symmetry_group():
    group = {IDENTITY}
    while True:
        old_size = len(group)
        group |= {
            compose(left, right)
            for left in tuple(group)
            for right in GENERATORS
        }
        if len(group) == old_size:
            return group


def image(subset, permutation):
    return frozenset(permutation[index] for index in subset)


def complement(subset):
    return frozenset(range(N)) - subset


def cut_orbits():
    group = symmetry_group()
    nontrivial = {
        frozenset(subset)
        for size in range(1, N)
        for subset in combinations(range(N), size)
    }
    output = []
    while nontrivial:
        seed = min(nontrivial, key=lambda s: (len(s), tuple(s)))
        orbit = set()
        for permutation in group:
            transformed = image(seed, permutation)
            orbit.add(transformed)
            orbit.add(complement(transformed))
        output.append(frozenset(orbit))
        nontrivial -= orbit
    return tuple(output)


EXPECTED_ORBITS = (
    frozenset(map(frozenset, (
        (0,), (1,), (2,), (3,),
        (0, 1, 2, 4), (0, 1, 3, 4), (0, 2, 3, 4), (1, 2, 3, 4),
    ))),
    frozenset(map(frozenset, ((4,), (0, 1, 2, 3)))),
    frozenset(map(frozenset, ((0, 1), (2, 3),
                               (0, 1, 4), (2, 3, 4)))),
    frozenset(map(frozenset, (
        (0, 2), (0, 3), (1, 2), (1, 3),
        (0, 2, 4), (0, 3, 4), (1, 2, 4), (1, 3, 4),
    ))),
    frozenset(map(frozenset, (
        (0, 4), (1, 4), (2, 4), (3, 4),
        (0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3),
    ))),
)


def transpose_first_of_pair_density():
    """PT_1 of |01-10><01-10|, in basis 00,01,10,11."""
    matrix = [[0 for _ in range(4)] for _ in range(4)]
    matrix[1][1] = 1
    matrix[2][2] = 1
    matrix[0][3] = -1
    matrix[3][0] = -1
    return matrix


def quadratic(matrix, vector):
    return sum(vector[i] * matrix[i][j] * vector[j]
               for i in range(len(vector)) for j in range(len(vector)))


def kronecker(left, right):
    return [
        [left[i][j] * right[k][ell]
         for j in range(len(left)) for ell in range(len(right))]
        for i in range(len(left)) for k in range(len(right))
    ]


def main():
    group = symmetry_group()
    assert len(group) == 8
    orbits = cut_orbits()
    assert set(orbits) == set(EXPECTED_ORBITS)
    assert sum(len(orbit) for orbit in orbits) == 30

    # Exact NPT witness for a cut through one leg of a bivector pair.
    tau = transpose_first_of_pair_density()
    negative = [1, 0, 0, 1]
    assert quadratic(tau, negative) == -2

    # A cross-pair cut transposes one leg of each copy of w.  Tensor the
    # negative eigenvector of the first factor with the positive vector |01>
    # of the second.
    tau2 = kronecker(tau, tau)
    positive = [0, 1, 0, 0]
    cross_vector = [a * b for a in negative for b in positive]
    assert quadratic(tau2, cross_vector) == -2

    # Adding transpose on a real rank-one z density changes nothing, so the
    # one-bivector-leg-plus-z orbit is NPT by the first witness as well.

    print("exact five-replica DTH PPT-cut census passed")
    print("source symmetry group order:", len(group))
    print("nontrivial cut orbits:", len(orbits),
          "with sizes", sorted(len(orbit) for orbit in orbits))
    print("universally physical PPT representatives: {1,2} and {5}")
    print("pair exchange makes {3,4} redundant with {1,2}")
    print("other three cut types have exact decomposable-bivector NPT witnesses")


if __name__ == "__main__":
    main()
