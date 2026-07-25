#!/usr/bin/env python3
"""Post-search comparison with round-5/6 basins.

This program is deliberately separate from ``compress_d6.py``.  Prior
five-dimensional coordinates are not read until every compression path has
already terminated and been written.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


STATUS = "NUMERICAL EVIDENCE ONLY — POST-SEARCH COMPARISON"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def descriptor(coordinates):
    x = np.asarray(coordinates, dtype=float)
    x /= np.linalg.norm(x, axis=1)[:, None]
    ii, jj = np.triu_indices(len(x), 1)
    return np.sort(np.sum(x[ii] * x[jj], axis=1))


def load_round5(path: Path):
    payload = json.loads(path.read_text())
    answer = []
    for index, run in enumerate(payload["runs"]):
        best = run["best"]
        answer.append(
            {
                "n": run["n"],
                "label": f"round5:{path.name}:run{index}:seed={run['seed']}",
                "maximum": best["maximum"],
                "coordinates": best["coordinates_float64"],
            }
        )
    return answer


def load_round6(path: Path):
    payload = json.loads(path.read_text())
    answer = []
    for index, run in enumerate(payload["runs"]):
        best = run["best"]
        answer.append(
            {
                "n": run["n"],
                "label": f"round6:{path.name}:run{index}:seed={run['seed']}",
                "maximum": best["maximum"],
                "coordinates": best["coordinates_float64"],
            }
        )
    return answer


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--round7", type=Path, required=True)
    parser.add_argument("--round5", nargs="+", type=Path, required=True)
    parser.add_argument("--round6", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args(argv)
    round7 = json.loads(arguments.round7.read_text())
    prior = []
    for path in arguments.round5:
        prior.extend(load_round5(path))
    prior.extend(load_round6(arguments.round6))
    prior_descriptors = [descriptor(entry["coordinates"]) for entry in prior]
    records = []
    for run_index, run in enumerate(round7["runs"]):
        here = descriptor(
            run["final_five_dimensional"]["coordinates_float64"]
        )
        candidates = []
        for entry, old in zip(prior, prior_descriptors):
            if entry["n"] != run["n"]:
                continue
            difference = here - old
            candidates.append(
                (
                    float(np.sqrt(np.mean(difference * difference))),
                    float(np.max(np.abs(difference))),
                    entry,
                )
            )
        rms, maximum_difference, nearest = min(
            candidates, key=lambda item: item[0]
        )
        records.append(
            {
                "round7_run": run_index,
                "n": run["n"],
                "seed": run["seed"],
                "origin": run["origin"],
                "round7_maximum": run["final_five_dimensional"]["maximum"],
                "nearest_prior_label": nearest["label"],
                "nearest_prior_maximum": nearest["maximum"],
                "sorted_pair_descriptor_rms": rms,
                "sorted_pair_descriptor_l_infinity": maximum_difference,
                "same_numerical_distance_distribution_1e-7": (
                    maximum_difference <= 1e-7
                ),
            }
        )
    summary = {}
    for n in (41, 42, 43, 44):
        current = [record for record in records if record["n"] == n]
        summary[str(n)] = {
            "paths": len(current),
            "same_prior_distribution_count_1e-7": sum(
                record["same_numerical_distance_distribution_1e-7"]
                for record in current
            ),
            "minimum_descriptor_rms": min(
                record["sorted_pair_descriptor_rms"] for record in current
            ),
            "best_round7_maximum": min(
                record["round7_maximum"] for record in current
            ),
        }
    output = {
        "status": STATUS,
        "statement": (
            "Prior artifacts were read only after the round-7 portfolio "
            "was complete; they were never search seeds or objectives."
        ),
        "input_hashes": {
            "round7": {
                "path": str(arguments.round7),
                "sha256": sha256(arguments.round7),
            },
            "round5": [
                {"path": str(path), "sha256": sha256(path)}
                for path in arguments.round5
            ],
            "round6": {
                "path": str(arguments.round6),
                "sha256": sha256(arguments.round6),
            },
        },
        "records": records,
        "summary": summary,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    with arguments.output.open("w") as stream:
        json.dump(output, stream, indent=2, sort_keys=True)
        stream.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
