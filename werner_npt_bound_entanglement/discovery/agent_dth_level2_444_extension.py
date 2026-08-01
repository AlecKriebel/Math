#!/usr/bin/env python3
"""Numerical fixed-marginal test for the smallest DTH level-two sector.

This discovery script constructs the post-Omega degree-three Grassmann
contraction into the five-replica (2,2,1)^3 (index 444) block.  It works in
Young orthogonal bases and never constructs the 27^7 physical tensor.

The exact representation census and normalization are recorded separately in
``verify_dth_level2_s7_census.py`` and
``verify_dth_seven_to_five_contraction.py``.  Numerical feasibility here is
discovery evidence until converted to an exact certificate.
"""

from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product
from pathlib import Path
import gzip
import importlib.util
import json
import sys

import numpy as np
import scipy.linalg as la


ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "verification"
sys.path.insert(0, str(VERIFY))

import verify_dth_level2_s7_census as CENSUS


S7 = [
    (7,), (6, 1), (5, 2), (5, 1, 1),
    (4, 3), (4, 2, 1), (3, 3, 1), (3, 2, 2),
]
TARGET_SHAPE = (2, 2, 1)
TARGET_INDEX = 4
SOURCE_INDICES = (5, 6, 7)
SOURCE_CARRIER_DIMS = {5: 15, 6: 6, 7: 3}
W_SLOTS = (0, 1, 2, 3, 5, 6)
PAIR_SLOTS = ((0, 1), (2, 3), (5, 6))
Z_SLOT = 4
RNG = np.random.default_rng(20260801)


def removable_cells(shape):
    out = []
    for row in range(len(shape)):
        if row + 1 == len(shape) or shape[row] > shape[row + 1]:
            out.append((row, shape[row] - 1))
    return out


@lru_cache(None)
def standard_tableaux(shape):
    """Tableaux as tuples giving the cell occupied by labels 0,...,n-1."""
    shape = tuple(shape)
    n = sum(shape)
    if n == 0:
        return ((),)
    out = []
    for cell in removable_cells(shape):
        row, column = cell
        smaller = list(shape)
        smaller[row] -= 1
        if smaller[row] == 0:
            smaller.pop(row)
        for tableau in standard_tableaux(tuple(smaller)):
            out.append(tuple(tableau) + (cell,))
    return tuple(sorted(out))


@lru_cache(None)
def adjacent_matrix(shape, generator):
    tabs = standard_tableaux(shape)
    index = {tab: i for i, tab in enumerate(tabs)}
    out = np.zeros((len(tabs), len(tabs)))
    for column, tab in enumerate(tabs):
        r0, c0 = tab[generator]
        r1, c1 = tab[generator + 1]
        axial = (c1 - r1) - (c0 - r0)
        out[column, column] = 1.0 / axial
        if abs(axial) != 1:
            swapped = list(tab)
            swapped[generator], swapped[generator + 1] = (
                swapped[generator + 1], swapped[generator]
            )
            row = index[tuple(swapped)]
            out[row, column] = np.sqrt(1.0 - 1.0 / (axial * axial))
    assert np.linalg.norm(out.T - out) < 1e-12
    assert np.linalg.norm(out @ out - np.eye(len(tabs))) < 1e-12
    return out


def compose(left, right):
    return tuple(left[right[i]] for i in range(len(left)))


@lru_cache(None)
def representation(shape, permutation):
    """Young orthogonal representation in image-form convention."""
    n = len(permutation)
    current = list(range(n))
    out = np.eye(len(standard_tableaux(shape)))
    for position in range(n):
        location = current.index(permutation[position])
        while location > position:
            generator = location - 1
            current[generator], current[generator + 1] = (
                current[generator + 1], current[generator]
            )
            out = out @ adjacent_matrix(shape, generator)
            location -= 1
    assert tuple(current) == tuple(permutation)
    return out


def transposition(n, first, second):
    out = list(range(n))
    out[first], out[second] = out[second], out[first]
    return tuple(out)


def subset_permutation(n, subset, permutation):
    out = list(range(n))
    for source, target in enumerate(permutation):
        out[subset[source]] = subset[target]
    return tuple(out)


def pair_permutation(permutation):
    out = list(range(7))
    for source, target in enumerate(permutation):
        for bit in (0, 1):
            out[PAIR_SLOTS[source][bit]] = PAIR_SLOTS[target][bit]
    return tuple(out)


def global_action(matrix, shapes, permutation):
    dimensions = [len(standard_tableaux(S7[index])) for index in shapes]
    columns = matrix.shape[1]
    tensor = matrix.reshape(*dimensions, columns)
    local = [representation(S7[index], permutation) for index in shapes]
    tensor = np.einsum("ia,abcq->ibcq", local[0], tensor, optimize=True)
    tensor = np.einsum("jb,ibcq->ijcq", local[1], tensor, optimize=True)
    tensor = np.einsum("kc,ijcq->ijkq", local[2], tensor, optimize=True)
    return tensor.reshape(-1, columns)


def pair_wreath_project(matrix, shapes):
    out = matrix
    for first, second in PAIR_SLOTS:
        out = 0.5 * (
            out - global_action(out, shapes, transposition(7, first, second))
        )
    averaged = np.zeros_like(out)
    for permutation in permutations(range(3)):
        averaged += global_action(out, shapes, pair_permutation(permutation))
    return averaged / 6.0


def central_transposition_sum(matrix, shapes):
    out = np.zeros_like(matrix)
    for first, second in combinations(W_SLOTS, 2):
        out += global_action(matrix, shapes, transposition(7, first, second))
    return out


def source_project(matrix, shapes):
    """Orthogonal S_(3,3) projector on the three bivector pairs."""
    wreath = pair_wreath_project(matrix, shapes)
    once = central_transposition_sum(wreath, shapes)
    twice = central_transposition_sum(once, shapes)
    # On Sym^3(wedge^2), the central transposition eigenvalues are
    # 3, -5, -15 for [33], [2211], [1^6].
    return (twice + 20.0 * once + 75.0 * wreath) / 144.0


@lru_cache(None)
def local_triple_antisym(shape_index):
    slots = (5, 6, Z_SLOT)
    out = np.zeros((len(standard_tableaux(S7[shape_index])),) * 2)
    for q in permutations(range(3)):
        sign = -1 if sum(q[i] > q[j] for i in range(3) for j in range(i + 1, 3)) % 2 else 1
        out += sign * representation(
            S7[shape_index], subset_permutation(7, slots, q)
        )
    out /= 6.0
    assert np.linalg.norm(out @ out - out) < 2e-12
    return out


def omega_gram_action(matrix, shapes):
    dimensions = [len(standard_tableaux(S7[index])) for index in shapes]
    columns = matrix.shape[1]
    tensor = matrix.reshape(*dimensions, columns)
    local = [local_triple_antisym(index) for index in shapes]
    tensor = np.einsum("ia,abcq->ibcq", local[0], tensor, optimize=True)
    tensor = np.einsum("jb,ibcq->ijcq", local[1], tensor, optimize=True)
    tensor = np.einsum("kc,ijcq->ijkq", local[2], tensor, optimize=True)
    return tensor.reshape(-1, columns)


def orthonormal_columns(matrix, tolerance=1e-10):
    if matrix.shape[1] == 0:
        return matrix[:, :0], np.array([])
    gram = (matrix.T @ matrix + matrix.T @ matrix.T.T) / 2.0
    values, vectors = la.eigh(gram)
    threshold = tolerance * max(1.0, values[-1])
    keep = values > threshold
    return matrix @ (vectors[:, keep] / np.sqrt(values[keep])), values[keep]


def omega_range(shapes, raw_dimension, expected_rank):
    if expected_rank == 0:
        return np.zeros((raw_dimension, 0))
    trial = RNG.standard_normal((raw_dimension, expected_rank + 4))
    trial = source_project(trial, shapes)
    trial = omega_gram_action(trial, shapes)
    trial = source_project(trial, shapes)
    basis, values = orthonormal_columns(trial, tolerance=1e-9)
    assert basis.shape[1] == expected_rank, (shapes, basis.shape, expected_rank, values)
    return basis


def sequential_branch_embeddings(source_shape, target_shape=TARGET_SHAPE):
    source_tabs = standard_tableaux(source_shape)
    target_tabs = standard_tableaux(target_shape)
    target_index = {tab: i for i, tab in enumerate(target_tabs)}
    grouped = {}
    for source_index, tab in enumerate(source_tabs):
        restricted = tuple(tab[:5])
        rows = Counter(row for row, column in restricted)
        restricted_shape = tuple(rows[row] for row in range(len(rows)))
        if restricted_shape != target_shape:
            continue
        output_tab = tuple(restricted)
        path = (tab[5], tab[6])
        matrix = grouped.setdefault(
            path, np.zeros((len(source_tabs), len(target_tabs)))
        )
        matrix[source_index, target_index[output_tab]] = 1.0
    return grouped


def branch_channels(source_index):
    source_shape = S7[source_index]
    sequential = sequential_branch_embeddings(source_shape)
    paths = sorted(sequential)
    assert len(paths) in (1, 2)
    swap = representation(source_shape, transposition(7, 5, 6))
    f = len(standard_tableaux(TARGET_SHAPE))
    path_swap = np.empty((len(paths), len(paths)))
    for i, left in enumerate(paths):
        for j, right in enumerate(paths):
            path_swap[i, j] = np.trace(
                sequential[left].T @ swap @ sequential[right]
            ) / f
    values, vectors = la.eigh(path_swap)
    out = {}
    for value, coefficients in zip(values, vectors.T):
        label = "H" if value > 0 else "V"
        embedding = sum(
            coefficient * sequential[path]
            for coefficient, path in zip(coefficients, paths)
        )
        assert np.linalg.norm(embedding.T @ embedding - np.eye(f)) < 2e-12
        assert np.linalg.norm(swap @ embedding - value * embedding) < 3e-12
        out[label] = embedding
    expected = CENSUS.two_box_strip_types(source_shape, TARGET_SHAPE)
    assert set(out) == set(expected), (source_shape, out, expected)
    return out


def kron3(matrices):
    return np.kron(np.kron(matrices[0], matrices[1]), matrices[2])


def load_exact_target():
    """Convert the exact 444 chart into the Young orthogonal K basis."""
    module_path = VERIFY / "agent_dth_exact_k_coordinates.py"
    spec = importlib.util.spec_from_file_location("exact_k", module_path)
    exact_k = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(exact_k)

    physical, gram_poly, _ = exact_k.hol_k_coordinates((4, 4, 4))
    physical = np.array(physical, dtype=float)
    gram_poly = np.array(gram_poly, dtype=float)

    # Average an intertwiner from the Young orthogonal model to the exact
    # integral-polytabloid model used by the certificate.
    intertwiner = np.zeros((5, 5))
    for permutation in permutations(range(5)):
        poly = np.array(exact_k.local_representation(4, permutation), dtype=float)
        semi = representation(TARGET_SHAPE, permutation)
        # The exact polytabloid routine records the pullback (anti-homomorphic)
        # coordinate convention, whereas ``representation`` is homomorphic.
        # Averaging poly(g) semi(g), rather than semi(g)^T, intertwines them.
        intertwiner += poly @ semi
    scalar_matrix = intertwiner.T @ np.array(exact_k.local_gram(4), dtype=float) @ intertwiner
    scalar = np.trace(scalar_matrix) / 5.0
    intertwiner /= np.sqrt(scalar)
    local_gram = np.array(exact_k.local_gram(4), dtype=float)
    assert np.linalg.norm(intertwiner.T @ local_gram @ intertwiner - np.eye(5)) < 2e-10
    for generator in range(4):
        permutation = transposition(5, generator, generator + 1)
        poly = np.array(exact_k.local_representation(4, permutation), dtype=float)
        semi = representation(TARGET_SHAPE, permutation)
        assert np.linalg.norm(poly @ intertwiner - intertwiner @ semi) < 2e-10

    total_intertwiner = kron3((intertwiner, intertwiner, intertwiner))
    physical_semi = la.solve(total_intertwiner, physical)
    gram = physical_semi.T @ physical_semi
    root = la.sqrtm(gram).real
    qout = physical_semi @ la.inv(root)
    assert np.linalg.norm(qout.T @ qout - np.eye(10)) < 2e-9

    certificate = ROOT / "verification/certificates/dth_complete_ppt_pseudomoment.json.gz"
    with gzip.open(certificate, "rt", encoding="utf-8") as stream:
        payload = json.load(stream)
    block = next(item for item in payload["blocks"] if item["shape"] == "444")
    chart = np.zeros((10, 10))
    cursor = 0
    for row in range(10):
        numerator, denominator = block["upper"][cursor]
        chart[row, row] = int(numerator) / int(denominator)
        cursor += 1
    for row in range(10):
        for column in range(row + 1, 10):
            numerator, denominator = block["upper"][cursor]
            value = int(numerator) / int(denominator)
            chart[row, column] = chart[column, row] = value
            cursor += 1
    target = root @ chart @ root
    target = (target + target.T) / 2.0
    target_spectrum = la.eigvalsh(target)
    print("raw converted target spectrum:", target_spectrum)
    assert target_spectrum[0] > -2e-14
    return qout, target


def omega_output_rank(shapes):
    local_map = {5: (3, 1), 6: (2, 2), 7: (2, 1, 1)}
    return CENSUS.kronecker_coefficient(
        (2, 2), [local_map[index] for index in shapes], 4
    )


def candidate_blocks():
    out = []
    for shapes in product(SOURCE_INDICES, repeat=3):
        channels = [branch_channels(index) for index in shapes]
        if any(
            sum(label == "V" for label in labels) % 2 == 1
            for labels in product(*(tuple(channel) for channel in channels))
        ):
            out.append(shapes)
    assert len(out) == 23
    return out


def construct_block(shapes, qout):
    channels = [branch_channels(index) for index in shapes]
    odd = [
        labels for labels in product(*(tuple(channel) for channel in channels))
        if sum(label == "V" for label in labels) % 2 == 1
    ]
    embedded = []
    for labels in odd:
        local = tuple(channels[site][labels[site]] for site in range(3))
        embedded.append(kron3(local) @ qout)

    raw_dimension = embedded[0].shape[0]
    expected_omega = omega_output_rank(shapes)
    qomega = omega_range(shapes, raw_dimension, expected_omega)
    projected = []
    for vector in embedded:
        value = source_project(vector, shapes)
        value -= qomega @ (qomega.T @ value)
        projected.append(value)
    union, values = orthonormal_columns(np.hstack(projected), tolerance=2e-9)
    kraus = [union.T @ value for value in projected]

    # Projection and kernel audits on the actually relevant source span.
    assert np.linalg.norm(source_project(union, shapes) - union) < 2e-8
    assert np.linalg.norm(omega_gram_action(union, shapes)) < 2e-8
    weight = np.prod([SOURCE_CARRIER_DIMS[index] for index in shapes]) / 27.0
    return {
        "shapes": shapes,
        "weight": float(weight),
        "kraus": kraus,
        "dimension": union.shape[1],
        "omega_rank": expected_omega,
        "projection_spectrum": values,
    }


def apply_marginal(blocks, variables):
    out = np.zeros((10, 10))
    for block, variable in zip(blocks, variables):
        for kraus in block["kraus"]:
            out += block["weight"] * kraus.T @ variable @ kraus
    return (out + out.T) / 2.0


def apply_adjoint(blocks, target):
    out = []
    for block in blocks:
        value = np.zeros((block["dimension"],) * 2)
        for kraus in block["kraus"]:
            value += block["weight"] * kraus @ target @ kraus.T
        out.append((value + value.T) / 2.0)
    return out


def symmetric_basis(size):
    out = []
    for row in range(size):
        for column in range(row, size):
            value = np.zeros((size, size))
            if row == column:
                value[row, column] = 1.0
            else:
                value[row, column] = value[column, row] = 1.0 / np.sqrt(2.0)
            out.append(value)
    return out


def project_psd(variables):
    out = []
    for variable in variables:
        values, vectors = la.eigh((variable + variable.T) / 2.0)
        out.append((vectors * np.maximum(values, 0.0)) @ vectors.T)
    return out


def solve_feasibility(blocks, target, iterations=4000):
    basis = symmetric_basis(10)
    superoperator = np.empty((55, 55))
    for column, direction in enumerate(basis):
        image = apply_marginal(blocks, apply_adjoint(blocks, direction))
        for row, test in enumerate(basis):
            superoperator[row, column] = np.sum(test * image)
    values, vectors = la.eigh((superoperator + superoperator.T) / 2.0)
    print("AA* spectrum:", values[0], values[-1], "rank", np.sum(values > 1e-11 * values[-1]))
    inverse = (vectors * np.where(values > 1e-12 * values[-1], 1.0 / values, 0.0)) @ vectors.T

    def affine_projection(variables):
        residual = apply_marginal(blocks, variables) - target
        coordinates = np.array([np.sum(element * residual) for element in basis])
        correction_coordinates = inverse @ coordinates
        correction = sum(value * element for value, element in zip(correction_coordinates, basis))
        adjoint = apply_adjoint(blocks, correction)
        return [variable - delta for variable, delta in zip(variables, adjoint)]

    zero = [np.zeros((block["dimension"],) * 2) for block in blocks]
    z = affine_projection(zero)
    best = None
    for iteration in range(iterations + 1):
        positive = project_psd(z)
        reflected = [2.0 * x - y for x, y in zip(positive, z)]
        affine = affine_projection(reflected)
        z = [old + new - pos for old, new, pos in zip(z, affine, positive)]
        if iteration % 25 == 0 or iteration == iterations:
            candidate = affine_projection(positive)
            residual = la.norm(apply_marginal(blocks, candidate) - target)
            minimum = min(la.eigvalsh((x + x.T) / 2.0)[0] for x in candidate)
            positive_residual = np.sqrt(sum(
                np.sum(np.minimum(la.eigvalsh((x + x.T) / 2.0), 0.0) ** 2)
                for x in candidate
            ))
            score = max(residual, positive_residual)
            if best is None or score < best[0]:
                best = (score, residual, positive_residual, minimum, candidate)
            if iteration % 250 == 0:
                print(
                    f"iter {iteration:5d} residual={residual:.3e} "
                    f"psd_defect={positive_residual:.3e} min={minimum:.3e}"
                )
            if residual < 2e-10 and positive_residual < 2e-10:
                break
    return best


def main():
    qout, target = load_exact_target()
    print("target trace/min/max:", np.trace(target), *la.eigvalsh(target)[[0, -1]])
    blocks = []
    for index, shapes in enumerate(candidate_blocks(), 1):
        block = construct_block(shapes, qout)
        blocks.append(block)
        print(
            f"block {index:2d}/23 {shapes}: relevant={block['dimension']} "
            f"channels={len(block['kraus'])} omega={block['omega_rank']}"
        )
    print("total relevant PSD dimension:", sum(block["dimension"] for block in blocks))
    print("total relevant symmetric variables:", sum(
        block["dimension"] * (block["dimension"] + 1) // 2 for block in blocks
    ))
    best = solve_feasibility(blocks, target)
    print(
        "best score/residual/PSD defect/min eigenvalue:",
        best[0], best[1], best[2], best[3],
    )


if __name__ == "__main__":
    main()
