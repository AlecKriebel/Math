#!/usr/bin/env python3
"""Common level-two extension over the largest negative target sectors.

The target set is the union of

* 444, 333, and every ordered 433 block;
* every ordered 141 block;
* every ordered 331 block; and
* every ordered 321 block.

It is deliberately a *single* extension problem: every output block is fed
by the same collection of PSD S7 source moments.  Use ``--build-only`` to
cache the expensive CP maps before applying site-symmetry reduction or a
custom solver.
"""

import argparse
from itertools import permutations
from pathlib import Path
import pickle
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))

import agent_dth_level2_joint_extension as ENGINE


def negative_targets():
    targets = set(ENGINE.CORE_TARGETS)
    for seed in ((1, 4, 1), (3, 3, 1), (3, 2, 1)):
        targets.update(permutations(seed))
    return tuple(sorted(targets))


def build():
    ENGINE.TARGETS = negative_targets()
    target_data = {target: ENGINE.load_target(target) for target in ENGINE.TARGETS}
    sources = ENGINE.candidate_sources(target_data)
    print("ordered targets:", len(ENGINE.TARGETS))
    print("target symmetric equations:", sum(
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
                f"rank={block['dimension']}"
            )
    print("total marginal-relevant PSD rank:", sum(
        block["dimension"] for block in blocks
    ))
    print("total marginal-relevant symmetric variables:", sum(
        block["dimension"] * (block["dimension"] + 1) // 2
        for block in blocks
    ))
    return {
        "targets": ENGINE.TARGETS,
        "target_data": target_data,
        "sources": sources,
        "blocks": blocks,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cache",
        type=Path,
        default=ROOT / "discovery/dth_level2_negative_blocks.pkl",
    )
    parser.add_argument("--build-only", action="store_true")
    args = parser.parse_args()

    payload = build()
    with args.cache.open("wb") as stream:
        pickle.dump(payload, stream, pickle.HIGHEST_PROTOCOL)
    print("cache:", args.cache)
    if args.build_only:
        return

    ENGINE.TARGETS = payload["targets"]
    best, spectrum = ENGINE.solve(
        payload["blocks"], payload["target_data"], iterations=3000
    )
    print("best score/residual/PSD defect/min:", best[:4])


if __name__ == "__main__":
    main()
