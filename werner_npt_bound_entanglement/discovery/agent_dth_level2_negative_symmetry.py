#!/usr/bin/env python3
"""Site-symmetric solve for the enlarged negative-sector DTH extension.

The 17 ordered targets comprise the 444, 333, 433, 141, 331, and 321 site
orbits.  Exact site symmetry reduces their 1,199 real-symmetric marginal
equations to 222.  Floating point is used for discovery only.
"""

from pathlib import Path
import pickle
import sys


ROOT = Path(__file__).resolve().parents[1]
DISCOVERY = ROOT / "discovery"
sys.path.insert(0, str(DISCOVERY))

import agent_dth_level2_joint_extension as JOINT
import agent_dth_level2_joint_symmetry as SYMMETRY
import agent_dth_level2_negative_extension as NEGATIVE


CACHE = DISCOVERY / "dth_level2_negative_blocks.pkl"


def load_or_build():
    if CACHE.exists():
        with CACHE.open("rb") as handle:
            return pickle.load(handle)
    return NEGATIVE.build()


def main():
    data = load_or_build()
    JOINT.TARGETS = tuple(data["targets"])
    target_data = data["target_data"]
    blocks = data["blocks"]
    directions = SYMMETRY.invariant_target_basis(target_data)
    assert len(directions) == 222
    target = SYMMETRY.invariant_projection(target_data, directions)
    original_norm = sum(
        SYMMETRY.la.norm(target_data[key][1]) ** 2 for key in JOINT.TARGETS
    ) ** 0.5
    average_change = sum(
        SYMMETRY.la.norm(target[key] - target_data[key][1]) ** 2
        for key in JOINT.TARGETS
    ) ** 0.5
    print("site-average relative change:", average_change / original_norm)
    superoperator = SYMMETRY.reduced_superoperator(
        blocks, target_data, directions
    )
    SYMMETRY.minimum_norm_preimage(
        blocks, target_data, directions, target, superoperator
    )
    SYMMETRY.reduced_dr(
        blocks, target_data, directions, target, superoperator,
        floor=0.0, iterations=10000, tolerance=1e-18,
    )
    SYMMETRY.reduced_dr(
        blocks, target_data, directions, target, superoperator,
        floor=1e-12, iterations=10000, tolerance=1e-18,
    )


if __name__ == "__main__":
    main()
