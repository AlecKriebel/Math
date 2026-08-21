#!/usr/bin/env python3
"""Standalone verification of the two-colour segment-word reduction.

This program deliberately imports no graph, switching, or certificate code.
It exhausts every binary word distribution with four through eight active
ports for the five primitive core arities and both root roles.  Each balanced
distribution is certified to have one of two forms:

* some segment contains at least three monochromatic runs, which is the
  direct path-order obstruction proved in ``CUT_PALETTE_REDUCTION.md``; or
* collapsing every run to one representative gives the short palette used by
  ``verify_cut.py``, possibly followed by the one permitted adjacent duplicate
  when a colour would otherwise have only one representative.

Thus this file verifies the combinatorial exhaustiveness of the reduction;
``verify_cut.py`` independently verifies that the resulting finite palette
has no all-switching survivor.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path


PALETTE = ((), (0,), (1,), (0, 1), (1, 0))
FAMILIES = (
    ("cycle", 2, 1),
    ("theta_TR_nested", 5, 1),
    ("theta_TR_separated", 5, 1),
    ("theta_TT_nested", 6, 2),
    ("theta_TT_separated", 6, 2),
)


def compositions(total: int, bins: int):
    if bins == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, bins - 1):
            yield (first, *rest)


def runs(word):
    answer = []
    for colour in word:
        if not answer or answer[-1][0] != colour:
            answer.append([colour, 1])
        else:
            answer[-1][1] += 1
    return tuple((colour, length) for colour, length in answer)


def palette_target(words, extras):
    """Return the exact short-palette target or the direct obstruction tag."""

    run_rows = tuple(runs(word) for word in words)
    if any(len(row) >= 3 for row in run_rows):
        return "three_run_path_obstruction", None

    reduced = tuple(tuple(colour for colour, _length in row) for row in run_rows)
    if not all(word in PALETTE for word in reduced):
        raise AssertionError("two-run word escaped the short palette")
    if tuple(bool(word) for word in reduced) != tuple(bool(word) for word in words):
        raise AssertionError("segment occupancy changed")

    counts = Counter(colour for word in reduced for colour in word)
    counts.update(extras)
    if min(counts[0], counts[1]) >= 2:
        return "direct_palette", reduced

    singleton_colours = tuple(colour for colour in (0, 1) if counts[colour] == 1)
    if len(singleton_colours) != 1:
        raise AssertionError("balanced input has an invalid reduced colour count")
    colour = singleton_colours[0]
    locations = [
        (segment, position)
        for segment, word in enumerate(reduced)
        for position, value in enumerate(word)
        if value == colour
    ]
    if len(locations) != 1 or colour in extras:
        raise AssertionError("the sole representative is not a segment run")
    segment, position = locations[0]
    matching_run = run_rows[segment][position]
    if matching_run[0] != colour or matching_run[1] < 2:
        raise AssertionError("singleton reduction lacks a second actual label")
    doubled = [list(word) for word in reduced]
    doubled[segment].insert(position, colour)
    doubled = tuple(tuple(word) for word in doubled)
    doubled_counts = Counter(value for word in doubled for value in word)
    doubled_counts.update(extras)
    if min(doubled_counts[0], doubled_counts[1]) < 2:
        raise AssertionError("adjacent duplication did not preserve balance")
    return "singleton_doubled_palette", doubled


def enumerate_family(segment_count: int, extra_count: int):
    for active_count in range(4, 9):
        segment_letters = active_count - extra_count
        if segment_letters < 0:
            continue
        for lengths in compositions(segment_letters, segment_count):
            for letters in itertools.product((0, 1), repeat=segment_letters):
                words = []
                offset = 0
                for length in lengths:
                    words.append(tuple(letters[offset : offset + length]))
                    offset += length
                for extras in itertools.product((0, 1), repeat=extra_count):
                    colours = (*letters, *extras)
                    counts = Counter(colours)
                    if min(counts[0], counts[1]) >= 2:
                        yield active_count, tuple(words), tuple(extras)


def audit():
    totals = Counter()
    by_family = []
    commitment = hashlib.sha256()
    failures = []
    for family, segment_count, sink_count in FAMILIES:
        for nonroot in (False, True):
            extra_count = sink_count + int(nonroot)
            local = Counter()
            by_size = defaultdict(Counter)
            for active_count, words, extras in enumerate_family(segment_count, extra_count):
                try:
                    disposition, target = palette_target(words, extras)
                except AssertionError as error:
                    failures.append({
                        "family": family,
                        "role": "nonroot" if nonroot else "root",
                        "active_count": active_count,
                        "words": words,
                        "extras": extras,
                        "error": str(error),
                    })
                    continue
                local[disposition] += 1
                by_size[active_count][disposition] += 1
                commitment.update(json.dumps(
                    [family, nonroot, active_count, words, extras, disposition, target],
                    separators=(",", ":"),
                ).encode())
            local["balanced_total"] = sum(
                value for key, value in local.items() if key != "balanced_total"
            )
            totals.update(local)
            by_family.append({
                "family": family,
                "role": "nonroot" if nonroot else "root",
                "segment_count": segment_count,
                "fixed_extra_count": extra_count,
                "counts": dict(sorted(local.items())),
                "by_active_port_count": {
                    str(size): dict(sorted(row.items()))
                    for size, row in sorted(by_size.items())
                },
            })

    mutation_results = []
    disposition, target = palette_target(((1, 0, 1), (0,)), (0,))
    mutation_results.append({
        "mutation": "historical_101_word_must_not_enter_palette",
        "rejected": disposition == "three_run_path_obstruction" and target is None,
    })
    disposition, target = palette_target(((0, 0), (1,)), (1,))
    mutation_results.append({
        "mutation": "removing_singleton_duplication_loses_balance",
        "rejected": disposition == "singleton_doubled_palette" and target == ((0, 0), (1,)),
    })
    disposition, target = palette_target(((1, 0),), (0, 1))
    mutation_results.append({
        "mutation": "sorting_run_order_changes_the_word",
        "rejected": disposition == "direct_palette" and target == ((1, 0),),
    })
    if not all(row["rejected"] for row in mutation_results):
        failures.append({"mutation_failures": mutation_results})

    return {
        "schema": "stc-jc-cut-palette-reduction-v1",
        "status": "EXACTLY COMPUTED" if not failures else "FALSE",
        "scope": {
            "active_port_counts": [4, 5, 6, 7, 8],
            "primitive_families": [row[0] for row in FAMILIES],
            "roles": ["root", "nonroot"],
            "short_palette": [list(word) for word in PALETTE],
        },
        "proof_partition": (
            "Every balanced word either has a three-run path obstruction or "
            "reduces, with unchanged occupied segments and fixed extras, to "
            "the direct or singleton-doubled short palette."
        ),
        "totals": dict(sorted(totals.items())),
        "families": by_family,
        "enumeration_commitment_sha256": commitment.hexdigest(),
        "mutation_results": mutation_results,
        "failure_count": len(failures),
        "failures": failures[:10],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    args.output.write_text(raw, encoding="utf-8")
    print(json.dumps({
        "status": payload["status"],
        "balanced_configurations": payload["totals"].get("balanced_total", 0),
        "three_run_obstructions": payload["totals"].get("three_run_path_obstruction", 0),
        "palette_reductions": (
            payload["totals"].get("direct_palette", 0)
            + payload["totals"].get("singleton_doubled_palette", 0)
        ),
        "failure_count": payload["failure_count"],
        "sha256": hashlib.sha256(raw.encode()).hexdigest(),
    }, indent=2, sort_keys=True))
    return 0 if payload["status"] == "EXACTLY COMPUTED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
