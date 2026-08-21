#!/usr/bin/env python3
"""Independent extension of the archived two-colour switching census.

The archived bridge/cut verifier tests a short per-segment word palette. This
audit enumerates every binary segment word whose total number of active ports,
including the structural sink/incoming ports, is at most eight. It reuses the
archive's graph validity and displayed-switching predicates, but not its word
universe, and records whether any valid strong noncut colouring is displayed
by every switching.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parents[1]
VERIFIER = (
    HERE
    / "work/extracted/stc_jc_sharp_boundary_atlas_certificates_v1.1.5"
    / "independent/bridge_cut/verify_cut.py"
)


def load_verifier():
    spec = importlib.util.spec_from_file_location("archived_verify_cut", VERIFIER)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def compositions(total: int, length: int, prefix=()):
    if length == 1:
        yield prefix + (total,)
        return
    for first in range(total + 1):
        yield from compositions(total - first, length - 1, prefix + (first,))


def palette_keys(vc, core, nonroot):
    """Configurations directly reached by the archived palette/duplication."""
    extra_count = len(core.sinks) + int(nonroot)
    result = set()
    for words in itertools.product(vc.COMPRESSED_WORDS, repeat=len(core.arcs)):
        for extras in itertools.product((0, 1), repeat=extra_count):
            result.add((tuple(words), tuple(extras)))
            expanded = vc.duplicate_singleton_colors(words, extras)
            if expanded is not None:
                result.add((tuple(expanded), tuple(extras)))
    return result


def main():
    vc = load_verifier()
    families = []
    total = {
        "enumerated_balanced": 0,
        "valid_standard_strong": 0,
        "covered_by_archived_palette": 0,
        "omitted_by_archived_palette": 0,
        "all_switching_survivors": 0,
        "omitted_all_switching_survivors": 0,
    }
    survivor_records = []

    for nonroot in (False, True):
        for core in vc.CORES:
            structural_count = len(core.sinks) + int(nonroot)
            covered = palette_keys(vc, core, nonroot)
            row = {
                "core": core.name,
                "role": "nonroot" if nonroot else "root",
                "enumerated_balanced": 0,
                "valid_standard_strong": 0,
                "covered_by_archived_palette": 0,
                "omitted_by_archived_palette": 0,
                "all_switching_survivors": 0,
                "omitted_all_switching_survivors": 0,
            }

            minimum_segment_ports = max(0, 4 - structural_count)
            maximum_segment_ports = 8 - structural_count
            for segment_port_count in range(
                minimum_segment_ports, maximum_segment_ports + 1
            ):
                for lengths in compositions(segment_port_count, len(core.arcs)):
                    for flat_word in itertools.product(
                        (0, 1), repeat=segment_port_count
                    ):
                        words = []
                        cursor = 0
                        for length in lengths:
                            words.append(tuple(flat_word[cursor : cursor + length]))
                            cursor += length
                        words = tuple(words)
                        for extras in itertools.product(
                            (0, 1), repeat=structural_count
                        ):
                            colors = flat_word + extras
                            if min(colors.count(0), colors.count(1)) < 2:
                                continue
                            row["enumerated_balanced"] += 1
                            network, actual_colors = vc.build_colored_network(
                                core, words, extras, nonroot
                            )
                            if not (
                                vc.rooted_valid(network)
                                and vc.standard_strong(network)
                            ):
                                continue
                            row["valid_standard_strong"] += 1
                            is_covered = (words, tuple(extras)) in covered
                            coverage_key = (
                                "covered_by_archived_palette"
                                if is_covered
                                else "omitted_by_archived_palette"
                            )
                            row[coverage_key] += 1
                            survivor = vc.displayed_color_split_by_all(
                                network, actual_colors
                            )
                            if survivor:
                                row["all_switching_survivors"] += 1
                                if not is_covered:
                                    row["omitted_all_switching_survivors"] += 1
                                survivor_records.append(
                                    {
                                        "core": core.name,
                                        "role": row["role"],
                                        "words": [list(word) for word in words],
                                        "extras": list(extras),
                                        "covered_by_archived_palette": is_covered,
                                        "arcs": [list(arc) for arc in network.arcs],
                                        "colors": list(actual_colors),
                                    }
                                )

            families.append(row)
            for key in total:
                total[key] += row[key]
            print(json.dumps(row, sort_keys=True), flush=True)

    result = {
        "scope": "all binary segment words with 4..8 active ports",
        "families": families,
        "total": total,
        "survivors": survivor_records,
        "status": "NO SURVIVOR" if not survivor_records else "SURVIVOR FOUND",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
