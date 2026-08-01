#!/usr/bin/env python3
"""Build the complete five-to-seven DTH fixed-marginal CP map.

All nonzero five-replica holomorphic support blocks are imposed on one shared
degree-three Grassmann source.  The raw, unaveraged target has 4139 symmetric
coordinates; downstream solvers should exploit physical-site averaging before
forming the affine normal operator.
"""

from itertools import product
from pathlib import Path
import argparse
import pickle
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))

import agent_dth_level2_joint_extension as ENGINE


def build():
    all_targets = tuple(product(range(5), repeat=3))
    preliminary = {target: ENGINE.load_target(target) for target in all_targets}
    targets = tuple(
        target for target in all_targets if preliminary[target][1].shape[0] > 0
    )
    ENGINE.TARGETS = targets
    target_data = {target: preliminary[target] for target in targets}
    sources = ENGINE.candidate_sources(target_data)
    print("active ordered targets:", len(targets))
    print("raw target symmetric equations:", sum(
        moment.shape[0] * (moment.shape[0] + 1) // 2
        for qout, moment in target_data.values()
    ))
    print("candidate source blocks:", len(sources))
    blocks = []
    for index, source in enumerate(sources, 1):
        block = ENGINE.construct_source_block(source, target_data)
        blocks.append(block)
        if index % 10 == 0 or index == len(sources):
            print(
                f"built {index}/{len(sources)}; latest={source}; "
                f"rank={block['dimension']}; targets={len(block['maps'])}"
            )
    print("total marginal-relevant PSD rank:", sum(
        block["dimension"] for block in blocks
    ))
    print("total marginal-relevant symmetric variables:", sum(
        block["dimension"] * (block["dimension"] + 1) // 2
        for block in blocks
    ))
    return {
        "targets": targets,
        "target_data": target_data,
        "sources": sources,
        "blocks": blocks,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cache",
        type=Path,
        default=ROOT / "discovery/dth_level2_full_blocks.pkl",
    )
    args = parser.parse_args()
    payload = build()
    with args.cache.open("wb") as stream:
        pickle.dump(payload, stream, pickle.HIGHEST_PROTOCOL)
    print("cache:", args.cache)


if __name__ == "__main__":
    main()
