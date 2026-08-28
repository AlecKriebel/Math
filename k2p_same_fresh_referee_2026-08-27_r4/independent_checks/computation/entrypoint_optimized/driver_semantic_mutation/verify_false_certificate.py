#!/usr/bin/env python3
"""Recompute both pullbacks of the optimized-mode mutation certificate."""
from __future__ import annotations

import importlib.util
import json
import pathlib
import pickle
import sys


HERE = pathlib.Path(__file__).resolve().parent
REVIEW_ROOT = HERE.parents[3]
SOURCE_PORTABLE = REVIEW_ROOT / (
    "isolated/k2p_principal_d_plus_submission_referee/"
    "package/referee/k2p_offline_sweep_portable"
)


def main() -> None:
    atlas_path = HERE / "mutation_payload/k2p_atlas_core.mutated.py"
    spec = importlib.util.spec_from_file_location("k2p_atlas_core", atlas_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {atlas_path}")
    atlas = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = atlas
    spec.loader.exec_module(atlas)
    with (SOURCE_PORTABLE / "atlas/descriptors_4.pkl").open("rb") as handle:
        _sources, _targets, rows, source_descriptors, cache = pickle.load(handle)
    with (SOURCE_PORTABLE / "atlas/rank_certs_4.pkl").open("rb") as handle:
        ranks = pickle.load(handle)
    source = source_descriptors[0]
    source_rank = ranks[source]["rank"]
    classes = []
    seen = set()
    for raw in rows[0]:
        target = cache[raw]
        if ranks[target]["rank"] < source_rank or target in seen:
            continue
        seen.add(target)
        classes.append(target)
    target = classes[0]
    record_path = HERE / "optimized_run/source_0/records/class_000000.json"
    certificate = json.loads(record_path.read_text())["certificate"]
    block = tuple(tuple(pair) for pair in certificate["coordinate_pairs"])
    coefficients = certificate["coefficients"]

    def pullback(descriptor):
        outputs = atlas.output_sparse_polynomials(descriptor)
        columns = [atlas.sparse_mul(outputs[left], outputs[right]) for left, right in block]
        return atlas.sparse_lincomb(columns, coefficients)

    target_pullback = pullback(target)
    source_pullback = pullback(source)
    print(json.dumps({
        "certificate_claims_target_zero": True,
        "observed_target_pullback_zero": not target_pullback,
        "observed_target_pullback_term_count": len(target_pullback),
        "observed_source_pullback_nonzero": bool(source_pullback),
        "observed_source_pullback_term_count": len(source_pullback),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
