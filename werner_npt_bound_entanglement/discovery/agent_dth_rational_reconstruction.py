#!/usr/bin/env python3
"""Discovery scaffolding for an exact constrained-DTH pseudomoment.

This file deliberately uses the *rational* highest-weight bases from the
exact local crossing verifier, converted to floating point only for pivot
selection and certificate reconstruction.  The final certificate verifier
must rebuild every selected object over QQ.

The useful public routines are:

``hol_support_blocks``
    Build the exact-coordinate holomorphic support bases.  A returned
    ``range`` matrix K has the convention that a supported raw restriction
    block is K A K^T.

``source_codec``
    Enumerate the independent symmetric entries of all A blocks.

No conclusion printed by this discovery file is a theorem.
"""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path

import numpy as np
import scipy.linalg as la


HERE = Path(__file__).resolve().parent
VERIFY = HERE.parent / "verification" / "agent_dth_local_crossing_exact.py"
SPEC = importlib.util.spec_from_file_location("dth_exact_bridge_reconstruct", VERIFY)
BRIDGE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(BRIDGE)


def kron3(a, b, c):
    return np.kron(np.kron(a, b), c)


def permutation_coordinate_representation(basis, permutation):
    """Coordinate matrix of P_permutation in a raw integer HW basis."""
    gram = np.asarray(BRIDGE.basis_gram(basis), dtype=float)
    restriction = np.asarray(
        BRIDGE.restriction_block(BRIDGE.permutation_operator(permutation), basis),
        dtype=float,
    )
    return la.solve(gram, restriction, assume_a="pos")


def local_representations(hol_bases):
    needed = set()
    needed.add((1, 0, 2, 3, 4))
    needed.add((0, 1, 3, 2, 4))
    needed.add((2, 3, 0, 1, 4))
    needed.update(tuple(q) + (4,) for q in itertools.permutations(range(4)))
    return [
        {
            permutation: permutation_coordinate_representation(basis, permutation)
            for permutation in needed
        }
        for basis in hol_bases
    ]


def parity(permutation):
    return -1 if sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    ) % 2 else 1


def epsilon(a, b, c):
    if len({a, b, c}) < 3:
        return 0
    return parity((a, b, c))


def omega_local(basis, first):
    retained = (2, 3) if first == 0 else (0, 1)
    out = np.zeros((9, len(basis)), dtype=float)
    for column, vector in enumerate(basis):
        for index, coefficient in vector.items():
            word = BRIDGE.WORDS[index]
            value = epsilon(word[4], word[first], word[first + 1])
            if value:
                row = 3 * word[retained[0]] + word[retained[1]]
                out[row, column] += float(coefficient) * value
    return out


def orthonormal_image(matrix, tolerance=2e-9):
    matrix = (matrix + matrix.T) / 2
    values, vectors = la.eigh(matrix)
    return vectors[:, values > 1 - tolerance]


def absolute_nullspace(matrix, tolerance=2e-9):
    if not matrix.shape[1]:
        return np.zeros((matrix.shape[1], 0))
    if not matrix.shape[0]:
        return np.eye(matrix.shape[1])
    _, singular, vh = la.svd(matrix, full_matrices=True)
    rank = int(np.sum(singular > tolerance))
    return vh[rank:, :].T


def hol_support_blocks(tolerance=2e-9):
    """Return all 125 exact-coordinate holomorphic support blocks."""
    _, _, hol_bases, _ = BRIDGE.exact_restriction_bridge()
    grams = [np.asarray(BRIDGE.basis_gram(basis), dtype=float) for basis in hol_bases]
    representations = local_representations(hol_bases)
    omegas = [(omega_local(basis, 0), omega_local(basis, 2)) for basis in hol_bases]

    blocks = []
    for shapes in itertools.product(range(5), repeat=3):
        dimensions = tuple(len(hol_bases[s]) for s in shapes)
        size = int(np.prod(dimensions))
        identity = np.eye(size)

        def global_rep(permutation):
            return kron3(*(representations[s][permutation] for s in shapes))

        p12 = (identity - global_rep((1, 0, 2, 3, 4))) / 2
        p34 = (identity - global_rep((0, 1, 3, 2, 4))) / 2
        ppair = (identity + global_rep((2, 3, 0, 1, 4))) / 2
        a4 = sum(
            parity(q) * global_rep(tuple(q) + (4,)) / 24
            for q in itertools.permutations(range(4))
        )
        # These commuting idempotents need not be orthogonal in the raw
        # coordinate basis.  Their product is still an exact projector.
        projector = p12 @ p34 @ ppair @ (identity - a4)
        _, singular, vh = la.svd(projector, full_matrices=False)
        rank = int(np.sum(singular > tolerance))
        source = projector[:, la.qr(projector, pivoting=True)[2][:rank]]

        omega0 = kron3(*(omegas[s][0] for s in shapes))
        omega2 = kron3(*(omegas[s][1] for s in shapes))
        kernel = absolute_nullspace((omega0 + omega2) @ source, tolerance)
        ket_basis = source @ kernel
        gram = kron3(*(grams[s] for s in shapes))
        restriction_range = gram @ ket_basis
        blocks.append(
            {
                "shapes": shapes,
                "dimensions": dimensions,
                "ket_basis": ket_basis,
                "range": restriction_range,
            }
        )
    return blocks


class SourceCodec:
    def __init__(self, blocks):
        self.blocks = []
        offset = 0
        for block in blocks:
            k = block["range"].shape[1]
            count = k * (k + 1) // 2
            self.blocks.append((block, slice(offset, offset + count)))
            offset += count
        self.size = offset

    @staticmethod
    def symmetric_basis(k):
        for i in range(k):
            matrix = np.zeros((k, k))
            matrix[i, i] = 1
            yield (i, i), matrix
        for i in range(k):
            for j in range(i + 1, k):
                matrix = np.zeros((k, k))
                matrix[i, j] = matrix[j, i] = 1
                yield (i, j), matrix


def source_codec(tolerance=2e-9):
    blocks = hol_support_blocks(tolerance)
    codec = SourceCodec(blocks)
    return blocks, codec


def block_ranges(multiplicities):
    out = []
    offset = 0
    for multiplicity in multiplicities:
        out.append(np.arange(offset, offset + multiplicity * multiplicity).reshape(
            multiplicity, multiplicity
        ))
        offset += multiplicity * multiplicity
    assert offset == 103
    return out


def mode3_apply(a, b, c, tensor):
    return np.einsum("ai,bj,ck,ijk->abc", a, b, c, tensor, optimize=True)


def raw_crossing_data():
    hol, mixed, hol_bases, mixed_bases = BRIDGE.exact_restriction_bridge()
    hol = np.asarray(hol, dtype=float)
    mixed = np.asarray(mixed, dtype=float)
    crossing = la.solve(hol.T, mixed.T).T
    return (
        crossing,
        block_ranges(BRIDGE.HOL_MULTS),
        block_ranges(BRIDGE.MIXED_MULTS),
        hol,
        mixed,
        hol_bases,
        mixed_bases,
    )


def raw_mixed_face_bases(raw_mixed_restriction, checkpoint_path,
                         metadata_path="/tmp/dth_obstruction_diagram_metadata.npz"):
    """Convert the numerical orthonormal-coordinate face to raw HW blocks.

    This uses the exported normalized restriction map itself, so it is
    independent of SVD sign/rotation conventions in the numerical mixed
    highest-weight bases.  If ``S_mu`` maps raw matrix entries to normalized
    ones locally, then a positive range matrix ``P`` is pulled back by
    ``S_mu^{-1}``; its range is the desired raw face range.
    """
    metadata = np.load(metadata_path)
    normalized_restriction = metadata["normalized_mixed_restriction"]
    raw_mixed_restriction = np.asarray(raw_mixed_restriction, dtype=float)
    transforms_inverse = []
    offset = 0
    for multiplicity in BRIDGE.MIXED_MULTS:
        count = multiplicity * multiplicity
        raw = raw_mixed_restriction[offset:offset + count]
        normalized = normalized_restriction[offset:offset + count]
        # raw has full row rank.  S raw = normalized.
        transform = normalized @ raw.T @ la.inv(raw @ raw.T)
        assert la.norm(transform @ raw - normalized) < 2e-8
        transforms_inverse.append(la.inv(transform))
        offset += count

    checkpoint = np.load(checkpoint_path)
    blocks = {}
    for shapes in itertools.product(range(6), repeat=3):
        key = "".join(map(str, shapes))
        normalized_range = checkpoint[f"L_{key}"] @ checkpoint[f"q_{key}"]
        dimensions = tuple(BRIDGE.MIXED_MULTS[s] for s in shapes)
        positive = normalized_range @ normalized_range.T
        tensor = positive.reshape((*dimensions, *dimensions)).transpose(
            0, 3, 1, 4, 2, 5
        ).reshape(tuple(d * d for d in dimensions))
        raw_tensor = mode3_apply(
            *(transforms_inverse[s] for s in shapes), tensor
        )
        raw_positive = raw_tensor.reshape(
            dimensions[0], dimensions[0],
            dimensions[1], dimensions[1],
            dimensions[2], dimensions[2],
        ).transpose(0, 2, 4, 1, 3, 5).reshape(positive.shape)
        raw_positive = (raw_positive + raw_positive.T) / 2
        values, vectors = la.eigh(raw_positive)
        rank = normalized_range.shape[1]
        raw_range = vectors[:, -rank:] if rank else np.zeros((positive.shape[0], 0))
        if rank:
            assert values[-rank] > 1e-11 * values[-1]
        blocks[shapes] = raw_range
    return blocks


def candidate_source_coordinates(blocks, codec, hol_restriction, diagram_tensor):
    hol_tensor = mode3_apply(
        hol_restriction, hol_restriction, hol_restriction, diagram_tensor
    )
    vector = np.zeros(codec.size)
    for block, section in codec.blocks:
        k = block["range"].shape[1]
        if not k:
            continue
        f1, f2, f3 = block["dimensions"]
        indices = [
            block_ranges(BRIDGE.HOL_MULTS)[shape]
            for shape in block["shapes"]
        ]
        local = hol_tensor[
            indices[0][:, None, None, :, None, None],
            indices[1][None, :, None, None, :, None],
            indices[2][None, None, :, None, None, :],
        ].reshape(f1 * f2 * f3, f1 * f2 * f3)
        left = la.pinv(block["range"])
        compressed = left @ ((local + local.T) / 2) @ left.T
        data = []
        data.extend(np.diag(compressed))
        for i in range(k):
            for j in range(i + 1, k):
                data.append(compressed[i, j])
        vector[section] = data
    return vector


def pullback_face_functional(
    shapes, y_matrix, crossing, hol_ranges, mixed_ranges, blocks, codec,
    prepared=None,
):
    """Pull one mixed face-annihilating functional to source coordinates."""
    dimensions = tuple(BRIDGE.MIXED_MULTS[s] for s in shapes)
    y_tensor = y_matrix.reshape((*dimensions, *dimensions)).transpose(
        0, 3, 1, 4, 2, 5
    ).reshape(tuple(d * d for d in dimensions))
    row = np.zeros(codec.size)
    if prepared is None:
        prepared = []
        for block, section in codec.blocks:
            r = block["range"]
            if not r.shape[1]:
                continue
            local_maps = [
                crossing[np.ix_(mixed_ranges[mu].reshape(-1),
                                hol_ranges[lam].reshape(-1))]
                for mu, lam in zip(shapes, block["shapes"])
            ]
            if any(la.norm(local) < 1e-13 for local in local_maps):
                continue
            prepared.append((block, section, local_maps))

    for block, section, local_maps in prepared:
        r = block["range"]
        k = r.shape[1]
        pulled = mode3_apply(
            local_maps[0].T,
            local_maps[1].T,
            local_maps[2].T,
            y_tensor,
        )
        f1, f2, f3 = block["dimensions"]
        matrix = pulled.reshape(f1, f1, f2, f2, f3, f3).transpose(
            0, 2, 4, 1, 3, 5
        ).reshape(f1 * f2 * f3, f1 * f2 * f3)
        compressed = r.T @ matrix @ r
        data = []
        data.extend(np.diag(compressed))
        for i in range(k):
            for j in range(i + 1, k):
                data.append(compressed[i, j] + compressed[j, i])
        row[section] = data
    return row


def randomized_defect_rows(
    count,
    seed,
    crossing,
    hol_ranges,
    mixed_ranges,
    face_blocks,
    blocks,
    codec,
):
    rng = np.random.default_rng(seed)
    choices = []
    weights = []
    complements = {}
    prepared = {}
    local_map_cache = {
        (mu, lam): crossing[np.ix_(mixed_ranges[mu].reshape(-1),
                                          hol_ranges[lam].reshape(-1))]
        for mu in range(len(BRIDGE.MIXED_MULTS))
        for lam in range(len(BRIDGE.HOL_MULTS))
    }
    for shapes, face in face_blocks.items():
        n, rank = face.shape
        if rank < n:
            choices.append(shapes)
            weights.append(max(1, n * (n - rank)))
            if not rank:
                complements[shapes] = np.eye(n)
            else:
                _, singular, vh = la.svd(
                    face.T, full_matrices=True, lapack_driver="gesvd"
                )
                numerical_rank = int(np.sum(singular > 1e-10 * singular[0]))
                assert numerical_rank == rank
                complements[shapes] = vh[numerical_rank:, :].T
            specs = []
            for block, section in codec.blocks:
                if not block["range"].shape[1]:
                    continue
                local_maps = [
                    local_map_cache[mu, lam]
                    for mu, lam in zip(shapes, block["shapes"])
                ]
                if any(la.norm(local) < 1e-13 for local in local_maps):
                    continue
                specs.append((block, section, local_maps))
            prepared[shapes] = specs
    weights = np.asarray(weights, dtype=float)
    weights /= np.sum(weights)
    rows = []
    labels = []
    for index in range(count):
        shapes = choices[int(rng.choice(len(choices), p=weights))]
        face = face_blocks[shapes]
        n = face.shape[0]
        complement = complements[shapes]
        left = complement @ rng.normal(size=complement.shape[1])
        right = rng.normal(size=n)
        y = np.outer(left, right) + np.outer(right, left)
        rows.append(
            pullback_face_functional(
                shapes, y, crossing, hol_ranges, mixed_ranges, blocks, codec,
                prepared[shapes],
            )
        )
        labels.append(shapes)
        if (index + 1) % 50 == 0:
            print("defect rows", index + 1, "/", count, flush=True)
    return np.asarray(rows), labels


def main():
    blocks, codec = source_codec()
    dimensions = [block["range"].shape[1] for block in blocks]
    print("nonzero holomorphic support blocks:", sum(k > 0 for k in dimensions))
    print("total supported carrier rank:", sum(dimensions))
    print("symmetric source coordinates:", codec.size)
    print("maximum compressed block:", max(dimensions))
    print("dimension histogram:", {k: dimensions.count(k) for k in sorted(set(dimensions))})
    assert codec.size == 4139


if __name__ == "__main__":
    main()
