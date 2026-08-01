#!/usr/bin/env python3
"""Discover an exposing functional for a boundary degree-three extension.

Given a source-reduced (or full ordered) near-feasible moment, this script
forms its stable component kernels.  It then constructs the target-space
Gram operator

    H = A (I - P_face) A^*,

whose nullspace consists exactly of target functionals y for which every
dual slack block A^*y is supported on those kernels.  Positive nullspace
slacks expose the primal face.

This is floating-point discovery code.  Any functional selected here must be
reconstructed and verified in the exact rational coordinates.
"""

from argparse import ArgumentParser
from pathlib import Path
import pickle
import sys

import numpy as np
import scipy.linalg as la


ROOT = Path(__file__).resolve().parents[1]
DISCOVERY = ROOT / "discovery"
sys.path.insert(0, str(DISCOVERY))

import agent_dth_level2_joint_extension as JOINT
import agent_dth_level2_joint_symmetry as TARGET_SYMMETRY
import agent_dth_level2_source_symmetry as SOURCE_SYMMETRY
import agent_dth_level2_source_reduced_full as REDUCED


DEFAULT_MAP = DISCOVERY / "dth_level2_full_blocks.pkl"
DEFAULT_CANDIDATE = DISCOVERY / "dth_level2_source_reduced_from_raw_floor0.pkl"
DEFAULT_GRAM = DISCOVERY / "dth_level2_face_violation_gram.npz"


def load_components(candidate, reduction):
    with candidate.open("rb") as stream:
        payload = pickle.load(stream)
    if "shifted_components" in payload:
        return payload["shifted_components"]
    if "shifted_candidate" in payload:
        return SOURCE_SYMMETRY.reduce_adjoint(
            reduction, payload["shifted_candidate"]
        )
    raise ValueError("candidate has neither reduced nor ordered source blocks")


def stable_kernels(components, threshold):
    kernels = []
    census = []
    for index, value in enumerate(components):
        eigenvalues, eigenvectors = la.eigh((value + value.T) / 2.0)
        selected = eigenvalues <= threshold
        kernels.append(eigenvectors[:, selected])
        census.append((
            index, value.shape[0], int(np.sum(selected)),
            float(eigenvalues[0]), float(eigenvalues[-1]),
        ))
    return kernels, census


def face_complement(values, kernels):
    output = []
    for value, kernel in zip(values, kernels):
        supported = kernel @ (kernel.T @ value @ kernel) @ kernel.T
        output.append(value - supported)
    return output


def build_face_gram(reduction, directions, kernels):
    dimension = len(directions)
    gram = np.empty((dimension, dimension))
    for column, direction in enumerate(directions):
        slack = REDUCED.reduced_adjoint(reduction, direction)
        violation = face_complement(slack, kernels)
        image = REDUCED.reduced_marginal(reduction, violation)
        gram[:, column] = TARGET_SYMMETRY.invariant_coordinates(
            image, directions
        )
        if column % 20 == 0:
            print("face violation Gram column", column, "/", dimension)
    gram = (gram + gram.T) / 2.0
    return gram


def direction_from_coordinates(reduction, directions, coordinates):
    return REDUCED.coordinates_to_direction(
        reduction, directions, coordinates
    )


def slack_metrics(reduction, directions, target_coordinates, coordinates,
                  kernels):
    direction = direction_from_coordinates(reduction, directions, coordinates)
    slack = REDUCED.reduced_adjoint(reduction, direction)
    trace = sum(np.trace(value) for value in slack)
    if trace < 0:
        coordinates = -coordinates
        slack = [-value for value in slack]
        trace = -trace
    norm = np.sqrt(sum(la.norm(value) ** 2 for value in slack))
    if norm:
        slack = [value / norm for value in slack]
        coordinates = coordinates / norm
        trace /= norm
    spectra = [la.eigvalsh((value + value.T) / 2.0) for value in slack]
    defect = np.sqrt(sum(
        np.sum(np.minimum(spectrum, 0.0) ** 2) for spectrum in spectra
    ))
    violation = face_complement(slack, kernels)
    violation_norm = np.sqrt(sum(la.norm(value) ** 2 for value in violation))
    return {
        "coordinates": coordinates,
        "minimum": min(spectrum[0] for spectrum in spectra),
        "defect": defect,
        "trace": trace,
        "face_violation": violation_norm,
        "target_pairing": float(target_coordinates @ coordinates),
        "positive_blocks": sum(spectrum[0] >= -1e-10 for spectrum in spectra),
    }


def main():
    parser = ArgumentParser()
    parser.add_argument("--map-cache", type=Path, default=DEFAULT_MAP)
    parser.add_argument("--candidate", type=Path, default=DEFAULT_CANDIDATE)
    parser.add_argument("--gram-cache", type=Path, default=DEFAULT_GRAM)
    parser.add_argument("--kernel-threshold", type=float, default=1e-12)
    parser.add_argument("--report", type=int, default=20)
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()

    with args.map_cache.open("rb") as stream:
        data = pickle.load(stream)
    JOINT.TARGETS = tuple(data["targets"])
    reduction = SOURCE_SYMMETRY.build_reduction(
        data["blocks"], data["target_data"], audit=args.audit
    )
    directions = TARGET_SYMMETRY.invariant_target_basis(data["target_data"])
    target = TARGET_SYMMETRY.invariant_projection(
        data["target_data"], directions
    )
    target_coordinates = TARGET_SYMMETRY.invariant_coordinates(
        target, directions
    )
    components = load_components(args.candidate, reduction)
    kernels, census = stable_kernels(components, args.kernel_threshold)
    print(
        "kernel threshold/count/components:", args.kernel_threshold,
        sum(row[2] for row in census),
        sum(row[2] > 0 for row in census),
    )
    print("twenty largest kernels:")
    for row in sorted(census, key=lambda value: value[2], reverse=True)[:20]:
        print(" ", row)

    if args.gram_cache.exists():
        stored = np.load(args.gram_cache)
        gram = stored["gram"]
        stored_threshold = float(stored["kernel_threshold"])
        if stored_threshold != args.kernel_threshold:
            raise ValueError(
                f"cached threshold {stored_threshold} != {args.kernel_threshold}"
            )
        print("loaded face violation Gram:", args.gram_cache)
    else:
        gram = build_face_gram(reduction, directions, kernels)
        np.savez_compressed(
            args.gram_cache, gram=gram,
            kernel_threshold=args.kernel_threshold,
        )
        print("saved face violation Gram:", args.gram_cache)

    eigenvalues, eigenvectors = la.eigh(gram)
    scale = max(1.0, eigenvalues[-1])
    print("face Gram spectrum:", eigenvalues[0], eigenvalues[-1])
    print("small eigenvalue census:", {
        threshold: int(np.sum(eigenvalues <= threshold * scale))
        for threshold in (1e-14, 1e-12, 1e-10, 1e-8, 1e-6)
    })
    for index in range(min(args.report, len(eigenvalues))):
        metrics = slack_metrics(
            reduction, directions, target_coordinates,
            eigenvectors[:, index], kernels,
        )
        print(
            "candidate", index, "face-eigenvalue", eigenvalues[index],
            "minimum/defect/face/pairing/positive-blocks",
            metrics["minimum"], metrics["defect"],
            metrics["face_violation"], metrics["target_pairing"],
            metrics["positive_blocks"],
        )


if __name__ == "__main__":
    main()
