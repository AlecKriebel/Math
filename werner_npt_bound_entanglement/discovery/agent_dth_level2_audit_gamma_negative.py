#!/usr/bin/env python3
"""Independent audit of the robust cap-100 Gamma_A negative blocks.

The script recomputes only the four substantive mixed blocks from the saved
degree-three source candidate.  It streams 112 source-site representatives,
uses the low-rank signed-Choi contraction, and compares the result with the
independently saved cap-100 cache.  Several small raw contributions are also
recomputed with the original six-index contraction.

Finally, it converts each numerical negative eigenvector from the orthonormal
mixed basis to the exact rational highest-weight basis and finds a sparse
integer direction that retains negative expectation.  These directions are
pullback seeds, not exact negativity certificates, because the source
candidate and crossed blocks remain floating-point discovery objects.
"""

from pathlib import Path
import json
import pickle
import sys


ROOT = Path(__file__).resolve().parents[1]
DISCOVERY = ROOT / "discovery"
VERIFY = ROOT / "verification"
sys.path[:0] = [str(DISCOVERY), str(VERIFY)]

import numpy as np
import scipy.linalg as la

import agent_dth_level2_cross_candidate as BASE
import agent_dth_level2_cross_candidate_orbits as ORBITS
import agent_dth_level2_local_crossing as LOCAL_CROSSING
import agent_dth_level2_reconstruct_union as RECONSTRUCT
import agent_dth_level2_source_symmetry as SOURCE_SYMMETRY
import verify_dth_level2_mixed_support_census as EXACT_MIXED


TARGETS = ((1, 2, 9), (1, 4, 9), (0, 2, 5), (1, 4, 6))
MIXED_GL_WEIGHTS = (
    (5, 0, -2), (5, -1, -1), (4, 1, -2), (4, 0, -1),
    (3, 2, -2), (3, 1, -1), (3, 0, 0), (2, 2, -1),
    (2, 1, 0), (1, 1, 1),
)
MIXED_DYNKIN = (
    (5, 2), (6, 0), (3, 3), (4, 1), (1, 4),
    (2, 2), (3, 0), (0, 3), (1, 1), (0, 0),
)

DEFAULT_CACHE = DISCOVERY / "dth_level2_crossed_orbits_max100.pkl"
DEFAULT_REPORT = DISCOVERY / "dth_level2_gammaA_negative_audit.json"


def exact_basis_bridges():
    numerical = LOCAL_CROSSING.mixed_highest_weight_bases()
    exact = EXACT_MIXED.highest_weight_bases(2, 5)
    transforms = []
    grams = []
    errors = []
    for index, (indices, lookup, orthonormal) in enumerate(numerical):
        basis = exact[MIXED_DYNKIN[index]]
        raw = np.zeros((len(indices), len(basis)))
        for column, vector in enumerate(basis):
            for word, coefficient in vector.items():
                row = lookup[LOCAL_CROSSING.WORD_INDEX[word]]
                assert row >= 0
                raw[row, column] = float(coefficient)
        gram = raw.T @ raw
        transform = la.solve(
            gram, raw.T @ orthonormal, assume_a="pos"
        )
        error = la.norm(raw @ transform - orthonormal)
        assert error < 2e-13
        transforms.append(transform)
        grams.append(gram)
        errors.append(error)
    return tuple(transforms), tuple(grams), max(errors)


def sparse_integer_seed(target, vector, crossed, transforms, grams):
    transform = np.kron(
        np.kron(transforms[target[0]], transforms[target[1]]),
        transforms[target[2]],
    )
    gram = np.kron(
        np.kron(grams[target[0]], grams[target[1]]), grams[target[2]]
    )
    exact_coordinates = transform @ vector
    exact_crossed = transform @ crossed @ la.inv(transform)
    original = float(
        exact_coordinates @ gram @ exact_crossed @ exact_coordinates
    )
    for bits in range(31):
        integer = np.rint(exact_coordinates * (2 ** bits)).astype(np.int64)
        if not np.any(integer):
            continue
        norm = float(integer @ gram @ integer)
        expectation = float(integer @ gram @ exact_crossed @ integer)
        if expectation < 0:
            return {
                "rounding_bits": bits,
                "vector": integer.tolist(),
                "support": int(np.count_nonzero(integer)),
                "max_abs": int(np.max(np.abs(integer))),
                "gram_norm_squared": norm,
                "numerical_expectation": expectation,
                "numerical_rayleigh": expectation / norm,
                "unrounded_expectation": original,
            }
    raise AssertionError((target, original))


def main():
    with BASE.DEFAULT_BLOCKS.open("rb") as stream:
        data = pickle.load(stream)
    BASE.JOINT.TARGETS = tuple(data["targets"])
    RECONSTRUCT.ENGINE.TARGETS = tuple(data["targets"])
    reduction = SOURCE_SYMMETRY.build_reduction(
        data["blocks"], data["target_data"], audit=False, compile_maps=False
    )
    with BASE.DEFAULT_CANDIDATE.open("rb") as stream:
        candidate = pickle.load(stream)
    shift = SOURCE_SYMMETRY.physical_floor_shift(
        reduction, candidate["floor"]
    )
    physical_components = [
        value + delta for value, delta in zip(
            candidate["shifted_components"], shift
        )
    ]
    representatives = ORBITS.representative_values(
        reduction, physical_components
    )

    with DEFAULT_CACHE.open("rb") as stream:
        cached = pickle.load(stream)
    reference = {target: cached["blocks"][target] for target in TARGETS}
    eigenvectors = {}
    reference_spectra = {}
    for target, matrix in reference.items():
        values, vectors = la.eigh((matrix + matrix.T) / 2.0)
        eigenvectors[target] = vectors[:, 0]
        reference_spectra[target] = (
            float(values[0]), float(values[-1]), float(np.trace(matrix))
        )

    crossing = np.load(BASE.DEFAULT_CROSSING)
    local, holomorphic_multiplicities, mixed_multiplicities = BASE.local_blocks(
        crossing
    )
    factors, maximum_choi_rank, choi_error = ORBITS.local_choi_factors(local)
    rebuilt = {target: np.zeros_like(reference[target]) for target in TARGETS}
    contributions = {target: [] for target in TARGETS}
    direct_audits = []
    direct_count = {target: 0 for target in TARGETS}
    block_by_source = {
        tuple(block["source"]): block for block in data["blocks"]
    }

    for orbit_index, (orbit, source_matrix) in enumerate(zip(
        reduction["orbits"], representatives
    ), 1):
        representative = tuple(orbit["representative"])
        union, _, _ = RECONSTRUCT.reconstruct_union(
            block_by_source[representative], data["target_data"], audit=False
        )
        eigenvalues, source_vectors = la.eigh(
            (source_matrix + source_matrix.T) / 2.0
        )
        assert eigenvalues[0] > -2e-16
        orbit_scale = 1.0 / np.sqrt(len(orbit["members"]))
        raw = union @ (
            source_vectors * np.sqrt(
                orbit_scale * np.maximum(eigenvalues, 0.0)
            )
        )
        raw = raw.reshape(
            *(holomorphic_multiplicities[index] for index in representative),
            raw.shape[1],
        )
        for member in orbit["members"]:
            member = tuple(member)
            permutation = ORBITS.member_permutation(representative, member)
            factor = ORBITS.permute_raw_factor(raw, permutation)
            for target in TARGETS:
                if not all((target[site], member[site]) in factors
                           for site in range(3)):
                    continue
                value = ORBITS.crossed_contribution_factored(
                    factors, factor, target, member
                )
                rebuilt[target] += value
                direction = eigenvectors[target]
                rayleigh = float(direction @ value @ direction)
                contributions[target].append((rayleigh, member))

                raw_dimension = int(np.prod(factor.shape[:3]))
                if (direct_count[target] < 4 and raw_dimension <= 1500
                        and factor.shape[-1] <= 12):
                    direct = BASE.crossed_contribution(
                        local, factor, target, member
                    )
                    absolute_error = la.norm(direct - value)
                    direct_scale = max(la.norm(direct), la.norm(value))
                    relative_error = (
                        absolute_error / direct_scale
                        if direct_scale else 0.0
                    )
                    # Several first eligible source terms vanish to working
                    # precision.  Their relative error is consequently not a
                    # stable diagnostic; retain it in the report, but audit
                    # such terms by absolute error.  Non-negligible terms are
                    # audited by both absolute and relative error.
                    assert absolute_error < 2e-13
                    if direct_scale > 1e-11:
                        assert relative_error < 2e-11
                    direct_audits.append({
                        "target": target,
                        "source": member,
                        "absolute_error": float(absolute_error),
                        "relative_error": float(relative_error),
                        "direct_scale": float(direct_scale),
                        "raw_dimension": raw_dimension,
                        "source_factor_rank": int(factor.shape[-1]),
                    })
                    direct_count[target] += 1
        if orbit_index % 20 == 0:
            print("audited source orbits", orbit_index, "/ 112", flush=True)

    transforms, grams, bridge_error = exact_basis_bridges()
    report = {
        "status": (
            "numerical audit and exact-coordinate pullback seeds; "
            "not an exact infeasibility certificate"
        ),
        "maximum_local_choi_rank": maximum_choi_rank,
        "local_choi_reconstruction_error": float(choi_error),
        "exact_basis_bridge_error": float(bridge_error),
        "direct_raw_audits": direct_audits,
        "blocks": {},
    }
    for target in TARGETS:
        matrix = (rebuilt[target] + rebuilt[target].T) / 2.0
        relative = la.norm(matrix - reference[target]) / max(
            1.0, la.norm(reference[target])
        )
        absolute = la.norm(matrix - reference[target])
        values = la.eigvalsh(matrix)
        direction = eigenvectors[target]
        total_rayleigh = float(direction @ matrix @ direction)
        source_terms = sorted(contributions[target])
        seed = sparse_integer_seed(
            target, direction, reference[target], transforms, grams
        )
        carriers = [
            int(crossing["mixed_carrier_dimensions"][index])
            for index in target
        ]
        multiplicities = [
            int(crossing["mixed_multiplicities"][index])
            for index in target
        ]
        report["blocks"][str(target)] = {
            "mixed_indices": target,
            "gl3_weights": [MIXED_GL_WEIGHTS[index] for index in target],
            "su3_dynkin_labels": [MIXED_DYNKIN[index] for index in target],
            "carrier_dimensions": carriers,
            "carrier_product": int(np.prod(carriers)),
            "multiplicities": multiplicities,
            "multiplicity_dimension": int(np.prod(multiplicities)),
            "reference_spectrum": reference_spectra[target],
            "rebuilt_minimum_eigenvalue": float(values[0]),
            "cache_absolute_error": float(absolute),
            "cache_scaled_error": float(relative),
            "summed_negative_rayleigh": total_rayleigh,
            "ten_most_negative_source_terms": [
                {"value": value, "s7_shape_indices": source}
                for value, source in source_terms[:10]
            ],
            "ten_most_positive_source_terms": [
                {"value": value, "s7_shape_indices": source}
                for value, source in source_terms[-10:][::-1]
            ],
            "exact_basis_integer_seed": seed,
        }
        print(
            "target", target,
            "min/cache error/rayleigh:", values[0], absolute, total_rayleigh,
            "integer support:", seed["support"],
        )

    with DEFAULT_REPORT.open("w", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
        stream.write("\n")
    print("saved:", DEFAULT_REPORT)


if __name__ == "__main__":
    main()
