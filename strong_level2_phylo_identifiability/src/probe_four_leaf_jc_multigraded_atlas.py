"""Multigraded finite-field fingerprints for the four-leaf JC atlas.

Pendant-edge factors give a four-component grading recording, for each leaf,
how many coordinate factors carry a nonzero character.  Degree-four spaces
then split into at most 75 columns per block, avoiding a 3060-column global
elimination.  Results remain discovery evidence until exact substitution and
stochastic certificates are supplied.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
from itertools import combinations_with_replacement, permutations
import random

from flint import nmod_mat

from enumerate_four_leaf_root_theta import enumerate_networks, labelled_canonical_codes
from generic_fourier_network import evaluate_jc_coordinates, reticulation_vertices
from probe_four_leaf_jc_atlas import JC_REPRESENTATIVES, coordinate_permutation


def coordinate_multidegree(assignment):
    return tuple(int(character != 0) for character in assignment)


def feature_data(degree):
    monomials = tuple(combinations_with_replacement(range(15), degree))
    coordinate_degrees = [coordinate_multidegree(g) for g in JC_REPRESENTATIVES]
    multidegrees = []
    buckets = defaultdict(list)
    for index, monomial in enumerate(monomials):
        multidegree = tuple(
            sum(coordinate_degrees[coordinate][leaf] for coordinate in monomial)
            for leaf in range(4)
        )
        multidegrees.append(multidegree)
        buckets[multidegree].append(index)
    return monomials, tuple(multidegrees), {key: tuple(value) for key, value in buckets.items()}


def feature_permutation(position_to_label, monomials):
    coordinate = coordinate_permutation(position_to_label)
    lookup = {monomial: index for index, monomial in enumerate(monomials)}
    return tuple(
        lookup[tuple(sorted(coordinate[index] for index in monomial))]
        for monomial in monomials
    )


def sample_coordinates(network, sample_count, prime, rng):
    vertices = network["vertices"]
    edges = tuple(tuple(edge) for edge in network["edges"])
    leaves = tuple(network["leaves"])
    labels = {leaf: index + 1 for index, leaf in enumerate(leaves)}
    reticulations = reticulation_vertices(vertices)
    rows = []
    for _ in range(sample_count):
        edge_parameters = [rng.randrange(2, prime - 1) for _ in edges]
        inheritance = {vertex: rng.randrange(2, prime - 1) for vertex in reticulations}
        rows.append(
            evaluate_jc_coordinates(
                vertices,
                edges,
                labels,
                JC_REPRESENTATIVES,
                edge_parameters,
                inheritance,
                modulus=prime,
            )
        )
    return rows


def monomial_value(coordinates, monomial, prime):
    value = 1
    for index in monomial:
        value = value * coordinates[index] % prime
    return value


def multigraded_ideal(network, monomials, buckets, sample_count, prime, rng):
    samples = sample_coordinates(network, sample_count, prime, rng)
    ideal = {}
    ranks = {}
    for multidegree, global_indices in buckets.items():
        rows = [
            [monomial_value(sample, monomials[index], prime) for index in global_indices]
            for sample in samples
        ]
        evaluation = nmod_mat(rows, prime)
        kernel, nullity = evaluation.nullspace()
        if nullity:
            basis = nmod_mat(
                [
                    [int(kernel[column, row]) for column in range(len(global_indices))]
                    for row in range(nullity)
                ],
                prime,
            )
            reduced, rank = basis.rref()
            assert rank == nullity
            ideal[multidegree] = reduced
        else:
            ideal[multidegree] = None
        ranks[multidegree] = evaluation.rank()
    return ideal, ranks


def transformed_digest(ideal, buckets, feature_map, feature_multidegrees, prime):
    bucket_local = {
        multidegree: {global_index: local for local, global_index in enumerate(indices)}
        for multidegree, indices in buckets.items()
    }
    digest = hashlib.sha256()
    for new_multidegree in sorted(buckets):
        new_indices = buckets[new_multidegree]
        mapped = tuple(feature_map[index] for index in new_indices)
        old_multidegrees = {feature_multidegrees[index] for index in mapped}
        assert len(old_multidegrees) == 1
        old_multidegree = old_multidegrees.pop()
        old_basis = ideal[old_multidegree]
        digest.update(bytes(new_multidegree))
        if old_basis is None:
            digest.update((0).to_bytes(2, "little"))
            continue
        column_order = [bucket_local[old_multidegree][index] for index in mapped]
        nullity = old_basis.nrows()
        transformed = nmod_mat(
            [
                [int(old_basis[row, column_order[column]]) for column in range(len(column_order))]
                for row in range(nullity)
            ],
            prime,
        )
        reduced, rank = transformed.rref()
        assert rank == nullity
        digest.update(nullity.to_bytes(2, "little"))
        for row in range(nullity):
            for column in range(reduced.ncols()):
                digest.update(int(reduced[row, column]).to_bytes(2, "little"))
    return digest.hexdigest()


def modular_jacobian_rank(network, prime, rng):
    vertices = network["vertices"]
    edges = tuple(tuple(edge) for edge in network["edges"])
    leaves = tuple(network["leaves"])
    labels = {leaf: index + 1 for index, leaf in enumerate(leaves)}
    reticulations = reticulation_vertices(vertices)
    edge_values = [rng.randrange(2, prime - 1) for _ in edges]
    inheritance = {vertex: rng.randrange(2, prime - 1) for vertex in reticulations}
    base = evaluate_jc_coordinates(
        vertices, edges, labels, JC_REPRESENTATIVES[1:], edge_values, inheritance, prime
    )
    columns = []
    for index in range(len(edges)):
        changed = list(edge_values)
        changed[index] = (changed[index] + 1) % prime
        value = evaluate_jc_coordinates(
            vertices, edges, labels, JC_REPRESENTATIVES[1:], changed, inheritance, prime
        )
        columns.append(tuple((a - b) % prime for a, b in zip(value, base)))
    for reticulation in reticulations:
        changed = dict(inheritance)
        changed[reticulation] = (changed[reticulation] + 1) % prime
        value = evaluate_jc_coordinates(
            vertices, edges, labels, JC_REPRESENTATIVES[1:], edge_values, changed, prime
        )
        columns.append(tuple((a - b) % prime for a, b in zip(value, base)))
    matrix = nmod_mat(
        [[columns[column][row] for column in range(len(columns))] for row in range(14)],
        prime,
    )
    return matrix.rank()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--degree", type=int, default=4)
    parser.add_argument("--prime", type=int, default=65521)
    parser.add_argument("--seed", type=int, default=20260801)
    parser.add_argument("--detail-limit", type=int, default=20)
    args = parser.parse_args()

    monomials, feature_multidegrees, buckets = feature_data(args.degree)
    sample_count = max(map(len, buckets.values())) + 12
    permutations4 = tuple(permutations((1, 2, 3, 4)))
    feature_maps = {
        permutation: feature_permutation(permutation, monomials)
        for permutation in permutations4
    }
    _raw, networks = enumerate_networks()
    rng = random.Random(args.seed)

    groups = defaultdict(list)
    self_symmetry_sizes = []
    model_dimensions = []
    rank_profiles = Counter()
    for network_index, network in enumerate(networks):
        ideal, ranks = multigraded_ideal(
            network, monomials, buckets, sample_count, args.prime, rng
        )
        rank_profiles[tuple(sorted(Counter(ranks.values()).items()))] += 1
        model_dimensions.append(modular_jacobian_rank(network, args.prime, rng))
        base_digest = transformed_digest(
            ideal,
            buckets,
            feature_maps[(1, 2, 3, 4)],
            feature_multidegrees,
            args.prime,
        )
        self_symmetry_sizes.append(
            sum(
                transformed_digest(
                    ideal, buckets, feature_maps[permutation], feature_multidegrees, args.prime
                )
                == base_digest
                for permutation in permutations4
            )
        )
        labelled = labelled_canonical_codes(
            network["vertices"], tuple(tuple(edge) for edge in network["edges"]), tuple(network["leaves"])
        )
        for assignment in labelled.values():
            permutation = tuple(assignment[leaf] for leaf in network["leaves"])
            digest = transformed_digest(
                ideal, buckets, feature_maps[permutation], feature_multidegrees, args.prime
            )
            groups[(model_dimensions[-1], digest)].append((network_index, permutation))

    cross = [
        items for items in groups.values() if len({network for network, _permutation in items}) > 1
    ]
    within = [
        items for items in groups.values() if len(items) > 1 and len({network for network, _permutation in items}) == 1
    ]
    print(
        "degree", args.degree,
        "features", len(monomials),
        "multidegrees", len(buckets),
        "max_bucket", max(map(len, buckets.values())),
        "samples", sample_count,
    )
    print("model_dimensions", dict(sorted(Counter(model_dimensions).items())))
    print("self_symmetry_sizes", dict(sorted(Counter(self_symmetry_sizes).items())))
    print("fingerprint_groups", len(groups), "collision_sizes", dict(sorted(Counter(map(len, groups.values())).items())))
    print("within_unlabelled_collision_groups", len(within))
    print("cross_unlabelled_collision_groups", len(cross))
    for index, items in enumerate(cross[: args.detail_limit]):
        print(
            "cross", index,
            "size", len(items),
            "networks", sorted({network for network, _permutation in items}),
            "first_items", items[:10],
        )
    for index, items in enumerate(within[: args.detail_limit]):
        print("within", index, "size", len(items), "items", items[:12])


if __name__ == "__main__":
    main()

