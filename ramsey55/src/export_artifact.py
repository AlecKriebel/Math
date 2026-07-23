#!/usr/bin/env python3
"""Export a graph6 input as the deterministic canonical JSON artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from graph_io import read_graph, write_canonical_artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--line", type=int, default=1)
    parser.add_argument("--source", default="unspecified")
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()
    provenance = {"source": args.source, "input": str(args.input), "line": args.line}
    if args.seed is not None:
        provenance["seed"] = args.seed
    digest = write_canonical_artifact(
        read_graph(args.input, args.line), args.output, provenance
    )
    print(
        json.dumps(
            {"artifact": str(args.output), "sha256": digest}, sort_keys=True
        )
    )


if __name__ == "__main__":
    main()
