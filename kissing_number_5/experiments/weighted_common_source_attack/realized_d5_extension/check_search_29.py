#!/usr/bin/env python3
"""Recompute all numerical diagnostics stored by ``search_29.py``.

This checker detects serialization or bookkeeping errors.  It deliberately
does not call a floating-point result an exact certificate.
"""

import argparse
import json
from pathlib import Path
import sys

import numpy as np

import search_29


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(path):
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    require(data.get("schema") == search_29.SCHEMA, "schema mismatch")
    require(data.get("status") == search_29.STATUS, "status mismatch")
    best = data.get("best")
    require(type(best) is dict, "missing best record")
    coordinates = np.asarray(best.get("coordinates"), dtype=float)
    require(coordinates.shape == (29, 5), "coordinate shape mismatch")
    require(np.all(np.isfinite(coordinates)), "non-finite coordinate")
    recomputed = search_29.diagnostics(coordinates)
    recorded = best.get("diagnostics")
    require(type(recorded) is dict, "missing recorded diagnostics")
    for key in (
        "maximum",
        "maximum_extension_pair",
        "maximum_support_pair",
        "minimum_inner_product",
        "norm_error",
        "frame_potential",
        "centroid_squared_norm",
        "v_trace",
    ):
        require(
            abs(float(recorded[key]) - float(recomputed[key])) <= 5e-13,
            "diagnostic mismatch for %s" % key,
        )
    require(
        recomputed["maximum"] > 0.5,
        "this checker is only labelled for an unsuccessful numerical search",
    )
    print(
        json.dumps(
            {
                "status": search_29.STATUS,
                "recomputed_maximum": recomputed["maximum"],
                "gap_above_one_half": recomputed["maximum"] - 0.5,
                "norm_error": recomputed["norm_error"],
            },
            sort_keys=True,
        )
    )


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parent / "search_29_result.json",
    )
    args = parser.parse_args(argv)
    check(args.path)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, TypeError) as exc:
        print("CHECK FAILED: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
