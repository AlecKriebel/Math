#!/usr/bin/env python3
"""Discovery scan for asymmetric greatest-family activity at order ten.

This deliberately reuses the already hostile-audited clean-room colored
configuration implementation from C-138, after resetting only its finite
order constants.  The order-ten stream is partitioned by nauty ``geng`` so
that every job is short, deterministic, and independently resumable.

The output is discovery evidence only.  It is not a coverage certificate
until every partition and the generator split are independently audited.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import subprocess
import sys
import time


ORDER = 10


def load_clean_checker(campaign: Path):
    source = (
        campaign
        / "reviews"
        / "greatest_family_reciprocity_rank_hostile"
        / "independent_checker.py"
    )
    spec = importlib.util.spec_from_file_location("c138_clean_checker", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load accepted C-138 checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ORDER = ORDER
    module.VERTICES = frozenset(range(ORDER))
    module.PAIRS = tuple(itertools.combinations(range(ORDER), 2))
    module.TRIPLES = tuple(itertools.combinations(range(ORDER), 3))
    module.FOURS = tuple(itertools.combinations(range(ORDER), 4))
    return module, source


def active_relation(checker, independent, survivors):
    active: set[tuple[int, int]] = set()
    survivor_set = set(survivors)
    for state in independent:
        occupied = frozenset(state)
        for source in state:
            for target in checker.VERTICES.difference(occupied):
                successor = tuple(
                    sorted(occupied.difference({source}) | {target})
                )
                if successor in survivor_set:
                    active.add((source, target))
    return active


def atomic_json(path: Path, data: dict[str, object]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--residue", type=int, required=True)
    parser.add_argument("--modulus", type=int, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--progress-every", type=int, default=100_000)
    args = parser.parse_args()
    if not 0 <= args.residue < args.modulus:
        raise ValueError("require 0 <= residue < modulus")

    campaign = Path(__file__).resolve().parents[3]
    checker, checker_source = load_clean_checker(campaign)
    geng = campaign / "tools" / "nauty2_9_3" / "geng"
    command = [
        str(geng),
        "-c",
        "-q",
        str(ORDER),
        f"{args.residue}/{args.modulus}",
    ]

    started = time.monotonic()
    stream_hash = hashlib.sha256()
    totals = {
        "records": 0,
        "static_equality_graphs": 0,
        "eternal_equality_graphs": 0,
        "active_orientations": 0,
        "asymmetric_active_orientations": 0,
    }
    first_asymmetry = None

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="ascii",
        bufsize=1,
    )
    if process.stdout is None or process.stderr is None:
        raise RuntimeError("failed to open geng pipes")

    for raw in process.stdout:
        stream_hash.update(raw.encode("ascii"))
        record = raw.strip()
        if not record:
            continue
        totals["records"] += 1
        if (
            args.progress_every > 0
            and totals["records"] % args.progress_every == 0
        ):
            print(
                json.dumps(
                    {
                        "records": totals["records"],
                        "static": totals["static_equality_graphs"],
                        "eternal": totals["eternal_equality_graphs"],
                        "asymmetric": totals[
                            "asymmetric_active_orientations"
                        ],
                        "elapsed_seconds": round(time.monotonic() - started, 2),
                    },
                    sort_keys=True,
                ),
                file=sys.stderr,
                flush=True,
            )
        adjacency = checker.decode_graph6(record)
        independent = checker.equality_static_filter(adjacency)
        if independent is None:
            continue
        totals["static_equality_graphs"] += 1
        survivors, _ranks, _dominating = checker.greatest_triple_kernel(
            adjacency
        )
        if not survivors:
            continue
        totals["eternal_equality_graphs"] += 1
        if not set(independent).issubset(survivors):
            raise AssertionError("maximum independent triple did not survive")

        active = active_relation(checker, independent, survivors)
        totals["active_orientations"] += len(active)
        asymmetric = sorted(
            (source, target)
            for source, target in active
            if (target, source) not in active
        )
        totals["asymmetric_active_orientations"] += len(asymmetric)
        if asymmetric and first_asymmetry is None:
            source, target = asymmetric[0]
            first_asymmetry = {
                "graph6": record,
                "source": source,
                "target": target,
                "greatest_family_size": len(survivors),
                "independent_triples": [list(state) for state in independent],
            }

    stderr = process.stderr.read()
    returncode = process.wait()
    process.stdout.close()
    process.stderr.close()
    if returncode != 0:
        raise RuntimeError(f"geng failed with {returncode}: {stderr}")
    if stderr:
        raise RuntimeError(f"unexpected geng diagnostics: {stderr}")

    result = {
        "schema": "order10-reciprocity-discovery-partition-v1",
        "classification": "OBSERVED_DISCOVERY_ONLY",
        "order": ORDER,
        "partition": {
            "residue": args.residue,
            "modulus": args.modulus,
        },
        "generator": {
            "command": command,
            "sha256": hashlib.sha256(geng.read_bytes()).hexdigest(),
            "stream_sha256": stream_hash.hexdigest(),
        },
        "checker_source": {
            "path": str(checker_source.relative_to(campaign)),
            "sha256": hashlib.sha256(checker_source.read_bytes()).hexdigest(),
        },
        "totals": totals,
        "first_asymmetry": first_asymmetry,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "scope_guardrail": (
            "A zero count is not a certified finite theorem without all "
            "partitions, independent coverage reconstruction, and a "
            "separate implementation. A witness must be independently "
            "replayed before use."
        ),
    }
    atomic_json(args.checkpoint, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
