#!/usr/bin/env python3
"""Deterministically polish the best general UNTF saved by optimize_untf."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import optimize_untf as optimizer


def main() -> None:
    path = optimizer.RESULT_PATH
    data = json.loads(path.read_text())
    frame = np.asarray(data["best_general"]["coordinates"], dtype=float)
    stages = [
        {"beta_schedule": [1280, 2560, 5120], "iterations": 500},
        {"beta_schedule": [2560, 5120, 10240], "iterations": 500},
        {
            "beta_schedule": [5120, 10240, 20480, 40960],
            "iterations": 1000,
        },
    ]
    records = []
    for stage in stages:
        frame = optimizer.optimize_general(
            frame,
            stage["beta_schedule"],
            stage["iterations"],
        )
        diagnostics = optimizer.frame_diagnostics(frame)
        records.append({**stage, **diagnostics})
        print(
            f"schedule={stage['beta_schedule']} "
            f"max={diagnostics['maximum_inner_product']:.12f}",
            flush=True,
        )
    data["polishing"] = records
    data["best_general"] = {
        **optimizer.frame_diagnostics(frame),
        "coordinates": frame.tolist(),
    }
    path.write_text(json.dumps(data, indent=2) + "\n")
    print(f"updated {path}")


if __name__ == "__main__":
    main()
