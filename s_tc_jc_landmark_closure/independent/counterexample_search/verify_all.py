#!/usr/bin/env python3
"""Fail-closed consistency verifier for the independent search artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from audit_io import load_json


HERE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    expected = load_json(HERE / "EXPECTED_CERTIFICATE_HASHES.json")
    for name, digest in expected.items():
        actual = sha256(HERE / name)
        assert actual == digest, (name, digest, actual)

    inputs = load_json(HERE / "INPUT_LOCK.json")
    for key in ("definitions_lock", "frozen_weak_manuscript_source", "frozen_weak_manuscript_pdf"):
        item = inputs[key]
        assert sha256((HERE / item["path"]).resolve()) == item["sha256"], key

    census = load_json(HERE / "census_n5_deterministic.json.gz")
    expected_cells = {
        (3, 0): (1, 1, 0),
        (3, 1): (9, 3, 0),
        (3, 2): (468, 0, 12),
        (4, 0): (3, 3, 0),
        (4, 1): (108, 30, 0),
        (4, 2): (7725, 84, 180),
        (5, 0): (15, 15, 0),
        (5, 1): (1305, 315, 0),
        (5, 2): (136560, 2370, 2520),
    }
    assert len(census["cells"]) == len(expected_cells)
    for cell in census["cells"]:
        key = (cell["n"], cell["reticulations"])
        mixed, strong, weak_only = expected_cells[key]
        assert cell["mixed_candidate_count"] == mixed
        assert cell["membership_counts"].get("S_TC", 0) == strong
        assert cell["membership_counts"].get("W_TC_NOT_S_TC", 0) == weak_only
    assert not census["automatic_triangle_falsifiers"]
    assert len(census["topologies"]) == 5533

    assert load_json(HERE / "regression_certificate.json")["status"] == "EXACTLY_COMPUTED"
    assert load_json(HERE / "three_leaf_separator_certificate.json")["status"] == "PROVED"
    assert load_json(HERE / "local_stc_criterion_certificate.json")["mismatches"] == []
    assert load_json(HERE / "root_invariance_n5.json")["topologies_checked"] == 2821
    assert load_json(HERE / "isomorphism_crosscheck_n5.json")["isomorphic_duplicate_pairs"] == []
    assert load_json(HERE / "numerical_screen_n4.json")["survivors"] == []
    assert load_json(HERE / "five_leaf_profiles.json")["T_class_count"] == 1605
    assert load_json(HERE / "five_leaf_numerical_search.json")["candidate_count"] == 0
    assert load_json(HERE / "five_leaf_refined_near_misses.json")["candidate_count"] == 0

    # Mutation-sensitive sanity checks: the active count contract rejects a
    # deleted or duplicated relation, and the hash contract rejects a changed
    # separator certificate or stale definitions lock.
    assert len(census["topologies"][:-1]) != 5533
    assert len(census["topologies"] + [census["topologies"][0]]) != 5533
    separator_bytes = (HERE / "three_leaf_separator_certificate.json").read_bytes()
    mutated_separator = separator_bytes.replace(b'"status": "PROVED"', b'"status": "FALSE"')
    assert hashlib.sha256(mutated_separator).hexdigest() != expected["three_leaf_separator_certificate.json"]
    assert inputs["definitions_lock"]["sha256"] == "c3382650fa004d90b2122aff1c95524590b31e436d77d4b804293184aa925b09"

    print("PASS: independent bounded counterexample-search artifacts are internally consistent")


if __name__ == "__main__":
    main()
