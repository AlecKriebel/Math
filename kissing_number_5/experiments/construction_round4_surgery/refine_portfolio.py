#!/usr/bin/env python3
"""Apply direct epigraph SQP to every stored surgery candidate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from . import contact_surgery


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    arguments = parser.parse_args()
    payload = json.loads(arguments.input.read_text())
    for run in payload["runs"]:
        points = np.asarray(run["coordinates"], dtype=float)
        points, history = contact_surgery.epigraph_refine(points)
        run["postprocessed_epigraph_slsqp"] = history
        run["coordinates"] = points.tolist()
        run["diagnostics"] = contact_surgery.diagnostics(points)
        print(
            run["n"],
            run["seed"],
            run["diagnostics"]["maximum_inner_product"],
            flush=True,
        )
    arguments.output.write_text(json.dumps(payload, indent=2) + "\n")


if __name__ == "__main__":
    main()
