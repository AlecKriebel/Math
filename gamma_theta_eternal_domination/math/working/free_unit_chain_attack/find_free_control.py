#!/usr/bin/env python3
"""Discovery scan for a small equality graph with a free singleton pin."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import subprocess


def load_helpers(path: Path):
    spec = importlib.util.spec_from_file_location("fixed_verify", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load verifier helpers")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--geng", required=True, type=Path)
    parser.add_argument("--helpers", required=True, type=Path)
    parser.add_argument("--min-order", type=int, default=6)
    parser.add_argument("--max-order", type=int, default=9)
    parser.add_argument("--min-free-component-size", type=int, default=1)
    parser.add_argument("--require-exact-two-in-component", action="store_true")
    args = parser.parse_args()
    helper = load_helpers(args.helpers)
    for order in range(args.min_order, args.max_order + 1):
        run = subprocess.run(
            [str(args.geng), "-cq", str(order)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        tested = 0
        for raw in run.stdout.splitlines():
            record = raw.decode("ascii")
            n, adjacency = helper.decode_graph6(record)
            tested += 1
            if helper.domination_number(n, adjacency) != 3:
                continue
            if helper.independence_number(n, adjacency) != 3:
                continue
            family, _rounds = helper.greatest_family(n, adjacency, 3)
            if not family:
                continue
            for reference in sorted(family):
                if not helper.independent(reference, adjacency):
                    continue
                lists = helper.response_lists(
                    n, adjacency, family, reference
                )
                if any(len(response) == 3 for response in lists.values()):
                    continue
                if not any(len(response) == 1 for response in lists.values()):
                    continue
                projections = helper.frozen_projections(
                    n, adjacency, reference, lists
                )
                classification = helper.classify_fixed_incidents(
                    n, adjacency, reference, lists, projections
                )
                qualifying = []
                for singleton, frozen, demanded in classification[
                    "free_singletons"
                ]:
                    data = projections[frozen]
                    component_index = data["component"][singleton]
                    members = data["components"][component_index]
                    has_exact_two = any(
                        len(lists.get(vertex, ())) == 2
                        and frozen not in lists[vertex]
                        for vertex in members
                    )
                    if len(members) < args.min_free_component_size:
                        continue
                    if args.require_exact_two_in_component and not has_exact_two:
                        continue
                    qualifying.append(
                        [singleton, frozen, demanded, members]
                    )
                if qualifying:
                    theta = helper.theta_number(n, adjacency)
                    print(
                        f"order={order} tested={tested} graph6={record}"
                        f" reference={helper.vertices(reference)}"
                        f" theta={theta} family={len(family)}"
                        f" lists={lists}"
                        f" free={qualifying}"
                    )
                    return
        print(f"order={order} tested={tested} no_control")
    raise SystemExit("no control found")


if __name__ == "__main__":
    main()
