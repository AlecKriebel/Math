#!/usr/bin/env python3
"""Verify the exact input lock without requiring a .git directory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]


def sha256(path: Path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    lock = json.loads((HERE / "TRACKED_INPUTS.json").read_text())
    assert lock["status"] == "VERIFIED"
    assert lock["forbidden_verbose_probe_extension_inputs"] == []
    assert lock["input_count"] == len(lock["inputs"])
    seen = set()
    forbidden = []
    for row in lock["inputs"]:
        path_text = row["path"]
        assert path_text not in seen
        seen.add(path_text)
        path = REPO / path_text
        assert path.is_file(), path_text
        assert path.stat().st_size == int(row["bytes"]), path_text
        assert sha256(path) == row["sha256"], path_text
        if "probe_extension_" in path.name and "compact_probe_" not in path.name:
            forbidden.append(path_text)
    assert not forbidden, forbidden
    print(json.dumps({"status": "VERIFIED", "inputs": len(seen),
                      "git_not_required": True,
                      "forbidden_verbose_inputs": forbidden}, sort_keys=True))


if __name__ == "__main__":
    main()
