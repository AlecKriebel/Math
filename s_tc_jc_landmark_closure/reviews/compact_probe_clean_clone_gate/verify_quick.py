#!/usr/bin/env python3
"""Fast integrity and theorem-summary gate for precomputed compact replay."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def sha256(path: Path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_manifest():
    rows = []
    for line in (HERE / "MANIFEST.sha256").read_text().splitlines():
        if not line.strip():
            continue
        digest, relative = line.split("  ", 1)
        path = HERE / relative
        assert path.is_file(), relative
        assert sha256(path) == digest, relative
        rows.append(relative)
    assert len(rows) == len(set(rows))
    assert "MANIFEST.sha256" not in rows
    return len(rows)


def main():
    inputs = json.loads((HERE / "TRACKED_INPUTS.json").read_text())
    assert inputs["status"] == "VERIFIED"
    assert inputs["input_count"] == 50
    semantic = json.loads((HERE / "certificates" /
                           "compact_only_semantic_replay.json").read_text())
    assert semantic["status"] == "VERIFIED"
    by_name = {row["family"]: row for row in semantic["families"]}
    assert by_name["n3"]["path_inventory_count"] == 144
    assert by_name["n3"]["total_relations"] == 101148
    assert by_name["n3"]["classification_counts"] == {
        "generic_polynomial_separation": 90008,
        "labelled_isomorphism": 9676,
        "ordinary_T": 840,
        "strict_open_cube_separation": 624,
    }
    assert by_name["theta2_n4"]["path_inventory_count"] == 132
    assert by_name["theta2_n4"]["total_relations"] == 168582
    assert by_name["theta2_n4"]["classification_counts"] == {
        "generic_polynomial_separation": 153072,
        "labelled_isomorphism": 15510,
    }
    assert semantic["totals"] == {
        "all_four_classes_exercised": True,
        "maximum_probe_port_count": 10,
        "paths": 276,
        "relations": 269730,
    }
    assert semantic["implementation"]["uses_verbose_probe_extension_streams"] is False
    assert semantic["implementation"]["imports_primary_code"] is False
    mutations = json.loads((HERE / "certificates" / "mutation_tests.json").read_text())
    assert mutations["status"] == "VERIFIED"
    assert mutations["outer_hashes_bypassed"] is True
    assert len(mutations["mutations"]) == 9
    assert all(row["rejected"] for row in mutations["mutations"])
    manifest_rows = verify_manifest()
    print(json.dumps({"status": "VERIFIED", "manifest_rows": manifest_rows,
                      "paths": 276, "relations": 269730,
                      "mutations_rejected": 9}, sort_keys=True))


if __name__ == "__main__":
    main()
