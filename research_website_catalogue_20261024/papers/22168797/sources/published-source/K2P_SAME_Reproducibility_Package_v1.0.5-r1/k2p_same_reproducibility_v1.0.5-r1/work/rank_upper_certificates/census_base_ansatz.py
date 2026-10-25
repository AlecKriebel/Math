#!/usr/bin/env python3
"""Census the base exact syzygy ansatz over all unique four-port descriptors."""

from __future__ import annotations

import argparse
import json
import pickle
import time
from collections import Counter
from pathlib import Path

from k2p_atlas_core import default_exact_point, output_sparse_polynomials
from syzygy_upper import upper_certificate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--atlas", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    with (args.atlas / "descriptors_4.pkl").open("rb") as handle:
        sources, targets, compatible, source_descriptors, descriptor_map = pickle.load(handle)
    with (args.atlas / "rank_certs_4.pkl").open("rb") as handle:
        lower_certificates = pickle.load(handle)

    unique = sorted(
        set(source_descriptors) | set(descriptor_map.values()),
        key=lambda d: (d.retic_count, d.edge_class_count, d.outputs, d.edge_signatures),
    )
    counts = Counter()
    exceptional = []
    started = time.monotonic()
    for index, descriptor in enumerate(unique, 1):
        upper = upper_certificate(descriptor, output_sparse_polynomials, default_exact_point)
        lower = int(lower_certificates[descriptor]["rank"])
        certified_upper = int(upper["certified_rank_upper"])
        gap = certified_upper - lower
        if gap < 0:
            raise AssertionError((index, lower, certified_upper))
        family = (
            descriptor.retic_count,
            descriptor.edge_class_count,
            lower,
            certified_upper,
        )
        counts[family] += 1
        if gap:
            exceptional.append(
                {
                    "descriptor_index": index - 1,
                    "retic_count": descriptor.retic_count,
                    "edge_class_count": descriptor.edge_class_count,
                    "parameter_count": upper["parameter_count"],
                    "lower_rank": lower,
                    "base_upper_rank": certified_upper,
                    "upper_gap": gap,
                    "coefficient_equation_count": upper["coefficient_equation_count"],
                    "unknown_coefficient_count": upper["unknown_coefficient_count"],
                    "coefficient_system_rank": upper["coefficient_system_rank"],
                    "stacked_system_rank": upper["stacked_system_rank"],
                }
            )
        if index % 250 == 0:
            print(
                f"progress {index}/{len(unique)} exceptional={len(exceptional)} "
                f"elapsed={time.monotonic()-started:.1f}s",
                flush=True,
            )

    result = {
        "schema": "k2p-exact-rank-upper-base-ansatz-census-v1",
        "descriptor_count": len(unique),
        "exact_matches": len(unique) - len(exceptional),
        "exceptional_count": len(exceptional),
        "family_counts": [
            {
                "retic_count": key[0],
                "edge_class_count": key[1],
                "lower_rank": key[2],
                "base_upper_rank": key[3],
                "count": count,
            }
            for key, count in sorted(counts.items())
        ],
        "exceptional": exceptional,
        "elapsed_seconds": time.monotonic() - started,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: result[k] for k in ("descriptor_count", "exact_matches", "exceptional_count", "elapsed_seconds")}, indent=2))


if __name__ == "__main__":
    main()
