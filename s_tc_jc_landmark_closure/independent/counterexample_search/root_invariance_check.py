#!/usr/bin/env python3
"""Exact effective-map comparison across every admissible rooting."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from audit_io import load_json
from clean_graph import class_membership
from fourier_engine import effective_unrooted_signature
from screen_models import graph_from_record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--max-n", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = load_json(args.census)
    checked = 0
    rootings = 0
    by_cell = {}
    for record in data["topologies"]:
        if record["membership"] != "S_TC" or record["n"] > args.max_n:
            continue
        graph = graph_from_record(record)
        membership, roots = class_membership(graph)
        assert membership == "S_TC"
        signatures = [effective_unrooted_signature(graph, root) for root in roots]
        assert signatures and all(sig == signatures[0] for sig in signatures)
        checked += 1
        rootings += len(roots)
        key = f"n={record['n']},r={len(record['reticulations'])}"
        cell = by_cell.setdefault(key, {"topologies": 0, "rootings": 0})
        cell["topologies"] += 1
        cell["rootings"] += len(roots)
    payload = {
        "schema": 1,
        "status": "EXACTLY_COMPUTED",
        "topologies_checked": checked,
        "admissible_rootings_checked": rootings,
        "cells": by_cell,
        "conclusion": "Every admissible rooting of every bounded S_TC topology induces the same displayed-tree JC map after replacing the two root arcs by one effective mixed-edge multiplier.",
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("PASS", hashlib.sha256(args.output.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
