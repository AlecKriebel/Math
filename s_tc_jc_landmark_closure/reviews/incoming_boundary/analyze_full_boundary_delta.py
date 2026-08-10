#!/usr/bin/env python3
"""Compute the exact candidate delta between full-S_p and fixed-IN screens."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import defaultdict
from pathlib import Path

import run_cleanroom


HERE = Path(__file__).resolve().parent
CERT = HERE / "certificates" / "verified"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ports", type=int, choices=(4, 5), required=True)
    args = parser.parse_args()
    outgoing = args.ports - 1
    p = args.ports
    module = run_cleanroom.load_cleanroom()
    engine = module.BitEngine(module.invariant_orbit())
    engine.load(CERT / "descriptor_bits.json.gz")
    sources = module.source_models(outgoing, engine)
    source_incoming = defaultdict(set)
    for source in sources:
        for rooted in source["rooted_variants"]:
            source_incoming[source["signature"]].add(int(rooted["incoming_physical"].split("_")[-1]))
    source_signatures = sorted(source_incoming)

    necessary = set()
    fixed_representable = set()
    pair_modes = defaultdict(set)
    pair_presentations = defaultdict(int)
    groups = module.target_descriptor_groups(outgoing)
    permutations = tuple(itertools.permutations(range(p)))
    for structural_descriptor, bases in sorted(groups.items(), key=lambda item: repr(item[0])):
        orbit = defaultdict(list)
        for assignment in permutations:
            orbit[module.permute_descriptor(structural_descriptor, assignment)].append(assignment)
        for moved, assignments in orbit.items():
            target_signature, _deck = module.full_deck_signature(moved, p, engine)
            for source_signature in source_signatures:
                if source_signature & ~target_signature:
                    continue
                pair = (source_signature, target_signature)
                necessary.add(pair)
                pair_presentations[pair] += len(assignments) * len(bases)
                for base in bases:
                    pair_modes[pair].add(base["incoming_mode"])
                    if base["incoming_mode"] != "incoming_selected":
                        continue
                    incoming_position = base["slots"].index(("incoming", 0, 0))
                    if any(
                        assignment[incoming_position] in source_incoming[source_signature]
                        for assignment in assignments
                    ):
                        fixed_representable.add(pair)

    screen = json.loads((CERT / f"screen_n{outgoing}.json").read_text())
    necessary_hash = module.digest(sorted((str(a), str(b)) for a, b in necessary))
    if necessary_hash != screen["necessary_pairs_sha256"]:
        raise AssertionError(("screen/delta necessary-pair mismatch", necessary_hash, screen["necessary_pairs_sha256"]))
    missed = necessary - fixed_representable
    equal = {pair for pair in necessary if pair[0] == pair[1]}
    equal_missed = equal - fixed_representable

    def serial(pair):
        return {
            "source_signature": str(pair[0]),
            "target_signature": str(pair[1]),
            "equal_signature": pair[0] == pair[1],
            "target_incoming_modes": sorted(pair_modes[pair]),
            "raw_presentation_multiplicity": pair_presentations[pair],
        }

    result = {
        "schema": "full-boundary-fixed-IN-candidate-delta-v1",
        "port_count": p,
        "source_signature_count": len(source_signatures),
        "necessary_full_boundary_candidate_pairs": len(necessary),
        "fixed_IN_representable_candidate_pairs": len(fixed_representable),
        "genuinely_missed_by_fixed_IN": len(missed),
        "equal_signature_pairs": len(equal),
        "equal_signature_pairs_missed_by_fixed_IN": len(equal_missed),
        "missed_pairs": [serial(pair) for pair in sorted(missed)],
        "equal_missed_pairs": [serial(pair) for pair in sorted(equal_missed)],
        "necessary_pairs_sha256": necessary_hash,
        "fixed_pairs_sha256": module.digest(sorted((str(a), str(b)) for a, b in fixed_representable)),
        "missed_pairs_sha256": module.digest(sorted((str(a), str(b)) for a, b in missed)),
    }
    result["body_sha256"] = module.digest(result)
    path = CERT / f"full_boundary_delta_p{p}.json"
    path.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
