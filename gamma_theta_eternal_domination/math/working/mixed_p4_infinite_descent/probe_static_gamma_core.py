#!/usr/bin/env python3
"""Discovery probe for the exact static mixed-P4 obstruction.

This extends ``free_unit_chain_attack/synth_mixed_path.py`` by requiring
the six negative direct swaps to be *statically* illegal: either the
corresponding guard--target pair is a graph nonedge, or the direct
successor misses an explicitly witnessed vertex.  The base encoder already
requires the six positive direct states and an arbitrary literal eternal
family.

The probe is intentionally a discovery tool.  An UNSAT result is not a
certificate or an all-order theorem.
"""

from __future__ import annotations

import argparse
import importlib.util
from itertools import combinations
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "math/working/free_unit_chain_attack/synth_mixed_path.py"


def load_source():
    spec = importlib.util.spec_from_file_location("mixed_synth", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load mixed-P4 synthesis source")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add_exact_static_negatives(
    cnf,
    edge_h,
    order: int,
    selected: set[tuple[int, int]] | None = None,
) -> None:
    reference = (0, 1, 2)
    exact_lists = {
        3: frozenset((0,)),
        4: frozenset((0, 2)),
        5: frozenset((1, 2)),
        6: frozenset((1,)),
    }

    def edge(first: int, second: int) -> int:
        return edge_h[(first, second) if first < second else (second, first)]

    for target, positive in exact_lists.items():
        for omitted in reference:
            if omitted in positive:
                continue
            if selected is not None and (target, omitted) not in selected:
                continue
            successor = (set(reference) - {omitted}) | {target}
            missed_candidates = tuple(
                vertex for vertex in range(order) if vertex not in successor
            )
            missed_markers = []
            for missed in missed_candidates:
                marker = cnf.var(
                    f"static_missed({target},{omitted};{missed})"
                )
                missed_markers.append(marker)
                for guard in sorted(successor):
                    cnf.add(-marker, edge(missed, guard))

            # H(omitted,target) makes the move unavailable.  Otherwise at
            # least one marker witnesses failure of domination.
            cnf.add(edge(omitted, target), *missed_markers)


def selected_gamma_pairs(order: int, mode: str) -> set[tuple[int, int]]:
    vertices = range(order)
    if mode == "none":
        return set()
    if mode == "all":
        return set(combinations(vertices, 2))
    if mode == "core":
        return {
            pair
            for pair in combinations(vertices, 2)
            if pair[0] < 7 and pair[1] < 7
        }
    if mode == "core-incident":
        return {
            pair
            for pair in combinations(vertices, 2)
            if pair[0] < 7 or pair[1] < 7
        }
    if mode == "two-anchor":
        return {
            pair
            for pair in combinations(vertices, 2)
            if pair[0] in (0, 1) or pair[1] in (0, 1)
        }
    raise ValueError(f"unknown gamma mode {mode!r}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument(
        "--gamma",
        choices=("none", "core", "core-incident", "two-anchor", "all"),
        default="all",
    )
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--instance", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument(
        "--static-negatives",
        help=(
            "comma-separated target:omitted pairs; default is all six, "
            "and an empty string selects none"
        ),
    )
    args = parser.parse_args()

    source = load_source()
    pairs = selected_gamma_pairs(args.order, args.gamma)
    cnf, edge_h, family = source.build(
        args.order,
        enforce_gamma=bool(pairs),
        gamma_pairs=pairs,
    )
    selected_negatives = None
    if args.static_negatives is not None:
        selected_negatives = set()
        for item in args.static_negatives.split(","):
            if not item:
                continue
            target_text, omitted_text = item.split(":", 1)
            selected_negatives.add((int(target_text), int(omitted_text)))
    add_exact_static_negatives(
        cnf,
        edge_h,
        args.order,
        selected_negatives,
    )
    args.instance.write_text(cnf.dimacs(), encoding="ascii")

    command = [
        str(args.solver),
        "--quiet",
        "--binary=false",
        "-w",
        str(args.model),
        str(args.instance),
    ]
    if args.proof is not None:
        command.append(str(args.proof))
    try:
        run = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=args.timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        print(
            f"order={args.order} gamma={args.gamma} "
            f"variables={len(cnf.names)-1} clauses={len(cnf.clauses)} "
            "status=TIMEOUT"
        )
        raise SystemExit(124)

    if run.returncode == 10:
        status = "SAT"
    elif run.returncode == 20:
        status = "UNSAT"
    else:
        status = f"EXIT_{run.returncode}"
    print(
        f"order={args.order} gamma={args.gamma} "
        f"gamma_pairs={len(pairs)} variables={len(cnf.names)-1} "
        f"static_negatives="
        f"{6 if selected_negatives is None else len(selected_negatives)} "
        f"clauses={len(cnf.clauses)} status={status}"
    )
    raise SystemExit(
        10 if status == "SAT" else 20 if status == "UNSAT" else 1
    )


if __name__ == "__main__":
    main()
