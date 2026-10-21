#!/usr/bin/env python3
"""Replay mathematical components only; no external PDFs or account access.

Source-custody helpers remain historical optional tools. This wrapper imports
the sealed math code on the runner's scratch copy and emits complete records.
It does not assert that missing third-party papers have been inspected.
"""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys

if not __debug__ or os.environ.get("PYTHONOPTIMIZE"):
    raise RuntimeError("Run without Python optimization")

ROOT = Path(__file__).resolve().parent.parent


def module(family, filename):
    name = "supplied_primary_" + family
    path = ROOT / "reviews" / family / filename
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    sys.modules[name] = loaded
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(loaded)
    return loaded, path.parent


def main():
    source06, _ = module("priority06_zemyan2003", "checks.py")
    results = {"priority06_zemyan2003": {
        "exact_controls": source06.exact_controls(),
        "interval_controls": source06.interval_controls(),
    }}
    _, p07 = module("priority07_zemyan_bounds", "checks.py")
    results["priority07_zemyan_bounds"] = json.loads((p07 / "CHECKS.json").read_text())
    source08, _ = module("priority08_radial_extrema", "exact_checks.py")
    results["priority08_radial_extrema"] = source08.out
    source09, _ = module("priority09_commentary_citations", "exact_checks.py")
    results["priority09_commentary_citations"] = source09.result
    source10, _ = module("priority10_adversary", "exact_checks.py")
    results["priority10_adversary"] = source10.record
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
