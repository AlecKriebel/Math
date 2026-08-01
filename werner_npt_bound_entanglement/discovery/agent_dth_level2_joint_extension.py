#!/usr/bin/env python3
"""Joint numerical S_(3,3) extension test for DTH sectors 444,333,433.

Unlike separate sector tests, this script uses one PSD source block for every
S7 local type and requires it to reproduce all five ordered target blocks

    444, 333, 433, 343, 334

simultaneously.  It imports the Young/projector machinery from the companion
444 script.  Output remains numerical discovery evidence.
"""

from functools import lru_cache
from itertools import permutations, product
from pathlib import Path
import gzip
import importlib.util
import json
import sys

import numpy as np
import scipy.linalg as la


ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "verification"
DISCOVERY = ROOT / "discovery"
sys.path.insert(0, str(VERIFY))
sys.path.insert(0, str(DISCOVERY))

import agent_dth_level2_444_extension as BASE
import verify_dth_level2_s7_census as CENSUS


CORE_TARGETS = ((4, 4, 4), (3, 3, 3), (4, 3, 3), (3, 4, 3), (3, 3, 4))
TARGETS = CORE_TARGETS
S5_SHAPES = ((5,), (4, 1), (3, 2), (3, 1, 1), (2, 2, 1))
S5_CARRIER_DIMS = (21, 24, 15, 6, 3)
S7_CARRIER_DIMS = (36, 48, 42, 15, 24, 15, 6, 3)
OMEGA_LOCAL_OUTPUT = {
    3: (4,),
    5: (3, 1),
    6: (2, 2),
    7: (2, 1, 1),
}
RNG = np.random.default_rng(20260802)


@lru_cache(None)
def exact_k_module():
    module_path = VERIFY / "agent_dth_exact_k_coordinates.py"
    spec = importlib.util.spec_from_file_location("joint_exact_k", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


@lru_cache(None)
def local_intertwiner(target_index):
    exact_k = exact_k_module()
    shape = S5_SHAPES[target_index]
    dimension = len(BASE.standard_tableaux(shape))
    out = np.zeros((dimension, dimension))
    for permutation in permutations(range(5)):
        poly = np.array(exact_k.local_representation(target_index, permutation), dtype=float)
        semi = BASE.representation(shape, permutation)
        out += poly @ semi
    gram = np.array(exact_k.local_gram(target_index), dtype=float)
    scalar_matrix = out.T @ gram @ out
    scalar = np.trace(scalar_matrix) / dimension
    out /= np.sqrt(scalar)
    assert np.linalg.norm(out.T @ gram @ out - np.eye(dimension)) < 3e-9
    for generator in range(4):
        permutation = BASE.transposition(5, generator, generator + 1)
        poly = np.array(exact_k.local_representation(target_index, permutation), dtype=float)
        semi = BASE.representation(shape, permutation)
        assert np.linalg.norm(poly @ out - out @ semi) < 3e-9
    return out


@lru_cache(None)
def certificate_coordinates():
    certificate = VERIFY / "certificates/dth_complete_ppt_pseudomoment.json.gz"
    with gzip.open(certificate, "rt", encoding="utf-8") as stream:
        payload = json.load(stream)
    return {tuple(map(int, block["shape"])): block for block in payload["blocks"]}


def decode_chart(block):
    dimension = block["dimension"]
    chart = np.zeros((dimension, dimension))
    cursor = 0
    for row in range(dimension):
        numerator, denominator = block["upper"][cursor]
        chart[row, row] = int(numerator) / int(denominator)
        cursor += 1
    for row in range(dimension):
        for column in range(row + 1, dimension):
            numerator, denominator = block["upper"][cursor]
            value = int(numerator) / int(denominator)
            chart[row, column] = chart[column, row] = value
            cursor += 1
    return chart


@lru_cache(None)
def load_target(target):
    exact_k = exact_k_module()
    physical, _, _ = exact_k.hol_k_coordinates(target)
    physical = np.array(physical, dtype=float)
    local = [local_intertwiner(index) for index in target]
    total = BASE.kron3(tuple(local))
    physical_semi = la.solve(total, physical)
    gram = physical_semi.T @ physical_semi
    root = la.sqrtm(gram).real
    qout = physical_semi @ la.inv(root)
    assert np.linalg.norm(qout.T @ qout - np.eye(qout.shape[1])) < 5e-8
    chart = decode_chart(certificate_coordinates()[target])
    moment = root @ chart @ root
    moment = (moment + moment.T) / 2.0
    if moment.shape[0]:
        assert la.eigvalsh(moment)[0] > -2e-13
    return qout, moment


@lru_cache(None)
def sequential_branch_embeddings(source_index, target_index):
    source_shape = BASE.S7[source_index]
    target_shape = S5_SHAPES[target_index]
    source_tabs = BASE.standard_tableaux(source_shape)
    target_tabs = BASE.standard_tableaux(target_shape)
    target_lookup = {tab: i for i, tab in enumerate(target_tabs)}
    grouped = {}
    for source_row, tab in enumerate(source_tabs):
        restricted = tuple(tab[:5])
        counts = {}
        for row, column in restricted:
            counts[row] = counts.get(row, 0) + 1
        restricted_shape = tuple(counts[row] for row in range(len(counts)))
        if restricted_shape != target_shape:
            continue
        path = (tab[5], tab[6])
        matrix = grouped.setdefault(
            path, np.zeros((len(source_tabs), len(target_tabs)))
        )
        matrix[source_row, target_lookup[restricted]] = 1.0
    return grouped


@lru_cache(None)
def branch_channels(source_index, target_index):
    sequential = sequential_branch_embeddings(source_index, target_index)
    if not sequential:
        return {}
    paths = sorted(sequential)
    swap = BASE.representation(
        BASE.S7[source_index], BASE.transposition(7, 5, 6)
    )
    f = len(BASE.standard_tableaux(S5_SHAPES[target_index]))
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
        assert np.linalg.norm(embedding.T @ embedding - np.eye(f)) < 4e-12
        out[label] = embedding
    exact_types = CENSUS.two_box_strip_types(
        BASE.S7[source_index], S5_SHAPES[target_index]
    )
    assert set(out) == set(exact_types)
    return out


def target_embeddings(source, target, qout):
    channels = [
        branch_channels(source[site], target[site]) for site in range(3)
    ]
    if not all(channels):
        return []
    out = []
    for labels in product(*(tuple(channel) for channel in channels)):
        if sum(label == "V" for label in labels) % 2 != 1:
            continue
        local = tuple(channels[site][labels[site]] for site in range(3))
        out.append(BASE.kron3(local) @ qout)
    return out


def target_reachable(source, target):
    channels = [
        branch_channels(source[site], target[site]) for site in range(3)
    ]
    if not all(channels):
        return False
    return any(
        sum(label == "V" for label in labels) % 2 == 1
        for labels in product(*(tuple(channel) for channel in channels))
    )


def omega_output_rank(source):
    if any(index not in OMEGA_LOCAL_OUTPUT for index in source):
        return 0
    return CENSUS.kronecker_coefficient(
        (2, 2), [OMEGA_LOCAL_OUTPUT[index] for index in source], 4
    )


@lru_cache(None)
def post_omega_source_rank(source):
    rank = CENSUS.kronecker_coefficient(
        (3, 3), [BASE.S7[index] for index in source], 6
    )
    return rank - omega_output_rank(source)


def candidate_sources(target_data):
    out = []
    for source in product(range(8), repeat=3):
        if (post_omega_source_rank(source) > 0
                and any(target_reachable(source, target) for target in TARGETS)):
            out.append(source)
    return out


def omega_range(source, raw_dimension, expected_rank):
    if expected_rank == 0:
        return np.zeros((raw_dimension, 0))
    trial = RNG.standard_normal((raw_dimension, expected_rank + 5))
    trial = BASE.source_project(trial, source)
    trial = BASE.omega_gram_action(trial, source)
    trial = BASE.source_project(trial, source)
    basis, values = BASE.orthonormal_columns(trial, tolerance=2e-9)
    assert basis.shape[1] == expected_rank, (source, basis.shape, expected_rank, values)
    return basis


def construct_source_block(source, target_data):
    raw_by_target = {}
    raw_dimension = None
    for target in TARGETS:
        embeddings = target_embeddings(source, target, target_data[target][0])
        if embeddings:
            raw_by_target[target] = embeddings
            raw_dimension = embeddings[0].shape[0]
    assert raw_by_target and raw_dimension is not None
    qomega = omega_range(source, raw_dimension, omega_output_rank(source))
    # Project all reachable target columns in one tensor pass.  This is a
    # substantial speedup for the full 118-block marginal while preserving
    # the separate Kraus-channel boundaries below.
    layout = []
    raw_columns = []
    cursor = 0
    for target, embeddings in raw_by_target.items():
        for embedding in embeddings:
            width = embedding.shape[1]
            layout.append((target, cursor, cursor + width))
            raw_columns.append(embedding)
            cursor += width
    all_vectors = BASE.source_project(np.hstack(raw_columns), source)
    all_vectors -= qomega @ (qomega.T @ all_vectors)
    projected = {target: [] for target in raw_by_target}
    for target, start, stop in layout:
        projected[target].append(all_vectors[:, start:stop])
    union, values = BASE.orthonormal_columns(all_vectors, tolerance=3e-9)
    assert np.linalg.norm(BASE.source_project(union, source) - union) < 6e-8
    assert np.linalg.norm(BASE.omega_gram_action(union, source)) < 6e-8
    maps = {
        target: [union.T @ vector for vector in vectors]
        for target, vectors in projected.items()
    }
    weights = {
        target: (
            np.prod([S7_CARRIER_DIMS[index] for index in source])
            / np.prod([S5_CARRIER_DIMS[index] for index in target])
        )
        for target in maps
    }
    return {
        "source": source,
        "dimension": union.shape[1],
        "maps": maps,
        "weights": weights,
        "omega_rank": omega_output_rank(source),
        "projection_spectrum": values,
    }


def zero_targets(target_data):
    return {target: np.zeros_like(target_data[target][1]) for target in TARGETS}


def apply_marginal(blocks, variables, target_data):
    out = zero_targets(target_data)
    for block, variable in zip(blocks, variables):
        for target, kraus_list in block["maps"].items():
            for kraus in kraus_list:
                out[target] += block["weights"][target] * kraus.T @ variable @ kraus
    return {target: (value + value.T) / 2.0 for target, value in out.items()}


def apply_adjoint(blocks, directions):
    out = []
    for block in blocks:
        value = np.zeros((block["dimension"],) * 2)
        for target, kraus_list in block["maps"].items():
            for kraus in kraus_list:
                value += block["weights"][target] * kraus @ directions[target] @ kraus.T
        out.append((value + value.T) / 2.0)
    return out


def target_basis(target_data):
    out = []
    for target in TARGETS:
        dimension = target_data[target][1].shape[0]
        for matrix in BASE.symmetric_basis(dimension):
            direction = zero_targets(target_data)
            direction[target] = matrix
            out.append((target, matrix, direction))
    return out


def target_inner(left, right):
    return sum(np.sum(left[target] * right[target]) for target in TARGETS)


def solve(blocks, target_data, iterations=6000):
    basis = target_basis(target_data)
    n = len(basis)
    superoperator = np.empty((n, n))
    for column, (_, _, direction) in enumerate(basis):
        image = apply_marginal(blocks, apply_adjoint(blocks, direction), target_data)
        for row, (target, test, _) in enumerate(basis):
            superoperator[row, column] = np.sum(test * image[target])
        if column % 50 == 0:
            print(f"AA* column {column}/{n}")
    superoperator = (superoperator + superoperator.T) / 2.0
    values, vectors = la.eigh(superoperator)
    threshold = 1e-11 * values[-1]
    print("AA* dimension/rank/spectrum:", n, np.sum(values > threshold), values[0], values[-1])
    inverse = (vectors * np.where(values > threshold, 1.0 / values, 0.0)) @ vectors.T
    target = {key: value for key, (_, value) in target_data.items()}

    def affine_projection(variables):
        image = apply_marginal(blocks, variables, target_data)
        residual = {key: image[key] - target[key] for key in TARGETS}
        coordinates = np.array([
            np.sum(test * residual[key]) for key, test, _ in basis
        ])
        correction_coordinates = inverse @ coordinates
        correction = zero_targets(target_data)
        for value, (key, test, _) in zip(correction_coordinates, basis):
            correction[key] += value * test
        adjoint = apply_adjoint(blocks, correction)
        return [variable - delta for variable, delta in zip(variables, adjoint)]

    variables = [np.zeros((block["dimension"],) * 2) for block in blocks]
    z = affine_projection(variables)
    best = None
    for iteration in range(iterations + 1):
        positive = BASE.project_psd(z)
        reflected = [2.0 * x - y for x, y in zip(positive, z)]
        affine = affine_projection(reflected)
        z = [old + new - pos for old, new, pos in zip(z, affine, positive)]
        if iteration % 25 == 0 or iteration == iterations:
            candidate = affine_projection(positive)
            image = apply_marginal(blocks, candidate, target_data)
            residual = np.sqrt(sum(
                la.norm(image[key] - target[key]) ** 2 for key in TARGETS
            ))
            psd_defect = np.sqrt(sum(
                np.sum(np.minimum(la.eigvalsh((x + x.T) / 2.0), 0.0) ** 2)
                for x in candidate
            ))
            minimum = min(la.eigvalsh((x + x.T) / 2.0)[0] for x in candidate)
            score = max(residual, psd_defect)
            if best is None or score < best[0]:
                best = (score, residual, psd_defect, minimum, candidate)
            if iteration % 250 == 0:
                print(
                    f"iter {iteration:5d} residual={residual:.3e} "
                    f"psd_defect={psd_defect:.3e} min={minimum:.3e}"
                )
            if residual < 2e-13 and psd_defect < 2e-13:
                break
    return best, values


def main():
    target_data = {target: load_target(target) for target in TARGETS}
    for target in TARGETS:
        moment = target_data[target][1]
        spectrum = la.eigvalsh(moment)
        print(
            "target", target, "dimension", moment.shape[0],
            "trace/min/max", np.trace(moment), spectrum[0], spectrum[-1],
        )
    sources = candidate_sources(target_data)
    print("candidate source blocks:", len(sources))
    blocks = []
    for index, source in enumerate(sources, 1):
        block = construct_source_block(source, target_data)
        blocks.append(block)
        print(
            f"source {index:2d}/{len(sources)} {source}: relevant={block['dimension']} "
            f"targets={len(block['maps'])} omega={block['omega_rank']}"
        )
    print("total relevant PSD rank:", sum(block["dimension"] for block in blocks))
    print("total relevant symmetric variables:", sum(
        block["dimension"] * (block["dimension"] + 1) // 2 for block in blocks
    ))
    best, aa_spectrum = solve(blocks, target_data)
    print("best score/residual/PSD defect/min:", best[:4])


if __name__ == "__main__":
    main()
