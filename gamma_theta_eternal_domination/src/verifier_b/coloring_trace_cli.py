"""Command line interface for exhaustive complement-coloring traces."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys

from .coloring_trace_checker import (
    TraceVerificationError,
    check_uncolorability_trace,
)
from .coloring_trace_generator import (
    ColorableGraphError,
    write_uncolorability_trace,
)
from .graph import Graph


def main() -> None:
    parser = argparse.ArgumentParser(
        description="generate or independently replay theta(G)>k certificates"
    )
    commands = parser.add_subparsers(dest="command", required=True)

    generate = commands.add_parser(
        "generate",
        help="write a full proof that the complement is not k-colorable",
    )
    generate.add_argument("graph6", help="canonical graph6 record for G")
    generate.add_argument("k", type=int, help="number of complement colors")
    generate.add_argument("output", type=Path, help="output trace path")
    generate.add_argument(
        "--overwrite",
        action="store_true",
        help="replace an existing output atomically",
    )

    verify = commands.add_parser(
        "verify", help="replay every branch in a saved trace"
    )
    verify.add_argument("certificate", type=Path)
    verify.add_argument(
        "--graph6",
        help="optionally require this externally supplied graph6 record",
    )
    verify.add_argument(
        "--k",
        type=int,
        help="optionally require this externally supplied color count",
    )

    arguments = parser.parse_args()
    if arguments.command == "generate":
        try:
            graph = Graph.from_graph6(arguments.graph6)
            if graph.to_graph6() != arguments.graph6:
                raise ValueError("input must use canonical graph6 syntax")
            summary = write_uncolorability_trace(
                graph,
                arguments.k,
                arguments.output,
                overwrite=arguments.overwrite,
            )
        except (ColorableGraphError, FileExistsError, OSError, TypeError, ValueError) as error:
            print(json.dumps({"ok": False, "error": str(error)}), file=sys.stderr)
            raise SystemExit(2)
        output = asdict(summary)
        output["output_path"] = str(summary.output_path)
        output["ok"] = True
        print(json.dumps(output, indent=2, sort_keys=True))
        return

    expected_graph = None
    try:
        if arguments.graph6 is not None:
            expected_graph = Graph.from_graph6(arguments.graph6)
            if expected_graph.to_graph6() != arguments.graph6:
                raise ValueError(
                    "expected graph must use canonical graph6 syntax"
                )
        check = check_uncolorability_trace(
            arguments.certificate,
            expected_graph=expected_graph,
            expected_k=arguments.k,
        )
    except (TraceVerificationError, OSError, TypeError, ValueError) as error:
        print(json.dumps({"ok": False, "error": str(error)}), file=sys.stderr)
        raise SystemExit(1)
    output = asdict(check)
    output["ok"] = True
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
