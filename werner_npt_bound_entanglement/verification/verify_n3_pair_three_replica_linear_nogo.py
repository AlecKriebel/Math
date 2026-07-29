#!/usr/bin/env python3
"""Exact audit of the three-replica linear-rank relaxation obstruction.

The calculation is performed only on the nontrivial third physical site.
The first two physical sites are fixed to the traceless matrix unit E_01
in every replica, so the degree-two projector is the scalar projector on
the third row/column qutrit pair.

No external package is required.
"""

from fractions import Fraction
from itertools import permutations, product


Q = Fraction
PERMS = tuple(permutations(range(3)))


def sign(perm):
    inversions = sum(
        perm[i] > perm[j] for i in range(3) for j in range(i + 1, 3)
    )
    return -1 if inversions % 2 else 1


def clean(vector):
    return {key: value for key, value in vector.items() if value}


def add(*vectors):
    out = {}
    for vector in vectors:
        for key, value in vector.items():
            out[key] = out.get(key, Q(0)) + value
    return clean(out)


def scale(vector, scalar):
    return clean({key: scalar * value for key, value in vector.items()})


def inner(left, right):
    return sum(value * right.get(key, Q(0)) for key, value in left.items())


def permute_tuple(values, perm):
    # Any consistent left action suffices because we average over S_3.
    return tuple(values[perm[index]] for index in range(3))


def act_replica_permutation(vector, perm, row=True, column=True):
    out = {}
    for (rows, columns), value in vector.items():
        new_rows = permute_tuple(rows, perm) if row else rows
        new_columns = permute_tuple(columns, perm) if column else columns
        key = (new_rows, new_columns)
        out[key] = out.get(key, Q(0)) + value
    return clean(out)


def antisymmetrize(vector, row=True, column=False):
    return scale(
        add(
            *(
                scale(
                    act_replica_permutation(
                        vector, perm, row=row, column=column
                    ),
                    Q(sign(perm)),
                )
                for perm in PERMS
            )
        ),
        Q(1, 6),
    )


def bell_projector(vector, replica):
    """Apply |Omega_3><Omega_3|/3 to one row/column replica pair."""

    out = {}
    for (rows, columns), value in vector.items():
        if rows[replica] != columns[replica]:
            continue
        for label in range(3):
            new_rows = list(rows)
            new_columns = list(columns)
            new_rows[replica] = label
            new_columns[replica] = label
            key = (tuple(new_rows), tuple(new_columns))
            out[key] = out.get(key, Q(0)) + value / 3
    return clean(out)


# zeta is three normalized-Bell numerators, without the factor 3^{-3/2}.
zeta = {
    (labels, labels): Q(1)
    for labels in product(range(3), repeat=3)
}

# chi is the product of the two unnormalized Levi-Civita tensors.
chi = {}
for row_perm in PERMS:
    for column_perm in PERMS:
        chi[(row_perm, column_perm)] = Q(
            sign(row_perm) * sign(column_perm)
        )

# This is the orthogonal projection of zeta away from sign x sign.
eta = add(zeta, scale(chi, Q(-1, 6)))

assert inner(zeta, zeta) == 27
assert inner(chi, chi) == 36
assert inner(zeta, chi) == 6
assert inner(eta, eta) == 26

# eta is invariant under simultaneous replica permutations.
for perm in PERMS:
    assert act_replica_permutation(
        eta, perm, row=True, column=True
    ) == eta

# Both necessary linear rank-two constraints hold.
assert antisymmetrize(eta, row=True, column=False) == {}
assert antisymmetrize(eta, row=False, column=True) == {}

# The intermediate identities make the projection coefficient checkable.
assert antisymmetrize(zeta, row=True, column=False) == scale(
    chi, Q(1, 6)
)
assert antisymmetrize(zeta, row=False, column=True) == scale(
    chi, Q(1, 6)
)

# The three scalar-projector expectations coincide.
projector_expectations = []
for replica in range(3):
    projected = bell_projector(eta, replica)
    expectation = inner(eta, projected)
    projector_expectations.append(expectation)
    assert expectation == Q(226, 9)
    assert expectation / inner(eta, eta) == Q(113, 117)

# On the fixed E_01 x E_01 sector, Pi_2 is precisely this Bell
# projector on the third site.  Hence W_bar=2I/3-(P_1+P_2+P_3)/3.
rayleigh_numerator = (
    Q(2, 3) * inner(eta, eta)
    - sum(projector_expectations, Q(0)) / 3
)
rayleigh_quotient = rayleigh_numerator / inner(eta, eta)

assert rayleigh_numerator == Q(-70, 9)
assert rayleigh_quotient == Q(-35, 117)

print("exact three-replica pair-sector linear no-go verified")
print("norm squared:", inner(eta, eta))
print("each Pi_2 expectation:", projector_expectations[0])
print("Rayleigh quotient:", rayleigh_quotient)
