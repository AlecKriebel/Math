#!/usr/bin/env python3
"""Site-symmetric solve of the complete PSD fixed-marginal DTH lift.

The complete nonzero five-replica target has 4,139 ordered real-symmetric
coordinates.  Exact physical-site symmetry reduces it to 761.  This script
loads the full degree-three CP-map cache and first tests the minimum-norm
affine preimage.  Douglas--Rachford feasibility is optional because a full
PSD projection sweep over all 487 source blocks is comparatively costly.

Floating point is used only for discovery.  Any obstruction or feasible
point found here must be reconstructed exactly before being claimed.
"""

from argparse import ArgumentParser
from pathlib import Path
import pickle
import sys


ROOT = Path(__file__).resolve().parents[1]
DISCOVERY = ROOT / "discovery"
sys.path.insert(0, str(DISCOVERY))

import agent_dth_level2_joint_extension as JOINT
import agent_dth_level2_joint_symmetry as SYMMETRY


DEFAULT_CACHE = DISCOVERY / "dth_level2_full_blocks.pkl"
DEFAULT_NORMAL_CACHE = DISCOVERY / "dth_level2_full_symmetric_normal.npz"
DEFAULT_CANDIDATE_CACHE = DISCOVERY / "dth_level2_full_symmetric_best.pkl"


def main():
    parser = ArgumentParser()
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument(
        "--normal-cache", type=Path, default=DEFAULT_NORMAL_CACHE
    )
    parser.add_argument("--dr", action="store_true")
    parser.add_argument("--iterations", type=int, default=10000)
    parser.add_argument("--floor", type=float, default=0.0)
    parser.add_argument(
        "--candidate-cache", type=Path, default=DEFAULT_CANDIDATE_CACHE
    )
    args = parser.parse_args()

    if not args.cache.exists():
        raise SystemExit(
            f"missing full CP-map cache {args.cache}; run the full builder first"
        )
    with args.cache.open("rb") as handle:
        data = pickle.load(handle)

    JOINT.TARGETS = tuple(data["targets"])
    target_data = data["target_data"]
    blocks = data["blocks"]
    print("active targets/source blocks:", len(target_data), len(blocks))
    print("source relevant rank:", sum(block["dimension"] for block in blocks))

    directions = SYMMETRY.invariant_target_basis(target_data)
    assert len(directions) == 761
    target = SYMMETRY.invariant_projection(target_data, directions)
    original_norm = sum(
        SYMMETRY.la.norm(target_data[key][1]) ** 2 for key in JOINT.TARGETS
    ) ** 0.5
    average_change = sum(
        SYMMETRY.la.norm(target[key] - target_data[key][1]) ** 2
        for key in JOINT.TARGETS
    ) ** 0.5
    print("site-average relative change:", average_change / original_norm)

    if args.normal_cache.exists():
        superoperator = SYMMETRY.np.load(args.normal_cache)["normal"]
        assert superoperator.shape == (761, 761)
        print("loaded reduced AA* cache:", args.normal_cache)
    else:
        superoperator = SYMMETRY.reduced_superoperator(
            blocks, target_data, directions
        )
        SYMMETRY.np.savez_compressed(
            args.normal_cache, normal=superoperator
        )
        print("saved reduced AA* cache:", args.normal_cache)
    SYMMETRY.minimum_norm_preimage(
        blocks, target_data, directions, target, superoperator
    )
    if args.dr:
        best = SYMMETRY.reduced_dr(
            blocks, target_data, directions, target, superoperator,
            floor=args.floor, iterations=args.iterations, tolerance=1e-18,
        )
        with args.candidate_cache.open("wb") as handle:
            pickle.dump({
                "targets": JOINT.TARGETS,
                "floor": args.floor,
                "score": best[0],
                "residual": best[1],
                "psd_defect": best[2],
                "minimum_shifted_eigenvalue": best[3],
                "shifted_candidate": best[4],
            }, handle, pickle.HIGHEST_PROTOCOL)
        print("saved full symmetric DR candidate:", args.candidate_cache)


if __name__ == "__main__":
    main()
