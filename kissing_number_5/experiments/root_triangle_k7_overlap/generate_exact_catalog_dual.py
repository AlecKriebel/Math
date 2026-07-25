#!/usr/bin/env python3
"""Generate the exact finite-catalog root-triangle dual certificate.

The NumPy moment cache and numerical seed are discovery aids.  The resulting
JSON is checked from the original catalog by a separate standard-library
verifier.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
CATALOG = (
    ROOT
    / "experiments"
    / "centered_quarter_k6_rank"
    / "k7"
    / "results"
    / "direct_k7_from_51.csv"
)
SEED = HERE / "exact_dual_seed.json"
MOMENTS = HERE / "root_triangle_degree3_moments.npz"
OUTPUT = HERE / "root_triangle_degree3_catalog_dual.json"

SOURCE_SHA256 = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)
CATALOG_SHA256 = (
    "16cee0b4f7b6b7655990a74f7ffef104c4aef43d5074696cbbb1bcf413d1a623"
)
SEED_SHA256 = (
    "026695345deccff04b5210d9ff45061e869258e7c50ff3e86fc67794430e558c"
)
MOMENTS_SHA256 = (
    "d2e79f0604eccce564bfa79d9c052f98996cbc54aa33789ce261aa69e53fae15"
)
KERNEL = {"2": 703, "3": 12654, "4": 442890}
LOCAL_EDGES = (
    (0, 1),
    (0, 2),
    (1, 2),
    (0, 3),
    (0, 4),
    (1, 3),
    (1, 4),
    (2, 3),
    (2, 4),
    (3, 4),
)
LOCAL_EDGE_INDEX = {pair: index for index, pair in enumerate(LOCAL_EDGES)}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_integers(values):
    payload = "".join(f"{value}\n" for value in values).encode()
    return hashlib.sha256(payload).hexdigest()


def weak_compositions(total, length):
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, length - 1):
            yield (first,) + rest


def invariant_monomial_orbits():
    actions = []
    for root_permutation in itertools.permutations(range(3)):
        for extension_permutation in ((3, 4), (4, 3)):
            permutation = tuple(root_permutation) + extension_permutation
            actions.append(
                tuple(
                    LOCAL_EDGE_INDEX[
                        tuple(
                            sorted(
                                (
                                    permutation[first],
                                    permutation[second],
                                )
                            )
                        )
                    ]
                    for first, second in LOCAL_EDGES
                )
            )
    exponents = tuple(
        exponent
        for degree in range(4)
        for exponent in weak_compositions(degree, 10)
    )
    seen = set()
    orbits = []
    for exponent in exponents:
        if exponent in seen:
            continue
        orbit = set()
        for action in actions:
            image = [0] * 10
            for old_index, new_index in enumerate(action):
                image[new_index] = exponent[old_index]
            orbit.add(tuple(image))
        seen.update(orbit)
        orbits.append(tuple(sorted(orbit)))
    if len(orbits) != 48 or len(seen) != 286:
        raise RuntimeError("wrong invariant monomial basis")
    return tuple(orbits)


def main():
    if sha256(SOURCE) != SOURCE_SHA256:
        raise RuntimeError("source hash mismatch")
    if sha256(CATALOG) != CATALOG_SHA256:
        raise RuntimeError("catalog hash mismatch")
    if sha256(SEED) != SEED_SHA256:
        raise RuntimeError("seed hash mismatch")
    if sha256(MOMENTS) != MOMENTS_SHA256:
        raise RuntimeError("moment-cache hash mismatch")

    source = json.loads(SOURCE.read_text())
    seed = json.loads(SEED.read_text())
    factor = np.asarray(seed["B"], dtype=object)
    dual = tuple(int(value) for value in seed["Y"])
    if factor.shape != (48, 8) or len(dual) != 52:
        raise RuntimeError("wrong dual dimensions")

    lines = CATALOG.read_text().splitlines()
    triangle_counts = []
    for line in lines[1:]:
        fields = tuple(map(int, line.split(",")))
        counts = [0] * 51
        for triangle in fields[21:]:
            counts[triangle] += 1
        triangle_counts.append(tuple(counts))

    moments = np.load(MOMENTS)["moments"].astype(object)
    if moments.shape != (len(triangle_counts), 48, 48):
        raise RuntimeError("moment cache has wrong shape")
    projections = []
    for moment in moments:
        value = 0
        for column in range(8):
            vector = factor[:, column]
            value += int(vector @ moment @ vector)
        projections.append(value)

    slacks = [
        dual[0]
        + sum(
            dual[1 + triangle] * counts[triangle]
            for triangle in range(51)
        )
        - projection
        for counts, projection in zip(triangle_counts, projections)
    ]
    if min(slacks) < 0:
        raise RuntimeError("dual has a negative atom slack")

    target = [Q(1)] + [
        Q(7) * Q(value) / 312 for value in source["nu"]
    ]
    objective = sum(value * coefficient for value, coefficient in zip(dual, target))
    if objective >= 0:
        raise RuntimeError("dual objective is not negative")

    certificate = {
        "schema": "kissing5.root_triangle_degree3_catalog_dual.v1",
        "status": (
            "exact rank-eight sum-of-squares dual excluding every mixture "
            "over the authenticated 1782-atom K7 catalog with the fixed "
            "triangle marginal"
        ),
        "scope_warning": (
            "The K7 catalog is incomplete. This is an exact finite-catalog "
            "obstruction, not a continuous nonexistence theorem and not an "
            "upper bound on tau(5)."
        ),
        "target_cardinality": 41,
        "local_size": 7,
        "root_size": 3,
        "extension_size": 2,
        "feature_degree": 3,
        "feature_dimension": 48,
        "local_edge_variable_order": [
            "r01",
            "r02",
            "r12",
            "r0p",
            "r0q",
            "r1p",
            "r1q",
            "r2p",
            "r2q",
            "pq",
        ],
        "basis_definition": (
            "Orbit sums of all monomials of total degree at most three, "
            "ordered by degree, weak-composition order, and first unseen "
            "orbit, under S3 on roots and S2 on extension vertices."
        ),
        "feature_orbits": [
            [list(exponent) for exponent in orbit]
            for orbit in invariant_monomial_orbits()
        ],
        "sum_of_squares_rank": 8,
        "integer_kernel_by_union_size": KERNEL,
        "kernel_note": (
            "Six times binom(38,u)/binom(4,u), for u=2,3,4."
        ),
        "source": str(SOURCE.relative_to(ROOT)),
        "source_sha256": SOURCE_SHA256,
        "catalog": str(CATALOG.relative_to(ROOT)),
        "catalog_sha256": CATALOG_SHA256,
        "catalog_header": lines[0],
        "catalog_atoms": len(triangle_counts),
        "factor_B": seed["B"],
        "triangle_dual_Y": list(dual),
        "target_objective": str(objective),
        "minimum_atom_slack": min(slacks),
        "zero_slack_catalog_indices": [
            index for index, slack in enumerate(slacks) if slack == 0
        ],
        "atom_projection_sha256": digest_integers(projections),
        "atom_slack_sha256": digest_integers(slacks),
        "discovery_seed": str(SEED.relative_to(ROOT)),
        "discovery_seed_sha256": SEED_SHA256,
        "discovery_moment_cache": str(MOMENTS.relative_to(ROOT)),
        "discovery_moment_cache_sha256": MOMENTS_SHA256,
    }
    OUTPUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(OUTPUT)
    print(sha256(OUTPUT))
    print("objective", objective)
    print("minimum_slack", min(slacks))


if __name__ == "__main__":
    main()
