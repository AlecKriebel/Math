#!/usr/bin/env python3
"""Verify that the import-only Omega shim equals the frozen source literal."""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
FROZEN = (
    HERE.parent
    / "frozen_input"
    / "historical"
    / "src"
    / "probe_four_leaf_jc_atlas.py"
)
SHIM = HERE / "probe_four_leaf_jc_atlas.py"


def frozen_literal() -> tuple[tuple[int, ...], ...]:
    tree = ast.parse(FROZEN.read_text(encoding="utf-8"), filename=str(FROZEN))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(
            isinstance(target, ast.Name) and target.id == "JC_REPRESENTATIVES"
            for target in node.targets
        ):
            value = ast.literal_eval(node.value)
            return tuple(tuple(int(entry) for entry in row) for row in value)
    raise AssertionError("JC_REPRESENTATIVES literal not found in frozen source")


def shim_literal() -> tuple[
    tuple[tuple[int, ...], ...], dict[tuple[int, ...], int]
]:
    spec = importlib.util.spec_from_file_location("omega_orbit_shim", SHIM)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load Omega orbit shim")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return tuple(tuple(row) for row in module.JC_REPRESENTATIVES), module.ORBIT_INDEX


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    frozen = frozen_literal()
    shim, orbit_index = shim_literal()
    assert frozen == shim
    assert len(shim) == 15 and len(set(shim)) == 15
    assert all(len(row) == 4 and row[0] ^ row[1] ^ row[2] ^ row[3] == 0 for row in shim)
    assert len(orbit_index) == 64
    assert set(orbit_index.values()) == set(range(15))
    print(
        json.dumps(
            {
                "frozen_source_sha256": digest(FROZEN),
                "orbit_assignments": len(orbit_index),
                "representatives": len(shim),
                "shim_sha256": digest(SHIM),
                "status": "VERIFIED",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
