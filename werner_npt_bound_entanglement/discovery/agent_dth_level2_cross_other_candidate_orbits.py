#!/usr/bin/env python3
"""Stream a site-symmetric DTH source through Gamma_z or Gamma_AA.

This companion to ``agent_dth_level2_cross_candidate_orbits.py`` accepts any
audited local crossing cache.  It provides two contraction engines:

* ``choi`` uses signed local Choi factors and is exceptionally efficient for
  Gamma_z (every nonzero local block has Choi rank at most two);
* ``direct`` contracts the local four-index maps without expanding their
  Choi spectra and is the safe fallback for the direct Gamma_AA crossing.

Only selected small mixed blocks are materialized.  The source is rebuilt
once per physical-site orbit, so all 487 ordered source blocks are obtained
from 112 union reconstructions.  Output is numerical discovery evidence.
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
import agent_dth_level2_cross_candidate_orbits as ORBITS
import agent_dth_level2_joint_extension as JOINT
import agent_dth_level2_reconstruct_union as RECONSTRUCT
import agent_dth_level2_source_symmetry as SOURCE_SYMMETRY


DEFAULT_OUTPUT = DISCOVERY / "dth_level2_crossed_other_orbits.pkl"


def direct_contribution(local, source_factor, mixed, source):
    return BASE.crossed_contribution(local, source_factor, mixed, source)


def main():
    parser = ArgumentParser()
    parser.add_argument("--blocks", type=Path, default=BASE.DEFAULT_BLOCKS)
    parser.add_argument("--candidate", type=Path,
                        default=BASE.DEFAULT_CANDIDATE)
    parser.add_argument("--crossing", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--method", choices=("auto", "choi", "direct"),
                        default="auto")
    parser.add_argument("--max-mixed-dimension", type=int, default=25)
    parser.add_argument("--limit-orbits", type=int, default=None)
    parser.add_argument("--report", type=int, default=5)
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
        reduction, candidate.get("floor", 0.0)
    )
    physical_components = [
        value + delta for value, delta in zip(
            candidate["shifted_components"], shift
        )
    ]
    representatives = ORBITS.representative_values(
        reduction, physical_components
    )

    crossing = np.load(args.crossing)
    local, holomorphic_multiplicities, mixed_multiplicities = (
        BASE.local_blocks(crossing)
    )
    factors = None
    maximum_choi_rank = None
    choi_error = None
    if args.method in ("auto", "choi"):
        factors, maximum_choi_rank, choi_error = ORBITS.local_choi_factors(
            local
        )
    method = args.method
    if method == "auto":
        method = "choi" if maximum_choi_rank <= 4 else "direct"
    print("cut/method/local Choi max rank/error:",
          str(crossing.get("cut", "unknown")), method,
          maximum_choi_rank, choi_error, flush=True)

    selected = tuple(
        triple for triple in product(
            range(len(mixed_multiplicities)), repeat=3
        )
        if tuple(sorted(triple)) == triple
        and np.prod([
            mixed_multiplicities[index] for index in triple
        ]) <= args.max_mixed_dimension
    )
    output = {
        triple: np.zeros((dimension, dimension))
        for triple in selected
        for dimension in (int(np.prod([
            mixed_multiplicities[index] for index in triple
        ])),)
    }
    print("selected sorted mixed blocks:", len(selected), flush=True)

    block_by_source = {
        tuple(block["source"]): block for block in data["blocks"]
    }
    orbit_count = len(reduction["orbits"])
    if args.limit_orbits is not None:
        orbit_count = min(orbit_count, args.limit_orbits)
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
        raw_factor = (union @ coefficient_factor).reshape(
            *(holomorphic_multiplicities[index]
              for index in representative),
            coefficient_factor.shape[1],
        )

        for member in orbit["members"]:
            member = tuple(member)
            permutation = ORBITS.member_permutation(representative, member)
            member_factor = ORBITS.permute_raw_factor(raw_factor, permutation)
            compatible = [
                mixed for mixed in selected
                if all((mixed[site], member[site]) in local
                       for site in range(3))
            ]
            for mixed in compatible:
                if method == "choi":
                    output[mixed] += ORBITS.crossed_contribution_factored(
                        factors, member_factor, mixed, member
                    )
                else:
                    output[mixed] += direct_contribution(
                        local, member_factor, mixed, member
                    )

        if orbit_index % args.report == 0 or orbit_index == orbit_count:
            print(
                "crossed source orbits", orbit_index, "/", orbit_count,
                "representative", representative,
                "raw/rank", union.shape,
                "members", len(orbit["members"]),
                "union error", metrics["isometry_error"], flush=True,
            )

    rows = []
    for triple, matrix in output.items():
        matrix = (matrix + matrix.T) / 2.0
        values = la.eigvalsh(matrix)
        trace_value = float(np.trace(matrix))
        negative = float(np.sqrt(np.sum(np.minimum(values, 0.0) ** 2)))
        quotient = float(values[0] / max(abs(trace_value), 1e-300))
        rows.append((
            quotient, triple, matrix.shape[0], float(values[0]),
            float(values[-1]), trace_value, negative,
        ))
        output[triple] = matrix
    rows.sort()
    print("thirty least crossed blocks:")
    for row in rows[:30]:
        print(" ", row)
    with args.output.open("wb") as stream:
        pickle.dump({
            "crossing": str(args.crossing),
            "method": method,
            "max_mixed_dimension": args.max_mixed_dimension,
            "orbit_count": orbit_count,
            "spectral_rows": rows,
            "blocks": output,
        }, stream, pickle.HIGHEST_PROTOCOL)
    print("saved:", args.output)


if __name__ == "__main__":
    main()
