#!/usr/bin/env python3
"""Exact support bounds reducing arbitrary strong theta port chains to size six."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

from enumerate_theta_orientation_cores import enumerate_cores, minimal_strong_repairs


HERE = Path(__file__).resolve().parent.parent
CERTIFICATE = HERE / "certificates" / "theta_support_reduction.json"
CORE_NAMES = (
    "theta-TT-nested",
    "theta-TT-separated",
    "theta-TR-nested",
    "theta-TR-separated",
)


def generate_certificate():
    raw_valid, cores = enumerate_cores()
    assert raw_valid == 24
    assert len(cores) == 4
    records = []
    for core_index, (name, core) in enumerate(zip(CORE_NAMES, cores)):
        vertices = core["vertex_types"]
        edges = core["directed_segments"]
        repairs = minimal_strong_repairs(vertices, edges)
        assert repairs
        assert len({len(repair) for repair in repairs}) == 1
        repair_size = len(repairs[0])
        sink_count = sum(color == "X" for color in vertices.values())
        support_size = sink_count + repair_size
        assert support_size in {3, 4}

        strong_occupancies = []
        for mask in range(1 << len(edges)):
            occupied = frozenset(
                index for index in range(len(edges)) if mask & (1 << index)
            )
            contained_repairs = [
                repair for repair in repairs if set(repair) <= occupied
            ]
            if not contained_repairs:
                continue
            chosen = min(contained_repairs)
            assert len(chosen) == repair_size
            strong_occupancies.append(
                {
                    "occupied_segments": sorted(occupied),
                    "canonical_support_repair_segments": list(chosen),
                }
            )

        # The tree-child conditions are monotone in occupied segments and
        # minimal_strong_repairs enumerates every minimal satisfying set.
        assert len(strong_occupancies) == sum(
            any(set(repair) <= {
                index for index in range(len(edges)) if mask & (1 << index)
            } for repair in repairs)
            for mask in range(1 << len(edges))
        )

        records.append(
            {
                "core_index": core_index,
                "core_name": name,
                "segment_count": len(edges),
                "path_sink_port_count": sink_count,
                "minimal_repair_size": repair_size,
                "core_preserving_strong_support_size": support_size,
                "support_plus_one_port_bound": support_size + 1,
                "support_plus_two_ports_bound": support_size + 2,
                "minimal_repair_segment_sets": [list(repair) for repair in repairs],
                "strong_occupied_segment_patterns": len(strong_occupancies),
                "strong_occupancy_certificates": strong_occupancies,
            }
        )

    support_distribution = Counter(
        record["core_preserving_strong_support_size"] for record in records
    )
    assert support_distribution == {3: 3, 4: 1}
    assert max(record["support_plus_two_ports_bound"] for record in records) == 6
    return {
        "status": {
            "core_preserving_support_bound": "PROVED",
            "ordered_port_chain_deck_bound": "PROVED",
            "uniform_outgoing_port_witness_bound": 6,
        },
        "theta_orientation_cores": len(records),
        "support_size_distribution": dict(sorted(support_distribution.items())),
        "maximum_core_preserving_strong_support_size": 4,
        "maximum_support_plus_one_port_size": 5,
        "maximum_support_plus_two_ports_size": 6,
        "cores": records,
        "reconstruction_data": (
            "a support-plus-one restriction gives the directed segment of "
            "each extra port; support-plus-two restrictions give every "
            "pairwise order on a common segment, hence every full ordered chain"
        ),
        "remaining_statistical_task": (
            "classify the finite JC atlas of support-augmented restrictions "
            "with at most six outgoing ports"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()
    certificate = json.loads(json.dumps(generate_certificate(), sort_keys=True))
    if args.write_certificate:
        CERTIFICATE.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    else:
        assert certificate == json.loads(CERTIFICATE.read_text())
    print(
        json.dumps(
            {
                "theta_orientation_cores": certificate["theta_orientation_cores"],
                "maximum_core_preserving_strong_support_size": certificate[
                    "maximum_core_preserving_strong_support_size"
                ],
                "maximum_support_plus_two_ports_size": certificate[
                    "maximum_support_plus_two_ports_size"
                ],
                "status": certificate["status"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
