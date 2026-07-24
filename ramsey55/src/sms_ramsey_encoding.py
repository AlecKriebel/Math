#!/usr/bin/env python3
"""Build an SMS-compatible Ramsey CNF through the official PySMS interface.

The PySMS checkout is supplied explicitly.  This keeps the third-party tool
isolated while preserving the edge-variable numbering required by ``smsg``.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import itertools
import json
import math
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path


GENERATOR_ID = "ramsey_sms_pysms_graph_builder_v1"
COUNTER = "sequential"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge_variable(order: int, left: int, right: int) -> int:
    """SMS/PySMS upper-triangle row-major edge-variable numbering."""
    if left > right:
        left, right = right, left
    if not 0 <= left < right < order:
        raise ValueError(f"invalid edge ({left},{right}) for order {order}")
    return 1 + left * (2 * order - left - 1) // 2 + right - left - 1


def git_value(root: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root), *arguments],
        text=True,
        capture_output=True,
        check=False,
    )
    return completed.stdout.strip() if completed.returncode == 0 else ""


def load_builder(pysms_root: Path):
    root = str(pysms_root.resolve())
    if root not in sys.path:
        sys.path.insert(0, root)
    module = importlib.import_module("pysms.graph_builder")
    return module.GraphEncodingBuilder


def generate(
    *,
    pysms_root: Path,
    output: Path,
    order: int,
    independent_size: int,
    clique_size: int,
    degree_lower: int,
    degree_upper: int,
) -> dict[str, object]:
    if order < 1:
        raise ValueError("order must be positive")
    if not 2 <= independent_size <= order:
        raise ValueError("independent size is outside the graph")
    if not 2 <= clique_size <= order:
        raise ValueError("clique size is outside the graph")
    if not 0 <= degree_lower <= degree_upper < order:
        raise ValueError("invalid degree interval")
    graph_builder_path = pysms_root / "pysms/graph_builder.py"
    counters_path = pysms_root / "pysms/counters.py"
    if not graph_builder_path.is_file() or not counters_path.is_file():
        raise ValueError("PySMS root does not contain the expected sources")

    GraphEncodingBuilder = load_builder(pysms_root)
    builder = GraphEncodingBuilder(order, directed=False, DEBUG=0)
    for left, right in itertools.combinations(range(order), 2):
        observed = builder.var_edge(left, right)
        expected = edge_variable(order, left, right)
        if observed != expected:
            raise RuntimeError(
                f"PySMS edge map mismatch for ({left},{right}): "
                f"{observed} != {expected}"
            )

    started = time.monotonic()
    builder.degreeBounds(
        builder.V,
        degree_lower,
        degree_upper,
        encoding=COUNTER,
    )
    degree_clause_count = len(builder)
    builder.maxIndependentSet(independent_size - 1)
    independent_clause_count = len(builder) - degree_clause_count
    builder.maxClique(clique_size - 1)
    clique_clause_count = (
        len(builder) - degree_clause_count - independent_clause_count
    )
    if independent_clause_count != math.comb(order, independent_size):
        raise RuntimeError("unexpected independent-set clause count")
    if clique_clause_count != math.comb(order, clique_size):
        raise RuntimeError("unexpected clique clause count")

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="ascii",
            prefix=output.name + ".",
            suffix=".tmp",
            dir=output.parent,
            delete=False,
        ) as stream:
            temporary = stream.name
            builder.print_dimacs(stream)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, output)
        temporary = None
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)

    patch = git_value(pysms_root, "diff", "--", "src/useful.h")
    return {
        "schema": "ramsey55.sms_encoding_metadata.v1",
        "generator": GENERATOR_ID,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "order": order,
        "independent_size_forbidden": independent_size,
        "clique_size_forbidden": clique_size,
        "degree_lower": degree_lower,
        "degree_upper": degree_upper,
        "counter_encoding": COUNTER,
        "edge_variable_order": (
            "one-based row-major upper triangle "
            "(0,1),(0,2),...,(1,2),..."
        ),
        "primary_variable_count": math.comb(order, 2),
        "variable_count": builder.nextId - 1,
        "auxiliary_variable_count": builder.nextId - 1 - math.comb(order, 2),
        "degree_clause_count": degree_clause_count,
        "independent_clause_count": independent_clause_count,
        "clique_clause_count": clique_clause_count,
        "clause_count": len(builder),
        "cnf_path": str(output.resolve()),
        "cnf_bytes": output.stat().st_size,
        "cnf_sha256": sha256(output),
        "generation_wall_seconds": time.monotonic() - started,
        "pysms_root": str(pysms_root.resolve()),
        "sms_git_commit": git_value(pysms_root, "rev-parse", "HEAD"),
        "sms_git_commit_date": git_value(
            pysms_root, "log", "-1", "--format=%cI"
        ),
        "cadical_git_commit": git_value(
            pysms_root / "cadical_sms", "rev-parse", "HEAD"
        ),
        "graph_builder_sha256": sha256(graph_builder_path),
        "counters_sha256": sha256(counters_path),
        "local_portability_patch": patch,
        "local_portability_patch_sha256": hashlib.sha256(
            patch.encode("utf-8")
        ).hexdigest(),
        "generator_source_sha256": sha256(Path(__file__)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pysms-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--order", type=int, default=43)
    parser.add_argument("--independent-size", type=int, default=5)
    parser.add_argument("--clique-size", type=int, default=5)
    parser.add_argument("--degree-lower", type=int, default=18)
    parser.add_argument("--degree-upper", type=int, default=24)
    args = parser.parse_args()
    result = generate(
        pysms_root=args.pysms_root,
        output=args.output,
        order=args.order,
        independent_size=args.independent_size,
        clique_size=args.clique_size,
        degree_lower=args.degree_lower,
        degree_upper=args.degree_upper,
    )
    args.metadata.parent.mkdir(parents=True, exist_ok=True)
    args.metadata.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
