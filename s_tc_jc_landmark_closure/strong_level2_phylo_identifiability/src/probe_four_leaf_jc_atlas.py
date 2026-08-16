"""Finite-field discovery probe for the root-spanning four-leaf JC atlas.

The probe computes low-degree implicit-ideal subspaces for all 27 unlabelled
root-spanning simple theta networks and transports those subspaces through all
leaf permutations.  Fingerprint collisions are discovery data, not final
stochastic classifications.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations_with_replacement, permutations
import random

from flint import nmod_mat

from enumerate_four_leaf_root_theta import (
    enumerate_networks,
    labelled_canonical_codes,
)
from generic_fourier_network import evaluate_jc_coordinates, reticulation_vertices


JC_REPRESENTATIVES = (
    (0, 0, 0, 0),
    (0, 0, 1, 1),
    (0, 1, 0, 1),
    (0, 1, 1, 0),
    (0, 1, 2, 3),
    (1, 0, 0, 1),
    (1, 0, 1, 0),
    (1, 0, 2, 3),
    (1, 1, 0, 0),
    (1, 1, 1, 1),
    (1, 1, 2, 2),
    (1, 2, 0, 3),
    (1, 2, 1, 2),
    (1, 2, 2, 1),
    (1, 2, 3, 0),
)


def canonical_character_orbit(assignment):
    images = []
    for perm in permutations((1, 2, 3)):
        mapping = {0: 0, 1: perm[0], 2: perm[1], 3: perm[2]}
        images.append(tuple(mapping[value] for value in assignment))
    return min(images)


ORBIT_INDEX = {}
for assignment in (
    (a, b, c, a ^ b ^ c)
    for a in range(4)
    for b in range(4)
    for c in range(4)
):
    canonical = canonical_character_orbit(assignment)
    ORBIT_INDEX[assignment] = JC_REPRESENTATIVES.index(canonical)


def coordinate_permutation(position_to_label):
    """Map new labelled-coordinate indices to base-position indices."""
    answer = []
    for assignment in JC_REPRESENTATIVES:
        by_position = [0] * 4
        for position, label in enumerate(position_to_label):
            by_position[position] = assignment[label - 1]
        answer.append(ORBIT_INDEX[tuple(by_position)])
    assert sorted(answer) == list(range(15))
    return tuple(answer)


def features(degree):
    return tuple(combinations_with_replacement(range(15), degree))


def feature_permutation(position_to_label, feature_list):
    coordinate = coordinate_permutation(position_to_label)
    lookup = {monomial: index for index, monomial in enumerate(feature_list)}
    return tuple(lookup[tuple(sorted(coordinate[index] for index in monomial))] for monomial in feature_list)


def monomial_values(coordinates, feature_list, prime):
    outputs = []
    for monomial in feature_list:
        value = 1
        for index in monomial:
            value = value * coordinates[index] % prime
        outputs.append(value)
    return outputs


def ideal_basis(network, degree, samples, prime, rng):
    vertices = network["vertices"]
    edges = tuple(tuple(edge) for edge in network["edges"])
    leaves = tuple(network["leaves"])
    leaf_labels = {leaf: index + 1 for index, leaf in enumerate(leaves)}
    reticulations = reticulation_vertices(vertices)
    feature_list = features(degree)
    rows = []
    for _ in range(samples):
        edge_parameters = [rng.randrange(2, prime - 1) for _ in edges]
        inheritance = {vertex: rng.randrange(2, prime - 1) for vertex in reticulations}
        coordinates = evaluate_jc_coordinates(
            vertices,
            edges,
            leaf_labels,
            JC_REPRESENTATIVES,
            edge_parameters,
            inheritance,
            modulus=prime,
        )
        rows.append(monomial_values(coordinates, feature_list, prime))
    evaluation = nmod_mat(rows, prime)
    nullspace, nullity = evaluation.nullspace()
    basis = nmod_mat(
        [[int(nullspace[row, column]) for row in range(len(feature_list))] for column in range(nullity)],
        prime,
    )
    reduced, rank = basis.rref()
    assert rank == nullity
    return reduced, nullity, evaluation.rank()


def transformed_fingerprint(reduced_basis, nullity, permutation, prime):
    if nullity == 0:
        return ()
    # If q_new[j] = q_base[perm[j]], then the coefficient of new monomial j is
    # the coefficient of base monomial perm[j].
    transformed = nmod_mat(
        [
            [int(reduced_basis[row, permutation[column]]) for column in range(len(permutation))]
            for row in range(nullity)
        ],
        prime,
    )
    canonical, rank = transformed.rref()
    assert rank == nullity
    return tuple(tuple(int(canonical[row, column]) for column in range(canonical.ncols())) for row in range(nullity))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--degree", type=int, default=2)
    parser.add_argument("--samples", type=int, default=180)
    parser.add_argument("--prime", type=int, default=65521)
    parser.add_argument("--seed", type=int, default=20260801)
    parser.add_argument("--detail-limit", type=int, default=5)
    args = parser.parse_args()

    _raw, networks = enumerate_networks()
    feature_list = features(args.degree)
    rng = random.Random(args.seed)
    leaf_permutations = tuple(permutations((1, 2, 3, 4)))
    feature_permutations = {
        permutation: feature_permutation(permutation, feature_list)
        for permutation in leaf_permutations
    }

    groups = defaultdict(list)
    ranks = Counter()
    nullities = Counter()
    self_symmetries = []
    for network_index, network in enumerate(networks):
        basis, nullity, rank = ideal_basis(
            network, args.degree, args.samples, args.prime, rng
        )
        ranks[rank] += 1
        nullities[nullity] += 1
        base = transformed_fingerprint(
            basis,
            nullity,
            feature_permutations[(1, 2, 3, 4)],
            args.prime,
        )
        symmetry_count = 0
        labelled = labelled_canonical_codes(
            network["vertices"], tuple(tuple(edge) for edge in network["edges"]), tuple(network["leaves"])
        )
        for assignment in labelled.values():
            permutation = tuple(assignment[leaf] for leaf in network["leaves"])
            fingerprint = transformed_fingerprint(
                basis, nullity, feature_permutations[permutation], args.prime
            )
            groups[fingerprint].append((network_index, permutation))
        for permutation in leaf_permutations:
            fingerprint = transformed_fingerprint(
                basis, nullity, feature_permutations[permutation], args.prime
            )
            symmetry_count += fingerprint == base
        self_symmetries.append(symmetry_count)

    collision_sizes = Counter(len(items) for items in groups.values())
    cross_topology = [
        items for items in groups.values() if len({network for network, _permutation in items}) > 1
    ]
    within_topology = [
        items for items in groups.values() if len(items) > 1 and len({network for network, _permutation in items}) == 1
    ]
    print("degree", args.degree, "features", len(feature_list), "samples", args.samples)
    print("evaluation_ranks", dict(sorted(ranks.items())))
    print("ideal_nullities", dict(sorted(nullities.items())))
    print("fingerprint_groups", len(groups), "collision_sizes", dict(sorted(collision_sizes.items())))
    print("self_symmetry_sizes", dict(sorted(Counter(self_symmetries).items())))
    print("within_unlabelled_collision_groups", len(within_topology))
    print("cross_unlabelled_collision_groups", len(cross_topology))
    for index, items in enumerate(cross_topology[: args.detail_limit]):
        print(
            "cross",
            index,
            "size", len(items),
            "networks", sorted({network for network, _permutation in items}),
            "first_items", items[:8],
        )
    for index, items in enumerate(within_topology[: args.detail_limit]):
        print("within", index, "size", len(items), "items", items[:12])


if __name__ == "__main__":
    main()
