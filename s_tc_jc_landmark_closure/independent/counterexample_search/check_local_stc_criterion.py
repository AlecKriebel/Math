#!/usr/bin/env python3
"""Compare the locked local S_TC criterion with exhaustive rootings."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from clean_graph import class_membership
from enumerate_census import internal_cores, mixed_graphs


def local_criterion(graph):
    arrows = graph.arrow_map()
    neighbors = graph.neighbors()
    for (u, v), heads in arrows.items():
        if len(heads) != 1:
            continue
        head = next(iter(heads))
        tail = v if head == u else u
        ordinary = sum(
            len(arrows[tuple(sorted((tail, other)))]) == 0
            for other in neighbors[tail]
        )
        if ordinary != 2:
            return False
    return True


def main():
    cells = []
    mismatches = []
    for n in range(3, 5):
        for r in range(3):
            rootable = 0
            for graph in mixed_graphs(n, r, internal_cores(n, r)):
                membership, roots = class_membership(graph)
                if not roots:
                    continue
                rootable += 1
                expected = membership == "S_TC"
                observed = local_criterion(graph)
                if expected != observed:
                    mismatches.append(
                        {
                            "n": n,
                            "reticulations": r,
                            "membership": membership,
                            "rooting_count": len(roots),
                        }
                    )
            cells.append({"n": n, "reticulations": r, "rootable_graphs": rootable})
    assert not mismatches, mismatches
    payload = {
        "schema": 1,
        "status": "EXACTLY_COMPUTED_BOUNDED_REGRESSION",
        "cells": cells,
        "mismatches": mismatches,
        "conclusion": "The locked tail-incidence S_TC criterion agrees with exhaustive admissible-rooting enumeration for every rootable graph with three or four leaves and at most two reticulations.",
    }
    out = Path("local_stc_criterion_certificate.json")
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("PASS", hashlib.sha256(out.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()

