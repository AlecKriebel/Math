#!/usr/bin/env python3
"""Orbit-streamed Gamma_A crossing of a saved degree-three DTH candidate.

This is the source-site-symmetry version of
``agent_dth_level2_cross_candidate.py``.  It reconstructs only the 112 sorted
source representatives.  Every ordered member is obtained by permuting the
three raw Specht tensor axes, so the 487 expensive union reconstructions are
not repeated.

The script initially materializes only mixed multiplicity blocks below a
requested dimension.  It is floating-point discovery infrastructure; exact
sign claims require rational reconstruction.
"""

from argparse import ArgumentParser
from itertools import product
from pathlib import Path
import pickle
import sys


ROOT = Path(__file__).resolve().parents[1]
DISCOVERY = ROOT / "discovery"
sys.path.insert(0, str(DISCOVERY))

import numpy as np
import scipy.linalg as la

import agent_dth_level2_cross_candidate as BASE
import agent_dth_level2_joint_extension as JOINT
import agent_dth_level2_reconstruct_union as RECONSTRUCT
import agent_dth_level2_source_symmetry as SOURCE_SYMMETRY


DEFAULT_OUTPUT = DISCOVERY / "dth_level2_crossed_orbit_blocks.pkl"


def representative_values(reduction, physical_components):
    """Return unscaled representative densities in orbit order."""
    cursor = 0
    output = []
    for orbit in reduction["orbits"]:
        dimension = orbit["transports"][orbit["representative"]].shape[0]
        value = np.zeros((dimension, dimension))
        for descriptor in orbit["components"]:
            value += SOURCE_SYMMETRY.embed_component(
                physical_components[cursor], descriptor
            )
            cursor += 1
        output.append(value)
    assert cursor == len(physical_components)
    return tuple(output)


def member_permutation(representative, member):
    return next(
        permutation for permutation in SOURCE_SYMMETRY.PERMUTATIONS
        if SOURCE_SYMMETRY.permute_triple(
            representative, permutation
        ) == member
    )


def permute_raw_factor(factor, permutation):
    """Permute the three physical-site Specht axes, retaining rank last."""
    return np.transpose(factor, tuple(permutation) + (3,))


def local_choi_factors(local, tolerance=2e-10):
    """Signed low-rank Choi factors of every local crossing block."""
    output = {}
    maximum_rank = 0
    maximum_error = 0.0
    for key, crossing in local.items():
        mixed = crossing.shape[0]
        holomorphic = crossing.shape[2]
        choi = crossing.transpose(0, 2, 1, 3).reshape(
            mixed * holomorphic, mixed * holomorphic
        )
        asymmetry = la.norm(choi - choi.T) / max(1.0, la.norm(choi))
        assert asymmetry < 3e-12, (key, asymmetry)
        choi = (choi + choi.T) / 2.0
        eigenvalues, eigenvectors = la.eigh(choi)
        scale = max(1.0, np.max(np.abs(eigenvalues)))
        keep = np.abs(eigenvalues) > tolerance * scale
        values = eigenvalues[keep]
        transforms = eigenvectors[:, keep].T.reshape(
            np.sum(keep), mixed, holomorphic
        )
        rebuilt = np.einsum(
            "h,hpa,hqd->pqad", values, transforms, transforms,
            optimize=True,
        )
        error = la.norm(rebuilt - crossing) / max(1.0, la.norm(crossing))
        assert error < 4e-10, (key, error)
        output[key] = (values, transforms)
        maximum_rank = max(maximum_rank, len(values))
        maximum_error = max(maximum_error, error)
    return output, maximum_rank, maximum_error


def crossed_contribution_factored(factors, source_factor, mixed, source):
    """Apply three local crossings as a signed sum of Gram matrices."""
    values_first, first = factors[(mixed[0], source[0])]
    values_second, second = factors[(mixed[1], source[1])]
    values_third, third = factors[(mixed[2], source[2])]

    # G1[x,p,b,c,k]
    transformed = np.tensordot(first, source_factor, axes=([2], [0]))
    # Raw tensordot order is [y,r,x,p,c,k]; reorder to [x,y,p,r,c,k].
    transformed = np.tensordot(
        second, transformed, axes=([2], [2])
    ).transpose(2, 0, 3, 1, 4, 5)
    # Raw order [z,t,x,y,p,r,k]; reorder to [x,y,z,p,r,t,k].
    transformed = np.tensordot(
        third, transformed, axes=([2], [4])
    ).transpose(2, 3, 0, 4, 5, 1, 6)

    output_dimension = int(np.prod(transformed.shape[3:6]))
    rank = transformed.shape[-1]
    transformed = transformed.reshape(-1, output_dimension, rank)
    weights = (
        values_first[:, None, None]
        * values_second[None, :, None]
        * values_third[None, None, :]
    ).reshape(-1)
    positive = weights > 0
    negative = weights < 0

    def gram(selected, signs):
        if not np.any(selected):
            return np.zeros((output_dimension, output_dimension))
        columns = (
            np.sqrt(signs[selected])[:, None, None]
            * transformed[selected]
        ).transpose(1, 0, 2).reshape(output_dimension, -1)
        return columns @ columns.T

    return gram(positive, weights) - gram(negative, -weights)


def main():
    parser = ArgumentParser()
    parser.add_argument("--blocks", type=Path, default=BASE.DEFAULT_BLOCKS)
    parser.add_argument("--candidate", type=Path, default=BASE.DEFAULT_CANDIDATE)
    parser.add_argument("--crossing", type=Path, default=BASE.DEFAULT_CROSSING)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-mixed-dimension", type=int, default=25)
    parser.add_argument(
        "--ordered-output", action="store_true",
        help=("materialize every ordered physical-site block; by default "
              "only sorted representatives are retained because the "
              "candidate and crossing are site invariant"),
    )
    parser.add_argument("--limit-orbits", type=int, default=None)
    parser.add_argument("--report", type=int, default=5)
    parser.add_argument(
        "--audit-members", action="store_true",
        help="reconstruct one nonrepresentative member per orbit and compare",
    )
    args = parser.parse_args()

    with args.blocks.open("rb") as stream:
        data = pickle.load(stream)
    JOINT.TARGETS = tuple(data["targets"])
    RECONSTRUCT.ENGINE.TARGETS = tuple(data["targets"])
    reduction = SOURCE_SYMMETRY.build_reduction(
        data["blocks"], data["target_data"], audit=False, compile_maps=False
    )
    with args.candidate.open("rb") as stream:
        candidate = pickle.load(stream)
    shift = SOURCE_SYMMETRY.physical_floor_shift(
        reduction, candidate["floor"]
    )
    physical_components = [
        value + delta for value, delta in zip(
            candidate["shifted_components"], shift
        )
    ]
    representatives = representative_values(reduction, physical_components)
    ordered_audit = (
        SOURCE_SYMMETRY.expand(reduction, physical_components)
        if args.audit_members else None
    )

    crossing = np.load(args.crossing)
    local, holomorphic_multiplicities, mixed_multiplicities = BASE.local_blocks(
        crossing
    )
    factors, maximum_choi_rank, choi_error = local_choi_factors(local)
    print("local Choi maximum rank/reconstruction error:",
          maximum_choi_rank, choi_error, flush=True)
    selected = tuple(
        triple for triple in product(range(len(mixed_multiplicities)), repeat=3)
        if np.prod([mixed_multiplicities[index] for index in triple])
        <= args.max_mixed_dimension
        and (args.ordered_output or tuple(sorted(triple)) == triple)
    )
    output = {
        triple: np.zeros((
            int(np.prod([mixed_multiplicities[index] for index in triple])),
        ) * 2)
        for triple in selected
    }
    print("selected mixed blocks:", len(selected), flush=True)

    block_by_source = {
        tuple(block["source"]): block for block in data["blocks"]
    }
    block_index_by_source = {
        tuple(block["source"]): index
        for index, block in enumerate(data["blocks"])
    }
    orbit_count = len(reduction["orbits"])
    if args.limit_orbits is not None:
        orbit_count = min(orbit_count, args.limit_orbits)
    maximum_member_error = 0.0
    for orbit_index, (orbit, source_matrix) in enumerate(zip(
        reduction["orbits"][:orbit_count], representatives[:orbit_count]
    ), 1):
        representative = tuple(orbit["representative"])
        block = block_by_source[representative]
        union, _, metrics = RECONSTRUCT.reconstruct_union(
            block, data["target_data"], audit=True
        )
        eigenvalues, eigenvectors = la.eigh(
            (source_matrix + source_matrix.T) / 2.0
        )
        assert eigenvalues[0] > -2e-16, (representative, eigenvalues[0])
        orbit_scale = 1.0 / np.sqrt(len(orbit["members"]))
        coefficient_factor = eigenvectors * np.sqrt(
            orbit_scale * np.maximum(eigenvalues, 0.0)
        )
        raw_factor = union @ coefficient_factor
        raw_factor = raw_factor.reshape(
            *(holomorphic_multiplicities[index] for index in representative),
            raw_factor.shape[1],
        )

        audited_member = False
        for member in orbit["members"]:
            member = tuple(member)
            permutation = member_permutation(representative, member)
            member_factor = permute_raw_factor(raw_factor, permutation)
            assert member_factor.shape[:3] == tuple(
                holomorphic_multiplicities[index] for index in member
            )
            compatible = [
                mu for mu in selected
                if all((mu[site], member[site]) in local for site in range(3))
            ]
            for mu in compatible:
                output[mu] += crossed_contribution_factored(
                    factors, member_factor, mu, member
                )

            if (args.audit_members and not audited_member
                    and member != representative
                    and member_factor.size <= 3_000_000):
                member_block = block_by_source[member]
                member_union, _, _ = RECONSTRUCT.reconstruct_union(
                    member_block, data["target_data"], audit=True
                )
                member_index = block_index_by_source[member]
                assert ordered_audit is not None
                expanded = ordered_audit[member_index]
                expected = member_union @ expanded @ member_union.T
                actual_matrix = member_factor.reshape(-1, member_factor.shape[-1])
                actual = actual_matrix @ actual_matrix.T
                error = la.norm(actual - expected) / max(1.0, la.norm(expected))
                assert error < 5e-7, (representative, member, error)
                maximum_member_error = max(maximum_member_error, error)
                audited_member = True

        if orbit_index % args.report == 0 or orbit_index == orbit_count:
            print(
                "crossed source orbits", orbit_index, "/", orbit_count,
                "representative", representative,
                "raw/rank", union.shape,
                "members", len(orbit["members"]),
                "union error", metrics["isometry_error"],
                flush=True,
            )

    rows = []
    for triple, matrix in output.items():
        matrix = (matrix + matrix.T) / 2.0
        values = la.eigvalsh(matrix)
        trace = float(np.trace(matrix))
        negative = float(np.sqrt(np.sum(np.minimum(values, 0.0) ** 2)))
        quotient = float(values[0] / max(abs(trace), 1e-300))
        rows.append((
            quotient, triple, matrix.shape[0], values[0], values[-1],
            trace, negative,
        ))
        output[triple] = matrix
    rows.sort()
    print("maximum raw-member covariance error:", maximum_member_error)
    print("thirty least crossed blocks:")
    for row in rows[:30]:
        print(" ", row)
    with args.output.open("wb") as stream:
        pickle.dump({
            "max_mixed_dimension": args.max_mixed_dimension,
            "orbit_count": orbit_count,
            "maximum_member_error": maximum_member_error,
            "spectral_rows": rows,
            "blocks": output,
        }, stream, pickle.HIGHEST_PROTOCOL)
    print("saved:", args.output)


if __name__ == "__main__":
    main()
