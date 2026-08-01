#!/usr/bin/env python3
"""Lossless numerical S3 reduction of the degree-three DTH source cone.

The full cache stores 487 ordered source blocks but does not retain their
large raw Young-space bases.  This module reconstructs every physical-site
transport directly from the cached, collectively full-rank Kraus frames.  It
then orbit-identifies the blocks and decomposes repeated-shape stabilizers
into 171 smaller PSD components.

Floating point is used for discovery.  The independent exact character
census is ``verify_dth_level2_source_site_symmetry.py``.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import permutations, product
from pathlib import Path
import pickle
import sys

import numpy as np
import scipy.linalg as la


ROOT = Path(__file__).resolve().parents[1]
DISCOVERY = ROOT / "discovery"
VERIFY = ROOT / "verification"
sys.path.insert(0, str(DISCOVERY))
sys.path.insert(0, str(VERIFY))

import agent_dth_level2_joint_extension as JOINT
import agent_dth_level2_joint_symmetry as TARGET_SYMMETRY
import verify_dth_level2_source_site_symmetry as EXACT


PERMUTATIONS = tuple(permutations(range(3)))
IDENTITY_PERMUTATION = (0, 1, 2)
DEFAULT_CACHE = DISCOVERY / "dth_level2_full_blocks.pkl"


def permute_triple(triple, permutation):
    return tuple(triple[index] for index in permutation)


@lru_cache(None)
def channel_labels(source, target):
    channels = [
        tuple(JOINT.branch_channels(source[site], target[site]))
        for site in range(3)
    ]
    return tuple(
        labels for labels in product(*channels)
        if sum(label == "V" for label in labels) % 2 == 1
    )


def transport_builder(blocks, target_data):
    """Return a cached orthogonal source transport constructor."""
    block_by_source = {tuple(block["source"]): block for block in blocks}
    target_transport_cache = {}

    def target_transport(target, permutation):
        key = (tuple(target), tuple(permutation))
        if key not in target_transport_cache:
            target_transport_cache[key] = TARGET_SYMMETRY.axis_intertwiner(
                target_data, key[0], key[1]
            )
        return target_transport_cache[key]

    @lru_cache(None)
    def source_transport(source, permutation):
        source = tuple(source)
        permutation = tuple(permutation)
        permuted_source = permute_triple(source, permutation)
        block = block_by_source[source]
        permuted_block = block_by_source[permuted_source]
        left_columns = []
        right_columns = []
        for target in sorted(block["maps"]):
            labels = channel_labels(source, target)
            maps = block["maps"][target]
            assert len(labels) == len(maps)
            permuted_target, target_unitary = target_transport(
                target, permutation
            )
            assert permuted_target == permute_triple(target, permutation)
            permuted_labels = channel_labels(
                permuted_source, permuted_target
            )
            label_index = {
                labels_value: index
                for index, labels_value in enumerate(permuted_labels)
            }
            permuted_maps = permuted_block["maps"][permuted_target]
            for labels_value, matrix in zip(labels, maps):
                transported_labels = permute_triple(
                    labels_value, permutation
                )
                paired = permuted_maps[label_index[transported_labels]]
                left_columns.append(matrix)
                right_columns.append(paired @ target_unitary)
        left = np.hstack(left_columns)
        right = np.hstack(right_columns)
        gram = left @ left.T
        transport = la.solve(
            gram, left @ right.T, assume_a="sym"
        ).T
        relative = la.norm(transport @ left - right) / max(1.0, la.norm(right))
        orthogonal = la.norm(
            transport.T @ transport - np.eye(transport.shape[0])
        )
        assert relative < 2e-7, (source, permutation, relative)
        assert orthogonal < 3e-7, (source, permutation, orthogonal)
        # Polar cleanup removes accumulated SVD/cache roundoff while retaining
        # the uniquely determined exact orthogonal transport.
        u, _, vt = la.svd(transport)
        transport = u @ vt
        relative = la.norm(transport @ left - right) / max(1.0, la.norm(right))
        assert relative < 4e-7, (source, permutation, relative)
        return transport

    return source_transport


def projector_basis(projector, expected):
    projector = (projector + projector.T) / 2.0
    values, vectors = la.eigh(projector)
    basis = vectors[:, values > 0.5]
    assert basis.shape[1] == expected, (basis.shape, expected, values)
    assert la.norm(basis.T @ basis - np.eye(expected)) < 2e-10
    return basis


def component(rank, kraus, label):
    """One isometric Sym_r -> Sym_m positive embedding by Kraus sum."""
    return {"rank": rank, "kraus": tuple(kraus), "label": label}


def representative_components(representative, transport):
    """Stabilizer-commutant PSD factors for one sorted source triple."""
    dimension = EXACT.post_omega_rank(representative)
    distinct = len(set(representative))
    if distinct == 3:
        return [component(dimension, (np.eye(dimension),), "free")]

    stabilizer = tuple(
        permutation for permutation in PERMUTATIONS
        if permute_triple(representative, permutation) == representative
    )
    transports = {
        permutation: transport(representative, permutation)
        for permutation in stabilizer
    }
    if distinct == 2:
        swap = next(
            value for permutation, value in transports.items()
            if permutation != IDENTITY_PERMUTATION
        )
        plus_projector = (np.eye(dimension) + swap) / 2.0
        trace = EXACT.swap_trace(
            next(index for index in representative
                 if representative.count(index) == 2),
            next(index for index in representative
                 if representative.count(index) == 1),
        )
        plus = (dimension + trace) // 2
        minus = (dimension - trace) // 2
        out = []
        if plus:
            out.append(component(
                plus, (projector_basis(plus_projector, plus),), "swap+"
            ))
        if minus:
            out.append(component(
                minus,
                (projector_basis(np.eye(dimension) - plus_projector, minus),),
                "swap-",
            ))
        return out

    # Full S3 stabilizer.  Central projectors give the trivial, sign, and
    # standard isotypic spaces.  On the standard space, one + eigenspace of a
    # transposition selects the multiplicity factor.  Averaging its orbit and
    # dividing by sqrt(2) gives an isometric C -> C tensor I_2 embedding.
    signs = {
        permutation: (-1) ** sum(
            permutation[i] > permutation[j]
            for i in range(3) for j in range(i + 1, 3)
        ) for permutation in stabilizer
    }
    trivial_projector = sum(transports.values()) / 6.0
    sign_projector = sum(
        signs[p] * transports[p] for p in stabilizer
    ) / 6.0
    standard_projector = (
        np.eye(dimension) - trivial_projector - sign_projector
    )
    transposition = transports[(1, 0, 2)]

    multiplicity = dimension
    tau = EXACT.swap_trace(representative[0], representative[0])
    cyc = EXACT.cycle_trace(representative[0])
    trivial_rank = (multiplicity + 3 * tau + 2 * cyc) // 6
    sign_rank = (multiplicity - 3 * tau + 2 * cyc) // 6
    standard_rank = (multiplicity - cyc) // 3
    out = []
    if trivial_rank:
        out.append(component(
            trivial_rank,
            (projector_basis(trivial_projector, trivial_rank),),
            "trivial",
        ))
    if sign_rank:
        out.append(component(
            sign_rank,
            (projector_basis(sign_projector, sign_rank),),
            "sign",
        ))
    if standard_rank:
        standard_plus = standard_projector @ (
            np.eye(dimension) + transposition
        ) / 2.0
        seed = projector_basis(standard_plus, standard_rank)
        scale = np.sqrt(1.0 / (3.0 * np.sqrt(2.0)))
        kraus = tuple(
            scale * transports[permutation] @ seed
            for permutation in stabilizer
        )
        out.append(component(standard_rank, kraus, "standard"))
    return out


def embed_component(value, descriptor):
    return sum(kraus @ value @ kraus.T for kraus in descriptor["kraus"])


def adjoint_component(value, descriptor):
    return sum(kraus.T @ value @ kraus for kraus in descriptor["kraus"])


def build_reduction(blocks, target_data, audit=True):
    block_index = {
        tuple(block["source"]): index for index, block in enumerate(blocks)
    }
    transport = transport_builder(blocks, target_data)
    orbits = []
    for representative in sorted({
        tuple(sorted(block["source"])) for block in blocks
    }):
        members = sorted({
            permute_triple(representative, permutation)
            for permutation in PERMUTATIONS
        })
        transports = {}
        for member in members:
            permutation = next(
                permutation for permutation in PERMUTATIONS
                if permute_triple(representative, permutation) == member
            )
            transports[member] = transport(representative, permutation)
        descriptors = representative_components(representative, transport)
        orbits.append({
            "representative": representative,
            "members": tuple(members),
            "transports": transports,
            "components": tuple(descriptors),
            "block_index": tuple(block_index[member] for member in members),
        })

    assert len(orbits) == 112
    descriptors = [
        descriptor for orbit in orbits for descriptor in orbit["components"]
    ]
    assert len(descriptors) == 171
    assert sum(item["rank"] for item in descriptors) == 3665
    assert sum(
        item["rank"] * (item["rank"] + 1) // 2 for item in descriptors
    ) == 87540
    assert max(item["rank"] for item in descriptors) == 106

    reduction = {
        "orbits": tuple(orbits),
        "blocks": blocks,
        "target_data": target_data,
        "component_descriptors": tuple(descriptors),
    }
    if audit:
        audit_reduction(reduction)
    return reduction


def zero_components(reduction):
    return [
        np.zeros((descriptor["rank"],) * 2)
        for descriptor in reduction["component_descriptors"]
    ]


def expand(reduction, values):
    blocks = reduction["blocks"]
    output = [np.zeros((block["dimension"],) * 2) for block in blocks]
    cursor = 0
    for orbit in reduction["orbits"]:
        representative_value = np.zeros_like(
            output[orbit["block_index"][0]]
        )
        for descriptor in orbit["components"]:
            representative_value += embed_component(values[cursor], descriptor)
            cursor += 1
        orbit_scale = 1.0 / np.sqrt(len(orbit["members"]))
        for member, index in zip(orbit["members"], orbit["block_index"]):
            unitary = orbit["transports"][member]
            output[index] = (
                orbit_scale * unitary @ representative_value @ unitary.T
            )
    assert cursor == len(values)
    return output


def reduce_adjoint(reduction, values):
    output = []
    for orbit in reduction["orbits"]:
        orbit_scale = 1.0 / np.sqrt(len(orbit["members"]))
        representative_value = np.zeros_like(
            values[orbit["block_index"][0]]
        )
        for member, index in zip(orbit["members"], orbit["block_index"]):
            unitary = orbit["transports"][member]
            representative_value += (
                orbit_scale * unitary.T @ values[index] @ unitary
            )
        for descriptor in orbit["components"]:
            output.append(adjoint_component(
                representative_value, descriptor
            ))
    return output


def project_psd(values):
    output = []
    for value in values:
        eigenvalues, eigenvectors = la.eigh((value + value.T) / 2.0)
        output.append(
            (eigenvectors * np.maximum(eigenvalues, 0.0)) @ eigenvectors.T
        )
    return output


def physical_floor_shift(reduction, floor):
    """Reduced component shift expanding to floor*I in every ordered block."""
    output = []
    for orbit in reduction["orbits"]:
        orbit_factor = np.sqrt(len(orbit["members"]))
        for descriptor in orbit["components"]:
            repeat_factor = np.sqrt(2.0) if descriptor["label"] == "standard" else 1.0
            output.append(
                floor * orbit_factor * repeat_factor
                * np.eye(descriptor["rank"])
            )
    expanded = expand(reduction, output)
    error = max(
        la.norm(value - floor * np.eye(value.shape[0]))
        for value in expanded
    )
    assert error < 2e-7 * max(1.0, abs(floor))
    return output


def audit_reduction(reduction):
    rng = np.random.default_rng(20260802)
    left = []
    right = []
    for descriptor in reduction["component_descriptors"]:
        a = rng.standard_normal((descriptor["rank"],) * 2)
        b = rng.standard_normal((descriptor["rank"],) * 2)
        left.append((a + a.T) / 2.0)
        right.append((b + b.T) / 2.0)
    expanded_left = expand(reduction, left)
    expanded_right = expand(reduction, right)
    inner_reduced = sum(np.sum(a * b) for a, b in zip(left, right))
    inner_full = sum(
        np.sum(a * b) for a, b in zip(expanded_left, expanded_right)
    )
    assert abs(inner_reduced - inner_full) < 3e-7 * max(1.0, abs(inner_full))
    recovered = reduce_adjoint(reduction, expanded_left)
    error = np.sqrt(sum(
        la.norm(a - b) ** 2 for a, b in zip(left, recovered)
    ))
    norm = np.sqrt(sum(la.norm(a) ** 2 for a in left))
    assert error < 3e-7 * max(1.0, norm), error
    physical_floor_shift(reduction, 1.0)

    # The inferred source transports must be the physical ones, not merely
    # arbitrary orthogonal identifications of equal-dimensional blocks.  A
    # random invariant source therefore has an invariant marginal in every
    # one of the 118 ordered target blocks.
    image = JOINT.apply_marginal(
        reduction["blocks"], expanded_left, reduction["target_data"]
    )
    maximum_covariance_error = 0.0
    image_norm = np.sqrt(sum(la.norm(value) ** 2 for value in image.values()))
    target_transport_cache = {}
    for target in JOINT.TARGETS:
        for permutation in PERMUTATIONS:
            key = (target, permutation)
            if key not in target_transport_cache:
                target_transport_cache[key] = (
                    TARGET_SYMMETRY.axis_intertwiner(
                        reduction["target_data"], target, permutation
                    )
                )
            permuted_target, unitary = target_transport_cache[key]
            difference = (
                image[permuted_target]
                - unitary @ image[target] @ unitary.T
            )
            maximum_covariance_error = max(
                maximum_covariance_error, la.norm(difference)
            )
    assert maximum_covariance_error < 4e-7 * max(1.0, image_norm), (
        maximum_covariance_error, image_norm
    )

    # Directly audit the reduced adjoint identity for the complete marginal.
    direction = {
        target: (
            lambda raw: (raw + raw.T) / 2.0
        )(rng.standard_normal(moment.shape))
        for target, (_, moment) in reduction["target_data"].items()
    }
    full_adjoint = JOINT.apply_adjoint(reduction["blocks"], direction)
    reduced_adjoint_value = reduce_adjoint(reduction, full_adjoint)
    left_inner = JOINT.target_inner(image, direction)
    right_inner = sum(
        np.sum(value * gradient)
        for value, gradient in zip(left, reduced_adjoint_value)
    )
    assert abs(left_inner - right_inner) < 5e-7 * max(1.0, abs(left_inner))
    print("source S3 numerical reduction audit passed")
    print("orbits/components/variables:", 112, 171, 87540)
    print("maximum marginal covariance error:", maximum_covariance_error)


def load_default():
    with DEFAULT_CACHE.open("rb") as stream:
        data = pickle.load(stream)
    JOINT.TARGETS = tuple(data["targets"])
    return data, build_reduction(
        data["blocks"], data["target_data"], audit=True
    )


def main():
    load_default()


if __name__ == "__main__":
    main()
