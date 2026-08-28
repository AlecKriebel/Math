#!/usr/bin/env python3
"""Demonstrate that -O erases a load-bearing target-zero certificate check."""
from __future__ import annotations

import importlib.util
import json
import pathlib
import sys


ATLAS = pathlib.Path(__file__).resolve().parents[3] / (
    "execution/k2p_principal_d_plus_submission_referee/"
    "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
)


def load_atlas():
    spec = importlib.util.spec_from_file_location("optimized_probe_atlas", ATLAS)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {ATLAS}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    atlas = load_atlas()
    # A deliberately faulty kernel provider returns a non-kernel unit vector.
    # Source and target are identical, so no valid separator can exist.
    atlas.kernel_sparse_columns_fast = lambda columns: (
        (1,) + (0,) * (len(columns) - 1),
    )
    outputs = tuple(
        (
            (
                ((0, 1, coordinate + 1),),
                ((0, 1),),
            ),
        )
        for coordinate in range(len(atlas.orbit_assignments(4)))
    )
    descriptor = atlas.MapDescriptor(4, 0, 1, outputs, ())
    try:
        certificate = atlas.quadratic_separator_fast(descriptor, descriptor)
    except AssertionError:
        print(json.dumps({
            "optimized": not __debug__,
            "outcome": "invalid_target_certificate_rejected_by_assert",
        }, sort_keys=True))
        return
    if certificate is None:
        raise SystemExit("probe failed to exercise the target-zero check")
    print(json.dumps({
        "optimized": not __debug__,
        "outcome": "invalid_separator_returned_for_identical_maps",
        "certificate_degree": certificate["degree"],
        "source_nonzero_terms": certificate["source_nonzero_terms"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
